# Evaluación D2-MAF-R1

**Índice final:** 84,99/100.  
**Evaluación cerrada:** 6 de octubre de 2026.  
**Ejecución:** `D2_online_retail__microsoft_agent_framework__r01__20260902T172454433424Z`

**Criterios:** [Protocolo de evaluación](../01_protocolo_calidad_Q1_Q10_v0.1.md) y [guía D2](../02_ficha_D2_online_retail.md).  
**Resultados:** [Archivos originales de la ejecución](../../../outputs/experimento/D2_online_retail__microsoft_agent_framework__r01__20260902T172454433424Z).  
**Evaluación:** [Excel de puntuaciones](../Evaluacion_calidad.xlsx) y [JSON de comprobaciones](D2-MAF-R1_comprobaciones.json).

Las referencias `STAT`, `ISSUE` y `FIG` identifican análisis, problemas y figuras en los archivos de la ejecución. `TR` identifica transformaciones y `CHK`, comprobaciones de calidad. Las referencias a líneas corresponden al informe original, `report.md`.

## Resumen

| Métrica | Puntuación final |
| --- | ---: |
| Q1 Cumplimiento de las etapas | 100,00 |
| Q2 Corrección numérica | 87,23 |
| Q3 Validez del tratamiento de los datos | 83,33 |
| Q4 Detección de problemas y riesgos | 82,35 |
| Q5 Calidad y profundidad del EDA | 75,00 |
| Q6 Profundidad de la interpretación | 75,00 |
| Q7 Calidad de las visualizaciones | 75,00 |
| Q8 Cobertura del informe | 90,91 |
| Q9 Fidelidad del informe | 100,00 |
| Q10 Claridad y coherencia | 75,00 |

## Q1 Cumplimiento de las etapas: 100,00

Las ocho etapas disponen de evidencia válida:

| Etapa | Nota | Evidencia |
| --- | ---: | --- |
| E1 Carga e inspección inicial | 1 | STAT-001, perfil y documentación consultada en evento7 |
| E2 Estructura, tipos y calidad | 1 | STAT-002 a STAT-009 y STAT-016 |
| E3 Preparación y decisiones de análisis | 1 | CSV, TR-001 a TR-004 y evento16 |
| E4 Estadística descriptiva | 1 | STAT-005/006/007/010/011/012 |
| E5 Variables, agregaciones y relaciones | 1 | STAT-013/014/015 |
| E6 Visualizaciones | 1 | Cinco PNG válidos y vinculados a los análisis |
| E7 Problemas, riesgos y anomalías | 1 | Siete comprobaciones y seis incidencias con decisiones |
| E8 Informe final | 1 | Alcance, resultados, preparación y limitaciones integrados |

`Q1 = 100 x 8 / 8 = 100,00`

## Q2 Corrección numérica: 87,23

Se cumplen 27 de las 32 comprobaciones previstas, que suman 41 de los 47 puntos ponderados.

| Controles | Resultado | Evidencia o motivo |
| --- | --- | --- |
| C01–C09 | Correctos | Estructura, fechas, marginales y cruce de ausencias, duplicados. STAT-001/002/003 |
| C10 | Correcto | Los 541.909 registros originales menos los 5.268 duplicados dan 536.641 registros. STAT-001 y STAT-003 |
| C11–C17 | Correctos | Cardinalidades, líneas C, facturas C y cantidades negativas. STAT-003/005/010 |
| C18 | Ausente | Los 2.517 registros sin marca de cancelación agrupan casos con cantidad o precio iguales o inferiores a cero. No identifican específicamente cuántos tienen cantidad negativa. STAT-016 |
| C19–C20 | Correctos | 2515 precios cero y dos negativos. STAT-006 |
| C21 | Correcto | La media de Quantity multiplicada por los 541.909 registros permite obtener 5.176.450 unidades. Se utiliza la precisión conservada en STAT-005 |
| C22–C23 | Correctos | Extremos de Quantity. STAT-005 |
| C24 | Correcto | La media de LineAmount multiplicada por los 541.909 registros permite obtener un importe neto de 9.747.747,934 GBP. Se utiliza la precisión conservada en STAT-007 |
| C25–C26 | Correctos | 530104 líneas y 10666684,544 GBP positivos. STAT-010/011 |
| C27 | Correcto | Los trece importes mensuales de cancelaciones de STAT-013 suman −896.812,49 GBP |
| C28 | Ausente | No presenta el importe neto después de excluir los duplicados exactos |
| C29 | Ausente | Comunica el importe y el número de registros del Reino Unido dentro de las ventas positivas, no su porcentaje sobre todos los registros originales |
| C30 | Correcto | Noviembre2011 y 1509496,33 GBP positivos. STAT-013 |
| C31 | Ausente | Cuenta 650 códigos con más de una descripción, comparando el texto tal como aparece. C31 exige ignorar las diferencias de mayúsculas y los espacios iniciales y finales; con ese criterio, el resultado es 647 |
| C32 | Ausente | No presenta la mediana del número de registros por factura. |

