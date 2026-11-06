"""Registro y control de las llamadas al modelo realizadas por LangGraph."""

from __future__ import annotations

import time
from typing import Any, Mapping, Sequence

from langchain_core.messages import AIMessage, BaseMessage

from experimento.capa_comun import CapaComunError

from .cliente_openai import (
    FalloAdaptador,
    descongelar,
    hash_json,
    json_canonico,
    mensaje_visible,
    texto_mensaje,
    uso_modelo,
    utc_actual,
)


FASES_ROL = {
    "planner": "planning",
    "analyst_initial": "analysis",
    "reviewer": "review",
    "analyst_correction": "correction",
}
ROL_TRAZA = {
    "planner": "planner",
    "analyst_initial": "analyst",
    "reviewer": "reviewer",
    "analyst_correction": "analyst",
}


class RegistroModeloLangGraph:
    """Comprueba los límites y registra cada petición al modelo y su resultado."""

    def _llamar_modelo(
        self,
        rol: str,
        role_execution_id: str,
        mensajes: Sequence[BaseMessage],
        schemas: Sequence[Mapping[str, Any]],
        parent_event_id: str,
    ) -> tuple[AIMessage, str, str]:
        visibles = [mensaje_visible(mensaje) for mensaje in mensajes]
        caracteres_estimados = sum(len(str(mensaje.content)) for mensaje in mensajes)
        entrada_estimada = max(caracteres_estimados // 4, 1)
        retry_of: str | None = None
        intento = 1
        while True:
            autorizacion = self.limites.autorizar_modelo(
                rol,
                FASES_ROL[rol],
                entrada_estimada,
            )
            if not autorizacion.autorizada:
                error = CapaComunError(
                    "La llamada al modelo fue bloqueada por el límite "
                    f"{autorizacion.motivo}"
                )
                error_id = self._registrar_error(
                    error,
                    FASES_ROL[rol],
                    ROL_TRAZA[rol],
                    "model_authorization",
                    parent_event_id,
                    retryable=False,
                    retry_triggered=False,
                )
                raise FalloAdaptador(str(error), error_id)
            self.contador_modelo += 1
            model_call_id = f"{self.contexto.run_id}__model_{self.contador_modelo:03d}"
            inicio_utc = utc_actual()
            inicio = time.perf_counter_ns()
            parametros = descongelar(
                self.configuracion.datos["model"]["request_parameters"]
            )
            parametros["max_output_tokens"] = autorizacion.max_output_tokens
            evento_inicio = self.traza.registrar(
                "model_call_started",
                FASES_ROL[rol],
                ROL_TRAZA[rol],
                "model",
                {
                    "model_call_id": model_call_id,
                    "role_execution_id": role_execution_id,
                    "attempt": intento,
                    "retry_of": retry_of,
                    "provider": self.configuracion.datos["model"]["provider"],
                    "requested_model": self.configuracion.datos["model"][
                        "requested_model"
                    ],
                    "api": self.configuracion.datos["model"]["api"],
                    "requested_service_tier": self.configuracion.datos["model"][
                        "request_parameters"
                    ]["service_tier"],
                    "reasoning_effort": self.configuracion.datos["model"][
                        "request_parameters"
                    ]["reasoning"]["effort"],
                    "active_parameters": parametros,
                    "prompt_version": self.configuracion.datos["versions"]["prompts"],
                    "prompt_sha256": hash_json(visibles),
                    "message_count": len(visibles),
                    "tool_count": len(schemas),
                    "visible_messages": visibles,
                    "tool_schema_sha256": hash_json(list(schemas)),
                    "provider_request_id": None,
                },
                correlation_id=model_call_id,
                parent_event_id=parent_event_id,
            )
            self.limites.registrar_modelo_iniciado(rol, FASES_ROL[rol])
            try:
                mensaje = self.modelo.invocar(
                    mensajes,
                    schemas,
                    autorizacion.max_output_tokens,
                )
                uso = uso_modelo(mensaje)
                coste = self.limites.registrar_uso_modelo(
                    uso["input_tokens"],
                    uso["output_tokens"],
                    uso["total_tokens"],
                    uso["cached_input_tokens"],
                    uso["reasoning_output_tokens"],
                    FASES_ROL[rol],
                    rol,
                )
                metadatos = dict(mensaje.response_metadata or {})
                llamadas = [
                    {
                        "id": llamada.get("id"),
                        "name": llamada.get("name"),
                        "arguments": llamada.get("args"),
                    }
                    for llamada in mensaje.tool_calls
                ]
                evento_fin = self.traza.registrar(
                    "model_call_finished",
                    FASES_ROL[rol],
                    ROL_TRAZA[rol],
                    "model",
                    {
                        "model_call_id": model_call_id,
                        "provider_response_id": metadatos.get("id") or mensaje.id,
                        "reported_service_tier": metadatos.get("service_tier"),
                        "outcome": "success",
                        "finish_reason": metadatos.get("finish_reason"),
                        "visible_output": texto_mensaje(mensaje),
                        "requested_tool_calls": llamadas,
                        "input_tokens": uso["input_tokens"],
                        "output_tokens": uso["output_tokens"],
                        "total_tokens": uso["total_tokens"],
                        "cached_input_tokens": uso["cached_input_tokens"],
                        "reasoning_output_tokens": uso["reasoning_output_tokens"],
                        "usage_extensions": {
                            "reported_model": metadatos.get("model_name")
                            or metadatos.get("model"),
                            "input_token_details": uso["input_token_details"],
                            "output_token_details": uso["output_token_details"],
                        },
                        "estimated_cost": float(coste),
                        "started_at_utc": inicio_utc,
                        "finished_at_utc": utc_actual(),
                        "duration_ms": max(
                            (time.perf_counter_ns() - inicio) // 1_000_000,
                            0,
                        ),
                    },
                    correlation_id=model_call_id,
                    parent_event_id=evento_inicio,
                )
                return mensaje, model_call_id, evento_fin
            except Exception as exc:
                retryable = self._es_error_transitorio(exc)
                puede_reintentar = False
                if retryable and intento == 1:
                    puede_reintentar = self.limites.registrar_reintento(
                        FASES_ROL[rol],
                        rol,
                    )
                error_id = self._registrar_error(
                    exc,
                    FASES_ROL[rol],
                    ROL_TRAZA[rol],
                    "model_call",
                    evento_inicio,
                    retryable=retryable,
                    retry_triggered=puede_reintentar,
                )
                evento_fallo = self.traza.registrar(
                    "model_call_failed",
                    FASES_ROL[rol],
                    ROL_TRAZA[rol],
                    "model",
                    {
                        "model_call_id": model_call_id,
                        "provider_request_id": None,
                        "provider_response_id": None,
                        "duration_ms": max(
                            (time.perf_counter_ns() - inicio) // 1_000_000,
                            0,
                        ),
                        "error_id": error_id,
                        "partial_usage": None,
                        "retry_planned": puede_reintentar,
                    },
                    correlation_id=model_call_id,
                    parent_event_id=self.traza.ultimo_evento_id,
                )
                if not puede_reintentar:
                    raise FalloAdaptador(str(exc), error_id) from exc
                siguiente = (
                    f"{self.contexto.run_id}__model_{self.contador_modelo + 1:03d}"
                )
                self.traza.registrar(
                    "retry_recorded",
                    FASES_ROL[rol],
                    ROL_TRAZA[rol],
                    "framework_adapter",
                    {
                        "retry_id": (
                            f"{self.contexto.run_id}__retry_{self.limites.retries:03d}"
                        ),
                        "target_type": "model_call",
                        "failed_operation_id": model_call_id,
                        "new_operation_id": siguiente,
                        "reason": type(exc).__name__,
                        "attempt": intento + 1,
                        "authorized": True,
                    },
                    parent_event_id=evento_fallo,
                )
                retry_of = model_call_id
                intento += 1
                parent_event_id = self.traza.ultimo_evento_id

    @staticmethod
    def _es_error_transitorio(exc: Exception) -> bool:
        if hasattr(exc, "retryable"):
            return bool(getattr(exc, "retryable"))
        try:
            from openai import (
                APIConnectionError,
                APITimeoutError,
                InternalServerError,
                RateLimitError,
            )

            return isinstance(
                exc,
                (
                    APIConnectionError,
                    APITimeoutError,
                    InternalServerError,
                    RateLimitError,
                ),
            )
        except ImportError:
            return False

    def _registrar_error(
        self,
        exc: Exception,
        fase: str,
        rol: str,
        operacion: str,
        related_event_id: str,
        retryable: bool,
        retry_triggered: bool,
    ) -> str:
        self.contador_errores += 1
        error_id = f"ERR-ADAPTER-{self.contador_errores:06d}"
        self.limites.registrar_error(error_id, "error")
        categoria = "model" if operacion.startswith("model") else (
            "format" if operacion == "role_output" else "framework"
        )
        severidad = "recoverable" if retry_triggered else "fatal"
        self.traza.registrar(
            "error_recorded",
            fase,
            rol,
            "framework_adapter",
            {
                "error_id": error_id,
                "category": categoria,
                "code": type(exc).__name__,
                "message": str(exc) or "Error sin mensaje",
                "severity": severidad,
                "related_event_id": related_event_id,
                "operation": operacion,
                "retryable": retryable,
                "retry_triggered": retry_triggered,
                "exception_type": type(exc).__name__,
                "technical_trace": None,
            },
            parent_event_id=related_event_id,
        )
        return error_id
