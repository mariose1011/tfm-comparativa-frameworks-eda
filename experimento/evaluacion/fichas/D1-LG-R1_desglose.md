# Evaluación D1-LG-R1

**Índice final:** 86,60/100.  
**Evaluación cerrada:** 6 de octubre de 2026.  
**Ejecución:** `D1_bike_sharing__langgraph__r01__20260831T172857425785Z`

**Criterios:** [Protocolo de evaluación](../01_protocolo_calidad_Q1_Q10_v0.1.md) y [guía D1](../02_ficha_D1_bike_sharing.md).  
**Resultados:** [Archivos originales de la ejecución](../../../outputs/experimento/D1_bike_sharing__langgraph__r01__20260831T172857425785Z).  
**Evaluación:** [Excel de puntuaciones](../Evaluacion_calidad.xlsx) y [JSON de comprobaciones](D1-LG-R1_comprobaciones.json).

Las referencias `STAT`, `ISSUE` y `FIG` identifican análisis, problemas y figuras en los archivos de la ejecución. Las referencias a líneas corresponden a su informe original, `report.md`.

## Resumen

| Métrica | Puntuación final |
| --- | ---: |
| Q1 Cumplimiento de las etapas | 93,75 |
| Q2 Corrección numérica | 94,29 |
| Q3 Validez del tratamiento de los datos | 87,50 |
| Q4 Detección de problemas y riesgos | 87,80 |
| Q5 Calidad y profundidad del EDA | 75,00 |
| Q6 Profundidad de la interpretación | 75,00 |
| Q7 Calidad de las visualizaciones | 90,00 |
| Q8 Cobertura del informe | 79,55 |
| Q9 Fidelidad del informe | 98,45 |
| Q10 Claridad y coherencia | 75,00 |

## Q1 Cumplimiento de las etapas: 93,75

| Etapa | Nota | Evidencia y motivo |
| --- | ---: | --- |
| E1 Carga e inspección inicial | 1 | STAT-001 y perfil. Dimensiones, columnas y unidad horaria identificadas |
| E2 Estructura, tipos y calidad | 1 | STAT-002 y STAT-003. Nulos, duplicados, dominios, identidad y cobertura cuantificados |
| E3 Preparación y decisiones de análisis | 0,5 | STAT-004 y CSV. Copia utilizable y variables fuente conservadas, pero timestamp pierde la hora |
| E4 Estadística descriptiva | 1 | STAT-005–STAT-007. Distribuciones, frecuencias y composición con población identificada |
| E5 Variables, agregaciones y relaciones | 1 | STAT-008–STAT-011. Comparaciones por grupos, perfiles y asociaciones |
| E6 Visualizaciones | 1 | FIG-001–FIG-005. Imágenes válidas, referenciadas y explicadas |
| E7 Problemas, riesgos y anomalías | 1 | issues.json, CHK-001–CHK-005 e ISSUE-001–ISSUE-002. Registro estructurado con decisiones y consecuencias |
| E8 Informe final | 1 | report.md. Integra alcance, preparación, hallazgos, evidencias y limitaciones |

`Q1 = 100 x 7,5 / 8 = 93,75`

## Q2 Corrección numérica: 94,29

**94,29/100.** Se consideran correctas 25 de las 26 comprobaciones, con un peso acumulado de 33 sobre 35. C17 permanece ausente. C18 y C19 se obtienen combinando las medias y los tamaños de los grupos que la ejecución ya presenta.

