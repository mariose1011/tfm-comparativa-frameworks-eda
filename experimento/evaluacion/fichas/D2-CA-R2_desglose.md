# Evaluación D2-CA-R2

**Índice final:** 84,49/100.  
**Evaluación cerrada:** 6 de octubre de 2026.  
**Ejecución:** `D2_online_retail__crewai__r02__20260902T193106552358Z`

**Criterios:** [Protocolo de evaluación](../01_protocolo_calidad_Q1_Q10_v0.1.md) y [guía D2](../02_ficha_D2_online_retail.md).  
**Resultados:** [Archivos originales de la ejecución](../../../outputs/experimento/D2_online_retail__crewai__r02__20260902T193106552358Z).  
**Evaluación:** [Excel de puntuaciones](../Evaluacion_calidad.xlsx) y [JSON de comprobaciones](D2-CA-R2_comprobaciones.json).

Las referencias `STAT`, `ISSUE` y `FIG` identifican análisis, problemas y figuras en los archivos de la ejecución. `TR` identifica transformaciones y `CHK`, comprobaciones de calidad. Las referencias a líneas corresponden al informe original, `report.md`.

## Resumen

| Métrica | Puntuación final |
| --- | ---: |
| Q1 Cumplimiento de las etapas | 100,00 |
| Q2 Corrección numérica | 89,36 |
| Q3 Validez del tratamiento de los datos | 91,67 |
| Q4 Detección de problemas y riesgos | 90,45 |
| Q5 Calidad y profundidad del EDA | 75,00 |
| Q6 Profundidad de la interpretación | 75,00 |
| Q7 Calidad de las visualizaciones | 60,00 |
| Q8 Cobertura del informe | 81,82 |
| Q9 Fidelidad del informe | 99,38 |
| Q10 Claridad y coherencia | 75,00 |

## Q1 Cumplimiento de las etapas: 100,00

Las ocho etapas tienen evidencia:

| Etapa | Nota | Evidencia |
| --- | ---: | --- |
| E1 Carga e inspección inicial | 1 | STAT-001/004/005, plan y documentación pública |
| E2 Estructura, tipos y calidad | 1 | STAT-002/003/004/006/007/008/016 |
| E3 Preparación y decisiones de análisis | 1 | TR-001 a TR-004, CSV y evento16 |
| E4 Estadística descriptiva | 1 | STAT-006/009/010/011/012 |
| E5 Variables, agregaciones y relaciones | 1 | STAT-007/008/011/012/013/014 |
| E6 Visualizaciones | 1 | Cuatro PNG válidos |
| E7 Problemas, riesgos y anomalías | 1 | Seis incidencias, decisiones y comprobaciones |
| E8 Informe final | 1 | Alcance, resultados, preparación y límites integrados |

`Q1 = 100 x 8 / 8 = 100,00`

## Q2 Corrección numérica: 89,36

Se cumplen 28 de las 32 comprobaciones previstas, que suman 42 de los 47 puntos ponderados.

| Controles | Resultado | Evidencia o motivo |
| --- | --- | --- |
| C01–C09 | Correctos | Estructura, fechas, ausencias y duplicados. STAT-001/002/003/005 |
| C10 | Correcto | Los 541.909 registros originales menos los 5.268 duplicados dan 536.641 registros. STAT-001 y STAT-003. |
| C11–C20 | Correctos | Cardinalidades, C, cantidades negativas, negativos sin C y precios no positivos. STAT-006/007/009 |
| C21 | Correcto | La media de Quantity multiplicada por los 541.909 registros permite obtener 5.176.450 unidades. Se utiliza la precisión conservada en STAT-006. |
| C22–C27 | Correctos | Extremos, neto, positivos y cancelaciones. STAT-006/007/009 |
| C28 | Ausente | No presenta el importe neto después de excluir los duplicados exactos. |
| C29 | Ausente | Presenta los recuentos del Reino Unido y del conjunto completo, pero no su porcentaje. |
| C30 | Ausente | La serie mensual corresponde a importes netos o a registros sin marca de cancelación, no a ventas positivas. Aunque el importe sin cancelaciones de noviembre coincide con la referencia, no se presenta el máximo calculado sobre el grupo requerido. |
| C31 | Correcto | 647 códigos con varias descripciones. STAT-008 y equivalencia externa de conjuntos |
| C32 | Ausente | No presenta la mediana del número de registros por factura. |

`Q2 = 100 x 42 / 47 = 89,36`

## Q3 Validez del tratamiento de los datos: 91,67

Once de doce ámbitos válidos, sin limpieza perjudicial.

