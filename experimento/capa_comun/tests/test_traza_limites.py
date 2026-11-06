"""Pruebas de la traza común y de los límites cuantitativos."""

from __future__ import annotations

import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from experimento.capa_comun.configuracion import cargar_configuracion
from experimento.capa_comun.ejecucion import preparar_ejecucion
from experimento.capa_comun.errores import CapaComunError
from experimento.capa_comun.limites import ControlLimites
from experimento.capa_comun.traza import EscritorTraza, validar_archivo_traza


RAIZ_TFM = Path(__file__).resolve().parents[3]
RUTA_CONFIGURACION = (
    RAIZ_TFM / "experimento" / "configuracion" / "configuracion_experimento_v1.0.json"
)


def _crear_contexto(
    temporal: Path,
    sufijo: str,
    dataset_id: str = "D0_piloto",
    framework_id: str = "langgraph",
):
    datos = json.loads(RUTA_CONFIGURACION.read_text(encoding="utf-8"))
    salida = temporal / "resultados"
    datos["paths"]["output_root"] = salida.relative_to(RAIZ_TFM).as_posix()
    ruta_configuracion = temporal / f"config_{sufijo}.json"
    ruta_configuracion.write_text(
        json.dumps(datos, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    configuracion = cargar_configuracion(ruta_configuracion, RAIZ_TFM)
    contexto = preparar_ejecucion(
        configuracion,
        framework_id,
        dataset_id,
        1,
        run_id=f"{dataset_id}__{framework_id}__r01__{sufijo}",
    )
    return configuracion, contexto


def _crear_escritor(configuracion, contexto) -> EscritorTraza:
    hashes = {
        identificador: "A" * 64
        for identificador in configuracion.datos["prompts"]["component_ids"]
    }
    return EscritorTraza(
        contexto,
        configuracion,
        framework_version="prueba-1.0",
        dependencies={"dependencia_prueba": "1.0"},
        prompt_hashes=hashes,
    )


def _cerrar_ejecucion(
    escritor: EscritorTraza,
    totales: dict | None = None,
    limites: list[str] | None = None,
):
    ahora = escritor.started_at_utc
    escritor.registrar(
        "run_finished",
        "closure",
        "runtime",
        "common_runtime",
        {
            "final_status": "failed",
            "reason_code": "TEST_RUN",
            "reason": "Ejecución creada únicamente para una prueba automática",
            "started_at_utc": ahora,
            "finished_at_utc": ahora,
            "duration_ms": escritor.elapsed_ms(),
            "final_validation_id": None,
            "totals": totales or {
                "model_calls": 0,
                "turns": 0,
                "input_tokens": 0,
                "output_tokens": 0,
                "total_tokens": 0,
                "cached_input_tokens": 0,
                "reasoning_output_tokens": 0,
                "estimated_cost": {
                    "amount": 0.0,
                    "currency": "USD",
                    "pricing_table_id": "prueba",
                },
                "tool_calls": 0,
                "tool_successes": 0,
                "errors": 0,
                "retries": 0,
                "python_time_seconds": 0.0,
            },
            "correction_used": False,
            "correction_request_id": None,
            "limits_reached": limites or [],
            "artifacts": [],
        },
        parent_event_id=escritor.ultimo_evento_id,
    )
    return escritor.cerrar()


class PruebasTraza(unittest.TestCase):
    def test_traza_minima_cerrada_es_valida(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            configuracion, contexto = _crear_contexto(Path(directorio), "traza_valida")
            escritor = _crear_escritor(configuracion, contexto)
            resultado = _cerrar_ejecucion(escritor)

            self.assertEqual(resultado.estado, "valid")
            self.assertEqual(resultado.campos_ausentes_o_invalidos, 0)
            self.assertEqual(resultado.eventos_por_tipo["run_started"], 1)
            self.assertEqual(resultado.eventos_por_tipo["run_finished"], 1)
            self.assertEqual(resultado.eventos_por_tipo["trace_closed"], 1)

    def test_sanea_secretos_y_rutas_antes_de_escribir(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            configuracion, contexto = _crear_contexto(Path(directorio), "traza_saneada")
            escritor = _crear_escritor(configuracion, contexto)
            escritor.registrar(
                "state_transition",
                "planning",
                "planner",
                "framework_adapter",
                {
                    "from_state": "inicio",
                    "to_state": "planificacion",
                    "reason": "sk-1234567890ABC C:\\datos\\privados.csv",
                    "trigger_event_id": escritor.ultimo_evento_id,
                },
                parent_event_id=escritor.ultimo_evento_id,
            )
            resultado = _cerrar_ejecucion(escritor)
            contenido = contexto.directorio_salida.joinpath("trace.jsonl").read_text(
                encoding="utf-8"
            )

            self.assertEqual(resultado.estado, "valid")
            self.assertNotIn("sk-1234567890ABC", contenido)
            self.assertNotIn("C:\\datos\\privados.csv", contenido)
            self.assertIn("[REDACTED]", contenido)
            self.assertEqual(resultado.eventos_por_tipo["error_recorded"], 1)

    def test_no_confunde_enumeracion_escapada_con_ruta_windows(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            configuracion, contexto = _crear_contexto(
                Path(directorio),
                "traza_enumeracion",
            )
            escritor = _crear_escritor(configuracion, contexto)
            texto = r"Decisiones de preparación:\n\n1. Conservar los datos"
            escritor.registrar(
                "state_transition",
                "planning",
                "planner",
                "framework_adapter",
                {
                    "from_state": "inicio",
                    "to_state": "planificacion",
                    "reason": texto,
                    "trigger_event_id": escritor.ultimo_evento_id,
                },
                parent_event_id=escritor.ultimo_evento_id,
            )
            resultado = _cerrar_ejecucion(escritor)
            contenido = contexto.directorio_salida.joinpath("trace.jsonl").read_text(
                encoding="utf-8"
            )

            self.assertEqual(resultado.estado, "valid")
            self.assertNotIn("[REDACTED]", contenido)
            self.assertNotIn("error_recorded", contenido)

    def test_no_confunde_alias_python_con_ruta_windows(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            configuracion, contexto = _crear_contexto(
                Path(directorio),
                "traza_alias_python",
            )
            escritor = _crear_escritor(configuracion, contexto)
            texto = r"with open('statistics.json') as f:\n    stats = json.load(f)"
            escritor.registrar(
                "state_transition",
                "planning",
                "planner",
                "framework_adapter",
                {
                    "from_state": "inicio",
                    "to_state": "planificacion",
                    "reason": texto,
                    "trigger_event_id": escritor.ultimo_evento_id,
                },
                parent_event_id=escritor.ultimo_evento_id,
            )
            resultado = _cerrar_ejecucion(escritor)
            contenido = contexto.directorio_salida.joinpath("trace.jsonl").read_text(
                encoding="utf-8"
            )

            self.assertEqual(resultado.estado, "valid")
            self.assertIn(r"as f:\\n    stats", contenido)
            self.assertNotIn("[REDACTED]", contenido)
            self.assertNotIn("error_recorded", contenido)

    def test_detecta_una_secuencia_manipulada(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            configuracion, contexto = _crear_contexto(Path(directorio), "traza_alterada")
            escritor = _crear_escritor(configuracion, contexto)
            _cerrar_ejecucion(escritor)
            ruta = contexto.directorio_salida / "trace.jsonl"
            lineas = ruta.read_text(encoding="utf-8").splitlines()
            evento = json.loads(lineas[1])
            evento["sequence"] = 99
            lineas[1] = json.dumps(evento, ensure_ascii=False)
            ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")

            resultado = validar_archivo_traza(ruta)
            self.assertEqual(resultado.estado, "invalid")
            self.assertTrue(
                any("sequence" in fallo for fallo in resultado.comprobaciones_fallidas)
            )


class PruebasLimites(unittest.TestCase):
    def test_calcula_coste_y_contadores_comunes(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            configuracion, contexto = _crear_contexto(Path(directorio), "limites_coste")
            escritor = _crear_escritor(configuracion, contexto)
            control = ControlLimites(configuracion, escritor)

            autorizacion = control.autorizar_modelo(
                "planner",
                "planning",
                input_tokens_estimados=1000,
                output_tokens_solicitados=2000,
            )
            self.assertTrue(autorizacion.autorizada)
            self.assertEqual(autorizacion.max_output_tokens, 2000)
            control.registrar_modelo_iniciado("planner", "planning")
            coste = control.registrar_uso_modelo(
                input_tokens=1000,
                output_tokens=500,
                total_tokens=1500,
                cached_input_tokens=100,
                reasoning_output_tokens=100,
                fase="planning",
                rol="planner",
            )

            self.assertEqual(coste, Decimal("0.00782"))
            self.assertEqual(control.resumen()["total_tokens"], 1500)
            self.assertEqual(control.resumen()["model_calls"], 1)
            resultado = _cerrar_ejecucion(
                escritor,
                control.resumen(),
                list(control.limites_alcanzados),
            )
            self.assertEqual(resultado.estado, "valid")

    def test_bloquea_la_segunda_inspeccion_solicitada_por_el_planificador(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            configuracion, contexto = _crear_contexto(Path(directorio), "limite_herramienta")
            escritor = _crear_escritor(configuracion, contexto)
            control = ControlLimites(configuracion, escritor)

            self.assertTrue(
                control.autorizar_herramienta(
                    "planner",
                    "inspect_dataset",
                    "planning",
                )
            )
            control.registrar_herramienta_iniciada(
                "planner",
                "inspect_dataset",
                "planning",
            )
            self.assertFalse(
                control.autorizar_herramienta(
                    "planner",
                    "inspect_dataset",
                    "planning",
                )
            )
            resultado = _cerrar_ejecucion(
                escritor,
                control.resumen(),
                list(control.limites_alcanzados),
            )
            self.assertEqual(resultado.estado, "valid")
            self.assertEqual(resultado.eventos_por_tipo["limit_reached"], 1)

    def test_rechaza_un_total_de_tokens_incoherente(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            configuracion, contexto = _crear_contexto(Path(directorio), "tokens_invalidos")
            escritor = _crear_escritor(configuracion, contexto)
            control = ControlLimites(configuracion, escritor)
            with self.assertRaises(CapaComunError):
                control.registrar_uso_modelo(
                    input_tokens=100,
                    output_tokens=50,
                    total_tokens=100,
                    cached_input_tokens=0,
                    reasoning_output_tokens=0,
                    fase="planning",
                    rol="planner",
                )
            _cerrar_ejecucion(escritor)


if __name__ == "__main__":
    unittest.main()
