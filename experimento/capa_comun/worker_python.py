"""Ejecución del código del Analista en un proceso separado"""

from __future__ import annotations

import ast
import builtins
import csv
import datetime
import decimal
import io
import itertools
import json
import math
import os
import random
import re
import socket
import statistics
import subprocess
import sys
import warnings
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import openpyxl
import pandas as pd
import scipy
import seaborn as sns


MODULOS_TERCEROS = {
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


def _denegado(*args: Any, **kwargs: Any) -> Any:
    """Interrumpe una operación que el código del Analista no tiene permitida."""
    raise PermissionError("Operación bloqueada por el entorno de execute_python")


def _configurar_archivos(input_path: Path, output_dir: Path, temporary_dir: Path) -> None:
    """Instala las comprobaciones de lectura y escritura de archivos."""
    original_open = builtins.open
    original_io_open = io.open
    original_os_open = os.open
    entrada = input_path.resolve()
    salida = output_dir.resolve()
    temporal = temporary_dir.resolve()
    raices_tecnicas = {
        Path(sys.base_prefix).resolve(),
        Path(sys.prefix).resolve(),
    }
    if os.environ.get("WINDIR"):
        raices_tecnicas.add(Path(os.environ["WINDIR"]).resolve() / "Fonts")
    for valor in sys.path:
        if valor:
            try:
                raices_tecnicas.add(Path(valor).resolve())
            except OSError:
                pass

    def comprobar(file: Any, modo: str) -> None:
        if isinstance(file, int):
            raise PermissionError("No se permite acceder directamente a descriptores")
        ruta = Path(os.fspath(file)).resolve()
        escritura = any(marca in modo for marca in ("w", "a", "x", "+"))
        if escritura:
            try:
                relativa = ruta.relative_to(salida)
            except ValueError as exc:
                raise PermissionError("La escritura sale del directorio autorizado") from exc
            partes = relativa.parts
            if not partes:
                raise PermissionError("No puede escribirse directamente sobre OUTPUT_DIR")
            permanente = partes[0] in {
                "prepared_data.csv",
                "statistics.json",
                "issues.json",
            } and len(partes) == 1
            figura = (
                partes[0] == "figures"
                and len(partes) == 2
                and ruta.suffix.casefold() == ".png"
            )
            temporal_autorizado = ruta == temporal or temporal in ruta.parents
            if not (permanente or figura or temporal_autorizado):
                raise PermissionError("La ruta de escritura no corresponde a una salida autorizada")
            if ruta == entrada:
                raise PermissionError("El dataset original es de solo lectura")
        else:
            dentro_salida = ruta == salida or salida in ruta.parents
            lectura_tecnica = any(
                ruta == raiz or raiz in ruta.parents for raiz in raices_tecnicas
            )
            if ruta != entrada and not dentro_salida and not lectura_tecnica:
                raise PermissionError("La lectura sale de las entradas autorizadas")

    def open_seguro(file: Any, mode: str = "r", *args: Any, **kwargs: Any):
        comprobar(file, mode)
        return original_open(file, mode, *args, **kwargs)

    def io_open_seguro(file: Any, mode: str = "r", *args: Any, **kwargs: Any):
        comprobar(file, mode)
        return original_io_open(file, mode, *args, **kwargs)

    def os_open_seguro(file: Any, flags: int, *args: Any, **kwargs: Any):
        marcas_escritura = (
            os.O_WRONLY
            | os.O_RDWR
            | os.O_APPEND
            | os.O_CREAT
            | os.O_TRUNC
        )
        modo = "w" if flags & marcas_escritura else "r"
        comprobar(file, modo)
        return original_os_open(file, flags, *args, **kwargs)

    builtins.open = open_seguro
    io.open = io_open_seguro
    os.open = os_open_seguro


def _configurar_importaciones() -> None:
    """Restringe los módulos que puede importar el código del Analista."""
    importacion_original = builtins.__import__
    estandar = set(getattr(sys, "stdlib_module_names", ()))

    def importar(
        name: str,
        globals: dict[str, Any] | None = None,
        locals: dict[str, Any] | None = None,
        fromlist: tuple[str, ...] = (),
        level: int = 0,
    ) -> Any:
        raiz = name.split(".", 1)[0]
        llamada_usuario = globals is not None and globals.get("__name__") == "__main__"
        if llamada_usuario:
            if raiz in MODULOS_PROHIBIDOS:
                raise ImportError(f"El módulo {raiz} no está autorizado")
            if raiz not in MODULOS_TERCEROS and raiz not in estandar:
                raise ImportError(f"El módulo {raiz} no forma parte del entorno congelado")
        return importacion_original(name, globals, locals, fromlist, level)

    builtins.__import__ = importar


def _configurar_operaciones_prohibidas() -> None:
    """Bloquea determinadas operaciones de red, procesos y modificación de archivos."""
    builtins.input = _denegado
    subprocess.Popen = _denegado
    subprocess.run = _denegado
    subprocess.call = _denegado
    subprocess.check_call = _denegado
    subprocess.check_output = _denegado
    os.system = _denegado
    os.popen = _denegado
    for nombre in dir(os):
        if nombre.startswith("spawn") or nombre.startswith("exec"):
            setattr(os, nombre, _denegado)
    socket.socket = _denegado
    socket.create_connection = _denegado
    socket.getaddrinfo = _denegado
    os.remove = _denegado
    os.unlink = _denegado
    os.rmdir = _denegado
    os.removedirs = _denegado
    os.rename = _denegado
    os.replace = _denegado


def _ejecutar(configuracion: dict[str, Any]) -> int:
    """Prepara los controles y las bibliotecas y ejecuta el código recibido."""
    entrada = Path(configuracion["input_path"]).resolve()
    salida = Path(configuracion["output_dir"]).resolve()
    figuras = Path(configuracion["figures_dir"]).resolve()
    temporal = Path(configuracion["temporary_dir"]).resolve()
    codigo = configuracion["code"]

    _configurar_archivos(entrada, salida, temporal)
    _configurar_importaciones()
    _configurar_operaciones_prohibidas()
    os.environ.clear()

    espacio = {
        "__name__": "__main__",
        "INPUT_PATH": str(entrada),
        "OUTPUT_DIR": str(salida),
        "FIGURES_DIR": str(figuras),
        "RUN_ID": configuracion["run_id"],
        "DATASET_ID": configuracion["dataset_id"],
        "EXPERIMENT_SEED": configuracion["experiment_seed"],
        "pd": pd,
        "np": np,
        "scipy": scipy,
        "plt": plt,
        "sns": sns,
        "openpyxl": openpyxl,
        "json": json,
        "csv": csv,
        "math": math,
        "statistics": statistics,
        "datetime": datetime,
        "decimal": decimal,
        "itertools": itertools,
        "random": random,
        "re": re,
        "warnings": warnings,
        "Counter": Counter,
        "defaultdict": defaultdict,
    }
    try:
        arbol = ast.parse(codigo, filename="<execute_python>", mode="exec")
        compilado = compile(arbol, "<execute_python>", "exec")
        exec(compilado, espacio, espacio)
    except BaseException as exc:
        print(f"{type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    return 0


def main() -> int:
    """Lee la configuración de la llamada e inicia su ejecución."""
    if len(sys.argv) != 2:
        print("Configuración de ejecución ausente", file=sys.stderr)
        return 2
    try:
        configuracion = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    except Exception:
        print("No puede leerse la configuración aislada", file=sys.stderr)
        return 2
    return _ejecutar(configuracion)


if __name__ == "__main__":
    raise SystemExit(main())
