"""Nodos y transiciones propios del flujo experimental de LangGraph."""

from __future__ import annotations

from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph

from experimento.capa_comun import (
    cerrar_ejecucion_comun,
    interpretar_decision_revisor,
    interpretar_respuesta_correccion,
    materializar_markdown_rol,
)


class EstadoLangGraph(TypedDict, total=False):
    """Estado mínimo que circula entre los nodos del grafo."""

    plan: str
    report: str
    validation_pre_review: dict[str, Any]
    review_decision: dict[str, Any]
    correction_summary: dict[str, Any]
    final_status: str
    resultado_cierre: Any


class GrafoLangGraph:
    """Define los nodos y las transiciones entre los roles del experimento."""

    def construir_grafo(self) -> Any:
        constructor = StateGraph(EstadoLangGraph)
        constructor.add_node("planner", self._nodo_planner)
        constructor.add_node("analyst", self._nodo_analyst)
        constructor.add_node("pre_review_validation", self._nodo_validacion_previa)
        constructor.add_node("reviewer", self._nodo_reviewer)
        constructor.add_node("correction", self._nodo_correction)
        constructor.add_node("final_validation", self._nodo_validacion_final)
        constructor.add_node("closure", self._nodo_cierre)
        constructor.add_edge(START, "planner")
        constructor.add_edge("planner", "analyst")
        constructor.add_edge("analyst", "pre_review_validation")
        constructor.add_edge("pre_review_validation", "reviewer")
        constructor.add_conditional_edges(
            "reviewer",
            self._ruta_revision,
            {
                "correction": "correction",
                "final_validation": "final_validation",
            },
        )
        constructor.add_edge("correction", "final_validation")
        constructor.add_edge("final_validation", "closure")
        constructor.add_edge("closure", END)
        return constructor.compile()

    def _nodo_planner(self, estado: EstadoLangGraph) -> EstadoLangGraph:
        self._transicionar("planning", "Inicio del Planificador")
        prompt = self._prompt("planner")

        def procesar(texto: str, evento_origen: str) -> str:
            self.herramientas.inspeccion_cacheada()
            materializar_markdown_rol(
                self.configuracion,
                self.contexto,
                self.traza,
                "plan.md",
                texto,
                "planner",
                "initial",
                evento_origen,
            )
            return texto

        plan = self._intervencion(
            "planner",
            prompt,
            self._schemas_rol("planner"),
            procesar,
            "plan.md",
            1,
        )
        return {"plan": plan}

    def _nodo_analyst(self, estado: EstadoLangGraph) -> EstadoLangGraph:
        self._transicionar("analysis", "Plan válido disponible")
        inspeccion = self.herramientas.inspeccion_cacheada()
        prompt = self._prompt(
            "analyst_initial",
            inspeccion=inspeccion,
            plan=estado["plan"],
        )

        def procesar(texto: str, evento_origen: str) -> str:
            materializar_markdown_rol(
                self.configuracion,
                self.contexto,
                self.traza,
                "report.md",
                texto,
                "analyst",
                "initial",
                evento_origen,
            )
            return texto

        informe = self._intervencion(
            "analyst_initial",
            prompt,
            self._schemas_rol("analyst_initial"),
            procesar,
            "report.md",
            1,
        )
        return {"report": informe}

    def _nodo_validacion_previa(self, estado: EstadoLangGraph) -> EstadoLangGraph:
        respuesta = self.herramientas.validate_outputs(
            {},
            "runtime",
            trigger="pre_review",
            automatic=True,
            parent_event_id=self.traza.ultimo_evento_id,
        )
        return {"validation_pre_review": respuesta["data"]}

    def _nodo_reviewer(self, estado: EstadoLangGraph) -> EstadoLangGraph:
        self._transicionar("review", "Resultados iniciales disponibles")
        prompt = self._prompt(
            "reviewer",
            validacion_previa=estado["validation_pre_review"],
        )

        def procesar(texto: str, evento_origen: str) -> dict[str, Any]:
            decision = interpretar_decision_revisor(texto)
            decision_id = f"{self.contexto.run_id}__review_001"
            hashes = {
                artefacto["name"]: artefacto.get("sha256")
                for artefacto in estado["validation_pre_review"].get("artifacts", [])
            }
            self.traza.registrar(
                "review_decision",
                "review",
                "reviewer",
                "framework_adapter",
                {
                    "review_decision_id": decision_id,
                    "decision": decision["decision"],
                    "summary": decision["summary"],
                    "findings": decision["findings"],
                    "correction_allowed": True,
                    "correction_requested": decision["correction_requested"],
                    "reviewed_artifact_hashes": hashes,
                },
                parent_event_id=evento_origen,
            )
            self.decision_revision = decision
            return decision

        decision = self._intervencion(
            "reviewer",
            prompt,
            self._schemas_rol("reviewer"),
            procesar,
            None,
            1,
        )
        return {"review_decision": decision}

    @staticmethod
    def _ruta_revision(estado: EstadoLangGraph) -> str:
        if estado["review_decision"]["decision"] == "correction_required":
            return "correction"
        return "final_validation"

    def _nodo_correction(self, estado: EstadoLangGraph) -> EstadoLangGraph:
        self._transicionar("correction", "Corrección solicitada por el Revisor")
        self.correction_used = True
        self.correction_request_id = f"{self.contexto.run_id}__correction_001"
        self.herramientas.marcar_correccion_pendiente(True)
        hashes_iniciales = self._hashes_resultados()
        hallazgos = [
            hallazgo
            for hallazgo in estado["review_decision"]["findings"]
            if hallazgo["requires_correction"]
        ]
        afectados = sorted(
            {
                artefacto
                for hallazgo in hallazgos
                for artefacto in hallazgo["affected_artifacts"]
            }
        )
        self.traza.registrar(
            "correction_started",
            "correction",
            "analyst",
            "framework_adapter",
            {
                "correction_request_id": self.correction_request_id,
                "finding_ids": [hallazgo["finding_id"] for hallazgo in hallazgos],
                "potentially_affected_artifacts": afectados,
                "initial_hashes": hashes_iniciales,
            },
            parent_event_id=self.traza.ultimo_evento_id,
        )
        validacion_actual = dict(estado["validation_pre_review"])
        validacion_actual["pending_correction"] = True
        prompt = self._prompt(
            "analyst_correction",
            inspeccion=self.herramientas.inspeccion_cacheada(),
            plan=estado["plan"],
            decision_revision=estado["review_decision"],
            validacion_actual=validacion_actual,
        )

        def procesar(texto: str, evento_origen: str) -> dict[str, Any]:
            respuesta = interpretar_respuesta_correccion(
                texto,
                estado["review_decision"],
            )
            self.correction_resolved = not bool(
                respuesta.resumen["unresolved_findings"]
            )
            materializar_markdown_rol(
                self.configuracion,
                self.contexto,
                self.traza,
                "report.md",
                respuesta.informe,
                "analyst",
                "correction",
                evento_origen,
            )
            self.herramientas.marcar_correccion_pendiente(False)
            validacion = self.herramientas.validate_outputs(
                {},
                "analyst_correction",
                trigger="analyst",
                automatic=True,
                parent_event_id=self.traza.ultimo_evento_id,
            )
            hashes_finales = self._hashes_resultados()
            modificados = sorted(
                nombre
                for nombre, hash_final in hashes_finales.items()
                if hashes_iniciales.get(nombre) != hash_final
            )
            self.traza.registrar(
                "correction_finished",
                "correction",
                "analyst",
                "framework_adapter",
                {
                    "correction_request_id": self.correction_request_id,
                    "outcome": (
                        "success"
                        if not respuesta.resumen["unresolved_findings"]
                        else "partial"
                    ),
                    "declared_changes": respuesta.resumen["changes"],
                    "modified_files": modificados,
                    "post_validation_id": validacion["data"]["validation_id"],
                    "addressed_findings": respuesta.resumen["addressed_findings"],
                    "unresolved_findings": respuesta.resumen["unresolved_findings"],
                },
                parent_event_id=self.traza.ultimo_evento_id,
            )
            return dict(respuesta.resumen)

        resumen = self._intervencion(
            "analyst_correction",
            prompt,
            self._schemas_rol("analyst_correction"),
            procesar,
            "report.md",
            2,
        )
        return {
            "correction_summary": resumen,
            "report": self.contexto.directorio_salida.joinpath("report.md").read_text(
                encoding="utf-8"
            ),
        }

    def _nodo_validacion_final(self, estado: EstadoLangGraph) -> EstadoLangGraph:
        self._transicionar("final_validation", "Flujo de roles finalizado")
        return {}

    def _nodo_cierre(self, estado: EstadoLangGraph) -> EstadoLangGraph:
        cierre = cerrar_ejecucion_comun(
            self.herramientas,
            self.limites,
            self.traza,
            dataset_cargado=True,
            flujo_roles_completo=True,
            decision_revision=(
                self.decision_revision["decision"]
                if self.decision_revision
                else None
            ),
            correccion_resuelta=self.correction_resolved,
            correction_used=self.correction_used,
            correction_request_id=self.correction_request_id,
            estado_origen=self.estado_actual,
        )
        self.estado_actual = cierre.estado
        return {
            "final_status": cierre.estado,
            "resultado_cierre": cierre,
        }