| Control | Peso | Resultado | Valor | Evidencia |
| --- | ---: | --- | --- | --- |
| C01 Número de filas | 2 | Correcta | 17379 | STAT-001.result.rows |
| C02 Número de columnas | 2 | Correcta | 17 | STAT-001.result.columns |
| C03 Fechas distintas | 1 | Correcta | 731 | STAT-001.result.distinct_dates |
| C04 Celdas ausentes | 2 | Correcta | 0 | STAT-002.result.missing_by_column |
| C05 Filas duplicadas | 2 | Correcta | 0 | STAT-002.result.exact_duplicate_rows |
| C06 Huecos en la secuencia horaria | 1 | Correcta | 165 | STAT-003.result.missing_hourly_timestamps |
| C07 Alquileres totales | 2 | Correcta | 3292679 | STAT-007.result.total_cnt |
| C08 Media horaria de alquileres | 2 | Correcta | 189,463088 | STAT-005.result.cnt.mean |
| C09 Mediana horaria de alquileres | 1 | Correcta | 142 | STAT-005.result.cnt.median |
| C10 Desviación típica muestral | 1 | Correcta | 181,387599 | STAT-005.result.cnt.std |
| C11 Máximo horario | 1 | Correcta | 977 | STAT-005.result.cnt.max |
| C12 Total de alquileres de usuarios ocasionales | 1 | Correcta | 620017 | STAT-007.result.total_casual |
| C13 Total de alquileres de usuarios registrados | 1 | Correcta | 2672662 | STAT-007.result.total_registered |
| C14 Proporción de alquileres de usuarios registrados sobre el total | 1 | Correcta | 0,811698316 | STAT-007.result.registered_share_of_total |
| C15 Alquileres totales en 2011 | 1 | Correcta | 1243103 | STAT-008.result.by_yr[yr=0].cnt_sum |
| C16 Alquileres totales en 2012 | 1 | Correcta | 2049576 | STAT-008.result.by_yr[yr=1].cnt_sum |
| C17 Variación total de 2012 respecto a 2011 | 2 | Ausente | — | Ausente: no calcular la variación a partir de los totales del agente |
| C18 Hora con mayor media | 2 | Correcta | 17, 461,452055 | STAT-009.result, hr=17, workingday=0 y 1. Suma de (media x n) / suma de n por hora. Misma población, operandos conservados en revisión Q2 del 06/10/2026. |
| C19 Hora con menor media | 1 | Correcta | 4, 6,35294118 | STAT-009.result, hr=4, workingday=0 y 1. Suma de (media x n) / suma de n por hora. Misma población, operandos conservados en revisión Q2 del 06/10/2026. |
| C20 Temporada con mayor media | 1 | Correcta | 236,016237 | STAT-008.result.by_season[season=3].cnt_mean |
| C21 Media con tiempo despejado | 1 | Correcta | 204,869272 | STAT-008.result.by_weathersit[weathersit=1].cnt_mean |
| C22 Media con tiempo adverso de categoría 3 | 1 | Correcta | 111,579281 | STAT-008.result.by_weathersit[weathersit=3].cnt_mean |
| C23 Observaciones meteorológicas de categoría 4 | 1 | Correcta | 3 | STAT-008.result.by_weathersit[weathersit=4].n |
| C24 Correlación de Pearson entre temperatura y cnt | 1 | Correcta | 0,4048 | STAT-011.result.pearson.temp.cnt |
| C25 Correlación de Pearson entre humedad y cnt | 1 | Correcta | -0,3229 | STAT-011.result.pearson.hum.cnt |
| C26 Inconsistencias en cnt = casual + registered | 2 | Correcta | 0 | STAT-002.result.identity_violations |

`Q2 = 100 x 33 / 35 = 94,29`

## Q3 Validez del tratamiento de los datos: 87,50

| ID | Nota | Decisión y evidencia |
| --- | ---: | --- |
| D01 | 0 | CSV y traza, evento 22. La fecha y hora se combinan correctamente durante el análisis, pero la columna timestamp pierde la hora al guardarse |
| D02 | 1 | profile.columns y STAT-006–STAT-010. Las ocho variables se identifican como categorías y se analizan mediante frecuencias y agrupaciones |
| D03 | 1 | STAT-001 e informe, línea 13. instant como índice. No participa en medidas explicativas ni correlaciones |
| D04 | 1 | TR-004, STAT-002, STAT-004 y contraste de las 17 columnas fuente. No se eliminan filas |
| D05 | 1 | ISSUE-001 e informe, línea 90. Se detectan huecos y se conservan sin imputación |
| D06 | 1 | ISSUE-002 y STAT-012. Se conservan los 505 extremos horarios por falta de evidencia de error |
| D07 | 1 | STAT-002, STAT-007 e informe, líneas 28 y 44. `casual` y `registered` se presentan como partes del total cnt, no como resultados independientes. |
| D08 | 1 | Informe, líneas 46 y 100. Se conservan las escalas normalizadas, verificadas frente a la entrada |

`Q3 = 100 x 7 / 8 = 87,50`

