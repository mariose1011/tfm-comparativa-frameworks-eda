"""Cliente Responses y registro común de las peticiones realizadas por MAF."""

from __future__ import annotations

import copy
import json
import os
import time
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Mapping, Protocol, Sequence

from agent_framework import ChatContext, ChatMiddleware, ChatResponse, Message
from agent_framework.openai import OpenAIChatClient
from openai import AsyncOpenAI

from experimento.capa_comun import CapaComunError
from experimento.capa_comun.utilidades import (
    descongelar,
    json_canonico,
    sha256_json,
    utc_actual,
)

from .herramientas import DespachadorHerramientasMAF


if TYPE_CHECKING:
    from .sesion import SesionMAF


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


class FalloAdaptadorMAF(CapaComunError):
    """Fallo del adaptador asociado a un identificador de la traza."""

    def __init__(self, mensaje: str, error_id: str | None = None) -> None:
        super().__init__(mensaje)
        self.error_id = error_id


class ClienteOpenAIMAFControlado(OpenAIChatClient):
    """Conserva el cliente nativo y aplica el modo estricto del contrato."""

    def _prepare_tools_for_openai(self, tools: Any) -> list[Any]:
        preparadas = super()._prepare_tools_for_openai(tools)
        for herramienta in preparadas:
            if isinstance(herramienta, dict) and herramienta.get("type") == "function":
                herramienta["strict"] = True
        return preparadas


class FabricaClienteMAF(Protocol):
    """Operación mínima para crear un cliente aislado por intervención."""

    def crear(
        self,
        sesion: SesionMAF,
        rol: str,
        role_execution_id: str,
        esquemas: Sequence[Mapping[str, Any]],
        despachador: DespachadorHerramientasMAF,
    ) -> ClienteOpenAIMAFControlado:
        ...


@dataclass(slots=True)
class CapturaLlamada:
    """Información temporal de una petición individual al proveedor."""

    model_call_id: str
    evento_inicio: str
    started_at_utc: str
    inicio_ns: int
    intento: int
    retry_of: str | None


