""""Registro de eventos, ocultación de información sensible y comprobación de la traza."""

from __future__ import annotations

import json
import os
import platform
import re
import time
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping

from .configuracion import ConfiguracionExperimento
from .ejecucion import ContextoEjecucion
from .errores import CapaComunError, ConfiguracionError
from .utilidades import sha256_archivo


TIPOS_EVENTO = {
    "run_started",
    "run_finished",
    "trace_closed",
    "state_transition",
    "role_started",
    "role_finished",
    "role_failed",
    "model_call_started",
    "model_call_finished",
    "model_call_failed",
    "tool_call_started",
    "tool_call_finished",
    "tool_call_failed",
    "artifact_written",
    "validation_completed",
    "review_decision",
    "correction_started",
    "correction_finished",
    "error_recorded",
    "retry_recorded",
    "limit_warning",
    "limit_reached",
}
FASES = {
    "setup",
    "planning",
    "analysis",
    "review",
    "correction",
    "final_validation",
    "closure",
}
ROLES = {"runtime", "planner", "analyst", "reviewer"}
FUENTES = {"common_runtime", "framework_adapter", "model", "tool"}
CAMPOS_COMUNES = {
    "schema_version",
    "event_id",
    "sequence",
    "timestamp_utc",
    "elapsed_ms",
    "run_id",
    "framework",
    "dataset_id",
    "repetition",
    "phase",
    "role",
    "source",
    "event_type",
    "correlation_id",
    "parent_event_id",
    "payload",
}
CAMPOS_PAYLOAD: dict[str, set[str]] = {
    "run_started": {
        "contract_version",
        "trace_schema_version",
        "prompt_version",
        "tools_version",
        "output_schema_version",
        "framework_version",
        "python_version",
        "dependencies",
        "provider",
        "requested_model",
        "api",
        "requested_service_tier",
        "reasoning_effort",
        "request_parameters",
        "dataset_sha256",
        "dataset_manifest_version",
        "public_documentation",
        "experiment_seed",
        "limits_version",
        "pricing_table_id",
        "prices",
        "configuration_sha256",
        "prompt_hashes",
        "started_at_utc",
    },
    "state_transition": {"from_state", "to_state", "reason", "trigger_event_id"},
    "role_started": {"role_execution_id", "role_name", "attempt", "started_at_utc"},
    "role_finished": {
        "role_execution_id",
        "role_name",
        "attempt",
        "finished_at_utc",
        "duration_ms",
        "outcome",
        "output_artifact",
        "error_id",
    },
    "role_failed": {
        "role_execution_id",
        "role_name",
        "attempt",
        "finished_at_utc",
        "duration_ms",
        "outcome",
        "output_artifact",
        "error_id",
    },
    "run_finished": {
        "final_status",
        "reason_code",
        "reason",
        "started_at_utc",
        "finished_at_utc",
        "duration_ms",
        "final_validation_id",
        "totals",
        "correction_used",
        "correction_request_id",
        "limits_reached",
        "artifacts",
    },
    "trace_closed": {
        "event_count",
        "last_sequence",
        "events_by_type",
        "integrity_status",
        "required_fields_expected",
        "required_fields_valid",
        "required_fields_missing_or_invalid",
        "failed_integrity_checks",
    },
    "model_call_started": {
        "model_call_id",
        "role_execution_id",
        "attempt",
        "retry_of",
        "provider",
        "requested_model",
        "api",
        "requested_service_tier",
        "reasoning_effort",
        "active_parameters",
        "prompt_version",
        "prompt_sha256",
        "message_count",
        "tool_count",
        "visible_messages",
        "tool_schema_sha256",
        "provider_request_id",
    },
    "model_call_finished": {
        "model_call_id",
        "provider_response_id",
        "reported_service_tier",
        "outcome",
        "finish_reason",
        "visible_output",
        "requested_tool_calls",
        "input_tokens",
        "output_tokens",
        "total_tokens",
        "cached_input_tokens",
        "reasoning_output_tokens",
        "usage_extensions",
        "estimated_cost",
        "started_at_utc",
        "finished_at_utc",
        "duration_ms",
    },
    "model_call_failed": {
        "model_call_id",
        "provider_request_id",
        "provider_response_id",
        "duration_ms",
        "error_id",
        "partial_usage",
        "retry_planned",
    },
    "tool_call_started": {
        "tool_call_id",
        "tool_name",
        "model_call_id",
        "role_execution_id",
        "arguments",
        "attempt",
        "retry_of",
        "tool_version",
    },
    "tool_call_finished": {
        "tool_call_id",
        "tool_name",
        "duration_ms",
        "outcome",
        "response",
        "affected_files",
        "error_id",
        "retry_planned",
    },
    "tool_call_failed": {
        "tool_call_id",
        "tool_name",
        "duration_ms",
        "outcome",
        "response",
        "affected_files",
        "error_id",
        "retry_planned",
    },
    "error_recorded": {
        "error_id",
        "category",
        "code",
        "message",
        "severity",
        "related_event_id",
        "operation",
        "retryable",
        "retry_triggered",
        "exception_type",
        "technical_trace",
    },
    "retry_recorded": {
        "retry_id",
        "target_type",
        "failed_operation_id",
        "new_operation_id",
        "reason",
        "attempt",
        "authorized",
    },
    "limit_warning": {
        "limit_type",
        "configured_value",
        "unit",
        "observed_value",
        "scope",
        "action",
    },
    "limit_reached": {
        "limit_type",
        "configured_value",
        "unit",
        "observed_value",
        "scope",
        "action",
    },
    "artifact_written": {
        "artifact_name",
        "relative_path",
        "writer",
        "phase_written",
        "bytes",
        "sha256",
        "format",
        "replaces_sha256",
        "origin_event_id",
    },
    "validation_completed": {
        "trigger",
        "automatic",
        "validation_id",
        "validation_status",
        "response",
    },
    "review_decision": {
        "review_decision_id",
        "decision",
        "summary",
        "findings",
        "correction_allowed",
        "correction_requested",
        "reviewed_artifact_hashes",
    },
    "correction_started": {
        "correction_request_id",
        "finding_ids",
        "potentially_affected_artifacts",
        "initial_hashes",
    },
    "correction_finished": {
        "correction_request_id",
        "outcome",
        "declared_changes",
        "modified_files",
        "post_validation_id",
        "addressed_findings",
        "unresolved_findings",
    },
}

