"""Flujo nativo de Microsoft Agent Framework para los roles del contrato."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from agent_framework import (
    Case,
    Default,
    Executor,
    WorkflowBuilder,
    WorkflowContext,
    handler,
)


if TYPE_CHECKING:
    from .sesion import SesionMAF


@dataclass(slots=True)
class EstadoFlujoMAF:
    """Datos mínimos que pasan entre los nodos nativos del flujo."""

    plan: str = ""
    validacion: dict[str, Any] = field(default_factory=dict)
    decision: dict[str, Any] = field(default_factory=dict)


class NodoPlanificador(Executor):
    def __init__(self, sesion: SesionMAF) -> None:
        super().__init__(id="planificador")
        self.sesion = sesion

    @handler(input=str, output=EstadoFlujoMAF)
    async def ejecutar(
        self,
        _: str,
        ctx: WorkflowContext[EstadoFlujoMAF],
    ) -> None:
        plan = await self.sesion.ejecutar_planificador()
        await ctx.send_message(EstadoFlujoMAF(plan=plan))


class NodoAnalista(Executor):
    def __init__(self, sesion: SesionMAF) -> None:
        super().__init__(id="analista")
        self.sesion = sesion

    @handler(input=EstadoFlujoMAF, output=EstadoFlujoMAF)
    async def ejecutar(
        self,
        estado: EstadoFlujoMAF,
        ctx: WorkflowContext[EstadoFlujoMAF],
    ) -> None:
        await self.sesion.ejecutar_analista(estado.plan)
        estado.validacion = self.sesion.validacion_previa()
        await ctx.send_message(estado)


class NodoRevisor(Executor):
    def __init__(self, sesion: SesionMAF) -> None:
        super().__init__(id="revisor")
        self.sesion = sesion

    @handler(input=EstadoFlujoMAF, output=EstadoFlujoMAF)
    async def ejecutar(
        self,
        estado: EstadoFlujoMAF,
        ctx: WorkflowContext[EstadoFlujoMAF],
    ) -> None:
        estado.decision = await self.sesion.ejecutar_revisor(estado.validacion)
        await ctx.send_message(estado)


class NodoCorreccion(Executor):
    def __init__(self, sesion: SesionMAF) -> None:
        super().__init__(id="correccion_opcional")
        self.sesion = sesion

    @handler(input=EstadoFlujoMAF, output=EstadoFlujoMAF)
    async def ejecutar(
        self,
        estado: EstadoFlujoMAF,
        ctx: WorkflowContext[EstadoFlujoMAF],
    ) -> None:
        await self.sesion.ejecutar_correccion(
            estado.plan,
            estado.validacion,
            estado.decision,
        )
        await ctx.send_message(estado)


class NodoCierre(Executor):
    def __init__(self, sesion: SesionMAF) -> None:
        super().__init__(id="validacion_final")
        self.sesion = sesion

    @handler(input=EstadoFlujoMAF, workflow_output=EstadoFlujoMAF)
    async def ejecutar(
        self,
        estado: EstadoFlujoMAF,
        ctx: WorkflowContext[Any, EstadoFlujoMAF],
    ) -> None:
        self.sesion.preparar_cierre()
        await ctx.yield_output(estado)


def crear_flujo_maf(sesion: SesionMAF) -> Any:
    """Construye un flujo nuevo y aislado para una sola ejecución."""

    planificador = NodoPlanificador(sesion)
    analista = NodoAnalista(sesion)
    revisor = NodoRevisor(sesion)
    correccion = NodoCorreccion(sesion)
    cierre = NodoCierre(sesion)
    return (
        WorkflowBuilder(
            max_iterations=8,
            name="TFM_MAF_Planificador_Analista_Revisor",
            description="Flujo controlado de EDA tabular",
            start_executor=planificador,
            output_from=[cierre],
        )
        .add_edge(planificador, analista)
        .add_edge(analista, revisor)
        .add_switch_case_edge_group(
            revisor,
            [
                Case(
                    condition=lambda estado: estado.decision.get("decision")
                    == "correction_required",
                    target=correccion,
                ),
                Default(target=cierre),
            ],
        )
        .add_edge(correccion, cierre)
        .build()
    )

