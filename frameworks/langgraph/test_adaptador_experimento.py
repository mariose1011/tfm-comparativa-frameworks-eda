"""Pruebas sin coste del flujo experimental completo de LangGraph."""

from __future__ import annotations

import json
import tempfile
import unittest
from collections import deque
from pathlib import Path
from typing import Any, Mapping, Sequence

from langchain_core.messages import AIMessage, BaseMessage

from frameworks.langgraph.adaptador_experimento import (
    FalloModeloSimulado,
    ejecutar_experimento,
)
from frameworks.langgraph.cliente_openai import mensaje_visible


RAIZ_TFM = Path(__file__).resolve().parents[2]
RUTA_CONFIGURACION = (
    RAIZ_TFM / "experimento" / "configuracion" / "configuracion_experimento_v1.0.json"
)


class PruebasMensajeVisible(unittest.TestCase):
    def test_excluye_razonamiento_cifrado_de_la_traza(self) -> None:
        mensaje = AIMessage(
            content=[
                {
                    "type": "reasoning",
                    "encrypted_content": "contenido_cifrado_no_visible",
                },
                {"type": "text", "text": "Respuesta visible"},
            ]
        )

        visible = mensaje_visible(mensaje)
        serializado = json.dumps(visible, ensure_ascii=False)

        self.assertEqual(visible["content"], "Respuesta visible")
        self.assertNotIn("encrypted_content", serializado)
        self.assertNotIn("contenido_cifrado_no_visible", serializado)


class ModeloSecuencial:
    def __init__(self, respuestas: Sequence[AIMessage | Exception]) -> None:
        self.respuestas = deque(respuestas)
        self.invocaciones: list[dict[str, Any]] = []

    def invocar(
        self,
        mensajes: Sequence[BaseMessage],
        herramientas: Sequence[Mapping[str, Any]],
        max_output_tokens: int,
    ) -> AIMessage:
        self.invocaciones.append(
            {
                "message_types": [mensaje.type for mensaje in mensajes],
                "tools": [herramienta["name"] for herramienta in herramientas],
                "max_output_tokens": max_output_tokens,
            }
        )
        if not self.respuestas:
            raise AssertionError("El adaptador solicitó más respuestas de las previstas")
        respuesta = self.respuestas.popleft()
        if isinstance(respuesta, Exception):
            raise respuesta
        return respuesta


def _mensaje(
    indice: int,
    contenido: str = "",
    herramienta: str | None = None,
    argumentos: Mapping[str, Any] | None = None,
) -> AIMessage:
    llamadas = []
    if herramienta:
        llamadas.append(
            {
                "name": herramienta,
                "args": dict(argumentos or {}),
                "id": f"call_simulada_{indice:03d}",
                "type": "tool_call",
            }
        )
    return AIMessage(
        content=contenido,
        id=f"resp_simulada_{indice:03d}",
        tool_calls=llamadas,
        usage_metadata={
            "input_tokens": 100,
            "output_tokens": 40,
            "total_tokens": 140,
            "input_token_details": {"cache_read": 10},
            "output_token_details": {"reasoning": 5},
        },
        response_metadata={
            "id": f"resp_simulada_{indice:03d}",
            "model_name": "gpt-5.6-terra",
            "service_tier": "default",
            "finish_reason": "tool_calls" if herramienta else "stop",
        },
    )


def _plan(run_id: str) -> str:
    etapas = []
    for numero in range(1, 9):
        etapas.append(
            f"""## E{numero}

Objetivo: comprobar la etapa {numero}.

Comprobaciones: realizar una comprobación reproducible.

Variables o grupos: se concretarán a partir de la inspección.

Evidencia esperada: resultado estructurado y trazable.

Supuestos o dependencias: no se asumen hallazgos previos.
"""
        )
    return f"""# Identificación

run_id: {run_id}

framework_id: langgraph

dataset_id: D0_piloto

contract_version: 1.0

prompt_version: 1.0

# Comprensión inicial

Se analizará el dataset autorizado y se conservarán las incertidumbres.

# Preguntas analíticas

Se estudiarán la calidad, las distribuciones y las relaciones pertinentes.

# Plan por etapas

{"".join(etapas)}
# Visualizaciones previstas

Se representará una distribución relevante con una figura trazable.

# Supuestos y riesgos

Los tipos, ausencias y valores extremos deberán comprobarse.

# Criterios de finalización

Los resultados deberán ser reproducibles, coherentes y estar referenciados.
"""