_PATRON_CLAVE = re.compile(r"sk-[A-Za-z0-9_-]{10,}")
_PATRON_BEARER = re.compile(r"(?i)bearer\s+[A-Za-z0-9._~+/=-]+")
_PATRON_RUTA_WINDOWS = re.compile(
    r"(?i)(?<!\w)[A-Z]:(?:/|\\(?![nrtbf](?:\s|$)))[^\s\"']+"
)
_CLAVES_SENSIBLES = {
    "api_key",
    "openai_api_key",
    "authorization",
    "cookie",
    "set_cookie",
    "password",
    "secret",
    "access_token",
    "refresh_token",
}


def _utc_iso(instante: datetime | None = None) -> str:
    """Convierte una fecha al formato UTC utilizado en la traza."""
    valor = instante or datetime.now(timezone.utc)
    if valor.tzinfo is None or valor.utcoffset() is None:
        raise ConfiguracionError("Las fechas de la traza deben incluir zona horaria")
    return valor.astimezone(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _sanear(valor: Any, clave: str | None = None) -> tuple[Any, int]:
    """Oculta los datos sensibles reconocidos y cuenta las sustituciones."""
    if clave is not None and clave.lower() in _CLAVES_SENSIBLES:
        return "[REDACTED]", 1
    if isinstance(valor, Mapping):
        resultado: dict[str, Any] = {}
        total = 0
        for subclave, contenido in valor.items():
            limpio, cambios = _sanear(contenido, str(subclave))
            resultado[str(subclave)] = limpio
            total += cambios
        return resultado, total
    if isinstance(valor, (list, tuple)):
        resultado_lista = []
        total = 0
        for contenido in valor:
            limpio, cambios = _sanear(contenido)
            resultado_lista.append(limpio)
            total += cambios
        return resultado_lista, total
    if isinstance(valor, Path):
        return "[REDACTED]", 1
    if isinstance(valor, str):
        limpio = valor
        cambios = 0
        for patron in (_PATRON_CLAVE, _PATRON_BEARER, _PATRON_RUTA_WINDOWS):
            limpio, encontrados = patron.subn("[REDACTED]", limpio)
            cambios += encontrados
        if "datasets/reference_private" in limpio.replace("\\", "/").lower():
            return "[REDACTED]", cambios + 1
        if "datasets/raw" in limpio.replace("\\", "/").lower():
            return "[REDACTED]", cambios + 1
        return limpio, cambios
    return valor, 0


@dataclass(frozen=True, slots=True)
class ResultadoIntegridad:
    estado: str
    campos_esperados: int
    campos_validos: int
    campos_ausentes_o_invalidos: int
    comprobaciones_fallidas: tuple[str, ...]
    eventos_por_tipo: Mapping[str, int]

    @property
    def porcentaje(self) -> float:
        """Calcula el porcentaje de campos obligatorios presentes."""
        if self.campos_esperados == 0:
            return 0.0
        return round(self.campos_validos / self.campos_esperados * 100, 4)


def _validar_eventos(
    eventos: list[dict[str, Any]],
    validar_resumen_cierre: bool = True,
) -> ResultadoIntegridad:
    """Comprueba los campos, la secuencia y las relaciones entre eventos."""
    fallos: list[str] = []
    incompletos: list[str] = []
    esperados = 0
    validos = 0
    eventos_por_tipo = Counter()
    ids_evento: set[str] = set()
    identidad: tuple[Any, ...] | None = None
    secuencia_anterior = 0
    elapsed_anterior = -1

    for indice, evento in enumerate(eventos, start=1):
        if not isinstance(evento, dict):
            fallos.append(f"La línea {indice} no es un objeto JSON")
            continue
        tipo = evento.get("event_type")
        eventos_por_tipo[str(tipo)] += 1
        esperados += len(CAMPOS_COMUNES)
        for campo in CAMPOS_COMUNES:
            if campo in evento:
                validos += 1
            else:
                fallos.append(f"Falta {campo} en el evento {indice}")

        if tipo not in TIPOS_EVENTO:
            fallos.append(f"Tipo de evento no autorizado en la línea {indice}: {tipo}")
            continue
        payload = evento.get("payload")
        requeridos = CAMPOS_PAYLOAD.get(tipo, set())
        esperados += len(requeridos)
        if not isinstance(payload, dict):
            fallos.append(f"payload no es un objeto en el evento {indice}")
        else:
            for campo in requeridos:
                if campo in payload:
                    validos += 1
                else:
                    fallos.append(f"Falta payload.{campo} en el evento {indice}")

        if evento.get("schema_version") != "1.0":
            fallos.append(f"schema_version inválida en el evento {indice}")
        if evento.get("phase") not in FASES:
            fallos.append(f"phase inválida en el evento {indice}")
        if evento.get("role") not in ROLES:
            fallos.append(f"role inválido en el evento {indice}")
        if evento.get("source") not in FUENTES:
            fallos.append(f"source inválido en el evento {indice}")
        if not isinstance(evento.get("sequence"), int) or isinstance(evento.get("sequence"), bool):
            fallos.append(f"sequence inválida en el evento {indice}")
        elif evento["sequence"] != secuencia_anterior + 1:
            fallos.append(f"sequence no consecutiva en el evento {indice}")
        else:
            secuencia_anterior = evento["sequence"]
        if not isinstance(evento.get("elapsed_ms"), int) or evento.get("elapsed_ms", -1) < 0:
            fallos.append(f"elapsed_ms inválido en el evento {indice}")
        elif evento["elapsed_ms"] < elapsed_anterior:
            fallos.append(f"elapsed_ms decrece en el evento {indice}")
        else:
            elapsed_anterior = evento["elapsed_ms"]

        event_id = evento.get("event_id")
        if not isinstance(event_id, str) or not event_id:
            fallos.append(f"event_id inválido en el evento {indice}")
        elif event_id in ids_evento:
            fallos.append(f"event_id duplicado: {event_id}")
        else:
            ids_evento.add(event_id)

        actual = (
            evento.get("run_id"),
            evento.get("framework"),
            evento.get("dataset_id"),
            evento.get("repetition"),
        )
        if identidad is None:
            identidad = actual
        elif actual != identidad:
            fallos.append(f"Identidad de ejecución incoherente en el evento {indice}")

    tipos = [evento.get("event_type") for evento in eventos if isinstance(evento, dict)]
    ciclos = {
        "run_started": CAMPOS_PAYLOAD["run_started"],
        "run_finished": CAMPOS_PAYLOAD["run_finished"],
        "trace_closed": CAMPOS_PAYLOAD["trace_closed"],
    }
    for tipo, campos in ciclos.items():
        cantidad = tipos.count(tipo)
        if cantidad != 1:
            incompletos.append(f"Debe existir exactamente un evento {tipo}")
            if cantidad == 0:
                esperados += len(CAMPOS_COMUNES) + len(campos)
    if tipos and tipos[0] != "run_started":
        fallos.append("run_started no es el primer evento")
    if tipos and tipos[-1] != "trace_closed":
        incompletos.append("trace_closed no es el último evento")

    _validar_cierres_operaciones(eventos, incompletos)
    _validar_referencias(eventos, ids_evento, fallos)

    if validar_resumen_cierre and tipos.count("trace_closed") == 1:
        cierre = next(evento for evento in eventos if evento.get("event_type") == "trace_closed")
        payload_cierre = cierre.get("payload", {})
        if payload_cierre.get("event_count") != len(eventos):
            fallos.append("trace_closed.event_count no coincide con la traza")
        if payload_cierre.get("last_sequence") != len(eventos):
            fallos.append("trace_closed.last_sequence no coincide con la traza")
        if payload_cierre.get("events_by_type") != dict(eventos_por_tipo):
            fallos.append("trace_closed.events_by_type no coincide con la traza")

    todos_fallos = tuple(dict.fromkeys([*fallos, *incompletos]))
    ausentes = max(esperados - validos, 0)
    if fallos:
        estado = "invalid"
    elif incompletos:
        estado = "incomplete"
    else:
        estado = "valid"
    return ResultadoIntegridad(
        estado=estado,
        campos_esperados=esperados,
        campos_validos=validos,
        campos_ausentes_o_invalidos=ausentes,
        comprobaciones_fallidas=todos_fallos,
        eventos_por_tipo=dict(eventos_por_tipo),
    )


def _validar_cierres_operaciones(
    eventos: Iterable[Mapping[str, Any]],
    fallos: list[str],
) -> None:
    """Comprueba que las operaciones iniciadas tengan un evento de finalización."""
    pares = [
        ("role_started", {"role_finished", "role_failed"}, "role_execution_id"),
        ("model_call_started", {"model_call_finished", "model_call_failed"}, "model_call_id"),
        ("tool_call_started", {"tool_call_finished", "tool_call_failed"}, "tool_call_id"),
    ]
    lista = list(eventos)
    for inicio, cierres, campo in pares:
        iniciadas = {
            evento.get("payload", {}).get(campo)
            for evento in lista
            if evento.get("event_type") == inicio
        }
        terminadas = {
            evento.get("payload", {}).get(campo)
            for evento in lista
            if evento.get("event_type") in cierres
        }
        pendientes = {identificador for identificador in iniciadas - terminadas if identificador}
        if pendientes:
            fallos.append(f"Operaciones {inicio} sin cierre: {sorted(pendientes)}")


def _validar_referencias(
    eventos: Iterable[Mapping[str, Any]],
    ids_evento: set[str],
    fallos: list[str],
) -> None:
    """Comprueba las referencias a eventos anteriores y errores registrados."""
    vistos: set[str] = set()
    errores = {
        evento.get("payload", {}).get("error_id")
        for evento in eventos
        if evento.get("event_type") == "error_recorded"
    }
    for evento in eventos:
        padre = evento.get("parent_event_id")
        if padre is not None and padre not in vistos:
            fallos.append(f"parent_event_id no referencia un evento anterior: {padre}")
        payload = evento.get("payload", {})
        error_id = payload.get("error_id") if isinstance(payload, dict) else None
        if error_id is not None and evento.get("event_type") != "error_recorded" and error_id not in errores:
            fallos.append(f"error_id sin error_recorded relacionado: {error_id}")
        event_id = evento.get("event_id")
        if isinstance(event_id, str) and event_id in ids_evento:
            vistos.add(event_id)


def validar_archivo_traza(ruta: Path) -> ResultadoIntegridad:
    """Lee y valida una traza JSONL completa."""

    eventos: list[dict[str, Any]] = []
    try:
        with ruta.open("r", encoding="utf-8") as archivo:
            for numero, linea in enumerate(archivo, start=1):
                try:
                    evento = json.loads(linea)
                except json.JSONDecodeError:
                    return ResultadoIntegridad(
                        estado="invalid",
                        campos_esperados=len(CAMPOS_COMUNES),
                        campos_validos=0,
                        campos_ausentes_o_invalidos=len(CAMPOS_COMUNES),
                        comprobaciones_fallidas=(f"JSON inválido en la línea {numero}",),
                        eventos_por_tipo={},
                    )
                eventos.append(evento)
    except OSError as exc:
        raise CapaComunError("No puede leerse trace.jsonl") from exc
    return _validar_eventos(eventos)


class EscritorTraza:
    """Registra los eventos de la ejecución y los guarda inmediatamente en disco."""

    def __init__(
        self,
        contexto: ContextoEjecucion,
        configuracion: ConfiguracionExperimento,
        framework_version: str,
        dependencies: Mapping[str, str],
        prompt_hashes: Mapping[str, str],
    ) -> None:
        self.contexto = contexto
        self.configuracion = configuracion
        self.ruta = contexto.directorio_salida / "trace.jsonl"
        if self.ruta.exists():
            raise CapaComunError("trace.jsonl ya existe en la ejecución")
        self._inicio_monotono = time.perf_counter_ns()
        self._inicio_utc = _utc_iso()
        self._eventos: list[dict[str, Any]] = []
        self._cerrada = False
        self._archivo = self.ruta.open("x", encoding="utf-8", newline="\n")
        payload = self._crear_payload_inicio(
            framework_version,
            dependencies,
            prompt_hashes,
        )
        self._registrar_interno(
            "run_started",
            "setup",
            "runtime",
            "common_runtime",
            payload,
        )

    def _crear_payload_inicio(
        self,
        framework_version: str,
        dependencies: Mapping[str, str],
        prompt_hashes: Mapping[str, str],
    ) -> dict[str, Any]:
        """Reúne la configuración y los datos que identifican el inicio de la ejecución."""
        datos = self.configuracion.datos
        documentos = []
        for ruta in self.contexto.dataset.documentacion_publica:
            documentos.append(
                {
                    "path": ruta.relative_to(self.configuracion.raiz_tfm).as_posix(),
                    "sha256": sha256_archivo(ruta),
                }
            )
        return {
            "contract_version": datos["versions"]["contract"],
            "trace_schema_version": datos["versions"]["trace_schema"],
            "prompt_version": datos["versions"]["prompts"],
            "tools_version": datos["versions"]["tools"],
            "output_schema_version": datos["versions"]["output_schemas"],
            "framework_version": framework_version,
            "python_version": platform.python_version(),
            "dependencies": dict(dependencies),
            "provider": datos["model"]["provider"],
            "requested_model": datos["model"]["requested_model"],
            "api": datos["model"]["api"],
            "requested_service_tier": datos["model"]["request_parameters"]["service_tier"],
            "reasoning_effort": datos["model"]["request_parameters"]["reasoning"]["effort"],
            "request_parameters": dict(datos["model"]["request_parameters"]),
            "dataset_sha256": self.contexto.dataset.sha256,
            "dataset_manifest_version": datos["versions"]["dataset_manifest"],
            "public_documentation": documentos,
            "experiment_seed": datos["security"]["experiment_seed"],
            "limits_version": datos["versions"]["limits"],
            "pricing_table_id": datos["pricing"]["table_version"],
            "prices": {
                "currency": datos["pricing"]["currency"],
                "consulted_on": datos["pricing"]["consulted_on"],
                "source": datos["pricing"]["source"],
                "per_million_tokens": dict(datos["pricing"]["per_million_tokens"]),
            },
            "configuration_sha256": self.configuracion.sha256,
            "prompt_hashes": dict(prompt_hashes),
            "started_at_utc": self._inicio_utc,
        }

    @property
    def ultimo_evento_id(self) -> str:
        return self._eventos[-1]["event_id"]

    @property
    def started_at_utc(self) -> str:
        return self._inicio_utc

    def elapsed_ms(self) -> int:
        return max((time.perf_counter_ns() - self._inicio_monotono) // 1_000_000, 0)

    def registrar(
        self,
        event_type: str,
        phase: str,
        role: str,
        source: str,
        payload: Mapping[str, Any],
        correlation_id: str | None = None,
        parent_event_id: str | None = None,
    ) -> str:
        """Añade a la traza un evento de la ejecución."""
        if event_type in {"run_started", "trace_closed"}:
            raise CapaComunError(f"{event_type} solo puede gestionarlo el escritor de traza")
        return self._registrar_interno(
            event_type,
            phase,
            role,
            source,
            payload,
            correlation_id,
            parent_event_id,
        )

    def _registrar_interno(
        self,
        event_type: str,
        phase: str,
        role: str,
        source: str,
        payload: Mapping[str, Any],
        correlation_id: str | None = None,
        parent_event_id: str | None = None,
        permitir_aviso_saneamiento: bool = True,
    ) -> str:
        """Comprueba el evento, oculta datos sensibles y prepara su escritura."""
        if self._cerrada:
            raise CapaComunError("La traza ya está cerrada")
        if event_type not in TIPOS_EVENTO or phase not in FASES or role not in ROLES or source not in FUENTES:
            raise CapaComunError("Evento, fase, rol o fuente no autorizados")
        requeridos = CAMPOS_PAYLOAD.get(event_type, set())
        faltantes = requeridos - set(payload)
        if faltantes:
            raise CapaComunError(
                f"Faltan campos de payload para {event_type}: {sorted(faltantes)}"
            )

        payload_limpio, saneamientos = _sanear(dict(payload))
        secuencia = len(self._eventos) + 1
        event_id = f"{self.contexto.run_id}__e{secuencia:06d}"
        evento = {
            "schema_version": self.configuracion.datos["versions"]["trace_schema"],
            "event_id": event_id,
            "sequence": secuencia,
            "timestamp_utc": _utc_iso(),
            "elapsed_ms": self.elapsed_ms(),
            "run_id": self.contexto.run_id,
            "framework": self.contexto.framework_id,
            "dataset_id": self.contexto.dataset.dataset_id,
            "repetition": self.contexto.repeticion,
            "phase": phase,
            "role": role,
            "source": source,
            "event_type": event_type,
            "correlation_id": correlation_id,
            "parent_event_id": parent_event_id,
            "payload": payload_limpio,
        }
        self._escribir(evento)

        if saneamientos and permitir_aviso_saneamiento:
            error_id = f"ERR-TRACE-{secuencia:06d}"
            self._registrar_interno(
                "error_recorded",
                phase,
                "runtime",
                "common_runtime",
                {
                    "error_id": error_id,
                    "category": "environment",
                    "code": "TRACE_CONTENT_REDACTED",
                    "message": f"Se sanearon {saneamientos} valores antes de escribir la traza",
                    "severity": "warning",
                    "related_event_id": event_id,
                    "operation": event_type,
                    "retryable": False,
                    "retry_triggered": False,
                    "exception_type": None,
                    "technical_trace": None,
                },
                correlation_id=correlation_id,
                parent_event_id=event_id,
                permitir_aviso_saneamiento=False,
            )
        return event_id

    def _escribir(self, evento: dict[str, Any]) -> None:
        """Añade el evento al archivo y fuerza su guardado en disco."""
        linea = json.dumps(evento, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
        self._archivo.write(linea + "\n")
        self._archivo.flush()
        os.fsync(self._archivo.fileno())
        self._eventos.append(evento)

    def cerrar(self) -> ResultadoIntegridad:
        """Comprueba la traza, registra su cierre y devuelve el resultado de integridad."""
        if self._cerrada:
            raise CapaComunError("La traza ya está cerrada")
        secuencia = len(self._eventos) + 1
        payload_provisional = {
            "event_count": secuencia,
            "last_sequence": secuencia,
            "events_by_type": {},
            "integrity_status": "incomplete",
            "required_fields_expected": 0,
            "required_fields_valid": 0,
            "required_fields_missing_or_invalid": 0,
            "failed_integrity_checks": [],
        }
        evento_cierre = self._construir_cierre(payload_provisional)
        informe = _validar_eventos([*self._eventos, evento_cierre], validar_resumen_cierre=False)
        conteos = Counter(
            evento["event_type"] for evento in [*self._eventos, evento_cierre]
        )
        evento_cierre["payload"] = {
            "event_count": secuencia,
            "last_sequence": secuencia,
            "events_by_type": dict(conteos),
            "integrity_status": informe.estado,
            "required_fields_expected": informe.campos_esperados,
            "required_fields_valid": informe.campos_validos,
            "required_fields_missing_or_invalid": informe.campos_ausentes_o_invalidos,
            "failed_integrity_checks": list(informe.comprobaciones_fallidas),
        }
        self._escribir(evento_cierre)
        self._cerrada = True
        self._archivo.close()
        return validar_archivo_traza(self.ruta)

    def _construir_cierre(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        """Prepara el evento final con el resumen de la traza."""
        secuencia = len(self._eventos) + 1
        return {
            "schema_version": self.configuracion.datos["versions"]["trace_schema"],
            "event_id": f"{self.contexto.run_id}__e{secuencia:06d}",
            "sequence": secuencia,
            "timestamp_utc": _utc_iso(),
            "elapsed_ms": self.elapsed_ms(),
            "run_id": self.contexto.run_id,
            "framework": self.contexto.framework_id,
            "dataset_id": self.contexto.dataset.dataset_id,
            "repetition": self.contexto.repeticion,
            "phase": "closure",
            "role": "runtime",
            "source": "common_runtime",
            "event_type": "trace_closed",
            "correlation_id": None,
            "parent_event_id": self.ultimo_evento_id,
            "payload": dict(payload),
        }

    def abandonar(self) -> None:
        """Cierra el archivo tras un fallo sin añadir eventos que no han ocurrido."""

        if not self._cerrada:
            self._archivo.flush()
            os.fsync(self._archivo.fileno())
            self._archivo.close()
            self._cerrada = True
