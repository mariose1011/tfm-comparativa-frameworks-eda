"""Punto de entrada del adaptador experimental de CrewAI."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from importlib.metadata import version
from pathlib import Path

from dotenv import load_dotenv

from experimento.capa_comun import (
    ControlLimites,
    EscritorTraza,
    HerramientasComunes,
    cargar_configuracion,
    cargar_documentacion_publica,
    cargar_plantillas_prompts,
    preparar_ejecucion,
)

from .modelo import FabricaModeloCrewAI, FabricaOpenAICrewAI
from .sesion import ResultadoAdaptadorCrewAI, SesionCrewAI


RAIZ_TFM = Path(__file__).resolve().parents[2]
CONFIGURACION_PREDETERMINADA = (
    RAIZ_TFM / "experimento" / "configuracion" / "configuracion_experimento_v1.0.json"
)
ARCHIVO_ENV = RAIZ_TFM / "frameworks" / "framework_keys.env"

__all__ = [
    "FabricaModeloCrewAI",
    "FabricaOpenAICrewAI",
    "ResultadoAdaptadorCrewAI",
    "SesionCrewAI",
    "ejecutar_experimento",
]


def ejecutar_experimento(
    dataset_id: str,
    repeticion: int,
    ruta_configuracion: Path = CONFIGURACION_PREDETERMINADA,
    run_id: str | None = None,
    fabrica_modelo: FabricaModeloCrewAI | None = None,
) -> ResultadoAdaptadorCrewAI:
    """Prepara y ejecuta una secuencia nativa de agentes y tareas CrewAI."""

    configuracion = cargar_configuracion(ruta_configuracion, RAIZ_TFM)
    fabrica = fabrica_modelo or FabricaOpenAICrewAI(configuracion)
    contexto = preparar_ejecucion(
        configuracion,
        "crewai",
        dataset_id,
        repeticion,
        run_id=run_id,
    )
    plantillas = cargar_plantillas_prompts(configuracion)
    documentacion = cargar_documentacion_publica(configuracion, contexto)
    dependencias = {
        paquete: version(paquete)
        for paquete in (
            "crewai",
            "crewai-core",
            "openai",
            "pydantic",
        )
    }
    traza = EscritorTraza(
        contexto,
        configuracion,
        framework_version=dependencias["crewai"],
        dependencies=dependencias,
        prompt_hashes=plantillas.hashes,
    )
    limites = ControlLimites(configuracion, traza)
    herramientas = HerramientasComunes(
        configuracion,
        contexto,
        traza,
        limites,
    )
    sesion = SesionCrewAI(
        configuracion,
        contexto,
        fabrica,
        traza,
        limites,
        herramientas,
        plantillas,
        documentacion,
    )
    return sesion.ejecutar()


def main() -> int:
    """Ejecuta el adaptador desde PowerShell."""

    parser = argparse.ArgumentParser(description="Ejecución experimental de CrewAI")
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--repeticion", type=int, required=True)
    parser.add_argument("--config", type=Path, default=CONFIGURACION_PREDETERMINADA)
    parser.add_argument("--run-id")
    argumentos = parser.parse_args()
    if ARCHIVO_ENV.is_file():
        load_dotenv(ARCHIVO_ENV, override=False)
    resultado = ejecutar_experimento(
        argumentos.dataset,
        argumentos.repeticion,
        argumentos.config,
        argumentos.run_id,
    )
    print(json.dumps(asdict(resultado), ensure_ascii=False, indent=2))
    return 0 if resultado.final_status in {"completed", "partial"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
