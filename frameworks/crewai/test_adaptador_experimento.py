"""Pruebas sin coste del adaptador experimental de CrewAI."""

from __future__ import annotations

import json
import tempfile
import unittest
from collections import deque
from pathlib import Path
from typing import Any, Mapping, Sequence

from crewai.events.types.llm_events import LLMCallType
from pydantic import PrivateAttr

from experimento.capa_comun import PromptConstruido
from experimento.capa_comun.tests.fixtures_adaptadores import (
    codigo_artefactos_simulados,
    decision_aprobada_simulada,
    decision_correccion_simulada,
    informe_simulado,
    plan_simulado,
    plan_simulado_con_formato_invalido,
    respuesta_correccion_simulada,
)

from .adaptador_experimento import ejecutar_experimento
from .modelo import ModeloOpenAICrewAIControlado


RAIZ_TFM = Path(__file__).resolve().parents[2]
RUTA_CONFIGURACION = (
    RAIZ_TFM / "experimento" / "configuracion" / "configuracion_experimento_v1.0.json"
)


class FalloModeloSimulado(Exception):
    """Fallo determinista empleado para comprobar el cierre controlado."""

    def __init__(self, mensaje: str, retryable: bool = False) -> None:
        super().__init__(mensaje)
        self.retryable = retryable


