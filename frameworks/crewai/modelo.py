"""Modelo OpenAI Responses controlado para las tareas nativas de CrewAI."""

from __future__ import annotations

import copy
import json
import os
import time
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Mapping, Protocol, Sequence

from crewai.events.types.llm_events import LLMCallType
from crewai.llms.providers.openai.completion import OpenAICompletion
from pydantic import PrivateAttr

from experimento.capa_comun import CapaComunError, PromptConstruido
from experimento.capa_comun.utilidades import (
    descongelar,
    json_canonico,
    sha256_json,
    utc_actual,
)

from .herramientas import DespachadorHerramientasCrewAI


if TYPE_CHECKING:
    from crewai.agents.agent_builder.base_agent import BaseAgent
    from crewai.task import Task
    from crewai.tools import BaseTool
    from crewai.utilities.types import LLMMessage

    from .sesion import SesionCrewAI


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


class FalloAdaptadorCrewAI(CapaComunError):
    """Fallo del adaptador asociado a un error de la traza común."""

    def __init__(self, mensaje: str, error_id: str | None = None) -> None:
        super().__init__(mensaje)
        self.error_id = error_id


class FabricaModeloCrewAI(Protocol):
    """Contrato mínimo para crear un contexto nuevo por rol."""

    def crear(
        self,
        sesion: SesionCrewAI,
        rol: str,
        role_execution_id: str,
        prompt: PromptConstruido,
        esquemas: Sequence[Mapping[str, Any]],
        despachador: DespachadorHerramientasCrewAI,
    ) -> OpenAICompletion:
        ...


@dataclass(slots=True)
class CapturaLlamada:
    """Datos temporales de una petición individual a OpenAI."""

    model_call_id: str
    role_execution_id: str
    evento_inicio: str
    started_at_utc: str
    inicio_ns: int
    intento: int
    retry_of: str | None
    mensajes: list[dict[str, Any]]
    uso: dict[str, Any] = field(default_factory=dict)
    reported_model: str | None = None
    reported_service_tier: str | None = None
    finalizada: bool = False


