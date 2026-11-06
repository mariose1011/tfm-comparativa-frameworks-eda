# Evaluación D2-LG-R1

**Índice final:** 82,91/100.  
**Evaluación cerrada:** 6 de octubre de 2026.  
**Ejecución:** `D2_online_retail__langgraph__r01__20260902T170409927746Z`

**Criterios:** [Protocolo de evaluación](../01_protocolo_calidad_Q1_Q10_v0.1.md) y [guía D2](../02_ficha_D2_online_retail.md).  
**Resultados:** [Archivos originales de la ejecución](../../../outputs/experimento/D2_online_retail__langgraph__r01__20260902T170409927746Z).  
**Evaluación:** [Excel de puntuaciones](../Evaluacion_calidad.xlsx) y [JSON de comprobaciones](D2-LG-R1_comprobaciones.json).

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
| Q7 Calidad de las visualizaciones | 50,00 |
| Q8 Cobertura del informe | 90,91 |
| Q9 Fidelidad del informe | 99,45 |
| Q10 Claridad y coherencia | 75,00 |

## Q1 Cumplimiento de las etapas: 100,00

| Etapa | Nota | Evidencia |
| --- | ---: | --- |
| E1 Carga e inspección inicial | 1 | STAT-001 y profile |
| E2 Estructura, tipos y calidad | 1 | STAT-002 a STAT-006 |
| E3 Preparación y decisiones de análisis | 1 | TR-001 a TR-004, STAT-007 y CSV de 541909 x 11 |
| E4 Estadística descriptiva | 1 | STAT-006/008/009/010/011 |
| E5 Variables, agregaciones y relaciones | 1 | STAT-012/013/014 y agregaciones por cliente y país |
| E6 Visualizaciones | 1 | Cuatro PNG legibles e identificados. V05 ausente se puntúa en Q7 |
| E7 Problemas, riesgos y anomalías | 1 | Siete comprobaciones y seis incidencias con evidencias y decisiones |
| E8 Informe final | 1 | Informe evaluable con las secciones requeridas |

`Q1 = 100 x 8 / 8 = 100,00`

## Q2 Corrección numérica: 82,98

Se obtienen resultados correctos en 26 de las 32 comprobaciones, que suman 39 de los 47 puntos posibles.

| Controles | Resultado | Evidencia o motivo |
| --- | --- | --- |
| C01–C07 | Correctos | Estructura, fechas, nulos y sus marginales, STAT-001/002/005 |
| C08 | Ausente | No se produjo el cruce de ausencias CustomerID–Description |
| C09 | Correcto | 5268 duplicados exactos, STAT-003 |
| C10 | Correcto | C01 (STAT-001.rows) menos C09 (STAT-003.exact_duplicate_rows): 541909 − 5268 = 536641. Tamaño hipotético sin duplicados, no eliminación ejecutada. |
| C11–C20 | Correctos | Cardinalidades, cancelaciones, signos y ceros, STAT-006/008/009 |
| C21–C24 | Correctos | Cantidad e importe de la partición exhaustiva C, extremos de Quantity |
| C25 | Correcto | STAT-013.filter_lines = 530104. El filtro coincide fila a fila con las ventas positivas en esta entrada |
| C26 | Ausente | No presenta el importe de las ventas positivas, calculado sobre registros con cantidad y precio mayores que cero. El importe comunicado corresponde a los registros sin marca de cancelación, un grupo diferente. |
| C27 | Correcto | Importe cancelado de −896812,49, STAT-009 |
| C28 | Ausente | Sin valor monetario deduplicado |
| C29 | Ausente | Cuota monetaria no cancelada en lugar de proporción de líneas originales |
| C30 | Ausente | Máximo mensual no cancelado, no máximo calculado sobre ventas positivas |
| C31 | Ausente | 650 códigos con descripciones originales, no los 647 con descripciones normalizadas de la referencia |
| C32 | Correcto | Mediana de 10 líneas por factura, STAT-003 |

C10 se obtiene restando los 5.268 duplicados a las 541.909 filas originales. Esta operación permite conocer el número de filas que quedarían, pero no cuantifica el cambio de los importes y, por tanto, no completa C28.

Para C31 se cuentan códigos con varias descripciones después de eliminar espacios exteriores y convertir el texto a mayúsculas. El análisis obtiene 650 códigos utilizando las descripciones originales, una definición distinta de la referencia.

`Q2 = 100 x 39 / 47 = 82,98`

## Q3 Validez del tratamiento de los datos: 91,67

