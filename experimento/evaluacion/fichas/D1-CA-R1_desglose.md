# Evaluación D1-CA-R1

**Índice final:** 89,27/100.  
**Evaluación cerrada:** 6 de octubre de 2026.  
**Ejecución:** `D1_bike_sharing__crewai__r01__20260831T173704649061Z`

**Criterios:** [Protocolo de evaluación](../01_protocolo_calidad_Q1_Q10_v0.1.md) y [guía D1](../02_ficha_D1_bike_sharing.md).  
**Resultados:** [Archivos originales de la ejecución](../../../outputs/experimento/D1_bike_sharing__crewai__r01__20260831T173704649061Z).  
**Evaluación:** [Excel de puntuaciones](../Evaluacion_calidad.xlsx) y [JSON de comprobaciones](D1-CA-R1_comprobaciones.json).

Las referencias `STAT`, `ISSUE` y `FIG` identifican análisis, problemas y figuras en los archivos de la ejecución. Las referencias a líneas corresponden a su informe original, `report.md`.

## Resumen

| Métrica | Puntuación final |
| --- | ---: |
| Q1 Cumplimiento de las etapas | 100,00 |
| Q2 Corrección numérica | 85,71 |
| Q3 Validez del tratamiento de los datos | 100,00 |
| Q4 Detección de problemas y riesgos | 100,00 |
| Q5 Calidad y profundidad del EDA | 75,00 |
| Q6 Profundidad de la interpretación | 75,00 |
| Q7 Calidad de las visualizaciones | 100,00 |
| Q8 Cobertura del informe | 77,27 |
| Q9 Fidelidad del informe | 99,35 |
| Q10 Claridad y coherencia | 75,00 |

## Q1 Cumplimiento de las etapas: 100,00

| ID | Puntos | Etapa | Evidencia |
| --- | --- | --- | --- |
| E1 Carga e inspección inicial | 1 | Carga e inspección | STAT-001 y profile, filas, columnas y unidad de observación |
| E2 Estructura, tipos y calidad | 1 | Tipos y calidad | profile.columns, STAT-002/003/004 y CHK-001 a CHK-007 |
| E3 Preparación y decisiones de análisis | 1 | Preparación válida | TR-001/002/003, CSV de 17379 x 20 y contraste de fecha-hora y columnas fuente |
| E4 Estadística descriptiva | 1 | Descripción reproducible | STAT-005, conteos y escalas ambientales, rangos y cuartiles |
| E5 Variables, agregaciones y relaciones | 1 | Relaciones y agregaciones | STAT-006/007/008, año, temporada, meteorología, mes, perfiles y Spearman |
| E6 Visualizaciones | 1 | Figuras utilizables | FIG-001 a FIG-005, PNG abiertos y contrastados con agregaciones |
| E7 Problemas, riesgos y anomalías | 1 | Riesgos estructurados | issues.json, controles CHK-001 a CHK-007 e ISSUE-001/002 |
| E8 Informe final | 1 | Informe final integrado | report.md, alcance, preparación, hallazgos y limitaciones |

`Q1 = 100 x 8 / 8 = 100,00`

## Q2 Corrección numérica: 85,71

Se consideran correctas 22 de las 26 comprobaciones, con un peso acumulado de 30 sobre 35. Permanecen ausentes C14, C17, C24 y C25.

