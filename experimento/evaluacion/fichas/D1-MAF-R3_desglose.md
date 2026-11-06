# Evaluación D1-MAF-R3

**Índice final:** 90,31/100.  
**Evaluación cerrada:** 6 de octubre de 2026.  
**Ejecución:** `D1_bike_sharing__microsoft_agent_framework__r03__20260831T213622746167Z`

**Criterios:** [Protocolo de evaluación](../01_protocolo_calidad_Q1_Q10_v0.1.md) y [guía D1](../02_ficha_D1_bike_sharing.md).  
**Resultados:** [Archivos originales de la ejecución](../../../outputs/experimento/D1_bike_sharing__microsoft_agent_framework__r03__20260831T213622746167Z).  
**Evaluación:** [Excel de puntuaciones](../Evaluacion_calidad.xlsx) y [JSON de comprobaciones](D1-MAF-R3_comprobaciones.json).

Las referencias `STAT`, `ISSUE` y `FIG` identifican análisis, problemas y figuras en los archivos de la ejecución. `TR` identifica transformaciones y `CHK`, comprobaciones de calidad. Las referencias a líneas corresponden al informe original, `report.md`.

## Resumen

| Métrica | Puntuación final |
| --- | ---: |
| Q1 Cumplimiento de las etapas | 100,00 |
| Q2 Corrección numérica | 94,29 |
| Q3 Validez del tratamiento de los datos | 100,00 |
| Q4 Detección de problemas y riesgos | 92,31 |
| Q5 Calidad y profundidad del EDA | 75,00 |
| Q6 Profundidad de la interpretación | 100,00 |
| Q7 Calidad de las visualizaciones | 75,00 |
| Q8 Cobertura del informe | 81,82 |
| Q9 Fidelidad del informe | 100,00 |
| Q10 Claridad y coherencia | 75,00 |

## Q1 Cumplimiento de las etapas: 100,00

| Etapa | Puntos | Evidencia |
| --- | --- | --- |
| E1 Carga e inspección inicial | 1 | STAT-001 y profile |
| E2 Estructura, tipos y calidad | 1 | STAT-002 a STAT-006 |
| E3 Preparación y decisiones de análisis | 1 | TR-001/002/003 y CSV contrastado |
| E4 Estadística descriptiva | 1 | STAT-007/008/009 |
| E5 Variables, agregaciones y relaciones | 1 | STAT-010 a STAT-013 |
| E6 Visualizaciones | 1 | Cinco PNG utilizables y report 59–77 |
| E7 Problemas, riesgos y anomalías | 1 | ISSUE-001/002 y STAT-014 |
| E8 Informe final | 1 | report completo tras corrección |

`Q1 = 100 x 8 / 8 = 100,00`

## Q2 Corrección numérica: 94,29

