"""Conexión de las herramientas de MAF con las funciones de la capa común."""

from __future__ import annotations

import copy
import json
from typing import Any, Mapping

from agent_framework import FunctionTool

from experimento.capa_comun import (
    CapaComunError,
    ESQUEMA_EXECUTE_PYTHON,
    ESQUEMA_INSPECT_DATASET,
    ESQUEMA_READ_OUTPUT,
    ESQUEMA_VALIDATE_OUTPUTS,
    HerramientasComunes,
)


ESQUEMAS_COMUNES = {
    "inspect_dataset": ESQUEMA_INSPECT_DATASET,
    "execute_python": ESQUEMA_EXECUTE_PYTHON,
    "read_output": ESQUEMA_READ_OUTPUT,
    "validate_outputs": ESQUEMA_VALIDATE_OUTPUTS,
}


class DespachadorHerramientasMAF:
    """Delega cada llamada nativa de MAF en la implementación compartida."""

    def __init__(self, herramientas: HerramientasComunes) -> None:
        self.herramientas = herramientas
        self.model_call_id: str | None = None
        self.role_execution_id: str | None = None
        self.parent_event_id: str | None = None

    def fijar_origen(
        self,
        model_call_id: str,
        role_execution_id: str,
        parent_event_id: str,
    ) -> None:
        """Relaciona la siguiente herramienta con la petición que la solicitó."""

        self.model_call_id = model_call_id
        self.role_execution_id = role_execution_id
        self.parent_event_id = parent_event_id

    def ejecutar(
        self,
        nombre: str,
        argumentos: Mapping[str, Any] | None,
        rol: str,
    ) -> dict[str, Any]:
        """Llama a la única implementación autorizada de cada herramienta."""

        if not self.model_call_id or not self.role_execution_id:
            raise CapaComunError(
                "MAF intentó usar una herramienta sin una petición de modelo asociada"
            )
        comunes = {
            "rol": rol,
            "model_call_id": self.model_call_id,
            "role_execution_id": self.role_execution_id,
            "parent_event_id": self.parent_event_id,
        }
        if nombre == "inspect_dataset":
            return self.herramientas.inspect_dataset(argumentos, **comunes)
        if nombre == "execute_python":
            return self.herramientas.execute_python(argumentos, **comunes)
        if nombre == "read_output":
            return self.herramientas.read_output(argumentos, **comunes)
        if nombre == "validate_outputs":
            trigger = "reviewer" if rol == "reviewer" else "analyst"
            return self.herramientas.validate_outputs(
                argumentos,
                trigger=trigger,
                **comunes,
            )
        raise CapaComunError(f"Herramienta común desconocida: {nombre}")


def _crear_funcion(
    nombre: str,
    rol: str,
    despachador: DespachadorHerramientasMAF,
) -> Any:
    def ejecutar(**argumentos: Any) -> str:
        respuesta = despachador.ejecutar(nombre, argumentos, rol)
        return json.dumps(respuesta, ensure_ascii=False, allow_nan=False)

    return ejecutar


def construir_herramientas_maf(
    rol: str,
    nombres: list[str] | tuple[str, ...],
    despachador: DespachadorHerramientasMAF,
) -> list[FunctionTool]:
    """Prepara las herramientas autorizadas con los nombres y parámetros del contrato común."""

    herramientas: list[FunctionTool] = []
    for nombre in nombres:
        esquema = ESQUEMAS_COMUNES[nombre]
        herramientas.append(
            FunctionTool(
                name=nombre,
                description=esquema["description"],
                approval_mode="never_require",
                func=_crear_funcion(nombre, rol, despachador),
                input_model=copy.deepcopy(esquema["parameters"]),
            )
        )
    return herramientas

