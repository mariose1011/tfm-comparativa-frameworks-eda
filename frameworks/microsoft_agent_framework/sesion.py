"""Coordinación de MAF, sus agentes y el cierre de la capa común."""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from typing import Any, Callable, Mapping

from agent_framework import Agent, AgentResponse

from experimento.capa_comun import (
    CapaComunError,
    ControlLimites,
    ErrorMaterializacion,
    ErrorPrompt,
    EscritorTraza,
    HerramientasComunes,
    PromptConstruido,
    cerrar_ejecucion_comun,
    construir_prompt_reparacion_formato,
    construir_prompt_rol,
    interpretar_decision_revisor,
    interpretar_respuesta_correccion,
    materializar_markdown_rol,
)
from experimento.capa_comun.utilidades import (
    descongelar,
    sha256_archivo,
    utc_actual,
)

from .flujo import crear_flujo_maf
from .herramientas import (
    ESQUEMAS_COMUNES,
    DespachadorHerramientasMAF,
    construir_herramientas_maf,
)
from .modelo import (
    FASES_ROL,
    ROL_TRAZA,
    FabricaClienteMAF,
    FalloAdaptadorMAF,
)


@dataclass(frozen=True, slots=True)
class ResultadoAdaptadorMAF:
    """Resume el estado final, el motivo del cierre y la ubicación de los resultados."""

    run_id: str
    framework_id: str
    dataset_id: str
    repetition: int
    final_status: str
    reason_code: str
    output_directory: str
    review_decision: str | None
    correction_used: bool
    trace_valid: bool


