"""Control de la ejecución de Python y comprobación de los archivos generados."""

from __future__ import annotations

import ast
import ctypes
import json
import os
import site
import subprocess
import sys
import threading
import time
from ctypes import wintypes
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .configuracion import ConfiguracionExperimento
from .ejecucion import ContextoEjecucion
from .errores import CapaComunError
from .utilidades import sha256_archivo


MODULOS_TERCEROS_PERMITIDOS = {
    "pandas",
    "numpy",
    "scipy",
    "matplotlib",
    "seaborn",
    "openpyxl",
}
MODULOS_PROHIBIDOS = {
    "asyncio",
    "builtins",
    "ctypes",
    "ftplib",
    "getpass",
    "glob",
    "http",
    "importlib",
    "inspect",
    "marshal",
    "multiprocessing",
    "os",
    "pathlib",
    "pickle",
    "pip",
    "platform",
    "requests",
    "resource",
    "secrets",
    "shelve",
    "shutil",
    "signal",
    "site",
    "smtplib",
    "socket",
    "sqlite3",
    "subprocess",
    "sys",
    "tarfile",
    "tempfile",
    "urllib",
    "venv",
    "webbrowser",
    "winreg",
    "zipfile",
}
LLAMADAS_PROHIBIDAS = {
    "breakpoint",
    "compile",
    "delattr",
    "eval",
    "exec",
    "getattr",
    "globals",
    "help",
    "input",
    "locals",
    "setattr",
    "vars",
    "__import__",
}
ATRIBUTOS_PROHIBIDOS = {
    "environ",
    "getenv",
    "popen",
    "read_pickle",
    "to_pickle",
    "system",
}


class ErrorCodigo(CapaComunError):
    def __init__(self, code: str, message: str, retryable: bool = False) -> None:
        super().__init__(message)
        self.code = code
        self.retryable = retryable


class _ValidadorCodigo(ast.NodeVisitor):
    """Revisa las importaciones, nombres y llamadas del código antes de ejecutarlo."""
    def __init__(self) -> None:
        self.errores: list[str] = []
        self.estandar = set(getattr(sys, "stdlib_module_names", ()))

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self._comprobar_modulo(alias.name, node.lineno)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.level:
            self.errores.append(f"Línea {node.lineno}: no se permiten importaciones relativas")
        elif node.module:
            self._comprobar_modulo(node.module, node.lineno)
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> None:
        if node.id.startswith("__"):
            self.errores.append(f"Línea {node.lineno}: nombre interno no autorizado")
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        if node.attr.startswith("__") or node.attr in ATRIBUTOS_PROHIBIDOS:
            self.errores.append(
                f"Línea {node.lineno}: atributo no autorizado {node.attr}"
            )
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Name) and node.func.id in LLAMADAS_PROHIBIDAS:
            self.errores.append(
                f"Línea {node.lineno}: llamada no autorizada {node.func.id}"
            )
        self.generic_visit(node)

    def _comprobar_modulo(self, modulo: str, linea: int) -> None:
        raiz = modulo.split(".", 1)[0]
        if raiz in MODULOS_PROHIBIDOS:
            self.errores.append(f"Línea {linea}: el módulo {raiz} no está autorizado")
        elif raiz not in MODULOS_TERCEROS_PERMITIDOS and raiz not in self.estandar:
            self.errores.append(
                f"Línea {linea}: el módulo {raiz} no pertenece al entorno congelado"
            )


def validar_codigo(codigo: str) -> None:
    """Comprueba la sintaxis y las restricciones del código recibido."""
    if not isinstance(codigo, str) or not codigo.strip():
        raise ErrorCodigo("INVALID_ARGUMENT", "code debe ser una cadena no vacía")
    try:
        arbol = ast.parse(codigo, filename="<execute_python>", mode="exec")
    except SyntaxError as exc:
        raise ErrorCodigo(
            "INVALID_ARGUMENT",
            f"Código Python inválido en la línea {exc.lineno}: {exc.msg}",
        ) from exc
    validador = _ValidadorCodigo()
    validador.visit(arbol)
    if validador.errores:
        raise ErrorCodigo("ACCESS_DENIED", validador.errores[0])


