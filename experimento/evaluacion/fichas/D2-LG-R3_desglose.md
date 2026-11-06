# Evaluación D2-LG-R3

**Índice final:** 83,83/100.  
**Evaluación cerrada:** 6 de octubre de 2026.  
**Ejecución:** `D2_online_retail__langgraph__r03__20260902T200956928988Z`

**Criterios:** [Protocolo de evaluación](../01_protocolo_calidad_Q1_Q10_v0.1.md) y [guía D2](../02_ficha_D2_online_retail.md).  
**Resultados:** [Archivos originales de la ejecución](../../../outputs/experimento/D2_online_retail__langgraph__r03__20260902T200956928988Z).  
**Evaluación:** [Excel de puntuaciones](../Evaluacion_calidad.xlsx) y [JSON de comprobaciones](D2-LG-R3_comprobaciones.json).

Las referencias `STAT`, `ISSUE` y `FIG` identifican análisis, problemas y figuras en los archivos de la ejecución. `TR` identifica transformaciones y `CHK`, comprobaciones de calidad. Las referencias a líneas corresponden al informe original, `report.md`.

## Resumen

| Métrica | Puntuación final |
| --- | ---: |
| Q1 Cumplimiento de las etapas | 100,00 |
| Q2 Corrección numérica | 82,98 |
| Q3 Validez del tratamiento de los datos | 83,33 |
| Q4 Detección de problemas y riesgos | 88,89 |
| Q5 Calidad y profundidad del EDA | 75,00 |
| Q6 Profundidad de la interpretación | 75,00 |
| Q7 Calidad de las visualizaciones | 70,00 |
| Q8 Cobertura del informe | 84,09 |
| Q9 Fidelidad del informe | 100,00 |
| Q10 Claridad y coherencia | 75,00 |

## Q1 Cumplimiento de las etapas: 100,00

Las ocho etapas tienen evidencia válida:

| Etapa | Nota | Evidencia |
| --- | ---: | --- |
| E1 Carga e inspección inicial | 1 | STAT-001, perfil y documentación consultada |
| E2 Estructura, tipos y calidad | 1 | STAT-002–006 |
| E3 Preparación y decisiones de análisis | 1 | CSV, TR-001–004 y STAT-007 |
| E4 Estadística descriptiva | 1 | STAT-005/008/009/010 |
| E5 Variables, agregaciones y relaciones | 1 | STAT-011–015 |
| E6 Visualizaciones | 1 | Cinco PNG válidos e integrados |
| E7 Problemas, riesgos y anomalías | 1 | Seis comprobaciones y cinco incidencias |
| E8 Informe final | 1 | Alcance, preparación, resultados y límites |

`Q1 = 100 x 8 / 8 = 100,00`

## Q2 Corrección numérica: 82,98

Se cumplen 26 de las 32 comprobaciones previstas, que suman 39 de los 47 puntos ponderados.

| Controles | Resultado | Evidencia o motivo |
| --- | --- | --- |
| C01–C07 | Correctos | Estructura, fechas y ausencias. STAT-001/002/004 |
| C08 | Ausente | No presenta cuántos registros tienen ausentes simultáneamente CustomerID y Description |
| C09 | Correcto | 5268 duplicados después del primero. STAT-003 |
| C10 | Correcto | Los 541.909 registros originales menos los 5.268 duplicados dan 536.641 registros. STAT-001 y STAT-003 |
| C11–C17 | Correctos | Entidades, líneas y facturas C, Quantity negativa. STAT-003/005/006/008/012 |
| C18 | Correcto | Hay 10.624 registros con cantidad negativa y 9.288 cancelaciones, todas con cantidad negativa. La resta permite obtener 1.336 registros con cantidad negativa sin marca de cancelación. STAT-005 y STAT-009 |
| C19–C25 | Correctos | Precios, Quantity, neto y conteo positivo. STAT-005/015 |
| C26 | Ausente | No presenta el importe de las ventas positivas. Los 10.644.560,424 GBP comunicados corresponden a los registros sin marca de cancelación, que también incluyen cantidades o precios no positivos |
| C27 | Correcto | Cancelaciones −896812,49 GBP. STAT-009/012 |
| C28 | Ausente | No presenta el importe neto después de excluir los duplicados exactos |
| C29 | Ausente | Presenta 495.478 registros del Reino Unido y 541.909 registros totales, pero no su porcentaje. El porcentaje monetario comunicado es una medida diferente |
| C30 | Ausente | Identifica el máximo mensual del importe neto, no el de las ventas positivas |
| C31 | Correcto | 647 códigos multidescripción normalizada. STAT-006 |
| C32 | Ausente | Presenta el número de facturas por cliente, pero no el número de registros por factura |

