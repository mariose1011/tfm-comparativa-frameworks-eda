"""Identificación de cada ejecución y preparación de sus carpetas de trabajo."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .configuracion import ConfiguracionExperimento
from .datasets import DatasetValidado, validar_datasets
from .errores import EjecucionError
from .utilidades import resolver_ruta_relativa, validar_identificador


@dataclass(frozen=True, slots=True)
class ContextoEjecucion:
    """Información y rutas necesarias para una ejecución."""

    run_id: str
    framework_id: str
    dataset: DatasetValidado
    repeticion: int
    directorio_salida: Path
    directorio_temporal: Path
    directorio_figuras: Path
    config_version: str
    config_sha256: str


def crear_run_id(
    framework_id: str,
    dataset_id: str,
    repeticion: int,
    instante_utc: datetime | None = None,
) -> str:
    """Construye el identificador único con el dataset, framework, repetición y fecha UTC."""

    validar_identificador(framework_id, "framework_id")
    validar_identificador(dataset_id, "dataset_id")
    if not isinstance(repeticion, int) or isinstance(repeticion, bool) or repeticion < 1:
        raise EjecucionError("La repetición debe ser un entero positivo")

    instante = instante_utc or datetime.now(timezone.utc)
    if instante.tzinfo is None or instante.utcoffset() is None:
        raise EjecucionError("El instante utilizado para run_id debe incluir zona horaria")
    marca = instante.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    return f"{dataset_id}__{framework_id}__r{repeticion:02d}__{marca}"


def _crear_directorio_ejecucion(
    raiz_salida: Path,
    run_id: str,
    nombre_temporal: str,
) -> tuple[Path, Path, Path]:
    """Crea la carpeta de ejecución y los subdirectorios de figuras y temporales."""

    validar_identificador(run_id, "run_id")
    validar_identificador(nombre_temporal, "temporary_directory_name")
    raiz_salida.mkdir(parents=True, exist_ok=True)
    directorio = resolver_ruta_relativa(raiz_salida, run_id)
    if directorio.parent != raiz_salida.resolve():
        raise EjecucionError("El directorio de ejecución debe depender directamente de output_root")
    try:
        directorio.mkdir(exist_ok=False)
        figuras = directorio / "figures"
        temporal = directorio / nombre_temporal
        figuras.mkdir()
        temporal.mkdir()
    except FileExistsError as exc:
        raise EjecucionError(f"La ejecución ya existe: {run_id}") from exc
    except OSError as exc:
        raise EjecucionError(f"No puede crearse el directorio de ejecución: {run_id}") from exc
    return directorio, temporal, figuras


def preparar_ejecucion(
    configuracion: ConfiguracionExperimento,
    framework_id: str,
    dataset_id: str,
    repeticion: int,
    run_id: str | None = None,
    instante_utc: datetime | None = None,
) -> ContextoEjecucion:
    """Comprueba las entradas y prepara las carpetas y el contexto de la ejecución."""
    
    if framework_id not in configuracion.datos["frameworks"]["allowed"]:
        raise EjecucionError(f"Framework no autorizado: {framework_id}")
    if dataset_id not in configuracion.datos["datasets"]["allowed_ids"]:
        raise EjecucionError(f"Dataset no autorizado: {dataset_id}")
    if not isinstance(repeticion, int) or isinstance(repeticion, bool) or repeticion < 1:
        raise EjecucionError("La repetición debe ser un entero positivo")

    datasets = validar_datasets(configuracion)
    dataset = datasets[dataset_id]
    identificador = run_id or crear_run_id(
        framework_id,
        dataset_id,
        repeticion,
        instante_utc,
    )
    validar_identificador(identificador, "run_id")

    raiz_salida = configuracion.resolver_ruta(configuracion.datos["paths"]["output_root"])
    nombre_temporal = configuracion.datos["output_contract"]["temporary_directory_name"]
    directorio, temporal, figuras = _crear_directorio_ejecucion(
        raiz_salida,
        identificador,
        nombre_temporal,
    )

    return ContextoEjecucion(
        run_id=identificador,
        framework_id=framework_id,
        dataset=dataset,
        repeticion=repeticion,
        directorio_salida=directorio,
        directorio_temporal=temporal,
        directorio_figuras=figuras,
        config_version=configuracion.datos["config_version"],
        config_sha256=configuracion.sha256,
    )