| Decisión | Nota | Justificación y evidencia |
| --- | ---: | --- |
| D01 Identificadores | 1 | Texto nominal, valores y ausencias conservados. TR-001 y CSV |
| D02 Fecha-hora | 1 | El CSV conserva la fecha y la hora de todos los registros en formato ISO 8601. TR-002. |
| D03 Importe | 1 | Identidad correcta y poblaciones declaradas. STAT-007/009/010/015 |
| D04 Unidades | 1 | Distingue líneas, facturas, clientes y pares de artículo/descripción |
| D05 Cancelaciones | 1 | C conservado, identificado y cuantificado. STAT-007 |
| D06 Cliente ausente | 1 | Retiene filas globales e informa cobertura. STAT-002/012 |
| D07 Descripción ausente | 1 | Retiene ausencias, sin inventar etiquetas en las filas |
| D08 Duplicados | 0 | Conserva los duplicados, pero no compara los resultados con y sin esas filas. ISSUE-003. |
| D09 Ajustes | 1 | Identifica por separado las cantidades negativas sin marca de cancelación, los precios cero y los precios negativos. STAT-006/007/010. |
| D10 Extremos | 1 | Conserva los valores extremos y los describe mediante cuantiles y comprobaciones IQR. STAT-006/016. |
| D11 Mes final | 1 | Diciembre 2011 marcado como parcial. STAT-005, ISSUE-004 |
| D12 Categorías | 1 | Limita los gráficos a las categorías principales y conserva el detalle original. FIG-002/004. |

`Q3 = 100 x 11 / 12 = 91,67`

## Q4 Detección de problemas y riesgos: 90,45

Se detectan por completo nueve de los diez riesgos de referencia (K = 9), se identifica un riesgo adicional válido (A = 1) y se registra una afirmación sin respaldo suficiente (F = 1). Diez de los once hallazgos son válidos, lo que da una precisión del 90,91 %, mientras que la cobertura de los riesgos de referencia es del 90 %. Ambas medidas se combinan mediante F1 para obtener la puntuación de Q4.

| Riesgo | Resultado | Evidencia |
| --- | --- | --- |
| R01 Ausencias | Detectado | STAT-002, ISSUE-001/002 |
| R02 Duplicados | Detectado | STAT-003, ISSUE-003 |
| R03 Cancelaciones y signos | Detectado | STAT-007, informe7/47 |
| R04 Negativos sin C | Detectado | 1336 casos aislados en STAT-007 e informe47 |
| R05 Precios cero y negativos | Detectado | STAT-006/010 e ISSUE-005 |
| R06 Unidad e identificadores | Detectado | Perfil, TR-001, plan e informe15/23/95 |
| R07 Mes final parcial | Detectado | STAT-005, ISSUE-004 |
| R08 Concentración UK | Detectado | Conteos originales en STAT-009/011 e interpretación en informe9/51 |
| R09 Asimetría y extremos | Detectado | STAT-006/016, ISSUE-005 |
| R10 Definiciones monetarias | Parcial | Neto, positivos y C presentes, sin efecto de deduplicar |
| A01 Códigos y descripciones sin correspondencia única | Adicional válido | Un mismo código tiene varias descripciones y una misma descripción corresponde a varios códigos. STAT-008, ISSUE-006 y línea 55 del informe |
| F01 Diciembre 2010 incompleto | Sin respaldo | ISSUE-004 e informe9/49/61/107. Empezar el día1 no acredita truncamiento mensual |

`Q4 = 100 x [2 x (10 / 11) x (9 / 10)] / [(10 / 11) + (9 / 10)] = 90,45`

## Q5 Calidad y profundidad del EDA: 75,00

El análisis examina la evolución temporal, países, artículos, signos, ausencias conjuntas, disponibilidad del identificador de cliente, relaciones entre códigos y descripciones y valores extremos. Recibe 3 de 4 puntos porque no cuantifica el efecto de excluir duplicados ni completa la comparación mensual de ventas positivas.

Evidencia: STAT-005/006/007/008/010/011/012/013/014/016.

`Q5 = 100 x 3 / 4 = 75,00`

## Q6 Profundidad de la interpretación: 75,00

El informe distingue los grupos de registros y las unidades analizadas, compara distintas definiciones de importe y explica que la frecuencia y el importe destacan artículos diferentes. Recibe 3 de 4 puntos porque afirma sin respaldo suficiente que diciembre de 2010 está incompleto y no desarrolla el efecto de los duplicados sobre los resultados.

Evidencia: líneas 5/7/39/45/49/51/55/61/93/97 del informe.

`Q6 = 100 x 3 / 4 = 75,00`

## Q7 Calidad de las visualizaciones: 60,00

Las puntuaciones 4, 0, 2, 2 y 4 suman 12/20, equivalentes a 60,00.

