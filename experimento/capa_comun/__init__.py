"""Capa de ejecución compartida por los tres frameworks."""

from .configuracion import ConfiguracionExperimento, cargar_configuracion
from .artefactos import (
    ArtefactoMaterializado,
    ErrorMaterializacion,
    materializar_markdown_rol,
)
from .cierre import ResultadoCierre, cerrar_ejecucion_comun
from .datasets import DatasetValidado, validar_datasets
from .ejecucion import ContextoEjecucion, crear_run_id, preparar_ejecucion
from .herramientas import (
    ESQUEMA_EXECUTE_PYTHON,
    ESQUEMA_INSPECT_DATASET,
    ESQUEMA_READ_OUTPUT,
    ESQUEMA_VALIDATE_OUTPUTS,
    HerramientasComunes,
)
from .limites import AutorizacionModelo, ControlLimites
from .prompts import (
    ErrorPrompt,
    PlantillasPrompts,
    PromptConstruido,
    RespuestaCorreccion,
    cargar_documentacion_publica,
    cargar_plantillas_prompts,
    construir_prompt_reparacion_formato,
    construir_prompt_rol,
    interpretar_decision_revisor,
    interpretar_respuesta_correccion,
)
from .traza import EscritorTraza, ResultadoIntegridad, validar_archivo_traza
from .validacion import ValidadorSalidas, determinar_estado_terminal
from .errores import (
    CapaComunError,
    ConfiguracionError,
    EjecucionError,
    HashNoCoincideError,
    ManifiestoError,
    RutaNoAutorizadaError,
)

__all__ = [
    "CapaComunError",
    "AutorizacionModelo",
    "ArtefactoMaterializado",
    "ConfiguracionError",
    "ConfiguracionExperimento",
    "ContextoEjecucion",
    "ControlLimites",
    "DatasetValidado",
    "EjecucionError",
    "ErrorMaterializacion",
    "ErrorPrompt",
    "ESQUEMA_EXECUTE_PYTHON",
    "ESQUEMA_INSPECT_DATASET",
    "ESQUEMA_READ_OUTPUT",
    "ESQUEMA_VALIDATE_OUTPUTS",
    "EscritorTraza",
    "HashNoCoincideError",
    "HerramientasComunes",
    "ManifiestoError",
    "PlantillasPrompts",
    "PromptConstruido",
    "RutaNoAutorizadaError",
    "ResultadoIntegridad",
    "ResultadoCierre",
    "RespuestaCorreccion",
    "ValidadorSalidas",
    "cargar_configuracion",
    "cargar_documentacion_publica",
    "cargar_plantillas_prompts",
    "cerrar_ejecucion_comun",
    "crear_run_id",
    "construir_prompt_reparacion_formato",
    "construir_prompt_rol",
    "determinar_estado_terminal",
    "materializar_markdown_rol",
    "interpretar_decision_revisor",
    "interpretar_respuesta_correccion",
    "preparar_ejecucion",
    "validar_archivo_traza",
    "validar_datasets",
]
