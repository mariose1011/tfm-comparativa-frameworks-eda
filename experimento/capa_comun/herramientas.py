"""Herramientas comunes para inspeccionar datos, ejecutar Python, consultar archivos y comprobar resultados."""

from __future__ import annotations

import copy
import json
import math
import random
import time
from datetime import date, datetime, time as hora
from decimal import Decimal
from pathlib import Path
from typing import Any, Mapping

import numpy as np
import pandas as pd

from .configuracion import ConfiguracionExperimento
from .ejecucion import ContextoEjecucion
from .ejecutor_python import EjecutorPython, ErrorCodigo, ResultadoProcesoPython
from .errores import CapaComunError
from .lectura import ErrorConsulta, LectorResultados
from .limites import ControlLimites
from .traza import EscritorTraza
from .utilidades import sha256_archivo
from .validacion import ValidadorSalidas


ESQUEMA_INSPECT_DATASET = {
    "type": "function",
    "name": "inspect_dataset",
    "description": (
        "Devuelve una inspección determinista y de solo lectura del dataset "
        "asociado a la ejecución. No admite parámetros."
    ),
    "parameters": {
        "type": "object",
        "properties": {},
        "additionalProperties": False,
    },
    "strict": True,
}
ESQUEMA_EXECUTE_PYTHON = {
    "type": "function",
    "name": "execute_python",
    "description": (
        "Ejecuta código Python para el EDA en un proceso limpio, sin red y con "
        "lecturas y escrituras limitadas a la ejecución actual. El entorno ya "
        "inyecta INPUT_PATH, OUTPUT_DIR, FIGURES_DIR, RUN_ID, DATASET_ID y "
        "EXPERIMENT_SEED. También precarga pd, np, scipy, plt, sns, openpyxl, "
        "json, csv, math, statistics, datetime, decimal, itertools, random, re, "
        "warnings y Counter. Utiliza directamente esos nombres, sin importar "
        "módulos para descubrir rutas o inspeccionar el entorno. Lee el dataset "
        "desde INPUT_PATH con pandas según su formato. Escribe únicamente "
        "prepared_data.csv, statistics.json e issues.json dentro de OUTPUT_DIR, "
        "y figuras PNG dentro de FIGURES_DIR. No utilices os, pathlib, glob, "
        "globals, locals, vars ni atributos internos. Cada llamada empieza sin "
        "variables de memoria de llamadas anteriores, aunque conserva los "
        "archivos autorizados ya creados."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "purpose": {
                "type": "string",
                "minLength": 1,
                "description": "Objetivo analítico concreto de esta ejecución de código.",
            },
            "code": {
                "type": "string",
                "minLength": 1,
                "description": (
                    "Código Python completo que usa las variables y bibliotecas "
                    "ya inyectadas. No debe buscar ni inventar rutas."
                ),
            },
        },
        "required": ["purpose", "code"],
        "additionalProperties": False,
    },
    "strict": True,
}
ESQUEMA_READ_OUTPUT = {
    "type": "function",
    "name": "read_output",
    "description": (
        "Consulta de forma controlada los resultados de la ejecución actual. "
        "Combinaciones permitidas: plan y report admiten summary, full, section "
        "y next. statistics e issues admiten summary, full, id y next. "
        "prepared_data solo admite summary. figures admite summary e id."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "artifact": {
                "type": "string",
                "description": (
                    "Nombre lógico del resultado que se desea consultar. No se "
                    "proporcionan rutas de archivos."
                ),
                "enum": [
                    "plan",
                    "prepared_data",
                    "statistics",
                    "issues",
                    "figures",
                    "report",
                ],
            },
            "query": {
                "type": "string",
                "description": (
                    "Tipo de lectura. Usa summary para un resumen, full para el "
                    "contenido completo paginado, id para un identificador, "
                    "section para un encabezado Markdown y next para continuar "
                    "con un cursor devuelto previamente."
                ),
                "enum": ["summary", "full", "id", "section", "next"],
            },
            "selector": {
                "type": ["string", "null"],
                "description": (
                    "Identificador o encabezado. Debe ser una cadena no vacía "
                    "solo cuando query sea id o section. Debe ser null para "
                    "summary, full y next."
                ),
            },
            "cursor": {
                "type": ["string", "null"],
                "description": (
                    "Cursor devuelto por una lectura anterior. Debe utilizarse "
                    "solo cuando query sea next y debe ser null en las demás "
                    "consultas."
                ),
            },
        },
        "required": ["artifact", "query", "selector", "cursor"],
        "additionalProperties": False,
    },
    "strict": True,
}
ESQUEMA_VALIDATE_OUTPUTS = {
    "type": "function",
    "name": "validate_outputs",
    "description": (
        "Valida la presencia, estructura y coherencia básica de todos los resultados. "
        "No evalúa la calidad analítica."
    ),
    "parameters": {
        "type": "object",
        "properties": {},
        "additionalProperties": False,
    },
    "strict": True,
}