`Q2 = 100 x 39 / 47 = 82,98`

## Q3 Validez del tratamiento de los datos: 83,33

| Decisión | Nota | Justificación y evidencia |
| --- | ---: | --- |
| D01 Identificadores | 1 | Identificadores como texto, con sus valores conservados. TR-001 |
| D02 Fecha-hora | 1 | CSV conserva fecha y hora fila a fila |
| D03 Importe | 1 | Identidad correcta y agregados netos, regulares y C definidos. STAT-005/009/012 |
| D04 Unidades | 1 | Distingue líneas, facturas, pares de artículos y clientes. STAT-008/013/014 |
| D05 Cancelaciones | 1 | C identificado, conservado y analizado por separado. STAT-009/012 |
| D06 Cliente ausente | 1 | Retiene filas globales y restringe clientes a identificadores presentes. STAT-014 |
| D07 Descripción ausente | 1 | Conserva ausencias, sin inventar texto. TR-002 |
| D08 Duplicados | 0 | Conserva los duplicados, pero no compara los resultados con y sin esas filas. ISSUE-002 |
| D09 Ajustes | 0 | Cuantifica los precios cero y negativos, pero no identifica ni examina por separado los registros con cantidad negativa sin marca de cancelación |
| D10 Extremos | 1 | Conserva extremos, cuantiles y escala logarítmica sin recorte. STAT-005/015, FIG-004 |
| D11 Mes final | 1 | Informa cierre del día 9 y advierte comparabilidad. Informe31/93 |
| D12 Categorías | 1 | Limita los gráficos a las categorías principales y conserva el detalle original. FIG-002/005 y STAT-010/013 |

`Q3 = 100 x 10 / 12 = 83,33`

## Q4 Detección de problemas y riesgos: 88,89

| Riesgo | Resultado | Evidencia |
| --- | --- | --- |
| R01 Ausencias | Detectado | STAT-002, ISSUE-001 |
| R02 Duplicados | Detectado | STAT-003, ISSUE-002 |
| R03 C y cantidades negativas | Detectado | STAT-009: Quantity máxima C = −1. Prefijo documentado en informe9 |
| R04 Negativos sin C | Parcial | STAT-009 regular contiene Quantity mínima −9600, sin conteo ni explicación específica |
| R05 Precios cero y negativos | Detectado | STAT-005 e informe41 |
| R06 Unidad e identificadores | Detectado | Perfil, TR-001 e informe3/25/35 |
| R07 Mes final hasta día 9 | Detectado | STAT-004, informe31/93 |
| R08 Concentración original UK | Detectado | 495478 líneas del total 541909 y advertencia de concentración. STAT-010, informe51 |
| R09 Asimetría y extremos | Detectado | STAT-005/009/014/015, ISSUE-003 |
| R10 Definiciones monetarias | Parcial | Neto, regulares y C, sin importe positivo ni efecto deduplicado |
| A01 Varias descripciones para un mismo código | Adicional válido | STAT-006, ISSUE-004 y líneas 59/91 del informe |
| A02 Cancelaciones sin vinculación a ventas previas | Adicional válido | Las líneas 49/99 del informe explican que no existe una relación verificable entre cada cancelación y una factura original |