| Decisión | Nota | Justificación y evidencia |
| --- | ---: | --- |
| D01 Identificadores | 1 | Texto nominal y CustomerID nullable. TR-001, código16 y CSV |
| D02 Fecha-hora | 1 | InvoiceDate ISO conserva fecha y hora en todas las filas. TR-002 |
| D03 Importe de línea | 1 | Producto Quantity x UnitPrice y agregados definidos, STAT-009/014 |
| D04 Unidades | 1 | Distingue líneas, facturas, clientes y conceptos, report3/35/53/55 |
| D05 Cancelaciones | 1 | Prefijo C conservado y analizado por separado, STAT-009 |
| D06 Cliente ausente | 1 | Se mantiene en globales, se excluye solo del análisis de clientes y se comunica cobertura, STAT-002/011 |
| D07 Descripción ausente | 1 | No se inventan descripciones. Filtro de ranking declarado, STAT-013 |
| D08 Duplicados | 0 | Conserva los duplicados y justifica la decisión, pero no compara los agregados con y sin esas filas para cuantificar su efecto. STAT-003 e ISSUE-003 |
| D09 Ajustes y precios | 1 | Cuantifica negativos sin C, ceros y precios negativos, STAT-006/009/014 |
| D10 Extremos | 1 | Conserva extremos y usa cuantiles/IQR como diagnóstico. No elimina según umbral, STAT-006 e ISSUE-004 |
| D11 Diciembre de 2011 | 1 | Advierte que termina el día 9 y evita compararlo como mes completo, report49 |
| D12 Categorías | 1 | Mantiene detalle y limita rankings a diez categorías con filtros declarados |

`Q3 = 100 x 11 / 12 = 91,67`

## Q4 Detección de problemas y riesgos: 85,11

| Riesgo | Clasificación | Evidencia |
| --- | --- | --- |
| R01 Ausencias | Detectado | CustomerID y Description, STAT-002 e ISSUE-001/002 |
| R02 Duplicados | Detectado | 5268 y cautela sobre su naturaleza, report37/81 |
| R03 Cancelaciones | Detectado | C y cantidades negativas, STAT-009 y report43/92 |
| R04 Negativos sin C | Detectado | 1336, STAT-009 y report43 |
| R05 Precios no positivos | Detectado | 2515 ceros y dos negativos, STAT-006 y report41 |
| R06 Unidad y cardinalidad | Detectado | Línea distinta de factura, identificadores nominales y alta cardinalidad, report3/15/35/98 |
| R07 Último mes parcial | Detectado | Diciembre de 2011 hasta el día9, report49 |
| R08 Más del 91 % de líneas en UK | Parcial | Predominio monetario descrito, pero no proporción de líneas de la tabla completa |
| R09 Asimetría y extremos | Detectado | Tres distribuciones completas y diagnóstico IQR, STAT-006 |
| R10 Dependencia de definición monetaria | Parcial | Distingue total y no cancelado, conoce inclusión de duplicados y filtro positivo, pero no completa contraste positivo/neto/deduplicado |
| A01 Códigos y descripciones sin correspondencia única | Adicional válido | Un mismo código tiene varias descripciones y viceversa. STAT-004 e ISSUE-005 |
| A02 Cancelaciones sin vinculación a ventas previas | Adicional válido | No puede vincularse cada cancelación con una venta previa. Líneas 73/92 del informe y estructura del dataset |
| F01 Diciembre de 2010 truncado | Sin respaldo | ISSUE-006 y report47 generalizan el problema del último mes al primero sin justificarlo |

Se identifican ocho riesgos previstos y dos adicionales, y se registra una afirmación de problema sin respaldo. La precisión es 10/11 y la cobertura es 8/10.

`Q4 = 100 x [2 x (10 / 11) x (8 / 10)] / [(10 / 11) + (8 / 10)] = 85,11`

## Q5 Calidad y profundidad del EDA: 75,00

El análisis examina calidad, distribuciones, clientes, países, catálogo y evolución temporal. Recibe 3 de 4 puntos porque no cuantifica el efecto de los duplicados ni compara de forma completa los importes de ventas positivas, todas las líneas y cancelaciones.

`Q5 = 100 x 3 / 4 = 75,00`

## Q6 Profundidad de la interpretación: 75,00

La interpretación distingue líneas, facturas, clientes y conceptos, y reconoce las limitaciones de las medidas monetarias. Recibe 3 de 4 puntos porque presenta diciembre de 2010 como incompleto sin respaldo suficiente y no analiza cómo cambiarían los importes al limitarse a ventas positivas o excluir duplicados.

Evidencia: report7/31/47/49/51/53/55/88/92/94.

`Q6 = 100 x 3 / 4 = 75,00`

## Q7 Calidad de las visualizaciones: 50,00

