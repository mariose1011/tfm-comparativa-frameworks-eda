# Evaluación D2-CA-R1

**Índice final:** 82,47/100.  
**Evaluación cerrada:** 6 de octubre de 2026.  
**Ejecución:** `D2_online_retail__crewai__r01__20260902T171610603875Z`

**Criterios:** [Protocolo de evaluación](../01_protocolo_calidad_Q1_Q10_v0.1.md) y [guía D2](../02_ficha_D2_online_retail.md).  
**Resultados:** [Archivos originales de la ejecución](../../../outputs/experimento/D2_online_retail__crewai__r01__20260902T171610603875Z).  
**Evaluación:** [Excel de puntuaciones](../Evaluacion_calidad.xlsx) y [JSON de comprobaciones](D2-CA-R1_comprobaciones.json).

Las referencias `STAT`, `ISSUE` y `FIG` identifican análisis, problemas y figuras en los archivos de la ejecución. `TR` identifica transformaciones y `CHK`, comprobaciones de calidad. Las referencias a líneas corresponden al informe original, `report.md`.

## Resumen

| Métrica | Puntuación final |
| --- | ---: |
| Q1 Cumplimiento de las etapas | 100,00 |
| Q2 Corrección numérica | 82,98 |
| Q3 Validez del tratamiento de los datos | 91,67 |
| Q4 Detección de problemas y riesgos | 85,11 |
| Q5 Calidad y profundidad del EDA | 75,00 |
| Q6 Profundidad de la interpretación | 75,00 |
| Q7 Calidad de las visualizaciones | 45,00 |
| Q8 Cobertura del informe | 90,91 |
| Q9 Fidelidad del informe | 100,00 |
| Q10 Claridad y coherencia | 75,00 |

## Q1 Cumplimiento de las etapas: 100,00

Las ocho etapas tienen evidencia válida:

| Etapa | Nota | Evidencia |
| --- | ---: | --- |
| E1 Carga e inspección inicial | 1 | STAT-001, profile y documentación |
| E2 Estructura, tipos y calidad | 1 | STAT-002 a STAT-006 |
| E3 Preparación y decisiones de análisis | 1 | TR-001 a TR-004, STAT-007 y CSV |
| E4 Estadística descriptiva | 1 | STAT-008/009/010 |
| E5 Variables, agregaciones y relaciones | 1 | STAT-011/012/013/014 finales |
| E6 Visualizaciones | 1 | Cuatro figuras válidas e identificadas. Los objetivos ausentes se valoran en Q7 |
| E7 Problemas, riesgos y anomalías | 1 | Seis comprobaciones y siete incidencias con decisiones y evidencias |
| E8 Informe final | 1 | Informe final con alcance, preparación, resultados y limitaciones |

`Q1 = 100 x 8 / 8 = 100,00`

## Q2 Corrección numérica: 82,98

Se cumplen 25 de las 32 comprobaciones previstas, que suman 39 de los 47 puntos ponderados.

| Controles | Resultado | Evidencia o motivo |
| --- | --- | --- |
| C01–C07 | Correctos | Estructura, fechas y marginales de ausencias, STAT-001/002 |
| C08 | Ausente | No presenta cuántos registros tienen ausentes simultáneamente CustomerID y Description |
| C09 | Correcto | 5268 duplicados exactos, STAT-003 |
| C10 | Correcto | Los 541.909 registros originales menos los 5.268 duplicados dan 536.641 registros. STAT-001 y STAT-003 |
| C11–C15 | Correctos | Cardinalidades y líneas C, STAT-002/004 |
| C16 | Ausente | No presenta el número de facturas distintas cuyo identificador comienza por C |
| C17–C26 | Correctos | Signos, extremos, cantidad e importes netos/positivos, STAT-004/008/009 |
| C27 | Ausente | No presenta el importe total de los registros identificados como cancelaciones |
| C28 | Ausente | No presenta el importe neto después de excluir los duplicados exactos |
| C29 | Ausente | Comunica la participación del Reino Unido en el importe de las ventas positivas, no su porcentaje sobre todos los registros originales |
| C30 | Correcto | Identifica noviembre de 2011 como máximo mensual de las ventas positivas, con 1.509.496,33 GBP. STAT-011 |
| C31 | Ausente | Identifica 650 códigos con varias descripciones originales, pero no los 647 obtenidos después de eliminar espacios iniciales y finales y convertir las descripciones a mayúsculas |
| C32 | Ausente | La mediana de 15 registros por factura corresponde a las ventas positivas, no al conjunto completo de facturas |

`Q2 = 100 x 39 / 47 = 82,98`

## Q3 Validez del tratamiento de los datos: 91,67

