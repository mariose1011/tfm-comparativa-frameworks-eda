"""Pruebas de la inspección determinista del dataset."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from experimento.capa_comun.herramientas import (
    ESQUEMA_INSPECT_DATASET,
    HerramientasComunes,
)
from experimento.capa_comun.limites import ControlLimites

from .test_traza_limites import (
    RAIZ_TFM,
    _cerrar_ejecucion,
    _crear_contexto,
    _crear_escritor,
)


class PruebasInspeccion(unittest.TestCase):
    def test_esquema_no_admite_parametros(self) -> None:
        parametros = ESQUEMA_INSPECT_DATASET["parameters"]
        self.assertEqual(parametros["properties"], {})
        self.assertFalse(parametros["additionalProperties"])
        self.assertTrue(ESQUEMA_INSPECT_DATASET["strict"])

    def test_inspeccion_d0_es_completa_determinista_y_cacheada(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            configuracion, contexto = _crear_contexto(Path(directorio), "inspeccion_d0")
            escritor = _crear_escritor(configuracion, contexto)
            control = ControlLimites(configuracion, escritor)
            herramientas = HerramientasComunes(
                configuracion,
                contexto,
                escritor,
                control,
            )

            respuesta = herramientas.inspect_dataset({}, "planner")
            reutilizada = herramientas.inspeccion_cacheada()
            repetida = herramientas.inspect_dataset({}, "planner")

            self.assertEqual(respuesta["status"], "success")
            self.assertEqual(respuesta, reutilizada)
            self.assertEqual(respuesta, repetida)
            self.assertEqual(control.tool_calls, 1)
            self.assertEqual(control.tool_successes, 1)
            datos = respuesta["data"]
            self.assertEqual(datos["dataset_id"], "D0_piloto")
            self.assertEqual(datos["rows"], 246)
            self.assertEqual(datos["columns"], 13)
            self.assertIsNone(datos["selected_sheet"])
            self.assertEqual(len(datos["column_profile"]), 13)
            self.assertEqual(len(datos["head_sample"]), 5)
            self.assertEqual(len(datos["tail_sample"]), 5)
            self.assertEqual(len(datos["random_sample"]), 10)
            self.assertEqual(len(datos["public_documentation"]), 1)
            self.assertEqual(datos["source_sha256"], contexto.dataset.sha256)

            resultado = _cerrar_ejecucion(
                escritor,
                control.resumen(),
                list(control.limites_alcanzados),
            )
            self.assertEqual(resultado.estado, "valid")
            self.assertEqual(resultado.eventos_por_tipo["tool_call_started"], 1)
            self.assertEqual(resultado.eventos_por_tipo["tool_call_finished"], 1)

    def test_rechaza_parametros_e_informa_el_error(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            configuracion, contexto = _crear_contexto(Path(directorio), "inspeccion_argumentos")
            escritor = _crear_escritor(configuracion, contexto)
            control = ControlLimites(configuracion, escritor)
            herramientas = HerramientasComunes(
                configuracion,
                contexto,
                escritor,
                control,
            )

            respuesta = herramientas.inspect_dataset(
                {"path": "otro_archivo.csv"},
                "planner",
            )

            self.assertEqual(respuesta["status"], "error")
            self.assertEqual(respuesta["error"]["code"], "INVALID_ARGUMENT")
            self.assertEqual(control.tool_calls, 1)
            resultado = _cerrar_ejecucion(
                escritor,
                control.resumen(),
                list(control.limites_alcanzados),
            )
            self.assertEqual(resultado.estado, "valid")
            self.assertEqual(resultado.eventos_por_tipo["tool_call_failed"], 1)
            eventos = [
                json.loads(linea)
                for linea in contexto.directorio_salida.joinpath(
                    "trace.jsonl"
                ).read_text(encoding="utf-8").splitlines()
            ]
            error = next(
                evento
                for evento in eventos
                if evento["event_type"] == "error_recorded"
            )
            self.assertEqual(error["payload"]["severity"], "recoverable")

    def test_inspecciona_los_datasets_definitivos_con_su_estructura_congelada(self) -> None:
        casos = (
            ("D1_bike_sharing", 17379, 17, None),
            ("D2_online_retail", 541909, 8, "Online Retail"),
        )
        for dataset_id, filas, columnas, hoja in casos:
            with self.subTest(dataset_id=dataset_id):
                with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
                    configuracion, contexto = _crear_contexto(
                        Path(directorio),
                        f"inspeccion_{dataset_id}",
                        dataset_id=dataset_id,
                    )
                    escritor = _crear_escritor(configuracion, contexto)
                    control = ControlLimites(configuracion, escritor)
                    herramientas = HerramientasComunes(
                        configuracion,
                        contexto,
                        escritor,
                        control,
                    )

                    respuesta = herramientas.inspect_dataset({}, "planner")

                    self.assertEqual(respuesta["status"], "success")
                    self.assertEqual(respuesta["data"]["rows"], filas)
                    self.assertEqual(respuesta["data"]["columns"], columnas)
                    self.assertEqual(respuesta["data"]["selected_sheet"], hoja)
                    self.assertLessEqual(
                        respuesta["duration_ms"],
                        configuracion.datos["limits"]["time_seconds"]["tools"][
                            "inspect_dataset"
                        ]
                        * 1000,
                    )
                    resultado = _cerrar_ejecucion(
                        escritor,
                        control.resumen(),
                        list(control.limites_alcanzados),
                    )
                    self.assertEqual(resultado.estado, "valid")

    def test_analista_no_puede_repetir_la_inspeccion(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            configuracion, contexto = _crear_contexto(Path(directorio), "inspeccion_denegada")
            escritor = _crear_escritor(configuracion, contexto)
            control = ControlLimites(configuracion, escritor)
            herramientas = HerramientasComunes(
                configuracion,
                contexto,
                escritor,
                control,
            )

            respuesta = herramientas.inspect_dataset({}, "analyst_initial")

            self.assertEqual(respuesta["status"], "error")
            self.assertEqual(respuesta["error"]["code"], "ACCESS_DENIED")
            self.assertEqual(control.tool_calls, 1)
            resultado = _cerrar_ejecucion(
                escritor,
                control.resumen(),
                list(control.limites_alcanzados),
            )
            self.assertEqual(resultado.estado, "valid")
            self.assertEqual(resultado.eventos_por_tipo["limit_reached"], 1)


if __name__ == "__main__":
    unittest.main()
