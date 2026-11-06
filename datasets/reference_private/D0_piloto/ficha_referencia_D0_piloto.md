# Ficha de referencia D0 - Pedidos sintéticos

**Versión:** 0.1 
**Uso:** referencia para el piloto técnico
**Acceso durante el experimento:** no disponible para los agentes

## 1. Procedencia y finalidad

D0 es un dataset sintético generado específicamente para probar el flujo común de LangGraph, CrewAI y Microsoft Agent Framework antes de utilizar D1 y D2. No representa personas ni empresas reales y sus resultados no forman parte de la comparación definitiva.

- Generador: `datasets/reference_private/D0_piloto/generate_pilot.mjs`.
- Versión del generador: 1.0.
- Semilla: `20260808`.
- Entrada: `datasets/experiment_inputs/D0_piloto/pedidos_piloto.csv`.
- SHA-256: `9073C498158358126C1F10A27BD0C6144A59814C33CDF99314C31C42A1F11412`.
- Documentación pública: `datasets/experiment_inputs/D0_piloto/Readme.md`.

El piloto debe comprobar que los tres frameworks pueden ejecutar las ocho etapas del EDA, utilizar las herramientas comunes, producir los archivos obligatorios y dejar una traza evaluable. También servirá para validar que el corrector acepta tratamientos alternativos razonables.

## 2. Estructura esperada

- 246 filas y 13 columnas.
- 240 identificadores de pedido distintos.
- Periodo válido: 1 de enero a 10 de junio de 2025.
- Seis meses naturales presentes; junio solo contiene observaciones hasta el día 10.
- Cada fila representa un pedido.

## 3. Situaciones de calidad controladas

| Situación | Resultado esperado |
| --- | ---: |
| Celdas ausentes | 24 |
| Fechas ausentes | 2 |
| Regiones ausentes | 3 |
| Plazos de entrega ausentes | 5 |
| Valoraciones ausentes | 14 |
| Duplicados exactos después del primero | 6 |
| Filas después de deduplicar | 240 |
| Descuentos fuera de 0-1 | 2 |
| Plazos de entrega negativos | 2 |
| Incumplimientos de la fórmula del importe | 4 |

Las etiquetas de región aparecen en nueve formas textuales, pero corresponden a cuatro categorías después de recortar espacios y normalizar mayúsculas. Los canales aparecen en seis formas y corresponden a tres categorías.

## 4. Valores descriptivos principales

| Medida | Resultado |
| --- | ---: |
| Unidades totales | 2.179 |
| Media de unidades | 8,857724 |
| Mediana de unidades | 5 |
| Máximo de unidades | 85 |
| Importe neto registrado | 178.802,89 € |
| Importe neto recalculado | 178.793,05 € |
| Importe registrado después de deduplicar | 170.319,56 € |
| Diferencia atribuible a duplicados exactos | 8.483,33 € |
| Pedidos devueltos | 10 |
| Tasa de devolución | 4,0650 % |

El máximo de 85 unidades pertenece a un pedido mayorista creado como extremo válido. Debe conservarse salvo que exista una razón adicional, y puede requerir medidas o visualizaciones robustas.

## 5. Patrones de referencia

- Enero de 2025 es el mes completo con mayor importe registrado: 39.091,87 €.
- Junio de 2025 es parcial y no debe compararse directamente con los meses completos.
- Tienda presenta el menor plazo medio válido de entrega: aproximadamente 1,14 días.
- La satisfacción media, excluidos los valores ausentes, es 4,6622 en pedidos no devueltos y 3,7000 en devueltos.
- La asociación entre devolución y satisfacción es descriptiva; no permite establecer causalidad.

## 6. Tratamientos que debe admitir el piloto

1. Normalizar región y canal eliminando espacios iniciales y finales y unificando mayúsculas y minúsculas.
2. Eliminar duplicados exactos y documentar su efecto, o conservarlos y comparar los resultados con y sin esas filas.
3. Excluir descuentos inválidos del análisis monetario, marcarlos como ausentes o aplicar otro tratamiento justificado que no los corrija silenciosamente.
4. Transformar plazos negativos en ausentes o excluirlos de estadísticas de entrega, con trazabilidad.
5. Conservar `net_amount_eur` y crear un importe recalculado para comprobar diferencias.
6. Mantener el pedido mayorista de 85 unidades y evitar su eliminación automática.
7. Conservar ausencias o imputarlas únicamente cuando exista una justificación explícita y una marca de imputación.
8. Excluir junio de comparaciones entre meses completos o señalar claramente su cobertura parcial.

El corrector no deberá exigir un único archivo preparado. Debe puntuar la validez, la justificación y la trazabilidad de las decisiones.

## 7. Riesgos conocidos para Q4

1. Ausencias en fecha, región, entrega y satisfacción.
2. Duplicados exactos e identificadores repetidos.
3. Variantes de escritura en región y canal.
4. Descuentos fuera del intervalo 0-1.
5. Plazos de entrega negativos.
6. Importes que incumplen la fórmula documentada.
7. Pedido mayorista extremo pero válido.
8. Cobertura parcial de junio.
9. Diferencia de satisfacción entre pedidos devueltos y no devueltos sin base causal.
10. Naturaleza sintética y pequeño tamaño del dataset.

## 8. Unidades de información y visualizaciones

`evaluation_spec.json` define once unidades de información para Q8 y cuatro objetivos visuales para Q7. Los objetivos cubren temporalidad, distribución y extremo, comparación de categorías normalizadas y relaciones entre entrega, devolución y satisfacción.

Cada objetivo visual se puntúa de 0 a 4. Q7 se expresa de 0 a 100 mediante `Q7 = 100 x suma de las cuatro puntuaciones / 16`.

## 9. Comprobaciones numéricas

Las 32 comprobaciones de `evaluation_spec.json` se contrastarán con `reference_values.json`.

- Conteos, fechas y categorías: coincidencia exacta.
- Importes: tolerancia absoluta de 0,01 €.
- Medias: tolerancia absoluta de 0,01.
- Proporciones: tolerancia absoluta de 0,001.

Se aceptarán cifras equivalentes después de un tratamiento válido cuando el informe declare claramente la población y la transformación. Los valores de referencia permiten comparar los resultados originales con los obtenidos después de eliminar duplicados o recalcular importes.

## 10. Salidas esperadas

Las salidas esperadas son `plan.md`, `prepared_data.csv`, `statistics.json`, `issues.json`, `figures/`, `report.md` y `trace.jsonl`.