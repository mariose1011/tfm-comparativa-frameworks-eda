"""Datos simulados reutilizables por las pruebas de los tres adaptadores."""

from __future__ import annotations

import json
from typing import Any


def plan_simulado(run_id: str, framework_id: str) -> str:
    etapas = []
    for numero in range(1, 9):
        etapas.append(
            f"""## E{numero}

Objetivo: comprobar la etapa {numero}.

Comprobaciones: realizar una comprobación reproducible.

Variables o grupos: se concretarán a partir de la inspección.

Evidencia esperada: resultado estructurado y trazable.

Supuestos o dependencias: no se asumen hallazgos previos.
"""
        )
    return f"""# Identificación

run_id: {run_id}

framework_id: {framework_id}

dataset_id: D0_piloto

contract_version: 1.0

prompt_version: 1.0

# Comprensión inicial

Se analizará el dataset autorizado y se conservarán las incertidumbres.

# Preguntas analíticas

Se estudiarán la calidad, las distribuciones y las relaciones pertinentes.

# Plan por etapas

{"".join(etapas)}
# Visualizaciones previstas

Se representará una distribución relevante con una figura trazable.

# Supuestos y riesgos

Los tipos, ausencias y valores extremos deberán comprobarse.

# Criterios de finalización

Los resultados deberán ser reproducibles, coherentes y estar referenciados.
"""


def plan_simulado_con_formato_invalido(run_id: str, framework_id: str) -> str:
    """Reproduce el uso de títulos añadidos después de E1 a E8."""

    contenido = plan_simulado(run_id, framework_id)
    for numero in range(1, 9):
        contenido = contenido.replace(
            f"## E{numero}\n",
            f"## E{numero}. Etapa {numero}\n",
        )
    return contenido


def informe_simulado(corregido: bool = False) -> str:
    nota = (
        " La referencia ha sido comprobada durante la corrección."
        if corregido
        else ""
    )
    return f"""# Resumen ejecutivo

Se presenta un resultado descriptivo respaldado por evidencia [STAT-001].{nota}

# Dataset y alcance

El análisis se limita al dataset autorizado y al EDA tabular.

# Inspección, calidad y preparación

Se creó una copia preparada trazable y separada del original.

# Estadística descriptiva

El recuento de la copia preparada se conserva en [STAT-001].

# Variables, agregaciones y relaciones

Se resume una variable sin formular afirmaciones causales [STAT-001].

# Visualizaciones y hallazgos

La figura [FIG-001] está disponible en figures/fig_001_prueba.png.

# Problemas, riesgos y anomalías

Las comprobaciones realizadas están documentadas en issues.json.

# Limitaciones e incertidumbres

Esta ejecución simulada comprueba el flujo y no la calidad del análisis.

# Conclusiones

Los artefactos mantienen referencias estructurales resolubles [STAT-001].
"""