| Objetivo | Nota 0–4 | Justificación |
| --- | ---: | --- |
| V01 Evolución | 4 | FIG-001 mensual neta, definición y unidades claras, máximo y mes final explicados |
| V02 Cancelaciones/ajustes | 0 | Ninguna figura representa por separado la frecuencia o el importe de cancelaciones y ajustes |
| V03 Distribuciones | 2 | FIG-003 solo muestra importes positivos y representa los superiores al percentil 99 con el valor de ese límite. No permite ver el alcance real de los extremos ni los valores cero o negativos |
| V04 Países | 2 | FIG-002 representa correctamente los importes, pero el valor del Reino Unido dificulta comparar los demás países |
| V05 Productos/conceptos | 4 | FIG-004 muestra los diez pares de código y descripción con más registros, con códigos legibles y una métrica definida. Líneas 53/73 del informe |

`Q7 = 100 x 12 / 20 = 60,00`

## Q8 Cobertura del informe: 81,82

| Unidad | Peso | Nota | Evidencia o motivo |
| --- | ---: | ---: | --- |
| U01 Estructura y periodo | 2 | 1 | Informe3/13/17/21 |
| U02 Ausencias e impacto | 2 | 1 | Informe27/77/79/89 |
| U03 Unidades | 2 | 1 | Informe15/31/51/55 |
| U04 Duplicados y decisión | 2 | 1 | Informe29/81 |
| U05 C y negativos | 2 | 1 | Informe7/47 |
| U06 Ajustes | 2 | 0,5 | Comunica cantidades negativas sin marca de cancelación e importes cero, pero no identifica por separado los precios cero y negativos |
| U07 Agregados monetarios | 2 | 0,5 | Comunica importes netos, positivos y de cancelaciones, pero no el efecto de excluir duplicados |
| U08 Evolución y mes final | 2 | 0,5 | Describe la evolución y la cobertura incompleta de diciembre de 2011, pero no comunica el máximo mensual de las ventas positivas |
| U09 Concentración UK | 2 | 1 | Informe9/51/65, con cautela sobre comparaciones no ajustadas |
| U10 Cardinalidad y conceptos | 1 | 0,5 | Comunica el elevado número de códigos distintos e incluye DOTCOM POSTAGE, pero no explica que algunos códigos representan gastos de envío o ajustes |
| U11 Asimetría y extremos | 2 | 1 | Informe33/35/37/85 |
| U12 Cobertura y límites | 1 | 0,5 | Explica las ausencias y la incertidumbre sobre ajustes y duplicados, pero no indica que los datos proceden de una sola empresa |

`Q8 = 100 x 18 / 22 = 81,82`

## Q9 Fidelidad del informe: 99,38

Se respaldan 160 de las 161 afirmaciones evaluadas. AF161 carece de respaldo suficiente porque el informe presenta diciembre de 2010 como incompleto sin evidencia que permita demostrarlo.

El inventario situado al final de esta ficha recoge las afirmaciones revisadas, su clasificación y las evidencias utilizadas.

`Q9 = 100 x 160 / 161 = 99,38`

## Q10 Claridad y coherencia: 75,00

El informe presenta una estructura ordenada y referencias claras. Recibe 3 de 4 puntos porque desarrolla poco el significado de algunas variables, afirma sin respaldo suficiente que diciembre de 2010 está incompleto y denomina "nulos" a importes iguales a cero, lo que puede confundirse con datos ausentes.

`Q10 = 100 x 3 / 4 = 75,00`

## Inventario de afirmaciones

R = respaldada. S = sin respaldo suficiente.