| Control | Peso | Resultado | Valor | Evidencia |
| --- | ---: | --- | --- | --- |
| C01 Número de filas | 2 | Correcta | 17379 | STAT-001.rows |
| C02 Número de columnas | 2 | Correcta | 17 | STAT-001.columns |
| C03 Fechas distintas | 1 | Correcta | 731 | STAT-001.unique_dates |
| C04 Celdas ausentes | 2 | Correcta | 0 | STAT-002.missing_by_column |
| C05 Filas duplicadas | 2 | Correcta | 0 | STAT-002.exact_duplicate_rows |
| C06 Huecos en la secuencia horaria | 1 | Correcta | 165 | STAT-004.missing_hour_slots |
| C07 Alquileres totales | 2 | Correcta | 3292679 | STAT-006.result.by_year[].total_cnt. Suma de los dos totales anuales |
| C08 Media horaria de alquileres | 2 | Correcta | 189,463088 | STAT-005.cnt.mean |
| C09 Mediana horaria de alquileres | 1 | Correcta | 142 | STAT-005.cnt.median |
| C10 Desviación típica muestral | 1 | Correcta | 181,387599 | STAT-005.cnt.std |
| C11 Máximo horario | 1 | Correcta | 977 | STAT-005.cnt.max |
| C12 Total de alquileres de usuarios ocasionales | 1 | Correcta | 620017 | STAT-006.result.by_year[].casual. Suma de los dos totales anuales |
| C13 Total de alquileres de usuarios registrados | 1 | Correcta | 2672662 | STAT-006.result.by_year[].registered. Suma de los dos totales anuales |
| C14 Proporción de alquileres de usuarios registrados sobre el total | 1 | Ausente | — | No se emitió el resultado exigido. |
| C15 Alquileres totales en 2011 | 1 | Correcta | 1243103 | STAT-006.by_year[yr=0].total_cnt |
| C16 Alquileres totales en 2012 | 1 | Correcta | 2049576 | STAT-006.by_year[yr=1].total_cnt |
| C17 Variación total de 2012 respecto a 2011 | 2 | Ausente | — | No se emitió el resultado exigido. |
| C18 Hora con mayor media | 2 | Correcta | 17, 461,452055 | STAT-007.result.hourly_by_workingday, hora 17. Media ponderada de los grupos laborable y no laborable según su número de observaciones |
| C19 Hora con menor media | 1 | Correcta | 4, 6,35294118 | STAT-007.result.hourly_by_workingday, hr=4, workingday=0 y 1. Suma de (media x n) / suma de n por hora |
| C20 Temporada con mayor media | 1 | Correcta | 3, 236,016237 | STAT-006.by_season[season=3].mean_cnt |
| C21 Media con tiempo despejado | 1 | Correcta | 1, 204,869272 | STAT-006.by_weathersit[weathersit=1].mean_cnt |
| C22 Media con tiempo adverso de categoría 3 | 1 | Correcta | 3, 111,579281 | STAT-006.by_weathersit[weathersit=3].mean_cnt |
| C23 Observaciones meteorológicas de categoría 4 | 1 | Correcta | 3 | STAT-006.by_weathersit[weathersit=4].n |
| C24 Correlación de Pearson entre temperatura y cnt | 1 | Ausente | — | No se emitió el resultado exigido. |
| C25 Correlación de Pearson entre humedad y cnt | 1 | Ausente | — | No se emitió el resultado exigido. |
| C26 Inconsistencias en cnt = casual + registered | 2 | Correcta | 0 | STAT-003.identity_cnt_equals_components_violations |

`Q2 = 100 x 30 / 35 = 85,71`

## Q3 Validez del tratamiento de los datos: 100,00

| ID | Puntos | Decisión | Evidencia |
| --- | --- | --- | --- |
| D01 | 1 | Fecha-hora correcta | TR-001/002, date_hour coincide con dteday + hr en las 17379 filas |
| D02 | 1 | Códigos usados como categorías | STAT-003, STAT-006/007 y código del evento 16. Los códigos se utilizan como categorías para formar los grupos del análisis |
| D03 | 1 | instant como identificador | STAT-002, controles de identificadores y STAT-009, localizador del máximo. No se usa como predictor ni correlación |
| D04 | 1 | Conservación sin limpieza innecesaria | STAT-002 y TR-003, sin nulos ni duplicados, 17379 filas conservadas |
| D05 | 1 | No imputación de huecos | STAT-004, ISSUE-001 y código del evento 16, conserva las horas observadas |
| D06 | 1 | Extremos conservados | STAT-009 e ISSUE-002, regla IQR no se interpreta como error |
| D07 | 1 | Identidad preservada e interpretada | STAT-003 y report.md, líneas 3, 25 y 49 |
| D08 | 1 | Escalas normalizadas preservadas | STAT-003, TR-003 y report.md, líneas 17, 37 y 93 |

`Q3 = 100 x 8 / 8 = 100,00`

## Q4 Detección de problemas y riesgos: 100,00

