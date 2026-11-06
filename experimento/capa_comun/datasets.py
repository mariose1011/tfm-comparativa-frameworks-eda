"""Lectura del registro de datasets y comprobación de las entradas públicas."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

from .configuracion import ConfiguracionExperimento
from .errores import HashNoCoincideError, ManifiestoError
from .utilidades import cargar_json_sin_duplicados, sha256_archivo


@dataclass(frozen=True, slots=True)
class DatasetValidado:
    """Entrada pública comprobada y lista para una ejecución."""

    dataset_id: str
    nombre: str
    ruta_entrada: Path
    formato: str
    hoja_seleccionada: str | None
    sha256: str
    bytes: int
    filas_esperadas: int
    columnas_esperadas: int
    documentacion_publica: tuple[Path, ...]
    solo_piloto: bool


def _registro_archivo(archivos: list[dict[str, Any]], ruta: str) -> dict[str, Any]:
    """Busca el único registro correspondiente a la ruta indicada."""
    coincidencias = [archivo for archivo in archivos if archivo.get("path") == ruta]
    if len(coincidencias) != 1:
        raise ManifiestoError(f"El manifiesto debe contener un único registro para {ruta}")
    return coincidencias[0]


def _validar_archivo(
    configuracion: ConfiguracionExperimento,
    registro: Mapping[str, Any],
) -> tuple[Path, int, str]:
    """Comprueba la existencia, el tamaño y el hash de un archivo."""
    ruta_relativa = registro.get("path")
    bytes_esperados = registro.get("bytes")
    hash_esperado = registro.get("sha256")
    if not isinstance(ruta_relativa, str):
        raise ManifiestoError("Un archivo del manifiesto no contiene una ruta válida")
    if not isinstance(bytes_esperados, int) or bytes_esperados < 0:
        raise ManifiestoError(f"Tamaño inválido en el manifiesto para {ruta_relativa}")
    if not isinstance(hash_esperado, str) or len(hash_esperado) != 64:
        raise ManifiestoError(f"Hash inválido en el manifiesto para {ruta_relativa}")

    ruta = configuracion.resolver_ruta(ruta_relativa)
    if not ruta.is_file():
        raise ManifiestoError(f"No existe el archivo declarado: {ruta_relativa}")
    if ruta.stat().st_size != bytes_esperados:
        raise HashNoCoincideError(f"El tamaño no coincide para {ruta_relativa}")
    hash_real = sha256_archivo(ruta)
    if hash_real != hash_esperado.upper():
        raise HashNoCoincideError(f"El SHA-256 no coincide para {ruta_relativa}")
    return ruta, bytes_esperados, hash_real


def validar_datasets(
    configuracion: ConfiguracionExperimento,
) -> Mapping[str, DatasetValidado]:
    """Comprueba el registro de datasets, las entradas y su documentación pública."""

    ruta_manifiesto = configuracion.resolver_ruta(configuracion.datos["paths"]["dataset_manifest"])
    manifiesto, _ = cargar_json_sin_duplicados(ruta_manifiesto)

    version_esperada = configuracion.datos["versions"]["dataset_manifest"]
    if manifiesto.get("manifest_version") != version_esperada:
        raise ManifiestoError("La versión del manifiesto no coincide con la configuración")

    entradas = manifiesto.get("datasets")
    if not isinstance(entradas, list):
        raise ManifiestoError("datasets debe ser una lista en el manifiesto")

    identificadores = [entrada.get("id") for entrada in entradas if isinstance(entrada, dict)]
    esperados = set(configuracion.datos["datasets"]["allowed_ids"])
    if len(identificadores) != len(set(identificadores)) or set(identificadores) != esperados:
        raise ManifiestoError("Los datasets del manifiesto no coinciden con la configuración")

    resultado: dict[str, DatasetValidado] = {}
    for entrada in entradas:
        if not isinstance(entrada, dict):
            raise ManifiestoError("Cada dataset del manifiesto debe ser un objeto")
        dataset_id = entrada.get("id")
        nombre = entrada.get("name")
        seleccionada = entrada.get("selected_input")
        hoja_seleccionada = entrada.get("selected_sheet")
        estructura = entrada.get("selected_input_structure")
        archivos = entrada.get("files")
        if not isinstance(dataset_id, str) or not isinstance(nombre, str):
            raise ManifiestoError("Un dataset no contiene id y nombre válidos")
        if not isinstance(seleccionada, str) or not isinstance(archivos, list):
            raise ManifiestoError(f"Entrada seleccionada o archivos inválidos para {dataset_id}")
        if not isinstance(estructura, dict):
            raise ManifiestoError(f"Falta selected_input_structure para {dataset_id}")
        filas_esperadas = estructura.get("rows")
        columnas_esperadas = estructura.get("columns")
        if not isinstance(filas_esperadas, int) or filas_esperadas < 0:
            raise ManifiestoError(f"Número de filas esperado inválido para {dataset_id}")
        if not isinstance(columnas_esperadas, int) or columnas_esperadas < 1:
            raise ManifiestoError(f"Número de columnas esperado inválido para {dataset_id}")

        prefijo_publico = f"datasets/experiment_inputs/{dataset_id}/"
        if not seleccionada.startswith(prefijo_publico):
            raise ManifiestoError(f"La entrada de {dataset_id} no está en experiment_inputs")

        registro_entrada = _registro_archivo(archivos, seleccionada)
        ruta_entrada, bytes_entrada, hash_entrada = _validar_archivo(
            configuracion,
            registro_entrada,
        )

        registros_documentacion = [
            archivo
            for archivo in archivos
            if isinstance(archivo, dict)
            and isinstance(archivo.get("path"), str)
            and archivo["path"].startswith(prefijo_publico)
            and archivo["path"] != seleccionada
        ]
        if not registros_documentacion:
            raise ManifiestoError(f"No hay documentación pública para {dataset_id}")
        rutas_documentacion = tuple(
            _validar_archivo(configuracion, registro)[0]
            for registro in registros_documentacion
        )

        extension = ruta_entrada.suffix.lower()
        if extension == ".csv":
            formato = "csv"
            if hoja_seleccionada is not None:
                raise ManifiestoError(f"Un CSV no puede declarar hoja para {dataset_id}")
        elif extension == ".xlsx":
            formato = "xlsx"
            if not isinstance(hoja_seleccionada, str) or not hoja_seleccionada:
                raise ManifiestoError(f"El XLSX debe declarar una hoja para {dataset_id}")
        else:
            raise ManifiestoError(f"Formato no autorizado para {dataset_id}: {extension}")

        resultado[dataset_id] = DatasetValidado(
            dataset_id=dataset_id,
            nombre=nombre,
            ruta_entrada=ruta_entrada,
            formato=formato,
            hoja_seleccionada=hoja_seleccionada,
            sha256=hash_entrada,
            bytes=bytes_entrada,
            filas_esperadas=filas_esperadas,
            columnas_esperadas=columnas_esperadas,
            documentacion_publica=rutas_documentacion,
            solo_piloto=bool(entrada.get("pilot_only", False)),
        )

    return MappingProxyType(resultado)