class ErrorHerramienta(CapaComunError):
    """Fallo controlado que puede devolverse al modelo sin información privada."""

    def __init__(self, code: str, message: str, retryable: bool = False) -> None:
        super().__init__(message)
        self.code = code
        self.retryable = retryable


class _FalloProcesoPython(Exception):
    """Conserva el error de Python junto con los resultados parciales disponibles."""
    def __init__(
        self,
        resultado: ResultadoProcesoPython,
        data: dict[str, Any],
        affected_files: list[dict[str, Any]],
    ) -> None:
        mensaje = resultado.error_message or "La ejecución de Python terminó con error"
        super().__init__(mensaje)
        self.code = resultado.error_code or "EXECUTION_ERROR"
        self.retryable = resultado.retryable
        self.data = data
        self.affected_files = affected_files
        self.outcome = "timeout" if resultado.exit_status == "timeout" else "error"


def _rol_traza(rol: str) -> str:
    """Agrupa las intervenciones inicial y de corrección bajo el rol Analista en la traza."""
    if rol.startswith("analyst"):
        return "analyst"
    return rol


def _valor_json(valor: Any) -> Any:
    """Convierte los valores de las tablas a tipos que pueden incluirse en JSON."""
    if valor is None or valor is pd.NA:
        return None
    if isinstance(valor, np.generic):
        return _valor_json(valor.item())
    if isinstance(valor, pd.Timestamp):
        return valor.isoformat()
    if isinstance(valor, (datetime, date, hora)):
        return valor.isoformat()
    if isinstance(valor, Decimal):
        return str(valor)
    if isinstance(valor, float):
        if math.isnan(valor):
            return None
        if math.isinf(valor):
            return "Infinity" if valor > 0 else "-Infinity"
    try:
        if bool(pd.isna(valor)):
            return None
    except (TypeError, ValueError):
        pass
    if isinstance(valor, (str, int, float, bool)):
        return valor
    return str(valor)


def _registros_json(tabla: pd.DataFrame, posiciones: list[int]) -> list[dict[str, Any]]:
    """Convierte las filas seleccionadas en diccionarios con los nombres y valores de sus columnas."""
    registros: list[dict[str, Any]] = []
    for posicion in posiciones:
        fila = tabla.iloc[posicion]
        registros.append(
            {
                str(nombre): _valor_json(fila.iloc[indice])
                for indice, nombre in enumerate(tabla.columns)
            }
        )
    return registros


