# Evaluación D2-CA-R3

**Índice final:** 82,19/100.  
**Evaluación cerrada:** 6 de octubre de 2026.  
**Ejecución:** `D2_online_retail__crewai__r03__20260902T212422402094Z`

**Criterios:** [Protocolo de evaluación](../01_protocolo_calidad_Q1_Q10_v0.1.md) y [guía D2](../02_ficha_D2_online_retail.md).  
**Resultados:** [Archivos originales de la ejecución](../../../outputs/experimento/D2_online_retail__crewai__r03__20260902T212422402094Z).  
**Evaluación:** [Excel de puntuaciones](../Evaluacion_calidad.xlsx) y [JSON de comprobaciones](D2-CA-R3_comprobaciones.json).

Las referencias `STAT`, `ISSUE` y `FIG` identifican análisis, problemas y figuras en los archivos de la ejecución. `TR` identifica transformaciones y `CHK`, comprobaciones de calidad. Las referencias a líneas corresponden al informe original, `report.md`.

## Resumen

| Métrica | Puntuación final |
| --- | ---: |
| Q1 Cumplimiento de las etapas | 100,00 |
| Q2 Corrección numérica | 76,60 |
| Q3 Validez del tratamiento de los datos | 83,33 |
| Q4 Detección de problemas y riesgos | 85,44 |
| Q5 Calidad y profundidad del EDA | 75,00 |
| Q6 Profundidad de la interpretación | 75,00 |
| Q7 Calidad de las visualizaciones | 65,00 |
| Q8 Cobertura del informe | 86,36 |
| Q9 Fidelidad del informe | 99,41 |
| Q10 Claridad y coherencia | 75,00 |

## Q1 Cumplimiento de las etapas: 100,00

Ocho etapas acreditadas:

| Etapa | Nota | Evidencia |
| --- | ---: | --- |
| E1 Carga e inspección inicial | 1 | STAT-001/005, documentación y plan |
| E2 Estructura, tipos y calidad | 1 | STAT-002–005/014, seis incidencias |
| E3 Preparación y decisiones de análisis | 1 | TR-001–004, STAT-006, CSV y evento16 |
| E4 Estadística descriptiva | 1 | STAT-004/007/008 |
| E5 Variables, agregaciones y relaciones | 1 | STAT-009–013 |
| E6 Visualizaciones | 1 | Cuatro PNG válidos |
| E7 Problemas, riesgos y anomalías | 1 | Seis ISSUE con evidencias, decisiones y consecuencias |
| E8 Informe final | 1 | Alcance, preparación, hallazgos y límites integrados |

`Q1 = 100 x 8 / 8 = 100,00`

## Q2 Corrección numérica: 76,60

Se cumplen 24 de las 32 comprobaciones previstas, que suman 36 de los 47 puntos ponderados.

| Controles | Resultado | Evidencia o motivo |
| --- | --- | --- |
| C01–C07 | Correctos | Estructura, fechas y ausencias. El total de celdas ausentes se obtiene sumando los recuentos por columna de STAT-002. |
| C08 | Ausente | No presenta cuántos registros tienen ausentes simultáneamente CustomerID y Description. |
| C09 | Correcto | 5268 duplicados, STAT-003 |
| C10 | Correcto | Los 541.909 registros originales menos los 5.268 duplicados dan 536.641 registros. STAT-001 y STAT-003. |
| C11–C17 | Correctos | STAT-003/004/005/007 |
| C18 | Ausente | No presenta cuántos registros tienen cantidad negativa sin marca de cancelación. Tampoco aporta información suficiente para reconstruir ese recuento. |
| C19–C25 | Correctos | STAT-004/007/013 |
| C26 | Ausente | Presenta el importe de los registros sin marca de cancelación, pero no el de las ventas positivas, que exige cantidades y precios mayores que cero. |
| C27 | Correcto | -896812,49 GBP, STAT-008 |
| C28 | Ausente | No presenta el importe neto después de excluir los duplicados exactos. |
| C29 | Ausente | Presenta los recuentos del Reino Unido y del conjunto completo, pero no su porcentaje. |
| C30 | Ausente | Identifica el máximo mensual del importe neto, no el de las ventas positivas. |
| C31 | Ausente | Identifica 650 códigos con varias descripciones originales, pero no los 647 obtenidos después de eliminar espacios iniciales y finales y convertir las descripciones a mayúsculas. |
| C32 | Ausente | No presenta la mediana del número de registros por factura. |