| Control | Producido | Referencia | Estado | Puntos | Evidencia |
| --- | --- | --- | --- | --- | --- |
| C01 Número de filas | 17.379 | 17.379 | correcta | 2/2 | STAT-001.rows |
| C02 Número de columnas | 17 | 17 | correcta | 2/2 | STAT-001.columns |
| C03 Fechas distintas | 731 | 731 | correcta | 1/1 | STAT-010.days |
| C04 Celdas ausentes | 0 | 0 | correcta | 2/2 | STAT-002 |
| C05 Filas duplicadas | 0 | 0 | correcta | 2/2 | STAT-003.full_row_duplicates |
| C06 Huecos en la secuencia horaria | 165 | 165 | correcta | 1/1 | STAT-004.missing_hour_count |
| C07 Alquileres totales | 3.292.679 | 3.292.679 | correcta | 2/2 | STAT-008.cnt_total |
| C08 Media horaria de alquileres | 189,463088 | 189,463088 | correcta | 2/2 | STAT-007.cnt.mean |
| C09 Mediana horaria de alquileres | 142 | 142 | correcta | 1/1 | STAT-007.cnt.median |
| C10 Desviación típica muestral | 181,387599 | 181,387599 | correcta | 1/1 | STAT-007.cnt.std |
| C11 Máximo horario | 977 | 977 | correcta | 1/1 | STAT-007.cnt.max |
| C12 Alquileres de usuarios ocasionales | 620.017 | 620.017 | correcta | 1/1 | STAT-008.casual_total |
| C13 Alquileres de usuarios registrados | 2.672.662 | 2.672.662 | correcta | 1/1 | STAT-008.registered_total |
| C14 Proporción de alquileres de usuarios registrados | 0,811698 | 0,811698 | correcta | 1/1 | STAT-008.registered_share_of_cnt |
| C15 Alquileres totales en 2011 | 1.243.103 | 1.243.103 | correcta | 1/1 | STAT-009.by_yr[yr=0].sum |
| C16 Alquileres totales en 2012 | 2.049.576 | 2.049.576 | correcta | 1/1 | STAT-009.by_yr[yr=1].sum |
| C17 Variación total de 2012 respecto a 2011 | No producido | 64,875799 | ausente | 0/2 | Variación porcentual anual no producida |
| C18 Hora con mayor media | Categoría 17, 461,452055 | 461,452055 | correcta | 2/2 | STAT-011.by_hr_overall[hr=17].mean_cnt |
| C19 Hora con menor media | Categoría 4, 6,352941 | 6,352941 | correcta | 1/1 | STAT-011.by_hr_overall[hr=4].mean_cnt |
| C20 Temporada con mayor media | Categoría 3, 236,016237 | 236,016237 | correcta | 1/1 | STAT-009.by_season[season=3].mean |
| C21 Media con tiempo despejado | Categoría 1, 204,869272 | 204,869272 | correcta | 1/1 | STAT-009.by_weathersit[weathersit=1].mean |
| C22 Media con tiempo adverso de categoría 3 | Categoría 3, 111,579281 | 111,579281 | correcta | 1/1 | STAT-009.by_weathersit[weathersit=3].mean |
| C23 Observaciones meteorológicas de categoría 4 | 3 | 3 | correcta | 1/1 | STAT-009.by_weathersit[weathersit=4].n |
| C24 Correlación de Pearson entre temperatura y cnt | 0,404772 | 0,404772 | correcta | 1/1 | STAT-013.correlations_with_cnt[temp].pearson_with_cnt |
| C25 Correlación de Pearson entre humedad y cnt | -0,322911 | -0,322911 | correcta | 1/1 | STAT-013.correlations_with_cnt[hum].pearson_with_cnt |
| C26 Inconsistencias en cnt = casual + registered | 0 | 0 | correcta | 2/2 | STAT-006.identity_mismatch_count |

Se obtienen resultados correctos en 25 de las 26 comprobaciones, que suman 33 de los 35 puntos posibles. Solo permanece ausente el crecimiento porcentual entre los totales de alquileres de 2011 y 2012.

`Q2 = 100 x 33 / 35 = 94,29`

## Q3 Validez del tratamiento de los datos: 100,00

| Decisión | Puntos | Evidencia |
| --- | --- | --- |
| D01 Fecha-hora correcta | 1 | timestamp sin discrepancias en 17379 filas |
| D02 Categorías como grupos | 1 | Etiquetas y agrupaciones por códigos, STAT-005/009/011 |
| D03 instant solo identificador | 1 | instant se conserva como identificador y no se utiliza para explicar los alquileres. STAT-003 y código del análisis |
| D04 Sin limpieza innecesaria | 1 | CSV conserva columnas fuente y TR-003 |
| D05 No imputar huecos | 1 | ISSUE-001, report 81 |
| D06 Extremos conservados | 1 | CSV completo, ISSUE-002, report 33 |
| D07 Identidad no usada como evidencia independiente | 1 | user_total_check, STAT-006 y composición. No se presenta la identidad como descubrimiento predictivo |
| D08 Escalas normalizadas conservadas | 1 | CSV, STAT-006/007 y report 41 |

`Q3 = 100 x 8 / 8 = 100,00`

## Q4 Detección de problemas y riesgos: 92,31

