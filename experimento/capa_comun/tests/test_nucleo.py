"""Pruebas del núcleo inicial compartido."""

from __future__ import annotations

import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from experimento.capa_comun.configuracion import cargar_configuracion
from experimento.capa_comun.datasets import validar_datasets
from experimento.capa_comun.ejecucion import crear_run_id, preparar_ejecucion
from experimento.capa_comun.errores import (
    ConfiguracionError,
    EjecucionError,
    RutaNoAutorizadaError,
)
from experimento.capa_comun.herramientas import ESQUEMA_EXECUTE_PYTHON
from experimento.capa_comun.prompts import (
    cargar_documentacion_publica,
    cargar_plantillas_prompts,
    construir_prompt_rol,
)
from experimento.capa_comun.utilidades import resolver_ruta_relativa, sha256_archivo


RAIZ_TFM = Path(__file__).resolve().parents[3]
RUTA_CONFIGURACION = (
    RAIZ_TFM / "experimento" / "configuracion" / "configuracion_experimento_v1.0.json"
)


class PruebasConfiguracion(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.configuracion = cargar_configuracion(RUTA_CONFIGURACION, RAIZ_TFM)

    def test_configuracion_real_es_valida(self) -> None:
        self.assertEqual(self.configuracion.datos["config_version"], "1.0")
        self.assertEqual(self.configuracion.datos["model"]["requested_model"], "gpt-5.6-terra")
        self.assertEqual(self.configuracion.datos["versions"]["tools"], "1.0")
        self.assertEqual(self.configuracion.datos["versions"]["limits"], "1.0")
        self.assertEqual(self.configuracion.datos["tools"]["version"], "1.0")
        self.assertEqual(
            self.configuracion.datos["limits"]["tokens"]["run_input_max"],
            720000,
        )
        self.assertIs(
            self.configuracion.datos["model"]["request_parameters"]["store"],
            True,
        )
        self.assertEqual(len(self.configuracion.sha256), 64)

    def test_configuracion_es_inmutable(self) -> None:
        with self.assertRaises(TypeError):
            self.configuracion.datos["config_version"] = "otra"

    def test_datasets_y_documentacion_coinciden_con_manifest(self) -> None:
        datasets = validar_datasets(self.configuracion)
        self.assertEqual(
            set(datasets),
            {"D0_piloto", "D1_bike_sharing", "D2_online_retail"},
        )
        self.assertEqual(datasets["D0_piloto"].formato, "csv")
        self.assertEqual(datasets["D1_bike_sharing"].formato, "csv")
        self.assertEqual(datasets["D2_online_retail"].formato, "xlsx")
        self.assertIsNone(datasets["D0_piloto"].hoja_seleccionada)
        self.assertEqual(datasets["D2_online_retail"].hoja_seleccionada, "Online Retail")
        self.assertTrue(all(dataset.documentacion_publica for dataset in datasets.values()))

    def test_hash_de_configuracion_coincide_con_archivo(self) -> None:
        self.assertEqual(self.configuracion.sha256, sha256_archivo(RUTA_CONFIGURACION))

    def test_se_rechaza_activar_reintentos_nativos(self) -> None:
        datos = json.loads(RUTA_CONFIGURACION.read_text(encoding="utf-8"))
        datos["frameworks"]["native_retries_allowed"] = True
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as temporal:
            ruta_temporal = Path(temporal) / "config_invalida.json"
            ruta_temporal.write_text(
                json.dumps(datos, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            with self.assertRaises(ConfiguracionError):
                cargar_configuracion(ruta_temporal, RAIZ_TFM)

    def test_se_rechaza_desactivar_el_almacenamiento_en_openai(self) -> None:
        datos = json.loads(RUTA_CONFIGURACION.read_text(encoding="utf-8"))
        datos["model"]["request_parameters"]["store"] = False
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as temporal:
            ruta_temporal = Path(temporal) / "config_store_invalida.json"
            ruta_temporal.write_text(
                json.dumps(datos, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            with self.assertRaises(ConfiguracionError):
                cargar_configuracion(ruta_temporal, RAIZ_TFM)


class PruebasRutasYEjecucion(unittest.TestCase):
    def test_ruta_fuera_de_la_raiz_es_rechazada(self) -> None:
        with tempfile.TemporaryDirectory() as temporal:
            with self.assertRaises(RutaNoAutorizadaError):
                resolver_ruta_relativa(Path(temporal), "../fuera.txt")

    def test_run_id_es_reproducible_con_instante_fijo(self) -> None:
        instante = datetime(2026, 8, 28, 10, 30, 45, 123456, tzinfo=timezone.utc)
        run_id = crear_run_id("langgraph", "D0_piloto", 1, instante)
        self.assertEqual(
            run_id,
            "D0_piloto__langgraph__r01__20260828T103045123456Z",
        )

    def test_preparacion_publica_crea_solo_directorios_permitidos(self) -> None:
        datos = json.loads(RUTA_CONFIGURACION.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as temporal:
            raiz_temporal = Path(temporal)
            salida_relativa = raiz_temporal.relative_to(RAIZ_TFM) / "resultados"
            datos["paths"]["output_root"] = salida_relativa.as_posix()
            ruta_temporal = raiz_temporal / "config_prueba.json"
            ruta_temporal.write_text(
                json.dumps(datos, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            configuracion = cargar_configuracion(ruta_temporal, RAIZ_TFM)
            contexto = preparar_ejecucion(
                configuracion,
                "langgraph",
                "D0_piloto",
                1,
                run_id="D0_piloto__langgraph__r01__prueba",
            )
            self.assertTrue(contexto.directorio_salida.is_dir())
            self.assertTrue(contexto.directorio_temporal.is_dir())
            self.assertTrue(contexto.directorio_figuras.is_dir())
            archivos = [ruta for ruta in contexto.directorio_salida.iterdir() if ruta.is_file()]
            self.assertEqual(archivos, [])
            with self.assertRaises(EjecucionError):
                preparar_ejecucion(
                    configuracion,
                    "langgraph",
                    "D0_piloto",
                    1,
                    run_id="D0_piloto__langgraph__r01__prueba",
                )


class PruebasPrompts(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.configuracion = cargar_configuracion(RUTA_CONFIGURACION, RAIZ_TFM)
        cls.plantillas = cargar_plantillas_prompts(cls.configuracion)

    def test_componentes_y_hashes_coinciden_con_la_configuracion(self) -> None:
        self.assertEqual(
            set(self.plantillas.hashes),
            set(self.configuracion.datos["prompts"]["component_ids"]),
        )
        self.assertTrue(
            all(len(valor) == 64 for valor in self.plantillas.hashes.values())
        )

    def test_prompt_del_planificador_resuelve_todas_las_variables(self) -> None:
        datos = json.loads(RUTA_CONFIGURACION.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as temporal:
            raiz_temporal = Path(temporal)
            datos["paths"]["output_root"] = (
                raiz_temporal.relative_to(RAIZ_TFM) / "resultados"
            ).as_posix()
            ruta = raiz_temporal / "config_prompt.json"
            ruta.write_text(json.dumps(datos, ensure_ascii=False), encoding="utf-8")
            configuracion = cargar_configuracion(ruta, RAIZ_TFM)
            contexto = preparar_ejecucion(
                configuracion,
                "langgraph",
                "D0_piloto",
                1,
                run_id="D0_piloto__langgraph__r01__prompt",
            )
            prompt = construir_prompt_rol(
                self.plantillas,
                configuracion,
                contexto,
                "planner",
                cargar_documentacion_publica(configuracion, contexto),
            )
            self.assertNotIn("{{", prompt.instruccion_sistema)
            self.assertNotIn("{{", prompt.contenido_usuario)
            self.assertIn("framework_id: langgraph", prompt.contenido_usuario)
            self.assertIn("inspect_dataset({})", prompt.contenido_usuario)
            self.assertEqual(len(prompt.sha256), 64)


class PruebasEsquemasHerramientas(unittest.TestCase):
    def test_execute_python_explica_el_entorno_real_al_modelo(self) -> None:
        texto = " ".join(
            (
                ESQUEMA_EXECUTE_PYTHON["description"],
                ESQUEMA_EXECUTE_PYTHON["parameters"]["properties"]["purpose"]["description"],
                ESQUEMA_EXECUTE_PYTHON["parameters"]["properties"]["code"]["description"],
            )
        )
        nombres_obligatorios = {
            "INPUT_PATH",
            "OUTPUT_DIR",
            "FIGURES_DIR",
            "RUN_ID",
            "DATASET_ID",
            "EXPERIMENT_SEED",
            "pd",
            "np",
            "scipy",
            "plt",
            "sns",
            "openpyxl",
        }
        for nombre in nombres_obligatorios:
            self.assertIn(nombre, texto)
        for nombre_bloqueado in ("os", "pathlib", "glob", "globals", "locals", "vars"):
            self.assertIn(nombre_bloqueado, texto)


if __name__ == "__main__":
    unittest.main()