`Q2 = 100 x 36 / 47 = 76,60`

## Q3 Validez del tratamiento de los datos: 83,33

| Decisión | Nota | Justificación y evidencia |
| --- | ---: | --- |
| D01 Identificadores | 1 | Texto nominal, valores y ausencias conservados, TR-001 |
| D02 Fecha-hora | 1 | El CSV conserva la fecha y la hora de todos los registros en formato ISO 8601. TR-002. |
| D03 Importe | 1 | Identidad y filtros declarados, STAT-007–013 |
| D04 Unidades | 1 | Distingue líneas, facturas, clientes y conceptos |
| D05 Cancelaciones | 1 | Identifica las cancelaciones por el prefijo C y presenta sus resultados por separado. STAT-008. |
| D06 Cliente ausente | 1 | Conserva las filas en los análisis generales y limita los análisis de clientes a los registros con identificador disponible. STAT-012. |
| D07 Descripción ausente | 1 | Sin imputación ni descripción inventada |
| D08 Duplicados | 0 | Conserva los duplicados, pero no compara los resultados con y sin esas filas. |
| D09 Ajustes | 0 | Cuantifica los precios cero y negativos, pero no identifica ni examina por separado las cantidades negativas sin marca de cancelación. |
| D10 Extremos | 1 | Retiene y usa cuantiles, IQR y escala logarítmica |
| D11 Mes final | 1 | Advierte explícitamente que diciembre 2011 termina el día9 |
| D12 Categorías | 1 | Conserva el detalle original y limita los gráficos a los conceptos principales, identificados mediante sus códigos. |

`Q3 = 100 x 10 / 12 = 83,33`

## Q4 Detección de problemas y riesgos: 85,44

Se detectan por completo ocho de los diez riesgos de referencia (K = 8), se identifican tres riesgos adicionales válidos (A = 3) y se registra una afirmación sin respaldo suficiente (F = 1). Once de los doce hallazgos son válidos, lo que da una precisión del 91,67 %, mientras que la cobertura de los riesgos de referencia es del 80 %. Ambas medidas se combinan mediante F1 para obtener la puntuación de Q4.

| Riesgo | Resultado | Evidencia |
| --- | --- | --- |
| R01 Ausencias | Detectado | STAT-002, ISSUE-001/002 |
| R02 Duplicados | Detectado | STAT-003, ISSUE-003 |
| R03 C y negativos | Detectado | STAT-008, informe5/53, signos contrastados |
| R04 Negativos sin C | No acreditado | No se aíslan como riesgo distinto. Conteos generales no bastan |
| R05 Precios cero y negativos | Detectado | STAT-004 corregido, informe93 |
| R06 Unidad e identificadores | Detectado | Informe15/23/39/63, perfil y TR-001 |
| R07 Mes final parcial | Detectado | STAT-005, ISSUE-004, informe17/59 |
| R08 Concentración UK | Detectado | STAT-005/010, informe7/61 |
| R09 Asimetría y extremos | Detectado | STAT-004/014, ISSUE-005 |
| R10 Definiciones monetarias | Parcial | Neto y C diferenciados, sin positivo agregado ni deduplicación |
| A01 Varias descripciones para un mismo código | Adicional válido | Identifica 650 códigos asociados a varias descripciones originales. ISSUE-006 |
| A02 Códigos de gastos de envío y operaciones manuales | Adicional válido | Las líneas 63/85 del informe explican que estos conceptos no son productos físicos |
| A03 Cancelaciones sin vinculación a ventas previas | Adicional válido | Las líneas 53/98/100 del informe explican que no puede vincularse cada cancelación con una venta original |
| F01 Diciembre 2010 incompleto | Sin respaldo | ISSUE-004 e informe7/59/73/92/104. Inicio el día1 no acredita truncamiento |