| Objetivo | Nota | Justificación |
| --- | ---: | --- |
| V01 Evolución | 4 | Serie mensual cronológica, total y no cancelado claramente definidos. Advertencia de diciembre2011 en el informe, FIG-001 |
| V02 Cancelaciones y ajustes | 2 | FIG-004 muestra magnitud cancelada, pero no representa negativos sin C ni precios no positivos como situaciones distintas |
| V03 Distribuciones robustas | 2 | Histograma legible y recorte declarado, pero solo de importes positivos centrales. No hay complemento gráfico para negativos y extremos |
| V04 Concentración geográfica | 2 | Top10 ordenado y correctamente etiquetado, pero el importe del Reino Unido es tan superior al de los demás países que dificulta comparar sus barras entre sí. FIG-002 |
| V05 Productos/clientes | 0 | Rankings numéricos válidos en STAT-011/013 y el informe, pero ninguna figura cubre este objetivo |

`Q7 = 100 x 10 / 20 = 50,00`

## Q8 Cobertura del informe: 90,91

| Unidad | Peso | Nota | Motivo |
| --- | ---: | ---: | --- |
| U01 Estructura y periodo | 2 | 1 | Report3/21/47 |
| U02 Ausencias e impacto | 2 | 1 | Report31/79/80 |
| U03 Unidades distintas | 2 | 1 | Report3/35/53/55 |
| U04 Duplicados y decisión | 2 | 1 | Report37/81. Esta unidad no exige toda la sensibilidad de D08 |
| U05 C y magnitud negativa | 2 | 1 | Report43 |
| U06 Precios y ajustes | 2 | 1 | Report41/43/82 |
| U07 Definiciones monetarias | 2 | 0,5 | Total, no cancelado y cancelaciones explicados. Falta importe global positivo y efecto monetario de deduplicar |
| U08 Evolución y máximo completo | 2 | 0,5 | Describe evolución y diciembre2011 parcial. El máximo se comunica sobre importe no cancelado, no se calcula sobre venta positiva |
| U09 Predominio geográfico | 2 | 1 | Importe UK y siguientes países, con cautela de no equiparar a tamaño de mercado, report51/65 |
| U10 Productos y conceptos | 1 | 1 | Alta cardinalidad y gastos de envío y operaciones manuales explícitos, report55/83/98 |
| U11 Asimetría y extremos | 2 | 1 | Descriptivos de las tres variables, report39/41 |
| U12 Cobertura y límites | 1 | 1 | Empresa, periodo, ausencias e incertidumbre sobre ajustes y duplicados cubiertos. La afirmación adicional sobre diciembre2010 mantiene su valoración en Q4/Q6/Q9 |

`Q8 = 100 x 20 / 22 = 90,91`

## Q9 Fidelidad del informe: 99,45

Se respaldan 182 de las 183 afirmaciones evaluadas. AF118 carece de respaldo suficiente porque el informe presenta diciembre de 2010 como un mes incompleto por ser el primero del periodo, aunque los datos comienzan el día 1 y no se aporta evidencia de registros ausentes.

El inventario situado al final de esta ficha recoge las afirmaciones revisadas, su clasificación y las evidencias utilizadas.

`Q9 = 100 x 182 / 183 = 99,45`

## Q10 Claridad y coherencia: 75,00

El informe está organizado y presenta sus filtros y limitaciones. Recibe 3 de 4 puntos porque "no hay fechas ausentes" puede confundirse con ausencia de días sin actividad y porque en el párrafo de noviembre, el importe excluye las cancelaciones, pero los recuentos de líneas y facturas las incluyen, sin aclarar esta diferencia.

Evidencia: Informe, líneas 47 y 49; STAT-005 y STAT-012.

`Q10 = 100 x 3 / 4 = 75,00`

## Inventario de afirmaciones

R = respaldada; S = sin respaldo suficiente