## Q4 Detección de problemas y riesgos: 87,80

| ID | Resultado | Evidencia y motivo |
| --- | --- | --- |
| R01 | Completo | STAT-001 e informe, línea 13. instant es índice, no medida |
| R02 | Completo | profile.columns y STAT-006. Se reconoce que los códigos numéricos representan categorías, no cantidades. |
| R03 | Completo | STAT-002 e informe, líneas 28 y 44. Identidad exacta de los conteos |
| R04 | Completo | Informe, líneas 46 y 100. Las cuatro variables ambientales normalizadas |
| R05 | Completo | STAT-003 e ISSUE-001. 165 huecos y consecuencias para agregaciones |
| R06 | Completo | STAT-006, STAT-008 e informe, líneas 48, 54 y 76. Tres observaciones y cautela |
| R07 | Ausente | No se explican conjuntamente dependencia entre observaciones temporales y derivación entre variables de calendario. El plan lo anticipa, pero no acredita ejecución |
| A01 | Adicional válido | STAT-011 e informe, línea 62. Redundancia temp–atemp, Pearson 0,9877 |
| A02 | Adicional válido | STAT-012 e ISSUE-002. Extremos horarios retenidos que pueden afectar medidas no robustas |
| A03 | Adicional válido | profile.unit_of_analysis, STAT-007 e informe, líneas 44 y 98. Conteos agregados no equivalen a personas únicas ni datos individuales |
| F01 | Falsa alarma | Informe, línea 92, frente a STAT-012 e ISSUE-002. Se afirma existencia de extremos diarios completos, aunque el recuento es 0 |

K=6, A=3, F=1. Precisión=9/10=0,90. Cobertura=6/7=0,857142857.

`Q4 = 100 x [2 x 0,90 x (6 / 7)] / [0,90 + (6 / 7)] = 87,80`

## Q5 Calidad y profundidad del EDA: 75,00

Examina distribuciones, composición, grupos, asociaciones y extremos, por lo que supera un EDA básico. La marca temporal defectuosa y las omisiones de dependencia y perfil horario global impiden el nivel 4.

Evidencia: STAT-004 a STAT-012, CSV.

`Q5 = 100 x 3 / 4 = 75,00`

## Q6 Profundidad de la interpretación: 75,00

Relaciona perfiles y composición con sus cálculos y evita atribuir causalidad. Sin embargo, describe una marca temporal guardada con hora y extremos diarios que los productos finales no respaldan.

Evidencia: report.md, líneas 30, 58, 80 y 92, CSV y STAT-012.

`Q6 = 100 x 3 / 4 = 75,00`

## Q7 Calidad de las visualizaciones: 90,00

| ID | Nota 0–4 | Figuras y motivo |
| --- | ---: | --- |
| V01 | 4 | FIG-001 y STAT-010. 24 meses ordenados, total claramente etiquetado y cautela sobre cobertura en el informe, línea 68 |
| V02 | 4 | FIG-002 y STAT-009. Dos curvas legibles, leyenda correcta y todas las horas. Interpretación de picos en líneas 58 y 72 |
| V03 | 4 | FIG-001 cubre también el patrón mensual con orden cronológico. Informe, líneas 56 y 68 |
| V04 | 3 | FIG-003 e informe, líneas 48 y 76. El gráfico omite los valores extremos sin indicarlo. El informe advierte que la categoría meteorológica 4 solo contiene tres observaciones |
| V05 | 3 | FIG-004. Las medias de temperatura aparecen separadas por la misma distancia en el eje, aunque las diferencias entre sus valores no son iguales. Tampoco se indican los límites de los grupos ni cuántas observaciones contiene cada uno |

`Q7 = 100 x 18 / 20 = 90,00`

## Q8 Cobertura del informe: 79,55