class ModeloCrewAISimulado(ModeloOpenAICrewAIControlado):
    """Proveedor local que conserva el ciclo nativo de CrewAI."""

    _respuestas: deque[dict[str, Any] | Exception] = PrivateAttr()
    _invocaciones: list[dict[str, Any]] = PrivateAttr()

    def __init__(
        self,
        respuestas: deque[dict[str, Any] | Exception],
        invocaciones: list[dict[str, Any]],
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self._respuestas = respuestas
        self._invocaciones = invocaciones

    def _call_responses(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        available_functions: dict[str, Any] | None = None,
        from_task: Any | None = None,
        from_agent: Any | None = None,
        response_model: type[Any] | None = None,
    ) -> str | Any:
        parametros = self._prepare_responses_params(
            messages=messages,
            tools=tools,
            response_model=response_model,
        )
        self._invocaciones.append(parametros)
        if not self._respuestas:
            raise AssertionError("El guion simulado no contiene más respuestas")
        preparada = self._respuestas.popleft()
        if isinstance(preparada, Exception):
            raise preparada

        indice = len(self._invocaciones)
        uso = {
            "prompt_tokens": 100,
            "completion_tokens": 40,
            "total_tokens": 140,
            "cached_prompt_tokens": 10,
            "reasoning_tokens": 5,
        }
        self._track_token_usage_internal(uso)
        if self._captura is not None:
            self._captura.uso = dict(uso)
            self._captura.reported_model = "gpt-5.6-terra"
            self._captura.reported_service_tier = "default"

        if preparada.get("tool"):
            respuesta: str | list[dict[str, Any]] = [
                {
                    "id": f"call_simulada_{indice:03d}",
                    "name": preparada["tool"],
                    "arguments": json.dumps(
                        preparada.get("arguments", {}),
                        ensure_ascii=False,
                    ),
                }
            ]
            tipo = LLMCallType.TOOL_CALL
        else:
            respuesta = str(preparada.get("content", ""))
            tipo = LLMCallType.LLM_CALL

        self._emit_call_completed_event(
            response=respuesta,
            call_type=tipo,
            from_task=from_task,
            from_agent=from_agent,
            messages=messages,
            usage=uso,
            finish_reason="completed",
            response_id=f"resp_simulada_{indice:03d}",
        )
        return respuesta


class FabricaSecuencialCrewAI:
    """Comparte un único guion entre los contextos aislados de los roles."""

    def __init__(self, respuestas: Sequence[dict[str, Any] | Exception]) -> None:
        self.respuestas = deque(respuestas)
        self.invocaciones: list[dict[str, Any]] = []

    def crear(
        self,
        sesion: Any,
        rol: str,
        role_execution_id: str,
        prompt: PromptConstruido,
        esquemas: Sequence[Mapping[str, Any]],
        despachador: Any,
    ) -> ModeloCrewAISimulado:
        return ModeloCrewAISimulado(
            respuestas=self.respuestas,
            invocaciones=self.invocaciones,
            sesion=sesion,
            rol=rol,
            role_execution_id=role_execution_id,
            prompt=prompt,
            esquemas=esquemas,
            despachador=despachador,
            model="gpt-5.6-terra",
            provider="openai",
            api="responses",
            api_key="clave_simulada",
            max_completion_tokens=32000,
            reasoning_effort="medium",
            timeout=300,
            max_retries=0,
            stream=False,
            store=True,
            auto_chain=False,
            additional_params={
                "service_tier": "default",
                "tool_choice": "auto",
                "parallel_tool_calls": False,
                "truncation": "disabled",
                "background": False,
            },
            stop=[],
        )


def _llamada_herramienta(
    nombre: str,
    argumentos: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "tool": nombre,
        "arguments": dict(argumentos or {}),
    }


def _texto(contenido: str) -> dict[str, Any]:
    return {"content": contenido}


def _plan_crewai(run_id: str) -> str:
    return plan_simulado(run_id, "crewai")


class PruebasAdaptadorCrewAI(unittest.TestCase):
    def _configuracion_temporal(
        self,
        temporal: Path,
        sufijo: str,
        limite_planner: int | None = None,
    ) -> Path:
        datos = json.loads(RUTA_CONFIGURACION.read_text(encoding="utf-8"))
        datos["paths"]["output_root"] = (
            temporal.relative_to(RAIZ_TFM) / "resultados"
        ).as_posix()
        if limite_planner is not None:
            anterior = datos["limits"]["model_requests"]["roles"]["planner"]
            datos["limits"]["model_requests"]["roles"]["planner"] = limite_planner
            datos["limits"]["model_requests"]["run"] -= anterior - limite_planner
        ruta = temporal / f"config_{sufijo}.json"
        ruta.write_text(
            json.dumps(datos, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return ruta

    def test_flujo_completo_usa_crewai_y_la_capa_comun(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            temporal = Path(directorio)
            run_id = "D0_piloto__crewai__r01__simulado_aprobado"
            fabrica = FabricaSecuencialCrewAI(
                [
                    _llamada_herramienta("inspect_dataset"),
                    _texto(_plan_crewai(run_id)),
                    _llamada_herramienta(
                        "execute_python",
                        {
                            "purpose": "Generar los resultados de la prueba técnica",
                            "code": codigo_artefactos_simulados(),
                        },
                    ),
                    _texto(informe_simulado()),
                    _llamada_herramienta(
                        "read_output",
                        {
                            "artifact": "report",
                            "query": "summary",
                            "selector": None,
                            "cursor": None,
                        },
                    ),
                    _texto(decision_aprobada_simulada()),
                ]
            )
            resultado = ejecutar_experimento(
                "D0_piloto",
                1,
                self._configuracion_temporal(temporal, "aprobado"),
                run_id,
                fabrica,
            )

            self.assertEqual(resultado.final_status, "completed")
            self.assertEqual(resultado.review_decision, "approved")
            self.assertTrue(resultado.trace_valid)
            self.assertEqual(len(fabrica.invocaciones), 6)
            salida = RAIZ_TFM / resultado.output_directory
            self.assertTrue((salida / "report.md").is_file())
            self.assertTrue((salida / "statistics.json").is_file())
            self.assertTrue((salida / "trace.jsonl").is_file())

            for invocacion in fabrica.invocaciones:
                self.assertEqual(invocacion["input"][0]["role"], "user")
                self.assertNotIn("Current Task", json.dumps(invocacion))
                self.assertNotIn("expected criteria", json.dumps(invocacion))
                self.assertTrue(invocacion.get("instructions"))
                for herramienta in invocacion.get("tools", []):
                    self.assertTrue(herramienta.get("strict"))

    def test_flujo_con_una_correccion(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            temporal = Path(directorio)
            run_id = "D0_piloto__crewai__r01__simulado_correccion"
            decision = decision_correccion_simulada()
            fabrica = FabricaSecuencialCrewAI(
                [
                    _llamada_herramienta("inspect_dataset"),
                    _texto(_plan_crewai(run_id)),
                    _llamada_herramienta(
                        "execute_python",
                        {
                            "purpose": "Generar los resultados de la prueba técnica",
                            "code": codigo_artefactos_simulados(),
                        },
                    ),
                    _texto(informe_simulado()),
                    _texto(json.dumps(decision, ensure_ascii=False)),
                    _llamada_herramienta(
                        "read_output",
                        {
                            "artifact": "report",
                            "query": "summary",
                            "selector": None,
                            "cursor": None,
                        },
                    ),
                    _texto(respuesta_correccion_simulada()),
                ]
            )
            resultado = ejecutar_experimento(
                "D0_piloto",
                1,
                self._configuracion_temporal(temporal, "correccion"),
                run_id,
                fabrica,
            )

            self.assertEqual(resultado.final_status, "completed")
            self.assertTrue(resultado.correction_used)
            self.assertTrue(resultado.trace_valid)

    def test_repara_una_salida_de_plan_con_formato_invalido(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            temporal = Path(directorio)
            run_id = "D0_piloto__crewai__r01__simulado_reparacion_formato"
            fabrica = FabricaSecuencialCrewAI(
                [
                    _llamada_herramienta("inspect_dataset"),
                    _texto(plan_simulado_con_formato_invalido(run_id, "crewai")),
                    _texto(_plan_crewai(run_id)),
                    _llamada_herramienta(
                        "execute_python",
                        {
                            "purpose": "Generar los resultados de la prueba técnica",
                            "code": codigo_artefactos_simulados(),
                        },
                    ),
                    _texto(informe_simulado()),
                    _texto(decision_aprobada_simulada()),
                ]
            )
            resultado = ejecutar_experimento(
                "D0_piloto",
                1,
                self._configuracion_temporal(temporal, "reparacion_formato"),
                run_id,
                fabrica,
            )

            self.assertEqual(resultado.final_status, "completed")
            self.assertTrue(resultado.trace_valid)
            self.assertEqual(fabrica.invocaciones[2].get("tools", []), [])
            traza = (
                RAIZ_TFM / resultado.output_directory / "trace.jsonl"
            ).read_text(encoding="utf-8")
            self.assertIn('"target_type":"role_output"', traza)
            self.assertIn('"severity":"recoverable"', traza)
            self.assertEqual(traza.count('"event_type":"retry_recorded"'), 1)

    def test_no_repara_dos_veces_la_salida_del_planificador(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            temporal = Path(directorio)
            run_id = "D0_piloto__crewai__r01__simulado_formato_fallido"
            invalido = plan_simulado_con_formato_invalido(run_id, "crewai")
            fabrica = FabricaSecuencialCrewAI(
                [
                    _llamada_herramienta("inspect_dataset"),
                    _texto(invalido),
                    _texto(invalido),
                ]
            )
            resultado = ejecutar_experimento(
                "D0_piloto",
                1,
                self._configuracion_temporal(temporal, "formato_fallido"),
                run_id,
                fabrica,
            )

            self.assertEqual(resultado.final_status, "failed")
            self.assertTrue(resultado.trace_valid)
            traza = (
                RAIZ_TFM / resultado.output_directory / "trace.jsonl"
            ).read_text(encoding="utf-8")
            self.assertEqual(traza.count('"event_type":"retry_recorded"'), 1)
            self.assertEqual(traza.count('"event_type":"role_failed"'), 2)

    def test_limite_del_planificador_cierra_failed_sin_salida_inventada(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            temporal = Path(directorio)
            run_id = "D0_piloto__crewai__r01__simulado_limite"
            fabrica = FabricaSecuencialCrewAI(
                [_llamada_herramienta("inspect_dataset")]
            )
            resultado = ejecutar_experimento(
                "D0_piloto",
                1,
                self._configuracion_temporal(
                    temporal,
                    "limite",
                    limite_planner=1,
                ),
                run_id,
                fabrica,
            )

            self.assertEqual(resultado.final_status, "failed")
            self.assertEqual(resultado.reason_code, "REPORT_MISSING_OR_INVALID")
            self.assertTrue(resultado.trace_valid)
            self.assertEqual(len(fabrica.invocaciones), 1)

    def test_reintento_transitorio_es_unico_y_visible(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            temporal = Path(directorio)
            run_id = "D0_piloto__crewai__r01__simulado_reintento"
            fabrica = FabricaSecuencialCrewAI(
                [
                    FalloModeloSimulado("Fallo transitorio", retryable=True),
                    _llamada_herramienta("inspect_dataset"),
                    _texto(_plan_crewai(run_id)),
                    _llamada_herramienta(
                        "execute_python",
                        {
                            "purpose": "Generar los resultados de la prueba técnica",
                            "code": codigo_artefactos_simulados(),
                        },
                    ),
                    _texto(informe_simulado()),
                    _texto(decision_aprobada_simulada()),
                ]
            )
            resultado = ejecutar_experimento(
                "D0_piloto",
                1,
                self._configuracion_temporal(temporal, "reintento"),
                run_id,
                fabrica,
            )

            self.assertEqual(resultado.final_status, "completed")
            self.assertTrue(resultado.trace_valid)
            traza = (
                RAIZ_TFM / resultado.output_directory / "trace.jsonl"
            ).read_text(encoding="utf-8")
            self.assertEqual(traza.count('"event_type":"retry_recorded"'), 1)
            self.assertEqual(traza.count('"event_type":"model_call_failed"'), 1)


if __name__ == "__main__":
    unittest.main()