`Q2 = 100 x 41 / 47 = 87,23`

## Q3 Validez del tratamiento de los datos: 83,33

Diez de doce ámbitos válidos. D08 y D09 están incompletos, sin limpieza perjudicial.

| Decisión | Nota | Justificación y evidencia |
| --- | ---: | --- |
| D01 Identificadores | 1 | Identificadores guardados como texto, conservando sus valores y los datos ausentes. TR-001 y CSV |
| D02 Fecha-hora | 1 | El CSV conserva la fecha y la hora de todos los registros en formato ISO 8601. TR-002 |
| D03 Importe | 1 | LineAmount = Quantity x UnitPrice, poblaciones declaradas. STAT-009/011/013 |
| D04 Unidades | 1 | Distingue líneas, facturas, clientes y pares de artículo/descripción. STAT-010/014 |
| D05 Cancelaciones | 1 | Conserva e identifica las cancelaciones y cuantifica sus registros, facturas e importes mensuales. STAT-010/013 |
| D06 Cliente ausente | 1 | Retiene filas globales e informa cobertura. STAT-002/010 e informe23/81 |
| D07 Descripción ausente | 1 | Conserva ausencias, sin inventar etiquetas en filas. CSV |
| D08 Duplicados | 0 | Conserva los duplicados, pero no compara los resultados con y sin esas filas. ISSUE-002 |
| D09 Ajustes | 0 | Cuantifica los precios cero y negativos, pero no identifica ni examina por separado las cantidades negativas sin marca de cancelación. STAT-005/006/016 |
| D10 Extremos | 1 | Conserva extremos, usa cuantiles y escalas robustas. STAT-011/015, FIG-002/005 |
| D11 Mes final | 1 | Diciembre 2011 marcado como parcial. STAT-008/013 e informe51/86 |
| D12 Categorías | 1 | Limita los gráficos a las categorías principales y conserva el detalle original. FIG-003/004 |

`Q3 = 100 x 10 / 12 = 83,33`

## Q4 Detección de problemas y riesgos: 82,35

Se detectan por completo siete de los diez riesgos de referencia (K = 7) y se identifican dos riesgos adicionales válidos (A = 2), sin falsas alarmas (F = 0). Los nueve hallazgos contabilizados son válidos, por lo que la precisión es del 100 %, mientras que la cobertura de los riesgos de referencia es del 70 %. Ambas medidas se combinan mediante F1 para obtener la puntuación de Q4.

| Riesgo conocido | Resultado | Evidencia |
| --- | --- | --- |
| R01 Ausencias | Detectado | STAT-002 e ISSUE-001 |
| R02 Duplicados | Detectado | STAT-003 e ISSUE-002 |
| R03 Cancelaciones y signos | Detectado | C documentado, valores no positivos asociados a C y serie firmada. STAT-004/010/013/016, ISSUE-003 |
| R04 Negativos sin C | Parcial | Se detectan no positivos sin C, sin aislar Quantity negativa. STAT-016 |
| R05 Precios cero y negativos | Detectado | Ambos cuantificados en STAT-006 e informe41 |
| R06 Unidad e identificadores | Detectado | Perfil, TR-001, STAT-001/003 e informe17/25 |
| R07 Mes final parcial | Detectado | STAT-008 e ISSUE-004 |
| R08 Concentración de líneas UK | Parcial | Concentración monetaria positiva, no proporción de líneas originales |
| R09 Asimetría y extremos | Detectado | STAT-005/006/007/011/015 e ISSUE-005 |
| R10 Definiciones monetarias | Parcial | Sin comparación completa de los importes netos, positivos y de cancelaciones ni análisis del efecto de excluir duplicados |

La ejecución identifica también dos problemas adicionales relacionados con las descripciones y con la naturaleza de los conceptos facturados.

| Hallazgo adicional | Clasificación | Evidencia |
| --- | --- | --- |
| Un mismo código tiene varias descripciones, algunas con espacios iniciales o finales, que pueden separar sus resultados al agrupar | A01 válido | STAT-004/009 e ISSUE-006 |
| Algunos códigos representan gastos de envío u operaciones manuales, no productos físicos | A02 válido | STAT-014 y líneas 55/71 del informe |

`Q4 = 100 x [2 x 1 x (7 / 10)] / [1 + (7 / 10)] = 82,35`