def _plan_con_formato_invalido(run_id: str) -> str:
    contenido = _plan(run_id)
    for numero in range(1, 9):
        contenido = contenido.replace(
            f"## E{numero}\n",
            f"## E{numero}. Etapa {numero}\n",
        )
    return contenido


def _informe(corregido: bool = False) -> str:
    nota = " La referencia ha sido comprobada durante la corrección." if corregido else ""
    return f"""# Resumen ejecutivo

Se presenta un resultado descriptivo respaldado por evidencia [STAT-001].{nota}

# Dataset y alcance

El análisis se limita al dataset autorizado y al EDA tabular.

# Inspección, calidad y preparación

Se creó una copia preparada trazable y separada del original.

# Estadística descriptiva

El recuento de la copia preparada se conserva en [STAT-001].

# Variables, agregaciones y relaciones

Se resume una variable sin formular afirmaciones causales [STAT-001].

# Visualizaciones y hallazgos

La figura [FIG-001] está disponible en figures/fig_001_prueba.png.

# Problemas, riesgos y anomalías

Las comprobaciones realizadas están documentadas en issues.json.

# Limitaciones e incertidumbres

Esta ejecución simulada comprueba el flujo y no la calidad del análisis.

# Conclusiones

Los artefactos mantienen referencias estructurales resolubles [STAT-001].
"""


def _codigo_artefactos() -> str:
    return '''tabla = pd.read_csv(INPUT_PATH)
preparada = tabla.iloc[:2, :2].copy()
preparada.to_csv(f"{OUTPUT_DIR}/prepared_data.csv", index=False)
nombres = [str(nombre) for nombre in preparada.columns]
columnas = []
for nombre in nombres:
    columnas.append({
        "name": nombre,
        "origin": "source",
        "source_name": nombre,
        "original_type": str(tabla[nombre].dtype),
        "prepared_type": str(preparada[nombre].dtype),
        "missing_original": int(tabla[nombre].isna().sum()),
        "missing_prepared": int(preparada[nombre].isna().sum()),
        "unique_prepared": int(preparada[nombre].nunique(dropna=True))
    })
estadisticas = {
    "schema_version": "1.0",
    "run_id": RUN_ID,
    "dataset_id": DATASET_ID,
    "generated_at_utc": "2026-08-29T10:00:00Z",
    "profile": {
        "original_rows": int(tabla.shape[0]),
        "original_columns": int(tabla.shape[1]),
        "prepared_rows": int(preparada.shape[0]),
        "prepared_columns": int(preparada.shape[1]),
        "unit_of_analysis": "Una observación del dataset autorizado",
        "columns": columnas
    },
    "preparation": {
        "summary": "Se crea una copia mínima para comprobar el flujo técnico.",
        "changes": [{
            "id": "TR-001",
            "action": "selection",
            "description": "Selección de dos filas y dos columnas para la simulación",
            "justification": "Comprobar la generación controlada de resultados",
            "affected_columns": nombres,
            "rows_affected": 2,
            "before": {"rows": int(tabla.shape[0])},
            "after": {"rows": 2}
        }]
    },
    "analyses": [{
        "id": "STAT-001",
        "stage": "E1",
        "analysis_type": "count",
        "title": "Filas de la copia preparada",
        "variables": [nombres[0]],
        "population": "Copia preparada de la simulación",
        "method": "Recuento de filas",
        "result": {"rows": 2},
        "interpretation": "La copia preparada contiene dos filas."
    }],
    "figures": [{
        "id": "FIG-001",
        "file": "figures/fig_001_prueba.png",
        "title": "Figura de prueba técnica",
        "objective": "Comprobar la generación y el registro de una figura",
        "variables": [nombres[0]],
        "source_analysis_ids": ["STAT-001"]
    }],
    "limitations": ["Resultados creados para una prueba técnica simulada"]
}
with open(f"{OUTPUT_DIR}/statistics.json", "w", encoding="utf-8") as archivo:
    json.dump(estadisticas, archivo, ensure_ascii=False, indent=2, allow_nan=False)
incidencias = {
    "schema_version": "1.0",
    "run_id": RUN_ID,
    "dataset_id": DATASET_ID,
    "checks_performed": [{
        "id": "CHK-001",
        "category": "completeness",
        "description": "Comprobación de la estructura preparada",
        "outcome": "La copia preparada contiene dos filas",
        "evidence_ids": ["STAT-001"]
    }],
    "issues": []
}
with open(f"{OUTPUT_DIR}/issues.json", "w", encoding="utf-8") as archivo:
    json.dump(incidencias, archivo, ensure_ascii=False, indent=2, allow_nan=False)
plt.figure(figsize=(4, 3))
plt.plot([1, 2], [1, 2])
plt.title("Figura de prueba técnica")
plt.xlabel("Observación")
plt.ylabel("Valor")
plt.tight_layout()
plt.savefig(f"{FIGURES_DIR}/fig_001_prueba.png")
plt.close()
print("Artefactos simulados creados")
'''


