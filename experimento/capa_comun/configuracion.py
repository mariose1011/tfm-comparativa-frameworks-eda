"""Carga y validación de la configuración común del experimento."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

from .errores import ConfiguracionError
from .utilidades import cargar_json_sin_duplicados, resolver_ruta_relativa, sha256_bytes


FRAMEWORKS_ESPERADOS = {
    "langgraph",
    "crewai",
    "microsoft_agent_framework",
}
DATASETS_ESPERADOS = {
    "D0_piloto",
    "D1_bike_sharing",
    "D2_online_retail",
}
SALIDAS_ESPERADAS = {
    "plan.md",
    "prepared_data.csv",
    "statistics.json",
    "issues.json",
    "figures/",
    "report.md",
    "trace.jsonl",
}


def _congelar(valor: Any) -> Any:
    """Protege los datos cargados frente a modificaciones."""
    if isinstance(valor, dict):
        return MappingProxyType({clave: _congelar(contenido) for clave, contenido in valor.items()})
    if isinstance(valor, list):
        return tuple(_congelar(elemento) for elemento in valor)
    return valor


def _obtener(datos: Mapping[str, Any], ruta: str, tipo: type | tuple[type, ...]) -> Any:
    """Obtiene un campo de la configuración y comprueba su tipo."""
    actual: Any = datos
    for parte in ruta.split("."):
        if not isinstance(actual, Mapping) or parte not in actual:
            raise ConfiguracionError(f"Falta el campo obligatorio de configuración: {ruta}")
        actual = actual[parte]
    if not isinstance(actual, tipo):
        raise ConfiguracionError(f"El campo {ruta} tiene un tipo incorrecto")
    return actual


def _exigir_positivo(datos: Mapping[str, Any], ruta: str) -> int | float:
    """Comprueba que el campo contenga un número positivo."""
    valor = _obtener(datos, ruta, (int, float))
    if isinstance(valor, bool) or valor <= 0:
        raise ConfiguracionError(f"El campo {ruta} debe ser un número positivo")
    return valor


def _exigir_booleano(datos: Mapping[str, Any], ruta: str, esperado: bool) -> None:
    """Comprueba que el campo tenga el valor booleano exigido."""
    valor = _obtener(datos, ruta, bool)
    if valor is not esperado:
        raise ConfiguracionError(f"El campo {ruta} contradice el contrato")


def _descubrir_raiz(ruta_configuracion: Path) -> Path:
    """Localiza la raíz del proyecto desde la ubicación del JSON."""
    for candidata in (ruta_configuracion.parent, *ruta_configuracion.parents):
        if (candidata / "datasets" / "manifest.json").is_file() and (
            candidata / "experimento" / "contrato_comun_v1.0.md"
        ).is_file():
            return candidata.resolve()
    raise ConfiguracionError("No se ha podido localizar la raíz del TFM")


def _validar_rutas(datos: Mapping[str, Any], raiz: Path) -> None:
    """Valida que las rutas de los archivos estén correctamente definidas."""
    
    if _obtener(datos, "paths.base", str) != "workspace_root":
        raise ConfiguracionError("paths.base debe ser workspace_root")

    rutas_archivo = [
        _obtener(datos, "paths.contract_index", str),
        _obtener(datos, "paths.dataset_manifest", str),
        _obtener(datos, "paths.common_requirements", str),
        _obtener(datos, "paths.framework_requirements.langgraph", str),
        _obtener(datos, "paths.framework_requirements.crewai", str),
        _obtener(datos, "paths.framework_requirements.microsoft_agent_framework", str),
        _obtener(datos, "prompts.contract_source", str),
    ]
    for ruta_relativa in rutas_archivo:
        ruta = resolver_ruta_relativa(raiz, ruta_relativa)
        if not ruta.is_file():
            raise ConfiguracionError(f"No existe el archivo declarado: {ruta_relativa}")

    resolver_ruta_relativa(raiz, _obtener(datos, "paths.output_root", str))


def _validar_contrato_fijo(datos: Mapping[str, Any]) -> None:
    """Comprueba las condiciones comunes del contrato experimental."""
    if _obtener(datos, "config_version", str) != "1.0":
        raise ConfiguracionError("La campaña definitiva requiere config_version 1.0")
    if _obtener(datos, "status", str) != "frozen_for_definitive_runs":
        raise ConfiguracionError("La configuración 1.0 debe permanecer congelada")

    versiones = _obtener(datos, "versions", Mapping)
    versiones_esperadas = {
        "contract": "1.0",
        "prompts": "1.0",
        "tools": "1.0",
        "limits": "1.0",
        "output_schemas": "1.0",
        "trace_schema": "1.0",
    }
    for campo, version_esperada in versiones_esperadas.items():
        if _obtener(versiones, campo, str) != version_esperada:
            raise ConfiguracionError(
                f"versions.{campo} debe ser {version_esperada}"
            )

    frameworks = _obtener(datos, "frameworks.allowed", list)
    if len(frameworks) != len(set(frameworks)) or set(frameworks) != FRAMEWORKS_ESPERADOS:
        raise ConfiguracionError("La lista de frameworks no coincide con el contrato")

    datasets = _obtener(datos, "datasets.allowed_ids", list)
    if len(datasets) != len(set(datasets)) or set(datasets) != DATASETS_ESPERADOS:
        raise ConfiguracionError("La lista de datasets no coincide con el contrato")
    if _obtener(datos, "datasets.pilot_id", str) != "D0_piloto":
        raise ConfiguracionError("El piloto debe utilizar D0_piloto")
    if set(_obtener(datos, "datasets.definitive_ids", list)) != {
        "D1_bike_sharing",
        "D2_online_retail",
    }:
        raise ConfiguracionError("Los datasets definitivos no coinciden con el contrato")

    if _obtener(datos, "model.provider", str) != "openai":
        raise ConfiguracionError("El proveedor configurado debe ser OpenAI")
    if _obtener(datos, "model.api", str) != "responses":
        raise ConfiguracionError("La API configurada debe ser Responses")
    if _obtener(datos, "model.requested_model", str) != "gpt-5.6-terra":
        raise ConfiguracionError("El modelo configurado debe ser gpt-5.6-terra")

    booleanos_falsos = [
        "frameworks.native_memory_allowed",
        "frameworks.native_retries_allowed",
        "frameworks.model_fallback_allowed",
        "frameworks.dynamic_agent_creation_allowed",
        "model.pro_mode_enabled",
        "model.provider_builtin_tools_enabled",
        "security.manual_intervention_during_run_allowed",
        "security.record_credentials",
        "security.record_absolute_paths",
        "security.access_other_run_directories_allowed",
        "security.external_sources_allowed",
        "security.tools_network_allowed",
        "tools.parallel_execution_allowed",
        "tools.execute_python.network_allowed",
        "tools.execute_python.child_processes_allowed",
        "tools.execute_python.install_dependencies_during_run",
        "tools.validate_outputs.quality_scoring_allowed",
    ]
    for ruta in booleanos_falsos:
        _exigir_booleano(datos, ruta, False)

    booleanos_verdaderos = [
        "frameworks.clean_processes_per_run",
        "frameworks.fresh_output_directory_per_run",
        "datasets.validate_manifest_version",
        "datasets.validate_input_hash_before_run",
        "datasets.input_read_only",
        "datasets.public_documentation_only",
        "output_contract.paths_must_be_relative",
        "security.credentials_from_environment_only",
        "security.provider_connection_allowed_only_for_model_calls",
        "environment.same_machine_required",
        "environment.same_power_profile_required",
    ]
    for ruta in booleanos_verdaderos:
        _exigir_booleano(datos, ruta, True)

    parametros = _obtener(datos, "model.request_parameters", Mapping)
    valores_esperados = {
        "service_tier": "default",
        "tool_choice": "auto",
        "parallel_tool_calls": False,
        "truncation": "disabled",
        "background": False,
        "stream": False,
        "store": True,
    }
    for campo, esperado in valores_esperados.items():
        if parametros.get(campo) != esperado:
            raise ConfiguracionError(f"model.request_parameters.{campo} contradice el contrato")
    if _obtener(parametros, "reasoning.effort", str) != "medium":
        raise ConfiguracionError("El esfuerzo de razonamiento debe ser medium")
    if set(_obtener(datos, "model.omitted_parameters", list)) != {"temperature", "top_p"}:
        raise ConfiguracionError("temperature y top_p deben permanecer omitidos")

    herramientas_por_rol = {
        "planner": {"inspect_dataset"},
        "analyst_initial": {"execute_python", "read_output", "validate_outputs"},
        "reviewer": {"read_output", "validate_outputs"},
        "analyst_correction": {"execute_python", "read_output", "validate_outputs"},
    }
    for rol, esperadas in herramientas_por_rol.items():
        configuradas = set(_obtener(datos, f"roles.{rol}.exposed_tools", list))
        if configuradas != esperadas:
            raise ConfiguracionError(f"Las herramientas de {rol} no coinciden con el contrato")

    componentes_prompt = {
        "PROMPT-COMMON-1.0",
        "PROMPT-PLANNER-1.0",
        "PROMPT-ANALYST-1.0",
        "PROMPT-REVIEWER-1.0",
        "PROMPT-CORRECTION-1.0",
        "CONTEXT-SCHEMA-1.0",
    }
    if set(_obtener(datos, "prompts.component_ids", list)) != componentes_prompt:
        raise ConfiguracionError("Los componentes de prompts no coinciden con la Parte 6")

    if set(_obtener(datos, "output_contract.required_entries", list)) != SALIDAS_ESPERADAS:
        raise ConfiguracionError("Las salidas obligatorias no coinciden con el contrato")
    if _obtener(datos, "output_contract.missing_or_invalid_report_status", str) != "failed":
        raise ConfiguracionError("La ausencia de report.md debe producir el estado failed")


def _validar_limites(datos: Mapping[str, Any]) -> None:
    """Comprueba los límites contemplados y su coherencia entre sí."""
    aviso = _obtener(datos, "limits.warning_threshold_ratio", (int, float))
    if isinstance(aviso, bool) or not 0 < aviso < 1:
        raise ConfiguracionError("limits.warning_threshold_ratio debe estar entre cero y uno")

    rutas_positivas = [
        "limits.time_seconds.run",
        "limits.time_seconds.model_request",
        "limits.model_requests.run",
        "limits.tokens.request_input_estimate_max",
        "limits.tokens.request_output_max",
        "limits.tokens.run_input_max",
        "limits.tokens.run_output_max",
        "limits.tokens.run_total_max",
        "limits.tokens.minimum_run_output_remaining_for_new_request",
        "limits.model_requested_tool_calls.run",
        "limits.sizes.tool_text_response_max_characters",
        "limits.sizes.read_output_chunk_max_characters",
        "tools.execute_python.cumulative_time_max_seconds",
        "tools.execute_python.memory_max_bytes",
        "pricing.budgets.maximum_per_run",
    ]
    for ruta in rutas_positivas:
        _exigir_positivo(datos, ruta)

    entrada = _obtener(datos, "limits.tokens.run_input_max", int)
    salida = _obtener(datos, "limits.tokens.run_output_max", int)
    total = _obtener(datos, "limits.tokens.run_total_max", int)
    if entrada + salida != total:
        raise ConfiguracionError("El máximo total de tokens debe sumar entrada y salida")
    if _obtener(datos, "limits.tokens.request_output_max", int) > salida:
        raise ConfiguracionError("La salida por petición no puede superar la salida de la ejecución")
    if _obtener(datos, "limits.tokens.minimum_run_output_remaining_for_new_request", int) > salida:
        raise ConfiguracionError("La reserva mínima de salida supera el presupuesto de ejecución")

    peticiones_roles = _obtener(datos, "limits.model_requests.roles", Mapping)
    if set(peticiones_roles) != {"planner", "analyst_initial", "reviewer", "analyst_correction"}:
        raise ConfiguracionError("Los límites de peticiones no cubren exactamente los cuatro roles")
    for rol, valor in peticiones_roles.items():
        if not isinstance(valor, int) or isinstance(valor, bool) or valor <= 0:
            raise ConfiguracionError(f"El límite de peticiones de {rol} debe ser un entero positivo")
    if sum(peticiones_roles.values()) != _obtener(datos, "limits.model_requests.run", int):
        raise ConfiguracionError("Los máximos de peticiones por rol no coinciden con el máximo global")

    if _obtener(datos, "security.experiment_seed", int) != 20260808:
        raise ConfiguracionError("La semilla experimental no coincide con el contrato")
    if _obtener(datos, "tools.version", str) != _obtener(datos, "versions.tools", str):
        raise ConfiguracionError("La versión de herramientas no coincide con versions.tools")
    if _obtener(datos, "prompts.version", str) != _obtener(datos, "versions.prompts", str):
        raise ConfiguracionError("La versión de prompts no coincide con versions.prompts")


def _validar_ausencia_de_secretos(datos: Mapping[str, Any]) -> None:
    """Rechaza cadenas que comienzan por el prefijo de clave de API sk-."""
    def recorrer(valor: Any) -> None:
        if isinstance(valor, Mapping):
            for contenido in valor.values():
                recorrer(contenido)
        elif isinstance(valor, list):
            for contenido in valor:
                recorrer(contenido)
        elif isinstance(valor, str) and valor.startswith("sk-"):
            raise ConfiguracionError("La configuración no puede contener una clave de API")

    recorrer(datos)


@dataclass(frozen=True, slots=True)
class ConfiguracionExperimento:
    """Configuración validada, inmutable y asociada a su hash."""

    ruta: Path
    raiz_tfm: Path
    datos: Mapping[str, Any]
    sha256: str

    def resolver_ruta(self, ruta_relativa: str) -> Path:
        return resolver_ruta_relativa(self.raiz_tfm, ruta_relativa)


def cargar_configuracion(
    ruta: str | Path = "experimento/configuracion/configuracion_experimento_v1.0.json",
    raiz_tfm: str | Path | None = None,
) -> ConfiguracionExperimento:
    """Carga, valida y congela la configuración antes de una ejecución."""

    ruta_configuracion = Path(ruta).resolve()
    if not ruta_configuracion.is_file():
        raise ConfiguracionError(f"No existe la configuración: {ruta_configuracion.name}")

    raiz = Path(raiz_tfm).resolve() if raiz_tfm is not None else _descubrir_raiz(ruta_configuracion)
    try:
        ruta_relativa_configuracion = str(ruta_configuracion.relative_to(raiz))
    except ValueError as exc:
        raise ConfiguracionError("La configuración debe estar dentro de la raíz del TFM") from exc
    resolver_ruta_relativa(raiz, ruta_relativa_configuracion)

    datos, contenido = cargar_json_sin_duplicados(ruta_configuracion)
    _validar_rutas(datos, raiz)
    _validar_contrato_fijo(datos)
    _validar_limites(datos)
    _validar_ausencia_de_secretos(datos)

    return ConfiguracionExperimento(
        ruta=ruta_configuracion,
        raiz_tfm=raiz,
        datos=_congelar(datos),
        sha256=sha256_bytes(contenido),
    )