| ID | Clasificación | Riesgo | Evidencia |
| --- | --- | --- | --- |
| R01 | Completo | Identificador secuencial | STAT-002, título de control de identificadores, secuencia y uso de instant solo para identificación en STAT-009. Se contrasta el uso efectivo, no solo el plan |
| R02 | Completo | Códigos numéricos categóricos/binarios | STAT-003 verifica los ocho dominios y STAT-006/007 agrupa sin tratarlos como medidas continuas |
| R03 | Completo | Identidad de componentes | STAT-003 y report.md, línea 49, no son resultados independientes |
| R04 | Completo | Normalización meteorológica | STAT-003 y report.md, líneas 17 y 93 |
| R05 | Completo | 165 horas ausentes | STAT-004 e ISSUE-001, exposición desigual y no imputación |
| R06 | Completo | Categoría meteorológica 4 con n = 3 | STAT-006 y report.md, líneas 41, 63 y 93 |
| R07 | Completo | Dependencia y redundancia temporal | STAT-003, yr/mnth/weekday derivados de fecha, report.md, líneas 51 y 91, dependencia entre horas |
| A01 | Adicional válido | Redundancia temp-atemp | STAT-008, Spearman 0,9896, report.md, líneas 51 y 101 |
| A02 | Adicional válido | Sensibilidad de la media a extremos altos | STAT-009 e ISSUE-002, 505 extremos, conservados sin falsa clasificación de error |
| A03 | Adicional válido | Limitación por agregación horaria | profile.unit_of_analysis y report.md, líneas 15 y 87, no permite mecanismos individuales |

K = 7 riesgos previstos completos, A = 3 adicionales válidos, F = 0 falsas alarmas. Precisión = 10/10 = 1. Cobertura = 7/7 = 1.

`Q4 = 100 x (2 x 1 x 1) / (1 + 1) = 100,00`

## Q5 Calidad y profundidad del EDA: 75,00

Compara distribuciones, calendario, meteorología, composición y relaciones, y considera extremos y cobertura. Se asigna 3/4 porque quedan incompletos la composición global, el cambio anual porcentual y el perfil horario global.

Evidencia: STAT-005 a STAT-009, report.md líneas 33–51 y 79–93.

`Q5 = 100 x 3 / 4 = 75,00`

## Q6 Profundidad de la interpretación: 75,00

El informe relaciona los resultados con la cobertura temporal, los tamaños de los grupos y las limitaciones del análisis. Sin embargo, interpreta los picos laborables como "horas de desplazamiento", aunque los datos no recogen los motivos de los viajes y esa explicación no se presenta claramente como hipótesis.

Evidencia: report.md, líneas 45, 49, 51, 59, 67, 79, 81 y 91, AF130.

`Q6 = 100 x 3 / 4 = 75,00`

## Q7 Calidad de las visualizaciones: 100,00

| ID | Nota 0–4 | Objetivo | Evidencia y juicio |
| --- | --- | --- | --- |
| V01 | 4 | Evolución 2011–2012 | FIG-001, series mensuales por año, sumas observadas y explicación de cobertura, líneas 45 y 55 |
| V02 | 4 | Perfil laborable/no laborable | FIG-002 y FIG-005, 24 horas ordenadas, leyenda y medias, STAT-007 y líneas 47, 59 y 71 |
| V03 | 4 | Estacionalidad ordenada | FIG-001, meses 1 a 12 en orden natural y ambas series anuales, líneas 45 y 55 |
| V04 | 4 | Meteorología y grupo pequeño | FIG-003 y STAT-006. Las categorías y medias son correctas. El informe advierte que la categoría 4 solo contiene tres observaciones, líneas 41, 63 y 93. |
| V05 | 4 | Relación entre temperatura y alquileres | FIG-004. Las observaciones se agrupan en hexágonos cuyo color indica su cantidad, lo que permite representar la relación sin superponer todos los puntos. Ejes claros, línea 67 |

`Q7 = 100 x 20 / 20 = 100,00`

## Q8 Cobertura del informe: 77,27

| ID | Peso | Nota | Puntos | Justificación |
| --- | --- | --- | --- | --- |
| U01 | 2 | 1 | 2 | Estructura y periodo comunicados, líneas 3 y 13 |
| U02 | 2 | 1 | 2 | Ausencias y duplicados distintos de las 165 horas ausentes, líneas 21 y 29 |
| U03 | 2 | 1 | 2 | Media, mediana, dispersión, cuartiles y rango correctos, líneas 5 y 33 |
| U04 | 2 | 0 | 0 | No indica qué porcentaje de todos los alquileres corresponde a usuarios registrados. La media de la proporción de alquileres ocasionales por hora, presentada en la línea 35, es una medida diferente |
| U05 | 2 | 0,5 | 1 | Comunica los dos totales anuales y la dirección de la diferencia sin causalidad, línea 39. Falta el crecimiento del 64,88 %, por eso recibe crédito parcial |
| U06 | 2 | 0 | 0 | El informe presenta las horas de mayor demanda por separado para días laborables y no laborables, pero no identifica las horas con mayor y menor media del conjunto completo |
| U07 | 2 | 1 | 2 | Máximos por tipo de día correctos y explicados, líneas 7 y 47 |
| U08 | 1 | 1 | 1 | Diferencias mensuales y estacionales correctas, temporada 3 con mayor media inequívoca, líneas 41 y 45 |
| U09 | 2 | 1 | 2 | Menor demanda con categorías adversas y n = 3 explícito, líneas 41 y 63 |
| U10 | 2 | 1 | 2 | Spearman temperatura/humedad prudente, sin causalidad, línea 51 |
| U11 | 2 | 1 | 2 | Identidad exacta y no independencia, líneas 3, 25 y 49 |
| U12 | 1 | 1 | 1 | Washington D.C., dependencia temporal y ausencia de base causal explícitas, líneas 3, 51 y 91 |

