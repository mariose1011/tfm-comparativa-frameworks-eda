"""Validación final y cierre técnico común de una ejecución."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping

from .herramientas import HerramientasComunes
from .limites import ControlLimites
from .traza import EscritorTraza, ResultadoIntegridad
from .validacion import determinar_estado_terminal


@dataclass(frozen=True, slots=True)
class ResultadoCierre:
    """Reúne el estado final, su motivo y las comprobaciones de las salidas y la traza."""
    estado: str
    motivo: str
    validacion: Mapping[str, Any]
    integridad_traza: ResultadoIntegridad


def _utc_actual() -> str:
    """Devuelve la fecha y hora actuales en UTC."""
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace(
        "+00:00",
        "Z",
    )


def cerrar_ejecucion_comun(
    herramientas: HerramientasComunes,
    limites: ControlLimites,
    traza: EscritorTraza,
    dataset_cargado: bool,
    *,
    flujo_roles_completo: bool,
    decision_revision: str | None,
    correccion_resuelta: bool = True,
    correction_used: bool = False,
    correction_request_id: str | None = None,
    estado_origen: str = "final_validation",
) -> ResultadoCierre:
    """Comprueba las salidas, registra el estado final y cierra la traza."""

    respuesta = herramientas.validate_outputs(
        {},
        "runtime",
        trigger="final",
        automatic=True,
        parent_event_id=traza.ultimo_evento_id,
    )
    validacion = respuesta["data"]
    estado, motivo = determinar_estado_terminal(
        validacion,
        dataset_cargado,
        limites_alcanzados=limites.limites_alcanzados,
        flujo_roles_completo=flujo_roles_completo,
        decision_revision=decision_revision,
        correccion_resuelta=correccion_resuelta,
    )
    explicaciones = {
        "DATASET_NOT_LOADED": "El dataset no pudo cargarse",
        "REPORT_MISSING_OR_INVALID": "report.md no existe o no supera su estructura mínima",
        "NO_ANALYTICAL_OUTPUT": "No existe ningún resultado analítico válido",
        "ALL_OUTPUTS_VALID": "Los siete resultados superan la validación común",
        "LIMIT_REACHED_WITH_EVALUABLE_OUTPUT": (
            "Se alcanzó un límite obligatorio después de obtener resultados evaluables"
        ),
        "ROLE_FLOW_INCOMPLETE_WITH_EVALUABLE_OUTPUT": (
            "El flujo de roles no terminó, pero conserva resultados evaluables"
        ),
        "REVIEW_DECISION_MISSING": (
            "El Revisor no emitió una decisión, pero existen resultados evaluables"
        ),
        "REVIEW_CANNOT_REVIEW": (
            "El Revisor no pudo completar la revisión, pero existen resultados evaluables"
        ),
        "CORRECTION_UNRESOLVED": (
            "La corrección terminó con hallazgos sin resolver"
        ),
        "MINIMUM_EVALUABLE_OUTPUT_AVAILABLE": (
            "Existe un mínimo evaluable, pero uno o más requisitos no se cumplen"
        ),
    }
    artefactos = [
        {
            "name": artefacto["name"],
            "exists": artefacto["exists"],
            "size_bytes": artefacto["size_bytes"],
            "schema_valid": artefacto["schema_valid"],
            "sha256": artefacto["sha256"],
        }
        for artefacto in validacion["artifacts"]
    ]
    finalizado = _utc_actual()
    evento_anterior = traza.ultimo_evento_id
    traza.registrar(
        "state_transition",
        "closure",
        "runtime",
        "common_runtime",
        {
            "from_state": estado_origen,
            "to_state": estado,
            "reason": motivo,
            "trigger_event_id": evento_anterior,
        },
        parent_event_id=evento_anterior,
    )
    traza.registrar(
        "run_finished",
        "closure",
        "runtime",
        "common_runtime",
        {
            "final_status": estado,
            "reason_code": motivo,
            "reason": explicaciones[motivo],
            "started_at_utc": traza.started_at_utc,
            "finished_at_utc": finalizado,
            "duration_ms": traza.elapsed_ms(),
            "final_validation_id": validacion["validation_id"],
            "totals": limites.resumen(),
            "correction_used": correction_used,
            "correction_request_id": correction_request_id,
            "limits_reached": list(limites.limites_alcanzados),
            "artifacts": artefactos,
        },
        parent_event_id=traza.ultimo_evento_id,
    )
    integridad = traza.cerrar()
    return ResultadoCierre(
        estado=estado,
        motivo=motivo,
        validacion=validacion,
        integridad_traza=integridad,
    )