`Q4 = 100 x [2 x (11 / 12) x (8 / 10)] / [(11 / 12) + (8 / 10)] = 85,44`

## Q5 Calidad y profundidad del EDA: 75,00

El análisis examina la evolución temporal, países, conceptos facturados, clientes, distribuciones, valores extremos y asociaciones mediante Spearman. Recibe 3 de 4 puntos porque no cuantifica el efecto de excluir duplicados, no examina por separado las cantidades negativas sin marca de cancelación y no completa la comparación entre importes netos y ventas positivas.

Evidencia: STAT-004/007–014.

`Q5 = 100 x 3 / 4 = 75,00`

## Q6 Profundidad de la interpretación: 75,00

El informe interpreta la concentración geográfica, la influencia de los extremos, los signos y las limitaciones del análisis de clientes. También distingue las cancelaciones de su posible vinculación con ventas previas. Recibe 3 de 4 puntos porque afirma sin respaldo suficiente que diciembre de 2010 está incompleto.

Evidencia: informe líneas 51/53/59/61/63/65/67/89–104.

`Q6 = 100 x 3 / 4 = 75,00`

## Q7 Calidad de las visualizaciones: 65,00

Las puntuaciones 4, 0, 3, 2 y 4 suman 13/20, equivalentes a 65,00.

| Objetivo | Nota 0–4 | Justificación |
| --- | ---: | --- |
| V01 Evolución | 4 | FIG-001 neta mensual clara, unidades y definición explícitas. Mes final explicado en el informe |
| V02 Cancelaciones/ajustes | 0 | Ninguna figura representa su frecuencia o magnitud separadamente |
| V03 Distribuciones | 3 | FIG-003 muestra las cantidades entre 1 y 50 y la distribución completa de precios positivos en escala logarítmica. No representa precios cero o negativos |
| V04 Países | 2 | FIG-002 representa correctamente los importes, pero el valor del Reino Unido dificulta comparar los demás países |
| V05 Conceptos | 4 | FIG-004 muestra los diez conceptos con mayor importe sin marca de cancelación, con códigos legibles. El informe explica la presencia de gastos de envío y operaciones manuales |

`Q7 = 100 x 13 / 20 = 65,00`

## Q8 Cobertura del informe: 86,36

| Unidad | Peso | Nota | Evidencia o motivo |
| --- | ---: | ---: | --- |
| U01 Estructura y periodo | 2 | 1 | Informe3/13/17/21 |
| U02 Ausencias e impacto | 2 | 1 | Informe33/89/90 |
| U03 Unidades | 2 | 1 | Informe15/39/53/63/67 |
| U04 Duplicados y decisión | 2 | 1 | Informe35/91 |
| U05 C y negativos | 2 | 1 | Informe5/53/93 |
| U06 Ajustes | 2 | 0,5 | Comunica precios cero y negativos, pero no identifica por separado las cantidades negativas sin marca de cancelación |
| U07 Agregados monetarios | 2 | 0,5 | Distingue los importes netos, los de registros sin marca de cancelación y los de cancelaciones. Faltan el importe de las ventas positivas y el efecto de excluir duplicados |
| U08 Evolución y mes final | 2 | 0,5 | Describe la evolución y la cobertura incompleta de diciembre de 2011, pero no comunica el máximo mensual de las ventas positivas |
| U09 Concentración UK | 2 | 1 | Informe7/61/77, con advertencia de tamaños desiguales |
| U10 Cardinalidad y conceptos | 1 | 1 | Informe39/63/85/94 explica códigos, gastos de envío y operaciones manuales |
| U11 Asimetría y extremos | 2 | 1 | Informe41–51/63/81/93 |
| U12 Cobertura y límites | 1 | 1 | Informe17/89–104 identifica una empresa, periodo y límites de ausencias/ajustes/duplicados |