@dataclass(frozen=True, slots=True)
class ResultadoProcesoPython:
    execution_id: str
    exit_status: str
    stdout: str
    stderr: str
    truncated: bool
    files_created: tuple[Mapping[str, Any], ...]
    files_modified: tuple[Mapping[str, Any], ...]
    files_deleted: tuple[str, ...]
    duration_seconds: float
    error_code: str | None
    error_message: str | None
    retryable: bool


class _IO_COUNTERS(ctypes.Structure):
    _fields_ = [
        ("ReadOperationCount", ctypes.c_ulonglong),
        ("WriteOperationCount", ctypes.c_ulonglong),
        ("OtherOperationCount", ctypes.c_ulonglong),
        ("ReadTransferCount", ctypes.c_ulonglong),
        ("WriteTransferCount", ctypes.c_ulonglong),
        ("OtherTransferCount", ctypes.c_ulonglong),
    ]


class _JOBOBJECT_BASIC_LIMIT_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("PerProcessUserTimeLimit", ctypes.c_longlong),
        ("PerJobUserTimeLimit", ctypes.c_longlong),
        ("LimitFlags", wintypes.DWORD),
        ("MinimumWorkingSetSize", ctypes.c_size_t),
        ("MaximumWorkingSetSize", ctypes.c_size_t),
        ("ActiveProcessLimit", wintypes.DWORD),
        ("Affinity", ctypes.c_size_t),
        ("PriorityClass", wintypes.DWORD),
        ("SchedulingClass", wintypes.DWORD),
    ]


class _JOBOBJECT_EXTENDED_LIMIT_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BasicLimitInformation", _JOBOBJECT_BASIC_LIMIT_INFORMATION),
        ("IoInfo", _IO_COUNTERS),
        ("ProcessMemoryLimit", ctypes.c_size_t),
        ("JobMemoryLimit", ctypes.c_size_t),
        ("PeakProcessMemoryUsed", ctypes.c_size_t),
        ("PeakJobMemoryUsed", ctypes.c_size_t),
    ]


class _TrabajoWindows:
    """Aplica los límites de memoria y número de procesos mediante Windows."""
    JOB_OBJECT_LIMIT_ACTIVE_PROCESS = 0x00000008
    JOB_OBJECT_LIMIT_PROCESS_MEMORY = 0x00000100
    JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000
    JobObjectExtendedLimitInformation = 9

    def __init__(self, memoria_maxima: int) -> None:
        if os.name != "nt":
            raise ErrorCodigo(
                "INTERNAL_ERROR",
                "El aislamiento de recursos requiere Windows",
            )
        self.kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        self.kernel32.CreateJobObjectW.restype = wintypes.HANDLE
        self.kernel32.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
        self.kernel32.SetInformationJobObject.restype = wintypes.BOOL
        self.kernel32.AssignProcessToJobObject.restype = wintypes.BOOL
        self.kernel32.TerminateJobObject.restype = wintypes.BOOL
        self.kernel32.CloseHandle.restype = wintypes.BOOL
        self.handle = self.kernel32.CreateJobObjectW(None, None)
        if not self.handle:
            raise ErrorCodigo("INTERNAL_ERROR", "No puede crearse el límite de proceso")
        informacion = _JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
        informacion.BasicLimitInformation.LimitFlags = (
            self.JOB_OBJECT_LIMIT_ACTIVE_PROCESS
            | self.JOB_OBJECT_LIMIT_PROCESS_MEMORY
            | self.JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
        )
        informacion.BasicLimitInformation.ActiveProcessLimit = 1
        informacion.ProcessMemoryLimit = memoria_maxima
        correcto = self.kernel32.SetInformationJobObject(
            self.handle,
            self.JobObjectExtendedLimitInformation,
            ctypes.byref(informacion),
            ctypes.sizeof(informacion),
        )
        if not correcto:
            self.cerrar()
            raise ErrorCodigo("INTERNAL_ERROR", "No pueden configurarse los límites de proceso")

    def asignar(self, proceso: subprocess.Popen[str]) -> None:
        """Asocia el proceso de Python con los límites configurados."""
        correcto = self.kernel32.AssignProcessToJobObject(
            self.handle,
            wintypes.HANDLE(int(proceso._handle)),
        )
        if not correcto:
            raise ErrorCodigo("INTERNAL_ERROR", "No puede aislarse el proceso de Python")

    def terminar(self) -> None:
        """Ordena la terminación de los procesos asociados."""
        if self.handle:
            self.kernel32.TerminateJobObject(self.handle, 1)

    def cerrar(self) -> None:
        """Libera el recurso de Windows utilizado para controlar el proceso."""
        if getattr(self, "handle", None):
            self.kernel32.CloseHandle(self.handle)
            self.handle = None