| Riesgo | Clasificación | Evidencia |
| --- | --- | --- |
| R01 Identificador secuencial | completo | instant se utiliza como identificador, no como variable explicativa. STAT-003 y código del análisis |
| R02 Códigos categóricos | completo | STAT-005/009/011, TR-002 y report 27 |
| R03 Identidad de componentes | completo | STAT-006/008, user_total_check y report 29/51 |
| R04 Meteorología normalizada | completo | STAT-006/007 y report 41 |
| R05 165 huecos horarios | completo | STAT-004, ISSUE-001 y report 81 |
| R06 Weathersit4 n=3 | completo | STAT-009 y report 53/71 |
| R07 Dependencia y derivación temporal | parcial | STAT-005 contrasta calendario, sin tratamiento de dependencia entre observaciones sucesivas |
| A01 Redundancia temp-atemp | adicional válido | STAT-013 Pearson0,987672 y report 55 |
| A02 Influencia de extremos válidos | adicional válido | STAT-014, ISSUE-002 y report 83 |
| A03 Limitación de datos individuales y espaciales | adicional válido | Profile y report 89 |

Se identifican seis riesgos previstos y tres adicionales, sin falsas alarmas. La precisión es 1, la cobertura es 6/7 y F1 es 12/13.

`Q4 = 100 x [2 x 1 x (6 / 7)] / [1 + (6 / 7)] = 92,31`

## Q5 Calidad y profundidad del EDA: 75,00

El análisis examina distribuciones, diferencias entre grupos, correlaciones y extremos diarios contextualizados. Recibe 3 de 4 puntos porque no desarrolla la dependencia temporal y explica poco los patrones mensuales y estacionales calculados.

**Evidencia:** STAT-007 a STAT-014, report37–55/75/83/93 y figuras. El nivel 3 reconoce análisis correcto más allá de resultados básicos. Falta desarrollo de la dependencia y de algunos patrones calculados para alcanzar el nivel 4.

`Q5 = 100 x 3 / 4 = 75,00`

## Q6 Profundidad de la interpretación: 100,00

El informe relaciona los hallazgos con las evidencias y sus limitaciones. Contextualiza el mínimo diario según su única hora observada, interpreta la composición de los alquileres y distingue las asociaciones de las explicaciones causales. Recibe 4 de 4 puntos por una interpretación integrada, prudente y respaldada.

**Evidencia:** Líneas 47, 51, 53, 55 y 95 del informe y estadísticas correspondientes.

`Q6 = 100 x 4 / 4 = 100,00`

## Q7 Calidad de las visualizaciones: 75,00

| Objetivo | Puntos de 4 | Evidencia y decisión |
| --- | --- | --- |
| V01 Evolución 2011–2012 | 4 | FIG-001 y report 59. Agregación diaria legible, ejes y cobertura advertida |
| V02 Hora por tipo de día | 4 | FIG-002 y report 9/49/63. 24 horas, curvas y picos correctos. FIG-003 aporta composición, no sustituye el contraste workingday |
| V03 Patrón mensual o estacional | 4 | FIG-005 y report 75. Meses1–12 ordenados y dos años comparados. yr0/1 se identifican en report43 |
| V04 Meteorología y n reducido | 3 | FIG-004 permite comparar las distribuciones y el informe advierte que la categoría 4 tiene tres observaciones. El gráfico oculta los valores extremos sin indicarlo |
| V05 Relación con temperatura o humedad | 0 | No se genera ninguna figura que relacione los alquileres con la temperatura o la humedad |

`Q7 = 100 x 15 / 20 = 75,00`

## Q8 Cobertura del informe: 81,82