`Q8 = 100 x 19 / 22 = 86,36`

## Q9 Fidelidad del informe: 99,41

Se respaldan 169 de las 170 afirmaciones evaluadas. AF170 carece de respaldo suficiente porque el informe presenta diciembre de 2010 como incompleto sin evidencia que permita demostrarlo.

El inventario situado al final de esta ficha recoge las afirmaciones revisadas, su clasificación y las evidencias utilizadas.

`Q9 = 100 x 169 / 170 = 99,41`

## Q10 Claridad y coherencia: 75,00

El informe presenta una estructura organizada, referencias localizables y definiciones de los filtros utilizados. Recibe 3 de 4 puntos porque repite hallazgos en varias secciones, explica de forma incompleta algunas variables y afirma S que diciembre de 2010 está incompleto.

`Q10 = 100 x 3 / 4 = 75,00`

## Inventario de afirmaciones

R = respaldada; S = sin respaldo suficiente.

| ID | Líneas | Afirmación | Clasificación | Evidencia |
| --- | --- | --- | --- | --- |
| AF001 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | 541909 líneas originales | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF002 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | Periodo desde 2010-12-01 | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF003 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | Periodo hasta2011-12-09 | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF004 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | Todas las líneas conservadas | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF005 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | Tres derivadas añadidas | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF006 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | IsCancellation indica prefijo C | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF007 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | LineAmount=QuantityxUnitPrice | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF008 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | YearMonth deriva de fecha | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF009 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | Entrada XLSX hoja Online Retail | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF010 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | Ocho columnas fuente | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF011 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | Listado de ocho variables fuente correcto | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF012 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | Fuente no modificada | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF013 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | Fila es línea de factura | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF014 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | Fila no equivale necesariamente a factura completa | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF015 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | Fila no equivale necesariamente a compra completa | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF016 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | Fila no equivale a cliente | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF017 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | InvoiceNo nominal | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF018 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | StockCode nominal | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF019 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | CustomerID nominal | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF020 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | 305 fechas distintas con actividad | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF021 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | Análisis limitado a una empresa | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF022 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | No se infiere a otros negocios | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF023 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | No se infiere a otros años | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF024 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | No se infiere a otras poblaciones | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF025 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | Once columnas preparadas | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF026 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | Ninguna observación eliminada | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF027 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | Tres identificadores normalizados como texto | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF028 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | CustomerID serializado sin sufijo decimal | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF029 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | InvoiceDate conserva fecha y hora | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF030 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | Fecha-hora CSV ISO8601 | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF031 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | Primera fecha-hora2010-12-01T08:26:00 | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF032 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | Última fecha-hora2011-12-09T12:50:00 | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF033 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | Identidad de importe comprobada para todas las líneas | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF034 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | Diferencia absoluta máxima de identidad cero | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF035 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | No se imputaron ausencias | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF036 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | No se eliminaron duplicados | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF037 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | No se eliminaron extremos | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF038 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | No se eliminaron negativos | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF039 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | Agregados netos incluyen C y no C | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF040 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | Importe deriva de campos disponibles | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF041 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | No se incorpora información externa de impuestos | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF042 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | No se incorpora información externa de gastos adicionales | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF043 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | No se incorpora información externa de descuentos adicionales | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF044 | 3/13/15/17/21/23/27/28/29/31/33/35/98/110/112 | No se emparejan C con venta original | R | STAT-001/006/013, TR-001–004, CSV, evento16 y diccionario |
| AF045 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Importe neto9747747,93 GBP | R | STAT-002–014 contrastados con entrada y código |
| AF046 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Unidades netas5176450 | R | STAT-002–014 contrastados con entrada y código |
| AF047 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | 9288 líneas C | R | STAT-002–014 contrastados con entrada y código |
| AF048 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | C1,71% de líneas | R | STAT-002–014 contrastados con entrada y código |
| AF049 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Importe C-896812,49 GBP | R | STAT-002–014 contrastados con entrada y código |
| AF050 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Importe no C10644560,42 GBP | R | STAT-002–014 contrastados con entrada y código |
| AF051 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | UK495478 líneas | R | STAT-002–014 contrastados con entrada y código |
| AF052 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | UK84,00% del importe neto | R | STAT-002–014 contrastados con entrada y código |
| AF053 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Noviembre2011 máximo mensual neto | R | STAT-002–014 contrastados con entrada y código |
| AF054 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Noviembre neto1461756,25 GBP | R | STAT-002–014 contrastados con entrada y código |
| AF055 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | CustomerID ausente135080 líneas | R | STAT-002–014 contrastados con entrada y código |
| AF056 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | CustomerID ausente24,93% | R | STAT-002–014 contrastados con entrada y código |
| AF057 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Description ausente1454 líneas | R | STAT-002–014 contrastados con entrada y código |
| AF058 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Description ausente0,268% | R | STAT-002–014 contrastados con entrada y código |
| AF059 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | 5268 duplicados exactos | R | STAT-002–014 contrastados con entrada y código |
| AF060 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Duplicados0,97% | R | STAT-002–014 contrastados con entrada y código |
| AF061 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | 25900 facturas distintas | R | STAT-002–014 contrastados con entrada y código |
| AF062 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | 4070 códigos distintos | R | STAT-002–014 contrastados con entrada y código |
| AF063 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | 4223 descripciones distintas | R | STAT-002–014 contrastados con entrada y código |
| AF064 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | 4372 clientes identificados | R | STAT-002–014 contrastados con entrada y código |
| AF065 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | 38 países | R | STAT-002–014 contrastados con entrada y código |
| AF066 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | 99% de Quantity no supera100 | R | STAT-002–014 contrastados con entrada y código |
| AF067 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Quantity máxima80995 | R | STAT-002–014 contrastados con entrada y código |
| AF068 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | C unidades-277574 | R | STAT-002–014 contrastados con entrada y código |
| AF069 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | C mediana cantidad-2 | R | STAT-002–014 contrastados con entrada y código |
| AF070 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | C mediana importe-8,50 GBP | R | STAT-002–014 contrastados con entrada y código |
| AF071 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | 532621 líneas no C | R | STAT-002–014 contrastados con entrada y código |
| AF072 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | No C unidades5454024 | R | STAT-002–014 contrastados con entrada y código |
| AF073 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | No C mediana importe9,90 GBP | R | STAT-002–014 contrastados con entrada y código |
| AF074 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Septiembre2011 neto1019687,62 GBP | R | STAT-002–014 contrastados con entrada y código |
| AF075 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Octubre2011 neto1070704,67 GBP | R | STAT-002–014 contrastados con entrada y código |
| AF076 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Neto aumenta septiembre–noviembre2011 | R | STAT-002–014 contrastados con entrada y código |
| AF077 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Noviembre84711 líneas | R | STAT-002–014 contrastados con entrada y código |
| AF078 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Noviembre3462 facturas | R | STAT-002–014 contrastados con entrada y código |
| AF079 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Noviembre máximo de líneas | R | STAT-002–014 contrastados con entrada y código |
| AF080 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Noviembre máximo de facturas | R | STAT-002–014 contrastados con entrada y código |
| AF081 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Diciembre 2010 tiene42481 líneas | R | STAT-002–014 contrastados con entrada y código |
| AF082 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Diciembre 2011 tiene25525 líneas | R | STAT-002–014 contrastados con entrada y código |
| AF083 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Diciembre 2011 termina el día9 | R | STAT-002–014 contrastados con entrada y código |
| AF084 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Diciembre 2011 parcial | R | STAT-002–014 contrastados con entrada y código |
| AF085 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | UK neto8187806,36 GBP | R | STAT-002–014 contrastados con entrada y código |
| AF086 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | UK unidades4263829 | R | STAT-002–014 contrastados con entrada y código |
| AF087 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | UK23494 facturas | R | STAT-002–014 contrastados con entrada y código |
| AF088 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Netherlands segundo por neto | R | STAT-002–014 contrastados con entrada y código |
| AF089 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Netherlands neto284661,54 GBP | R | STAT-002–014 contrastados con entrada y código |
| AF090 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | EIRE tercero por neto | R | STAT-002–014 contrastados con entrada y código |
| AF091 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | EIRE neto263276,82 GBP | R | STAT-002–014 contrastados con entrada y código |
| AF092 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Germany cuarto por neto | R | STAT-002–014 contrastados con entrada y código |
| AF093 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Germany neto221698,21 GBP | R | STAT-002–014 contrastados con entrada y código |
| AF094 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | France quinto por neto | R | STAT-002–014 contrastados con entrada y código |
| AF095 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | France neto197403,90 GBP | R | STAT-002–014 contrastados con entrada y código |
| AF096 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Ranking de conceptos usa líneas no C | R | STAT-002–014 contrastados con entrada y código |
| AF097 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Par DOT DOTCOM POSTAGE primero por importe | R | STAT-002–014 contrastados con entrada y código |
| AF098 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Par DOT importe206248,77 GBP | R | STAT-002–014 contrastados con entrada y código |
| AF099 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Par22423 REGENCY CAKESTAND segundo | R | STAT-002–014 contrastados con entrada y código |
| AF100 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Par22423 importe174484,74 GBP | R | STAT-002–014 contrastados con entrada y código |
| AF101 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Par23843 PAPER CRAFT importe168469,60 GBP | R | STAT-002–014 contrastados con entrada y código |
| AF102 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Par23843 una línea | R | STAT-002–014 contrastados con entrada y código |
| AF103 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Par23843 80995 unidades | R | STAT-002–014 contrastados con entrada y código |
| AF104 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Par23843 influye en ranking y extremos | R | STAT-002–014 contrastados con entrada y código |
| AF105 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Ranking mezcla artículos y portes | R | STAT-002–014 contrastados con entrada y código |
| AF106 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Ranking incluye entradas Manual | R | STAT-002–014 contrastados con entrada y código |
| AF107 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Código no equivale siempre a producto físico | R | STAT-002–014 contrastados con entrada y código |
| AF108 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | 530104 líneas no C con Quantity y UnitPrice positivos | R | STAT-002–014 contrastados con entrada y código |
| AF109 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Spearman Quantity–UnitPrice-0,403 | R | STAT-002–014 contrastados con entrada y código |
| AF110 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Asociación monotónica negativa moderada | R | STAT-002–014 contrastados con entrada y código |
| AF111 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Análisis por cliente solo con identificador | R | STAT-002–014 contrastados con entrada y código |
| AF112 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Cliente14646 mayor neto identificado | R | STAT-002–014 contrastados con entrada y código |
| AF113 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Cliente14646 neto279489,02 GBP | R | STAT-002–014 contrastados con entrada y código |
| AF114 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Cliente14646 77 facturas | R | STAT-002–014 contrastados con entrada y código |
| AF115 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Cliente18102 segundo neto identificado | R | STAT-002–014 contrastados con entrada y código |
| AF116 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Cliente18102 neto256438,49 GBP | R | STAT-002–014 contrastados con entrada y código |
| AF117 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Cliente18102 62 facturas | R | STAT-002–014 contrastados con entrada y código |
| AF118 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | 10624 cantidades negativas | R | STAT-002–014 contrastados con entrada y código |
| AF119 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | 9290 importes negativos | R | STAT-002–014 contrastados con entrada y código |
| AF120 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | 2515 precios cero | R | STAT-002–014 contrastados con entrada y código |
| AF121 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Dos precios negativos | R | STAT-002–014 contrastados con entrada y código |
| AF122 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | IQR Quantity58619 fuera de vallas | R | STAT-002–014 contrastados con entrada y código |
| AF123 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | IQR UnitPrice39627 fuera de vallas | R | STAT-002–014 contrastados con entrada y código |
| AF124 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | IQR LineAmount44997 fuera de vallas | R | STAT-002–014 contrastados con entrada y código |
| AF125 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | 650 códigos con varias descripciones literales | R | STAT-002–014 contrastados con entrada y código |
| AF126 | 5/7/9/33/39/51/53/57/59/61/63/65/67/89/90/91/93/94/108 | Rankings agrupados por pareja código–descripción | R | STAT-002–014 contrastados con entrada y código |
| AF127 | 43–49 | Quantity completa mediana=3.0 | R | STAT-004/007, tabla del informe |
| AF128 | 43–49 | Quantity completa media=9.55 | R | STAT-004/007, tabla del informe |
| AF129 | 43–49 | Quantity completa P99=100.0 | R | STAT-004/007, tabla del informe |
| AF130 | 43–49 | Quantity completa mínimo=-80995.0 | R | STAT-004/007, tabla del informe |
| AF131 | 43–49 | UnitPrice completa mediana=2.08 | R | STAT-004/007, tabla del informe |
| AF132 | 43–49 | UnitPrice completa media=4.61 | R | STAT-004/007, tabla del informe |
| AF133 | 43–49 | UnitPrice completa P99=18.0 | R | STAT-004/007, tabla del informe |
| AF134 | 43–49 | UnitPrice completa mínimo=-11062.06 | R | STAT-004/007, tabla del informe |
| AF135 | 43–49 | UnitPrice completa máximo=38970.0 | R | STAT-004/007, tabla del informe |
| AF136 | 43–49 | LineAmount completa mediana=9.75 | R | STAT-004/007, tabla del informe |
| AF137 | 43–49 | LineAmount completa media=17.99 | R | STAT-004/007, tabla del informe |
| AF138 | 43–49 | LineAmount completa P99=180.0 | R | STAT-004/007, tabla del informe |
| AF139 | 43–49 | LineAmount completa mínimo=-168469.6 | R | STAT-004/007, tabla del informe |
| AF140 | 43–49 | LineAmount completa máximo=168469.6 | R | STAT-004/007, tabla del informe |
| AF141 | 71/73/75/77/79/81/83/85 | FIG-001 muestra neto mensual | R | Cuatro PNG inspeccionados y código evento16 |
| AF142 | 71/73/75/77/79/81/83/85 | FIG-001 incluye cancelaciones | R | Cuatro PNG inspeccionados y código evento16 |
| AF143 | 71/73/75/77/79/81/83/85 | FIG-002 compara diez países principales por neto | R | Cuatro PNG inspeccionados y código evento16 |
| AF144 | 71/73/75/77/79/81/83/85 | UK domina figura geográfica | R | Cuatro PNG inspeccionados y código evento16 |
| AF145 | 71/73/75/77/79/81/83/85 | FIG-003 muestra Quantity central1–50 | R | Cuatro PNG inspeccionados y código evento16 |
| AF146 | 71/73/75/77/79/81/83/85 | FIG-003 muestra UnitPrice positivo en log10 | R | Cuatro PNG inspeccionados y código evento16 |
| AF147 | 71/73/75/77/79/81/83/85 | La escala del precio no recorta su cola positiva | R | Cuatro PNG inspeccionados y código evento16 |
| AF148 | 71/73/75/77/79/81/83/85 | Recorte Quantity solo gráfico, no CSV ni cálculos | R | Cuatro PNG inspeccionados y código evento16 |
| AF149 | 71/73/75/77/79/81/83/85 | FIG-004 muestra conceptos principales por importe no C | R | Cuatro PNG inspeccionados y código evento16 |
| AF150 | 71/73/75/77/79/81/83/85 | FIG-004 incluye DOTCOM POSTAGE | R | Cuatro PNG inspeccionados y código evento16 |
| AF151 | 71/73/75/77/79/81/83/85 | FIG-004 incluye POSTAGE | R | Cuatro PNG inspeccionados y código evento16 |
| AF152 | 71/73/75/77/79/81/83/85 | FIG-004 incluye Manual | R | Cuatro PNG inspeccionados y código evento16 |
| AF153 | 9/33/35/51/61/65/89/90/91/92/93/98/100/102/104/112 | Ausencia CustomerID limita representatividad de resultados por cliente | R | ISSUE-001–006, diccionario, campos y operaciones |
| AF154 | 9/33/35/51/61/65/89/90/91/92/93/98/100/102/104/112 | Imputar cliente inventaría asociación no observada | R | ISSUE-001–006, diccionario, campos y operaciones |
| AF155 | 9/33/35/51/61/65/89/90/91/92/93/98/100/102/104/112 | No se infirió descripción desde StockCode | R | ISSUE-001–006, diccionario, campos y operaciones |
| AF156 | 9/33/35/51/61/65/89/90/91/92/93/98/100/102/104/112 | Código puede tener varias descripciones | R | ISSUE-001–006, diccionario, campos y operaciones |
| AF157 | 9/33/35/51/61/65/89/90/91/92/93/98/100/102/104/112 | No se confirma origen técnico o comercial de duplicados | R | ISSUE-001–006, diccionario, campos y operaciones |
| AF158 | 9/33/35/51/61/65/89/90/91/92/93/98/100/102/104/112 | No hay calendario operativo | R | ISSUE-001–006, diccionario, campos y operaciones |
| AF159 | 9/33/35/51/61/65/89/90/91/92/93/98/100/102/104/112 | No se normalizó por días | R | ISSUE-001–006, diccionario, campos y operaciones |
| AF160 | 9/33/35/51/61/65/89/90/91/92/93/98/100/102/104/112 | Tamaños de grupo geográfico desiguales | R | ISSUE-001–006, diccionario, campos y operaciones |
| AF161 | 9/33/35/51/61/65/89/90/91/92/93/98/100/102/104/112 | Extremos pueden afectar medias y totales | R | ISSUE-001–006, diccionario, campos y operaciones |
| AF162 | 9/33/35/51/61/65/89/90/91/92/93/98/100/102/104/112 | Correlación no demuestra causalidad | R | ISSUE-001–006, diccionario, campos y operaciones |
| AF163 | 9/33/35/51/61/65/89/90/91/92/93/98/100/102/104/112 | Correlación no demuestra mecanismo de precios | R | ISSUE-001–006, diccionario, campos y operaciones |
| AF164 | 9/33/35/51/61/65/89/90/91/92/93/98/100/102/104/112 | Regla C no determina motivo comercial | R | ISSUE-001–006, diccionario, campos y operaciones |
| AF165 | 9/33/35/51/61/65/89/90/91/92/93/98/100/102/104/112 | No hay emparejamiento C–venta original en la evidencia | R | ISSUE-001–006, diccionario, campos y operaciones |
| AF166 | 9/33/35/51/61/65/89/90/91/92/93/98/100/102/104/112 | IQR no confirma error por sí solo | R | ISSUE-001–006, diccionario, campos y operaciones |
| AF167 | 9/33/35/51/61/65/89/90/91/92/93/98/100/102/104/112 | Signos no positivos no confirman error por sí solos | R | ISSUE-001–006, diccionario, campos y operaciones |
| AF168 | 9/33/35/51/61/65/89/90/91/92/93/98/100/102/104/112 | La documentación no clasifica todos los extremos ni ajustes | R | ISSUE-001–006, diccionario, campos y operaciones |
| AF169 | 9/33/35/51/61/65/89/90/91/92/93/98/100/102/104/112 | Mes final requiere cautela frente a meses completos | R | ISSUE-001–006, diccionario, campos y operaciones |
| AF170 | 7/59/73/92/104 | Diciembre 2010 es incompleto por ser frontera temporal | S | STAT-005 e ISSUE-004 repiten la inferencia. Inicio el día1 sin calendario no acredita truncamiento. |