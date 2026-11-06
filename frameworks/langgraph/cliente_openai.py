"""Cliente de OpenAI y lectura de sus respuestas y consumo de tokens, adaptado a la interfaz de LangGraph."""

from __future__ import annotations

import json
import os
from typing import Any, Mapping, Protocol, Sequence

from langchain_core.messages import AIMessage, BaseMessage, ToolMessage
from langchain_openai import ChatOpenAI

from experimento.capa_comun import CapaComunError
from experimento.capa_comun.utilidades import (
    descongelar,
    json_canonico,
    sha256_json,
    utc_actual,
)


class ProveedorModelo(Protocol):
    """Operación mínima compartida por OpenAI y los simuladores locales."""

    def invocar(
        self,
        mensajes: Sequence[BaseMessage],
        herramientas: Sequence[Mapping[str, Any]],
        max_output_tokens: int,
    ) -> AIMessage:
        ...


class FalloModeloSimulado(Exception):
    """Fallo controlable utilizado por las pruebas sin conexión externa."""

    def __init__(self, mensaje: str, retryable: bool = False) -> None:
        super().__init__(mensaje)
        self.retryable = retryable


class FalloAdaptador(CapaComunError):
    """Error del adaptador asociado a un identificador de la traza."""

    def __init__(self, mensaje: str, error_id: str | None = None) -> None:
        super().__init__(mensaje)
        self.error_id = error_id


class ClienteOpenAILangGraph:
    """Cliente real de OpenAI Responses utilizado por LangGraph."""

    def __init__(self, configuracion: Any) -> None:
        variable_clave = configuracion.datos["model"]["api_key_environment_variable"]
        if not os.getenv(variable_clave):
            raise CapaComunError(f"Falta {variable_clave} en el entorno")
        os.environ["LANGSMITH_TRACING"] = "false"
        os.environ["LANGCHAIN_TRACING_V2"] = "false"
        modelo = configuracion.datos["model"]
        parametros = modelo["request_parameters"]
        self._tool_choice = parametros["tool_choice"]
        self._parallel_tool_calls = parametros["parallel_tool_calls"]
        self._modelo = ChatOpenAI(
            model=modelo["requested_model"],
            cache=False,
            use_responses_api=True,
            reasoning={"effort": parametros["reasoning"]["effort"]},
            service_tier=parametros["service_tier"],
            store=parametros["store"],
            truncation=parametros["truncation"],
            streaming=parametros["stream"],
            max_retries=0,
            timeout=configuracion.datos["limits"]["time_seconds"]["model_request"],
            model_kwargs={"background": parametros["background"]},
        )

    def invocar(
        self,
        mensajes: Sequence[BaseMessage],
        herramientas: Sequence[Mapping[str, Any]],
        max_output_tokens: int,
    ) -> AIMessage:
        modelo = self._modelo
        if herramientas:
            modelo = self._modelo.bind_tools(
                list(herramientas),
                tool_choice=self._tool_choice,
                parallel_tool_calls=self._parallel_tool_calls,
                strict=True,
            )
        respuesta = modelo.invoke(
            list(mensajes),
            max_completion_tokens=max_output_tokens,
        )
        if not isinstance(respuesta, AIMessage):
            raise CapaComunError("LangGraph no devolvió un AIMessage")
        return respuesta


def hash_json(valor: Any) -> str:
    """Calcula el SHA-256 de una estructura JSON canónica."""

    return sha256_json(valor)


def texto_mensaje(mensaje: AIMessage) -> str:
    """Extrae únicamente el texto visible de una respuesta del modelo."""

    if isinstance(mensaje.content, str):
        return mensaje.content.strip()
    textos: list[str] = []
    if isinstance(mensaje.content, list):
        for bloque in mensaje.content:
            if isinstance(bloque, str):
                textos.append(bloque)
            elif isinstance(bloque, Mapping):
                texto = bloque.get("text")
                if isinstance(texto, str):
                    textos.append(texto)
                elif isinstance(texto, Mapping) and isinstance(texto.get("value"), str):
                    textos.append(texto["value"])
    return "\n".join(textos).strip()


def mensaje_visible(mensaje: BaseMessage) -> dict[str, Any]:
    """Convierte un mensaje de LangChain al contenido permitido en la traza."""

    contenido = (
        texto_mensaje(mensaje)
        if isinstance(mensaje, AIMessage)
        else mensaje.content
    )
    visible: dict[str, Any] = {
        "type": mensaje.type,
        "content": contenido,
    }
    if isinstance(mensaje, AIMessage):
        visible["tool_calls"] = [
            {
                "id": llamada.get("id"),
                "name": llamada.get("name"),
                "args": llamada.get("args"),
            }
            for llamada in mensaje.tool_calls
        ]
    if isinstance(mensaje, ToolMessage):
        visible["tool_call_id"] = mensaje.tool_call_id
        visible["name"] = mensaje.name
    return visible


def uso_modelo(mensaje: AIMessage) -> dict[str, Any]:
    """Normaliza y valida los contadores de tokens informados por OpenAI."""

    uso = dict(mensaje.usage_metadata or {})
    entrada = uso.get("input_tokens")
    salida = uso.get("output_tokens")
    total = uso.get("total_tokens")
    valores_validos = all(
        isinstance(valor, int) and not isinstance(valor, bool) and valor >= 0
        for valor in (entrada, salida)
    )
    if not valores_validos:
        raise CapaComunError("La respuesta del modelo no informa tokens válidos")
    if total is None:
        total = entrada + salida
    if not isinstance(total, int) or isinstance(total, bool) or total != entrada + salida:
        raise CapaComunError("El total de tokens informado no es coherente")
    detalle_entrada = uso.get("input_token_details") or {}
    detalle_salida = uso.get("output_token_details") or {}
    cache = detalle_entrada.get("cache_read", 0)
    razonamiento = detalle_salida.get("reasoning", 0)
    return {
        "input_tokens": entrada,
        "output_tokens": salida,
        "total_tokens": total,
        "cached_input_tokens": cache if isinstance(cache, int) else 0,
        "reasoning_output_tokens": razonamiento if isinstance(razonamiento, int) else 0,
        "input_token_details": detalle_entrada,
        "output_token_details": detalle_salida,
    }