`Q8 = 100 x 17 / 22 = 77,27`

## Q9 Fidelidad del informe: 99,35

Se respaldan 154 de las 155 afirmaciones revisadas. AF130, que relaciona los picos laborables con "horas de desplazamiento", carece de respaldo suficiente porque el dataset no recoge los motivos de los viajes. No se identifican afirmaciones contradichas.


El inventario situado al final de esta ficha recoge las afirmaciones revisadas, su clasificación y las evidencias utilizadas. R significa afirmación respaldada y S, afirmación sin respaldo suficiente.

`Q9 = 100 x 154 / 155 = 99,35`

## Q10 Claridad y coherencia: 75,00

El informe está ordenado y conecta texto, estadísticas y figuras. Repite prácticamente el perfil horario en dos imágenes y explica poco algunas variables codificadas. Se asigna 3/4 por esas carencias de comunicación.

Evidencia: report.md y FIG-002/FIG-005.

`Q10 = 100 x 3 / 4 = 75,00`

## Inventario de afirmaciones

Detalle de Q9 para comprobar el recuento. Las líneas corresponden al informe original, report.md

| ID | Líneas del informe | Afirmación distinta | Evidencia | Estado |
| --- | --- | --- | --- | --- |
| AF001 | 3 | El dataset procede de Capital Bikeshare en Washington D.C. | Readme.txt, sección Data Set | R |
| AF002 | 3 | La unidad es una hora agregada, no un viaje individual. | Readme.txt, Files y profile.unit_of_analysis | R |
| AF003 | 3 | La fila no representa una estación. | Readme.txt y columnas de STAT-001 | R |
| AF004 | 3,13,21,27,33,97 | Hay 17379 registros originales y se conservan 17379 preparados. | STAT-001.rows y profile.original_rows/prepared_rows, contraste CSV | R |
| AF005 | 3,21 | La fecha inicial es 2011-01-01. | STAT-001.date_min | R |
| AF006 | 3,21 | La fecha final es 2012-12-31. | STAT-001.date_max | R |
| AF007 | 3,25,77 | cnt = casual + registered en todas las filas, con cero incumplimientos. | STAT-003.identity_cnt_equals_components_violations | R |
| AF008 | 3,21,77 | No hay celdas ausentes en las columnas fuente. | STAT-002.missing_by_column | R |
| AF009 | 3,21,77 | No hay filas duplicadas exactas. | STAT-002.exact_duplicate_rows | R |
| AF010 | 5,33,99 | Media horaria de cnt = 189,46. | STAT-005.cnt.mean | R |
| AF011 | 5,33,99 | Mediana de cnt = 142. | STAT-005.cnt.median | R |
| AF012 | 5,33 | Mínimo horario de cnt = 1. | STAT-005.cnt.min | R |
| AF013 | 5,33,81 | Máximo horario de cnt = 977. | STAT-005.cnt.max y STAT-009 | R |
| AF014 | 5 | Desviación típica de cnt = 181,39. | STAT-005.cnt.std | R |
| AF015 | 5,33 | La media supera a la mediana, compatible con una cola superior. | STAT-005.cnt y STAT-009, sin inferir una distribución paramétrica | R |
| AF016 | 5,99 | Los conteos horarios tienen amplia dispersión. | STAT-005.cnt, cuartiles, rango y desviación | R |
| AF017 | 7,39,99 | Media horaria de 2011 = 143,79. | STAT-006.by_year[yr=0].mean_hourly_cnt | R |
| AF018 | 7,39,99 | Media horaria de 2012 = 234,67. | STAT-006.by_year[yr=1].mean_hourly_cnt | R |
| AF019 | 7,99 | La media horaria observada es mayor en 2012 que en 2011. | STAT-006.by_year | R |
| AF020 | 7,47 | Media en laborables a las 08 h = 477,01. | STAT-007.hourly_by_workingday[workingday=1,hr=8] | R |
| AF021 | 7,47 | Media en laborables a las 17 h = 525,29. | STAT-007.hourly_by_workingday[workingday=1,hr=17] | R |
| AF022 | 7,47 | Las 08 y 17 h son picos locales del perfil laborable. | STAT-007, comparación con horas vecinas, FIG-002 | R |
| AF023 | 7,47 | El máximo medio no laborable está a las 13 h. | STAT-007.hourly_by_workingday[workingday=0], FIG-002 | R |
| AF024 | 7,47 | Media no laborable a las 13 h = 372,73. | STAT-007.hourly_by_workingday[workingday=0,hr=13] | R |
| AF025 | 7,47,99 | Los perfiles horarios difieren según el tipo de día. | STAT-007 y FIG-002/FIG-005 | R |
| AF026 | 9,21,29,79 | Hay 731 fechas distintas. | STAT-001.unique_dates y STAT-004.dates | R |
| AF027 | 9,29,79 | La retícula completa de 731 días contiene 17544 horas. | STAT-004.expected_hour_slots | R |
| AF028 | 9,29,79,89 | Faltan 165 franjas horarias. | STAT-004.missing_hour_slots | R |
| AF029 | 9,29,79 | 76 días tienen menos de 24 registros. | STAT-004.days_with_not_24_hours | R |
| AF030 | 9,29,79,89 | No se imputaron las horas ausentes. | preparation.TR-003, CSV conservado y traza, evento 16 | R |
| AF031 | 9,45,79 | Las sumas temporales son observadas, no ajustadas por horas ausentes. | STAT-007, código de agrupación del evento 16 e ISSUE-001 | R |
| AF032 | 13 | La fuente es un CSV horario. | Readme.txt, Files y entrada hour.csv | R |
| AF033 | 13 | Hay 17 columnas fuente. | STAT-001.columns y column_names | R |
| AF034 | 13 | instant forma parte de las columnas fuente. | STAT-001.column_names | R |
| AF035 | 13 | dteday forma parte de las columnas fuente. | STAT-001.column_names | R |
| AF036 | 13 | season, yr, mnth, hr, holiday, weekday y workingday son variables de calendario. | Readme.txt, Dataset characteristics y STAT-001.column_names | R |
| AF037 | 13 | weathersit, temp, atemp, hum y windspeed describen meteorología. | Readme.txt, Dataset characteristics | R |
| AF038 | 13 | casual, registered y cnt son conteos de alquileres. | Readme.txt, Dataset characteristics | R |
| AF039 | 15,21 | dteday y hr identifican la observación horaria sin duplicación. | STAT-001.unique_date_hour y STAT-002.duplicate_date_hour | R |
| AF040 | 15 | Se examinaron calidad, distribuciones, agregaciones y relaciones bivariadas. | STAT-002 a STAT-009 | R |
| AF041 | 15,87 | No hay información de trayectos individuales. | Columnas fuente, Readme.txt y unidad agregada | R |
| AF042 | 15,87 | No hay ubicación de estaciones. | Columnas fuente de STAT-001 | R |
| AF043 | 15,87 | No hay disponibilidad de bicicletas. | Columnas fuente de STAT-001 | R |
| AF044 | 15,87 | No hay capacidad del sistema. | Columnas fuente de STAT-001 | R |
| AF045 | 17,93 | temp se conserva en escala normalizada, no en grados físicos. | Readme.txt, STAT-003.normalized_ranges y contraste CSV | R |
| AF046 | 17,93 | atemp se conserva en escala normalizada, no en grados físicos. | Readme.txt, STAT-003.normalized_ranges y contraste CSV | R |
| AF047 | 17,93 | hum se conserva en escala normalizada, no en porcentaje físico. | Readme.txt, STAT-003.normalized_ranges y contraste CSV | R |
| AF048 | 17,93 | windspeed se conserva en escala normalizada, no en velocidad física. | Readme.txt, STAT-003.normalized_ranges y contraste CSV | R |
| AF049 | 21 | Hay 17379 combinaciones fecha-hora únicas. | STAT-001.unique_date_hour y contraste CSV | R |
| AF050 | 21 | No hay duplicados de instant. | STAT-002.duplicate_instant | R |
| AF051 | 21 | No hay duplicados de fecha-hora. | STAT-002.duplicate_date_hour | R |
| AF052 | 21 | instant es consecutivo entre 1 y 17379. | STAT-002.instant_consecutive_positions y contraste CSV | R |
| AF053 | 23 | season tiene cuatro categorías dentro de su dominio. | STAT-003.invalid_domain_counts y profile.columns | R |
| AF054 | 23 | yr tiene dos categorías dentro de su dominio. | STAT-003.invalid_domain_counts y profile.columns | R |
| AF055 | 23 | mnth respeta 1 a 12. | STAT-003.invalid_domain_counts.mnth | R |
| AF056 | 23 | hr respeta 0 a 23. | STAT-003.invalid_domain_counts.hr | R |
| AF057 | 23 | holiday es binaria. | STAT-003.invalid_domain_counts.holiday | R |
| AF058 | 23 | workingday es binaria. | STAT-003.invalid_domain_counts.workingday | R |
| AF059 | 23,77 | No hay valores fuera de los rangos normalizados revisados. | STAT-003.normalized_ranges | R |
| AF060 | 23,37 | Máximo de temp = 1. | STAT-003.normalized_ranges.temp y STAT-005.temp | R |
| AF061 | 23,37 | Máximo de atemp = 1. | STAT-003.normalized_ranges.atemp y STAT-005.atemp | R |
| AF062 | 23,37 | Máximo de hum = 1. | STAT-003.normalized_ranges.hum y STAT-005.hum | R |
| AF063 | 23,37 | Máximo de windspeed = 0,8507. | STAT-003.normalized_ranges.windspeed y STAT-005.windspeed | R |
| AF064 | 25 | yr coincide con el año de dteday. | STAT-003.year_code_matches_date | R |
| AF065 | 25 | mnth coincide con el mes de dteday. | STAT-003.month_matches_date | R |
| AF066 | 25 | weekday coincide con domingo codificado como 0. | STAT-003.weekday_matches_sunday_zero_code | R |
| AF067 | 25 | season no coincide exactamente con el trimestre natural. | STAT-003.season_matches_calendar_quarter, CHK-007 | R |
| AF068 | 25 | No se sustituyó season por el trimestre natural. | CSV conservado, preparation y código del evento 16 | R |
| AF069 | 27 | prepared_data.csv se creó separado de la fuente. | Archivo conservado y preparation | R |
| AF070 | 27 | dteday se convirtió a fecha y se guardó como ISO YYYY-MM-DD. | TR-001, código del evento 16 y contraste CSV | R |
| AF071 | 27 | Se añadió date_hour con fecha y hora. | TR-002 y contraste independiente de las 17379 filas | R |
| AF072 | 27 | Se añadió casual_share. | TR-002 y contraste casual/cnt | R |
| AF073 | 27 | Se añadió registered_share. | TR-002 y contraste registered/cnt | R |
| AF074 | 27,97 | Las 17 columnas fuente se conservan sin cambios en sus valores. | Contraste CSV y TR-003 | R |
| AF075 | 27,81 | No se eliminaron registros extremos. | TR-003, ISSUE-002 y contraste CSV | R |
| AF076 | 27 | No hay horas con cnt = 0. | STAT-005.cnt_zero_hours | R |
| AF077 | 29 | La incidencia estructural sustantiva detectada es la cobertura temporal. | STAT-002/003 sin errores, ISSUE-001, ISSUE-002 no clasifica extremos como errores | R |
| AF078 | 33 | Primer cuartil de cnt = 40. | STAT-005.cnt.p25 | R |
| AF079 | 33 | Tercer cuartil de cnt = 281. | STAT-005.cnt.p75 | R |
| AF080 | 35 | Media horaria de registered = 153,79. | STAT-005.registered.mean | R |
| AF081 | 35 | Media horaria de casual = 35,68. | STAT-005.casual.mean | R |
| AF082 | 35 | Media de las proporciones casual/cnt por hora = 0,1721. | STAT-005.casual_share_nonzero_cnt.mean | R |
| AF083 | 35 | Mediana de las proporciones casual/cnt por hora = 0,1469. | STAT-005.casual_share_nonzero_cnt.median | R |
| AF084 | 35 | Predominan los registrados en la hora típica observada. | Mediana casual_share menor que 0,5, STAT-005, sin afirmar cuota global | R |
| AF085 | 37 | Media normalizada de temp = 0,4970. | STAT-005.temp.mean | R |
| AF086 | 37 | Media normalizada de atemp = 0,4758. | STAT-005.atemp.mean | R |
| AF087 | 37 | Media normalizada de hum = 0,6272. | STAT-005.hum.mean | R |
| AF088 | 37 | Media normalizada de windspeed = 0,1901. | STAT-005.windspeed.mean | R |
| AF089 | 37 | Mínimo normalizado de temp = 0,02. | STAT-005.temp.min | R |
| AF090 | 37 | Mínimo normalizado de atemp = 0. | STAT-005.atemp.min | R |
| AF091 | 37 | Mínimo normalizado de hum = 0. | STAT-005.hum.min | R |
| AF092 | 37 | Mínimo normalizado de windspeed = 0. | STAT-005.windspeed.min | R |
| AF093 | 39 | Total observado de 2011 = 1243103 alquileres. | STAT-006.by_year[yr=0].total_cnt | R |
| AF094 | 39 | 2011 incluye 8645 horas. | STAT-006.by_year[yr=0].hours | R |
| AF095 | 39 | Total observado de 2012 = 2049576 alquileres. | STAT-006.by_year[yr=1].total_cnt | R |
| AF096 | 39 | 2012 incluye 8734 horas. | STAT-006.by_year[yr=1].hours | R |
| AF097 | 41 | Media horaria season 1 = 111,11. | STAT-006.by_season[season=1].mean_cnt | R |
| AF098 | 41 | Media horaria season 2 = 208,34. | STAT-006.by_season[season=2].mean_cnt | R |
| AF099 | 41 | Media horaria season 3 = 236,02. | STAT-006.by_season[season=3].mean_cnt | R |
| AF100 | 41 | Media horaria season 4 = 198,87. | STAT-006.by_season[season=4].mean_cnt | R |
| AF101 | 41,63 | Media horaria weathersit 1 = 204,87. | STAT-006.by_weathersit[weathersit=1].mean_cnt | R |
| AF102 | 41,63 | Media horaria weathersit 2 = 175,17. | STAT-006.by_weathersit[weathersit=2].mean_cnt | R |
| AF103 | 41,63 | Media horaria weathersit 3 = 111,58. | STAT-006.by_weathersit[weathersit=3].mean_cnt | R |
| AF104 | 41,63 | Media horaria weathersit 4 = 74,33. | STAT-006.by_weathersit[weathersit=4].mean_cnt | R |
| AF105 | 41,63,93 | weathersit 4 contiene tres observaciones. | STAT-006.by_weathersit[weathersit=4].n | R |
| AF106 | 41,63,93 | La media de weathersit 4 es frágil y no generalizable por su tamaño. | STAT-006, n=3 y advertencia explícita | R |
| AF107 | 45,55 | Las sumas mensuales muestran variación estacional y diferencias entre años. | STAT-007.monthly y FIG-001 | R |
| AF108 | 45 | Total de enero de 2011 = 38189. | STAT-007.monthly[yr=0,mnth=1].total_cnt | R |
| AF109 | 45 | Total de enero de 2012 = 96744. | STAT-007.monthly[yr=1,mnth=1].total_cnt | R |
| AF110 | 45 | Total de septiembre de 2011 = 127418. | STAT-007.monthly[yr=0,mnth=9].total_cnt | R |
| AF111 | 45 | Total de septiembre de 2012 = 218573. | STAT-007.monthly[yr=1,mnth=9].total_cnt | R |
| AF112 | 45,55,89 | Las horas observadas no son iguales en todos los meses. | STAT-007.monthly.hours y STAT-004 | R |
| AF113 | 47 | En no laborables la media aumenta de la mañana al mediodía. | STAT-007.hourly_by_workingday y FIG-002, tendencia no exige monotonía a las 0–6 h | R |
| AF114 | 47,51,67 | Las asociaciones no demuestran causalidad ni efectos aislados. | Código descriptivo del evento 16 y STAT-007/008, sin identificación causal | R |
| AF115 | 49 | Media de registered en laborables a las 17 h = 468,39. | STAT-007[workingday=1,hr=17].mean_registered | R |
| AF116 | 49 | Media de casual en laborables a las 17 h = 56,90. | STAT-007[workingday=1,hr=17].mean_casual | R |
| AF117 | 49 | Media de registered en no laborables a las 13 h = 236,31. | STAT-007[workingday=0,hr=13].mean_registered | R |
| AF118 | 49 | Media de casual en no laborables a las 13 h = 136,42. | STAT-007[workingday=0,hr=13].mean_casual | R |
| AF119 | 49 | La composición varía entre los dos perfiles horarios. | STAT-007, comparación de medias por componentes | R |
| AF120 | 49 | cnt y sus componentes no son resultados independientes. | STAT-003.identity_cnt_equals_components_violations | R |
| AF121 | 51 | Spearman temp-cnt = 0,4233. | STAT-008.spearman_cnt_with.temp | R |
| AF122 | 51 | Spearman atemp-cnt = 0,4233. | STAT-008.spearman_cnt_with.atemp | R |
| AF123 | 51 | Spearman hum-cnt = −0,3596. | STAT-008.spearman_cnt_with.hum | R |
| AF124 | 51 | Spearman windspeed-cnt = 0,1266. | STAT-008.spearman_cnt_with.windspeed | R |
| AF125 | 51 | Las correlaciones usan la muestra completa. | STAT-008.method y código del evento 16, sin filtro | R |
| AF126 | 51,91,101 | No se controló hora, estación, calendario o dependencia temporal. | Código bivariado del evento 16 y STAT-008 | R |
| AF127 | 51 | Spearman temp-atemp = 0,9896. | STAT-008.spearman_temp_atemp | R |
| AF128 | 51,101 | temp y atemp contienen información térmica redundante. | STAT-008.spearman_temp_atemp | R |
| AF129 | 55 | Los totales mensuales aumentan de 2011 a 2012. | STAT-007.monthly y FIG-001 | R |
| AF130 | 59 | Los picos laborables se asocian en el texto a horas de desplazamiento. | STAT-007 acredita horarios, pero no motivos de viaje | S |
| AF131 | 59 | El máximo no laborable se sitúa en primeras horas de la tarde. | STAT-007 máximo a las 13 h y FIG-002, formulación imprecisa pero compatible | R |
| AF132 | 63 | Las categorías meteorológicas menos severas tienen más observaciones. | STAT-006.by_weathersit.n | R |
| AF133 | 63 | Las categorías menos severas tienen medias superiores. | STAT-006.by_weathersit.mean_cnt y FIG-003 | R |
| AF134 | 67 | El hexbin representa densidad y dispersión de temp frente a cnt. | FIG-004, código de representación del evento 16 | R |
| AF135 | 67 | La asociación temp-cnt es positiva moderada. | STAT-008.temp y FIG-004 | R |
| AF136 | 71 | FIG-005 muestra medias horarias, no totales diarios. | FIG-005 y STAT-007 | R |
| AF137 | 77 | No se detectaron códigos inválidos en los dominios revisados. | STAT-003.invalid_domain_counts | R |
| AF138 | 81 | Hay 505 valores por encima de la cerca IQR superior. | STAT-009.flagged_count | R |
| AF139 | 81 | La cerca superior de cnt es 642,5. | STAT-009.upper_fence | R |
| AF140 | 81 | Los extremos suponen el 2,91 % de las observaciones. | STAT-009.flagged_proportion | R |
| AF141 | 81 | El identificador del máximo es 14774. | STAT-009.maximum_rows | R |
| AF142 | 81 | La fecha del máximo es 2012-09-12. | STAT-009.maximum_rows | R |
| AF143 | 81 | La hora del máximo es 18 h. | STAT-009.maximum_rows | R |
| AF144 | 81 | casual en el máximo = 91. | STAT-009.maximum_rows | R |
| AF145 | 81 | registered en el máximo = 886. | STAT-009.maximum_rows | R |
| AF146 | 81 | Los máximos cumplen dominios e identidad y no prueban un error. | STAT-003, STAT-009 e ISSUE-002 | R |
| AF147 | 83 | Los valores altos pueden influir en la media más que en la mediana. | STAT-005, STAT-009 e ISSUE-002, afirmación de sensibilidad potencial | R |
| AF148 | 83 | El archivo no permite conocer la causa operacional de un extremo. | Columnas de STAT-001 e ISSUE-002.uncertainty | R |
| AF149 | 87 | No hay origen ni destino de los viajes. | Columnas fuente de STAT-001 | R |
| AF150 | 87 | No hay características individuales de personas usuarias. | Columnas fuente de STAT-001, conteos casual/registered no son fichas individuales | R |
| AF151 | 87 | No se pueden atribuir los perfiles a mecanismos individuales concretos. | Unidad horaria agregada y ausencia de motivos/origen/destino | R |
| AF152 | 89 | No hay base para reconstruir verificablemente los conteos ausentes. | STAT-004 e ISSUE-001.uncertainty, no se afirma un valor para las horas faltantes | R |
| AF153 | 91 | Factores temporales simultáneos pueden contribuir a las asociaciones. | STAT-007/008 y limitación bivariada explícita, hipótesis no causal | R |
| AF154 | 97 | Los controles estructurales son favorables salvo cobertura horaria. | STAT-002/003, preparado conservado y STAT-004 | R |
| AF155 | 103 | Las horas ausentes condicionan la comparación directa de sumas. | STAT-004, STAT-007.hours e ISSUE-001.potential_effect | R |