Se detectan por completo ocho de los diez riesgos de referencia (K = 8) y se identifican dos riesgos adicionales válidos (A = 2), sin falsas alarmas (F = 0). Los diez hallazgos contabilizados son válidos, por lo que la precisión es del 100 %, mientras que la cobertura de los riesgos de referencia es del 80 %. Ambas medidas se combinan mediante F1 para obtener la puntuación de Q4.

`Q4 = 100 x [2 x 1 x (8 / 10)] / [1 + (8 / 10)] = 88,89`

## Q5 Calidad y profundidad del EDA: 75,00

El análisis examina distribuciones generales y por tipo de factura, evolución temporal, países, productos, clientes y asociaciones mediante Spearman. Recibe 3 de 4 puntos porque no compara los resultados con y sin duplicados, no examina por separado las cantidades negativas sin marca de cancelación y no completa la comparación de importes con las ventas positivas.

Evidencia: STAT-005 y STAT-009 a STAT-015.

`Q5 = 100 x 3 / 4 = 75,00`

## Q6 Profundidad de la interpretación: 75,00

El informe explica la influencia de una observación extrema en la clasificación de productos, las diferencias entre medias y medianas y las limitaciones del análisis de clientes y cancelaciones. Recibe 3 de 4 puntos porque no desarrolla suficientemente cómo cambian los importes según los registros incluidos ni el efecto de los ajustes.

Evidencia: líneas 43/49/53/55/57/99/111 del informe.

`Q6 = 100 x 3 / 4 = 75,00`

## Q7 Calidad de las visualizaciones: 70,00

| Objetivo | Nota 0–4 | Justificación |
| --- | ---: | --- |
| V01 Evolución | 4 | FIG-001 neta mensual, unidades claras y advertencia temporal integrada en el informe |
| V02 Cancelaciones/ajustes | 2 | FIG-003 compara el número de registros con y sin marca de cancelación, pero no representa por separado las cantidades negativas sin esa marca ni los precios cero o negativos |
| V03 Distribuciones | 3 | FIG-004 muestra Quantity y UnitPrice positivos completos en log, sin recortar P99. Faltan negativos o ceros |
| V04 Países | 2 | FIG-002 representa correctamente los importes, pero el valor del Reino Unido dificulta comparar los demás países |
| V05 Productos/conceptos/clientes | 3 | FIG-005 muestra las doce combinaciones de código y descripción con mayor importe. Las etiquetas indican que las descripciones están recortadas, pero no muestran los códigos |

`Q7 = 100 x 14 / 20 = 70,00`

## Q8 Cobertura del informe: 84,09

| Unidad | Peso | Nota | Evidencia o motivo |
| --- | ---: | ---: | --- |
| U01 Estructura y periodo | 2 | 1 | Informe3/15/23/31 |
| U02 Ausencias e impacto | 2 | 1 | Informe27/55/85/101 |
| U03 Unidades | 2 | 1 | Informe3/35/53/55 |
| U04 Duplicados y decisión | 2 | 1 | Informe29/87 |
| U05 C y negativos | 2 | 1 | Informe9/41/43 y FIG-003 |
| U06 Ajustes | 2 | 0,5 | Comunica los precios cero y negativos, pero no identifica específicamente las cantidades negativas sin marca de cancelación |
| U07 Agregados monetarios | 2 | 0,5 | Distingue el importe neto, el de los registros sin marca de cancelación y el de las cancelaciones. Faltan el importe de las ventas positivas y el efecto de excluir duplicados |
| U08 Evolución y máximo | 2 | 0,5 | Describe la evolución y advierte sobre la cobertura temporal, pero no identifica el máximo mensual de las ventas positivas |
| U09 Concentración UK | 2 | 1 | Informe11/51/69 contextualiza composición y concentración |
| U10 Cardinalidad y conceptos | 1 | 0,5 | Comunica el elevado número de códigos distintos e incluye DOTCOM POSTAGE, pero no explica que algunos códigos representan gastos de envío o ajustes en lugar de productos|
| U11 Asimetría y extremos | 2 | 1 | Informe37/39/53/55/77 |
| U12 Cobertura y límites | 1 | 1 | Empresa en informe17, período, ausencias e incertidumbre en31/87/93/99/101/103 |