def codigo_artefactos_simulados() -> str:
    return '''tabla = pd.read_csv(INPUT_PATH)
preparada = tabla.iloc[:2, :2].copy()
preparada.to_csv(f"{OUTPUT_DIR}/prepared_data.csv", index=False)
nombres = [str(nombre) for nombre in preparada.columns]
columnas = []
for nombre in nombres:
    columnas.append({
        "name": nombre,
        "origin": "source",
        "source_name": nombre,
        "original_type": str(tabla[nombre].dtype),
        "prepared_type": str(preparada[nombre].dtype),
        "missing_original": int(tabla[nombre].isna().sum()),
        "missing_prepared": int(preparada[nombre].isna().sum()),
        "unique_prepared": int(preparada[nombre].nunique(dropna=True))
    })
estadisticas = {
    "schema_version": "1.0",
    "run_id": RUN_ID,
    "dataset_id": DATASET_ID,
    "generated_at_utc": "2026-08-29T10:00:00Z",
    "profile": {
        "original_rows": int(tabla.shape[0]),
        "original_columns": int(tabla.shape[1]),
        "prepared_rows": int(preparada.shape[0]),
        "prepared_columns": int(preparada.shape[1]),
        "unit_of_analysis": "Una observación del dataset autorizado",
        "columns": columnas
    },
    "preparation": {
        "summary": "Se crea una copia mínima para comprobar el flujo técnico.",
        "changes": [{
            "id": "TR-001",
            "action": "selection",
            "description": "Selección de dos filas y dos columnas para la simulación",
            "justification": "Comprobar la generación controlada de resultados",
            "affected_columns": nombres,
            "rows_affected": 2,
            "before": {"rows": int(tabla.shape[0])},
            "after": {"rows": 2}
        }]
    },
    "analyses": [{
        "id": "STAT-001",
        "stage": "E1",
        "analysis_type": "count",
        "title": "Filas de la copia preparada",
        "variables": [nombres[0]],
        "population": "Copia preparada de la simulación",
        "method": "Recuento de filas",
        "result": {"rows": 2},
        "interpretation": "La copia preparada contiene dos filas."
    }],
    "figures": [{
        "id": "FIG-001",
        "file": "figures/fig_001_prueba.png",
        "title": "Figura de prueba técnica",
        "objective": "Comprobar la generación y el registro de una figura",
        "variables": [nombres[0]],
        "source_analysis_ids": ["STAT-001"]
    }],
    "limitations": ["Resultados creados para una prueba técnica simulada"]
}
with open(f"{OUTPUT_DIR}/statistics.json", "w", encoding="utf-8") as archivo:
    json.dump(estadisticas, archivo, ensure_ascii=False, indent=2, allow_nan=False)
incidencias = {
    "schema_version": "1.0",
    "run_id": RUN_ID,
    "dataset_id": DATASET_ID,
    "checks_performed": [{
        "id": "CHK-001",
        "category": "completeness",
        "description": "Comprobación de la estructura preparada",
        "outcome": "La copia preparada contiene dos filas",
        "evidence_ids": ["STAT-001"]
    }],
    "issues": []
}
with open(f"{OUTPUT_DIR}/issues.json", "w", encoding="utf-8") as archivo:
    json.dump(incidencias, archivo, ensure_ascii=False, indent=2, allow_nan=False)
plt.figure(figsize=(4, 3))
plt.plot([1, 2], [1, 2])
plt.title("Figura de prueba técnica")
plt.xlabel("Observación")
plt.ylabel("Valor")
plt.tight_layout()
plt.savefig(f"{FIGURES_DIR}/fig_001_prueba.png")
plt.close()
print("Artefactos simulados creados")
'''


def decision_aprobada_simulada() -> str:
    return json.dumps(
        {
            "decision": "approved",
            "summary": "Los resultados permiten completar la revisión técnica.",
            "findings": [],
            "correction_requested": False,
        },
        ensure_ascii=False,
    )


def decision_correccion_simulada() -> dict[str, Any]:
    return {
        "decision": "correction_required",
        "summary": "Debe aclararse una referencia del informe.",
        "findings": [
            {
                "finding_id": "REV-001",
                "category": "traceability",
                "severity": "medium",
                "description": "Una referencia del informe requiere aclaración.",
                "affected_artifacts": ["report.md"],
                "evidence_refs": ["# Resumen ejecutivo"],
                "evidence": (
                    "La evidencia estructurada existe, pero debe aclararse su "
                    "comprobación."
                ),
                "requires_correction": True,
                "required_change": (
                    "Aclarar que la referencia ha sido comprobada."
                ),
                "resolution_condition": (
                    "El informe contiene la aclaración solicitada."
                ),
            }
        ],
        "correction_requested": True,
    }


def respuesta_correccion_simulada() -> str:
    resumen = {
        "addressed_findings": ["REV-001"],
        "unresolved_findings": [],
        "changes": [
            {
                "artifact": "report.md",
                "description": (
                    "Se aclara la comprobación de la referencia de REV-001."
                ),
            }
        ],
    }
    return (
        "<CORRECTION_SUMMARY>\n"
        + json.dumps(resumen, ensure_ascii=False)
        + "\n</CORRECTION_SUMMARY>\n<REPORT_MD>\n"
        + informe_simulado(corregido=True)
        + "\n</REPORT_MD>"
    )