class ModeloOpenAICrewAIControlado(OpenAICompletion):
    """Mantiene CrewAI nativo y aplica el contrato justo en la llamada API."""

    _sesion: SesionCrewAI = PrivateAttr()
    _rol: str = PrivateAttr()
    _role_execution_id: str = PrivateAttr()
    _prompt_comun: PromptConstruido = PrivateAttr()
    _esquemas_comunes: list[dict[str, Any]] = PrivateAttr()
    _despachador: DespachadorHerramientasCrewAI = PrivateAttr()
    _captura: CapturaLlamada | None = PrivateAttr(default=None)

    def __init__(
        self,
        sesion: SesionCrewAI,
        rol: str,
        role_execution_id: str,
        prompt: PromptConstruido,
        esquemas: Sequence[Mapping[str, Any]],
        despachador: DespachadorHerramientasCrewAI,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._sesion = sesion
        self._rol = rol
        self._role_execution_id = role_execution_id
        self._prompt_comun = prompt
        self._esquemas_comunes = [descongelar(esquema) for esquema in esquemas]
        self._despachador = despachador

    def call(
        self,
        messages: str | list[LLMMessage],
        tools: list[dict[str, BaseTool]] | None = None,
        callbacks: list[Any] | None = None,
        available_functions: dict[str, Any] | None = None,
        from_task: Task | None = None,
        from_agent: BaseAgent | None = None,
        response_model: type[Any] | None = None,
    ) -> str | Any:
        """Prepara los mensajes comunes, comprueba los límites y registra la petición."""

        mensajes_controlados = self._mensajes_controlados(messages)
        entrada_estimada = max(len(json_canonico(mensajes_controlados)) // 4, 1)
        intento = 1
        retry_of: str | None = None

        while True:
            autorizacion = self._sesion.limites.autorizar_modelo(
                self._rol,
                FASES_ROL[self._rol],
                entrada_estimada,
            )
            if not autorizacion.autorizada:
                error = CapaComunError(
                    "La llamada al modelo fue bloqueada por el límite "
                    f"{autorizacion.motivo}"
                )
                error_id = self._sesion.registrar_error(
                    error,
                    FASES_ROL[self._rol],
                    ROL_TRAZA[self._rol],
                    "model_authorization",
                    self._sesion.traza.ultimo_evento_id,
                    retryable=False,
                    retry_triggered=False,
                )
                raise FalloAdaptadorCrewAI(str(error), error_id)

            self.max_completion_tokens = autorizacion.max_output_tokens
            captura = self._iniciar_llamada(
                mensajes_controlados,
                autorizacion.max_output_tokens,
                intento,
                retry_of,
            )
            self._captura = captura
            try:
                resultado = super().call(
                    mensajes_controlados,
                    tools=tools,
                    callbacks=callbacks,
                    available_functions=available_functions,
                    from_task=from_task,
                    from_agent=from_agent,
                    response_model=response_model,
                )
                if not captura.finalizada:
                    self._finalizar_llamada(
                        resultado,
                        captura.uso,
                        None,
                        None,
                    )
                return resultado
            except Exception as exc:
                if captura.finalizada:
                    raise
                puede_reintentar = self._registrar_fallo_llamada(exc, captura)
                if not puede_reintentar:
                    error_id = getattr(exc, "error_id", None)
                    if not error_id:
                        error_id = self._sesion.ultimo_error_id
                    raise FalloAdaptadorCrewAI(str(exc), error_id) from exc
                retry_of = captura.model_call_id
                intento += 1

    def _mensajes_controlados(
        self,
        messages: str | list[LLMMessage],
    ) -> list[dict[str, Any]]:
        """Conserva el prompt común exacto y solo el historial de herramientas."""

        recibidos: list[Mapping[str, Any]]
        if isinstance(messages, str):
            recibidos = [{"role": "user", "content": messages}]
        else:
            recibidos = [
                mensaje
                for mensaje in messages
                if isinstance(mensaje, Mapping)
            ]

        historial: list[dict[str, Any]] = []
        encontrado = False
        for mensaje in recibidos:
            if mensaje.get("role") == "assistant" and mensaje.get("tool_calls"):
                encontrado = True
            if encontrado:
                historial.append(descongelar(mensaje))

        return [
            {
                "role": "system",
                "content": self._prompt_comun.instruccion_sistema,
            },
            {
                "role": "user",
                "content": self._prompt_comun.contenido_usuario,
            },
            *historial,
        ]

    def _convert_tools_for_responses(
        self,
        tools: list[dict[str, BaseTool]],
    ) -> list[dict[str, Any]]:
        """Entrega a OpenAI los esquemas comunes sin reescritura de CrewAI."""

        return copy.deepcopy(self._esquemas_comunes)

    def _iniciar_llamada(
        self,
        mensajes: list[dict[str, Any]],
        max_output_tokens: int,
        intento: int,
        retry_of: str | None,
    ) -> CapturaLlamada:
        self._sesion.contador_modelo += 1
        model_call_id = (
            f"{self._sesion.contexto.run_id}__model_"
            f"{self._sesion.contador_modelo:03d}"
        )
        parametros = descongelar(
            self._sesion.configuracion.datos["model"]["request_parameters"]
        )
        parametros["max_output_tokens"] = max_output_tokens
        inicio_utc = utc_actual()
        inicio_ns = time.perf_counter_ns()
        evento_inicio = self._sesion.traza.registrar(
            "model_call_started",
            FASES_ROL[self._rol],
            ROL_TRAZA[self._rol],
            "model",
            {
                "model_call_id": model_call_id,
                "role_execution_id": self._role_execution_id,
                "attempt": intento,
                "retry_of": retry_of,
                "provider": self._sesion.configuracion.datos["model"]["provider"],
                "requested_model": self._sesion.configuracion.datos["model"][
                    "requested_model"
                ],
                "api": self._sesion.configuracion.datos["model"]["api"],
                "requested_service_tier": self._sesion.configuracion.datos["model"][
                    "request_parameters"
                ]["service_tier"],
                "reasoning_effort": self._sesion.configuracion.datos["model"][
                    "request_parameters"
                ]["reasoning"]["effort"],
                "active_parameters": parametros,
                "prompt_version": self._sesion.configuracion.datos["versions"][
                    "prompts"
                ],
                "prompt_sha256": sha256_json(mensajes),
                "message_count": len(mensajes),
                "tool_count": len(self._esquemas_comunes),
                "visible_messages": mensajes,
                "tool_schema_sha256": sha256_json(self._esquemas_comunes),
                "provider_request_id": None,
            },
            correlation_id=model_call_id,
            parent_event_id=self._sesion.traza.ultimo_evento_id,
        )
        self._sesion.limites.registrar_modelo_iniciado(
            self._rol,
            FASES_ROL[self._rol],
        )
        return CapturaLlamada(
            model_call_id=model_call_id,
            role_execution_id=self._role_execution_id,
            evento_inicio=evento_inicio,
            started_at_utc=inicio_utc,
            inicio_ns=inicio_ns,
            intento=intento,
            retry_of=retry_of,
            mensajes=mensajes,
        )

    def _extract_responses_token_usage(self, response: Any) -> dict[str, Any]:
        uso = super()._extract_responses_token_usage(response)
        if self._captura is not None:
            self._captura.uso = dict(uso)
            modelo = getattr(response, "model", None)
            nivel = getattr(response, "service_tier", None)
            self._captura.reported_model = str(modelo) if modelo else None
            self._captura.reported_service_tier = str(nivel) if nivel else None
        return uso

    def _emit_call_completed_event(
        self,
        response: Any,
        call_type: LLMCallType,
        from_task: Task | None = None,
        from_agent: BaseAgent | None = None,
        messages: str | list[LLMMessage] | None = None,
        usage: dict[str, Any] | None = None,
        finish_reason: str | None = None,
        response_id: str | None = None,
    ) -> None:
        if self._captura is not None and not self._captura.finalizada and usage:
            self._finalizar_llamada(
                response,
                usage,
                finish_reason,
                response_id,
            )
        super()._emit_call_completed_event(
            response=response,
            call_type=call_type,
            from_task=from_task,
            from_agent=from_agent,
            messages=messages,
            usage=usage,
            finish_reason=finish_reason,
            response_id=response_id,
        )

    def _finalizar_llamada(
        self,
        response: Any,
        usage: Mapping[str, Any],
        finish_reason: str | None,
        response_id: str | None,
    ) -> None:
        captura = self._captura
        if captura is None or captura.finalizada:
            return

        entrada = self._entero_uso(usage, "prompt_tokens", "input_tokens")
        salida = self._entero_uso(usage, "completion_tokens", "output_tokens")
        total = self._entero_uso(usage, "total_tokens")
        if total == 0 and entrada + salida > 0:
            total = entrada + salida
        if total != entrada + salida:
            raise CapaComunError("El uso de tokens de CrewAI no es coherente")
        cache = self._entero_uso(
            usage,
            "cached_prompt_tokens",
            "cached_input_tokens",
        )
        razonamiento = self._entero_uso(
            usage,
            "reasoning_tokens",
            "reasoning_output_tokens",
        )
        coste = self._sesion.limites.registrar_uso_modelo(
            entrada,
            salida,
            total,
            cache,
            razonamiento,
            FASES_ROL[self._rol],
            self._rol,
        )
        llamadas = self._normalizar_llamadas(response)
        visible_output = "" if llamadas else self._texto_visible(response)
        evento_fin = self._sesion.traza.registrar(
            "model_call_finished",
            FASES_ROL[self._rol],
            ROL_TRAZA[self._rol],
            "model",
            {
                "model_call_id": captura.model_call_id,
                "provider_response_id": response_id,
                "reported_service_tier": captura.reported_service_tier,
                "outcome": "success",
                "finish_reason": finish_reason,
                "visible_output": visible_output,
                "requested_tool_calls": llamadas,
                "input_tokens": entrada,
                "output_tokens": salida,
                "total_tokens": total,
                "cached_input_tokens": cache,
                "reasoning_output_tokens": razonamiento,
                "usage_extensions": {
                    "reported_model": captura.reported_model,
                    "input_token_details": {"cache_read": cache},
                    "output_token_details": {"reasoning": razonamiento},
                },
                "estimated_cost": float(coste),
                "started_at_utc": captura.started_at_utc,
                "finished_at_utc": utc_actual(),
                "duration_ms": max(
                    (time.perf_counter_ns() - captura.inicio_ns) // 1_000_000,
                    0,
                ),
            },
            correlation_id=captura.model_call_id,
            parent_event_id=captura.evento_inicio,
        )
        captura.finalizada = True
        self._despachador.fijar_origen(
            captura.model_call_id,
            captura.role_execution_id,
            evento_fin,
        )

    def _registrar_fallo_llamada(
        self,
        exc: Exception,
        captura: CapturaLlamada,
    ) -> bool:
        retryable = self._es_error_transitorio(exc)
        puede_reintentar = False
        if retryable and captura.intento == 1:
            puede_reintentar = self._sesion.limites.registrar_reintento(
                FASES_ROL[self._rol],
                self._rol,
            )
        error_id = self._sesion.registrar_error(
            exc,
            FASES_ROL[self._rol],
            ROL_TRAZA[self._rol],
            "model_call",
            captura.evento_inicio,
            retryable=retryable,
            retry_triggered=puede_reintentar,
        )
        evento_fallo = self._sesion.traza.registrar(
            "model_call_failed",
            FASES_ROL[self._rol],
            ROL_TRAZA[self._rol],
            "model",
            {
                "model_call_id": captura.model_call_id,
                "provider_request_id": None,
                "provider_response_id": None,
                "duration_ms": max(
                    (time.perf_counter_ns() - captura.inicio_ns) // 1_000_000,
                    0,
                ),
                "error_id": error_id,
                "partial_usage": None,
                "retry_planned": puede_reintentar,
            },
            correlation_id=captura.model_call_id,
            parent_event_id=captura.evento_inicio,
        )
        captura.finalizada = True
        if puede_reintentar:
            siguiente = (
                f"{self._sesion.contexto.run_id}__model_"
                f"{self._sesion.contador_modelo + 1:03d}"
            )
            self._sesion.traza.registrar(
                "retry_recorded",
                FASES_ROL[self._rol],
                ROL_TRAZA[self._rol],
                "framework_adapter",
                {
                    "retry_id": (
                        f"{self._sesion.contexto.run_id}__retry_"
                        f"{self._sesion.limites.retries:03d}"
                    ),
                    "target_type": "model_call",
                    "failed_operation_id": captura.model_call_id,
                    "new_operation_id": siguiente,
                    "reason": type(exc).__name__,
                    "attempt": captura.intento + 1,
                    "authorized": True,
                },
                parent_event_id=evento_fallo,
            )
        return puede_reintentar

    @staticmethod
    def _normalizar_llamadas(response: Any) -> list[dict[str, Any]]:
        if not isinstance(response, list):
            return []
        llamadas: list[dict[str, Any]] = []
        for elemento in response:
            if isinstance(elemento, Mapping) and elemento.get("name"):
                argumentos = elemento.get("arguments", {})
                if isinstance(argumentos, str):
                    try:
                        argumentos = json.loads(argumentos)
                    except json.JSONDecodeError:
                        argumentos = argumentos
                llamadas.append(
                    {
                        "id": elemento.get("id"),
                        "name": elemento.get("name"),
                        "arguments": argumentos,
                    }
                )
        return llamadas

    @staticmethod
    def _texto_visible(response: Any) -> str:
        if isinstance(response, str):
            return response.strip()
        if response is None:
            return ""
        return str(response).strip()

    @staticmethod
    def _entero_uso(
        usage: Mapping[str, Any],
        *claves: str,
    ) -> int:
        for clave in claves:
            valor = usage.get(clave)
            if isinstance(valor, int) and not isinstance(valor, bool) and valor >= 0:
                return valor
        return 0

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

            if isinstance(
                exc,
                (
                    APIConnectionError,
                    APITimeoutError,
                    InternalServerError,
                    RateLimitError,
                ),
            ):
                return True
        except ImportError:
            pass
        return isinstance(exc, (ConnectionError, TimeoutError))


class FabricaOpenAICrewAI:
    """Crea una instancia Responses independiente para cada rol."""

    def __init__(self, configuracion: Any) -> None:
        self.configuracion = configuracion
        variable = configuracion.datos["model"]["api_key_environment_variable"]
        if not os.getenv(variable):
            raise CapaComunError(f"Falta {variable} en el entorno")
        self.api_key = os.environ[variable]

    def crear(
        self,
        sesion: SesionCrewAI,
        rol: str,
        role_execution_id: str,
        prompt: PromptConstruido,
        esquemas: Sequence[Mapping[str, Any]],
        despachador: DespachadorHerramientasCrewAI,
    ) -> ModeloOpenAICrewAIControlado:
        modelo = self.configuracion.datos["model"]
        parametros = modelo["request_parameters"]
        return ModeloOpenAICrewAIControlado(
            sesion=sesion,
            rol=rol,
            role_execution_id=role_execution_id,
            prompt=prompt,
            esquemas=esquemas,
            despachador=despachador,
            model=modelo["requested_model"],
            provider="openai",
            api="responses",
            api_key=self.api_key,
            max_completion_tokens=self.configuracion.datos["limits"]["tokens"][
                "request_output_max"
            ],
            reasoning_effort=parametros["reasoning"]["effort"],
            timeout=self.configuracion.datos["limits"]["time_seconds"][
                "model_request"
            ],
            max_retries=0,
            stream=False,
            store=parametros["store"],
            auto_chain=False,
            additional_params={
                "service_tier": parametros["service_tier"],
                "tool_choice": parametros["tool_choice"],
                "parallel_tool_calls": parametros["parallel_tool_calls"],
                "truncation": parametros["truncation"],
                "background": parametros["background"],
            },
            stop=[],
        )