def _decision_aprobada() -> str:
    return json.dumps(
        {
            "decision": "approved",
            "summary": "Los resultados permiten completar la revisión técnica.",
            "findings": [],
            "correction_requested": False,
        },
        ensure_ascii=False,
    )


def _decision_correccion() -> dict[str, Any]:
    return {
        "decision": "correction_required",
        "summary": "Debe aclararse una referencia del informe.",
        "findings": [
            {
                "finding_id": "REV-001",
                "category": "traceability",
                "severity": "medium",
                "description": "Una referencia del informe requiere aclaración.",
                "affected_artifacts": ["report.md"],
                "evidence_refs": ["# Resumen ejecutivo"],
                "evidence": "La evidencia estructurada existe, pero debe aclararse su comprobación.",
                "requires_correction": True,
                "required_change": "Aclarar que la referencia ha sido comprobada.",
                "resolution_condition": "El informe contiene la aclaración solicitada.",
            }
        ],
        "correction_requested": True,
    }


def _respuesta_correccion() -> str:
    resumen = {
        "addressed_findings": ["REV-001"],
        "unresolved_findings": [],
        "changes": [
            {
                "artifact": "report.md",
                "description": "Se aclara la comprobación de la referencia de REV-001.",
            }
        ],
    }
    return (
        "<CORRECTION_SUMMARY>\n"
        + json.dumps(resumen, ensure_ascii=False)
        + "\n</CORRECTION_SUMMARY>\n<REPORT_MD>\n"
        + _informe(corregido=True)
        + "\n</REPORT_MD>"
    )


