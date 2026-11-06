"""Pruebas de lectura, validación y estado terminal de las salidas."""

from __future__ import annotations

import base64
import json
import tempfile
import unittest
from pathlib import Path

from experimento.capa_comun.herramientas import HerramientasComunes
from experimento.capa_comun.artefactos import (
    ErrorMaterializacion,
    materializar_markdown_rol,
)
from experimento.capa_comun.cierre import cerrar_ejecucion_comun
from experimento.capa_comun.limites import ControlLimites
from experimento.capa_comun.validacion import (
    ValidadorSalidas,
    determinar_estado_terminal,
)

from .test_traza_limites import (
    RAIZ_TFM,
    _cerrar_ejecucion,
    _crear_contexto,
    _crear_escritor,
)


PNG_UN_PIXEL = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
)


def _plan(contexto, configuracion, relleno: str = "") -> str:
    etapas = []
    for numero in range(1, 9):
        etapas.append(
            f"""## E{numero}

Objetivo: comprobar la etapa {numero}.

Comprobaciones: realizar una comprobación reproducible.

Variables o grupos: se concretarán tras la inspección.

Evidencia esperada: resultado estructurado y trazable.

Supuestos o dependencias: no se asumen hallazgos previos.
"""
        )
    return f"""# Identificación

run_id: {contexto.run_id}

framework_id: {contexto.framework_id}

dataset_id: {contexto.dataset.dataset_id}

contract_version: {configuracion.datos["versions"]["contract"]}

prompt_version: {configuracion.datos["versions"]["prompts"]}

# Comprensión inicial

Se analizará una fila como unidad de observación y se comprobarán las incertidumbres.

# Preguntas analíticas

Se estudiarán la calidad, la distribución y las relaciones pertinentes.

# Plan por etapas

{"".join(etapas)}
# Visualizaciones previstas

Se generará una figura para resumir una distribución relevante.

# Supuestos y riesgos

Los tipos, ausencias y valores atípicos deberán comprobarse.

# Criterios de finalización

Los resultados deberán ser reproducibles, coherentes y estar referenciados. {relleno}
"""


def _informe() -> str:
    return """# Resumen ejecutivo

Se presenta un resultado descriptivo respaldado por evidencia [STAT-001].

# Dataset y alcance

El análisis se limita al dataset autorizado y a un EDA tabular.

# Inspección, calidad y preparación

Se conservó una muestra preparada trazable.

# Estadística descriptiva

El recuento utilizado se conserva en [STAT-001].

# Variables, agregaciones y relaciones

Se resume una variable sin establecer relaciones causales.

# Visualizaciones y hallazgos

La figura [FIG-001] está disponible en figures/fig_001_prueba.png.

# Problemas, riesgos y anomalías

Las comprobaciones realizadas no obligan a inventar incidencias.

# Limitaciones e incertidumbres

La muestra preparada de esta prueba no representa un análisis definitivo.

# Conclusiones

Los artefactos mantienen coherencia estructural y referencias resolubles.
"""