class RegistroModeloMAF(ChatMiddleware):
    """Comprueba los límites y registra cada petición al modelo y su resultado."""

    def __init__(
        self,
        sesion: SesionMAF,
        rol: str,
        role_execution_id: str,
        esquemas: Sequence[Mapping[str, Any]],
        despachador: DespachadorHerramientasMAF,
    ) -> None:
        self.sesion = sesion
        self.rol = rol
        self.role_execution_id = role_execution_id
        self.esquemas = [descongelar(esquema) for esquema in esquemas]
        self.despachador = despachador

    async def process(self, context: ChatContext, call_next: Any) -> None:
        mensajes = self._mensajes_visibles(context.messages, context.options)
        entrada_estimada = max(len(json_canonico(mensajes)) // 4, 1)
        intento = 1
        retry_of: str | None = None

        while True:
            autorizacion = self.sesion.limites.autorizar_modelo(
                self.rol,
                FASES_ROL[self.rol],
                entrada_estimada,
            )
            if not autorizacion.autorizada:
                error = CapaComunError(
                    "La llamada al modelo fue bloqueada por el límite "
                    f"{autorizacion.motivo}"
                )
                error_id = self.sesion.registrar_error(
                    error,
                    FASES_ROL[self.rol],
                    ROL_TRAZA[self.rol],
                    "model_authorization",
                    self.sesion.traza.ultimo_evento_id,
                    retryable=False,
                    retry_triggered=False,
                )
                raise FalloAdaptadorMAF(str(error), error_id)

            opciones = dict(context.options or {})
            opciones["max_tokens"] = autorizacion.max_output_tokens
            context.options = opciones
            captura = self._iniciar_llamada(
                mensajes,
                autorizacion.max_output_tokens,
                intento,
                retry_of,
            )
            try:
                await call_next()
                if not isinstance(context.result, ChatResponse):
                    raise CapaComunError("MAF no devolvió una respuesta de chat válida")
                self._finalizar_llamada(context.result, captura)
                return
            except Exception as exc:
                puede_reintentar = self._registrar_fallo(exc, captura)
                if not puede_reintentar:
                    error_id = getattr(exc, "error_id", None)
                    if not error_id:
                        error_id = self.sesion.ultimo_error_id
                    raise FalloAdaptadorMAF(str(exc), error_id) from exc
                retry_of = captura.model_call_id
                intento += 1
                context.result = None

    def _iniciar_llamada(
        self,
        mensajes: list[dict[str, Any]],
        max_output_tokens: int,
        intento: int,
        retry_of: str | None,
    ) -> CapturaLlamada:
        self.sesion.contador_modelo += 1
        model_call_id = (
            f"{self.sesion.contexto.run_id}__model_"
            f"{self.sesion.contador_modelo:03d}"
        )
        parametros = descongelar(
            self.sesion.configuracion.datos["model"]["request_parameters"]
        )
        parametros["max_output_tokens"] = max_output_tokens
        inicio_utc = utc_actual()
        inicio_ns = time.perf_counter_ns()
        evento_inicio = self.sesion.traza.registrar(
            "model_call_started",
            FASES_ROL[self.rol],
            ROL_TRAZA[self.rol],
            "model",
            {
                "model_call_id": model_call_id,
                "role_execution_id": self.role_execution_id,
                "attempt": intento,
                "retry_of": retry_of,
                "provider": self.sesion.configuracion.datos["model"]["provider"],
                "requested_model": self.sesion.configuracion.datos["model"][
                    "requested_model"
                ],
                "api": self.sesion.configuracion.datos["model"]["api"],
                "requested_service_tier": self.sesion.configuracion.datos["model"][
                    "request_parameters"
                ]["service_tier"],
                "reasoning_effort": self.sesion.configuracion.datos["model"][
                    "request_parameters"
                ]["reasoning"]["effort"],
                "active_parameters": parametros,
                "prompt_version": self.sesion.configuracion.datos["versions"][
                    "prompts"
                ],
                "prompt_sha256": sha256_json(mensajes),
                "message_count": len(mensajes),
                "tool_count": len(self.esquemas),
                "visible_messages": mensajes,
                "tool_schema_sha256": sha256_json(self.esquemas),
                "provider_request_id": None,
            },
            correlation_id=model_call_id,
            parent_event_id=self.sesion.traza.ultimo_evento_id,
        )
        self.sesion.limites.registrar_modelo_iniciado(
            self.rol,
            FASES_ROL[self.rol],
        )
        return CapturaLlamada(
            model_call_id=model_call_id,
            evento_inicio=evento_inicio,
            started_at_utc=inicio_utc,
            inicio_ns=inicio_ns,
            intento=intento,
            retry_of=retry_of,
        )

    def _finalizar_llamada(
        self,
        respuesta: ChatResponse,
        captura: CapturaLlamada,
    ) -> None:
        uso = self._normalizar_uso(respuesta.usage_details)
        coste = self.sesion.limites.registrar_uso_modelo(
            uso["input_tokens"],
            uso["output_tokens"],
            uso["total_tokens"],
            uso["cached_input_tokens"],
            uso["reasoning_output_tokens"],
            FASES_ROL[self.rol],
            self.rol,
        )
        llamadas = self._llamadas_herramientas(respuesta)
        nivel = getattr(respuesta.raw_representation, "service_tier", None)
        evento_fin = self.sesion.traza.registrar(
            "model_call_finished",
            FASES_ROL[self.rol],
            ROL_TRAZA[self.rol],
            "model",
            {
                "model_call_id": captura.model_call_id,
                "provider_response_id": respuesta.response_id,
                "reported_service_tier": str(nivel) if nivel else None,
                "outcome": "success",
                "finish_reason": self._valor_texto(respuesta.finish_reason),
                "visible_output": self._texto_visible(respuesta),
                "requested_tool_calls": llamadas,
                **uso,
                "usage_extensions": {
                    "reported_model": respuesta.model,
                    "input_token_details": {
                        "cache_read": uso["cached_input_tokens"]
                    },
                    "output_token_details": {
                        "reasoning": uso["reasoning_output_tokens"]
                    },
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
        self.despachador.fijar_origen(
            captura.model_call_id,
            self.role_execution_id,
            evento_fin,
        )

    def _registrar_fallo(self, exc: Exception, captura: CapturaLlamada) -> bool:
        retryable = self._es_error_transitorio(exc)
        puede_reintentar = False
        if retryable and captura.intento == 1:
            puede_reintentar = self.sesion.limites.registrar_reintento(
                FASES_ROL[self.rol],
                self.rol,
            )
        error_id = self.sesion.registrar_error(
            exc,
            FASES_ROL[self.rol],
            ROL_TRAZA[self.rol],
            "model_call",
            captura.evento_inicio,
            retryable=retryable,
            retry_triggered=puede_reintentar,
        )
        evento_fallo = self.sesion.traza.registrar(
            "model_call_failed",
            FASES_ROL[self.rol],
            ROL_TRAZA[self.rol],
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
        if puede_reintentar:
            siguiente = (
                f"{self.sesion.contexto.run_id}__model_"
                f"{self.sesion.contador_modelo + 1:03d}"
            )
            self.sesion.traza.registrar(
                "retry_recorded",
                FASES_ROL[self.rol],
                ROL_TRAZA[self.rol],
                "framework_adapter",
                {
                    "retry_id": (
                        f"{self.sesion.contexto.run_id}__retry_"
                        f"{self.sesion.limites.retries:03d}"
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

    @classmethod
    def _mensajes_visibles(
        cls,
        mensajes: Sequence[Message],
        opciones: Mapping[str, Any] | None,
    ) -> list[dict[str, Any]]:
        visibles: list[dict[str, Any]] = []
        instrucciones = (opciones or {}).get("instructions")
        if isinstance(instrucciones, str) and instrucciones:
            visibles.append(
                {
                    "role": "system",
                    "contents": [{"type": "text", "text": instrucciones}],
                }
            )
        for mensaje in mensajes:
            contenidos: list[dict[str, Any]] = []
            for contenido in mensaje.contents:
                if contenido.type == "text":
                    contenidos.append({"type": "text", "text": contenido.text or ""})
                elif contenido.type == "function_call":
                    contenidos.append(
                        {
                            "type": "function_call",
                            "call_id": contenido.call_id,
                            "name": contenido.name,
                            "arguments": cls._argumentos(contenido),
                        }
                    )
                elif contenido.type == "function_result":
                    contenidos.append(
                        {
                            "type": "function_result",
                            "call_id": contenido.call_id,
                            "result": cls._resultado_visible(contenido.result),
                        }
                    )
            visibles.append(
                {
                    "role": cls._valor_texto(mensaje.role),
                    "contents": contenidos,
                }
            )
        return visibles

    @classmethod
    def _llamadas_herramientas(cls, respuesta: ChatResponse) -> list[dict[str, Any]]:
        llamadas: list[dict[str, Any]] = []
        for mensaje in respuesta.messages:
            for contenido in mensaje.contents:
                if contenido.type == "function_call":
                    llamadas.append(
                        {
                            "id": contenido.call_id,
                            "name": contenido.name,
                            "arguments": cls._argumentos(contenido),
                        }
                    )
        return llamadas

    @staticmethod
    def _argumentos(contenido: Any) -> Any:
        try:
            return contenido.parse_arguments() or {}
        except Exception:
            argumentos = getattr(contenido, "arguments", {})
            if isinstance(argumentos, str):
                try:
                    return json.loads(argumentos)
                except json.JSONDecodeError:
                    return argumentos
            return argumentos

    @classmethod
    def _resultado_visible(cls, resultado: Any) -> Any:
        if isinstance(resultado, list):
            textos = [
                contenido.text
                for contenido in resultado
                if getattr(contenido, "type", None) == "text"
            ]
            return "".join(texto or "" for texto in textos)
        if isinstance(resultado, (str, int, float, bool)) or resultado is None:
            return resultado
        if isinstance(resultado, Mapping):
            return copy.deepcopy(dict(resultado))
        return str(resultado)

    @staticmethod
    def _texto_visible(respuesta: ChatResponse) -> str:
        textos = [
            contenido.text or ""
            for mensaje in respuesta.messages
            for contenido in mensaje.contents
            if contenido.type == "text"
        ]
        return "".join(textos).strip()

    @staticmethod
    def _normalizar_uso(uso: Mapping[str, Any] | None) -> dict[str, int]:
        if not isinstance(uso, Mapping):
            raise CapaComunError("La respuesta de MAF no informa el uso de tokens")

        def entero(clave: str, opcional: bool = False) -> int:
            valor = uso.get(clave)
            if valor is None and opcional:
                return 0
            if not isinstance(valor, int) or isinstance(valor, bool) or valor < 0:
                raise CapaComunError(f"Contador de tokens no válido: {clave}")
            return valor

        entrada = entero("input_token_count")
        salida = entero("output_token_count")
        total = entero("total_token_count")
        if total != entrada + salida:
            raise CapaComunError("El total de tokens informado por MAF no es coherente")
        return {
            "input_tokens": entrada,
            "output_tokens": salida,
            "total_tokens": total,
            "cached_input_tokens": entero(
                "cache_read_input_token_count",
                opcional=True,
            ),
            "reasoning_output_tokens": entero(
                "reasoning_output_token_count",
                opcional=True,
            ),
        }

    @staticmethod
    def _valor_texto(valor: Any) -> str | None:
        if valor is None:
            return None
        contenido = getattr(valor, "value", valor)
        return str(contenido)

    @staticmethod
    def _es_error_transitorio(exc: Exception) -> bool:
        actual: BaseException | None = exc
        visitados: set[int] = set()
        while actual is not None and id(actual) not in visitados:
            visitados.add(id(actual))
            if hasattr(actual, "retryable"):
                return bool(getattr(actual, "retryable"))
            try:
                from openai import (
                    APIConnectionError,
                    APITimeoutError,
                    InternalServerError,
                    RateLimitError,
                )

                if isinstance(
                    actual,
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
            if isinstance(actual, (ConnectionError, TimeoutError)):
                return True
            actual = getattr(actual, "inner_exception", None) or actual.__cause__
        return False


class FabricaOpenAIMAF:
    """Crea un cliente Responses independiente para cada intervención."""

    def __init__(self, configuracion: Any) -> None:
        self.configuracion = configuracion
        variable = configuracion.datos["model"]["api_key_environment_variable"]
        if not os.getenv(variable):
            raise CapaComunError(f"Falta {variable} en el entorno")
        self.api_key = os.environ[variable]

    def crear(
        self,
        sesion: SesionMAF,
        rol: str,
        role_execution_id: str,
        esquemas: Sequence[Mapping[str, Any]],
        despachador: DespachadorHerramientasMAF,
    ) -> ClienteOpenAIMAFControlado:
        limites = self.configuracion.datos["limits"]
        max_funciones = sum(
            limites["model_requested_tool_calls"]["roles"][rol].values()
        )
        registro = RegistroModeloMAF(
            sesion,
            rol,
            role_execution_id,
            esquemas,
            despachador,
        )
        cliente_openai = AsyncOpenAI(
            api_key=self.api_key,
            max_retries=0,
            timeout=limites["time_seconds"]["model_request"],
        )
        return ClienteOpenAIMAFControlado(
            model=self.configuracion.datos["model"]["requested_model"],
            async_client=cliente_openai,
            instruction_role="system",
            middleware=[registro],
            function_invocation_configuration={
                "enabled": True,
                "max_iterations": limites["model_requests"]["roles"][rol],
                "max_function_calls": max(max_funciones, 1),
                "max_consecutive_errors_per_request": limites["model_requests"][
                    "roles"
                ][rol],
                "terminate_on_unknown_calls": True,
                "include_detailed_errors": False,
            },
        )
