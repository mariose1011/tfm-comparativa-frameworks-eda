"""Comprobaciones y preparación de la capa común desde la consola."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .configuracion import cargar_configuracion
from .datasets import validar_datasets
from .ejecucion import preparar_ejecucion
from .errores import CapaComunError


CONFIGURACION_PREDETERMINADA = Path(
    "experimento/configuracion/configuracion_experimento_v1.0.json"
)


def _crear_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Capa común del experimento del TFM")
    parser.add_argument(
        "--config",
        type=Path,
        default=CONFIGURACION_PREDETERMINADA,
        help="Ruta al JSON de configuración",
    )
    subparsers = parser.add_subparsers(dest="comando", required=True)
    subparsers.add_parser("validar", help="Valida configuración, rutas, datasets y hashes")

    preparar = subparsers.add_parser("preparar", help="Prepara una carpeta de ejecución nueva")
    preparar.add_argument("--framework", required=True)
    preparar.add_argument("--dataset", required=True)
    preparar.add_argument("--repeticion", required=True, type=int)
    preparar.add_argument("--run-id")
    return parser


def main() -> int:
    argumentos = _crear_parser().parse_args()
    try:
        configuracion = cargar_configuracion(argumentos.config)
        if argumentos.comando == "validar":
            datasets = validar_datasets(configuracion)
            salida = {
                "status": "valid",
                "config_version": configuracion.datos["config_version"],
                "config_sha256": configuracion.sha256,
                "datasets": {
                    dataset_id: {
                        "format": dataset.formato,
                        "bytes": dataset.bytes,
                        "sha256": dataset.sha256,
                        "public_documentation_files": len(dataset.documentacion_publica),
                    }
                    for dataset_id, dataset in datasets.items()
                },
            }
        else:
            contexto = preparar_ejecucion(
                configuracion,
                argumentos.framework,
                argumentos.dataset,
                argumentos.repeticion,
                argumentos.run_id,
            )
            salida = {
                "status": "prepared",
                "run_id": contexto.run_id,
                "framework": contexto.framework_id,
                "dataset_id": contexto.dataset.dataset_id,
                "repetition": contexto.repeticion,
                "output_directory": str(
                    contexto.directorio_salida.relative_to(configuracion.raiz_tfm)
                ).replace("\\", "/"),
                "config_sha256": contexto.config_sha256,
            }
    except CapaComunError as exc:
        print(json.dumps({"status": "error", "message": str(exc)}, ensure_ascii=False))
        return 1

    print(json.dumps(salida, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
