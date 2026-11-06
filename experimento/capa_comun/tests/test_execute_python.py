"""Pruebas del proceso aislado utilizado por execute_python."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from experimento.capa_comun.herramientas import HerramientasComunes
from experimento.capa_comun.limites import ControlLimites

from .test_traza_limites import (
    RAIZ_TFM,
    _cerrar_ejecucion,
    _crear_contexto,
    _crear_escritor,
)


class PruebasExecutePython(unittest.TestCase):
    def _preparar(self, directorio: str, sufijo: str):
        configuracion, contexto = _crear_contexto(Path(directorio), sufijo)
        escritor = _crear_escritor(configuracion, contexto)
        self.addCleanup(escritor.abandonar)
        control = ControlLimites(configuracion, escritor)
        herramientas = HerramientasComunes(
            configuracion,
            contexto,
            escritor,
            control,
        )
        return configuracion, contexto, escritor, control, herramientas

    def test_ejecuta_en_proceso_limpio_y_registra_el_archivo_creado(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            _, contexto, escritor, control, herramientas = self._preparar(
                directorio,
                "python_exito",
            )
            codigo = """tabla = pd.read_csv(INPUT_PATH)
tabla.head(3).to_csv(f"{OUTPUT_DIR}/prepared_data.csv", index=False)
resumen = scipy.stats.describe(tabla["net_amount_eur"])
sns.histplot(data=tabla, x="net_amount_eur")
plt.title("Distribución de importe neto")
plt.savefig(f"{FIGURES_DIR}/fig_001_importe.png")
plt.close()
print(f"filas={len(tabla)}")
print(f"media={resumen.mean:.4f}")
"""
            respuesta = herramientas.execute_python(
                {
                    "purpose": "Cargar D0 y crear una copia preparada mínima",
                    "code": codigo,
                },
                "analyst_initial",
            )

            self.assertEqual(respuesta["status"], "success", msg=repr(respuesta))
            self.assertEqual(respuesta["data"]["exit_status"], "success")
            self.assertIn("filas=246", respuesta["data"]["stdout"])
            self.assertTrue(
                contexto.directorio_salida.joinpath("prepared_data.csv").is_file()
            )
            self.assertEqual(
                {archivo["path"] for archivo in respuesta["data"]["files_created"]},
                {"prepared_data.csv", "figures/fig_001_importe.png"},
            )
            self.assertEqual(control.tool_calls, 1)
            self.assertEqual(control.tool_successes, 1)
            self.assertGreater(control.python_time_seconds, 0)
            resultado = _cerrar_ejecucion(
                escritor,
                control.resumen(),
                list(control.limites_alcanzados),
            )
            self.assertEqual(resultado.estado, "valid")
            self.assertEqual(resultado.eventos_por_tipo["artifact_written"], 2)

    def test_rechaza_importaciones_de_sistema_sin_iniciar_otro_proceso(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            _, _, escritor, control, herramientas = self._preparar(
                directorio,
                "python_import_denegado",
            )
            respuesta = herramientas.execute_python(
                {
                    "purpose": "Intento no autorizado",
                    "code": "import os\nprint(os.environ)",
                },
                "analyst_initial",
            )

            self.assertEqual(respuesta["status"], "error")
            self.assertEqual(
                respuesta["error"]["code"],
                "ACCESS_DENIED",
                msg=repr(respuesta),
            )
            self.assertEqual(control.tool_calls, 1)
            self.assertEqual(control.tool_successes, 0)
            self.assertEqual(control.python_time_seconds, 0)
            resultado = _cerrar_ejecucion(
                escritor,
                control.resumen(),
                list(control.limites_alcanzados),
            )
            self.assertEqual(resultado.estado, "valid")
            self.assertEqual(resultado.eventos_por_tipo["tool_call_failed"], 1)

    def test_bloquea_la_escritura_de_report_md(self) -> None:
        with tempfile.TemporaryDirectory(dir=RAIZ_TFM) as directorio:
            _, contexto, escritor, control, herramientas = self._preparar(
                directorio,
                "python_report_protegido",
            )
            respuesta = herramientas.execute_python(
                {
                    "purpose": "Intento de escritura no autorizado",
                    "code": (
                        "with open(f'{OUTPUT_DIR}/report.md', 'w', encoding='utf-8') as archivo:\n"
                        "    archivo.write('contenido no autorizado')\n"
                    ),
                },
                "analyst_initial",
            )

            self.assertEqual(respuesta["status"], "error")
            self.assertEqual(respuesta["data"]["exit_status"], "error")
            self.assertEqual(
                respuesta["error"]["code"],
                "ACCESS_DENIED",
                msg=repr(respuesta),
            )
            self.assertFalse(contexto.directorio_salida.joinpath("report.md").exists())
            resultado = _cerrar_ejecucion(
                escritor,
                control.resumen(),
                list(control.limites_alcanzados),
            )
            self.assertEqual(resultado.estado, "valid")


if __name__ == "__main__":
    unittest.main()
