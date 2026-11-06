"""Comprobación y guardado del plan y del informe generados por los roles."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path

from .configuracion import ConfiguracionExperimento
from .ejecucion import ContextoEjecucion
from .errores import CapaComunError
from .traza import EscritorTraza
from .utilidades import sha256_archivo
from .validacion import ENCABEZADOS_INFORME, ENCABEZADOS_PLAN, _secciones_markdown


class ErrorMaterializacion(CapaComunError):
    """Error al comprobar o guardar la respuesta de un rol."""
    pass


@dataclass(frozen=True, slots=True)
class ArtefactoMaterializado:
    """Datos del archivo guardado y de la versión anterior, si existe."""
    nombre: str
    ruta_relativa: str
    bytes: int
    sha256: str
    reemplaza_sha256: str | None


def _validar_markdown(nombre: str, contenido: str) -> None:
    """Comprueba que el documento tenga la estructura Markdown exigida."""
    if not isinstance(contenido, str) or not contenido.strip():
        raise ErrorMaterializacion(f"La respuesta para {nombre} está vacía")
    if contenido.lstrip().startswith("```") and contenido.rstrip().endswith("```"):
        raise ErrorMaterializacion(f"La respuesta para {nombre} está envuelta en código")
    encabezados, secciones = _secciones_markdown(contenido)
    esperados = ENCABEZADOS_PLAN if nombre == "plan.md" else ENCABEZADOS_INFORME
    if encabezados != esperados:
        raise ErrorMaterializacion(f"Los encabezados de {nombre} no coinciden")
    if any(not secciones.get(encabezado, "").strip() for encabezado in esperados):
        raise ErrorMaterializacion(f"{nombre} contiene una sección principal vacía")
    if nombre == "plan.md":
        etapas = re.findall(r"(?m)^## E([1-8])(?:\s|$)", secciones["Plan por etapas"])
        if etapas != [str(numero) for numero in range(1, 9)]:
            raise ErrorMaterializacion("plan.md no contiene exactamente E1 a E8 en orden")


def materializar_markdown_rol(
    configuracion: ConfiguracionExperimento,
    contexto: ContextoEjecucion,
    traza: EscritorTraza,
    nombre: str,
    contenido: str,
    writer: str,
    phase_written: str,
    origin_event_id: str,
) -> ArtefactoMaterializado:
    """Comprueba, guarda y registra plan.md o report.md sin reescribir su contenido."""

    if nombre not in {"plan.md", "report.md"}:
        raise ErrorMaterializacion("Solo pueden materializarse plan.md y report.md")
    if writer not in {"planner", "analyst"}:
        raise ErrorMaterializacion("El rol escritor no está autorizado")
    if nombre == "plan.md" and writer != "planner":
        raise ErrorMaterializacion("plan.md solo puede proceder del Planificador")
    if nombre == "report.md" and writer != "analyst":
        raise ErrorMaterializacion("report.md solo puede proceder del Analista")
    if phase_written not in {"initial", "correction"}:
        raise ErrorMaterializacion("La fase de escritura no está autorizada")
    if nombre == "plan.md" and phase_written != "initial":
        raise ErrorMaterializacion("plan.md no puede modificarse durante la corrección")

    try:
        _validar_markdown(nombre, contenido)
    except ErrorMaterializacion:
        rechazado = contexto.directorio_temporal / f"rejected_{nombre.replace('.', '_')}.txt"
        rechazado.write_text(contenido if isinstance(contenido, str) else repr(contenido), encoding="utf-8")
        raise

    contenido_bytes = contenido.encode("utf-8")
    maximo = configuracion.datos["limits"]["sizes"]["files_max_bytes"][nombre]
    if len(contenido_bytes) > maximo:
        raise ErrorMaterializacion(f"{nombre} supera el tamaño máximo")

    destino = contexto.directorio_salida / nombre
    hash_anterior = sha256_archivo(destino) if destino.is_file() else None
    if nombre == "plan.md" and hash_anterior is not None:
        raise ErrorMaterializacion("plan.md ya existe y no puede sobrescribirse")
    temporal = contexto.directorio_temporal / f"_runtime_materialize_{nombre}"
    temporal.write_bytes(contenido_bytes)
    os.replace(temporal, destino)
    hash_nuevo = sha256_archivo(destino)
    metadatos = ArtefactoMaterializado(
        nombre=nombre,
        ruta_relativa=nombre,
        bytes=destino.stat().st_size,
        sha256=hash_nuevo,
        reemplaza_sha256=hash_anterior,
    )
    fase_traza = "correction" if phase_written == "correction" else (
        "planning" if writer == "planner" else "analysis"
    )
    traza.registrar(
        "artifact_written",
        fase_traza,
        writer,
        "common_runtime",
        {
            "artifact_name": nombre,
            "relative_path": nombre,
            "writer": writer,
            "phase_written": phase_written,
            "bytes": metadatos.bytes,
            "sha256": metadatos.sha256,
            "format": "markdown",
            "replaces_sha256": metadatos.reemplaza_sha256,
            "origin_event_id": origin_event_id,
        },
        parent_event_id=origin_event_id,
    )
    return metadatos