class EjecutorPython:
    """Ejecuta el código en un proceso nuevo e identifica los archivos creados, modificados o eliminados."""

    def __init__(
        self,
        configuracion: ConfiguracionExperimento,
        contexto: ContextoEjecucion,
    ) -> None:
        self.configuracion = configuracion
        self.contexto = contexto
        self._bloqueo = threading.Lock()

    def ejecutar(
        self,
        execution_id: str,
        codigo: str,
        timeout_seconds: float,
    ) -> ResultadoProcesoPython:
        """Valida el código e impide ejecutar dos llamadas de Python simultáneamente."""
        validar_codigo(codigo)
        if timeout_seconds <= 0:
            raise ErrorCodigo("TIMEOUT", "No queda tiempo de Python disponible")
        if not self._bloqueo.acquire(blocking=False):
            raise ErrorCodigo("ACCESS_DENIED", "Ya existe una llamada de Python activa")
        try:
            return self._ejecutar_bloqueado(execution_id, codigo, timeout_seconds)
        finally:
            self._bloqueo.release()

    def _ejecutar_bloqueado(
        self,
        execution_id: str,
        codigo: str,
        timeout_seconds: float,
    ) -> ResultadoProcesoPython:
        """Inicia el proceso, recoge su resultado y comprueba los archivos afectados."""
        entrada_hash_inicial = sha256_archivo(self.contexto.dataset.ruta_entrada)
        protegidos = self._hashes_protegidos()
        invocacion = self.contexto.directorio_temporal / f"_runtime_{execution_id}.json"
        configuracion_worker = {
            "input_path": str(self.contexto.dataset.ruta_entrada),
            "output_dir": str(self.contexto.directorio_salida),
            "figures_dir": str(self.contexto.directorio_figuras),
            "temporary_dir": str(self.contexto.directorio_temporal),
            "run_id": self.contexto.run_id,
            "dataset_id": self.contexto.dataset.dataset_id,
            "experiment_seed": self.configuracion.datos["security"]["experiment_seed"],
            "code": codigo,
        }
        invocacion.write_text(
            json.dumps(configuracion_worker, ensure_ascii=False, allow_nan=False),
            encoding="utf-8",
        )
        antes = self._snapshot()
        inicio = time.perf_counter()
        stdout = ""
        stderr = ""
        truncado = False
        estado = "error"
        codigo_error: str | None = None
        mensaje_error: str | None = None
        retryable = False
        trabajo: _TrabajoWindows | None = None
        proceso: subprocess.Popen[str] | None = None
        try:
            entorno = self._entorno_minimo()
            worker = Path(__file__).with_name("worker_python.py")
            ejecutable_base = getattr(sys, "_base_executable", sys.executable)
            proceso = subprocess.Popen(
                [ejecutable_base, str(worker), str(invocacion)],
                cwd=self.contexto.directorio_salida,
                env=entorno,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
            trabajo = _TrabajoWindows(
                self.configuracion.datos["tools"]["execute_python"]["memory_max_bytes"]
            )
            trabajo.asignar(proceso)
            salida_stdout: dict[str, Any] = {}
            salida_stderr: dict[str, Any] = {}
            limite_stdout = self.configuracion.datos["tools"]["execute_python"][
                "stdout_max_characters"
            ]
            limite_stderr = self.configuracion.datos["tools"]["execute_python"][
                "stderr_max_characters"
            ]
            hilo_stdout = threading.Thread(
                target=self._leer_stream,
                args=(proceso.stdout, limite_stdout, salida_stdout),
                daemon=True,
            )
            hilo_stderr = threading.Thread(
                target=self._leer_stream,
                args=(proceso.stderr, limite_stderr, salida_stderr),
                daemon=True,
            )
            hilo_stdout.start()
            hilo_stderr.start()
            try:
                retorno = proceso.wait(timeout=timeout_seconds)
            except subprocess.TimeoutExpired:
                trabajo.terminar()
                proceso.wait(timeout=10)
                retorno = None
            hilo_stdout.join(timeout=10)
            hilo_stderr.join(timeout=10)
            stdout = salida_stdout.get("text", "")
            stderr = salida_stderr.get("text", "")
            truncado = bool(
                salida_stdout.get("truncated", False)
                or salida_stderr.get("truncated", False)
            )
            if retorno is None:
                estado = "timeout"
                codigo_error = "TIMEOUT"
                mensaje_error = "La ejecución de Python ha superado el tiempo máximo"
                retryable = True
            elif retorno == 0:
                estado = "success"
            else:
                estado = "error"
                acceso_denegado = any(
                    linea.lstrip().startswith(("PermissionError:", "ImportError:"))
                    for linea in stderr.splitlines()
                )
                codigo_error = "ACCESS_DENIED" if acceso_denegado else "EXECUTION_ERROR"
                mensaje_error = stderr.strip() or "El proceso de Python terminó con error"
        except ErrorCodigo:
            if proceso is not None and proceso.poll() is None:
                proceso.kill()
                proceso.wait(timeout=10)
            raise
        except Exception as exc:
            if proceso is not None and proceso.poll() is None:
                proceso.kill()
                proceso.wait(timeout=10)
            estado = "error"
            codigo_error = "INTERNAL_ERROR"
            mensaje_error = f"No puede ejecutarse el proceso aislado: {type(exc).__name__}"
        finally:
            if trabajo is not None:
                trabajo.cerrar()
            try:
                invocacion.unlink()
            except OSError:
                pass

        despues = self._snapshot()
        creados, modificados, eliminados = self._comparar(antes, despues)
        errores_seguridad = self._comprobar_integridad(
            entrada_hash_inicial,
            protegidos,
            despues,
            eliminados,
        )
        if errores_seguridad:
            estado = "error"
            codigo_error = "ACCESS_DENIED"
            mensaje_error = errores_seguridad[0]
            retryable = False
        duracion = max(time.perf_counter() - inicio, 0.0)
        return ResultadoProcesoPython(
            execution_id=execution_id,
            exit_status=estado,
            stdout=stdout,
            stderr=stderr,
            truncated=truncado,
            files_created=tuple(creados),
            files_modified=tuple(modificados),
            files_deleted=tuple(eliminados),
            duration_seconds=duracion,
            error_code=codigo_error,
            error_message=mensaje_error,
            retryable=retryable,
        )

    def _entorno_minimo(self) -> dict[str, str]:
        """Prepara las variables de entorno necesarias."""
        entorno = {
            "PYTHONHASHSEED": str(self.configuracion.datos["security"]["experiment_seed"]),
            "PYTHONNOUSERSITE": "1",
            "PYTHONIOENCODING": "utf-8",
            "MPLBACKEND": "Agg",
            "MPLCONFIGDIR": str(self.contexto.directorio_temporal / "matplotlib"),
            "TEMP": str(self.contexto.directorio_temporal),
            "TMP": str(self.contexto.directorio_temporal),
            "OMP_NUM_THREADS": "1",
            "OPENBLAS_NUM_THREADS": "1",
            "MKL_NUM_THREADS": "1",
            "NUMEXPR_NUM_THREADS": "1",
        }
        for nombre in ("SYSTEMROOT", "WINDIR", "PATH"):
            if nombre in os.environ:
                entorno[nombre] = os.environ[nombre]
        rutas_paquetes = [ruta for ruta in site.getsitepackages() if "site-packages" in ruta]
        if rutas_paquetes:
            entorno["PYTHONPATH"] = os.pathsep.join(rutas_paquetes)
        return entorno

    @staticmethod
    def _leer_stream(stream: Any, maximo: int, resultado: dict[str, Any]) -> None:
        """Recoge el texto producido por el proceso y lo recorta si supera el máximo de caracteres."""
        partes: list[str] = []
        conservados = 0
        truncado = False
        if stream is not None:
            for fragmento in iter(lambda: stream.read(4096), ""):
                restante = maximo - conservados
                if restante > 0:
                    partes.append(fragmento[:restante])
                    conservados += min(len(fragmento), restante)
                if len(fragmento) > restante:
                    truncado = True
            stream.close()
        resultado["text"] = "".join(partes)
        resultado["truncated"] = truncado

    def _snapshot(self) -> dict[str, dict[str, Any]]:
        """Registra el tamaño y el hash de los archivos de la ejecución para detectar cambios posteriores."""
        resultado: dict[str, dict[str, Any]] = {}
        raiz = self.contexto.directorio_salida
        for ruta in sorted(raiz.rglob("*")):
            if ruta.is_symlink():
                raise ErrorCodigo("ACCESS_DENIED", "No se permiten enlaces en la ejecución")
            if not ruta.is_file():
                continue
            relativa = ruta.relative_to(raiz).as_posix()
            if (
                relativa == "trace.jsonl"
                or ruta.name.startswith("_runtime_")
                or relativa.startswith("_temporary/matplotlib/")
            ):
                continue
            resultado[relativa] = {
                "path": relativa,
                "bytes": ruta.stat().st_size,
                "sha256": sha256_archivo(ruta),
            }
        return resultado

    def _hashes_protegidos(self) -> dict[str, str | None]:
        """Obtiene los hashes del plan, el informe y la traza antes de ejecutar código."""
        resultado: dict[str, str | None] = {}
        for nombre in ("plan.md", "report.md", "trace.jsonl"):
            ruta = self.contexto.directorio_salida / nombre
            resultado[nombre] = sha256_archivo(ruta) if ruta.is_file() else None
        return resultado

    @staticmethod
    def _comparar(
        antes: Mapping[str, Mapping[str, Any]],
        despues: Mapping[str, Mapping[str, Any]],
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
        """Identifica los archivos creados, modificados y eliminados."""
        creados = [dict(despues[ruta]) for ruta in sorted(set(despues) - set(antes))]
        modificados = []
        for ruta in sorted(set(antes) & set(despues)):
            if antes[ruta]["sha256"] != despues[ruta]["sha256"]:
                item = dict(despues[ruta])
                item["previous_sha256"] = antes[ruta]["sha256"]
                modificados.append(item)
        eliminados = sorted(set(antes) - set(despues))
        return creados, modificados, eliminados

    def _comprobar_integridad(
        self,
        entrada_hash_inicial: str,
        protegidos: Mapping[str, str | None],
        despues: Mapping[str, Mapping[str, Any]],
        eliminados: list[str],
    ) -> list[str]:
        """Comprueba que se respeten los archivos protegidos y las rutas de salida."""
        errores: list[str] = []
        if entrada_hash_inicial != self.contexto.dataset.sha256:
            errores.append("El dataset no coincidía con el hash congelado antes de ejecutar")
        if sha256_archivo(self.contexto.dataset.ruta_entrada) != entrada_hash_inicial:
            errores.append("El código intentó modificar el dataset original")
        for nombre, hash_anterior in protegidos.items():
            ruta = self.contexto.directorio_salida / nombre
            hash_actual = sha256_archivo(ruta) if ruta.is_file() else None
            if hash_actual != hash_anterior:
                errores.append(f"El código modificó el archivo protegido {nombre}")
        if eliminados:
            errores.append("El código eliminó archivos existentes de la ejecución")
        for relativa in despues:
            partes = Path(relativa).parts
            permitido = (
                relativa in {"prepared_data.csv", "statistics.json", "issues.json"}
                or (
                    len(partes) == 2
                    and partes[0] == "figures"
                    and Path(relativa).suffix.casefold() == ".png"
                )
                or partes[0] == self.contexto.directorio_temporal.name
                or relativa in {"plan.md", "report.md"}
            )
            if not permitido:
                errores.append(f"Se ha creado una ruta no autorizada: {relativa}")
        return errores