def _materializar_salidas_validas(contexto, configuracion, relleno_plan: str = "") -> None:
    raiz = contexto.directorio_salida
    raiz.joinpath("plan.md").write_text(
        _plan(contexto, configuracion, relleno_plan),
        encoding="utf-8",
    )
    raiz.joinpath("prepared_data.csv").write_text(
        "pedido_id,importe\nP001,10.5\nP002,20.0\n",
        encoding="utf-8",
    )
    estadisticas = {
        "schema_version": "1.0",
        "run_id": contexto.run_id,
        "dataset_id": contexto.dataset.dataset_id,
        "generated_at_utc": "2026-08-28T12:00:00Z",
        "profile": {
            "original_rows": contexto.dataset.filas_esperadas,
            "original_columns": contexto.dataset.columnas_esperadas,
            "prepared_rows": 2,
            "prepared_columns": 2,
            "unit_of_analysis": "Un pedido",
            "columns": [
                {
                    "name": "pedido_id",
                    "origin": "source",
                    "source_name": "pedido_id",
                    "original_type": "object",
                    "prepared_type": "str",
                    "missing_original": 0,
                    "missing_prepared": 0,
                    "unique_prepared": 2,
                },
                {
                    "name": "importe",
                    "origin": "source",
                    "source_name": "importe",
                    "original_type": "float64",
                    "prepared_type": "float64",
                    "missing_original": 0,
                    "missing_prepared": 0,
                    "unique_prepared": 2,
                },
            ],
        },
        "preparation": {
            "summary": "Se conserva una copia mínima para comprobar el esquema.",
            "changes": [
                {
                    "id": "TR-001",
                    "action": "selection",
                    "description": "Selección de dos filas para la prueba automática",
                    "justification": "Comprobar la coherencia estructural",
                    "affected_columns": ["pedido_id", "importe"],
                    "rows_affected": 2,
                    "before": None,
                    "after": {"rows": 2},
                }
            ],
        },
        "analyses": [
            {
                "id": "STAT-001",
                "stage": "E1",
                "analysis_type": "count",
                "title": "Filas preparadas",
                "variables": ["pedido_id"],
                "population": "Copia preparada de prueba",
                "method": "Recuento de filas",
                "result": {"rows": 2},
                "interpretation": "La copia contiene dos filas.",
            }
        ],
        "figures": [
            {
                "id": "FIG-001",
                "file": "figures/fig_001_prueba.png",
                "title": "Figura de prueba",
                "objective": "Comprobar el registro de una figura",
                "variables": ["importe"],
                "source_analysis_ids": ["STAT-001"],
            }
        ],
        "limitations": ["Artefactos generados solo para una prueba estructural"],
    }
    raiz.joinpath("statistics.json").write_text(
        json.dumps(estadisticas, ensure_ascii=False, indent=2, allow_nan=False),
        encoding="utf-8",
    )
    incidencias = {
        "schema_version": "1.0",
        "run_id": contexto.run_id,
        "dataset_id": contexto.dataset.dataset_id,
        "checks_performed": [
            {
                "id": "CHK-001",
                "category": "completeness",
                "description": "Comprobación de estructura",
                "outcome": "La estructura puede validarse",
                "evidence_ids": ["STAT-001"],
            }
        ],
        "issues": [],
    }
    raiz.joinpath("issues.json").write_text(
        json.dumps(incidencias, ensure_ascii=False, indent=2, allow_nan=False),
        encoding="utf-8",
    )
    contexto.directorio_figuras.joinpath("fig_001_prueba.png").write_bytes(PNG_UN_PIXEL)
    raiz.joinpath("report.md").write_text(_informe(), encoding="utf-8")