class HerramientasComunes:
    """Expone una única implementación de herramientas a los tres adaptadores."""

    def __init__(
        self,
        configuracion: ConfiguracionExperimento,
        contexto: ContextoEjecucion,
        traza: EscritorTraza,
        limites: ControlLimites,
    ) -> None:
        self.configuracion = configuracion
        self.contexto = contexto
        self.traza = traza
        self.limites = limites
        self._contador = 0
        self._contador_validaciones = 0
        self._inspeccion_cacheada: dict[str, Any] | None = None
        self._lector = LectorResultados(configuracion, contexto)
        self._validador = ValidadorSalidas(configuracion, contexto)
        self._ejecutor_python = EjecutorPython(configuracion, contexto)
        self._correccion_pendiente = False

    def inspeccion_cacheada(self) -> dict[str, Any]:
        """Devuelve una copia de la inspección guardada sin volver a calcularla."""

        if self._inspeccion_cacheada is None:
            raise CapaComunError("La inspección común todavía no se ha calculado")
        return copy.deepcopy(self._inspeccion_cacheada)

    def inspect_dataset(
        self,
        argumentos: Mapping[str, Any] | None,
        rol: str,
        model_call_id: str | None = None,
        role_execution_id: str | None = None,
        attempt: int = 1,
        retry_of: str | None = None,
        parent_event_id: str | None = None,
    ) -> dict[str, Any]:
        """Obtiene la inspección inicial del dataset o reutiliza la que ya está guardada."""

        if self._inspeccion_cacheada is not None:
            return copy.deepcopy(self._inspeccion_cacheada)

        self._contador += 1
        tool_call_id = (
            f"{self.contexto.run_id}__inspect_dataset_{self._contador:03d}"
        )
        inicio = time.perf_counter_ns()
        argumentos_recibidos = dict(argumentos) if isinstance(argumentos, Mapping) else argumentos
        rol_evento = _rol_traza(rol)
        padre = parent_event_id or self.traza.ultimo_evento_id

        evento_inicio = self.traza.registrar(
            "tool_call_started",
            "planning",
            rol_evento,
            "tool",
            {
                "tool_call_id": tool_call_id,
                "tool_name": "inspect_dataset",
                "model_call_id": model_call_id,
                "role_execution_id": role_execution_id,
                "arguments": argumentos_recibidos,
                "attempt": attempt,
                "retry_of": retry_of,
                "tool_version": self.configuracion.datos["versions"]["tools"],
            },
            correlation_id=model_call_id,
            parent_event_id=padre,
        )

        try:
            autorizada = self.limites.autorizar_herramienta(
                rol,
                "inspect_dataset",
                "planning",
            )
        except CapaComunError:
            autorizada = False
        if rol in self.limites.tool_calls_por_rol:
            self.limites.registrar_herramienta_iniciada(
                rol,
                "inspect_dataset",
                "planning",
            )

        try:
            if not autorizada:
                raise ErrorHerramienta(
                    "ACCESS_DENIED",
                    "El rol no tiene autorización o ha agotado su límite de inspecciones",
                )
            if argumentos_recibidos != {}:
                raise ErrorHerramienta(
                    "INVALID_ARGUMENT",
                    "inspect_dataset requiere un objeto vacío",
                )
            datos = self._calcular_inspeccion()
            respuesta = self._respuesta(
                tool_call_id,
                "inspect_dataset",
                "success",
                datos,
                None,
                inicio,
            )
            limite_tiempo = self.configuracion.datos["limits"]["time_seconds"]["tools"][
                "inspect_dataset"
            ]
            if respuesta["duration_ms"] > limite_tiempo * 1000:
                raise ErrorHerramienta(
                    "TIMEOUT",
                    "inspect_dataset ha superado el tiempo máximo configurado",
                )
            self._comprobar_tamano(respuesta)
            self.limites.registrar_resultado_herramienta(True)
            self.traza.registrar(
                "tool_call_finished",
                "planning",
                rol_evento,
                "tool",
                {
                    "tool_call_id": tool_call_id,
                    "tool_name": "inspect_dataset",
                    "duration_ms": respuesta["duration_ms"],
                    "outcome": "success",
                    "response": respuesta,
                    "affected_files": [],
                    "error_id": None,
                    "retry_planned": False,
                },
                correlation_id=model_call_id,
                parent_event_id=evento_inicio,
            )
            self._inspeccion_cacheada = copy.deepcopy(respuesta)
            return respuesta
        except ErrorHerramienta as exc:
            return self._registrar_fallo(
                tool_call_id,
                "inspect_dataset",
                "planning",
                exc,
                inicio,
                rol_evento,
                evento_inicio,
                model_call_id,
            )
        except Exception:
            return self._registrar_fallo(
                tool_call_id,
                "inspect_dataset",
                "planning",
                ErrorHerramienta(
                    "EXECUTION_ERROR",
                    "No ha sido posible cargar o inspeccionar el dataset autorizado",
                ),
                inicio,
                rol_evento,
                evento_inicio,
                model_call_id,
            )

    def execute_python(
        self,
        argumentos: Mapping[str, Any] | None,
        rol: str,
        model_call_id: str | None = None,
        role_execution_id: str | None = None,
        attempt: int = 1,
        retry_of: str | None = None,
        parent_event_id: str | None = None,
    ) -> dict[str, Any]:
        """Comprueba la solicitud, ejecuta el código del Analista y registra sus resultados."""

        fase = self._fase_para_rol(rol)
        rol_evento = _rol_traza(rol)
        self._contador += 1
        tool_call_id = f"{self.contexto.run_id}__execute_python_{self._contador:03d}"
        execution_id = f"{self.contexto.run_id}__python_{self._contador:03d}"
        inicio = time.perf_counter_ns()
        argumentos_recibidos = dict(argumentos) if isinstance(argumentos, Mapping) else argumentos
        argumentos_traza = argumentos_recibidos
        if isinstance(argumentos_recibidos, dict) and isinstance(
            argumentos_recibidos.get("code"),
            str,
        ):
            argumentos_traza = dict(argumentos_recibidos)
            argumentos_traza["code_sha256"] = self._sha256_texto(argumentos_traza["code"])
        evento_inicio = self.traza.registrar(
            "tool_call_started",
            fase,
            rol_evento,
            "tool",
            {
                "tool_call_id": tool_call_id,
                "tool_name": "execute_python",
                "model_call_id": model_call_id,
                "role_execution_id": role_execution_id,
                "arguments": argumentos_traza,
                "attempt": attempt,
                "retry_of": retry_of,
                "tool_version": self.configuracion.datos["versions"]["tools"],
            },
            correlation_id=model_call_id,
            parent_event_id=parent_event_id or self.traza.ultimo_evento_id,
        )
        try:
            autorizada = self.limites.autorizar_herramienta(
                rol,
                "execute_python",
                fase,
            )
        except CapaComunError:
            autorizada = False
        if rol in self.limites.tool_calls_por_rol:
            self.limites.registrar_herramienta_iniciada(
                rol,
                "execute_python",
                fase,
            )

        try:
            if not autorizada:
                raise ErrorHerramienta(
                    "ACCESS_DENIED",
                    "El rol no tiene autorización o ha agotado su límite de ejecuciones Python",
                )
            if not isinstance(argumentos_recibidos, dict) or set(argumentos_recibidos) != {
                "purpose",
                "code",
            }:
                raise ErrorHerramienta(
                    "INVALID_ARGUMENT",
                    "execute_python requiere únicamente purpose y code",
                )
            purpose = argumentos_recibidos["purpose"]
            code = argumentos_recibidos["code"]
            if not isinstance(purpose, str) or not purpose.strip():
                raise ErrorHerramienta(
                    "INVALID_ARGUMENT",
                    "purpose debe ser una cadena no vacía",
                )
            if not isinstance(code, str) or not code.strip():
                raise ErrorHerramienta(
                    "INVALID_ARGUMENT",
                    "code debe ser una cadena no vacía",
                )
            maximo_acumulado = self.configuracion.datos["tools"]["execute_python"][
                "cumulative_time_max_seconds"
            ]
            restante_acumulado = maximo_acumulado - self.limites.python_time_seconds
            maximo_llamada = self.configuracion.datos["limits"]["time_seconds"]["tools"][
                "execute_python"
            ]
            restante_ejecucion = (
                self.configuracion.datos["limits"]["time_seconds"]["run"]
                - self.limites.elapsed_seconds()
            )
            timeout = min(maximo_llamada, restante_acumulado, restante_ejecucion)
            try:
                resultado = self._ejecutor_python.ejecutar(
                    execution_id,
                    code,
                    timeout,
                )
            except ErrorCodigo as exc:
                raise ErrorHerramienta(exc.code, str(exc), exc.retryable) from exc
            self.limites.registrar_tiempo_python(
                resultado.duration_seconds,
                fase,
                rol,
            )
            datos = self._datos_resultado_python(resultado)
            afectados = [
                dict(archivo)
                for archivo in (*resultado.files_created, *resultado.files_modified)
            ]
            self._registrar_artefactos_python(
                resultado,
                evento_inicio,
                fase,
            )
            if resultado.exit_status != "success":
                raise _FalloProcesoPython(resultado, datos, afectados)

            respuesta = self._respuesta(
                tool_call_id,
                "execute_python",
                "success",
                datos,
                None,
                inicio,
            )
            self._comprobar_tamano(respuesta)
            self.limites.registrar_resultado_herramienta(True)
            self.traza.registrar(
                "tool_call_finished",
                fase,
                rol_evento,
                "tool",
                {
                    "tool_call_id": tool_call_id,
                    "tool_name": "execute_python",
                    "duration_ms": respuesta["duration_ms"],
                    "outcome": "success",
                    "response": respuesta,
                    "affected_files": afectados,
                    "error_id": None,
                    "retry_planned": False,
                },
                correlation_id=model_call_id,
                parent_event_id=evento_inicio,
            )
            return respuesta
        except _FalloProcesoPython as exc:
            return self._registrar_fallo(
                tool_call_id,
                "execute_python",
                fase,
                ErrorHerramienta(exc.code, str(exc), exc.retryable),
                inicio,
                rol_evento,
                evento_inicio,
                model_call_id,
                data=exc.data,
                affected_files=exc.affected_files,
                outcome=exc.outcome,
            )
        except ErrorHerramienta as exc:
            return self._registrar_fallo(
                tool_call_id,
                "execute_python",
                fase,
                exc,
                inicio,
                rol_evento,
                evento_inicio,
                model_call_id,
            )
        except Exception:
            return self._registrar_fallo(
                tool_call_id,
                "execute_python",
                fase,
                ErrorHerramienta(
                    "INTERNAL_ERROR",
                    "No ha sido posible completar execute_python",
                ),
                inicio,
                rol_evento,
                evento_inicio,
                model_call_id,
            )

    @staticmethod
    def _sha256_texto(texto: str) -> str:
        """Calcula el hash SHA-256 del código recibido."""
        import hashlib

        return hashlib.sha256(texto.encode("utf-8")).hexdigest().upper()

    @staticmethod
    def _datos_resultado_python(resultado: ResultadoProcesoPython) -> dict[str, Any]:
        """Prepara la salida, los errores y los archivos que devuelve la ejecución de Python."""
        return {
            "execution_id": resultado.execution_id,
            "exit_status": resultado.exit_status,
            "stdout": resultado.stdout,
            "stderr": resultado.stderr,
            "truncated": resultado.truncated,
            "files_created": [dict(archivo) for archivo in resultado.files_created],
            "files_modified": [dict(archivo) for archivo in resultado.files_modified],
        }

    def _registrar_artefactos_python(
        self,
        resultado: ResultadoProcesoPython,
        origin_event_id: str,
        fase: str,
    ) -> None:
        """Registra en la traza los archivos creados o modificados por Python."""
        permanentes = {
            "prepared_data.csv",
            "statistics.json",
            "issues.json",
        }
        for archivo in (*resultado.files_created, *resultado.files_modified):
            ruta = str(archivo["path"])
            if ruta not in permanentes and not ruta.startswith("figures/"):
                continue
            extension = Path(ruta).suffix.casefold().lstrip(".")
            self.traza.registrar(
                "artifact_written",
                fase,
                "analyst",
                "common_runtime",
                {
                    "artifact_name": ruta,
                    "relative_path": ruta,
                    "writer": "analyst",
                    "phase_written": (
                        "correction" if fase == "correction" else "initial"
                    ),
                    "bytes": archivo["bytes"],
                    "sha256": archivo["sha256"],
                    "format": extension,
                    "replaces_sha256": archivo.get("previous_sha256"),
                    "origin_event_id": origin_event_id,
                },
                parent_event_id=origin_event_id,
            )

    def marcar_correccion_pendiente(self, pendiente: bool) -> None:
        """Indica si queda una corrección del Analista pendiente de realizar."""

        self._correccion_pendiente = bool(pendiente)

    def read_output(
        self,
        argumentos: Mapping[str, Any] | None,
        rol: str,
        model_call_id: str | None = None,
        role_execution_id: str | None = None,
        attempt: int = 1,
        retry_of: str | None = None,
        parent_event_id: str | None = None,
    ) -> dict[str, Any]:
        """Consulta los archivos autorizados y devuelve su contenido o un resumen."""

        fase = self._fase_para_rol(rol)
        rol_evento = _rol_traza(rol)
        self._contador += 1
        tool_call_id = f"{self.contexto.run_id}__read_output_{self._contador:03d}"
        inicio = time.perf_counter_ns()
        argumentos_recibidos = dict(argumentos) if isinstance(argumentos, Mapping) else argumentos
        evento_inicio = self.traza.registrar(
            "tool_call_started",
            fase,
            rol_evento,
            "tool",
            {
                "tool_call_id": tool_call_id,
                "tool_name": "read_output",
                "model_call_id": model_call_id,
                "role_execution_id": role_execution_id,
                "arguments": argumentos_recibidos,
                "attempt": attempt,
                "retry_of": retry_of,
                "tool_version": self.configuracion.datos["versions"]["tools"],
            },
            correlation_id=model_call_id,
            parent_event_id=parent_event_id or self.traza.ultimo_evento_id,
        )
        try:
            autorizada = self.limites.autorizar_herramienta(
                rol,
                "read_output",
                fase,
            )
        except CapaComunError:
            autorizada = False
        if rol in self.limites.tool_calls_por_rol:
            self.limites.registrar_herramienta_iniciada(
                rol,
                "read_output",
                fase,
            )
        try:
            if not autorizada:
                raise ErrorHerramienta(
                    "ACCESS_DENIED",
                    "El rol no tiene autorización o ha agotado su límite de lecturas",
                )
            if not isinstance(argumentos_recibidos, dict):
                raise ErrorHerramienta(
                    "INVALID_ARGUMENT",
                    "read_output requiere un objeto de argumentos",
                )
            try:
                datos = self._lector.consultar(argumentos_recibidos)
            except ErrorConsulta as exc:
                raise ErrorHerramienta(exc.code, str(exc)) from exc
            respuesta = self._respuesta(
                tool_call_id,
                "read_output",
                "success",
                datos,
                None,
                inicio,
            )
            self._comprobar_tamano(respuesta)
            limite_tiempo = self.configuracion.datos["limits"]["time_seconds"]["tools"][
                "read_output"
            ]
            if respuesta["duration_ms"] > limite_tiempo * 1000:
                raise ErrorHerramienta(
                    "TIMEOUT",
                    "read_output ha superado el tiempo máximo configurado",
                )
            self.limites.registrar_resultado_herramienta(True)
            self.traza.registrar(
                "tool_call_finished",
                fase,
                rol_evento,
                "tool",
                {
                    "tool_call_id": tool_call_id,
                    "tool_name": "read_output",
                    "duration_ms": respuesta["duration_ms"],
                    "outcome": "success",
                    "response": respuesta,
                    "affected_files": [],
                    "error_id": None,
                    "retry_planned": False,
                },
                correlation_id=model_call_id,
                parent_event_id=evento_inicio,
            )
            return respuesta
        except ErrorHerramienta as exc:
            return self._registrar_fallo(
                tool_call_id,
                "read_output",
                fase,
                exc,
                inicio,
                rol_evento,
                evento_inicio,
                model_call_id,
            )
        except Exception:
            return self._registrar_fallo(
                tool_call_id,
                "read_output",
                fase,
                ErrorHerramienta(
                    "INTERNAL_ERROR",
                    "No ha sido posible completar la lectura solicitada",
                ),
                inicio,
                rol_evento,
                evento_inicio,
                model_call_id,
            )

    def validate_outputs(
        self,
        argumentos: Mapping[str, Any] | None,
        rol: str,
        trigger: str,
        automatic: bool = False,
        model_call_id: str | None = None,
        role_execution_id: str | None = None,
        attempt: int = 1,
        retry_of: str | None = None,
        parent_event_id: str | None = None,
    ) -> dict[str, Any]:
        """Comprueba los archivos obligatorios y sus relaciones, sin modificar ni puntuar su contenido."""

        if trigger not in {"analyst", "reviewer", "pre_review", "final"}:
            raise CapaComunError("Trigger de validación no autorizado")
        if automatic and trigger not in {"analyst", "pre_review", "final"}:
            raise CapaComunError(
                "Una validación automática requiere analyst, pre_review o final"
            )
        fase = "final_validation" if trigger == "final" else self._fase_para_rol(rol)
        rol_evento = "runtime" if automatic else _rol_traza(rol)
        self._contador_validaciones += 1
        validation_id = (
            f"{self.contexto.run_id}__validation_{self._contador_validaciones:03d}"
        )
        inicio = time.perf_counter_ns()

        if automatic:
            if argumentos not in ({}, None):
                raise CapaComunError("La validación automática no admite argumentos")
            datos = self._validador.validar(
                validation_id,
                self._correccion_pendiente,
            )
            respuesta = self._respuesta(
                validation_id,
                "validate_outputs",
                "success",
                datos,
                None,
                inicio,
            )
            self._comprobar_tamano(respuesta)
            self._registrar_validacion(
                respuesta,
                datos,
                trigger,
                True,
                fase,
                "runtime",
                parent_event_id or self.traza.ultimo_evento_id,
            )
            return respuesta

        self._contador += 1
        tool_call_id = f"{self.contexto.run_id}__validate_outputs_{self._contador:03d}"
        argumentos_recibidos = dict(argumentos) if isinstance(argumentos, Mapping) else argumentos
        evento_inicio = self.traza.registrar(
            "tool_call_started",
            fase,
            rol_evento,
            "tool",
            {
                "tool_call_id": tool_call_id,
                "tool_name": "validate_outputs",
                "model_call_id": model_call_id,
                "role_execution_id": role_execution_id,
                "arguments": argumentos_recibidos,
                "attempt": attempt,
                "retry_of": retry_of,
                "tool_version": self.configuracion.datos["versions"]["tools"],
            },
            correlation_id=model_call_id,
            parent_event_id=parent_event_id or self.traza.ultimo_evento_id,
        )
        try:
            autorizada = self.limites.autorizar_herramienta(
                rol,
                "validate_outputs",
                fase,
            )
        except CapaComunError:
            autorizada = False
        if rol in self.limites.tool_calls_por_rol:
            self.limites.registrar_herramienta_iniciada(
                rol,
                "validate_outputs",
                fase,
            )
        try:
            if not autorizada:
                raise ErrorHerramienta(
                    "ACCESS_DENIED",
                    "El rol no tiene autorización o ha agotado su límite de validaciones",
                )
            if argumentos_recibidos != {}:
                raise ErrorHerramienta(
                    "INVALID_ARGUMENT",
                    "validate_outputs requiere un objeto vacío",
                )
            datos = self._validador.validar(
                validation_id,
                self._correccion_pendiente,
            )
            respuesta = self._respuesta(
                tool_call_id,
                "validate_outputs",
                "success",
                datos,
                None,
                inicio,
            )
            self._comprobar_tamano(respuesta)
            limite_tiempo = self.configuracion.datos["limits"]["time_seconds"]["tools"][
                "validate_outputs"
            ]
            if respuesta["duration_ms"] > limite_tiempo * 1000:
                raise ErrorHerramienta(
                    "TIMEOUT",
                    "validate_outputs ha superado el tiempo máximo configurado",
                )
            self.limites.registrar_resultado_herramienta(True)
            evento_fin = self.traza.registrar(
                "tool_call_finished",
                fase,
                rol_evento,
                "tool",
                {
                    "tool_call_id": tool_call_id,
                    "tool_name": "validate_outputs",
                    "duration_ms": respuesta["duration_ms"],
                    "outcome": "success",
                    "response": respuesta,
                    "affected_files": [],
                    "error_id": None,
                    "retry_planned": False,
                },
                correlation_id=model_call_id,
                parent_event_id=evento_inicio,
            )
            self._registrar_validacion(
                respuesta,
                datos,
                trigger,
                False,
                fase,
                rol_evento,
                evento_fin,
            )
            return respuesta
        except ErrorHerramienta as exc:
            return self._registrar_fallo(
                tool_call_id,
                "validate_outputs",
                fase,
                exc,
                inicio,
                rol_evento,
                evento_inicio,
                model_call_id,
            )
        except Exception:
            return self._registrar_fallo(
                tool_call_id,
                "validate_outputs",
                fase,
                ErrorHerramienta(
                    "INTERNAL_ERROR",
                    "No ha sido posible completar la validación",
                ),
                inicio,
                rol_evento,
                evento_inicio,
                model_call_id,
            )

    def _registrar_validacion(
        self,
        respuesta: Mapping[str, Any],
        datos: Mapping[str, Any],
        trigger: str,
        automatic: bool,
        fase: str,
        rol_evento: str,
        parent_event_id: str,
    ) -> str:
        """Guarda en la traza el resultado de la comprobación de las salidas."""
        return self.traza.registrar(
            "validation_completed",
            fase,
            rol_evento,
            "common_runtime",
            {
                "trigger": trigger,
                "automatic": automatic,
                "validation_id": datos["validation_id"],
                "validation_status": datos["validation_status"],
                "response": dict(respuesta),
            },
            parent_event_id=parent_event_id,
        )

    @staticmethod
    def _fase_para_rol(rol: str) -> str:
        """Devuelve la fase de ejecución correspondiente al rol indicado."""
        fases = {
            "planner": "planning",
            "analyst_initial": "analysis",
            "reviewer": "review",
            "analyst_correction": "correction",
            "runtime": "final_validation",
        }
        if rol not in fases:
            raise CapaComunError(f"Rol no reconocido: {rol}")
        return fases[rol]

    def _calcular_inspeccion(self) -> dict[str, Any]:
        """Comprueba el dataset y obtiene sus dimensiones, tipos, valores ausentes y muestras."""
        dataset = self.contexto.dataset
        if dataset.ruta_entrada.stat().st_size != dataset.bytes:
            raise ErrorHerramienta(
                "SCHEMA_ERROR",
                "El tamaño del dataset ya no coincide con el manifiesto",
            )
        if sha256_archivo(dataset.ruta_entrada) != dataset.sha256:
            raise ErrorHerramienta(
                "SCHEMA_ERROR",
                "El hash del dataset ya no coincide con el manifiesto",
            )

        warnings: list[str] = []
        if dataset.formato == "csv":
            tabla = pd.read_csv(dataset.ruta_entrada, encoding="utf-8", low_memory=False)
        elif dataset.formato == "xlsx":
            tabla = pd.read_excel(
                dataset.ruta_entrada,
                sheet_name=dataset.hoja_seleccionada,
                engine="openpyxl",
            )
        else:
            raise ErrorHerramienta("SCHEMA_ERROR", "Formato de dataset no autorizado")

        filas, columnas = tabla.shape
        if filas != dataset.filas_esperadas or columnas != dataset.columnas_esperadas:
            raise ErrorHerramienta(
                "SCHEMA_ERROR",
                "La estructura observada no coincide con la estructura congelada",
            )
        nombres = [str(nombre) for nombre in tabla.columns]
        if len(nombres) != len(set(nombres)):
            warnings.append("Se han observado nombres de columna duplicados")

        perfil = []
        for posicion, nombre in enumerate(tabla.columns):
            serie = tabla.iloc[:, posicion]
            no_nulos = int(serie.notna().sum())
            perfil.append(
                {
                    "name": str(nombre),
                    "position": posicion,
                    "observed_type": str(serie.dtype),
                    "non_null": no_nulos,
                    "missing": int(filas - no_nulos),
                    "cardinality": int(serie.nunique(dropna=True)),
                }
            )

        limites_muestra = self.configuracion.datos["tools"]["inspect_dataset"]
        primeras = list(range(min(limites_muestra["sample_first_rows"], filas)))
        inicio_ultimas = max(filas - limites_muestra["sample_last_rows"], 0)
        ultimas = [posicion for posicion in range(inicio_ultimas, filas) if posicion not in primeras]
        excluidas = set(primeras) | set(ultimas)
        candidatas = [posicion for posicion in range(filas) if posicion not in excluidas]
        cantidad_aleatoria = min(
            limites_muestra["sample_seeded_rows"],
            len(candidatas),
        )
        generador = random.Random(self.configuracion.datos["security"]["experiment_seed"])
        aleatorias = generador.sample(candidatas, cantidad_aleatoria)
        if len(primeras) + len(ultimas) + len(aleatorias) > limites_muestra["sample_rows_max"]:
            raise ErrorHerramienta(
                "INTERNAL_ERROR",
                "La configuración de la muestra supera el máximo autorizado",
            )

        documentacion = []
        for ruta in dataset.documentacion_publica:
            try:
                contenido = ruta.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                contenido = ruta.read_text(encoding="utf-8", errors="replace")
                warnings.append(
                    f"{ruta.name} contenía caracteres sustituidos durante la lectura UTF-8"
                )
            documentacion.append(
                {
                    "name": ruta.name,
                    "sha256": sha256_archivo(ruta),
                    "content": contenido,
                }
            )

        return {
            "dataset_id": dataset.dataset_id,
            "file_format": dataset.formato,
            "selected_sheet": dataset.hoja_seleccionada,
            "rows": filas,
            "columns": columnas,
            "column_profile": perfil,
            "head_sample": _registros_json(tabla, primeras),
            "tail_sample": _registros_json(tabla, ultimas),
            "random_sample": _registros_json(tabla, aleatorias),
            "public_documentation": documentacion,
            "warnings": warnings,
            "source_sha256": dataset.sha256,
        }

    def _comprobar_tamano(self, respuesta: Mapping[str, Any]) -> None:
        """Comprueba que la respuesta no supere el máximo de caracteres permitido."""
        maximo = self.configuracion.datos["limits"]["sizes"][
            "tool_text_response_max_characters"
        ]
        contenido = json.dumps(
            respuesta,
            ensure_ascii=False,
            separators=(",", ":"),
            allow_nan=False,
        )
        if len(contenido) > maximo:
            raise ErrorHerramienta(
                "OUTPUT_TOO_LARGE",
                "La respuesta de la herramienta supera el tamaño máximo configurado",
            )

    def _respuesta(
        self,
        tool_call_id: str,
        tool_name: str,
        status: str,
        data: dict[str, Any] | None,
        error: dict[str, Any] | None,
        inicio_ns: int,
    ) -> dict[str, Any]:
        """Construye la respuesta de la herramienta con su resultado, error y duración."""
        return {
            "tool_call_id": tool_call_id,
            "tool_name": tool_name,
            "status": status,
            "data": data,
            "error": error,
            "duration_ms": max((time.perf_counter_ns() - inicio_ns) // 1_000_000, 0),
        }

    def _registrar_fallo(
        self,
        tool_call_id: str,
        tool_name: str,
        fase: str,
        error: ErrorHerramienta,
        inicio_ns: int,
        rol_evento: str,
        evento_inicio: str,
        model_call_id: str | None,
        data: dict[str, Any] | None = None,
        affected_files: list[dict[str, Any]] | None = None,
        outcome: str = "error",
    ) -> dict[str, Any]:
        """Registra el error y la llamada fallida y prepara la respuesta que recibe el agente."""
        respuesta = self._respuesta(
            tool_call_id,
            tool_name,
            "error",
            data,
            {
                "code": error.code,
                "message": str(error),
                "retryable": error.retryable,
            },
            inicio_ns,
        )
        error_id = f"ERR-TOOL-{self._contador:06d}"
        evento_error = self.traza.registrar(
            "error_recorded",
            fase,
            "runtime",
            "common_runtime",
            {
                "error_id": error_id,
                "category": "tool",
                "code": error.code,
                "message": str(error),
                "severity": "recoverable",
                "related_event_id": evento_inicio,
                "operation": tool_name,
                "retryable": error.retryable,
                "retry_triggered": False,
                "exception_type": type(error).__name__,
                "technical_trace": None,
            },
            correlation_id=model_call_id,
            parent_event_id=evento_inicio,
        )
        self.limites.registrar_error(error_id, "recoverable")
        self.limites.registrar_resultado_herramienta(False)
        self.traza.registrar(
            "tool_call_failed",
            fase,
            rol_evento,
            "tool",
            {
                "tool_call_id": tool_call_id,
                "tool_name": tool_name,
                "duration_ms": respuesta["duration_ms"],
                "outcome": outcome,
                "response": respuesta,
                "affected_files": affected_files or [],
                "error_id": error_id,
                "retry_planned": False,
            },
            correlation_id=model_call_id,
            parent_event_id=evento_error,
        )
        return respuesta