| Contenido | Peso | Crédito | Puntos | Evidencia |
| --- | --- | --- | --- | --- |
| U01 Dimensiones y periodo | 2 | 1 | 2 | Report3/19 |
| U02 Nulos, duplicados y huecos | 2 | 1 | 2 | Report5/23/24/81 |
| U03 Nivel y dispersión cnt | 2 | 1 | 2 | Report37 comunica media, mediana, cuartiles y rango |
| U04 Proporción registered | 2 | 1 | 2 | Report7/39 |
| U05 Totales anuales y aumento64,88% | 2 | 0,5 | 1 | Report43 contiene totales y medias, no porcentaje de aumento |
| U06 Máximo y mínimo globales por hora | 2 | 0 | 0 | El informe no identifica las horas con mayor y menor media del conjunto completo. FIG-003 representa los componentes por separado |
| U07 Máximos17h laborables y13h no laborables | 2 | 1 | 2 | Report9/49 y FIG-002 |
| U08 Diferencias temporales y máximo season3 | 1 | 0,5 | 0,5 | El informe y FIG-005 muestran el patrón mensual, pero no comunican que season=3 tiene la mayor media |
| U09 Meteorología y categoría4 n=3 | 2 | 1 | 2 | Report53/71 |
| U10 Temperatura y humedad, prudencia | 2 | 1 | 2 | Report55/93 |
| U11 Identidad no predictiva | 2 | 1 | 2 | Report29/51 y alcance descriptivo, composición como suma de componentes |
| U12 Dependencia, una ciudad y no causalidad | 1 | 0,5 | 0,5 | El informe delimita el sistema estudiado y rechaza interpretaciones causales, pero no explica la dependencia temporal ni identifica expresamente la ciudad |

`Q8 = 100 x 18 / 22 = 81,82`

## Q9 Fidelidad del informe: 100,00

Se respaldan las 163 afirmaciones evaluadas. No se identifican afirmaciones contradichas ni sin respaldo suficiente.

El inventario situado al final de esta ficha recoge las afirmaciones revisadas, su clasificación y las evidencias utilizadas.

`Q9 = 100 x 163 / 163 = 100,00`

## Q10 Claridad y coherencia: 75,00

El informe está ordenado y permite seguir el análisis, pero explica poco algunos códigos y tipos de usuario y utiliza etiquetas inglesas. Además, CHK-007 de `issues.json` remite el cribado de valores extremos a STAT-012, que contiene el análisis mensual, en lugar de STAT-014. Recibe 3 de 4 puntos por estas carencias de claridad y coherencia.

**Evidencia:** Report13/26/53, figuras y issues.checks_performed[CHK-007].evidence_ids. Las explicaciones breves y la referencia residual impiden proponer claridad plena.

`Q10 = 100 x 3 / 4 = 75,00`

## Inventario de afirmaciones

R = respaldada