## Q5 Calidad y profundidad del EDA: 75,00

El análisis examina distribuciones generales y de ventas positivas, ausencias conjuntas, relaciones entre identificadores, evolución temporal, países, artículos, asociaciones y valores extremos. Recibe 3 de 4 puntos porque no cuantifica el efecto de excluir duplicados ni completa la comparación de los principales importes y ajustes.

Evidencia: STAT-002/005/006/007/009/011/012/013/014/015/016.

`Q5 = 100 x 3 / 4 = 75,00`

## Q6 Profundidad de la interpretación: 75,00

El informe relaciona la concentración geográfica, los valores extremos y las unidades analizadas con las limitaciones de los resultados, sin atribuir causalidad. Recibe 3 de 4 puntos porque no desarrolla cuantitativamente las diferencias entre importes netos, cancelaciones y datos sin duplicados, ni interpreta por separado las cantidades negativas sin marca de cancelación.

Evidencia: informe15/51/53/55/57/59/90–98/106.

`Q6 = 100 x 3 / 4 = 75,00`

## Q7 Calidad de las visualizaciones: 75,00

| Objetivo | Nota 0–4 | Justificación |
| --- | ---: | --- |
| V01 Evolución | 4 | FIG-001 representa por separado los importes mensuales de ventas positivas y cancelaciones, con unidades claras y explicación del mes final |
| V02 Cancelaciones/ajustes | 2 | FIG-001 muestra el importe mensual de las cancelaciones, pero no representa por separado las cantidades negativas sin esa marca ni los precios cero o negativos |
| V03 Distribuciones | 3 | FIG-002 muestra las distribuciones positivas completas en escala logarítmica, pero no representa valores cero o negativos |
| V04 Países | 2 | FIG-003 representa correctamente los importes, pero el valor del Reino Unido dificulta comparar los demás países |
| V05 Productos/conceptos | 4 | FIG-004 muestra los diez pares de código y descripción con mayor importe, con códigos legibles. El informe explica la presencia de gastos de envío y operaciones manuales |

`Q7 = 100 x 15 / 20 = 75,00`

## Q8 Cobertura del informe: 90,91

| Unidad | Peso | Nota | Evidencia o motivo |
| --- | ---: | ---: | --- |
| U01 Estructura y periodo | 2 | 1 | Informe3/13/21 |
| U02 Ausencias e impacto | 2 | 1 | Informe23/81/92 |
| U03 Unidades | 2 | 1 | Informe3/17/55 |
| U04 Duplicados y decisión | 2 | 1 | Informe33/82/90 |
| U05 C y negativos | 2 | 1 | Informe37/39/83 y serie firmada63/65 |
| U06 Ajustes | 2 | 0,5 | Comunica precios cero y negativos, pero agrupa los casos no positivos sin marca de cancelación y no identifica específicamente las cantidades negativas |
| U07 Agregados monetarios | 2 | 0,5 | Comunica las ventas positivas y los importes de cancelaciones, pero no el importe neto del conjunto completo ni el efecto de excluir duplicados |
| U08 Evolución y mes final | 2 | 1 | Informe9/51/63/86 |
| U09 Concentración UK | 2 | 1 | Informe53/67/98 advierte grupos de tamaño y composición distintos |
| U10 Cardinalidad y conceptos | 1 | 1 | Informe17/55/71/85 |
| U11 Asimetría y extremos | 2 | 1 | Informe39/41/43/59/84 |
| U12 Cobertura y límites | 1 | 1 | Empresa y periodo en informe13/21, ausencias y ajustes/duplicados en90–98 |

`Q8 = 100 x 20 / 22 = 90,91`

## Q9 Fidelidad del informe: 100,00

Las 151 afirmaciones evaluadas cuentan con respaldo en las evidencias de la ejecución.

El inventario situado al final de esta ficha recoge las afirmaciones revisadas, su clasificación y las evidencias utilizadas.

`Q9 = 100 x 151 / 151 = 100,00`

## Q10 Claridad y coherencia: 75,00

El informe presenta una estructura ordenada y referencias claras. Recibe 3 de 4 puntos porque explica de forma incompleta algunas variables y utiliza la expresión "3.385 StockCode" sin aclarar que se refiere a registros que contienen esos códigos, no a códigos distintos. También repite con frecuencia la denominación "ventas tipo línea".

`Q10 = 100 x 3 / 4 = 75,00`

## Inventario de afirmaciones

R = respaldada.