| ID | Peso | Cobertura | Componentes y evidencia |
| --- | ---: | ---: | --- |
| U01 | 2 | 1 | Filas, columnas y periodo. Líneas 3 y 19 |
| U02 | 2 | 1 | Sin nulos ni duplicados, diferenciados de huecos horarios. Líneas 7 y 23–24 |
| U03 | 2 | 1 | Nivel y dispersión de cnt, con media, mediana, desviación y cuartiles correctos. Línea 36 |
| U04 | 2 | 1 | Los alquileres de usuarios registrados representan el 81,2 % del total. Líneas 5 y 44 |
| U05 | 2 | 0 | No comunica totales anuales ni aumento porcentual del total. Las medias de la línea 52 son otra medida. FIG-001 representa meses, no la variación anual exigida |
| U06 | 2 | 0 | El informe presenta resultados separados entre días laborables y no laborables, pero no identifica las horas con mayor y menor media del conjunto completo |
| U07 | 2 | 1 | Máximo laborable 17 h y no laborable 13 h. Líneas 9 y 58 |
| U08 | 1 | 1 | Cuatro medias estacionales y patrón mensual. La lista de la línea 54 identifica inequívocamente la mayor media en season=3 |
| U09 | 2 | 1 | Menores medias con peor tiempo y cautela por categoría 4 con tres filas. Líneas 54 y 76 |
| U10 | 2 | 1 | Asociaciones positivas con temperatura y negativas con humedad, sin atribución causal. Líneas 60, 80 y 84 |
| U11 | 2 | 1 | Se reconoce que `cnt = casual + registered` y se utilizan los componentes para describir la composición del total. Líneas 28 y 44. |
| U12 | 1 | 0,5 | Ciudad delimitada en línea 3 y ausencia de base causal en líneas 15 y 104. Falta explicar la dependencia temporal de las observaciones |

`Q8 = 100 x 17,5 / 22 = 79,55`

## Q9 Fidelidad del informe: 98,45

**Justificación de la nota.** Se respaldan 127 de 129 afirmaciones distintas del informe completo. Las dos contradicciones son la hora de timestamp guardado y la existencia de extremos diarios.

**R:** respaldada. **C:** contradicha.