| ID | Líneas del informe | Afirmación | Estado | Evidencia |
| --- | --- | --- | --- | --- |
| AF001 | 3/13/15/17/21/101 | Libro XLSX con hoja Online Retail | R | STAT-001/005/009, perfil y diccionario público |
| AF002 | 3/13/15/17/21/101 | 541909 líneas originales | R | STAT-001/005/009, perfil y diccionario público |
| AF003 | 3/13/15/17/21/101 | Ocho variables fuente | R | STAT-001/005/009, perfil y diccionario público |
| AF004 | 3/13/15/17/21/101 | Lista de ocho campos fuente correcta | R | STAT-001/005/009, perfil y diccionario público |
| AF005 | 3/13/15/17/21/101 | Una fila es una línea de factura | R | STAT-001/005/009, perfil y diccionario público |
| AF006 | 3/13/15/17/21/101 | Una fila no equivale a factura completa | R | STAT-001/005/009, perfil y diccionario público |
| AF007 | 3/13/15/17/21/101 | Una fila no equivale a compra completa | R | STAT-001/005/009, perfil y diccionario público |
| AF008 | 3/13/15/17/21/101 | Una fila no equivale a cliente | R | STAT-001/005/009, perfil y diccionario público |
| AF009 | 3/13/15/17/21/101 | Conteos de filas, facturas y clientes no son intercambiables | R | STAT-001/005/009, perfil y diccionario público |
| AF010 | 3/13/15/17/21/101 | Primer registro 2010-12-01T08:26:00 | R | STAT-001/005/009, perfil y diccionario público |
| AF011 | 3/13/15/17/21/101 | Último registro 2011-12-09T12:50:00 | R | STAT-001/005/009, perfil y diccionario público |
| AF012 | 3/13/15/17/21/101 | Trece meses calendario observados | R | STAT-001/005/009, perfil y diccionario público |
| AF013 | 3/13/15/17/21/101 | Alcance descriptivo sin causalidad, rentabilidad ni extrapolación externa | R | STAT-001/005/009, perfil y diccionario público |
| AF014 | 3/13/21/23/25/101 | El archivo original no se modificó | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF015 | 3/13/21/23/25/101 | Se conservaron 541909 filas | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF016 | 3/13/21/23/25/101 | Copia preparada con doce columnas | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF017 | 3/13/21/23/25/101 | Se añadieron cuatro variables analíticas | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF018 | 3/13/21/23/25/101 | Las cuatro derivadas se llaman is_cancellation, line_amount, invoice_month y customer_id_available | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF019 | 3/13/21/23/25/101 | InvoiceNo tratado como identificador nominal de texto | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF020 | 3/13/21/23/25/101 | StockCode tratado como identificador nominal de texto | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF021 | 3/13/21/23/25/101 | CustomerID tratado como identificador nominal nullable | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF022 | 3/13/21/23/25/101 | InvoiceDate conservó fecha y hora | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF023 | 3/13/21/23/25/101 | InvoiceDate exportada en ISO8601 | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF024 | 3/13/21/23/25/101 | Description recortada en espacios periféricos | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF025 | 3/13/21/23/25/101 | Country recortada en espacios periféricos | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF026 | 3/13/21/23/25/101 | No hubo imputación | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF027 | 3/13/21/23/25/101 | Se conservaron cancelaciones | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF028 | 3/13/21/23/25/101 | Se conservaron importes negativos | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF029 | 3/13/21/23/25/101 | Se conservaron importes cero | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF030 | 3/13/21/23/25/101 | Se conservaron extremos | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF031 | 3/13/21/23/25/101 | Se conservaron ausencias | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF032 | 3/13/21/23/25/101 | Se conservaron filas repetidas | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF033 | 3/13/21/23/25/101 | La conservación evita clasificar automáticamente operaciones inciertas como errores | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF034 | 3/13/21/23/25/101 | Las transformaciones tienen justificación en TR-001 a TR-004 | R | CSV, TR-001 a TR-004, evento16 y hashes de cierre |
| AF035 | 5/7/9/31/45/49/51/55/103/105 | line_amount definido como Quantity por UnitPrice | R | STAT-005/007/009/011/013/015 |
| AF036 | 5/7/9/31/45/49/51/55/103/105 | Valor neto incluye importes negativos | R | STAT-005/007/009/011/013/015 |
| AF037 | 5/7/9/31/45/49/51/55/103/105 | Valor neto 9747747,93 GBP | R | STAT-005/007/009/011/013/015 |
| AF038 | 5/7/9/31/45/49/51/55/103/105 | Valor positivo 10666684,54 GBP | R | STAT-005/007/009/011/013/015 |
| AF039 | 5/7/9/31/45/49/51/55/103/105 | Las definiciones de población alteran la suma monetaria | R | STAT-005/007/009/011/013/015 |
| AF040 | 5/7/9/31/45/49/51/55/103/105 | C identifica cancelaciones según documentación | R | STAT-005/007/009/011/013/015 |
| AF041 | 5/7/9/31/45/49/51/55/103/105 | 9288 líneas C | R | STAT-005/007/009/011/013/015 |
| AF042 | 5/7/9/31/45/49/51/55/103/105 | 3836 facturas C | R | STAT-005/007/009/011/013/015 |
| AF043 | 5/7/9/31/45/49/51/55/103/105 | Importe C -896812,49 GBP | R | STAT-005/007/009/011/013/015 |
| AF044 | 5/7/9/31/45/49/51/55/103/105 | 532621 líneas sin C | R | STAT-005/007/009/011/013/015 |
| AF045 | 5/7/9/31/45/49/51/55/103/105 | Importe sin C 10644560,42 GBP | R | STAT-005/007/009/011/013/015 |
| AF046 | 5/7/9/31/45/49/51/55/103/105 | Sin C aún existen importes negativos | R | STAT-005/007/009/011/013/015 |
| AF047 | 5/7/9/31/45/49/51/55/103/105 | Sin C aún existen importes cero | R | STAT-005/007/009/011/013/015 |
| AF048 | 5/7/9/31/45/49/51/55/103/105 | UK neto 8187806,36 GBP | R | STAT-005/007/009/011/013/015 |
| AF049 | 5/7/9/31/45/49/51/55/103/105 | UK 495478 líneas | R | STAT-005/007/009/011/013/015 |
| AF050 | 5/7/9/31/45/49/51/55/103/105 | Noviembre2011 máximo mensual neto | R | STAT-005/007/009/011/013/015 |
| AF051 | 5/7/9/31/45/49/51/55/103/105 | Noviembre2011 neto 1461756,25 GBP | R | STAT-005/007/009/011/013/015 |
| AF052 | 5/7/9/31/45/49/51/55/103/105 | 25900 facturas distintas originales | R | STAT-005/007/009/011/013/015 |
| AF053 | 5/7/9/31/45/49/51/55/103/105 | 4070 StockCode distintos | R | STAT-005/007/009/011/013/015 |
| AF054 | 5/7/9/31/45/49/51/55/103/105 | 4372 clientes distintos identificados | R | STAT-005/007/009/011/013/015 |
| AF055 | 5/7/9/31/45/49/51/55/103/105 | 38 países | R | STAT-005/007/009/011/013/015 |
| AF056 | 5/7/9/31/45/49/51/55/103/105 | Error máximo de identidad del importe igual a cero en memoria | R | STAT-005/007/009/011/013/015 |
| AF057 | 5/7/9/31/45/49/51/55/103/105 | El importe derivado no es una medida independiente de Quantity y UnitPrice | R | STAT-005/007/009/011/013/015 |
| AF058 | 5/7/9/31/45/49/51/55/103/105 | Todas las 9288 líneas C tienen Quantity negativa | R | STAT-005/007/009/011/013/015 |
| AF059 | 5/7/9/31/45/49/51/55/103/105 | Todas las 9288 líneas C tienen importe negativo | R | STAT-005/007/009/011/013/015 |
| AF060 | 5/7/9/31/45/49/51/55/103/105 | 1336 cantidades negativas sin C | R | STAT-005/007/009/011/013/015 |
| AF061 | 5/7/9/31/45/49/51/55/103/105 | Dos importes negativos sin C | R | STAT-005/007/009/011/013/015 |
| AF062 | 5/7/9/31/45/49/51/55/103/105 | Abril2011 mínimo neto entre meses completos considerados | R | STAT-005/007/009/011/013/015 |
| AF063 | 5/7/9/31/45/49/51/55/103/105 | Abril2011 neto 493207,12 GBP | R | STAT-005/007/009/011/013/015 |
| AF064 | 5/7/9/31/45/49/51/55/103/105 | Incremento observado septiembre–noviembre2011 | R | STAT-005/007/009/011/013/015 |
| AF065 | 5/7/9/31/45/49/51/55/103/105 | UK 23494 facturas | R | STAT-005/007/009/011/013/015 |
| AF066 | 5/7/9/31/45/49/51/55/103/105 | Netherlands neto 284661,54 GBP | R | STAT-005/007/009/011/013/015 |
| AF067 | 5/7/9/31/45/49/51/55/103/105 | EIRE neto 263276,82 GBP | R | STAT-005/007/009/011/013/015 |
| AF068 | 5/7/9/31/45/49/51/55/103/105 | Germany neto 221698,21 GBP | R | STAT-005/007/009/011/013/015 |
| AF069 | 5/7/9/31/45/49/51/55/103/105 | France neto 197403,90 GBP | R | STAT-005/007/009/011/013/015 |
| AF070 | 5/7/9/31/45/49/51/55/103/105 | Ranking geográfico no ajustado por clientes | R | STAT-005/007/009/011/013/015 |
| AF071 | 5/7/9/31/45/49/51/55/103/105 | Ranking geográfico no ajustado por cobertura | R | STAT-005/007/009/011/013/015 |
| AF072 | 5/7/9/31/45/49/51/55/103/105 | Ranking geográfico no ajustado por tipo de operación | R | STAT-005/007/009/011/013/015 |
| AF073 | 5/7/9/31/45/49/51/55/103/105 | Par 85123A WHITE HANGING HEART T-LIGHT HOLDER más frecuente | R | STAT-005/007/009/011/013/015 |
| AF074 | 5/7/9/31/45/49/51/55/103/105 | Ese par tiene 2302 líneas | R | STAT-005/007/009/011/013/015 |
| AF075 | 5/7/9/31/45/49/51/55/103/105 | Par DOT DOTCOM POSTAGE máximo neto del ranking | R | STAT-005/007/009/011/013/015 |
| AF076 | 5/7/9/31/45/49/51/55/103/105 | Par DOT tiene 206245,48 GBP netos | R | STAT-005/007/009/011/013/015 |
| AF077 | 5/7/9/31/45/49/51/55/103/105 | Par DOT tiene 709 líneas | R | STAT-005/007/009/011/013/015 |
| AF078 | 5/7/9/31/45/49/51/55/103/105 | Frecuencia e importe destacan conceptos diferentes | R | STAT-005/007/009/011/013/015 |
| AF079 | 5/7/9/31/45/49/51/55/103/105 | 647 códigos con más de una descripción recortada | R | STAT-005/007/009/011/013/015 |
| AF080 | 5/7/9/31/45/49/51/55/103/105 | 177 descripciones con más de un código | R | STAT-005/007/009/011/013/015 |
| AF081 | 5/7/9/31/45/49/51/55/103/105 | StockCode–Description no estrictamente uno a uno | R | STAT-005/007/009/011/013/015 |
| AF082 | 5/7/9/31/45/49/51/55/103/105 | Los rankings usan pares StockCode–Description | R | STAT-005/007/009/011/013/015 |
| AF083 | 5/7/9/31/45/49/51/55/103/105 | El importe neto redondea a 9,75 millones GBP | R | STAT-005/007/009/011/013/015 |
| AF084 | 27/33/35/37/39/81/85 | CustomerID ausente en 135080 líneas | R | STAT-002/003/006/010/012/016 e incidencias |
| AF085 | 27/33/35/37/39/81/85 | CustomerID ausente en 24,93% de líneas | R | STAT-002/003/006/010/012/016 e incidencias |
| AF086 | 27/33/35/37/39/81/85 | Description ausente en 1454 líneas | R | STAT-002/003/006/010/012/016 e incidencias |
| AF087 | 27/33/35/37/39/81/85 | Description ausente en 0,27% de líneas | R | STAT-002/003/006/010/012/016 e incidencias |
| AF088 | 27/33/35/37/39/81/85 | Todas las ausencias Description coinciden con CustomerID ausente | R | STAT-002/003/006/010/012/016 e incidencias |
| AF089 | 27/33/35/37/39/81/85 | 133626 líneas con CustomerID ausente y Description presente | R | STAT-002/003/006/010/012/016 e incidencias |
| AF090 | 27/33/35/37/39/81/85 | 5268 duplicados exactos después del primero | R | STAT-002/003/006/010/012/016 e incidencias |
| AF091 | 27/33/35/37/39/81/85 | Duplicados 0,97% | R | STAT-002/003/006/010/012/016 e incidencias |
| AF092 | 27/33/35/37/39/81/85 | Origen técnico o legítimo de duplicados no resuelto | R | STAT-002/003/006/010/012/016 e incidencias |
| AF093 | 27/33/35/37/39/81/85 | Mediana Quantity igual a3 | R | STAT-002/003/006/010/012/016 e incidencias |
| AF094 | 27/33/35/37/39/81/85 | P99 Quantity igual a100 | R | STAT-002/003/006/010/012/016 e incidencias |
| AF095 | 27/33/35/37/39/81/85 | Quantity máxima80995 | R | STAT-002/003/006/010/012/016 e incidencias |
| AF096 | 27/33/35/37/39/81/85 | Quantity mínima-80995 | R | STAT-002/003/006/010/012/016 e incidencias |
| AF097 | 27/33/35/37/39/81/85 | Mediana UnitPrice 2,08 GBP | R | STAT-002/003/006/010/012/016 e incidencias |
| AF098 | 27/33/35/37/39/81/85 | P99 UnitPrice 18 GBP | R | STAT-002/003/006/010/012/016 e incidencias |
| AF099 | 27/33/35/37/39/81/85 | Precio mínimo-11062,06 GBP | R | STAT-002/003/006/010/012/016 e incidencias |
| AF100 | 27/33/35/37/39/81/85 | Precio máximo38970 GBP | R | STAT-002/003/006/010/012/016 e incidencias |
| AF101 | 27/33/35/37/39/81/85 | Mediana importe original 9,75 GBP | R | STAT-002/003/006/010/012/016 e incidencias |
| AF102 | 27/33/35/37/39/81/85 | P95 importe original 59,40 GBP | R | STAT-002/003/006/010/012/016 e incidencias |
| AF103 | 27/33/35/37/39/81/85 | P99 importe original 180 GBP | R | STAT-002/003/006/010/012/016 e incidencias |
| AF104 | 27/33/35/37/39/81/85 | Importe mínimo-168469,60 GBP | R | STAT-002/003/006/010/012/016 e incidencias |
| AF105 | 27/33/35/37/39/81/85 | Importe máximo168469,60 GBP | R | STAT-002/003/006/010/012/016 e incidencias |
| AF106 | 27/33/35/37/39/81/85 | 9290 importes negativos | R | STAT-002/003/006/010/012/016 e incidencias |
| AF107 | 27/33/35/37/39/81/85 | 2515 importes cero | R | STAT-002/003/006/010/012/016 e incidencias |
| AF108 | 27/33/35/37/39/81/85 | Quantity asimétrica y extrema | R | STAT-002/003/006/010/012/016 e incidencias |
| AF109 | 27/33/35/37/39/81/85 | UnitPrice asimétrico y extremo | R | STAT-002/003/006/010/012/016 e incidencias |
| AF110 | 27/33/35/37/39/81/85 | Importe asimétrico y extremo | R | STAT-002/003/006/010/012/016 e incidencias |
| AF111 | 27/33/35/37/39/81/85 | Medias y sumas sensibles a colas y ajustes | R | STAT-002/003/006/010/012/016 e incidencias |
| AF112 | 27/33/35/37/39/81/85 | Se acompañan con cuantiles | R | STAT-002/003/006/010/012/016 e incidencias |
| AF113 | 27/33/35/37/39/81/85 | Mediana importe sin C 9,90 GBP | R | STAT-002/003/006/010/012/016 e incidencias |
| AF114 | 27/33/35/37/39/81/85 | P99 importe sin C aproximadamente183,50 GBP | R | STAT-002/003/006/010/012/016 e incidencias |
| AF115 | 27/33/35/37/39/81/85 | 2515 importes cero sin C | R | STAT-002/003/006/010/012/016 e incidencias |
| AF116 | 27/33/35/37/39/81/85 | No C no garantiza venta regular validada | R | STAT-002/003/006/010/012/016 e incidencias |
| AF117 | 27/33/35/37/39/81/85 | 406829 líneas con CustomerID disponible | R | STAT-002/003/006/010/012/016 e incidencias |
| AF118 | 27/33/35/37/39/81/85 | Mediana importe identificado 11,10 GBP | R | STAT-002/003/006/010/012/016 e incidencias |
| AF119 | 27/33/35/37/39/81/85 | Mediana importe no identificado 4,96 GBP | R | STAT-002/003/006/010/012/016 e incidencias |
| AF120 | 27/33/35/37/39/81/85 | No se explica causalmente la ausencia de cliente | R | STAT-002/003/006/010/012/016 e incidencias |
| AF121 | 27/33/35/37/39/81/85 | 58619 Quantity fuera de vallas IQR | R | STAT-002/003/006/010/012/016 e incidencias |
| AF122 | 27/33/35/37/39/81/85 | 39627 UnitPrice fuera de vallas IQR | R | STAT-002/003/006/010/012/016 e incidencias |
| AF123 | 27/33/35/37/39/81/85 | 44997 importes fuera de vallas IQR | R | STAT-002/003/006/010/012/016 e incidencias |
| AF124 | 27/33/35/37/39/81/85 | Esos cribados no son recuentos de errores | R | STAT-002/003/006/010/012/016 e incidencias |
| AF125 | 27/33/35/37/39/81/85 | Los valores señalados se conservaron | R | STAT-002/003/006/010/012/016 e incidencias |
| AF126 | 59/61/63/65/67/69/71/73 | FIG-001 muestra evolución mensual neta | R | Cuatro PNG abiertos, STAT-005/010/011/013/016 y evento16 |
| AF127 | 59/61/63/65/67/69/71/73 | FIG-001 incorpora cancelaciones y ajustes en su agregado | R | Cuatro PNG abiertos, STAT-005/010/011/013/016 y evento16 |
| AF128 | 59/61/63/65/67/69/71/73 | FIG-002 top10 países por importe neto | R | Cuatro PNG abiertos, STAT-005/010/011/013/016 y evento16 |
| AF129 | 59/61/63/65/67/69/71/73 | UK domina el importe de los países representados | R | Cuatro PNG abiertos, STAT-005/010/011/013/016 y evento16 |
| AF130 | 59/61/63/65/67/69/71/73 | FIG-003 usa solo importes positivos sin C | R | Cuatro PNG abiertos, STAT-005/010/011/013/016 y evento16 |
| AF131 | 59/61/63/65/67/69/71/73 | FIG-003 limita representación superior a p99 | R | Cuatro PNG abiertos, STAT-005/010/011/013/016 y evento16 |
| AF132 | 59/61/63/65/67/69/71/73 | La limitación gráfica no elimina filas preparadas | R | Cuatro PNG abiertos, STAT-005/010/011/013/016 y evento16 |
| AF133 | 59/61/63/65/67/69/71/73 | La limitación gráfica no altera agregados | R | Cuatro PNG abiertos, STAT-005/010/011/013/016 y evento16 |
| AF134 | 59/61/63/65/67/69/71/73 | FIG-004 muestra diez pares por frecuencia de líneas | R | Cuatro PNG abiertos, STAT-005/010/011/013/016 y evento16 |
| AF135 | 59/61/63/65/67/69/71/73 | FIG-004 no representa todas las categorías | R | Cuatro PNG abiertos, STAT-005/010/011/013/016 y evento16 |
| AF136 | 77/79/81/83/87/89/91/93/95/97/107 | CustomerID ausente limita análisis por cliente | R | Diccionario, STAT-002/003/005/007/008/015 e incidencias |
| AF137 | 77/79/81/83/87/89/91/93/95/97/107 | No se imputó CustomerID | R | Diccionario, STAT-002/003/005/007/008/015 e incidencias |
| AF138 | 77/79/81/83/87/89/91/93/95/97/107 | Las métricas de clientes requieren declarar identificadores disponibles | R | Diccionario, STAT-002/003/005/007/008/015 e incidencias |
| AF139 | 77/79/81/83/87/89/91/93/95/97/107 | Description ausente puede limitar rankings por descripción | R | Diccionario, STAT-002/003/005/007/008/015 e incidencias |
| AF140 | 77/79/81/83/87/89/91/93/95/97/107 | No existe clave adicional de línea en las ocho columnas | R | Diccionario, STAT-002/003/005/007/008/015 e incidencias |
| AF141 | 77/79/81/83/87/89/91/93/95/97/107 | Diciembre 2011 termina el día9 | R | Diccionario, STAT-002/003/005/007/008/015 e incidencias |
| AF142 | 77/79/81/83/87/89/91/93/95/97/107 | Diciembre 2011 no es un mes calendario completo | R | Diccionario, STAT-002/003/005/007/008/015 e incidencias |
| AF143 | 77/79/81/83/87/89/91/93/95/97/107 | Diciembre 2010 es el mes inicial del registro | R | Diccionario, STAT-002/003/005/007/008/015 e incidencias |
| AF144 | 77/79/81/83/87/89/91/93/95/97/107 | No se conoce la comparabilidad de la población sin cliente | R | Diccionario, STAT-002/003/005/007/008/015 e incidencias |
| AF145 | 77/79/81/83/87/89/91/93/95/97/107 | C no explica todas las cantidades negativas | R | Diccionario, STAT-002/003/005/007/008/015 e incidencias |
| AF146 | 77/79/81/83/87/89/91/93/95/97/107 | C no explica todos los importes negativos | R | Diccionario, STAT-002/003/005/007/008/015 e incidencias |
| AF147 | 77/79/81/83/87/89/91/93/95/97/107 | C no explica ceros, códigos especiales ni extremos | R | Diccionario, STAT-002/003/005/007/008/015 e incidencias |
| AF148 | 77/79/81/83/87/89/91/93/95/97/107 | El importe calculado no certifica ingresos contables | R | Diccionario, STAT-002/003/005/007/008/015 e incidencias |
| AF149 | 77/79/81/83/87/89/91/93/95/97/107 | El importe no mide margen | R | Diccionario, STAT-002/003/005/007/008/015 e incidencias |
| AF150 | 77/79/81/83/87/89/91/93/95/97/107 | El importe no mide rentabilidad | R | Diccionario, STAT-002/003/005/007/008/015 e incidencias |
| AF151 | 77/79/81/83/87/89/91/93/95/97/107 | No hay campos independientes de impuestos | R | Diccionario, STAT-002/003/005/007/008/015 e incidencias |
| AF152 | 77/79/81/83/87/89/91/93/95/97/107 | No hay campos independientes de descuentos | R | Diccionario, STAT-002/003/005/007/008/015 e incidencias |
| AF153 | 77/79/81/83/87/89/91/93/95/97/107 | No hay enlaces explícitos de devoluciones a ventas | R | Diccionario, STAT-002/003/005/007/008/015 e incidencias |
| AF154 | 77/79/81/83/87/89/91/93/95/97/107 | No hay campos de costes | R | Diccionario, STAT-002/003/005/007/008/015 e incidencias |
| AF155 | 77/79/81/83/87/89/91/93/95/97/107 | No hay moneda alternativa documentada | R | Diccionario, STAT-002/003/005/007/008/015 e incidencias |
| AF156 | 77/79/81/83/87/89/91/93/95/97/107 | Alta cardinalidad de categorías | R | Diccionario, STAT-002/003/005/007/008/015 e incidencias |
| AF157 | 77/79/81/83/87/89/91/93/95/97/107 | Rankings no son catálogo depurado | R | Diccionario, STAT-002/003/005/007/008/015 e incidencias |
| AF158 | 77/79/81/83/87/89/91/93/95/97/107 | Rankings no son cuota completa de productos | R | Diccionario, STAT-002/003/005/007/008/015 e incidencias |
| AF159 | 77/79/81/83/87/89/91/93/95/97/107 | Comparaciones entre grupos no establecen causalidad | R | Diccionario, STAT-002/003/005/007/008/015 e incidencias |
| AF160 | 93 | El importe no incluye evidencia sobre envío | R | La línea 93 expresa una limitación de la información disponible sobre los envíos. La presencia de DOTCOM POSTAGE acredita cargos registrados, no entregas ni costes de envío confirmados. |
| AF161 | 9/49/61/97/107 | Diciembre 2010 es incompleto y no debe compararse con meses completos por ser el mes inicial | S | La primera fecha es el día1. Ni el horario de la primera transacción ni ser mes inicial acreditan truncamiento mensual. ISSUE-004 repite la inferencia sin demostrarla. |