| ID | Línea | Afirmación | Estado | Evidencia |
| --- | --- | --- | --- | --- |
| AF001 | 3 | 17379 observaciones | R | STAT-001/004, TR-001/002/003 y CSV |
| AF002 | 3 | Inicio 2011-01-01 | R | STAT-001/004, TR-001/002/003 y CSV |
| AF003 | 3 | Fin 2012-12-31 | R | STAT-001/004, TR-001/002/003 y CSV |
| AF004 | 3 | Agregados horarios de Capital Bikeshare | R | STAT-001/004, TR-001/002/003 y CSV |
| AF005 | 3 | La copia conserva las filas fuente | R | STAT-001/004, TR-001/002/003 y CSV |
| AF006 | 3 | Se añaden variables temporales | R | STAT-001/004, TR-001/002/003 y CSV |
| AF007 | 3 | Se añaden etiquetas de códigos | R | STAT-001/004, TR-001/002/003 y CSV |
| AF008 | 3 | Se añade comprobación de componentes | R | STAT-001/004, TR-001/002/003 y CSV |
| AF009 | 3 | No se imputan registros | R | STAT-001/004, TR-001/002/003 y CSV |
| AF010 | 3 | No se eliminan registros | R | STAT-001/004, TR-001/002/003 y CSV |
| AF011 | 5 | Cero valores ausentes en columnas fuente | R | STAT-002/003/005/006 y STAT-004, ISSUE-001 |
| AF012 | 5 | Cero filas duplicadas | R | STAT-002/003/005/006 y STAT-004, ISSUE-001 |
| AF013 | 5 | Cero instant repetidos | R | STAT-002/003/005/006 y STAT-004, ISSUE-001 |
| AF014 | 5 | Cero timestamp repetidos | R | STAT-002/003/005/006 y STAT-004, ISSUE-001 |
| AF015 | 5 | Cero códigos fuera de dominio | R | STAT-002/003/005/006 y STAT-004, ISSUE-001 |
| AF016 | 5 | Identidad cnt=casual+registered sin discrepancias | R | STAT-002/003/005/006 y STAT-004, ISSUE-001 |
| AF017 | 5 | 165 horas teóricas ausentes | R | STAT-002/003/005/006 y STAT-004, ISSUE-001 |
| AF018 | 5 | Huecos limitan comparaciones de sumas con cobertura distinta | R | STAT-002/003/005/006 y STAT-004, ISSUE-001 |
| AF019 | 7 | Total observado 3292679 | R | STAT-008/009 |
| AF020 | 7 | Registered cuota acumulada 81,2% | R | STAT-008/009 |
| AF021 | 7 | Casual cuota acumulada 18,8% | R | STAT-008/009 |
| AF022 | 7 | Media cnt yr0 143,8 | R | STAT-008/009 |
| AF023 | 7 | Media cnt yr1 234,7 | R | STAT-008/009 |
| AF024 | 7 | Media cnt mayor en yr1 | R | STAT-008/009 |
| AF025 | 7 | Suma cnt mayor en yr1 | R | STAT-008/009 |
| AF026 | 9 | Perfiles horarios distintos por workingday | R | STAT-011/009 |
| AF027 | 9 | Pico laboral a las 8 h | R | STAT-011/009 |
| AF028 | 9 | Media laboral hr8 477,0 | R | STAT-011/009 |
| AF029 | 9 | Máximo laboral a las 17 h | R | STAT-011/009 |
| AF030 | 9 | Media laboral hr17 525,3 | R | STAT-011/009 |
| AF031 | 9 | Máximo no laboral a las 13 h | R | STAT-011/009 |
| AF032 | 9 | Media no laboral hr13 372,7 | R | STAT-011/009 |
| AF033 | 9 | No laborables concentran mayores medias en mediodía y tarde temprana | R | STAT-011/009 |
| AF034 | 9 | Medias cnt disminuyen de weathersit1 a 4 | R | STAT-011/009 |
| AF035 | 9 | Comparación meteorológica sin ajuste simultáneo de calendario | R | STAT-011/009 |
| AF036 | 13 | CSV horario Bike Sharing hour.csv | R | STAT-001, CSV y Readme |
| AF037 | 13 | Fila definida por fecha y hora | R | STAT-001, CSV y Readme |
| AF038 | 13 | Incluye calendario | R | STAT-001, CSV y Readme |
| AF039 | 13 | Incluye meteorología normalizada | R | STAT-001, CSV y Readme |
| AF040 | 13 | Incluye los recuentos casual, registered y cnt | R | STAT-001, CSV y Readme |
| AF041 | 15 | Se examina estructura | R | STAT-001 a STAT-014 y código de traza |
| AF042 | 15 | Se examina calidad | R | STAT-001 a STAT-014 y código de traza |
| AF043 | 15 | Se examinan distribuciones | R | STAT-001 a STAT-014 y código de traza |
| AF044 | 15 | Se realizan agregaciones temporales | R | STAT-001 a STAT-014 y código de traza |
| AF045 | 15 | Se examina composición | R | STAT-001 a STAT-014 y código de traza |
| AF046 | 15 | Se calculan asociaciones de calendario | R | STAT-001 a STAT-014 y código de traza |
| AF047 | 15 | Se calculan asociaciones meteorológicas | R | STAT-001 a STAT-014 y código de traza |
| AF048 | 15 | No se entrenan modelos predictivos | R | STAT-001 a STAT-014 y código de traza |
| AF049 | 15 | No se realizan estimaciones causales | R | STAT-001 a STAT-014 y código de traza |
| AF050 | 19 | Fuente tiene 17 columnas | R | STAT-001/004 |
| AF051 | 19 | Primera marca 2011-01-01 00:00:00 | R | STAT-001/004 |
| AF052 | 19 | Última marca 2012-12-31 23:00:00 | R | STAT-001/004 |
| AF053 | 19 | hr y documentación acreditan granularidad horaria | R | STAT-001/004 |
| AF054 | 25 | Todas las fechas convertidas sin fallos | R | STAT-003 |
| AF055 | 26 | yr coincide con fecha | R | STAT-005 y fechas fuente |
| AF056 | 26 | mnth coincide con fecha | R | STAT-005 y fechas fuente |
| AF057 | 26 | weekday coincide con fecha | R | STAT-005 y fechas fuente |
| AF058 | 26 | workingday coincide con calendario y holiday | R | STAT-005 y fechas fuente |
| AF059 | 26 | weekday0 corresponde a Sunday | R | STAT-005 y fechas fuente |
| AF060 | 26 | weekday6 corresponde a Saturday | R | STAT-005 y fechas fuente |
| AF061 | 28 | Sin recuentos negativos | R | STAT-006 |
| AF062 | 28 | Cuatro variables meteorológicas en [0,1] | R | STAT-006 |
| AF063 | 31 | Las 17 variables fuente se conservan | R | TR-001/002, profile y CSV |
| AF064 | 31 | dteday analizada como fecha | R | TR-001/002, profile y CSV |
| AF065 | 31 | dteday serializada ISO | R | TR-001/002, profile y CSV |
| AF066 | 31 | timestamp corresponde a fecha más hora | R | TR-001/002, profile y CSV |
| AF067 | 31 | season_label corresponde a código season | R | TR-001/002, profile y CSV |
| AF068 | 31 | weathersit_label corresponde a código meteorológico | R | TR-001/002, profile y CSV |
| AF069 | 31 | weekday_label corresponde al día de semana | R | TR-001/002, profile y CSV |
| AF070 | 31 | user_total_check corresponde a casual+registered | R | TR-001/002, profile y CSV |
| AF071 | 31 | Derivadas no sustituyen columnas fuente | R | TR-001/002, profile y CSV |
| AF072 | 33 | 505 valores horarios altos según IQR | R | STAT-014/006, ISSUE-002 y CSV |
| AF073 | 33 | Umbral IQR superior 642,5 | R | STAT-014/006, ISSUE-002 y CSV |
| AF074 | 33 | No hay evidencia interna de error en los extremos | R | STAT-014/006, ISSUE-002 y CSV |
| AF075 | 33 | Extremos respetan rangos y claves temporales | R | STAT-014/006, ISSUE-002 y CSV |
| AF076 | 33 | Extremos respetan identidad de componentes | R | STAT-014/006, ISSUE-002 y CSV |
| AF077 | 37 | Media global cnt 189,5 | R | STAT-007.cnt |
| AF078 | 37 | Mediana global cnt 142 | R | STAT-007.cnt |
| AF079 | 37 | Cnt cuartil1 40 | R | STAT-007.cnt |
| AF080 | 37 | Cnt cuartil3 281 | R | STAT-007.cnt |
| AF081 | 37 | Máximo cnt 977 | R | STAT-007.cnt |
| AF082 | 37 | Mínimo cnt 1 | R | STAT-007.cnt |
| AF083 | 37 | Cnt presenta dispersión considerable y cola alta | R | STAT-007.cnt |
| AF084 | 39 | Casual media 35,7 | R | STAT-007/008 |
| AF085 | 39 | Casual mediana 17 | R | STAT-007/008 |
| AF086 | 39 | Registered media 153,8 | R | STAT-007/008 |
| AF087 | 39 | Registered mediana 115 | R | STAT-007/008 |
| AF088 | 39 | Registered total 2672662 | R | STAT-007/008 |
| AF089 | 39 | Casual total 620017 | R | STAT-007/008 |
| AF090 | 39 | Componentes presentan heterogeneidad | R | STAT-007/008 |
| AF091 | 41 | Temp mediana 0,50 | R | STAT-007 y Readme |
| AF092 | 41 | Atemp mediana 0,4848 | R | STAT-007 y Readme |
| AF093 | 41 | Hum mediana 0,63 | R | STAT-007 y Readme |
| AF094 | 41 | Windspeed mediana 0,194 | R | STAT-007 y Readme |
| AF095 | 41 | Meteorología no almacenada directamente en unidades físicas | R | STAT-007 y Readme |
| AF096 | 41 | Documentación indica divisores de normalización | R | STAT-007 y Readme |
| AF097 | 43 | Yr0 corresponde a 2011 | R | STAT-009.by_yr y Readme |
| AF098 | 43 | Yr1 corresponde a 2012 | R | STAT-009.by_yr y Readme |
| AF099 | 43 | Yr0 tiene 8645 registros | R | STAT-009.by_yr y Readme |
| AF100 | 43 | Yr1 tiene 8734 registros | R | STAT-009.by_yr y Readme |
| AF101 | 43 | Yr0 total cnt 1243103 | R | STAT-009.by_yr y Readme |
| AF102 | 43 | Yr1 total cnt 2049576 | R | STAT-009.by_yr y Readme |
| AF103 | 47 | 731 fechas observadas | R | STAT-010, ISSUE-001 |
| AF104 | 47 | Máximo diario registrado 8714 | R | STAT-010, ISSUE-001 |
| AF105 | 47 | Fecha máximo diario 2012-09-15 | R | STAT-010, ISSUE-001 |
| AF106 | 47 | Máximo diario corresponde a 24 horas registradas | R | STAT-010, ISSUE-001 |
| AF107 | 47 | Mínimo diario registrado 22 | R | STAT-010, ISSUE-001 |
| AF108 | 47 | Fecha mínimo diario 2012-10-29 | R | STAT-010, ISSUE-001 |
| AF109 | 47 | Mínimo diario contiene una hora observada | R | STAT-010, ISSUE-001 |
| AF110 | 47 | Mínimo diario incompleto no equivale a demanda de día completo | R | STAT-010, ISSUE-001 |
| AF111 | 51 | Registered domina los picos laborales | R | STAT-011.by_hr_workingday y STAT-008 |
| AF112 | 51 | La composición horaria varía entre segmentos | R | STAT-011.by_hr_workingday y STAT-008 |
| AF113 | 53 | Media weathersit1 204,9 | R | STAT-009.by_weathersit y Readme |
| AF114 | 53 | Media weathersit2 175,2 | R | STAT-009.by_weathersit y Readme |
| AF115 | 53 | Media weathersit3 111,6 | R | STAT-009.by_weathersit y Readme |
| AF116 | 53 | Media weathersit4 74,3 | R | STAT-009.by_weathersit y Readme |
| AF117 | 53 | Weathersit1 representa clear_or_partly_cloudy | R | STAT-009.by_weathersit y Readme |
| AF118 | 53 | Weathersit2 representa mist_or_cloudy | R | STAT-009.by_weathersit y Readme |
| AF119 | 53 | Weathersit3 agrupa precipitación ligera | R | STAT-009.by_weathersit y Readme |
| AF120 | 53 | Weathersit4 agrupa precipitación intensa | R | STAT-009.by_weathersit y Readme |
| AF121 | 53 | Weathersit4 tiene tres observaciones | R | STAT-009.by_weathersit y Readme |
| AF122 | 53 | Media de weathersit4 inestable por tamaño mínimo | R | STAT-009.by_weathersit y Readme |
| AF123 | 55 | Spearman cnt-temp 0,423 | R | STAT-013 |
| AF124 | 55 | Spearman cnt-atemp 0,423 | R | STAT-013 |
| AF125 | 55 | Spearman cnt-hum −0,360 | R | STAT-013 |
| AF126 | 55 | Spearman cnt-windspeed 0,127 | R | STAT-013 |
| AF127 | 55 | Pearson temp-atemp muy elevado | R | STAT-013 |
| AF128 | 55 | Temp y atemp son redundantes descriptivamente | R | STAT-013 |
| AF129 | 55 | Asociaciones bivariadas no ajustan por hora, año y estación | R | STAT-013 |
| AF130 | 59 | FIG-001 representa agregación diaria de ambos años | R | FIG-001 y STAT-010 |
| AF131 | 59 | FIG-001 muestra variación sustancial | R | FIG-001 y STAT-010 |
| AF132 | 59 | Agregación diaria evita saturación de serie horaria | R | FIG-001 y STAT-010 |
| AF133 | 63 | FIG-002 muestra perfiles separados por workingday | R | FIG-002 y STAT-011 |
| AF134 | 63 | FIG-002 muestra picos laborales mañana y tarde y máximo no laboral al mediodía | R | FIG-002 y STAT-011 |
| AF135 | 67 | FIG-003 representa medias horarias de los componentes | R | FIG-003 y STAT-011.by_hr_overall |
| AF136 | 67 | Registered es el componente mayoritario de los picos globales | R | FIG-003 y STAT-011.by_hr_overall |
| AF137 | 67 | Casual presenta medias globales menores que registered | R | FIG-003 y STAT-011.by_hr_overall |
| AF138 | 71 | FIG-004 representa dispersión central cnt dentro de cada categoría meteorológica | R | FIG-004, STAT-009 y código gráfico |
| AF139 | 75 | FIG-005 compara meses por yr | R | FIG-005 y STAT-012 |
| AF140 | 75 | Patrones mensuales difieren entre años | R | FIG-005 y STAT-012 |
| AF141 | 75 | Comparación mensual complementa medias anuales | R | FIG-005 y STAT-012 |
| AF142 | 81 | 17544 horas teóricas dentro de cobertura | R | STAT-004, ISSUE-001 y CSV |
| AF143 | 81 | No falta ningún día completo | R | STAT-004, ISSUE-001 y CSV |
| AF144 | 81 | No se crean filas artificiales | R | STAT-004, ISSUE-001 y CSV |
| AF145 | 81 | Horas ausentes no equivalen a cnt=0 | R | STAT-004, ISSUE-001 y CSV |
| AF146 | 81 | Sumas de fechas incompletas pueden subestimar un día completo | R | STAT-004, ISSUE-001 y CSV |
| AF147 | 83 | Extremos influyen en media | R | STAT-014, ISSUE-002 y STAT-007 |
| AF148 | 83 | Extremos influyen en desviación típica | R | STAT-014, ISSUE-002 y STAT-007 |
| AF149 | 83 | Se ofrecen mediana y cuantiles para complementar resúmenes | R | STAT-014, ISSUE-002 y STAT-007 |
| AF150 | 89 | No son viajes individuales | R | Profile, columnas CSV y Readme |
| AF151 | 89 | No contiene estaciones | R | Profile, columnas CSV y Readme |
| AF152 | 89 | No contiene origen de viajes | R | Profile, columnas CSV y Readme |
| AF153 | 89 | No contiene destino de viajes | R | Profile, columnas CSV y Readme |
| AF154 | 89 | No contiene duración individual | R | Profile, columnas CSV y Readme |
| AF155 | 89 | No hay información individual más allá de tipos casual/registered | R | Profile, columnas CSV y Readme |
| AF156 | 89 | No describe movilidad espacial | R | Profile, columnas CSV y Readme |
| AF157 | 89 | No describe comportamiento individual | R | Profile, columnas CSV y Readme |
| AF158 | 91 | Archivo no identifica razón de cada ausencia | R | ISSUE-001 y columnas CSV |
| AF159 | 93 | Comparaciones meteorológicas son descriptivas | R | STAT-013 y código |
| AF160 | 93 | Relaciones bivariadas pueden mezclar calendario y meteorología | R | STAT-013 y código |
| AF161 | 95 | Dataset no contiene variables de contexto operativo por observación | R | Columnas CSV y Readme |
| AF162 | 95 | La documentación suministrada no aporta información de eventos que permita explicar picos o caídas concretas | R | El Readme menciona Sandy como pista, no como explicación demostrada de cada extremo. Se acepta la cautela causal. |
| AF163 | 95 | No se atribuyen los extremos a sucesos específicos | R | ISSUE-002 y report final |

