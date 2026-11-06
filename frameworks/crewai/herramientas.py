"""Conexión de las herramientas de CrewAI con las funciones de la capa común."""

from __future__ import annotations

import json
from typing import Any, Literal, Mapping

from crewai.tools import BaseTool
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr

from experimento.capa_comun import (
    ESQUEMA_EXECUTE_PYTHON,
    ESQUEMA_INSPECT_DATASET,
    ESQUEMA_READ_OUTPUT,
    ESQUEMA_VALIDATE_OUTPUTS,
    CapaComunError,
    HerramientasComunes,
)


ESQUEMAS_COMUNES = {
    "inspect_dataset": ESQUEMA_INSPECT_DATASET,
    "execute_python": ESQUEMA_EXECUTE_PYTHON,
    "read_output": ESQUEMA_READ_OUTPUT,
    "validate_outputs": ESQUEMA_VALIDATE_OUTPUTS,
}


class ArgumentosVacios(BaseModel):
    """Esquema local para herramientas sin parámetros."""

    model_config = ConfigDict(extra="forbid")


class ArgumentosExecutePython(BaseModel):
    """Argumentos de execute_python sin alterar su contrato público."""

    model_config = ConfigDict(extra="forbid")

    purpose: str = Field(
        min_length=1,
        description=ESQUEMA_EXECUTE_PYTHON["parameters"]["properties"]["purpose"][
            "description"
        ],
    )
    code: str = Field(
        min_length=1,
        description=ESQUEMA_EXECUTE_PYTHON["parameters"]["properties"]["code"][
            "description"
        ],
    )


class ArgumentosReadOutput(BaseModel):
    """Argumentos de read_output sin ampliar valores permitidos."""

    model_config = ConfigDict(extra="forbid")

    artifact: Literal[
        "plan",
        "prepared_data",
        "statistics",
        "issues",
        "figures",
        "report",
    ]
    query: Literal["summary", "full", "id", "section", "next"]
    selector: str | None
    cursor: str | None


ARGUMENTOS = {
    "inspect_dataset": ArgumentosVacios,
    "execute_python": ArgumentosExecutePython,
    "read_output": ArgumentosReadOutput,
    "validate_outputs": ArgumentosVacios,
}


class DespachadorHerramientasCrewAI:
    """Conecta las llamadas de CrewAI con una única instancia común."""

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
        """Asocia la siguiente llamada de herramienta a la respuesta del modelo."""

        self.model_call_id = model_call_id
        self.role_execution_id = role_execution_id
        self.parent_event_id = parent_event_id

    def ejecutar(
        self,
        nombre: str,
        argumentos: Mapping[str, Any] | None,
        rol: str,
    ) -> dict[str, Any]:
        """Delega la ejecución sin duplicar lógica ni validadores."""

        if not self.model_call_id or not self.role_execution_id:
            raise CapaComunError(
                "CrewAI intentó usar una herramienta sin una llamada de modelo asociada"
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


class HerramientaCrewAI(BaseTool):
    """Presenta una herramienta común con el formato requerido por CrewAI."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    _despachador: DespachadorHerramientasCrewAI = PrivateAttr()
    _rol: str = PrivateAttr()

    def __init__(
        self,
        nombre: str,
        rol: str,
        despachador: DespachadorHerramientasCrewAI,
    ) -> None:
        esquema = ESQUEMAS_COMUNES[nombre]
        super().__init__(
            name=nombre,
            description=esquema["description"],
            args_schema=ARGUMENTOS[nombre],
            result_as_answer=False,
        )
        self._despachador = despachador
        self._rol = rol

    def _run(self, **kwargs: Any) -> str:
        respuesta = self._despachador.ejecutar(
            self.name,
            kwargs,
            self._rol,
        )
        return json.dumps(
            respuesta,
            ensure_ascii=False,
            allow_nan=False,
        )


def construir_herramientas_crewai(
    rol: str,
    nombres: list[str] | tuple[str, ...],
    despachador: DespachadorHerramientasCrewAI,
) -> list[HerramientaCrewAI]:
    """Prepara las herramientas autorizadas para el rol actual."""

    return [
        HerramientaCrewAI(nombre, rol, despachador)
        for nombre in nombres
    ]