class PruebasAdaptadorLangGraph(unittest.TestCase):
    def _configuracion_temporal(
        self,
        temporal: Path,
        sufijo: str,
        limite_planner: int | None = None,
        limite_reviewer: int | None = None,
    ) -> Path:
        datos = json.loads(RUTA_CONFIGURACION.read_text(encoding="utf-8"))
        datos["paths"]["output_root"] = (
            temporal.relative_to(RAIZ_TFM) / "resultados"
        ).as_posix()
        if limite_planner is not None:
            anterior = datos["limits"]["model_requests"]["roles"]["planner"]
            datos["limits"]["model_requests"]["roles"]["planner"] = limite_planner
            datos["limits"]["model_requests"]["run"] -= anterior - limite_planner
        if limite_reviewer is not None:
            anterior = datos["limits"]["model_requests"]["roles"]["reviewer"]
            datos["limits"]["model_requests"]["roles"]["reviewer"] = limite_reviewer
            datos["limits"]["model_requests"]["run"] -= anterior - limite_reviewer
        ruta = temporal / f"config_{sufijo}.json"
        ruta.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
        return ruta

    def test_flujo_completo_aprobado_sin_openai(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            temporal = Path(directorio)
            run_id = "D0_piloto__langgraph__r01__simulado_aprobado"
            modelo = ModeloSecuencial(
                [
                    _mensaje(1, herramienta="inspect_dataset"),
                    _mensaje(2, contenido=_plan(run_id)),
                    _mensaje(
                        3,
                        herramienta="execute_python",
                        argumentos={
                            "purpose": "Generar los resultados de la prueba técnica",
                            "code": _codigo_artefactos(),
                        },
                    ),
                    _mensaje(4, contenido=_informe()),
                    _mensaje(
                        5,
                        herramienta="read_output",
                        argumentos={
                            "artifact": "report",
                            "query": "summary",
                            "selector": None,
                            "cursor": None,
                        },
                    ),
                    _mensaje(6, contenido=_decision_aprobada()),
                ]
            )
            resultado = ejecutar_experimento(
                "D0_piloto",
                1,
                self._configuracion_temporal(temporal, "aprobado"),
                run_id,
                modelo,
            )

            self.assertEqual(resultado.final_status, "completed")
            self.assertEqual(resultado.review_decision, "approved")
            self.assertFalse(resultado.correction_used)
            self.assertTrue(resultado.trace_valid)
            self.assertEqual(len(modelo.invocaciones), 6)
            salida = RAIZ_TFM / resultado.output_directory
            self.assertEqual(
                {ruta.name for ruta in salida.iterdir()},
                {
                    "_temporary",
                    "figures",
                    "issues.json",
                    "plan.md",
                    "prepared_data.csv",
                    "report.md",
                    "statistics.json",
                    "trace.jsonl",
                },
            )

    def test_flujo_con_una_unica_correccion(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            temporal = Path(directorio)
            run_id = "D0_piloto__langgraph__r01__simulado_correccion"
            decision = _decision_correccion()
            modelo = ModeloSecuencial(
                [
                    _mensaje(1, herramienta="inspect_dataset"),
                    _mensaje(2, contenido=_plan(run_id)),
                    _mensaje(
                        3,
                        herramienta="execute_python",
                        argumentos={
                            "purpose": "Generar los resultados de la prueba técnica",
                            "code": _codigo_artefactos(),
                        },
                    ),
                    _mensaje(4, contenido=_informe()),
                    _mensaje(5, contenido=json.dumps(decision, ensure_ascii=False)),
                    _mensaje(
                        6,
                        herramienta="read_output",
                        argumentos={
                            "artifact": "report",
                            "query": "summary",
                            "selector": None,
                            "cursor": None,
                        },
                    ),
                    _mensaje(7, contenido=_respuesta_correccion()),
                ]
            )
            resultado = ejecutar_experimento(
                "D0_piloto",
                1,
                self._configuracion_temporal(temporal, "correccion"),
                run_id,
                modelo,
            )

            self.assertEqual(resultado.final_status, "completed")
            self.assertEqual(resultado.review_decision, "correction_required")
            self.assertTrue(resultado.correction_used)
            self.assertTrue(resultado.trace_valid)
            traza = (
                RAIZ_TFM / resultado.output_directory / "trace.jsonl"
            ).read_text(encoding="utf-8")
            self.assertEqual(traza.count('"event_type":"correction_started"'), 1)
            self.assertEqual(traza.count('"event_type":"correction_finished"'), 1)

    def test_repara_una_salida_de_plan_con_formato_invalido(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            temporal = Path(directorio)
            run_id = "D0_piloto__langgraph__r01__simulado_reparacion_formato"
            modelo = ModeloSecuencial(
                [
                    _mensaje(1, herramienta="inspect_dataset"),
                    _mensaje(2, contenido=_plan_con_formato_invalido(run_id)),
                    _mensaje(3, contenido=_plan(run_id)),
                    _mensaje(
                        4,
                        herramienta="execute_python",
                        argumentos={
                            "purpose": "Generar los resultados de la prueba técnica",
                            "code": _codigo_artefactos(),
                        },
                    ),
                    _mensaje(5, contenido=_informe()),
                    _mensaje(6, contenido=_decision_aprobada()),
                ]
            )
            resultado = ejecutar_experimento(
                "D0_piloto",
                1,
                self._configuracion_temporal(temporal, "reparacion_formato"),
                run_id,
                modelo,
            )

            self.assertEqual(resultado.final_status, "completed")
            self.assertTrue(resultado.trace_valid)
            self.assertEqual(modelo.invocaciones[2]["tools"], [])
            traza = (
                RAIZ_TFM / resultado.output_directory / "trace.jsonl"
            ).read_text(encoding="utf-8")
            self.assertIn('"target_type":"role_output"', traza)
            self.assertIn('"severity":"recoverable"', traza)
            self.assertEqual(traza.count('"event_type":"retry_recorded"'), 1)

    def test_no_repara_dos_veces_la_salida_del_planificador(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            temporal = Path(directorio)
            run_id = "D0_piloto__langgraph__r01__simulado_formato_fallido"
            invalido = _plan_con_formato_invalido(run_id)
            modelo = ModeloSecuencial(
                [
                    _mensaje(1, herramienta="inspect_dataset"),
                    _mensaje(2, contenido=invalido),
                    _mensaje(3, contenido=invalido),
                ]
            )
            resultado = ejecutar_experimento(
                "D0_piloto",
                1,
                self._configuracion_temporal(temporal, "formato_fallido"),
                run_id,
                modelo,
            )

            self.assertEqual(resultado.final_status, "failed")
            self.assertTrue(resultado.trace_valid)
            traza = (
                RAIZ_TFM / resultado.output_directory / "trace.jsonl"
            ).read_text(encoding="utf-8")
            self.assertEqual(traza.count('"event_type":"retry_recorded"'), 1)
            self.assertEqual(traza.count('"event_type":"role_failed"'), 2)

    def test_limite_de_modelo_interrumpe_el_flujo_y_cierra_failed(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            temporal = Path(directorio)
            run_id = "D0_piloto__langgraph__r01__simulado_limite"
            modelo = ModeloSecuencial([_mensaje(1, herramienta="inspect_dataset")])
            resultado = ejecutar_experimento(
                "D0_piloto",
                1,
                self._configuracion_temporal(temporal, "limite", limite_planner=1),
                run_id,
                modelo,
            )

            self.assertEqual(resultado.final_status, "failed")
            self.assertEqual(resultado.reason_code, "REPORT_MISSING_OR_INVALID")
            self.assertTrue(resultado.trace_valid)
            self.assertEqual(len(modelo.invocaciones), 1)
            traza = (
                RAIZ_TFM / resultado.output_directory / "trace.jsonl"
            ).read_text(encoding="utf-8")
            self.assertIn('"event_type":"limit_reached"', traza)
            self.assertIn('"event_type":"role_failed"', traza)

    def test_limite_durante_revision_con_informe_valido_cierra_partial(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            temporal = Path(directorio)
            run_id = "D0_piloto__langgraph__r01__simulado_limite_revision"
            modelo = ModeloSecuencial(
                [
                    _mensaje(1, herramienta="inspect_dataset"),
                    _mensaje(2, contenido=_plan(run_id)),
                    _mensaje(
                        3,
                        herramienta="execute_python",
                        argumentos={
                            "purpose": "Generar los resultados de la prueba técnica",
                            "code": _codigo_artefactos(),
                        },
                    ),
                    _mensaje(4, contenido=_informe()),
                    _mensaje(
                        5,
                        herramienta="read_output",
                        argumentos={
                            "artifact": "report",
                            "query": "summary",
                            "selector": None,
                            "cursor": None,
                        },
                    ),
                ]
            )
            resultado = ejecutar_experimento(
                "D0_piloto",
                1,
                self._configuracion_temporal(
                    temporal,
                    "limite_revision",
                    limite_reviewer=1,
                ),
                run_id,
                modelo,
            )

            self.assertEqual(resultado.final_status, "partial")
            self.assertEqual(
                resultado.reason_code,
                "LIMIT_REACHED_WITH_EVALUABLE_OUTPUT",
            )
            self.assertIsNone(resultado.review_decision)
            self.assertTrue(resultado.trace_valid)
            traza = (
                RAIZ_TFM / resultado.output_directory / "trace.jsonl"
            ).read_text(encoding="utf-8")
            self.assertIn('"event_type":"limit_reached"', traza)
            self.assertIn('"event_type":"role_failed"', traza)

    def test_fallo_del_proveedor_se_registra_y_cierra_failed(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            temporal = Path(directorio)
            run_id = "D0_piloto__langgraph__r01__simulado_fallo"
            modelo = ModeloSecuencial(
                [FalloModeloSimulado("Fallo local simulado", retryable=False)]
            )
            resultado = ejecutar_experimento(
                "D0_piloto",
                1,
                self._configuracion_temporal(temporal, "fallo"),
                run_id,
                modelo,
            )

            self.assertEqual(resultado.final_status, "failed")
            self.assertTrue(resultado.trace_valid)
            traza = (
                RAIZ_TFM / resultado.output_directory / "trace.jsonl"
            ).read_text(encoding="utf-8")
            self.assertIn('"event_type":"model_call_failed"', traza)
            self.assertIn('"event_type":"error_recorded"', traza)

    def test_un_error_transitorio_admite_un_solo_reintento_visible(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            temporal = Path(directorio)
            run_id = "D0_piloto__langgraph__r01__simulado_reintento"
            modelo = ModeloSecuencial(
                [
                    FalloModeloSimulado("Fallo transitorio simulado", retryable=True),
                    _mensaje(1, herramienta="inspect_dataset"),
                    _mensaje(2, contenido=_plan(run_id)),
                    _mensaje(
                        3,
                        herramienta="execute_python",
                        argumentos={
                            "purpose": "Generar los resultados de la prueba técnica",
                            "code": _codigo_artefactos(),
                        },
                    ),
                    _mensaje(4, contenido=_informe()),
                    _mensaje(5, contenido=_decision_aprobada()),
                ]
            )
            resultado = ejecutar_experimento(
                "D0_piloto",
                1,
                self._configuracion_temporal(temporal, "reintento"),
                run_id,
                modelo,
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
