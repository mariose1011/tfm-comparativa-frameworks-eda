"""Preparación de los mensajes de los roles y comprobación de sus respuestas."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

from .configuracion import ConfiguracionExperimento
from .ejecucion import ContextoEjecucion
from .errores import CapaComunError


VARIABLE = re.compile(r"\{\{([A-Z][A-Z0-9_]*)\}\}")
ENCABEZADO_H2 = re.compile(r"(?m)^## (\d+)\. .+$")
CATEGORIAS_REVISION = {
    "stage_coverage",
    "artifact",
    "schema",
    "traceability",
    "numeric_consistency",
    "preparation",
    "visualization_metadata",
    "interpretation",
    "causality",
    "limitations",
    "other",
}
ARTEFACTOS_CORREGIBLES = {
    "prepared_data.csv",
    "statistics.json",
    "issues.json",
    "report.md",
    "figures/",
}
ROLES = {
    "planner": "Planificador",
    "analyst_initial": "Analista",
    "reviewer": "Revisor",
    "analyst_correction": "Analista",
}
IDS_PROMPT = {
    "common": "PROMPT-COMMON-1.0",
    "planner": "PROMPT-PLANNER-1.0",
    "analyst_initial": "PROMPT-ANALYST-1.0",
    "reviewer": "PROMPT-REVIEWER-1.0",
    "analyst_correction": "PROMPT-CORRECTION-1.0",
    "context": "CONTEXT-SCHEMA-1.0",
}


class ErrorPrompt(CapaComunError):
    """El prompt o la respuesta de un rol no respeta el contrato."""


@dataclass(frozen=True, slots=True)
class PromptConstruido:
    rol: str
    instruccion_sistema: str
    contenido_usuario: str
    sha256: str


@dataclass(frozen=True, slots=True)
class RespuestaCorreccion:
    resumen: Mapping[str, Any]
    informe: str


@dataclass(frozen=True, slots=True)
class PlantillasPrompts:
    instruccion_comun: str
    contexto_comun: str
    instrucciones_roles: Mapping[str, str]
    objetivo_comun: str
    contrato_etapas: str
    contrato_salidas: str
    hashes: Mapping[str, str]


def _normalizar(texto: str) -> str:
    """Unifica los saltos de línea y elimina espacios de los extremos."""
    return texto.replace("\r\n", "\n").replace("\r", "\n").strip()


def _hash_texto(texto: str) -> str:
    """Calcula el hash SHA-256 de un texto."""
    return sha256(texto.encode("utf-8")).hexdigest().upper()


def _leer(ruta: Path) -> str:
    """Lee un documento UTF-8 y normaliza su texto."""
    try:
        return _normalizar(ruta.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ErrorPrompt(f"No puede leerse el documento de prompts: {ruta.name}") from exc


def _seccion_h2(texto: str, numero: int, incluir_encabezado: bool = False) -> str:
    """Extrae un apartado numerado del documento."""
    coincidencias = list(ENCABEZADO_H2.finditer(texto))
    for indice, coincidencia in enumerate(coincidencias):
        if int(coincidencia.group(1)) != numero:
            continue
        inicio = coincidencia.start() if incluir_encabezado else coincidencia.end()
        fin = coincidencias[indice + 1].start() if indice + 1 < len(coincidencias) else len(texto)
        return _normalizar(texto[inicio:fin])
    raise ErrorPrompt(f"No se encuentra la sección {numero} del contrato")


def _rango_h2(texto: str, primero: int, ultimo: int) -> str:
    """Extrae varios apartados numerados consecutivos."""
    return "\n\n".join(
        _seccion_h2(texto, numero, incluir_encabezado=True)
        for numero in range(primero, ultimo + 1)
    )


def _primer_bloque_codigo(seccion: str) -> str:
    """Extrae el primer bloque de código de una sección."""
    coincidencia = re.search(r"```(?:text|json)?\n(.*?)\n```", seccion, flags=re.DOTALL)
    if not coincidencia:
        raise ErrorPrompt("Falta un bloque ejecutable en el documento de prompts")
    return _normalizar(coincidencia.group(1))


def _subseccion_formato(seccion: str, numero: int) -> str:
    """Extrae los requisitos del formato de respuesta de un rol."""
    patron = re.compile(rf"(?m)^### {numero}\.2\. .+$")
    coincidencia = patron.search(seccion)
    if not coincidencia:
        raise ErrorPrompt(f"Falta el formato de salida de la sección {numero}")
    return _normalizar(seccion[coincidencia.end():])


def _plantilla_rol(texto_prompts: str, numero: int) -> str:
    """Combina las instrucciones del rol con su formato de respuesta."""
    seccion = _seccion_h2(texto_prompts, numero)
    instruccion = _primer_bloque_codigo(seccion)
    formato = _subseccion_formato(seccion, numero)
    return f"{instruccion}\n\n[OUTPUT_FORMAT]\n{formato}\n[/OUTPUT_FORMAT]"


def cargar_plantillas_prompts(
    configuracion: ConfiguracionExperimento,
) -> PlantillasPrompts:
    """Carga las instrucciones del contrato y calcula los hashes de sus componentes."""

    ruta_prompts = configuracion.resolver_ruta(
        configuracion.datos["prompts"]["contract_source"]
    )
    carpeta_contrato = ruta_prompts.parent
    texto_prompts = _leer(ruta_prompts)
    texto_alcance = _leer(carpeta_contrato / "01_alcance_entradas_y_etapas.md")
    texto_salidas = _leer(carpeta_contrato / "03_archivos_y_esquemas.md")

    instruccion_comun = _primer_bloque_codigo(_seccion_h2(texto_prompts, 55))
    contexto_comun = _primer_bloque_codigo(_seccion_h2(texto_prompts, 56))
    instrucciones = {
        "planner": _plantilla_rol(texto_prompts, 57),
        "analyst_initial": _plantilla_rol(texto_prompts, 58),
        "reviewer": _plantilla_rol(texto_prompts, 59),
        "analyst_correction": _plantilla_rol(texto_prompts, 60),
    }
    objetivo = _seccion_h2(texto_alcance, 5)
    etapas = _rango_h2(texto_alcance, 6, 7)
    salidas = _rango_h2(texto_salidas, 18, 28)
    contexto_canonico = json.dumps(
        {
            "context_template": contexto_comun,
            "common_objective": objetivo,
            "eda_stage_contract": etapas,
            "output_contract": salidas,
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    hashes = {
        IDS_PROMPT["common"]: _hash_texto(instruccion_comun),
        IDS_PROMPT["planner"]: _hash_texto(instrucciones["planner"]),
        IDS_PROMPT["analyst_initial"]: _hash_texto(instrucciones["analyst_initial"]),
        IDS_PROMPT["reviewer"]: _hash_texto(instrucciones["reviewer"]),
        IDS_PROMPT["analyst_correction"]: _hash_texto(
            instrucciones["analyst_correction"]
        ),
        IDS_PROMPT["context"]: _hash_texto(contexto_canonico),
    }
    esperados = set(configuracion.datos["prompts"]["component_ids"])
    if set(hashes) != esperados:
        raise ErrorPrompt("Los identificadores de prompts no coinciden con la configuración")
    return PlantillasPrompts(
        instruccion_comun=instruccion_comun,
        contexto_comun=contexto_comun,
        instrucciones_roles=MappingProxyType(instrucciones),
        objetivo_comun=objetivo,
        contrato_etapas=etapas,
        contrato_salidas=salidas,
        hashes=MappingProxyType(hashes),
    )


def cargar_documentacion_publica(
    configuracion: ConfiguracionExperimento,
    contexto: ContextoEjecucion,
) -> str:
    """Reúne los documentos públicos autorizados para la ejecución."""
    bloques: list[str] = []
    for ruta in contexto.dataset.documentacion_publica:
        try:
            contenido = _normalizar(ruta.read_text(encoding="utf-8"))
        except OSError as exc:
            raise ErrorPrompt(
                f"No puede leerse la documentación pública: {ruta.name}"
            ) from exc
        relativa = ruta.relative_to(configuracion.raiz_tfm).as_posix()
        bloques.append(
            f"[PUBLIC_DOCUMENT path={relativa}]\n{contenido}\n[/PUBLIC_DOCUMENT]"
        )
    if not bloques:
        raise ErrorPrompt("El dataset no tiene documentación pública autorizada")
    return "\n\n".join(bloques)


def _texto_dinamico(valor: Any) -> str:
    """Convierte a texto la información que se incorpora al prompt."""
    if isinstance(valor, str):
        return valor
    return json.dumps(valor, ensure_ascii=False, indent=2, sort_keys=True)


def _sustituir(plantilla: str, valores: Mapping[str, Any]) -> str:
    """Incorpora los valores de las variables y comprueba que no queden pendientes."""
    necesarias = set(VARIABLE.findall(plantilla))
    ausentes = sorted(necesarias - set(valores))
    if ausentes:
        raise ErrorPrompt(f"Faltan variables del prompt: {', '.join(ausentes)}")
    desconocidas = sorted(set(valores) - necesarias)
    if desconocidas:
        valores = {clave: valor for clave, valor in valores.items() if clave in necesarias}
    resultado = VARIABLE.sub(lambda match: _texto_dinamico(valores[match.group(1)]), plantilla)
    restantes = VARIABLE.findall(resultado)
    if restantes:
        raise ErrorPrompt(f"Quedan variables sin resolver: {', '.join(sorted(set(restantes)))}")
    return resultado


def construir_prompt_rol(
    plantillas: PlantillasPrompts,
    configuracion: ConfiguracionExperimento,
    contexto: ContextoEjecucion,
    rol: str,
    documentacion_publica: str,
    inspeccion: Mapping[str, Any] | None = None,
    plan: str | None = None,
    validacion_previa: Mapping[str, Any] | None = None,
    decision_revision: Mapping[str, Any] | None = None,
    validacion_actual: Mapping[str, Any] | None = None,
) -> PromptConstruido:
    """Prepara los mensajes del rol con las instrucciones y la información autorizadas."""

    if rol not in ROLES:
        raise ErrorPrompt(f"Rol de prompt desconocido: {rol}")
    sistema = _sustituir(
        plantillas.instruccion_comun,
        {
            "ROLE_NAME": ROLES[rol],
            "COMMON_OBJECTIVE": plantillas.objetivo_comun,
        },
    )
    comun = _sustituir(
        plantillas.contexto_comun,
        {
            "RUN_ID": contexto.run_id,
            "FRAMEWORK_ID": contexto.framework_id,
            "DATASET_ID": contexto.dataset.dataset_id,
            "INPUT_FORMAT": contexto.dataset.formato,
            "CONTRACT_VERSION": configuracion.datos["versions"]["contract"],
            "PROMPT_VERSION": configuracion.datos["versions"]["prompts"],
            "PUBLIC_DOCUMENTATION": documentacion_publica,
        },
    )
    valores: dict[str, Any] = {
        "EDA_STAGE_CONTRACT": plantillas.contrato_etapas,
        "OUTPUT_CONTRACT": plantillas.contrato_salidas,
    }
    if rol in {"analyst_initial", "analyst_correction"}:
        if inspeccion is None or plan is None:
            raise ErrorPrompt("El Analista requiere inspección y plan")
        valores["INSPECTION_RESULT"] = inspeccion
        valores["PLAN_CONTENT"] = plan
    if rol == "reviewer":
        if validacion_previa is None:
            raise ErrorPrompt("El Revisor requiere la validación previa")
        valores["PRE_REVIEW_VALIDATION"] = validacion_previa
    if rol == "analyst_correction":
        if decision_revision is None or validacion_actual is None:
            raise ErrorPrompt("La corrección requiere decisión y validación actual")
        valores["REVIEW_DECISION"] = decision_revision
        valores["CURRENT_VALIDATION"] = validacion_actual
    especifico = _sustituir(plantillas.instrucciones_roles[rol], valores)
    usuario = f"{comun}\n\n{especifico}"
    canonico = json.dumps(
        [
            {"role": "system", "content": sistema},
            {"role": "user", "content": usuario},
        ],
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return PromptConstruido(
        rol=rol,
        instruccion_sistema=sistema,
        contenido_usuario=usuario,
        sha256=_hash_texto(canonico),
    )


def construir_prompt_reparacion_formato(
    prompt_original: PromptConstruido,
    contenido_rechazado: str,
    error_validacion: str,
) -> PromptConstruido:
    """Prepara una solicitud para corregir el formato sin repetir el análisis."""

    if not isinstance(contenido_rechazado, str) or not contenido_rechazado.strip():
        raise ErrorPrompt("No existe una respuesta textual que reparar")
    if not isinstance(error_validacion, str) or not error_validacion.strip():
        raise ErrorPrompt("La reparación requiere el error de validación")
    coincidencia = re.search(
        r"\[OUTPUT_FORMAT\]\s*(.*?)\s*\[/OUTPUT_FORMAT\]",
        prompt_original.contenido_usuario,
        flags=re.DOTALL,
    )
    if not coincidencia:
        raise ErrorPrompt("El prompt original no contiene el formato de salida")
    formato = coincidencia.group(1).strip()
    usuario = (
        "[FORMAT_REPAIR]\n"
        "La respuesta anterior no pudo guardarse porque incumple el formato "
        "obligatorio. Esta intervención sirve exclusivamente para reparar su "
        "estructura.\n\n"
        "No realices nuevos cálculos, no cambies decisiones, cifras, hallazgos "
        "ni interpretaciones y no solicites herramientas. Conserva todo el "
        "contenido válido y devuelve nuevamente la respuesta completa. No "
        "añadas explicaciones sobre la reparación.\n\n"
        f"[VALIDATION_ERROR]\n{error_validacion.strip()}\n[/VALIDATION_ERROR]\n\n"
        f"[REQUIRED_OUTPUT_FORMAT]\n{formato}\n[/REQUIRED_OUTPUT_FORMAT]\n\n"
        "[REJECTED_RESPONSE]\n"
        f"{contenido_rechazado.strip()}\n"
        "[/REJECTED_RESPONSE]\n"
        "[/FORMAT_REPAIR]"
    )
    canonico = json.dumps(
        [
            {"role": "system", "content": prompt_original.instruccion_sistema},
            {"role": "user", "content": usuario},
        ],
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return PromptConstruido(
        rol=prompt_original.rol,
        instruccion_sistema=prompt_original.instruccion_sistema,
        contenido_usuario=usuario,
        sha256=_hash_texto(canonico),
    )


def interpretar_decision_revisor(texto: str) -> dict[str, Any]:
    """Comprueba la estructura y la coherencia de la decisión del Revisor."""

    try:
        valor = json.loads(texto)
    except (json.JSONDecodeError, TypeError) as exc:
        raise ErrorPrompt("La decisión del Revisor no es JSON válido") from exc
    if not isinstance(valor, dict):
        raise ErrorPrompt("La decisión del Revisor debe ser un objeto JSON")
    requeridos = {"decision", "summary", "findings", "correction_requested"}
    if set(valor) != requeridos:
        raise ErrorPrompt("La decisión del Revisor no contiene los campos exactos")
    decision = valor["decision"]
    if decision not in {"approved", "correction_required", "cannot_review"}:
        raise ErrorPrompt("La decisión del Revisor no está permitida")
    if not isinstance(valor["summary"], str) or not valor["summary"].strip():
        raise ErrorPrompt("El resumen de revisión está vacío")
    if not isinstance(valor["findings"], list):
        raise ErrorPrompt("findings debe ser una lista")
    if not isinstance(valor["correction_requested"], bool):
        raise ErrorPrompt("correction_requested debe ser booleano")

    ids: set[str] = set()
    bloqueantes = 0
    campos_hallazgo = {
        "finding_id",
        "category",
        "severity",
        "description",
        "affected_artifacts",
        "evidence_refs",
        "evidence",
        "requires_correction",
        "required_change",
        "resolution_condition",
    }
    for hallazgo in valor["findings"]:
        if not isinstance(hallazgo, dict) or set(hallazgo) != campos_hallazgo:
            raise ErrorPrompt("Un hallazgo del Revisor no respeta el esquema")
        identificador = hallazgo["finding_id"]
        if not isinstance(identificador, str) or not re.fullmatch(r"REV-\d{3}", identificador):
            raise ErrorPrompt("finding_id no respeta el formato REV-NNN")
        if identificador in ids:
            raise ErrorPrompt("finding_id está duplicado")
        ids.add(identificador)
        if hallazgo["category"] not in CATEGORIAS_REVISION:
            raise ErrorPrompt("La categoría del hallazgo no está permitida")
        if hallazgo["severity"] not in {"low", "medium", "high"}:
            raise ErrorPrompt("La severidad del hallazgo no está permitida")
        for campo in ("description", "evidence"):
            if not isinstance(hallazgo[campo], str) or not hallazgo[campo].strip():
                raise ErrorPrompt(f"{campo} del hallazgo está vacío")
        for campo in ("affected_artifacts", "evidence_refs"):
            if not isinstance(hallazgo[campo], list) or not all(
                isinstance(elemento, str) for elemento in hallazgo[campo]
            ):
                raise ErrorPrompt(f"{campo} del hallazgo debe ser una lista de cadenas")
        if not isinstance(hallazgo["requires_correction"], bool):
            raise ErrorPrompt("requires_correction debe ser booleano")
        if hallazgo["requires_correction"]:
            bloqueantes += 1
            if not all(
                isinstance(hallazgo[campo], str) and hallazgo[campo].strip()
                for campo in ("required_change", "resolution_condition")
            ):
                raise ErrorPrompt("Un hallazgo bloqueante requiere cambio y condición")
        elif hallazgo["required_change"] is not None or hallazgo["resolution_condition"] is not None:
            raise ErrorPrompt("Un hallazgo no bloqueante no debe solicitar cambios")

    solicitada = valor["correction_requested"]
    if decision == "correction_required" and (not solicitada or bloqueantes == 0):
        raise ErrorPrompt("correction_required exige al menos un hallazgo bloqueante")
    if decision in {"approved", "cannot_review"} and (solicitada or bloqueantes > 0):
        raise ErrorPrompt(f"{decision} no puede solicitar corrección")
    return valor


def interpretar_respuesta_correccion(
    texto: str,
    decision_revision: Mapping[str, Any],
) -> RespuestaCorreccion:
    """Comprueba el resumen de corrección y lo separa del informe actualizado."""

    patron = re.compile(
        r"^\s*<CORRECTION_SUMMARY>\s*(.*?)\s*</CORRECTION_SUMMARY>\s*"
        r"<REPORT_MD>\s*(.*?)\s*</REPORT_MD>\s*$",
        flags=re.DOTALL,
    )
    coincidencia = patron.fullmatch(texto)
    if not coincidencia:
        raise ErrorPrompt("La corrección no contiene exactamente los dos bloques requeridos")
    try:
        resumen = json.loads(coincidencia.group(1))
    except json.JSONDecodeError as exc:
        raise ErrorPrompt("CORRECTION_SUMMARY no es JSON válido") from exc
    if not isinstance(resumen, dict) or set(resumen) != {
        "addressed_findings",
        "unresolved_findings",
        "changes",
    }:
        raise ErrorPrompt("CORRECTION_SUMMARY no contiene los campos exactos")
    atendidos = resumen["addressed_findings"]
    no_resueltos = resumen["unresolved_findings"]
    if not all(
        isinstance(lista, list) and all(isinstance(valor, str) for valor in lista)
        for lista in (atendidos, no_resueltos)
    ):
        raise ErrorPrompt("Las listas de hallazgos de la corrección no son válidas")
    if set(atendidos) & set(no_resueltos):
        raise ErrorPrompt("Un hallazgo no puede estar atendido y no resuelto")
    requeridos = {
        hallazgo["finding_id"]
        for hallazgo in decision_revision.get("findings", [])
        if hallazgo.get("requires_correction") is True
    }
    if set(atendidos) | set(no_resueltos) != requeridos:
        raise ErrorPrompt("La corrección no clasifica todos los hallazgos requeridos")
    cambios = resumen["changes"]
    if not isinstance(cambios, list):
        raise ErrorPrompt("changes debe ser una lista")
    for cambio in cambios:
        if not isinstance(cambio, dict) or set(cambio) != {"artifact", "description"}:
            raise ErrorPrompt("Un cambio declarado no respeta el esquema")
        if cambio["artifact"] not in ARTEFACTOS_CORREGIBLES:
            raise ErrorPrompt("La corrección declara un artefacto no autorizado")
        if not isinstance(cambio["description"], str) or not cambio["description"].strip():
            raise ErrorPrompt("La descripción de un cambio está vacía")
    informe = coincidencia.group(2).strip()
    if not informe:
        raise ErrorPrompt("REPORT_MD está vacío")
    return RespuestaCorreccion(resumen=resumen, informe=informe)
