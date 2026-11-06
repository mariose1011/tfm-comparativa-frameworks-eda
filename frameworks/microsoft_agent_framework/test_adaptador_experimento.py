"""Pruebas sin coste del adaptador de Microsoft Agent Framework."""

from __future__ import annotations

import json
import tempfile
import unittest
from collections import deque
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Mapping, Sequence

from agent_framework import ChatResponse, Content, Message

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
from .modelo import ClienteOpenAIMAFControlado, RegistroModeloMAF


RAIZ_TFM = Path(__file__).resolve().parents[2]
RUTA_CONFIGURACION = (
    RAIZ_TFM / "experimento" / "configuracion" / "configuracion_experimento_v1.0.json"
)


class FalloModeloSimulado(Exception):
    """Fallo determinista para comprobar el reintento controlado."""

    def __init__(self, mensaje: str, retryable: bool = False) -> None:
        super().__init__(mensaje)
        self.retryable = retryable


class ClienteMAFSimulado(ClienteOpenAIMAFControlado):
    """Cliente local que conserva el bucle nativo de funciones de MAF."""

    def __init__(
        self,
        respuestas: deque[dict[str, Any] | Exception],
        invocaciones: list[dict[str, Any]],
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.respuestas = respuestas
        self.invocaciones = invocaciones

    def _inner_get_response(
        self,
        *,
        messages: Sequence[Message],
        options: Mapping[str, Any],
        stream: bool = False,
        **_: Any,
    ) -> Any:
        async def responder() -> ChatResponse:
            if stream:
                raise AssertionError("La prueba no admite streaming")
            parametros = await self._prepare_options(messages, options)
            self.invocaciones.append(parametros)
            if not self.respuestas:
                raise AssertionError("El guion simulado no contiene más respuestas")
            preparada = self.respuestas.popleft()
            if isinstance(preparada, Exception):
                raise preparada

            indice = len(self.invocaciones)
            response_id = f"resp_simulada_{indice:03d}"
            if preparada.get("tool"):
                contenido = Content.from_function_call(
                    call_id=f"call_simulada_{indice:03d}",
                    name=preparada["tool"],
                    arguments=preparada.get("arguments", {}),
                )
                finish_reason = "tool_calls"
            else:
                contenido = Content.from_text(
                    text=str(preparada.get("content", ""))
                )
                finish_reason = "stop"
            return ChatResponse(
                messages=Message("assistant", [contenido]),
                response_id=response_id,
                conversation_id=response_id,
                model="gpt-5.6-terra",
                finish_reason=finish_reason,
                usage_details={
                    "input_token_count": 100,
                    "output_token_count": 40,
                    "total_token_count": 140,
                    "cache_read_input_token_count": 10,
                    "reasoning_output_token_count": 5,
                },
                raw_representation=SimpleNamespace(service_tier="default"),
            )

        return responder()


class FabricaSecuencialMAF:
    """Comparte un único guion entre los clientes aislados de los roles."""

    def __init__(self, respuestas: Sequence[dict[str, Any] | Exception]) -> None:
        self.respuestas = deque(respuestas)
        self.invocaciones: list[dict[str, Any]] = []

    def crear(
        self,
        sesion: Any,
        rol: str,
        role_execution_id: str,
        esquemas: Sequence[Mapping[str, Any]],
        despachador: Any,
    ) -> ClienteMAFSimulado:
        limites = sesion.configuracion.datos["limits"]
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
        return ClienteMAFSimulado(
            respuestas=self.respuestas,
            invocaciones=self.invocaciones,
            model="gpt-5.6-terra",
            api_key="clave_simulada",
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


def _plan_maf(run_id: str) -> str:
    return plan_simulado(run_id, "microsoft_agent_framework")


class PruebasAdaptadorMAF(unittest.TestCase):
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

    def test_flujo_completo_usa_maf_y_la_capa_comun(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            temporal = Path(directorio)
            run_id = (
                "D0_piloto__microsoft_agent_framework__r01__simulado_aprobado"
            )
            fabrica = FabricaSecuencialMAF(
                [
                    _llamada_herramienta("inspect_dataset"),
                    _texto(_plan_maf(run_id)),
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

            primera = fabrica.invocaciones[0]
            self.assertEqual(primera["input"][0]["role"], "user")
            self.assertTrue(primera.get("instructions"))
            serializado = json.dumps(fabrica.invocaciones, ensure_ascii=False)
            self.assertNotIn("Current Task", serializado)
            self.assertNotIn("expected criteria", serializado)
            for invocacion in fabrica.invocaciones:
                for herramienta in invocacion.get("tools", []):
                    self.assertTrue(herramienta.get("strict"))

    def test_flujo_con_una_correccion(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            temporal = Path(directorio)
            run_id = (
                "D0_piloto__microsoft_agent_framework__r01__simulado_correccion"
            )
            decision = decision_correccion_simulada()
            fabrica = FabricaSecuencialMAF(
                [
                    _llamada_herramienta("inspect_dataset"),
                    _texto(_plan_maf(run_id)),
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
            run_id = (
                "D0_piloto__microsoft_agent_framework__r01__"
                "simulado_reparacion_formato"
            )
            fabrica = FabricaSecuencialMAF(
                [
                    _llamada_herramienta("inspect_dataset"),
                    _texto(
                        plan_simulado_con_formato_invalido(
                            run_id,
                            "microsoft_agent_framework",
                        )
                    ),
                    _texto(_plan_maf(run_id)),
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
            run_id = (
                "D0_piloto__microsoft_agent_framework__r01__"
                "simulado_formato_fallido"
            )
            invalido = plan_simulado_con_formato_invalido(
                run_id,
                "microsoft_agent_framework",
            )
            fabrica = FabricaSecuencialMAF(
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

    def test_limite_del_planificador_cierra_failed(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            temporal = Path(directorio)
            run_id = "D0_piloto__microsoft_agent_framework__r01__simulado_limite"
            fabrica = FabricaSecuencialMAF(
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
            run_id = (
                "D0_piloto__microsoft_agent_framework__r01__simulado_reintento"
            )
            fabrica = FabricaSecuencialMAF(
                [
                    FalloModeloSimulado("Fallo transitorio", retryable=True),
                    _llamada_herramienta("inspect_dataset"),
                    _texto(_plan_maf(run_id)),
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