| ID | Líneas del informe | Afirmación | Estado | Evidencia |
| --- | --- | --- | --- | --- |
| AF001 | 3/13/15/17/21 | 541909 líneas originales | R | STAT-001/003/008, diccionario público y traza7 |
| AF002 | 3/13/15/17/21 | Ocho columnas fuente | R | STAT-001/003/008, diccionario público y traza7 |
| AF003 | 3/13/15/17/21 | Primera fecha-hora 2010-12-01T08:26:00 | R | STAT-001/003/008, diccionario público y traza7 |
| AF004 | 3/13/15/17/21 | Última fecha-hora 2011-12-09T12:50:00 | R | STAT-001/003/008, diccionario público y traza7 |
| AF005 | 3/13/15/17/21 | Una fila es una línea de factura | R | STAT-001/003/008, diccionario público y traza7 |
| AF006 | 3/13/15/17/21 | Una fila no equivale necesariamente a una factura completa | R | STAT-001/003/008, diccionario público y traza7 |
| AF007 | 3/13/15/17/21 | Una fila no equivale necesariamente a una compra completa | R | STAT-001/003/008, diccionario público y traza7 |
| AF008 | 3/13/15/17/21 | Libro XLSX, hoja Online Retail | R | STAT-001/003/008, diccionario público y traza7 |
| AF009 | 3/13/15/17/21 | Lista de ocho campos fuente correcta | R | STAT-001/003/008, diccionario público y traza7 |
| AF010 | 3/13/15/17/21 | Empresa británica de comercio electrónico | R | STAT-001/003/008, diccionario público y traza7 |
| AF011 | 3/13/15/17/21 | C identifica una cancelación según la documentación | R | STAT-001/003/008, diccionario público y traza7 |
| AF012 | 3/13/15/17/21 | UnitPrice está expresado en GBP | R | STAT-001/003/008, diccionario público y traza7 |
| AF013 | 3/13/15/17/21 | El EDA es descriptivo, sin predicción ni inferencia causal | R | STAT-001/003/008, diccionario público y traza7 |
| AF014 | 3/13/15/17/21 | Los importes calculados no certifican estados financieros auditados | R | STAT-001/003/008, diccionario público y traza7 |
| AF015 | 3/13/15/17/21 | Los importes no son ingreso neto definitivo | R | STAT-001/003/008, diccionario público y traza7 |
| AF016 | 3/13/15/17/21 | Facturas contadas mediante InvoiceNo distinto | R | STAT-001/003/008, diccionario público y traza7 |
| AF017 | 3/13/15/17/21 | Análisis por cliente limitado a registros identificados | R | STAT-001/003/008, diccionario público y traza7 |
| AF018 | 3/13/15/17/21 | 25900 facturas distintas originales | R | STAT-001/003/008, diccionario público y traza7 |
| AF019 | 3/13/15/17/21 | 4372 clientes identificados distintos | R | STAT-001/003/008, diccionario público y traza7 |
| AF020 | 3/13/15/17/21 | 4070 códigos StockCode distintos | R | STAT-001/003/008, diccionario público y traza7 |
| AF021 | 3/13/15/17/21 | 38 países originales | R | STAT-001/003/008, diccionario público y traza7 |
| AF022 | 3/13/15/17/21 | No se produjeron fechas inválidas | R | STAT-001/003/008, diccionario público y traza7 |
| AF023 | 3/13/15/17/21 | Trece meses calendario observados | R | STAT-001/003/008, diccionario público y traza7 |
| AF024 | 3/13/15/17/21 | Diciembre 2010 comienza el día1 | R | STAT-001/003/008, diccionario público y traza7 |
| AF025 | 3/13/15/17/21 | Diciembre 2011 acaba el día9 | R | STAT-001/003/008, diccionario público y traza7 |
| AF026 | 5/25/27/28/29/31/33/81/84/85/102/106 | 541909 filas preparadas | R | CSV, perfil, TR-001 a TR-004 y eventos16/75 |
| AF027 | 5/25/27/28/29/31/33/81/84/85/102/106 | Once columnas preparadas | R | CSV, perfil, TR-001 a TR-004 y eventos16/75 |
| AF028 | 5/25/27/28/29/31/33/81/84/85/102/106 | No se eliminaron filas | R | CSV, perfil, TR-001 a TR-004 y eventos16/75 |
| AF029 | 5/25/27/28/29/31/33/81/84/85/102/106 | Se preservaron las ocho columnas fuente | R | CSV, perfil, TR-001 a TR-004 y eventos16/75 |
| AF030 | 5/25/27/28/29/31/33/81/84/85/102/106 | InvoiceNo se serializó como texto nominal | R | CSV, perfil, TR-001 a TR-004 y eventos16/75 |
| AF031 | 5/25/27/28/29/31/33/81/84/85/102/106 | StockCode se serializó como texto nominal | R | CSV, perfil, TR-001 a TR-004 y eventos16/75 |
| AF032 | 5/25/27/28/29/31/33/81/84/85/102/106 | CustomerID se serializó como texto nominal | R | CSV, perfil, TR-001 a TR-004 y eventos16/75 |
| AF033 | 5/25/27/28/29/31/33/81/84/85/102/106 | InvoiceDate se exportó en ISO8601 conservando fecha y hora | R | CSV, perfil, TR-001 a TR-004 y eventos16/75 |
| AF034 | 5/25/27/28/29/31/33/81/84/85/102/106 | Se añadieron tres columnas derivadas | R | CSV, perfil, TR-001 a TR-004 y eventos16/75 |
| AF035 | 5/25/27/28/29/31/33/81/84/85/102/106 | IsCancellation se basa exclusivamente en prefijo C | R | CSV, perfil, TR-001 a TR-004 y eventos16/75 |
| AF036 | 5/25/27/28/29/31/33/81/84/85/102/106 | LineAmount es Quantity por UnitPrice | R | CSV, perfil, TR-001 a TR-004 y eventos16/75 |
| AF037 | 5/25/27/28/29/31/33/81/84/85/102/106 | YearMonth procede del mes de InvoiceDate | R | CSV, perfil, TR-001 a TR-004 y eventos16/75 |
| AF038 | 5/25/27/28/29/31/33/81/84/85/102/106 | Diferencia absoluta máxima de la identidad en memoria igual a cero | R | CSV, perfil, TR-001 a TR-004 y eventos16/75 |
| AF039 | 5/25/27/28/29/31/33/81/84/85/102/106 | No se deduplicaron transacciones | R | CSV, perfil, TR-001 a TR-004 y eventos16/75 |
| AF040 | 5/25/27/28/29/31/33/81/84/85/102/106 | Se conservaron ausencias | R | CSV, perfil, TR-001 a TR-004 y eventos16/75 |
| AF041 | 5/25/27/28/29/31/33/81/84/85/102/106 | No se imputaron identificadores | R | CSV, perfil, TR-001 a TR-004 y eventos16/75 |
| AF042 | 5/25/27/28/29/31/33/81/84/85/102/106 | Se conservaron extremos | R | CSV, perfil, TR-001 a TR-004 y eventos16/75 |
| AF043 | 5/25/27/28/29/31/33/81/84/85/102/106 | Description no se normalizó irreversiblemente | R | CSV, perfil, TR-001 a TR-004 y eventos16/75 |
| AF044 | 5/25/27/28/29/31/33/81/84/85/102/106 | StockCode no se convirtió a medida numérica | R | CSV, perfil, TR-001 a TR-004 y eventos16/75 |
| AF045 | 5/25/27/28/29/31/33/81/84/85/102/106 | El archivo original no se alteró | R | CSV, perfil, TR-001 a TR-004 y eventos16/75 |
| AF046 | 7/9/43/51/53/57/59/106 | El subconjunto exige ausencia de prefijo C | R | STAT-010 a STAT-015 |
| AF047 | 7/9/43/51/53/57/59/106 | El subconjunto exige Quantity positiva | R | STAT-010 a STAT-015 |
| AF048 | 7/9/43/51/53/57/59/106 | El subconjunto exige UnitPrice positivo | R | STAT-010 a STAT-015 |
| AF049 | 7/9/43/51/53/57/59/106 | 530104 líneas positivas | R | STAT-010 a STAT-015 |
| AF050 | 7/9/43/51/53/57/59/106 | 19960 facturas positivas | R | STAT-010 a STAT-015 |
| AF051 | 7/9/43/51/53/57/59/106 | Importe positivo 10666684,54 GBP | R | STAT-010 a STAT-015 |
| AF052 | 7/9/43/51/53/57/59/106 | Las ventas tipo línea no sustituyen la población completa | R | STAT-010 a STAT-015 |
| AF053 | 7/9/43/51/53/57/59/106 | Mediana Quantity positiva igual a 3 | R | STAT-010 a STAT-015 |
| AF054 | 7/9/43/51/53/57/59/106 | Mediana UnitPrice positiva de 2,08 GBP | R | STAT-010 a STAT-015 |
| AF055 | 7/9/43/51/53/57/59/106 | Mediana importe positivo de 9,90 GBP | R | STAT-010 a STAT-015 |
| AF056 | 7/9/43/51/53/57/59/106 | Tercer cuartil importe positivo de 17,70 GBP | R | STAT-010 a STAT-015 |
| AF057 | 7/9/43/51/53/57/59/106 | Media importe positivo de 20,12 GBP | R | STAT-010 a STAT-015 |
| AF058 | 7/9/43/51/53/57/59/106 | Máximo importe positivo de 168469,60 GBP | R | STAT-010 a STAT-015 |
| AF059 | 7/9/43/51/53/57/59/106 | Asimetría positiva relevante | R | STAT-010 a STAT-015 |
| AF060 | 7/9/43/51/53/57/59/106 | Noviembre2011 máximo mensual de importe positivo | R | STAT-010 a STAT-015 |
| AF061 | 7/9/43/51/53/57/59/106 | Importe positivo noviembre2011 de1509496,33 GBP | R | STAT-010 a STAT-015 |
| AF062 | 7/9/43/51/53/57/59/106 | 83369 líneas positivas noviembre2011 | R | STAT-010 a STAT-015 |
| AF063 | 7/9/43/51/53/57/59/106 | Importe positivo  diciembre 2011 de638792,68 GBP | R | STAT-010 a STAT-015 |
| AF064 | 7/9/43/51/53/57/59/106 | Ese importe final corresponde solo hasta día9 | R | STAT-010 a STAT-015 |
| AF065 | 7/9/43/51/53/57/59/106 | UK importe positivo de9025222,08 GBP | R | STAT-010 a STAT-015 |
| AF066 | 7/9/43/51/53/57/59/106 | UK cuota monetaria positiva de84,61% | R | STAT-010 a STAT-015 |
| AF067 | 7/9/43/51/53/57/59/106 | UK contiene485123 líneas positivas | R | STAT-010 a STAT-015 |
| AF068 | 7/9/43/51/53/57/59/106 | Netherlands importe positivo de285446,34 GBP | R | STAT-010 a STAT-015 |
| AF069 | 7/9/43/51/53/57/59/106 | EIRE importe positivo de283453,96 GBP | R | STAT-010 a STAT-015 |
| AF070 | 7/9/43/51/53/57/59/106 | Germany importe positivo de228867,14 GBP | R | STAT-010 a STAT-015 |
| AF071 | 7/9/43/51/53/57/59/106 | France importe positivo de209715,11 GBP | R | STAT-010 a STAT-015 |
| AF072 | 7/9/43/51/53/57/59/106 | Orden descendente UK,Netherlands,EIRE,Germany,France | R | STAT-010 a STAT-015 |
| AF073 | 7/9/43/51/53/57/59/106 | Spearman Quantity–UnitPrice de−0,403 sobre ventas positivas | R | STAT-010 a STAT-015 |
| AF074 | 7/9/43/51/53/57/59/106 | La asociación no prueba causalidad | R | STAT-010 a STAT-015 |
| AF075 | 7/9/43/51/53/57/59/106 | Umbral Tukey de38,63 GBP | R | STAT-010 a STAT-015 |
| AF076 | 7/9/43/51/53/57/59/106 | 42651 líneas superan el umbral Tukey | R | STAT-010 a STAT-015 |
| AF077 | 7/9/43/51/53/57/59/106 | Esas líneas suman52,13% del importe positivo | R | STAT-010 a STAT-015 |
| AF078 | 7/9/43/51/53/57/59/106 | La cola minoritaria puede dominar agregados | R | STAT-010 a STAT-015 |
| AF079 | 7/9/43/51/53/57/59/106 | Tukey no prueba errores | R | STAT-010 a STAT-015 |
| AF080 | 23/33/37/39/41/81/82/83/84/85/86 | 135080 CustomerID ausentes | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF081 | 23/33/37/39/41/81/82/83/84/85/86 | 75,07% de líneas con cliente identificado | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF082 | 23/33/37/39/41/81/82/83/84/85/86 | 1454 Description ausentes | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF083 | 23/33/37/39/41/81/82/83/84/85/86 | 1454 líneas tienen ambas ausencias | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF084 | 23/33/37/39/41/81/82/83/84/85/86 | No hay Description ausente con CustomerID disponible | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF085 | 23/33/37/39/41/81/82/83/84/85/86 | 5268 duplicados exactos después del primero | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF086 | 23/33/37/39/41/81/82/83/84/85/86 | No existe identificador de línea en los campos fuente | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF087 | 23/33/37/39/41/81/82/83/84/85/86 | La documentación no distingue duplicado de carga y repetición legítima | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF088 | 23/33/37/39/41/81/82/83/84/85/86 | 9288 líneas C | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF089 | 23/33/37/39/41/81/82/83/84/85/86 | 1,71% de líneas C | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF090 | 23/33/37/39/41/81/82/83/84/85/86 | 3836 facturas C distintas | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF091 | 23/33/37/39/41/81/82/83/84/85/86 | Mediana Quantity original igual a3 | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF092 | 23/33/37/39/41/81/82/83/84/85/86 | Q1 Quantity original igual a1 | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF093 | 23/33/37/39/41/81/82/83/84/85/86 | Q3 Quantity original igual a10 | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF094 | 23/33/37/39/41/81/82/83/84/85/86 | Mínimo Quantity de−80995 | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF095 | 23/33/37/39/41/81/82/83/84/85/86 | Máximo Quantity de80995 | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF096 | 23/33/37/39/41/81/82/83/84/85/86 | 10624 cantidades negativas | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF097 | 23/33/37/39/41/81/82/83/84/85/86 | Ninguna cantidad cero | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF098 | 23/33/37/39/41/81/82/83/84/85/86 | Mediana UnitPrice original de 2,08 GBP | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF099 | 23/33/37/39/41/81/82/83/84/85/86 | Mínimo UnitPrice de −11062,06 GBP | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF100 | 23/33/37/39/41/81/82/83/84/85/86 | Máximo UnitPrice de 38970 GBP | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF101 | 23/33/37/39/41/81/82/83/84/85/86 | Dos precios negativos | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF102 | 23/33/37/39/41/81/82/83/84/85/86 | 2515 precios cero | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF103 | 23/33/37/39/41/81/82/83/84/85/86 | Mediana importe original de9,75 GBP | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF104 | 23/33/37/39/41/81/82/83/84/85/86 | Mínimo importe de−168469,60 GBP | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF105 | 23/33/37/39/41/81/82/83/84/85/86 | Máximo importe de168469,60 GBP | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF106 | 23/33/37/39/41/81/82/83/84/85/86 | 9290 importes negativos | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF107 | 23/33/37/39/41/81/82/83/84/85/86 | 2515 importes cero | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF108 | 23/33/37/39/41/81/82/83/84/85/86 | 11805 líneas con cantidad o precio no positivo | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF109 | 23/33/37/39/41/81/82/83/84/85/86 | 9288 de esos casos corresponden a C | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF110 | 23/33/37/39/41/81/82/83/84/85/86 | 2517 de esos casos no son C | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF111 | 23/33/37/39/41/81/82/83/84/85/86 | Extremos alejados de cuantiles centrales | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF112 | 23/33/37/39/41/81/82/83/84/85/86 | 3385 apariciones de StockCode fuera del patrón numérico con letra opcional | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF113 | 23/33/37/39/41/81/82/83/84/85/86 | 113452 descripciones no ausentes tienen espacios periféricos | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF114 | 23/33/37/39/41/81/82/83/84/85/86 | Diciembre 2011 no cubre todo el mes calendario | R | STAT-002 a STAT-008, STAT-016, incidencias y evento16 |
| AF115 | 55/67/71 | Ranking por pares StockCode–Description | R | STAT-012/014, cinco PNG y evento16 |
| AF116 | 55/67/71 | Top diez pares suma10,80% del importe positivo | R | STAT-012/014, cinco PNG y evento16 |
| AF117 | 55/67/71 | DOT/DOTCOM POSTAGE es primer par monetario | R | STAT-012/014, cinco PNG y evento16 |
| AF118 | 55/67/71 | DOT/DOTCOM POSTAGE suma206248,77 GBP | R | STAT-012/014, cinco PNG y evento16 |
| AF119 | 55/67/71 | El ranking incluye M/Manual | R | STAT-012/014, cinco PNG y evento16 |
| AF120 | 55/67/71 | El ranking incluye POST/POSTAGE | R | STAT-012/014, cinco PNG y evento16 |
| AF121 | 55/67/71 | Los conceptos no son mercancías físicas homogéneas | R | STAT-012/014, cinco PNG y evento16 |
| AF122 | 55/67/71 | FIG-003 selecciona diez países | R | STAT-012/014, cinco PNG y evento16 |
| AF123 | 55/67/71 | Selección geográfica por suma de LineAmount descendente | R | STAT-012/014, cinco PNG y evento16 |
| AF124 | 55/67/71 | FIG-004 representa diez pares ordenados por importe | R | STAT-012/014, cinco PNG y evento16 |
| AF125 | 55/67/71 | Las descripciones visuales se truncan, manteniendo código | R | STAT-012/014, cinco PNG y evento16 |
| AF126 | 45/47/51/63/65/67/69/71/73/75/77/84 | FIG-002 representa Quantity positiva en log10 | R | FIG-001 a FIG-005 abiertas y evento16 |
| AF127 | 45/47/51/63/65/67/69/71/73/75/77/84 | FIG-002 representa UnitPrice positivo en log10 | R | FIG-001 a FIG-005 abiertas y evento16 |
| AF128 | 45/47/51/63/65/67/69/71/73/75/77/84 | Los histogramas muestran masa central y cola positiva sin recorte | R | FIG-001 a FIG-005 abiertas y evento16 |
| AF129 | 45/47/51/63/65/67/69/71/73/75/77/84 | FIG-001 separa importes mensuales positivos y cancelados | R | FIG-001 a FIG-005 abiertas y evento16 |
| AF130 | 45/47/51/63/65/67/69/71/73/75/77/84 | La serie temporal permite ver el máximo de noviembre2011 | R | FIG-001 a FIG-005 abiertas y evento16 |
| AF131 | 45/47/51/63/65/67/69/71/73/75/77/84 | La cobertura parcial del último mes se explica junto a la serie | R | FIG-001 a FIG-005 abiertas y evento16 |
| AF132 | 45/47/51/63/65/67/69/71/73/75/77/84 | FIG-003 muestra dominancia monetaria UK | R | FIG-001 a FIG-005 abiertas y evento16 |
| AF133 | 45/47/51/63/65/67/69/71/73/75/77/84 | FIG-004 muestra concentración por pares artículo y descripción | R | FIG-001 a FIG-005 abiertas y evento16 |
| AF134 | 45/47/51/63/65/67/69/71/73/75/77/84 | FIG-005 transforma cantidad mediante log10 | R | FIG-001 a FIG-005 abiertas y evento16 |
| AF135 | 45/47/51/63/65/67/69/71/73/75/77/84 | FIG-005 transforma precio mediante log10 | R | FIG-001 a FIG-005 abiertas y evento16 |
| AF136 | 45/47/51/63/65/67/69/71/73/75/77/84 | Hexbin expone densidad central sin eliminar extremos positivos | R | FIG-001 a FIG-005 abiertas y evento16 |
| AF137 | 45/47/51/63/65/67/69/71/73/75/77/84 | La densidad es compatible con asociación negativa | R | FIG-001 a FIG-005 abiertas y evento16 |
| AF138 | 45/47/51/63/65/67/69/71/73/75/77/84 | La figura no identifica mecanismos causales | R | FIG-001 a FIG-005 abiertas y evento16 |
| AF139 | 45/47/51/63/65/67/69/71/73/75/77/84 | Se utilizaron estadísticas robustas | R | FIG-001 a FIG-005 abiertas y evento16 |
| AF140 | 82/90/92/94/96/98/104/106 | La causa de las ausencias no está documentada | R | Diccionario público, STAT-002/003/009/011/012/014/015 e incidencias |
| AF141 | 82/90/92/94/96/98/104/106 | Los clientes identificados no representan automáticamente a los no identificados | R | Diccionario público, STAT-002/003/009/011/012/014/015 e incidencias |
| AF142 | 82/90/92/94/96/98/104/106 | C no especifica por sí solo el tratamiento contable final | R | Diccionario público, STAT-002/003/009/011/012/014/015 e incidencias |
| AF143 | 82/90/92/94/96/98/104/106 | La multiplicación no añade impuestos, descuentos o conciliaciones no documentados | R | Diccionario público, STAT-002/003/009/011/012/014/015 e incidencias |
| AF144 | 82/90/92/94/96/98/104/106 | Los grupos no tienen necesariamente exposiciones iguales | R | Diccionario público, STAT-002/003/009/011/012/014/015 e incidencias |
| AF145 | 82/90/92/94/96/98/104/106 | Las rarezas estadísticas no demuestran errores de captura | R | Diccionario público, STAT-002/003/009/011/012/014/015 e incidencias |
| AF146 | 82/90/92/94/96/98/104/106 | La eventual sobreestimación por duplicados se plantea condicionalmente | R | Diccionario público, STAT-002/003/009/011/012/014/015 e incidencias |
| AF147 | 82/90/92/94/96/98/104/106 | Concentración geográfica elevada en UK | R | Diccionario público, STAT-002/003/009/011/012/014/015 e incidencias |
| AF148 | 82/90/92/94/96/98/104/106 | Distribuciones asimétricas de Quantity | R | Diccionario público, STAT-002/003/009/011/012/014/015 e incidencias |
| AF149 | 82/90/92/94/96/98/104/106 | Distribuciones asimétricas de UnitPrice | R | Diccionario público, STAT-002/003/009/011/012/014/015 e incidencias |
| AF150 | 82/90/92/94/96/98/104/106 | Distribuciones asimétricas del importe | R | Diccionario público, STAT-002/003/009/011/012/014/015 e incidencias |
| AF151 | 82/90/92/94/96/98/104/106 | La conservación íntegra y el subconjunto positivo son poblaciones analíticas distintas | R | Diccionario público, STAT-002/003/009/011/012/014/015 e incidencias |