class SesionMAF:
    """Aplica el contrato mediante agentes y un flujo nativo de MAF."""

    def __init__(
        self,
        configuracion: Any,
        contexto: Any,
        fabrica_cliente: FabricaClienteMAF,
        traza: EscritorTraza,
        limites: ControlLimites,
        herramientas: HerramientasComunes,
        plantillas: Any,
        documentacion_publica: str,
    ) -> None:
        self.configuracion = configuracion
        self.contexto = contexto
        self.fabrica_cliente = fabrica_cliente
        self.traza = traza
        self.limites = limites
        self.herramientas = herramientas
        self.plantillas = plantillas
        self.documentacion_publica = documentacion_publica
        self.despachador = DespachadorHerramientasMAF(herramientas)
        self.estado_actual = "initialized"
        self.contador_roles = 0
        self.contador_modelo = 0
        self.contador_errores = 0
        self.ultimo_error_id: str | None = None
        self.decision_revision: dict[str, Any] | None = None
        self.correction_used = False
        self.correction_request_id: str | None = None
        self.correction_resolved = True
        self.flujo_roles_completo = False

    def ejecutar(self) -> ResultadoAdaptadorMAF:
        cierre = None
        try:
            flujo = crear_flujo_maf(self)
            resultado_flujo = asyncio.run(flujo.run("iniciar_experimento"))
            if not resultado_flujo.get_outputs() or not self.flujo_roles_completo:
                raise CapaComunError("El flujo nativo de MAF terminó sin salida final")
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
        except Exception as exc:
            if self.estado_actual not in {
                "final_validation",
                "completed",
                "partial",
                "failed",
            }:
                try:
                    self._transicionar(
                        "final_validation",
                        f"Fallo controlado en {self.estado_actual}",
                    )
                except Exception:
                    pass
            try:
                cierre = cerrar_ejecucion_comun(
                    self.herramientas,
                    self.limites,
                    self.traza,
                    dataset_cargado=True,
                    flujo_roles_completo=False,
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
            except Exception:
                self.traza.abandonar()
                raise exc

        return ResultadoAdaptadorMAF(
            run_id=self.contexto.run_id,
            framework_id=self.contexto.framework_id,
            dataset_id=self.contexto.dataset.dataset_id,
            repetition=self.contexto.repeticion,
            final_status=cierre.estado,
            reason_code=cierre.motivo,
            output_directory=self.contexto.directorio_salida.relative_to(
                self.configuracion.raiz_tfm
            ).as_posix(),
            review_decision=(
                self.decision_revision["decision"]
                if self.decision_revision
                else None
            ),
            correction_used=self.correction_used,
            trace_valid=cierre.integridad_traza.estado == "valid",
        )

    async def ejecutar_planificador(self) -> str:
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

        return await self._intervencion(
            "planner",
            prompt,
            procesar,
            "plan.md",
            1,
        )

    async def ejecutar_analista(self, plan: str) -> str:
        self._transicionar("analysis", "Plan válido disponible")
        prompt = self._prompt(
            "analyst_initial",
            inspeccion=self.herramientas.inspeccion_cacheada(),
            plan=plan,
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

        return await self._intervencion(
            "analyst_initial",
            prompt,
            procesar,
            "report.md",
            1,
        )

    def validacion_previa(self) -> dict[str, Any]:
        respuesta = self.herramientas.validate_outputs(
            {},
            "runtime",
            trigger="pre_review",
            automatic=True,
            parent_event_id=self.traza.ultimo_evento_id,
        )
        return dict(respuesta["data"])

    async def ejecutar_revisor(
        self,
        validacion: Mapping[str, Any],
    ) -> dict[str, Any]:
        self._transicionar("review", "Resultados iniciales disponibles")
        prompt = self._prompt(
            "reviewer",
            validacion_previa=validacion,
        )

        def procesar(texto: str, evento_origen: str) -> dict[str, Any]:
            decision = interpretar_decision_revisor(texto)
            hashes = {
                artefacto["name"]: artefacto.get("sha256")
                for artefacto in validacion.get("artifacts", [])
            }
            self.traza.registrar(
                "review_decision",
                "review",
                "reviewer",
                "framework_adapter",
                {
                    "review_decision_id": f"{self.contexto.run_id}__review_001",
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

        return await self._intervencion(
            "reviewer",
            prompt,
            procesar,
            None,
            1,
        )

    async def ejecutar_correccion(
        self,
        plan: str,
        validacion_previa: Mapping[str, Any],
        decision: Mapping[str, Any],
    ) -> dict[str, Any]:
        self._transicionar("correction", "Corrección solicitada por el Revisor")
        self.correction_used = True
        self.correction_request_id = f"{self.contexto.run_id}__correction_001"
        self.herramientas.marcar_correccion_pendiente(True)
        hashes_iniciales = self._hashes_resultados()
        hallazgos = [
            hallazgo
            for hallazgo in decision["findings"]
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
                "finding_ids": [
                    hallazgo["finding_id"]
                    for hallazgo in hallazgos
                ],
                "potentially_affected_artifacts": afectados,
                "initial_hashes": hashes_iniciales,
            },
            parent_event_id=self.traza.ultimo_evento_id,
        )
        validacion_actual = dict(validacion_previa)
        validacion_actual["pending_correction"] = True
        prompt = self._prompt(
            "analyst_correction",
            inspeccion=self.herramientas.inspeccion_cacheada(),
            plan=plan,
            decision_revision=decision,
            validacion_actual=validacion_actual,
        )

        def procesar(texto: str, evento_origen: str) -> dict[str, Any]:
            respuesta = interpretar_respuesta_correccion(texto, decision)
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
                    "addressed_findings": respuesta.resumen[
                        "addressed_findings"
                    ],
                    "unresolved_findings": respuesta.resumen[
                        "unresolved_findings"
                    ],
                },
                parent_event_id=self.traza.ultimo_evento_id,
            )
            return dict(respuesta.resumen)

        return await self._intervencion(
            "analyst_correction",
            prompt,
            procesar,
            "report.md",
            2,
        )

    def preparar_cierre(self) -> None:
        self._transicionar("final_validation", "Flujo de roles finalizado")
        self.flujo_roles_completo = True

    async def _intervencion(
        self,
        rol: str,
        prompt: PromptConstruido,
        procesar: Callable[[str, str], Any],
        output_artifact: str | None,
        attempt_role: int,
        permitir_reparacion_formato: bool = True,
        usar_herramientas: bool = True,
    ) -> Any:
        self.contador_roles += 1
        role_execution_id = (
            f"{self.contexto.run_id}__role_{self.contador_roles:03d}_{rol}"
        )
        fase = FASES_ROL[rol]
        rol_traza = ROL_TRAZA[rol]
        inicio_utc = utc_actual()
        inicio_ns = time.perf_counter_ns()
        evento_inicio = self.traza.registrar(
            "role_started",
            fase,
            rol_traza,
            "framework_adapter",
            {
                "role_execution_id": role_execution_id,
                "role_name": rol_traza,
                "attempt": attempt_role,
                "started_at_utc": inicio_utc,
            },
            parent_event_id=self.traza.ultimo_evento_id,
        )
        cliente = None
        try:
            esquemas = self._schemas_rol(rol) if usar_herramientas else []
            nombres = (
                list(self.configuracion.datos["roles"][rol]["exposed_tools"])
                if usar_herramientas
                else []
            )
            herramientas = construir_herramientas_maf(
                rol,
                nombres,
                self.despachador,
            )
            cliente = self.fabrica_cliente.crear(
                self,
                rol,
                role_execution_id,
                esquemas,
                self.despachador,
            )
            agente = Agent(
                client=cliente,
                id=f"{rol}_{self.contador_roles:03d}",
                name=rol_traza,
                description="Intervención aislada del contrato común del TFM",
                instructions=prompt.instruccion_sistema,
                tools=herramientas,
                default_options=self._opciones_modelo(),
                context_providers=[],
                middleware=[],
                require_per_service_call_history_persistence=False,
                compaction_strategy=None,
                tokenizer=None,
            )
            respuesta = await asyncio.wait_for(
                agente.run(prompt.contenido_usuario),
                timeout=self.configuracion.datos["limits"]["time_seconds"][
                    "roles"
                ][rol],
            )
            if not isinstance(respuesta, AgentResponse):
                raise CapaComunError("El agente de MAF no devolvió una respuesta válida")
            texto = self._texto_final(respuesta)
            if not texto:
                raise CapaComunError("El rol terminó sin una respuesta textual")
            try:
                resultado = procesar(texto, self.traza.ultimo_evento_id)
            except (ErrorMaterializacion, ErrorPrompt) as exc:
                reparaciones = self.configuracion.datos["limits"]["retries"][
                    "format_repairs_per_role"
                ]
                puede_reparar = (
                    permitir_reparacion_formato
                    and reparaciones > 0
                    and self.limites.registrar_reintento(fase, rol)
                )
                if not puede_reparar:
                    raise
                error_id = self.registrar_error(
                    exc,
                    fase,
                    rol_traza,
                    "role_output",
                    self.traza.ultimo_evento_id,
                    retryable=True,
                    retry_triggered=True,
                )
                evento_fallo = self.traza.registrar(
                    "role_failed",
                    fase,
                    rol_traza,
                    "framework_adapter",
                    {
                        "role_execution_id": role_execution_id,
                        "role_name": rol_traza,
                        "attempt": attempt_role,
                        "finished_at_utc": utc_actual(),
                        "duration_ms": max(
                            (time.perf_counter_ns() - inicio_ns) // 1_000_000,
                            0,
                        ),
                        "outcome": "failed",
                        "output_artifact": None,
                        "error_id": error_id,
                    },
                    parent_event_id=self.traza.ultimo_evento_id,
                )
                siguiente = (
                    f"{self.contexto.run_id}__role_{self.contador_roles + 1:03d}_{rol}"
                )
                self.traza.registrar(
                    "retry_recorded",
                    fase,
                    rol_traza,
                    "framework_adapter",
                    {
                        "retry_id": (
                            f"{self.contexto.run_id}__retry_{self.limites.retries:03d}"
                        ),
                        "target_type": "role_output",
                        "failed_operation_id": role_execution_id,
                        "new_operation_id": siguiente,
                        "reason": type(exc).__name__,
                        "attempt": attempt_role + 1,
                        "authorized": True,
                    },
                    parent_event_id=evento_fallo,
                )
                prompt_reparacion = construir_prompt_reparacion_formato(
                    prompt,
                    texto,
                    str(exc),
                )
                return await self._intervencion(
                    rol,
                    prompt_reparacion,
                    procesar,
                    output_artifact,
                    attempt_role + 1,
                    permitir_reparacion_formato=False,
                    usar_herramientas=False,
                )
            self.traza.registrar(
                "role_finished",
                fase,
                rol_traza,
                "framework_adapter",
                {
                    "role_execution_id": role_execution_id,
                    "role_name": rol_traza,
                    "attempt": attempt_role,
                    "finished_at_utc": utc_actual(),
                    "duration_ms": max(
                        (time.perf_counter_ns() - inicio_ns) // 1_000_000,
                        0,
                    ),
                    "outcome": "success",
                    "output_artifact": output_artifact,
                    "error_id": None,
                },
                parent_event_id=self.traza.ultimo_evento_id,
            )
            return resultado
        except Exception as exc:
            if getattr(exc, "role_failure_recorded", False):
                raise
            error_id = getattr(exc, "error_id", None)
            if not error_id:
                error_id = self.registrar_error(
                    exc,
                    fase,
                    rol_traza,
                    "role_output",
                    evento_inicio,
                    retryable=False,
                    retry_triggered=False,
                )
            self.traza.registrar(
                "role_failed",
                fase,
                rol_traza,
                "framework_adapter",
                {
                    "role_execution_id": role_execution_id,
                    "role_name": rol_traza,
                    "attempt": attempt_role,
                    "finished_at_utc": utc_actual(),
                    "duration_ms": max(
                        (time.perf_counter_ns() - inicio_ns) // 1_000_000,
                        0,
                    ),
                    "outcome": "failed",
                    "output_artifact": None,
                    "error_id": error_id,
                },
                parent_event_id=self.traza.ultimo_evento_id,
            )
            fallo = FalloAdaptadorMAF(str(exc), error_id)
            fallo.role_failure_recorded = True
            raise fallo from exc
        finally:
            if cliente is not None:
                cerrar = getattr(getattr(cliente, "client", None), "close", None)
                if callable(cerrar):
                    await cerrar()

    def _opciones_modelo(self) -> dict[str, Any]:
        parametros = self.configuracion.datos["model"]["request_parameters"]
        return {
            "max_tokens": self.configuracion.datos["limits"]["tokens"][
                "request_output_max"
            ],
            "reasoning": descongelar(parametros["reasoning"]),
            "service_tier": parametros["service_tier"],
            "tool_choice": parametros["tool_choice"],
            "allow_multiple_tool_calls": parametros["parallel_tool_calls"],
            "truncation": parametros["truncation"],
            "background": parametros["background"],
            "store": parametros["store"],
        }

    @staticmethod
    def _texto_final(respuesta: AgentResponse) -> str:
        for mensaje in reversed(respuesta.messages):
            if str(getattr(mensaje.role, "value", mensaje.role)) != "assistant":
                continue
            textos = [
                contenido.text or ""
                for contenido in mensaje.contents
                if contenido.type == "text"
            ]
            texto = "".join(textos).strip()
            if texto:
                return texto
        return respuesta.text.strip()

    def _transicionar(self, destino: str, razon: str) -> str:
        fases = {
            "planning": ("planning", "planner"),
            "analysis": ("analysis", "analyst"),
            "review": ("review", "reviewer"),
            "correction": ("correction", "analyst"),
            "final_validation": ("final_validation", "runtime"),
        }
        fase, rol = fases[destino]
        anterior = self.traza.ultimo_evento_id
        evento = self.traza.registrar(
            "state_transition",
            fase,
            rol,
            "framework_adapter",
            {
                "from_state": self.estado_actual,
                "to_state": destino,
                "reason": razon,
                "trigger_event_id": anterior,
            },
            parent_event_id=anterior,
        )
        self.estado_actual = destino
        return evento

    def _schemas_rol(self, rol: str) -> list[Mapping[str, Any]]:
        nombres = self.configuracion.datos["roles"][rol]["exposed_tools"]
        return [ESQUEMAS_COMUNES[nombre] for nombre in nombres]

    def _prompt(self, rol: str, **contexto: Any) -> PromptConstruido:
        return construir_prompt_rol(
            self.plantillas,
            self.configuracion,
            self.contexto,
            rol,
            self.documentacion_publica,
            **contexto,
        )

    def _hashes_resultados(self) -> dict[str, str | None]:
        nombres = [
            "plan.md",
            "prepared_data.csv",
            "statistics.json",
            "issues.json",
            "report.md",
        ]
        hashes = {
            nombre: sha256_archivo(self.contexto.directorio_salida / nombre)
            if (self.contexto.directorio_salida / nombre).is_file()
            else None
            for nombre in nombres
        }
        for figura in sorted(self.contexto.directorio_figuras.glob("*.png")):
            hashes[f"figures/{figura.name}"] = sha256_archivo(figura)
        return hashes

    def registrar_error(
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
        self.ultimo_error_id = error_id
        self.limites.registrar_error(error_id, "error")
        categoria = (
            "model"
            if operacion.startswith("model")
            else "format"
            if operacion == "role_output"
            else "framework"
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