class PruebasValidacionSalidas(unittest.TestCase):
    def test_conjunto_completo_es_valido_y_completed(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            configuracion, contexto = _crear_contexto(Path(directorio), "salidas_validas")
            escritor = _crear_escritor(configuracion, contexto)
            _materializar_salidas_validas(contexto, configuracion)

            validacion = ValidadorSalidas(configuracion, contexto).validar("VAL-001")
            estado, motivo = determinar_estado_terminal(
                validacion,
                dataset_cargado=True,
                limites_alcanzados=(),
                flujo_roles_completo=True,
                decision_revision="approved",
            )

            self.assertEqual(validacion["validation_status"], "valid")
            self.assertEqual(validacion["error_count"], 0)
            self.assertEqual(estado, "completed")
            self.assertEqual(motivo, "ALL_OUTPUTS_VALID")
            _cerrar_ejecucion(escritor)

    def test_limite_con_resultados_evaluables_es_partial(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            configuracion, contexto = _crear_contexto(Path(directorio), "limite_partial")
            escritor = _crear_escritor(configuracion, contexto)
            _materializar_salidas_validas(contexto, configuracion)

            validacion = ValidadorSalidas(configuracion, contexto).validar("VAL-LIMIT")
            estado, motivo = determinar_estado_terminal(
                validacion,
                dataset_cargado=True,
                limites_alcanzados=("input_tokens:run",),
                flujo_roles_completo=False,
                decision_revision=None,
            )

            self.assertEqual(estado, "partial")
            self.assertEqual(motivo, "LIMIT_REACHED_WITH_EVALUABLE_OUTPUT")
            _cerrar_ejecucion(escritor)

    def test_sin_decision_del_revisor_es_partial(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            configuracion, contexto = _crear_contexto(Path(directorio), "sin_revision")
            escritor = _crear_escritor(configuracion, contexto)
            _materializar_salidas_validas(contexto, configuracion)

            validacion = ValidadorSalidas(configuracion, contexto).validar("VAL-REVIEW")
            estado, motivo = determinar_estado_terminal(
                validacion,
                dataset_cargado=True,
                limites_alcanzados=(),
                flujo_roles_completo=True,
                decision_revision=None,
            )

            self.assertEqual(estado, "partial")
            self.assertEqual(motivo, "REVIEW_DECISION_MISSING")
            _cerrar_ejecucion(escritor)

    def test_sin_plan_pero_con_minimo_evaluable_es_partial(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            configuracion, contexto = _crear_contexto(Path(directorio), "salidas_parciales")
            escritor = _crear_escritor(configuracion, contexto)
            _materializar_salidas_validas(contexto, configuracion)
            contexto.directorio_salida.joinpath("plan.md").unlink()

            validacion = ValidadorSalidas(configuracion, contexto).validar("VAL-002")
            estado, motivo = determinar_estado_terminal(
                validacion,
                dataset_cargado=True,
                limites_alcanzados=(),
                flujo_roles_completo=True,
                decision_revision="approved",
            )

            self.assertEqual(validacion["validation_status"], "incomplete")
            self.assertEqual(estado, "partial")
            self.assertEqual(motivo, "MINIMUM_EVALUABLE_OUTPUT_AVAILABLE")
            _cerrar_ejecucion(escritor)

    def test_sin_informe_es_failed_aunque_existan_otros_resultados(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            configuracion, contexto = _crear_contexto(Path(directorio), "salidas_fallidas")
            escritor = _crear_escritor(configuracion, contexto)
            _materializar_salidas_validas(contexto, configuracion)
            contexto.directorio_salida.joinpath("report.md").unlink()

            validacion = ValidadorSalidas(configuracion, contexto).validar("VAL-003")
            estado, motivo = determinar_estado_terminal(
                validacion,
                dataset_cargado=True,
                limites_alcanzados=(),
                flujo_roles_completo=True,
                decision_revision="approved",
            )

            self.assertEqual(estado, "failed")
            self.assertEqual(motivo, "REPORT_MISSING_OR_INVALID")
            _cerrar_ejecucion(escritor)

    def test_validacion_automatica_no_consume_llamada_de_herramienta(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            configuracion, contexto = _crear_contexto(Path(directorio), "validacion_automatica")
            escritor = _crear_escritor(configuracion, contexto)
            control = ControlLimites(configuracion, escritor)
            herramientas = HerramientasComunes(
                configuracion,
                contexto,
                escritor,
                control,
            )
            _materializar_salidas_validas(contexto, configuracion)

            respuesta = herramientas.validate_outputs(
                {},
                "runtime",
                trigger="pre_review",
                automatic=True,
            )

            self.assertEqual(respuesta["status"], "success")
            self.assertEqual(respuesta["data"]["validation_status"], "valid")
            self.assertEqual(control.tool_calls, 0)
            resultado = _cerrar_ejecucion(escritor)
            self.assertEqual(resultado.estado, "valid")
            self.assertEqual(resultado.eventos_por_tipo["validation_completed"], 1)


class PruebasLecturaSalidas(unittest.TestCase):
    def test_lectura_paginada_es_reproducible_y_trazada(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            configuracion, contexto = _crear_contexto(Path(directorio), "lectura_paginada")
            escritor = _crear_escritor(configuracion, contexto)
            control = ControlLimites(configuracion, escritor)
            herramientas = HerramientasComunes(
                configuracion,
                contexto,
                escritor,
                control,
            )
            _materializar_salidas_validas(
                contexto,
                configuracion,
                relleno_plan="X" * 70000,
            )
            primera = herramientas.read_output(
                {
                    "artifact": "plan",
                    "query": "full",
                    "selector": None,
                    "cursor": None,
                },
                "analyst_initial",
            )
            segunda = herramientas.read_output(
                {
                    "artifact": "plan",
                    "query": "next",
                    "selector": None,
                    "cursor": primera["data"]["next_cursor"],
                },
                "analyst_initial",
            )

            self.assertEqual(primera["status"], "success")
            self.assertTrue(primera["data"]["truncated"])
            self.assertIsNotNone(primera["data"]["next_cursor"])
            self.assertEqual(segunda["status"], "success")
            self.assertFalse(segunda["data"]["truncated"])
            original = contexto.directorio_salida.joinpath("plan.md").read_text(encoding="utf-8")
            reconstruido = primera["data"]["content"] + segunda["data"]["content"]
            self.assertEqual(reconstruido, original)
            self.assertEqual(control.tool_calls, 2)
            resultado = _cerrar_ejecucion(
                escritor,
                control.resumen(),
                list(control.limites_alcanzados),
            )
            self.assertEqual(resultado.estado, "valid")
            self.assertEqual(resultado.eventos_por_tipo["tool_call_started"], 2)
            self.assertEqual(resultado.eventos_por_tipo["tool_call_finished"], 2)


class PruebasMaterializacionYCierre(unittest.TestCase):
    def test_materializa_las_respuestas_y_cierra_completed(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            configuracion, contexto = _crear_contexto(Path(directorio), "cierre_completed")
            escritor = _crear_escritor(configuracion, contexto)
            control = ControlLimites(configuracion, escritor)
            herramientas = HerramientasComunes(
                configuracion,
                contexto,
                escritor,
                control,
            )
            _materializar_salidas_validas(contexto, configuracion)
            contexto.directorio_salida.joinpath("plan.md").unlink()
            contexto.directorio_salida.joinpath("report.md").unlink()

            materializar_markdown_rol(
                configuracion,
                contexto,
                escritor,
                "plan.md",
                _plan(contexto, configuracion),
                "planner",
                "initial",
                escritor.ultimo_evento_id,
            )
            materializar_markdown_rol(
                configuracion,
                contexto,
                escritor,
                "report.md",
                _informe(),
                "analyst",
                "initial",
                escritor.ultimo_evento_id,
            )
            cierre = cerrar_ejecucion_comun(
                herramientas,
                control,
                escritor,
                dataset_cargado=True,
                flujo_roles_completo=True,
                decision_revision="approved",
            )

            self.assertEqual(cierre.estado, "completed")
            self.assertEqual(cierre.motivo, "ALL_OUTPUTS_VALID")
            self.assertEqual(cierre.integridad_traza.estado, "valid")
            self.assertEqual(
                cierre.integridad_traza.eventos_por_tipo["artifact_written"],
                2,
            )

    def test_rechaza_un_informe_sin_estructura_y_conserva_la_respuesta(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            configuracion, contexto = _crear_contexto(Path(directorio), "informe_rechazado")
            escritor = _crear_escritor(configuracion, contexto)
            with self.assertRaises(ErrorMaterializacion):
                materializar_markdown_rol(
                    configuracion,
                    contexto,
                    escritor,
                    "report.md",
                    "Informe sin los encabezados obligatorios",
                    "analyst",
                    "initial",
                    escritor.ultimo_evento_id,
                )
            self.assertFalse(contexto.directorio_salida.joinpath("report.md").exists())
            self.assertTrue(
                contexto.directorio_temporal.joinpath("rejected_report_md.txt").is_file()
            )
            _cerrar_ejecucion(escritor)


if __name__ == "__main__":
    unittest.main()