`Q8 = 100 x 18,5 / 22 = 84,09`

## Q9 Fidelidad del informe: 100,00

Las 185 afirmaciones evaluadas cuentan con respaldo en las evidencias de la ejecución.

El inventario situado al final de esta ficha recoge las afirmaciones revisadas, su clasificación y las evidencias utilizadas.

`Q9 = 100 x 185 / 185 = 100,00`

## Q10 Claridad y coherencia: 75,00

El informe presenta una estructura ordenada y referencias claras. Recibe 3 de 4 puntos porque algunas variables no se explican suficientemente, el término "regular" depende de su definición previa y el gráfico de productos no muestra sus códigos.

`Q10 = 100 x 3 / 4 = 75,00`

## Inventario de afirmaciones

R = respaldada. Los localizadores son líneas del informe original. Las repeticiones sobre la misma población se cuentan una vez.

| ID | Líneas del informe | Afirmación | Estado | Evidencia |
| --- | --- | --- | --- | --- |
| AF001 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | 541909 líneas originales | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF002 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | 25900 InvoiceNo distintos originales | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF003 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | Una fila es una línea de factura | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF004 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | Una fila no es necesariamente una compra completa | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF005 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | Una factura no acredita necesariamente una compra completa | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF006 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | Primera fecha-hora 2010-12-01T08:26:00 | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF007 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | Última fecha-hora 2011-12-09T12:50:00 | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF008 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | Libro XLSX y hoja Online Retail | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF009 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | Ocho columnas originales | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF010 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | Lista de ocho campos fuente correcta | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF011 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | Empresa británica de comercio electrónico | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF012 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | Análisis descriptivo exploratorio | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF013 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | No se entrenaron modelos | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF014 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | No se realizaron inferencias causales | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF015 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | InvoiceDate original fecha-hora | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF016 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | Quantity original numérica | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF017 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | UnitPrice original numérica | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF018 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | Identificadores originales mixtos o nominales | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF019 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | Copia preparada conserva541909 líneas | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF020 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | Once columnas preparadas | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF021 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | Tres variables derivadas añadidas | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF022 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | IsCancellation identifica prefijo C | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF023 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | LineAmount=QuantityxUnitPrice | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF024 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | InvoiceMonth deriva del mes de InvoiceDate | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF025 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | InvoiceNo convertido a texto nominal | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF026 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | StockCode convertido a texto nominal | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF027 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | CustomerID convertido a texto nominal | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF028 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | CustomerID serializado sin sufijo decimal | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF029 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | Description recortada en espacios periféricos | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF030 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | Country recortado en espacios periféricos | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF031 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | No se imputaron identificadores | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF032 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | No se imputaron descripciones | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF033 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | No se eliminaron cancelaciones | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF034 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | No se eliminaron duplicados | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF035 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | No se eliminaron ausencias | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF036 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | No se eliminaron extremos | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF037 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | La repetición de InvoiceNo no se trata como duplicación | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF038 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | La repetición de StockCode no se trata como duplicación | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF039 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | La repetición de CustomerID no se trata como duplicación | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF040 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | No hay identificador propio independiente de línea | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF041 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | No hay regla documental de deduplicación | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF042 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | No se anualizaron importes | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF043 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | No se extrapolaron registros | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF044 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | LineAmount no acredita ingreso definitivo | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF045 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | LineAmount no acredita cobro confirmado | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF046 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | LineAmount no acredita rentabilidad | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF047 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | LineAmount no mide descuento confirmado | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF048 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | LineAmount no acredita envío confirmado | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF049 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | LineAmount no acredita valor final de compra | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF050 | 3/5/7/15/17/19/23/25/29/31/93/97/103/113 | Los agregados completos conservan signos, ceros y extremos | R | STAT-001/004/005/007, TR-001–004, CSV, evento 16 y diccionario público |
| AF051 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | C indica cancelación documentada | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF052 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | 9288 líneas C | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF053 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | C1,71% del total | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF054 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Importe C-896812,49 GBP | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF055 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | 532621 líneas sin C | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF056 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Importe sin C10644560,42 GBP | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF057 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Importe neto total9747747,93 GBP | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF058 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | UK neto8187806,36 GBP | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF059 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | UK84,0% del importe neto | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF060 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Noviembre2011 máximo mensual de líneas | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF061 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Noviembre84711 líneas | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF062 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Noviembre máximo mensual neto | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF063 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Noviembre neto1461756,25 GBP | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF064 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | CustomerID ausente135080 líneas | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF065 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | CustomerID ausente24,93% | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF066 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Description ausente1454 líneas | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF067 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Description ausente0,27% | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF068 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Sin ausencias InvoiceNo | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF069 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Sin ausencias StockCode | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF070 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Sin ausencias Quantity | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF071 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Sin ausencias InvoiceDate | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF072 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Sin ausencias UnitPrice | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF073 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Sin ausencias Country | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF074 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | 5268 duplicados después del primero | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF075 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Duplicados0,97% de líneas | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF076 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Ausencias de cliente limitan análisis por cliente | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF077 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Ausencias de descripción limitan agrupaciones descriptivas | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF078 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | 4070 StockCode distintos | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF079 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | 4372 clientes identificados originales | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF080 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | 38 países | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF081 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Quantity completa mediana3 | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF082 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Quantity completa P25=1 | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF083 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Quantity completa P75=10 | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF084 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Quantity completa mínima-80995 | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF085 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Quantity completa máxima80995 | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF086 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | UnitPrice completo mediana2,08 GBP | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF087 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | UnitPrice completo P25=1,25 GBP | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF088 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | UnitPrice completo P75=4,13 GBP | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF089 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | UnitPrice completo mínimo-11062,06 GBP | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF090 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | UnitPrice completo máximo38970 GBP | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF091 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Importe completo mediana9,75 GBP | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF092 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Importe completo P25=3,40 GBP | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF093 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Importe completo P75=17,40 GBP | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF094 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Importe completo mínimo-168469,60 GBP | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF095 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Importe completo máximo168469,60 GBP | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF096 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Quantity completa P99=100 | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF097 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | UnitPrice completo P99=18 GBP | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF098 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Importe completo P99=180 GBP | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF099 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Quantity presenta cola amplia | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF100 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | UnitPrice presenta cola amplia | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF101 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Importe presenta cola amplia | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF102 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Medias sensibles a extremos | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF103 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | 10624 cantidades negativas | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF104 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Dos precios negativos | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF105 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | 2515 precios cero | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF106 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | 11805 importes no positivos | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF107 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Unidades sin C5454024 | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF108 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Unidades C-277574 | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF109 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Mediana importe sin C9,90 GBP | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF110 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Mediana importe C-8,50 GBP | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF111 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Agregados C y sin C difieren en signo | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF112 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Noviembre3462 facturas | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF113 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Noviembre740286 unidades netas | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF114 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Cuota mensual mínima C aproximadamente1,27% | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF115 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Cuota mensual máxima C aproximadamente1,99% | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF116 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Cuota C noviembre1,27% | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF117 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Cuota C enero1,99% | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF118 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Cuota de líneas C no acredita tasa de devolución comercial | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF119 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | UK495478 líneas originales | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF120 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | UK23494 facturas | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF121 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Netherlands segundo neto | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF122 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Netherlands neto284661,54 GBP | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF123 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | EIRE tercero neto | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF124 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | EIRE neto263276,82 GBP | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF125 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Germany cuarto neto | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF126 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Germany neto221698,21 GBP | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF127 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | France quinto neto | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF128 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | France neto197403,90 GBP | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF129 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Ranking de pares código–descripción en líneas sin C | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF130 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Par DOT DOTCOM POSTAGE primero por importe regular | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF131 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Par DOT206248,77 GBP | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF132 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Par22423 REGENCY CAKESTAND segundo | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF133 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Par22423 importe174484,74 GBP | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF134 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Par23843 PAPER CRAFT tercero | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF135 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Par23843 importe168469,60 GBP | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF136 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Par23843 una línea | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF137 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Par23843 80995 unidades | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF138 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Par23843 influye en máximos y ranking | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF139 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | 397924 líneas regulares identificadas | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF140 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | 4339 clientes regulares identificados | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF141 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Importe regular por cliente mediana674,45 GBP | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF142 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Importe regular por cliente media2053,79 GBP | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF143 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Facturas por cliente regular mediana2 | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF144 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Facturas por cliente regular media4,27 | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF145 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Actividad identificada con concentración y cola alta | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF146 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Análisis por cliente no representa líneas sin identificador | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF147 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | 530104 líneas regulares con Quantity y UnitPrice positivos | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF148 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Correlación de Spearman entre Quantity y UnitPrice en las ventas positivas: −0,403 | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF149 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Asociación monotónica negativa moderada | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF150 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Spearman no identifica mecanismo causal | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF151 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Spearman no resume población excluida | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF152 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | 647 códigos multidescripción normalizada | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF153 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Máximo ocho descripciones por código | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF154 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Correspondencia código–descripción no unívoca | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF155 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | No se impuso una descripción única por código | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF156 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Los valores no positivos se registran como riesgos, no errores confirmados | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF157 | 9/11/27/29/35/37/39/41/43/47/49/51/53/55/57/59/85/87/89/91/101/107/109/111 | Las cancelaciones afectan sumas netas | R | STAT-002–006/008–015, incidencias y recálculo externo |
| AF158 | 63/65/67/69/71/73/75/77/79/81 | FIG-001 representa neto mensual | R | Cinco PNG inspeccionados, STAT-005/008/010/011/012/013/015 y evento 16 |
| AF159 | 63/65/67/69/71/73/75/77/79/81 | FIG-001 incluye cancelaciones | R | Cinco PNG inspeccionados, STAT-005/008/010/011/012/013/015 y evento 16 |
| AF160 | 63/65/67/69/71/73/75/77/79/81 | Neto crece septiembre–noviembre2011 | R | Cinco PNG inspeccionados, STAT-005/008/010/011/012/013/015 y evento 16 |
| AF161 | 63/65/67/69/71/73/75/77/79/81 | FIG-002 compara diez países principales por importe neto | R | Cinco PNG inspeccionados, STAT-005/008/010/011/012/013/015 y evento 16 |
| AF162 | 63/65/67/69/71/73/75/77/79/81 | UK domina la figura geográfica | R | Cinco PNG inspeccionados, STAT-005/008/010/011/012/013/015 y evento 16 |
| AF163 | 63/65/67/69/71/73/75/77/79/81 | FIG-003 representa frecuencia de C frente a no C | R | Cinco PNG inspeccionados, STAT-005/008/010/011/012/013/015 y evento 16 |
| AF164 | 63/65/67/69/71/73/75/77/79/81 | Líneas C son minoría | R | Cinco PNG inspeccionados, STAT-005/008/010/011/012/013/015 y evento 16 |
| AF165 | 63/65/67/69/71/73/75/77/79/81 | La clasificación C no prueba naturaleza homogénea de todas las operaciones | R | Cinco PNG inspeccionados, STAT-005/008/010/011/012/013/015 y evento 16 |
| AF166 | 63/65/67/69/71/73/75/77/79/81 | FIG-004 representa Quantity positiva en líneas regulares | R | Cinco PNG inspeccionados, STAT-005/008/010/011/012/013/015 y evento 16 |
| AF167 | 63/65/67/69/71/73/75/77/79/81 | FIG-004 representa UnitPrice positivo en líneas regulares | R | Cinco PNG inspeccionados, STAT-005/008/010/011/012/013/015 y evento 16 |
| AF168 | 63/65/67/69/71/73/75/77/79/81 | Los dos histogramas usan escala logarítmica | R | Cinco PNG inspeccionados, STAT-005/008/010/011/012/013/015 y evento 16 |
| AF169 | 63/65/67/69/71/73/75/77/79/81 | FIG-004 excluye valores no positivos de la representación, no del CSV | R | Cinco PNG inspeccionados, STAT-005/008/010/011/012/013/015 y evento 16 |
| AF170 | 63/65/67/69/71/73/75/77/79/81 | Las figuras positivas muestran masa y cola | R | Cinco PNG inspeccionados, STAT-005/008/010/011/012/013/015 y evento 16 |
| AF171 | 63/65/67/69/71/73/75/77/79/81 | FIG-005 muestra doce pares por mayor importe regular | R | Cinco PNG inspeccionados, STAT-005/008/010/011/012/013/015 y evento 16 |
| AF172 | 63/65/67/69/71/73/75/77/79/81 | Las figuras no eliminan datos del CSV | R | Cinco PNG inspeccionados, STAT-005/008/010/011/012/013/015 y evento 16 |
| AF173 | 5/29/31/87/91/93/97/99/101/103/113 | La documentación no clasifica concluyentemente todos los duplicados como errores | R | Campos fuente, diccionario público, operaciones e ISSUE-001–005 |
| AF174 | 5/29/31/87/91/93/97/99/101/103/113 | La documentación no clasifica concluyentemente todos los no positivos como errores | R | Campos fuente, diccionario público, operaciones e ISSUE-001–005 |
| AF175 | 5/29/31/87/91/93/97/99/101/103/113 | La documentación no clasifica concluyentemente todos los extremos como errores | R | Campos fuente, diccionario público, operaciones e ISSUE-001–005 |
| AF176 | 5/29/31/87/91/93/97/99/101/103/113 | No hay calendario operativo | R | Campos fuente, diccionario público, operaciones e ISSUE-001–005 |
| AF177 | 5/29/31/87/91/93/97/99/101/103/113 | La integridad operativa de diciembre 2010 no está acreditada | R | Campos fuente, diccionario público, operaciones e ISSUE-001–005 |
| AF178 | 5/29/31/87/91/93/97/99/101/103/113 | No se determinó origen técnico o legítimo de duplicados | R | Campos fuente, diccionario público, operaciones e ISSUE-001–005 |
| AF179 | 5/29/31/87/91/93/97/99/101/103/113 | No hay relación documentada verificable C–factura original | R | Campos fuente, diccionario público, operaciones e ISSUE-001–005 |
| AF180 | 5/29/31/87/91/93/97/99/101/103/113 | El proceso operativo que genera cada registro no está documentado | R | Campos fuente, diccionario público, operaciones e ISSUE-001–005 |
| AF181 | 5/29/31/87/91/93/97/99/101/103/113 | La ausencia CustomerID no puede asumirse aleatoria | R | Campos fuente, diccionario público, operaciones e ISSUE-001–005 |
| AF182 | 5/29/31/87/91/93/97/99/101/103/113 | Imputar identidad carece de evidencia | R | Campos fuente, diccionario público, operaciones e ISSUE-001–005 |
| AF183 | 5/29/31/87/91/93/97/99/101/103/113 | No hay reglas operativas para códigos especiales | R | Campos fuente, diccionario público, operaciones e ISSUE-001–005 |
| AF184 | 5/29/31/87/91/93/97/99/101/103/113 | No hay reglas operativas para precios no positivos | R | Campos fuente, diccionario público, operaciones e ISSUE-001–005 |
| AF185 | 5/29/31/87/91/93/97/99/101/103/113 | Los análisis de clientes se limitan a identidad observada | R | Campos fuente, diccionario público, operaciones e ISSUE-001–005 |