| ID | Líneas del informe | Afirmación | Estado | Evidencia |
| --- | --- | --- | --- | --- |
| AF001 | 3,13,15,21 | Formato XLSX, hoja Online Retail | R | STAT-001/008 y Readme |
| AF002 | 3,13,15,21 | Empresa británica de comercio electrónico | R | STAT-001/008 y Readme |
| AF003 | 3,13,15,21 | 541909 líneas originales | R | STAT-001/008 y Readme |
| AF004 | 3,13,15,21 | 8 columnas originales | R | STAT-001/008 y Readme |
| AF005 | 3,13,15,21 | 25900 InvoiceNo distintos | R | STAT-001/008 y Readme |
| AF006 | 3,13,15,21 | 4070 StockCode distintos | R | STAT-001/008 y Readme |
| AF007 | 3,13,15,21 | 4372 clientes identificables distintos | R | STAT-001/008 y Readme |
| AF008 | 3,13,15,21 | 38 países distintos | R | STAT-001/008 y Readme |
| AF009 | 3,13,15,21 | Cada fila es una línea de factura | R | STAT-001/008 y Readme |
| AF010 | 3,13,15,21 | Una fila no necesariamente constituye una factura completa | R | STAT-001/008 y Readme |
| AF011 | 3,13,15,21 | Una fila no necesariamente constituye una compra única | R | STAT-001/008 y Readme |
| AF012 | 3,13,15,21 | Una fila no necesariamente constituye un cliente único | R | STAT-001/008 y Readme |
| AF013 | 3,13,15,21 | Una factura puede ocupar varias filas | R | STAT-001/008 y Readme |
| AF014 | 3,13,15,21 | Un cliente puede ocupar varias filas | R | STAT-001/008 y Readme |
| AF015 | 3,13,15,21 | Un producto puede ocupar varias filas | R | STAT-001/008 y Readme |
| AF016 | 3,13,15,21 | Las ocho columnas fuente enumeradas coinciden con la entrada | R | STAT-001/008 y Readme |
| AF017 | 5,23,25,26,27,29 | 541909 filas preparadas | R | CSV, TR-001/002/003/004 y código16 |
| AF018 | 5,23,25,26,27,29 | Identificadores normalizados como texto | R | CSV, TR-001/002/003/004 y código16 |
| AF019 | 5,23,25,26,27,29 | InvoiceDate serializada ISO | R | CSV, TR-001/002/003/004 y código16 |
| AF020 | 5,23,25,26,27,29 | Se añadieron tres campos derivados | R | CSV, TR-001/002/003/004 y código16 |
| AF021 | 5,23,25,26,27,29 | is_cancellation indica InvoiceNo con prefijo C | R | CSV, TR-001/002/003/004 y código16 |
| AF022 | 5,23,25,26,27,29 | line_amount_gbp es Quantity multiplicada por UnitPrice | R | CSV, TR-001/002/003/004 y código16 |
| AF023 | 5,23,25,26,27,29 | invoice_month representa el mes YYYY-MM | R | CSV, TR-001/002/003/004 y código16 |
| AF024 | 5,23,25,26,27,29 | No se eliminaron duplicados | R | CSV, TR-001/002/003/004 y código16 |
| AF025 | 5,23,25,26,27,29 | No se eliminaron filas con ausencias | R | CSV, TR-001/002/003/004 y código16 |
| AF026 | 5,23,25,26,27,29 | No se eliminaron negativos | R | CSV, TR-001/002/003/004 y código16 |
| AF027 | 5,23,25,26,27,29 | No se eliminaron ceros | R | CSV, TR-001/002/003/004 y código16 |
| AF028 | 5,23,25,26,27,29 | No se eliminaron extremos | R | CSV, TR-001/002/003/004 y código16 |
| AF029 | 5,23,25,26,27,29 | CustomerID se mantiene vacío cuando la fuente carece de él | R | CSV, TR-001/002/003/004 y código16 |
| AF030 | 5,23,25,26,27,29 | No se imputaron identificadores | R | CSV, TR-001/002/003/004 y código16 |
| AF031 | 5,23,25,26,27,29 | No se imputaron descripciones | R | CSV, TR-001/002/003/004 y código16 |
| AF032 | 15,21 | InvoiceNo se trata como identificador nominal | R | STAT-001, TR-001 y Readme |
| AF033 | 15,21 | StockCode se trata como identificador nominal | R | STAT-001, TR-001 y Readme |
| AF034 | 15,21 | CustomerID se trata como identificador nominal | R | STAT-001, TR-001 y Readme |
| AF035 | 15,21 | UnitPrice está expresado en GBP | R | STAT-001, TR-001 y Readme |
| AF036 | 15,21 | Quantity cargada como entero | R | STAT-001, TR-001 y Readme |
| AF037 | 15,21 | UnitPrice cargada como numérica decimal | R | STAT-001, TR-001 y Readme |
| AF038 | 15,21 | InvoiceDate cargada como fecha-hora | R | STAT-001, TR-001 y Readme |
| AF039 | 15,21 | Los identificadores tenían representaciones objeto o numéricas antes de normalizar | R | STAT-001, TR-001 y Readme |
| AF040 | 17 | El trabajo es exploratorio y descriptivo | R | STAT-001 a STAT-014 y código16 |
| AF041 | 17 | Se examinan líneas | R | STAT-001 a STAT-014 y código16 |
| AF042 | 17 | Se examinan agregados por factura | R | STAT-001 a STAT-014 y código16 |
| AF043 | 17 | Se examinan meses | R | STAT-001 a STAT-014 y código16 |
| AF044 | 17 | Se examinan países | R | STAT-001 a STAT-014 y código16 |
| AF045 | 17 | Se examinan productos/conceptos | R | STAT-001 a STAT-014 y código16 |
| AF046 | 17 | Se examinan clientes identificables | R | STAT-001 a STAT-014 y código16 |
| AF047 | 17 | No se entrenaron modelos predictivos | R | STAT-001 a STAT-014 y código16 |
| AF048 | 17 | No se realizaron inferencias causales | R | STAT-001 a STAT-014 y código16 |
| AF049 | 7,43,57,73,88 | Importe no cancelado de 10644560,42 GBP | R | STAT-009/014 y diseño de la derivada |
| AF050 | 7,43,57,73,88 | Importe cancelado de -896812,49 GBP | R | STAT-009/014 y diseño de la derivada |
| AF051 | 7,43,57,73,88 | La clasificación de cancelación usa el prefijo C documentado | R | STAT-009/014 y diseño de la derivada |
| AF052 | 7,43,57,73,88 | Son importes aritméticos de línea, no ingresos netos contables verificados | R | STAT-009/014 y diseño de la derivada |
| AF053 | 7,43,57,73,88 | La identidad Quantity por UnitPrice se verifica en todas las filas | R | STAT-009/014 y diseño de la derivada |
| AF054 | 7,43,57,73,88 | La identidad se comprobó en 541909 filas | R | STAT-009/014 y diseño de la derivada |
| AF055 | 7,43,57,73,88 | La relación del importe derivado es constructiva, no independiente | R | STAT-009/014 y diseño de la derivada |
| AF056 | 7,43,57,73,88 | El importe no incorpora reglas contables, impuestos o costes no suministrados | R | STAT-009/014 y diseño de la derivada |
| AF057 | 9,49,51,100 | Reino Unido concentra el 84,579 % del importe no cancelado | R | STAT-010/012 |
| AF058 | 9,49,51,100 | El máximo mensual no cancelado corresponde a noviembre2011 | R | STAT-010/012 |
| AF059 | 9,49,51,100 | El importe no cancelado de noviembre2011 es 1509496,33 GBP | R | STAT-010/012 |
| AF060 | 9,49,51,100 | Reino Unido domina el importe no cancelado | R | STAT-010/012 |
| AF061 | 31,79,80 | CustomerID ausente en 135080 líneas | R | STAT-002/011/013 e ISSUE-001/002 |
| AF062 | 31,79,80 | CustomerID ausente en el 24,927 % de las líneas | R | STAT-002/011/013 e ISSUE-001/002 |
| AF063 | 31,79,80 | Description ausente en 1454 líneas | R | STAT-002/011/013 e ISSUE-001/002 |
| AF064 | 31,79,80 | Description ausente en el 0,268 % de las líneas | R | STAT-002/011/013 e ISSUE-001/002 |
| AF065 | 31,79,80 | Los análisis por cliente solo usan líneas identificadas | R | STAT-002/011/013 e ISSUE-001/002 |
| AF066 | 31,79,80 | Los rankings que exigen Description declaran ese filtro | R | STAT-002/011/013 e ISSUE-001/002 |
| AF067 | 31,79,80 | Los análisis por cliente no cubren toda la actividad | R | STAT-002/011/013 e ISSUE-001/002 |
| AF068 | 35,37,81,90 | Mediana de 10 líneas por factura | R | STAT-003 e ISSUE-003 |
| AF069 | 35,37,81,90 | Máximo de 1114 líneas por factura | R | STAT-003 e ISSUE-003 |
| AF070 | 35,37,81,90 | Repetir InvoiceNo es esperable en datos de líneas | R | STAT-003 e ISSUE-003 |
| AF071 | 35,37,81,90 | Repetir InvoiceNo no se clasificó por sí solo como duplicado | R | STAT-003 e ISSUE-003 |
| AF072 | 35,37,81,90 | Se detectaron 5268 duplicados exactos | R | STAT-003 e ISSUE-003 |
| AF073 | 35,37,81,90 | La documentación no decide si cada duplicado es técnico o legítimo | R | STAT-003 e ISSUE-003 |
| AF074 | 35,37,81,90 | Los conteos incluyen duplicados conservados | R | STAT-003 e ISSUE-003 |
| AF075 | 35,37,81,90 | Las sumas incluyen duplicados conservados | R | STAT-003 e ISSUE-003 |
| AF076 | 35,37,81,90 | Las facturas tienen número variable de líneas | R | STAT-003 e ISSUE-003 |
| AF077 | 35,37,81,90 | Analizar líneas da más peso a facturas con más líneas | R | STAT-003 e ISSUE-003 |
| AF078 | 39 | Mediana Quantity de 3 | R | STAT-006.summary_all |
| AF079 | 39 | Primer cuartil Quantity de 1 | R | STAT-006.summary_all |
| AF080 | 39 | Tercer cuartil Quantity de 10 | R | STAT-006.summary_all |
| AF081 | 39 | Mínimo Quantity de -80995 | R | STAT-006.summary_all |
| AF082 | 39 | Máximo Quantity de 80995 | R | STAT-006.summary_all |
| AF083 | 39 | Mediana UnitPrice de 2,08 GBP | R | STAT-006.summary_all |
| AF084 | 39 | Primer cuartil UnitPrice de 1,25 GBP | R | STAT-006.summary_all |
| AF085 | 39 | Tercer cuartil UnitPrice de 4,13 GBP | R | STAT-006.summary_all |
| AF086 | 39 | Mínimo UnitPrice de -11062,06 GBP | R | STAT-006.summary_all |
| AF087 | 39 | Máximo UnitPrice de 38970 GBP | R | STAT-006.summary_all |
| AF088 | 39 | Mediana de importe de línea de 9,75 GBP | R | STAT-006.summary_all |
| AF089 | 39 | Percentil99 global de importe de línea de 180 GBP | R | STAT-006.summary_all |
| AF090 | 39 | Mínimo de importe de línea de -168469,60 GBP | R | STAT-006.summary_all |
| AF091 | 39 | Máximo de importe de línea de 168469,60 GBP | R | STAT-006.summary_all |
| AF092 | 39 | Las distribuciones presentan fuerte asimetría y extremos | R | STAT-006.summary_all |
| AF093 | 41 | 10624 cantidades negativas | R | STAT-006.sign_zero_counts e IQR |
| AF094 | 41 | Dos precios negativos | R | STAT-006.sign_zero_counts e IQR |
| AF095 | 41 | 2515 precios cero | R | STAT-006.sign_zero_counts e IQR |
| AF096 | 41 | Umbral IQR superior Quantity de 23,5 | R | STAT-006.sign_zero_counts e IQR |
| AF097 | 41 | Umbral IQR superior UnitPrice de 8,45 GBP | R | STAT-006.sign_zero_counts e IQR |
| AF098 | 41 | 56635 líneas no canceladas superan umbral Quantity | R | STAT-006.sign_zero_counts e IQR |
| AF099 | 41 | 37999 líneas no canceladas superan umbral UnitPrice | R | STAT-006.sign_zero_counts e IQR |
| AF100 | 41 | Las reglas IQR se usaron como diagnóstico, no eliminación | R | STAT-006.sign_zero_counts e IQR |
| AF101 | 43 | 9288 líneas de cancelación | R | STAT-009.groups |
| AF102 | 43 | 3836 facturas de cancelación | R | STAT-009.groups |
| AF103 | 43 | Todas las cancelaciones C tienen Quantity negativa | R | STAT-009.groups |
| AF104 | 43 | 532621 líneas no canceladas | R | STAT-009.groups |
| AF105 | 43 | 22064 facturas no canceladas | R | STAT-009.groups |
| AF106 | 43 | Cantidad agregada no cancelada de 5454024 unidades | R | STAT-009.groups |
| AF107 | 43 | 1336 cantidades negativas sin C | R | STAT-009.groups |
| AF108 | 43 | 2515 precios cero en líneas no canceladas | R | STAT-009.groups |
| AF109 | 47,49,84,98 | Primera fecha-hora 2010-12-01T08:26:00 | R | STAT-005/012, rango contrastado |
| AF110 | 47,49,84,98 | Última fecha-hora 2011-12-09T12:50:00 | R | STAT-005/012, rango contrastado |
| AF111 | 47,49,84,98 | 374 días calendario inclusivos | R | STAT-005/012, rango contrastado |
| AF112 | 47,49,84,98 | 305 fechas con registros | R | STAT-005/012, rango contrastado |
| AF113 | 47,49,84,98 | No hay valores InvoiceDate ausentes | R | STAT-005/012, rango contrastado |
| AF114 | 47,49,84,98 | Diciembre2011 solo alcanza el día9 | R | STAT-005/012, rango contrastado |
| AF115 | 47,49,84,98 | Diciembre2011 es parcial frente a un mes calendario completo | R | STAT-005/012, rango contrastado |
| AF116 | 47,49,84,98 | No se anualizaron los agregados mensuales | R | STAT-005/012, rango contrastado |
| AF117 | 47,49,84,98 | No se ajustaron los agregados mensuales | R | STAT-005/012, rango contrastado |
| AF118 | 47,100 | Diciembre2010 tiene cobertura mensual parcial por ser el mes inicial | S | El inicio es el día1 de diciembre2010. El primer horario transaccional no demuestra falta de actividad anterior ni un mes truncado. La documentación no marca diciembre2010 como parcial. |
| AF119 | 49 | Noviembre2011 tiene 84711 líneas totales | R | STAT-005/012.monthly: conteos de todas las líneas, no solo no canceladas |
| AF120 | 49 | Noviembre2011 tiene 3462 facturas totales | R | STAT-005/012.monthly: conteos de todas las líneas, no solo no canceladas |
| AF121 | 49 | Importe no cancelado diciembre2011 de 638792,68 GBP | R | STAT-005/012.monthly: conteos de todas las líneas, no solo no canceladas |
| AF122 | 51 | Importe no cancelado Reino Unido de 9003097,96 GBP | R | STAT-010.top_10 |
| AF123 | 51 | 487622 líneas no canceladas Reino Unido | R | STAT-010.top_10 |
| AF124 | 51 | 20122 facturas no canceladas Reino Unido | R | STAT-010.top_10 |
| AF125 | 51 | Importe no cancelado Netherlands de 285446,34 GBP | R | STAT-010.top_10 |
| AF126 | 51 | Importe no cancelado EIRE de 283453,96 GBP | R | STAT-010.top_10 |
| AF127 | 51 | Importe no cancelado Germany de 228867,14 GBP | R | STAT-010.top_10 |
| AF128 | 51 | Importe no cancelado France de 209715,11 GBP | R | STAT-010.top_10 |
| AF129 | 51 | La concentración geográfica no es una medida de tamaño de mercado | R | STAT-010.top_10 |
| AF130 | 51 | La comparación geográfica no está ajustada por población | R | STAT-010.top_10 |
| AF131 | 53 | 4339 clientes con líneas no canceladas | R | STAT-011, población no cancelada identificada |
| AF132 | 53 | Mediana de importe por cliente de 674,45 GBP | R | STAT-011, población no cancelada identificada |
| AF133 | 53 | Media de importe por cliente de 2053,79 GBP | R | STAT-011, población no cancelada identificada |
| AF134 | 53 | Máximo por cliente de 280206,02 GBP | R | STAT-011, población no cancelada identificada |
| AF135 | 53 | Top10 clientes aporta 17,262 % del importe de población identificada | R | STAT-011, población no cancelada identificada |
| AF136 | 53 | La distribución del importe por cliente tiene cola alta | R | STAT-011, población no cancelada identificada |
| AF137 | 55 | Ranking producido con 530104 líneas | R | STAT-013, filtros y ranking comprobados |
| AF138 | 55 | Ranking excluye líneas C | R | STAT-013, filtros y ranking comprobados |
| AF139 | 55 | Ranking exige Quantity positiva | R | STAT-013, filtros y ranking comprobados |
| AF140 | 55 | Ranking exige UnitPrice positivo | R | STAT-013, filtros y ranking comprobados |
| AF141 | 55 | Ranking exige Description disponible | R | STAT-013, filtros y ranking comprobados |
| AF142 | 55 | DOT y DOTCOM POSTAGE lideran el ranking monetario | R | STAT-013, filtros y ranking comprobados |
| AF143 | 55 | Importe de DOT y DOTCOM POSTAGE de 206248,77 GBP | R | STAT-013, filtros y ranking comprobados |
| AF144 | 55 | 22423 y REGENCY CAKESTAND 3 TIER ocupa el segundo lugar | R | STAT-013, filtros y ranking comprobados |
| AF145 | 55 | Importe de ese segundo concepto de 174484,74 GBP | R | STAT-013, filtros y ranking comprobados |
| AF146 | 55 | 23843 y PAPER CRAFT LITTLE BIRDIE ocupa el tercer lugar | R | STAT-013, filtros y ranking comprobados |
| AF147 | 55 | Importe de ese tercer concepto de 168469,60 GBP | R | STAT-013, filtros y ranking comprobados |
| AF148 | 55 | El tercer concepto tiene una sola línea | R | STAT-013, filtros y ranking comprobados |
| AF149 | 55 | La línea del tercer concepto tiene 80995 unidades | R | STAT-013, filtros y ranking comprobados |
| AF150 | 55 | El ranking incluye envío y operaciones manuales | R | STAT-013, filtros y ranking comprobados |
| AF151 | 55 | No todos los conceptos del ranking son mercancía física | R | STAT-013, filtros y ranking comprobados |
| AF152 | 61,65,69,73 | FIG-001 representa importe mensual de todas las líneas | R | Cuatro PNG abiertos, datos y código16 |
| AF153 | 61,65,69,73 | FIG-001 representa importe mensual no cancelado | R | Cuatro PNG abiertos, datos y código16 |
| AF154 | 61,65,69,73 | Las cancelaciones reducen el total respecto al no cancelado | R | Cuatro PNG abiertos, datos y código16 |
| AF155 | 61,65,69,73 | FIG-002 presenta diez países líderes por importe no cancelado | R | Cuatro PNG abiertos, datos y código16 |
| AF156 | 61,65,69,73 | FIG-002 usa miles de GBP | R | Cuatro PNG abiertos, datos y código16 |
| AF157 | 61,65,69,73 | FIG-002 excluye líneas C | R | Cuatro PNG abiertos, datos y código16 |
| AF158 | 61,65,69,73 | FIG-003 representa solo importes positivos no cancelados | R | Cuatro PNG abiertos, datos y código16 |
| AF159 | 61,65,69,73 | FIG-003 limita la distribución central al percentil99 | R | Cuatro PNG abiertos, datos y código16 |
| AF160 | 61,65,69,73 | El recorte es gráfico y no modifica el CSV | R | Cuatro PNG abiertos, datos y código16 |
| AF161 | 61,65,69,73 | Los resúmenes completos conservan signos y extremos | R | Cuatro PNG abiertos, datos y código16 |
| AF162 | 61,65,69,73 | FIG-004 representa importe positivo agregado no cancelado | R | Cuatro PNG abiertos, datos y código16 |
| AF163 | 61,65,69,73 | FIG-004 representa importe agregado negativo cancelado | R | Cuatro PNG abiertos, datos y código16 |
| AF164 | 61,65,69,73 | FIG-004 usa el estado derivado de InvoiceNo | R | Cuatro PNG abiertos, datos y código16 |
| AF165 | 61,65,69,73 | No se emparejan devoluciones con ventas anteriores | R | Cuatro PNG abiertos, datos y código16 |
| AF166 | 82,83 | Hay dos líneas con importe negativo fuera de C | R | STAT-004/014 e ISSUE-004/005 |
| AF167 | 82,83 | 650 StockCode tienen varias Description sin normalizar | R | STAT-004/014 e ISSUE-004/005 |
| AF168 | 82,83 | 172 Description se asocian con varios StockCode | R | STAT-004/014 e ISSUE-004/005 |
| AF169 | 82,83 | 113452 Description tienen espacios iniciales o finales | R | STAT-004/014 e ISSUE-004/005 |
| AF170 | 82,83 | No se consolidó automáticamente el catálogo | R | STAT-004/014 e ISSUE-004/005 |
| AF171 | 82,83 | Los rankings agrupan por StockCode y Description conjuntamente | R | STAT-004/014 e ISSUE-004/005 |
| AF172 | 82,83 | La documentación no resuelve de manera concluyente ajustes ni extremos | R | STAT-004/014 e ISSUE-004/005 |
| AF173 | 88,92,94 | La fuente no aporta reglas de negocio de descuentos | R | Readme, esquema, método y agregados cliente/producto |
| AF174 | 88,92,94 | La fuente no aporta reglas de negocio de impuestos | R | Readme, esquema, método y agregados cliente/producto |
| AF175 | 88,92,94 | La fuente no aporta costes | R | Readme, esquema, método y agregados cliente/producto |
| AF176 | 88,92,94 | La fuente no vincula anulaciones con ventas originales | R | Readme, esquema, método y agregados cliente/producto |
| AF177 | 88,92,94 | La fuente no clasifica individualmente clientes mayoristas | R | Readme, esquema, método y agregados cliente/producto |
| AF178 | 88,92,94 | No puede calcularse una tasa de devolución emparejada con el método utilizado | R | Readme, esquema, método y agregados cliente/producto |
| AF179 | 88,92,94 | Los resultados por producto dependen del filtro positivo | R | Readme, esquema, método y agregados cliente/producto |
| AF180 | 88,92,94 | Los resultados por producto dependen de la pareja código-descripción | R | Readme, esquema, método y agregados cliente/producto |
| AF181 | 88,92,94 | Las operaciones de gran volumen pueden influir en la concentración | R | Readme, esquema, método y agregados cliente/producto |
| AF182 | 88,92,94 | Los conceptos de envío pueden influir en la concentración | R | Readme, esquema, método y agregados cliente/producto |
| AF183 | 88,92,94 | Los extremos conservados pueden influir en la concentración | R | Readme, esquema, método y agregados cliente/producto |