[Inventario completo de afirmaciones](#anexo-inventario-de-afirmaciones).

**129 afirmaciones, 127 respaldadas, 2 contradichas y 0 sin respaldo suficiente.**

`Q9 = 100 x 127 / 129 = 98,45`

## Q10 Claridad y coherencia: 75,00

El informe tiene secciones comprensibles, figuras integradas y evidencias localizables. Las contradicciones sobre la marca temporal y los extremos diarios impiden considerarlo plenamente coherente. Se asigna 3/4 porque son defectos localizados y no vuelven incomprensible el conjunto.

Evidencia: report.md completo, especialmente líneas 30 y 92, y conexión con CSV y STAT-012.

`Q10 = 100 x 3 / 4 = 75,00`

## Anexo inventario de afirmaciones

Detalle de Q9 para comprobar el recuento. Se conserva íntegro el inventario de 129 afirmaciones y sus clasificaciones. Las líneas remiten al informe original, no a esta ficha.

| ID | Línea | Afirmación distinta | Evidencia | Resultado |
| --- | ---: | --- | --- | --- |
| AF001 | 3 | 17379 registros fuente | STAT-001.rows | R |
| AF002 | 3 | 17 variables fuente | STAT-001.columns | R |
| AF003 | 3 | Inicio 2011-01-01 00:00 | STAT-001.date_range | R |
| AF004 | 3 | Fin 2012-12-31 23:00 | STAT-001.date_range | R |
| AF005 | 3 | Observación agregada por hora | profile.unit_of_analysis y STAT-001 | R |
| AF006 | 3 | Sistema Capital Bikeshare | STAT-001 y documentación pública consultada | R |
| AF007 | 3 | Datos de Washington D.C. | STAT-001 y documentación pública consultada | R |
| AF008 | 5 | cnt total 3292679 | STAT-007.total_cnt | R |
| AF009 | 5 | cnt media 189,5 | STAT-005.cnt.mean | R |
| AF010 | 5 | cnt mediana 142 | STAT-005.cnt.median | R |
| AF011 | 5 | cnt primer cuartil 40 | STAT-005.cnt.q1 | R |
| AF012 | 5 | cnt tercer cuartil 281 | STAT-005.cnt.q3 | R |
| AF013 | 5 | Conteos dispersos y valores altos relevantes | STAT-005.cnt y STAT-012.hourly_cnt_iqr | R |
| AF014 | 5 | registered 81,2 % del total | STAT-007.registered_share_of_total | R |
| AF015 | 5 | casual 18,8 % del total | STAT-007.casual_share_of_total | R |
| AF016 | 7 | No hay valores ausentes fuente | STAT-002.missing_by_column | R |
| AF017 | 7 | No hay duplicados exactos | STAT-002.exact_duplicate_rows | R |
| AF018 | 7 | No hay códigos fuera de dominio | STAT-002.domains | R |
| AF019 | 7 | No hay negativos en las variables revisadas | STAT-002.ranges | R |
| AF020 | 7 | cnt = casual + registered en cada fila | STAT-002.identity_violations | R |
| AF021 | 7 | Faltan 165 horas | STAT-003.missing_hourly_timestamps | R |
| AF022 | 7 | 76 fechas tienen menos de 24 filas | STAT-003.incomplete_days | R |
| AF023 | 9 | Los perfiles horarios difieren por tipo de día | STAT-009 y FIG-002 | R |
| AF024 | 9 | Media laborable a las 8 h: 477,0 | STAT-009, workingday=1, hr=8 | R |
| AF025 | 9 | Media laborable a las 17 h: 525,3 | STAT-009, workingday=1, hr=17 | R |
| AF026 | 9 | Media no laborable a las 13 h: 372,7 | STAT-009, workingday=0, hr=13 | R |
| AF027 | 9 | Máximo no laborable a las 13 h | STAT-009, máximo por segmento | R |
| AF028 | 13 | instant se utiliza como índice, no medida | STAT-001, código del evento 22 y matriz de STAT-011 | R |
| AF029 | 15 | No se entrenaron modelos predictivos | Operaciones ejecutadas, eventos 22 y 37, y STAT-001–STAT-012 | R |
| AF030 | 19 | 731 fechas distintas | STAT-001.distinct_dates | R |
| AF031 | 19 | Conteos y códigos cargados como numéricos | STAT-001.observed_dtypes | R |
| AF032 | 19 | dteday inicialmente textual | profile.columns, dteday.original_type | R |
| AF033 | 19 | dteday convertido a fecha sin fallos | TR-001 y STAT-004.date_parse_failures | R |
| AF034 | 30 | No se eliminaron registros | STAT-004.rows_removed y contraste CSV | R |
| AF035 | 30 | No se imputaron registros | TR-004, ISSUE-001 y contraste CSV | R |
| AF036 | 30 | La copia tiene 17379 filas | STAT-004.prepared_shape y CSV | R |
| AF037 | 30 | Se añaden dos variables | STAT-004.columns_added y CSV | R |
| AF038 | 30, 108 | timestamp guardado suma fecha y hora y añade trazabilidad horaria | CSV: 16653 filas discrepan. Serialización del evento 22 elimina la hora | C |
| AF039 | 30 | casual_share = casual / cnt | TR-003 y contraste de la columna preparada | R |
| AF040 | 30 | La copia tiene 19 columnas | STAT-004.prepared_shape y CSV | R |
| AF041 | 30 | No hay horas con cnt=0 | STAT-007.hours_with_zero_cnt | R |
| AF042 | 30 | casual_share no tiene ausencias | STAT-004.prepared_missing_by_column | R |
| AF043 | 32 | IQR señala 505 extremos horarios de cnt | STAT-012.hourly_cnt_iqr.flagged_hours | R |
| AF044 | 32 | No se acreditó que esos extremos fueran errores | ISSUE-002, status retained y uncertainty | R |
| AF045 | 36 | cnt desviación estándar 181,4 | STAT-005.cnt.std | R |
| AF046 | 36 | cnt mínimo 1 | STAT-005.cnt.min | R |
| AF047 | 36 | cnt máximo 977 | STAT-005.cnt.max | R |
| AF048 | 36 | Media superior a mediana, compatible con cola alta | STAT-005.cnt y STAT-012 | R |
| AF049 | 40 | casual media 35,7 | STAT-005.casual.mean | R |
| AF050 | 40 | casual mediana 17 | STAT-005.casual.median | R |
| AF051 | 40 | casual primer cuartil 4 | STAT-005.casual.q1 | R |
| AF052 | 40 | casual tercer cuartil 48 | STAT-005.casual.q3 | R |
| AF053 | 40 | casual máximo 367 | STAT-005.casual.max | R |
| AF054 | 41 | registered media 153,8 | STAT-005.registered.mean | R |
| AF055 | 41 | registered mediana 115 | STAT-005.registered.median | R |
| AF056 | 41 | registered primer cuartil 34 | STAT-005.registered.q1 | R |
| AF057 | 41 | registered tercer cuartil 220 | STAT-005.registered.q3 | R |
| AF058 | 41 | registered máximo 886 | STAT-005.registered.max | R |
| AF059 | 42 | casual_share media horaria 17,2 % | STAT-005.casual_share.mean | R |
| AF060 | 42 | casual_share mediana horaria 14,7 % | STAT-005.casual_share.median | R |
| AF061 | 44 | casual total 620017 | STAT-007.total_casual | R |
| AF062 | 44 | registered total 2672662 | STAT-007.total_registered | R |
| AF063 | 44 | Los totales de componentes suman cnt total | STAT-007 y contraste de sumas | R |
| AF064 | 44 | Los conteos no son personas usuarias únicas | STAT-007.interpretation y unidad de análisis | R |
| AF065 | 46 | temp está normalizada | Documentación consultada, STAT-005 y perfil | R |
| AF066 | 46 | atemp está normalizada | Documentación consultada, STAT-005 y perfil | R |
| AF067 | 46 | hum está normalizada | Documentación consultada, STAT-005 y perfil | R |
| AF068 | 46 | windspeed está normalizada | Documentación consultada, STAT-005 y perfil | R |
| AF069 | 46 | temp media 0,497 | STAT-005.temp.mean | R |
| AF070 | 46 | atemp media 0,476 | STAT-005.atemp.mean | R |
| AF071 | 46 | hum media 0,627 | STAT-005.hum.mean | R |
| AF072 | 46 | windspeed media 0,190 | STAT-005.windspeed.mean | R |
| AF073 | 46 | No se desnormalizaron las variables | Contraste de columnas fuente y código del evento 22 | R |
| AF074 | 48 | weathersit=1 contiene 11413 filas | STAT-006.weathersit y STAT-008 | R |
| AF075 | 48 | weathersit=1 representa 65,7 % | STAT-006.weathersit | R |
| AF076 | 48 | weathersit=2 contiene 4544 filas | STAT-006.weathersit y STAT-008 | R |
| AF077 | 48 | weathersit=2 representa 26,1 % | STAT-006.weathersit | R |
| AF078 | 48 | weathersit=3 contiene 1419 filas | STAT-006.weathersit y STAT-008 | R |
| AF079 | 48 | weathersit=3 representa 8,2 % | STAT-006.weathersit | R |
| AF080 | 48 | weathersit=4 contiene tres filas | STAT-006.weathersit y STAT-008 | R |
| AF081 | 48 | La categoría 4 es demasiado escasa para una comparación estable | STAT-006, n=3, y advertencias del informe | R |
| AF082 | 52 | Media de cnt en yr=0: 143,8 | STAT-008.by_yr, yr=0 | R |
| AF083 | 52 | Media de cnt en yr=1: 234,7 | STAT-008.by_yr, yr=1 | R |
| AF084 | 52 | Mediana de cnt en yr=0: 109 | STAT-008.by_yr, yr=0 | R |
| AF085 | 52 | Mediana de cnt en yr=1: 191 | STAT-008.by_yr, yr=1 | R |
| AF086 | 54 | Media de cnt en season=1: 111,1 | STAT-008.by_season | R |
| AF087 | 54 | Media de cnt en season=2: 208,3 | STAT-008.by_season | R |
| AF088 | 54 | Media de cnt en season=3: 236,0 | STAT-008.by_season | R |
| AF089 | 54 | Media de cnt en season=4: 198,9 | STAT-008.by_season | R |
| AF090 | 54 | Media de cnt en weathersit=1: 204,9 | STAT-008.by_weathersit | R |
| AF091 | 54 | Media de cnt en weathersit=2: 175,2 | STAT-008.by_weathersit | R |
| AF092 | 54 | Media de cnt en weathersit=3: 111,6 | STAT-008.by_weathersit | R |
| AF093 | 54 | Media de cnt en weathersit=4: 74,3 | STAT-008.by_weathersit | R |
| AF094 | 56 | Media de cnt en junio de yr=1: 281,7 | STAT-010, yr=1, mnth=6 | R |
| AF095 | 56 | Media de cnt en agosto de yr=1: 288,3 | STAT-010, yr=1, mnth=8 | R |
| AF096 | 56 | Media de cnt en septiembre de yr=1: 303,6 | STAT-010, yr=1, mnth=9 | R |
| AF097 | 56, 68, 102 | La cobertura horaria no es uniforme entre meses | STAT-003, STAT-010.n y días calendario de cada mes | R |
| AF098 | 58 | Hay un pico local laborable a las 8 h | STAT-009 y FIG-002 | R |
| AF099 | 58 | El máximo laborable está a las 17 h | STAT-009 y FIG-002 | R |
| AF100 | 58 | Niveles no laborables altos entre 12 y 16 h | STAT-009 y FIG-002 | R |
| AF101 | 58 | registered elevado en los picos laborables | STAT-009.registered_mean por hora y tipo de día | R |
| AF102 | 58 | casual relativamente más visible en horas centrales no laborables | STAT-009.casual_mean y cnt_mean | R |
| AF103 | 60 | Pearson temp–cnt = 0,4048 | STAT-011.pearson.temp.cnt | R |
| AF104 | 60 | Pearson atemp–cnt = 0,4009 | STAT-011.pearson.atemp.cnt | R |
| AF105 | 60 | Pearson hum–cnt = -0,3229 | STAT-011.pearson.hum.cnt | R |
| AF106 | 60 | Pearson windspeed–cnt = 0,0932 | STAT-011.pearson.windspeed.cnt | R |
| AF107 | 60 | Spearman temp–cnt = 0,4233 | STAT-011.spearman.temp.cnt | R |
| AF108 | 60 | Spearman hum–cnt = -0,3596 | STAT-011.spearman.hum.cnt | R |
| AF109 | 62 | Pearson temp–atemp = 0,9877 | STAT-011.pearson.temp.atemp | R |
| AF110 | 62 | temp y atemp aportan información muy redundante | STAT-011 y FIG-005 | R |
| AF111 | 68 | FIG-001 representa sumas mensuales observadas | STAT-010, FIG-001 y código del evento 22 | R |
| AF112 | 72 | También son altos los niveles laborables de 17–18 h | STAT-009 y FIG-002 | R |
| AF113 | 76 | Media meteorológica de código 1 mayor que código 2 | STAT-008.by_weathersit | R |
| AF114 | 76 | Media meteorológica de código 1 mayor que código 3 | STAT-008.by_weathersit | R |
| AF115 | 76 | La categoría meteorológica 4 se conserva en la figura | FIG-003 y código del evento 22 | R |
| AF116 | 80 | Las medias por decil de temp muestran asociación positiva | STAT-011.cnt_by_temp_decile y FIG-004 | R |
| AF117 | 88 | Se esperan 17544 horas entre los límites | STAT-003.expected_hours_between_bounds | R |
| AF118 | 88 | Una fecha contiene una sola hora | STAT-003.incomplete_day_hours_distribution, clave 1 | R |
| AF119 | 90 | No se acreditó la causa de los huecos | ISSUE-001.uncertainty y fuentes autorizadas | R |
| AF120 | 90 | El cribado diario usa solo 655 días completos | STAT-012.complete_daily_iqr.n_complete_days y código ejecutado | R |
| AF121 | 92 | Se detectaron días completos con totales extremos | STAT-012.flagged_days=0 e ISSUE-002.flagged_complete_days=0 | C |
| AF122 | 98 | No hay trayectos individuales | STAT-001.columns y unidad agregada documentada | R |
| AF123 | 98 | No hay estaciones de origen | STAT-001.columns y diccionario consultado | R |
| AF124 | 98 | No hay estaciones de destino | STAT-001.columns y diccionario consultado | R |
| AF125 | 98 | No hay duración de viajes | STAT-001.columns y diccionario consultado | R |
| AF126 | 98 | No hay datos de personas usuarias únicas | STAT-001.columns y STAT-007.interpretation | R |
| AF127 | 98 | No hay características individuales de personas | STAT-001.columns y diccionario consultado | R |
| AF128 | 98 | El agregado no acredita comportamiento individual | profile.unit_of_analysis y limitaciones registradas | R |
| AF129 | 108 | Los códigos fuente no se alteraron | Contraste de las 17 columnas fuente y TR-004 | R |