| Decisión | Nota | Justificación y evidencia |
| --- | ---: | --- |
| D01 Identificadores | 1 | Texto nominal, valores y ausencias conservados. TR-001 y CSV |
| D02 Fecha-hora | 1 | InvoiceDate ISO conserva fecha y hora en todas las filas. TR-002 |
| D03 Importe | 1 | LineAmount = Quantity x UnitPrice, con poblaciones explícitas. STAT-007/008/009/014 |
| D04 Unidades | 1 | Distingue líneas, facturas, clientes y productos. STAT-002/003/013/014 |
| D05 Cancelaciones | 1 | Conserva C, crea indicador y cuantifica sus líneas. STAT-004 |
| D06 Cliente ausente | 1 | Retiene filas en análisis global y compara disponibilidad sin imputar clientes. STAT-010 |
| D07 Descripción ausente | 1 | Conserva las descripciones ausentes. La descripción seleccionada para identificar cada producto no modifica los valores de las filas originales. CSV y operación del evento 86 |
| D08 Duplicados | 0 | Conserva los duplicados, pero no compara los resultados con y sin esas filas. STAT-003 |
| D09 Ajustes | 1 | Separa cantidades negativas sin C, precios cero y precios negativos. STAT-004 e ISSUE-004 |
| D10 Extremos | 1 | Conserva extremos, usa cuantiles, IQR y escala logarítmica. STAT-008/009/015 y FIG-003 |
| D11 Mes final | 1 | Conserva el periodo, informa de que diciembre de 2011 termina el día 9 y advierte sobre las comparaciones mensuales. STAT-001/005 y líneas 21/48/92 del informe |
| D12 Categorías | 1 | Limita las clasificaciones a los productos o países principales y conserva el detalle original |

`Q3 = 100 x 11 / 12 = 91,67`

## Q4 Detección de problemas y riesgos: 85,11

Se detectan por completo ocho de los diez riesgos de referencia (K = 8), se identifican dos riesgos adicionales válidos (A = 2) y se registra una afirmación sin respaldo suficiente (F = 1). Por tanto, diez de los once hallazgos son válidos, lo que da una precisión del 90,91 %, mientras que la cobertura de los riesgos de referencia es del 80 %. Ambas medidas se combinan mediante F1 para obtener la puntuación de Q4.

| Riesgo conocido | Resultado | Evidencia |
| --- | --- | --- |
| R01 Ausencias | Detectado | STAT-002, ISSUE-001/002 e informe42/78 |
| R02 Duplicados | Detectado | STAT-003, ISSUE-003 e informe32 |
| R03 C y cantidades negativas | Detectado | STAT-004 e informe46 |
| R04 Negativos sin C | Detectado | 1336 casos, STAT-004 e informe46/88 |
| R05 Precios cero y negativos | Detectado | Ambos en STAT-004 e ISSUE-004, aunque los negativos no llegan al informe |
| R06 Unidad e identificadores | Detectado | STAT-001/002/003/007 e informe3/15/21/36 |
| R07 Diciembre 2011 hasta día 9 | Detectado | STAT-001/005 e informe21/48/92 |
| R08 Concentración de líneas UK | Parcial | Concentración monetaria positiva, no proporción de líneas originales |
| R09 Asimetría y extremos | Detectado | STAT-008/009/015 e informe38/40/82 |
| R10 Definiciones monetarias | Parcial | Positivo y neto presentes, pero sin importe cancelado ni efecto deduplicado |

Además de los riesgos previstos, la ejecución identifica dos problemas adicionales válidos y formula una advertencia que no cuenta con respaldo suficiente. La siguiente tabla recoge estos tres casos.

| Hallazgo adicional o falsa alarma | Clasificación | Evidencia |
| --- | --- | --- |
| Varias descripciones para un mismo código, que pueden dividir sus resultados si se utilizan para agrupar | A01 válido | 	STAT-006/013, ISSUE-005 y operación del evento 86 |
| Códigos de gastos de envío y operaciones manuales, además de productos físicos | A02 válido | STAT-013 y línea 52 del informe |
| Diciembre de 2010 identificado como incompleto sin evidencia suficiente | F01 sin respaldo suficiente | Interpretación de STAT-011 y descripción de ISSUE-006 |

STAT-011 e ISSUE-006 presentan diciembre de 2010 como incompleto o no comparable con meses completos, sin evidencia suficiente para afirmarlo. El informe final expresa esa posibilidad como una incertidumbre, por lo que no se clasifica como una afirmación sin respaldo en Q9.

`Q4 = 100 x [2 x (10 / 11) x (8 / 10)] / [(10 / 11) + (8 / 10)] = 85,11`

## Q5 Calidad y profundidad del EDA: 75,00

El análisis incluye estadísticas descriptivas de distintos grupos de registros, comparaciones según la disponibilidad del identificador de cliente, evolución temporal, países, productos y correlaciones. Recibe 3 de 4 puntos porque no cuantifica el efecto de excluir duplicados ni compara los importes de cancelaciones y ajustes con los principales agregados monetarios.

