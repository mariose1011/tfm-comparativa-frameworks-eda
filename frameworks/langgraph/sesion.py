"""Coordinación de una ejecución experimental de LangGraph."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Any, Callable, Mapping, Sequence

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, ToolMessage

from experimento.capa_comun import (
    ESQUEMA_EXECUTE_PYTHON,
    ESQUEMA_INSPECT_DATASET,
    ESQUEMA_READ_OUTPUT,
    ESQUEMA_VALIDATE_OUTPUTS,
    CapaComunError,
    ControlLimites,
    ErrorMaterializacion,
    ErrorPrompt,
    EscritorTraza,
    HerramientasComunes,
    cerrar_ejecucion_comun,
    construir_prompt_reparacion_formato,
    construir_prompt_rol,
)
from experimento.capa_comun.prompts import PromptConstruido
from experimento.capa_comun.utilidades import sha256_archivo

from .cliente_openai import (
    FalloAdaptador,
    ProveedorModelo,
    texto_mensaje,
    utc_actual,
)
from .grafo import GrafoLangGraph
from .registro_modelo import FASES_ROL, ROL_TRAZA, RegistroModeloLangGraph


ESQUEMAS = {
    "inspect_dataset": ESQUEMA_INSPECT_DATASET,
    "execute_python": ESQUEMA_EXECUTE_PYTHON,
    "read_output": ESQUEMA_READ_OUTPUT,
    "validate_outputs": ESQUEMA_VALIDATE_OUTPUTS,
}


@dataclass(frozen=True, slots=True)
class ResultadoAdaptadorLangGraph:
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


@dataclass(frozen=True, slots=True)
class ResultadoDialogo:
    """Respuesta textual de un rol y evento que la originó."""

    texto: str
    ultimo_evento_modelo: str


class SesionLangGraph(GrafoLangGraph, RegistroModeloLangGraph):
    """Mantiene el estado técnico y aplica el contrato durante una ejecución."""

    def __init__(
        self,
        configuracion: Any,
        contexto: Any,
        modelo: ProveedorModelo,
        traza: EscritorTraza,
        limites: ControlLimites,
        herramientas: HerramientasComunes,
        plantillas: Any,
        documentacion_publica: str,
    ) -> None:
        self.configuracion = configuracion
        self.contexto = contexto
        self.modelo = modelo
        self.traza = traza
        self.limites = limites
        self.herramientas = herramientas
        self.plantillas = plantillas
        self.documentacion_publica = documentacion_publica
        self.estado_actual = "initialized"
        self.contador_roles = 0
        self.contador_modelo = 0
        self.contador_errores = 0
        self.decision_revision: dict[str, Any] | None = None
        self.correction_used = False
        self.correction_request_id: str | None = None
        self.correction_resolved = True

    def ejecutar(self) -> ResultadoAdaptadorLangGraph:
        cierre = None
        try:
            estado = self.construir_grafo().invoke({})
            cierre = estado["resultado_cierre"]
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
        return ResultadoAdaptadorLangGraph(
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
                self.decision_revision["decision"] if self.decision_revision else None
            ),
            correction_used=self.correction_used,
            trace_valid=cierre.integridad_traza.estado == "valid",
        )

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
        return [ESQUEMAS[nombre] for nombre in nombres]

    def _prompt(self, rol: str, **contexto: Any) -> PromptConstruido:
        return construir_prompt_rol(
            self.plantillas,
            self.configuracion,
            self.contexto,
            rol,
            self.documentacion_publica,
            **contexto,
        )

    def _intervencion(
        self,
        rol: str,
        prompt: PromptConstruido,
        schemas: Sequence[Mapping[str, Any]],
        procesar: Callable[[str, str], Any],
        output_artifact: str | None,
        attempt_role: int,
        permitir_reparacion_formato: bool = True,
    ) -> Any:
        self.contador_roles += 1
        role_execution_id = (
            f"{self.contexto.run_id}__role_{self.contador_roles:03d}_{rol}"
        )
        fase = FASES_ROL[rol]
        rol_traza = ROL_TRAZA[rol]
        inicio_utc = utc_actual()
        inicio = time.perf_counter_ns()
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
        try:
            dialogo = self._dialogo(
                rol,
                role_execution_id,
                prompt,
                schemas,
                evento_inicio,
            )
            try:
                resultado = procesar(
                    dialogo.texto,
                    dialogo.ultimo_evento_modelo,
                )
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
                error_id = self._registrar_error(
                    exc,
                    fase,
                    rol_traza,
                    "role_output",
                    dialogo.ultimo_evento_modelo,
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
                            (time.perf_counter_ns() - inicio) // 1_000_000,
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
                    dialogo.texto,
                    str(exc),
                )
                return self._intervencion(
                    rol,
                    prompt_reparacion,
                    [],
                    procesar,
                    output_artifact,
                    attempt_role + 1,
                    permitir_reparacion_formato=False,
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
                        (time.perf_counter_ns() - inicio) // 1_000_000,
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
                error_id = self._registrar_error(
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
                        (time.perf_counter_ns() - inicio) // 1_000_000,
                        0,
                    ),
                    "outcome": "failed",
                    "output_artifact": None,
                    "error_id": error_id,
                },
                parent_event_id=self.traza.ultimo_evento_id,
            )
            fallo = FalloAdaptador(str(exc), error_id)
            fallo.role_failure_recorded = True
            raise fallo from exc

    def _dialogo(
        self,
        rol: str,
        role_execution_id: str,
        prompt: PromptConstruido,
        schemas: Sequence[Mapping[str, Any]],
        parent_event_id: str,
    ) -> ResultadoDialogo:
        mensajes: list[BaseMessage] = [
            SystemMessage(content=prompt.instruccion_sistema),
            HumanMessage(content=prompt.contenido_usuario),
        ]
        ultimo_evento = parent_event_id
        while True:
            mensaje, model_call_id, ultimo_evento = self._llamar_modelo(
                rol,
                role_execution_id,
                mensajes,
                schemas,
                ultimo_evento,
            )
            mensajes.append(mensaje)
            if mensaje.tool_calls:
                for llamada in mensaje.tool_calls:
                    nombre = llamada.get("name")
                    if nombre not in {schema["name"] for schema in schemas}:
                        raise CapaComunError(
                            f"Herramienta no autorizada solicitada: {nombre}"
                        )
                    argumentos = llamada.get("args")
                    if isinstance(argumentos, str):
                        try:
                            argumentos = json.loads(argumentos)
                        except json.JSONDecodeError as exc:
                            raise CapaComunError(
                                f"Argumentos no válidos para {nombre}"
                            ) from exc
                    respuesta = self._ejecutar_herramienta(
                        nombre,
                        argumentos,
                        rol,
                        model_call_id,
                        role_execution_id,
                        ultimo_evento,
                    )
                    ultimo_evento = self.traza.ultimo_evento_id
                    mensajes.append(
                        ToolMessage(
                            content=json.dumps(
                                respuesta,
                                ensure_ascii=False,
                                allow_nan=False,
                            ),
                            tool_call_id=str(llamada.get("id")),
                            name=str(nombre),
                        )
                    )
                continue
            texto = texto_mensaje(mensaje)
            if not texto:
                raise CapaComunError("El rol terminó sin una respuesta textual")
            return ResultadoDialogo(
                texto=texto,
                ultimo_evento_modelo=ultimo_evento,
            )

    def _ejecutar_herramienta(
        self,
        nombre: str,
        argumentos: Mapping[str, Any] | None,
        rol: str,
        model_call_id: str,
        role_execution_id: str,
        parent_event_id: str,
    ) -> dict[str, Any]:
        comunes = {
            "rol": rol,
            "model_call_id": model_call_id,
            "role_execution_id": role_execution_id,
            "parent_event_id": parent_event_id,
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