`Q5 = 100 x 3 / 4 = 75,00`

## Q6 Profundidad de la interpretación: 75,00

El informe distingue los importes calculados de los cobros confirmados, la correlación de la causalidad y las asociaciones derivadas de calcular el importe como cantidad por precio. Recibe 3 de 4 puntos porque no cuantifica cómo influyen las cancelaciones, los ajustes y los duplicados en los resultados monetarios.

`Q6 = 100 x 3 / 4 = 75,00`

## Q7 Calidad de las visualizaciones: 45,00

| Objetivo | Nota 0–4 | Justificación |
| --- | ---: | --- |
| V01 Evolución | 4 | FIG-001 representa importe positivo y facturas, con ejes y unidades explícitos. Informe21/48/92 da cobertura y cautela del mes final |
| V02 Cancelaciones/ajustes | 0 | No hay gráficos específicos sobre cancelaciones o ajustes |
| V03 Distribuciones | 3 | FIG-003 representa las distribuciones positivas completas en escala logarítmica, pero no muestra los valores cero o negativos |
| V04 Países | 2 | FIG-002 representa correctamente los importes, pero el valor del Reino Unido dificulta comparar los demás países |
| V05 Productos/clientes | 0 | Las estadísticas y el informe contienen clasificaciones de productos, pero ninguna figura las representa |

FIG-004 muestra la relación entre precio y cantidad para los valores situados hasta el percentil 99, pero no cubre los objetivos visuales ausentes.

Las puntuaciones 4, 0, 3, 2 y 0 suman 9/20, equivalentes a 45,00.

`Q7 = 100 x 9 / 20 = 45,00`

## Q8 Cobertura del informe: 90,91

| Unidad | Peso | Nota | Motivo y evidencia |
| --- | ---: | ---: | --- |
| U01 Estructura y periodo | 2 | 1 | Informe3/21 |
| U02 Ausencias e impacto | 2 | 1 | Informe42/76/78/90 |
| U03 Unidades | 2 | 1 | Informe3/15/36/52/54/96 |
| U04 Duplicados y decisión | 2 | 1 | Línea 32 del informe |
| U05 C y cantidades negativas | 2 | 1 | Informe46 |
| U06 Precios y ajustes | 2 | 0,5 | Describe ceros y negativos sin C. No comunica los dos precios negativos, presentes en STAT-004 |
| U07 Definiciones monetarias | 2 | 0,5 | Explica las ventas positivas y sus limitaciones, pero no comunica el importe neto total, el de las cancelaciones ni el efecto de excluir duplicados |
| U08 Evolución y máximo | 2 | 1 | Máximo positivo de noviembre y cobertura final hasta día9, con advertencia de comparabilidad. Informe21/48/92 |
| U09 Predominio geográfico | 2 | 1 | Importe y cuota monetaria de UK, sin atribuirlos a tamaño de mercado o rentabilidad. Informe50/62 |
| U10 Productos/conceptos | 1 | 1 | Explica el elevado número de códigos distintos, las variaciones de descripción y la presencia de gastos de envío y operaciones manuales. Líneas 36/52/78 del informe |
| U11 Asimetría y extremos | 2 | 1 | Medianas, rangos, percentiles y explicación. Informe38/40/66/82 |
| U12 Limitaciones | 1 | 1 | Empresa y ventana identificadas, ausencias e incertidumbre sobre ajustes y duplicados. Informe13/32/86–92 |

`Q8 = 100 x 20 / 22 = 90,91`

## Q9 Fidelidad del informe: 100,00

Las 155 afirmaciones evaluadas cuentan con respaldo en las evidencias de la ejecución.

El inventario situado al final de esta ficha recoge las afirmaciones revisadas, su clasificación y las evidencias utilizadas.

`Q9 = 100 x 155 / 155 = 100,00`

## Q10 Claridad y coherencia: 75,00

El informe presenta una estructura clara, filtros consistentes y figuras explicadas. Recibe 3 de 4 puntos porque la expresión "4.223 valores no ausentes de Description" no especifica que son valores distintos y utiliza "precios nulos" para referirse a precios iguales a cero, lo que puede confundirse con datos ausentes.

`Q10 = 100 x 3 / 4 = 75,00`

## Inventario de afirmaciones

R = respaldada.

| ID | Líneas del informe | Afirmación | Estado | Evidencia |
| --- | --- | --- | --- | --- |
| AF001 | 3/13/15/21/36/96 | 541909 líneas originales | R | STAT-001/002/003 y Readme |
| AF002 | 3/13/15/21/36/96 | 25900 facturas distintas originales | R | STAT-001/002/003 y Readme |
| AF003 | 3/13/15/21/36/96 | Ocho columnas fuente | R | STAT-001/002/003 y Readme |
| AF004 | 3/13/15/21/36/96 | Periodo desde 2010-12-01 | R | STAT-001/002/003 y Readme |
| AF005 | 3/13/15/21/36/96 | Periodo hasta 2011-12-09 | R | STAT-001/002/003 y Readme |
| AF006 | 3/13/15/21/36/96 | Formato XLSX, hoja Online Retail | R | STAT-001/002/003 y Readme |
| AF007 | 3/13/15/21/36/96 | La lista de ocho campos coincide con la entrada | R | STAT-001/002/003 y Readme |
| AF008 | 3/13/15/21/36/96 | Una fila es una línea de factura | R | STAT-001/002/003 y Readme |
| AF009 | 3/13/15/21/36/96 | Una fila no equivale necesariamente a una factura completa | R | STAT-001/002/003 y Readme |
| AF010 | 3/13/15/21/36/96 | Una fila no equivale necesariamente a un pago | R | STAT-001/002/003 y Readme |
| AF011 | 3/13/15/21/36/96 | Una fila no equivale necesariamente a una compra consolidada | R | STAT-001/002/003 y Readme |
| AF012 | 3/13/15/21/36/96 | Las transacciones son de una empresa británica de comercio electrónico | R | STAT-001/002/003 y Readme |
| AF013 | 3/13/15/21/36/96 | La documentación admite clientes mayoristas | R | STAT-001/002/003 y Readme |
| AF014 | 3/13/15/21/36/96 | Una factura puede contener varias líneas | R | STAT-001/002/003 y Readme |
| AF015 | 3/13/15/21/36/96 | El máximo de líneas por InvoiceNo es 1114 | R | STAT-001/002/003 y Readme |
| AF016 | 3/13/15/21/36/96 | 4070 StockCode distintos | R | STAT-001/002/003 y Readme |
| AF017 | 3/13/15/21/36/96 | 4223 valores distintos no ausentes de Description | R | STAT-001/002/003 y Readme |
| AF018 | 3/13/15/21/36/96 | 4372 clientes identificados distintos | R | STAT-001/002/003 y Readme |
| AF019 | 3/13/15/21/36/96 | 38 categorías Country | R | STAT-001/002/003 y Readme |
| AF020 | 3/13/15/21/36/96 | La ventana incluye 13 meses calendario observados | R | STAT-001/002/003 y Readme |
| AF021 | 5/17/21/23/25–30/32/46/70/80/82/98 | Se conserva la población original íntegra | R | CSV, TR-001 a TR-004, código 16, STAT-007/014 |
| AF022 | 5/17/21/23/25–30/32/46/70/80/82/98 | No se eliminaron cancelaciones | R | CSV, TR-001 a TR-004, código 16, STAT-007/014 |
| AF023 | 5/17/21/23/25–30/32/46/70/80/82/98 | No se eliminaron filas con ausencias | R | CSV, TR-001 a TR-004, código 16, STAT-007/014 |
| AF024 | 5/17/21/23/25–30/32/46/70/80/82/98 | No se eliminaron duplicados exactos | R | CSV, TR-001 a TR-004, código 16, STAT-007/014 |
| AF025 | 5/17/21/23/25–30/32/46/70/80/82/98 | No se eliminaron extremos | R | CSV, TR-001 a TR-004, código 16, STAT-007/014 |
| AF026 | 5/17/21/23/25–30/32/46/70/80/82/98 | InvoiceNo se convirtió a texto nominal | R | CSV, TR-001 a TR-004, código 16, STAT-007/014 |
| AF027 | 5/17/21/23/25–30/32/46/70/80/82/98 | StockCode se convirtió a texto nominal | R | CSV, TR-001 a TR-004, código 16, STAT-007/014 |
| AF028 | 5/17/21/23/25–30/32/46/70/80/82/98 | CustomerID se convirtió a texto nominal | R | CSV, TR-001 a TR-004, código 16, STAT-007/014 |
| AF029 | 5/17/21/23/25–30/32/46/70/80/82/98 | Se recortaron espacios periféricos en identificadores | R | CSV, TR-001 a TR-004, código 16, STAT-007/014 |
| AF030 | 5/17/21/23/25–30/32/46/70/80/82/98 | InvoiceDate se serializó en ISO 8601 | R | CSV, TR-001 a TR-004, código 16, STAT-007/014 |
| AF031 | 5/17/21/23/25–30/32/46/70/80/82/98 | El CSV conserva 541909 filas | R | CSV, TR-001 a TR-004, código 16, STAT-007/014 |
| AF032 | 5/17/21/23/25–30/32/46/70/80/82/98 | El CSV contiene 12 columnas | R | CSV, TR-001 a TR-004, código 16, STAT-007/014 |
| AF033 | 5/17/21/23/25–30/32/46/70/80/82/98 | Se añadieron cuatro derivadas | R | CSV, TR-001 a TR-004, código 16, STAT-007/014 |
| AF034 | 5/17/21/23/25–30/32/46/70/80/82/98 | IsCancellation señala prefijo C | R | CSV, TR-001 a TR-004, código 16, STAT-007/014 |
| AF035 | 5/17/21/23/25–30/32/46/70/80/82/98 | HasCustomerID señala disponibilidad del identificador | R | CSV, TR-001 a TR-004, código 16, STAT-007/014 |
| AF036 | 5/17/21/23/25–30/32/46/70/80/82/98 | LineAmount es Quantity por UnitPrice | R | CSV, TR-001 a TR-004, código 16, STAT-007/014 |
| AF037 | 5/17/21/23/25–30/32/46/70/80/82/98 | InvoiceMonth es el periodo mensual de InvoiceDate | R | CSV, TR-001 a TR-004, código 16, STAT-007/014 |
| AF038 | 5/17/21/23/25–30/32/46/70/80/82/98 | Error absoluto máximo de la identidad de importe igual a cero | R | CSV, TR-001 a TR-004, código 16, STAT-007/014 |
| AF039 | 5/17/21/23/25–30/32/46/70/80/82/98 | Quantity se cargó como entero | R | CSV, TR-001 a TR-004, código 16, STAT-007/014 |
| AF040 | 5/17/21/23/25–30/32/46/70/80/82/98 | UnitPrice se cargó como flotante | R | CSV, TR-001 a TR-004, código 16, STAT-007/014 |
| AF041 | 5/17/21/23/25–30/32/46/70/80/82/98 | InvoiceDate se cargó como fecha-hora | R | CSV, TR-001 a TR-004, código 16, STAT-007/014 |
| AF042 | 5/17/21/23/25–30/32/46/70/80/82/98 | Los tres identificadores se usan como nominales, no magnitudes | R | CSV, TR-001 a TR-004, código 16, STAT-007/014 |
| AF043 | 5/17/21/23/25–30/32/46/70/80/82/98 | No se entrenaron modelos predictivos | R | CSV, TR-001 a TR-004, código 16, STAT-007/014 |
| AF044 | 5/17/21/23/25–30/32/46/70/80/82/98 | El análisis no realizó inferencias causales | R | CSV, TR-001 a TR-004, código 16, STAT-007/014 |
| AF045 | 5/17/21/23/25–30/32/46/70/80/82/98 | Los importes se expresan en GBP conforme al diccionario | R | CSV, TR-001 a TR-004, código 16, STAT-007/014 |
| AF046 | 5/17/21/23/25–30/32/46/70/80/82/98 | Los agregados se realizan sobre poblaciones declaradas | R | CSV, TR-001 a TR-004, código 16, STAT-007/014 |
| AF047 | 5/17/21/23/25–30/32/46/70/80/82/98 | Primera fecha-hora 2010-12-01T08:26:00 | R | CSV, TR-001 a TR-004, código 16, STAT-007/014 |
| AF048 | 5/17/21/23/25–30/32/46/70/80/82/98 | Última fecha-hora 2011-12-09T12:50:00 | R | CSV, TR-001 a TR-004, código 16, STAT-007/014 |
| AF049 | 7/9/40/48/98/100 | La venta operativa exige InvoiceNo sin C | R | STAT-009/011 y código 16 |
| AF050 | 7/9/40/48/98/100 | La venta operativa exige Quantity positiva | R | STAT-009/011 y código 16 |
| AF051 | 7/9/40/48/98/100 | La venta operativa exige UnitPrice positivo | R | STAT-009/011 y código 16 |
| AF052 | 7/9/40/48/98/100 | 530104 líneas de venta operativa | R | STAT-009/011 y código 16 |
| AF053 | 7/9/40/48/98/100 | 97,822% de líneas operativas | R | STAT-009/011 y código 16 |
| AF054 | 7/9/40/48/98/100 | 19960 facturas de venta operativa | R | STAT-009/011 y código 16 |
| AF055 | 7/9/40/48/98/100 | Importe positivo total 10666684,54 GBP | R | STAT-009/011 y código 16 |
| AF056 | 7/9/40/48/98/100 | Importe de línea no certifica cobro | R | STAT-009/011 y código 16 |
| AF057 | 7/9/40/48/98/100 | Importe de línea no certifica ingreso neto | R | STAT-009/011 y código 16 |
| AF058 | 7/9/40/48/98/100 | Mediana Quantity positiva igual a 3 | R | STAT-009/011 y código 16 |
| AF059 | 7/9/40/48/98/100 | Mediana UnitPrice positiva igual a 2,08 GBP | R | STAT-009/011 y código 16 |
| AF060 | 7/9/40/48/98/100 | Mediana LineAmount positiva igual a 9,90 GBP | R | STAT-009/011 y código 16 |
| AF061 | 7/9/40/48/98/100 | Percentil 99 de importe positivo igual a 183,60 GBP | R | STAT-009/011 y código 16 |
| AF062 | 7/9/40/48/98/100 | Máximo de importe positivo igual a 168469,60 GBP | R | STAT-009/011 y código 16 |
| AF063 | 7/9/40/48/98/100 | Distribución positiva de importe muy asimétrica | R | STAT-009/011 y código 16 |
| AF064 | 7/9/40/48/98/100 | La actividad positiva varía por mes | R | STAT-009/011 y código 16 |
| AF065 | 7/9/40/48/98/100 | Noviembre2011 es el máximo mensual de importe positivo | R | STAT-009/011 y código 16 |
| AF066 | 7/9/40/48/98/100 | Importe noviembre2011 de 1509496,33 GBP | R | STAT-009/011 y código 16 |
| AF067 | 7/9/40/48/98/100 | 83369 líneas positivas en noviembre2011 | R | STAT-009/011 y código 16 |
| AF068 | 7/9/40/48/98/100 | 2769 facturas positivas en noviembre2011 | R | STAT-009/011 y código 16 |
| AF069 | 7/9/40/48/98/100 | Importe octubre2011 de 1154979,30 GBP | R | STAT-009/011 y código 16 |
| AF070 | 32/38/42/46/76/78/80/82/88/90/102 | 5268 duplicados exactos después del primero | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF071 | 32/38/42/46/76/78/80/82/88/90/102 | 0,972% de duplicados exactos | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF072 | 32/38/42/46/76/78/80/82/88/90/102 | No existe clave de línea en los ocho campos fuente | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF073 | 32/38/42/46/76/78/80/82/88/90/102 | La documentación no distingue duplicados administrativos de líneas legítimas iguales | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF074 | 32/38/42/46/76/78/80/82/88/90/102 | La mediana Quantity en todas las líneas es 3 | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF075 | 32/38/42/46/76/78/80/82/88/90/102 | La mediana UnitPrice en todas las líneas es 2,08 GBP | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF076 | 32/38/42/46/76/78/80/82/88/90/102 | La mediana LineAmount en todas las líneas es 9,75 GBP | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF077 | 32/38/42/46/76/78/80/82/88/90/102 | Las medias de las tres variables exceden sus medianas | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF078 | 32/38/42/46/76/78/80/82/88/90/102 | Importe mínimo de línea −168469,60 GBP | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF079 | 32/38/42/46/76/78/80/82/88/90/102 | Importe máximo de línea 168469,60 GBP | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF080 | 32/38/42/46/76/78/80/82/88/90/102 | Medias y sumas incorporan extremos y ajustes con signo | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF081 | 32/38/42/46/76/78/80/82/88/90/102 | 135080 líneas sin CustomerID | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF082 | 32/38/42/46/76/78/80/82/88/90/102 | 24,927% de líneas sin CustomerID | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF083 | 32/38/42/46/76/78/80/82/88/90/102 | Mediana importe sin cliente de 4,96 GBP | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF084 | 32/38/42/46/76/78/80/82/88/90/102 | Mediana importe con cliente de 11,10 GBP | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF085 | 32/38/42/46/76/78/80/82/88/90/102 | Ausencia de identificador impide atribuir esas líneas a clientes individuales | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF086 | 32/38/42/46/76/78/80/82/88/90/102 | La comparación por disponibilidad de cliente no demuestra causas | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF087 | 32/38/42/46/76/78/80/82/88/90/102 | 9288 líneas de cancelación C | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF088 | 32/38/42/46/76/78/80/82/88/90/102 | 1,714% de líneas C | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF089 | 32/38/42/46/76/78/80/82/88/90/102 | 10624 líneas con cantidad negativa | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF090 | 32/38/42/46/76/78/80/82/88/90/102 | 9288 cantidades negativas corresponden a C | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF091 | 32/38/42/46/76/78/80/82/88/90/102 | 1336 cantidades negativas no tienen prefijo C | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF092 | 32/38/42/46/76/78/80/82/88/90/102 | 2515 precios cero fuera de C | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF093 | 32/38/42/46/76/78/80/82/88/90/102 | Los casos no positivos quedan fuera de la población operativa | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF094 | 32/38/42/46/76/78/80/82/88/90/102 | 1454 líneas sin Description | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF095 | 32/38/42/46/76/78/80/82/88/90/102 | 0,268% de líneas sin Description | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF096 | 32/38/42/46/76/78/80/82/88/90/102 | 650 códigos con varias descripciones originales no ausentes | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF097 | 32/38/42/46/76/78/80/82/88/90/102 | 112 códigos sin descripción no ausente | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF098 | 32/38/42/46/76/78/80/82/88/90/102 | Description no es identificador unívoco de producto | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF099 | 32/38/42/46/76/78/80/82/88/90/102 | No se imputaron clientes ni descripciones concretas | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF100 | 32/38/42/46/76/78/80/82/88/90/102 | Los negativos, ceros y duplicados no se clasificaron como errores confirmados | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF101 | 32/38/42/46/76/78/80/82/88/90/102 | La documentación define C como cancelación | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF102 | 32/38/42/46/76/78/80/82/88/90/102 | No hay reglas documentales suficientes para interpretar los demás ajustes o extremos | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF103 | 32/38/42/46/76/78/80/82/88/90/102 | IQR superior Quantity de 23,5 unidades | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF104 | 32/38/42/46/76/78/80/82/88/90/102 | 56363 cantidades positivas superan el umbral IQR | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF105 | 32/38/42/46/76/78/80/82/88/90/102 | IQR superior UnitPrice de 8,45 GBP | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF106 | 32/38/42/46/76/78/80/82/88/90/102 | 37999 precios positivos superan el umbral IQR | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF107 | 32/38/42/46/76/78/80/82/88/90/102 | IQR superior LineAmount de 38,625 GBP | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF108 | 32/38/42/46/76/78/80/82/88/90/102 | 42651 importes positivos superan el umbral IQR | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF109 | 32/38/42/46/76/78/80/82/88/90/102 | IQR señala valores estadísticamente altos, no demuestra errores | R | STAT-002/003/004/006/008/010/015 e incidencias |
| AF110 | 50/52/54/62/78/90/100 | Importe UK positivo de 9025222,08 GBP | R | STAT-012/013/014 finales y código86 |
| AF111 | 50/52/54/62/78/90/100 | Cuota UK positiva de 84,61% | R | STAT-012/013/014 finales y código86 |
| AF112 | 50/52/54/62/78/90/100 | Top diez países representa 97,21% del importe positivo | R | STAT-012/013/014 finales y código86 |
| AF113 | 50/52/54/62/78/90/100 | La concentración describe registros, no causas de actividad | R | STAT-012/013/014 finales y código86 |
| AF114 | 50/52/54/62/78/90/100 | Ranking final agrega exclusivamente por StockCode | R | STAT-012/013/014 finales y código86 |
| AF115 | 50/52/54/62/78/90/100 | Description no integra la clave final de agregación | R | STAT-012/013/014 finales y código86 |
| AF116 | 50/52/54/62/78/90/100 | Una etiqueta no ausente se elige por frecuencia dentro de la población operativa | R | STAT-012/013/014 finales y código86 |
| AF117 | 50/52/54/62/78/90/100 | El desempate de etiqueta es alfabético | R | STAT-012/013/014 finales y código86 |
| AF118 | 50/52/54/62/78/90/100 | PAPER CRAFT , LITTLE BIRDIE es la etiqueta de 23843 | R | STAT-012/013/014 finales y código86 |
| AF119 | 50/52/54/62/78/90/100 | 23843 suma 80995 unidades positivas | R | STAT-012/013/014 finales y código86 |
| AF120 | 50/52/54/62/78/90/100 | 23843 tiene una sola línea positiva | R | STAT-012/013/014 finales y código86 |
| AF121 | 50/52/54/62/78/90/100 | DOTCOM POSTAGE encabeza el ranking monetario | R | STAT-012/013/014 finales y código86 |
| AF122 | 50/52/54/62/78/90/100 | DOT es el código de DOTCOM POSTAGE | R | STAT-012/013/014 finales y código86 |
| AF123 | 50/52/54/62/78/90/100 | Importe positivo DOT de 206248,77 GBP | R | STAT-012/013/014 finales y código86 |
| AF124 | 50/52/54/62/78/90/100 | El catálogo incluye DOTCOM POSTAGE, POSTAGE y Manual | R | STAT-012/013/014 finales y código86 |
| AF125 | 50/52/54/62/78/90/100 | No todos los conceptos del ranking son productos físicos homogéneos | R | STAT-012/013/014 finales y código86 |
| AF126 | 50/52/54/62/78/90/100 | El ranking varía entre cantidad e importe | R | STAT-012/013/014 finales y código86 |
| AF127 | 50/52/54/62/78/90/100 | Mediana de 15 líneas por factura positiva | R | STAT-012/013/014 finales y código86 |
| AF128 | 50/52/54/62/78/90/100 | Mediana de importe por factura positiva 303,84 GBP | R | STAT-012/013/014 finales y código86 |
| AF129 | 50/52/54/62/78/90/100 | Spearman Quantity–UnitPrice de −0,403 | R | STAT-012/013/014 finales y código86 |
| AF130 | 50/52/54/62/78/90/100 | LineAmount tiene asociación positiva con Quantity | R | STAT-012/013/014 finales y código86 |
| AF131 | 50/52/54/62/78/90/100 | LineAmount tiene asociación positiva con UnitPrice | R | STAT-012/013/014 finales y código86 |
| AF132 | 50/52/54/62/78/90/100 | La relación con el importe es parcialmente mecánica por su identidad de producto | R | STAT-012/013/014 finales y código86 |
| AF133 | 50/52/54/62/78/90/100 | Una etiqueta elegida no recoge necesariamente todas las variantes de descripción | R | STAT-012/013/014 finales y código86 |
| AF134 | 58/60/62/64/66/68/70/72 | FIG-001 representa importe y facturas mensuales positivas | R | Cuatro PNG abiertos, FIG-001 a FIG-004, código 16 y STAT-011/012 |
| AF135 | 58/60/62/64/66/68/70/72 | Los dos ejes distinguen las métricas y sus unidades | R | Cuatro PNG abiertos, FIG-001 a FIG-004, código 16 y STAT-011/012 |
| AF136 | 58/60/62/64/66/68/70/72 | La figura mensual permite observar el máximo de noviembre2011 | R | Cuatro PNG abiertos, FIG-001 a FIG-004, código 16 y STAT-011/012 |
| AF137 | 58/60/62/64/66/68/70/72 | FIG-002 compara diez países por importe positivo | R | Cuatro PNG abiertos, FIG-001 a FIG-004, código 16 y STAT-011/012 |
| AF138 | 58/60/62/64/66/68/70/72 | FIG-002 muestra predominio UK | R | Cuatro PNG abiertos, FIG-001 a FIG-004, código 16 y STAT-011/012 |
| AF139 | 58/60/62/64/66/68/70/72 | FIG-002 no representa población, demanda ni rentabilidad por país | R | Cuatro PNG abiertos, FIG-001 a FIG-004, código 16 y STAT-011/012 |
| AF140 | 58/60/62/64/66/68/70/72 | FIG-003 usa log10 de Quantity positiva | R | Cuatro PNG abiertos, FIG-001 a FIG-004, código 16 y STAT-011/012 |
| AF141 | 58/60/62/64/66/68/70/72 | FIG-003 usa log10 de LineAmount positivo | R | Cuatro PNG abiertos, FIG-001 a FIG-004, código 16 y STAT-011/012 |
| AF142 | 58/60/62/64/66/68/70/72 | Los histogramas logarítmicos incluyen la masa central y toda la cola positiva | R | Cuatro PNG abiertos, FIG-001 a FIG-004, código 16 y STAT-011/012 |
| AF143 | 58/60/62/64/66/68/70/72 | La transformación logarítmica es exclusivamente visual | R | Cuatro PNG abiertos, FIG-001 a FIG-004, código 16 y STAT-011/012 |
| AF144 | 58/60/62/64/66/68/70/72 | Las estadísticas conservan la escala original | R | Cuatro PNG abiertos, FIG-001 a FIG-004, código 16 y STAT-011/012 |
| AF145 | 58/60/62/64/66/68/70/72 | FIG-004 representa la densidad central de Quantity y UnitPrice | R | Cuatro PNG abiertos, FIG-001 a FIG-004, código 16 y STAT-011/012 |
| AF146 | 58/60/62/64/66/68/70/72 | FIG-004 limita Quantity al percentil 99 | R | Cuatro PNG abiertos, FIG-001 a FIG-004, código 16 y STAT-011/012 |
| AF147 | 58/60/62/64/66/68/70/72 | FIG-004 limita UnitPrice al percentil 99 | R | Cuatro PNG abiertos, FIG-001 a FIG-004, código 16 y STAT-011/012 |
| AF148 | 58/60/62/64/66/68/70/72 | El recorte de FIG-004 no se aplica a los agregados | R | Cuatro PNG abiertos, FIG-001 a FIG-004, código 16 y STAT-011/012 |
| AF149 | 58/60/62/64/66/68/70/72 | El recorte de FIG-004 no se aplica al CSV | R | Cuatro PNG abiertos, FIG-001 a FIG-004, código 16 y STAT-011/012 |
| AF150 | 58/60/62/64/66/68/70/72 | Los extremos permanecen en el CSV y las estadísticas | R | Cuatro PNG abiertos, FIG-001 a FIG-004, código 16 y STAT-011/012 |
| AF151 | 9/48/86/88/92 | Ambos diciembres son meses de borde de la ventana observada | R | Readme, STAT-001/005 y fecha final observada |
| AF152 | 9/48/86/88/92 | Diciembre 2011 acaba el día9, por lo que no cubre el mes calendario | R | Readme, STAT-001/005 y fecha final observada |
| AF153 | 9/48/86/88/92 | El archivo no registra pagos ni entregas confirmadas | R | Readme, STAT-001/005 y fecha final observada |
| AF154 | 9/48/86/88/92 | El archivo no consolida devoluciones o facturas netas | R | Readme, STAT-001/005 y fecha final observada |
| AF155 | 9/48/86/88/92 | No se dispone de márgenes o rentabilidad realizada | R | Readme, STAT-001/005 y fecha final observada |
