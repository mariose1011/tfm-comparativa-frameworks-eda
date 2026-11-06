# Evaluación D1-CA-R3

**Índice final:** 87,50/100.  
**Evaluación cerrada:** 6 de octubre de 2026.  
**Ejecución:** `D1_bike_sharing__crewai__r03__20260831T214619590910Z`

**Criterios:** [Protocolo de evaluación](../01_protocolo_calidad_Q1_Q10_v0.1.md) y [guía D1](../02_ficha_D1_bike_sharing.md).  
**Resultados:** [Archivos originales de la ejecución](../../../outputs/experimento/D1_bike_sharing__crewai__r03__20260831T214619590910Z).  
**Evaluación:** [Excel de puntuaciones](../Evaluacion_calidad.xlsx) y [JSON de comprobaciones](D1-CA-R3_comprobaciones.json).

Las referencias `STAT`, `ISSUE` y `FIG` identifican análisis, problemas y figuras en los archivos de la ejecución. `TR` identifica transformaciones y `CHK`, comprobaciones de calidad. Las referencias a líneas corresponden al informe original, `report.md`.

## Resumen

| Métrica | Puntuación final |
| --- | ---: |
| Q1 Cumplimiento de las etapas | 100,00 |
| Q2 Corrección numérica | 88,57 |
| Q3 Validez del tratamiento de los datos | 100,00 |
| Q4 Detección de problemas y riesgos | 92,31 |
| Q5 Calidad y profundidad del EDA | 75,00 |
| Q6 Profundidad de la interpretación | 75,00 |
| Q7 Calidad de las visualizaciones | 85,00 |
| Q8 Cobertura del informe | 79,55 |
| Q9 Fidelidad del informe | 97,83 |
| Q10 Claridad y coherencia | 75,00 |

## Q1 Cumplimiento de las etapas: 100,00

| Etapa | Nota | Evidencia |
| --- | ---: | --- |
| E1 Carga e inspección inicial | 1 | STAT-001 y profile |
| E2 Estructura, tipos y calidad | 1 | STAT-002/003/004/005 y CHK-001 a CHK-005 |
| E3 Preparación y decisiones de análisis | 1 | TR-001/002/003 y CSV, 17379 x 19 |
| E4 Estadística descriptiva | 1 | STAT-006/007 |
| E5 Variables, agregaciones y relaciones | 1 | STAT-008 a STAT-014 |
| E6 Visualizaciones | 1 | Cinco PNG identificables, cuatro correctamente vinculados |
| E7 Problemas, riesgos y anomalías | 1 | CHK-001 a CHK-006, ISSUE-001/002 y decisiones |
| E8 Informe final | 1 | Nueve secciones del informe final |

`Q1 = 100 x 8 / 8 = 100,00`

## Q2 Corrección numérica: 88,57

Se obtienen resultados correctos en 23 de las 26 comprobaciones, que suman 31 de los 35 puntos posibles. No se calcula el crecimiento porcentual entre 2011 y 2012 ni las dos correlaciones de Pearson previstas.

| Control | Peso | Resultado | Valor | Evidencia |
| --- | ---: | --- | --- | --- |
| C01 Número de filas | 2 | Correcta | 17379 | STAT-001.rows |
| C02 Número de columnas | 2 | Correcta | 17 | STAT-001.columns |
| C03 Fechas distintas | 1 | Correcta | 731 | STAT-004.unique_dates |
| C04 Celdas ausentes | 2 | Correcta | 0 | STAT-002.total_missing |
| C05 Filas duplicadas | 2 | Correcta | 0 | STAT-002.duplicate_rows |
| C06 Huecos en la secuencia horaria | 1 | Correcta | 165 | STAT-004.missing_hourly_timestamps |
| C07 Alquileres totales | 2 | Correcta | 3292679 | STAT-005.total_cnt |
| C08 Media horaria de alquileres | 2 | Correcta | 189,463088 | STAT-006.cnt.mean |
| C09 Mediana horaria de alquileres | 1 | Correcta | 142 | STAT-006.cnt.median |
| C10 Desviación típica muestral | 1 | Correcta | 181,387599 | STAT-006.cnt.std |
| C11 Máximo horario | 1 | Correcta | 977 | STAT-006.cnt.max |
| C12 Alquileres de usuarios ocasionales | 1 | Correcta | 620017 | STAT-011.overall.casual_total |
| C13 Alquileres de usuarios registrados | 1 | Correcta | 2672662 | STAT-011.overall.registered_total |
| C14 Proporción de alquileres de usuarios registrados | 1 | Correcta | 0,811698316 | STAT-011.overall.registered_share |
| C15 Alquileres totales en 2011 | 1 | Correcta | 1243103 | STAT-009.by_year.0.sum_cnt |
| C16 Alquileres totales en 2012 | 1 | Correcta | 2049576 | STAT-009.by_year.1.sum_cnt |
| C17 Variación total de 2012 respecto a 2011 | 2 | Ausente | — | Variación anual no producida |
| C18 Hora con mayor media | 2 | Correcta | 17, 461,452055 | STAT-008. Media conjunta de las 17 h: (74.740 + 262.120) / (231 + 499) |
| C19 Hora con menor media | 1 | Correcta | 4, 6,35294118 | STAT-008. Media conjunta de las 4 h: (1.876 + 2.552) / (227 + 470) |
| C20 Temporada con mayor media | 1 | Correcta | 3, 236,016 | STAT-009.by_season.fall.mean_cnt |
| C21 Media con tiempo despejado | 1 | Correcta | 1, 204,869 | STAT-009.by_weather.clear_or_partly_cloudy.mean_cnt |
| C22 Media con tiempo adverso de categoría 3 | 1 | Correcta | 3, 111,579 | STAT-009.by_weather.light_precipitation.mean_cnt |
| C23 Observaciones meteorológicas de categoría 4 | 1 | Correcta | 3 | STAT-009.by_weather.heavy_precipitation.n |
| C24 Correlación de Pearson entre temperatura y cnt | 1 | Ausente | — | Spearman no sustituye Pearson |
| C25 Correlación de Pearson entre humedad y cnt | 1 | Ausente | — | Spearman no sustituye Pearson |
| C26 Inconsistencias en cnt = casual + registered | 2 | Correcta | 0 | STAT-005.mismatch_rows |

`Q2 = 100 x 31 / 35 = 88,57`

## Q3 Validez del tratamiento de los datos: 100,00

| Decisión | Nota | Justificación y evidencia |
| --- | ---: | --- |
| D01 Fecha-hora | 1 | Traza 16/32: fecha válida más hr mediante timedelta, usada para comprobar cobertura. Las dos columnas se conservan en el CSV |
| D02 Categorías | 1 | Frecuencias y agrupaciones de los ocho códigos, sin usarlos indiscriminadamente como magnitudes. STAT-003/007/008/009 |
| D03 instant | 1 | Identificador y control de secuencia, no correlación explicativa. STAT-002/004/013 y código |
| D04 Ausencias y duplicados | 1 | Verificados inexistentes, no se eliminan filas. STAT-002 y TR-003 |
| D05 Huecos | 1 | 165 huecos detectados, sin imputación. STAT-004 e ISSUE-001 |
| D06 Extremos | 1 | 505 horas señaladas por IQR y conservadas por falta de evidencia de error. STAT-013 e ISSUE-002 |
| D07 Componentes de cnt | 1 | Se comprueba que `cnt = casual + registered` y se calculan las proporciones de ambos componentes, sin tratarlos como predictores independientes. STAT-005/011 |
| D08 Normalizadas | 1 | Escalas fuente conservadas y comunicadas. STAT-003/006 y report17/37/91 |

`Q3 = 100 x 8 / 8 = 100,00`

## Q4 Detección de problemas y riesgos: 92,31

| Riesgo | Clasificación | Evidencia |
| --- | --- | --- |
| R01 Identificador | Detectado | instant como identificador y secuencia, STAT-002/004 y código |
| R02 Códigos numéricos | Detectado | Dominios y etiquetas, STAT-003/007, TR-002 y report23 |
| R03 Identidad de componentes | Detectado | STAT-005/011 y report27 |
| R04 Normalización | Detectado | STAT-003/006 y report17/37/91 |
| R05 Huecos horarios | Detectado | STAT-004, ISSUE-001 y report79/93 |
| R06 Meteorología n=3 | Detectado | STAT-007/009 y report23/49/65/83 |
| R07 Dependencia y calendario | Parcial | Calendario comprobado, pero no se explicita dependencia entre observaciones sucesivas |
| A01 Redundancia temp-atemp | Adicional válido | Spearman 0,9896 y cautela sobre fuentes independientes, report51 |
| A02 Influencia de extremos válidos | Adicional válido | IQR, conservación y sensibilidad de medias/correlaciones, report81/95 |
| A03 Alcance agregado | Adicional válido | Falta información de viajes y operación individual, report89 y esquema |

Se identifican seis de los siete riesgos previstos y tres adicionales, sin falsas alarmas. La precisión es 1, la cobertura es 6/7 y F1 es 12/13.

`Q4 = 100 x [2 x 1 x (6 / 7)] / [1 + (6 / 7)] = 92,31`

## Q5 Calidad y profundidad del EDA: 75,00

El análisis examina distribuciones, diferencias de calendario, composición de los alquileres, meteorología y extremos. También relaciona el mínimo diario con la cobertura incompleta. Recibe 3 de 4 puntos porque no desarrolla la dependencia temporal y mantiene una discrepancia entre la figura de temperatura y las estadísticas incorporadas durante la corrección.

`Q5 = 100 x 3 / 4 = 75,00`

## Q6 Profundidad de la interpretación: 75,00

La interpretación explica las diferencias entre grupos, los tamaños muestrales pequeños, la redundancia entre variables y las limitaciones de las asociaciones, sin atribuir causalidad. Recibe 3 de 4 puntos porque describe FIG-005 mediante una agrupación que no corresponde a la imagen guardada. Evidencia: report43/49/51/73/79/81/89/91/93.

`Q6 = 100 x 3 / 4 = 75,00`

## Q7 Calidad de las visualizaciones: 85,00

| Objetivo | Nota | Justificación |
| --- | ---: | --- |
| V01 Evolución | 4 | Serie diaria de los dos años legible, con cautela de cobertura en el informe. FIG-001 |
| V02 Perfiles horarios | 4 | Dos curvas, horas completas y leyenda workingday, con máximos descritos. FIG-002 |
| V03 Patrón mensual/estacional | 4 | Meses ordenados cronológicamente y barras apiladas por tipo de usuario, acompañadas de una explicación del patrón mensual y de las medias por estación. FIG-004 y líneas 39 y 69 |
| V04 Meteorología | 4 | Medias por categoría documentada, etiquetas legibles y n=3 explicado junto a la imagen. FIG-003 y report65 |
| V05 Temperatura/demanda | 1 | Valores reales y gráfica legible, pero método y correspondencia con la evidencia final gravemente incorrectos. FIG-005, STAT-014 y report73 |

FIG-005 agrupa la temperatura en diez intervalos de igual anchura. Durante la corrección se calcularon nuevos grupos con aproximadamente el mismo número de observaciones y se incorporaron a STAT-014 y al informe, pero no se regeneró la imagen. Por ello, los límites y las medias de las estadísticas finales no corresponden a los representados en el gráfico.

`Q7 = 100 x 17 / 20 = 85,00`

## Q8 Cobertura del informe: 79,55

| Unidad | Peso | Nota | Motivo |
| --- | ---: | ---: | --- |
| U01 Estructura y periodo | 2 | 1 | Report3/15/21 |
| U02 Calidad y huecos | 2 | 1 | Report21/25/79 |
| U03 Nivel y dispersión | 2 | 1 | Report7/33 |
| U04 Cuota global registrados | 2 | 1 | 81,17 % explícito en report7 |
| U05 Crecimiento anual total | 2 | 0 | No comunica totales anuales ni su variación porcentual. Las medias de report39 son otra medida |
| U06 Extremos horarios globales | 2 | 0 | La línea 45 presenta las horas de mayor demanda por separado para días laborables y no laborables, pero no identifica el máximo y el mínimo del conjunto completo |
| U07 Extremos por tipo de día | 2 | 1 | Report45/61 y FIG-002 |
| U08 Estacionalidad | 1 | 1 | Diferencias estacionales y mayor media de fall, report39, junto al patrón mensual de FIG-004 |
| U09 Meteorología y n=3 | 2 | 1 | Report49/65 |
| U10 Temperatura y humedad | 2 | 1 | Spearman y cautelas correctas en report51. El defecto de FIG-005 no vuelve falsos estos resultados |
| U11 Identidad de componentes | 2 | 1 | Report27, composición y ausencia de modelización predictiva |
| U12 Límites temporal/ciudad/causal | 1 | 0,5 | Ciudad y causalidad explícitas, dependencia temporal no desarrollada |

`Q8 = 100 x 17,5 / 22 = 79,55`

## Q9 Fidelidad del informe: 97,83

De las 184 afirmaciones evaluadas, 180 tienen respaldo y cuatro están contradichas. Estas últimas corresponden a AF157–AF160, que atribuyen a FIG-005 el método de agrupación, los límites, los tamaños y las medias documentados en STAT-014, aunque la imagen representa otra agrupación.

El inventario situado al final de esta ficha recoge las afirmaciones revisadas, su clasificación y las evidencias utilizadas.

`Q9 = 100 x 180 / 184 = 97,83`

## Q10 Claridad y coherencia: 75,00

**Nivel 3/4 → 75.** Informe bien organizado, con alcance, hallazgos y limitaciones localizables. La explicación de FIG-005 rompe la correspondencia entre evidencia e interpretación y algunos códigos o conceptos se desarrollan poco. El conjunto sigue siendo comprensible, por lo que no se aplica el nivel 1 de contradicciones importantes generalizadas. Evidencia: informe completo, especialmente report73 y STAT-014.

`Q10 = 100 x 3 / 4 = 75,00`

## Inventario de afirmaciones

R = respaldada; C = contradicha.

| ID | Líneas del informe | Afirmación | Estado | Evidencia |
| --- | --- | --- | --- | --- |
| AF001 | 3,13,15,21 | Fuente Bike Sharing horario de Capital Bikeshare | R | STAT-001/004 y Readme |
| AF002 | 3,13,15,21 | Sistema ubicado en Washington D.C. | R | STAT-001/004 y Readme |
| AF003 | 3,13,15,21 | 17379 registros originales | R | STAT-001/004 y Readme |
| AF004 | 3,13,15,21 | 17 columnas originales | R | STAT-001/004 y Readme |
| AF005 | 3,13,15,21 | Primera fecha 2011-01-01 | R | STAT-001/004 y Readme |
| AF006 | 3,13,15,21 | Última fecha 2012-12-31 | R | STAT-001/004 y Readme |
| AF007 | 3,13,15,21 | 731 fechas distintas | R | STAT-001/004 y Readme |
| AF008 | 3,13,15,21 | Cada fila contiene alquileres agregados en una hora | R | STAT-001/004 y Readme |
| AF009 | 3,13,15,21 | El esquema contiene hr y concuerda con el archivo horario documentado | R | STAT-001/004 y Readme |
| AF010 | 3,29,99 | 17379 filas preparadas | R | TR-001/002/003, CSV y traza16/32 |
| AF011 | 3,29,99 | 19 columnas preparadas | R | TR-001/002/003, CSV y traza16/32 |
| AF012 | 3,29,99 | 17 columnas fuente conservadas | R | TR-001/002/003, CSV y traza16/32 |
| AF013 | 3,29,99 | Dos columnas derivadas añadidas | R | TR-001/002/003, CSV y traza16/32 |
| AF014 | 3,29,99 | season_label traduce season conforme a la documentación | R | TR-001/002/003, CSV y traza16/32 |
| AF015 | 3,29,99 | weathersit_label traduce weathersit conforme a la documentación | R | TR-001/002/003, CSV y traza16/32 |
| AF016 | 3,29,99 | dteday validada como fecha | R | TR-001/002/003, CSV y traza16/32 |
| AF017 | 3,29,99 | dteday serializada en formato ISO YYYY-MM-DD | R | TR-001/002/003, CSV y traza16/32 |
| AF018 | 3,29,99 | No se eliminaron observaciones | R | TR-001/002/003, CSV y traza16/32 |
| AF019 | 3,29,99 | No se imputaron observaciones | R | TR-001/002/003, CSV y traza16/32 |
| AF020 | 3,29,99 | Las etiquetas no sustituyen los códigos fuente | R | TR-001/002/003, CSV y traza16/32 |
| AF021 | 5,21,25,27,85 | No hay celdas ausentes | R | STAT-002/004/005 |
| AF022 | 5,21,25,27,85 | No hay filas completas duplicadas | R | STAT-002/004/005 |
| AF023 | 5,21,25,27,85 | No hay instant duplicados | R | STAT-002/004/005 |
| AF024 | 5,21,25,27,85 | instant es único en 17379 filas | R | STAT-002/004/005 |
| AF025 | 5,21,25,27,85 | No hay combinaciones fecha-hora repetidas | R | STAT-002/004/005 |
| AF026 | 5,21,25,27,85 | cnt = casual + registered en todas las filas | R | STAT-002/004/005 |
| AF027 | 5,21,25,27,85 | Cero discrepancias de la identidad | R | STAT-002/004/005 |
| AF028 | 5,21,25,27,85 | La identidad se contrastó fila a fila | R | STAT-002/004/005 |
| AF029 | 5,21,25,27,85 | La suma de componentes coincide con el total cnt | R | STAT-002/004/005 |
| AF030 | 5,23,85 | season observado entre 1 y 4 | R | STAT-003 y Readme |
| AF031 | 5,23,85 | yr observado en códigos binarios | R | STAT-003 y Readme |
| AF032 | 5,23,85 | holiday observado en códigos binarios | R | STAT-003 y Readme |
| AF033 | 5,23,85 | workingday observado en códigos binarios | R | STAT-003 y Readme |
| AF034 | 5,23,85 | mnth observado de 1 a 12 | R | STAT-003 y Readme |
| AF035 | 5,23,85 | hr observado de 0 a 23 | R | STAT-003 y Readme |
| AF036 | 5,23,85 | weekday tiene siete categorías | R | STAT-003 y Readme |
| AF037 | 5,23,85 | weathersit observado de 1 a 4 | R | STAT-003 y Readme |
| AF038 | 5,23,85 | No hay códigos fuera de dominio | R | STAT-003 y Readme |
| AF039 | 5,23,85 | Los conteos no son negativos | R | STAT-003 y Readme |
| AF040 | 5,23,85 | Las cuatro variables meteorológicas mantienen el rango normalizado documentado | R | STAT-003 y Readme |
| AF041 | 7,33,35,101 | Total cnt de 3292679 | R | STAT-006/011 |
| AF042 | 7,33,35,101 | Media horaria cnt de 189,46 | R | STAT-006/011 |
| AF043 | 7,33,35,101 | Mediana horaria cnt de 142 | R | STAT-006/011 |
| AF044 | 7,33,35,101 | Máximo horario cnt de 977 | R | STAT-006/011 |
| AF045 | 7,33,35,101 | registered aporta el 81,17 % del total | R | STAT-006/011 |
| AF046 | 7,33,35,101 | casual aporta el 18,83 % del total | R | STAT-006/011 |
| AF047 | 7,33,35,101 | Total casual de 620017 | R | STAT-006/011 |
| AF048 | 7,33,35,101 | Total registered de 2672662 | R | STAT-006/011 |
| AF049 | 7,33,35,101 | Primer cuartil cnt de 40 | R | STAT-006/011 |
| AF050 | 7,33,35,101 | Tercer cuartil cnt de 281 | R | STAT-006/011 |
| AF051 | 7,33,35,101 | Desviación estándar cnt de 181,39 | R | STAT-006/011 |
| AF052 | 7,33,35,101 | La desviación estándar cnt es cercana a su media | R | STAT-006/011 |
| AF053 | 7,33,35,101 | Los cuantiles complementan la media para describir la dispersión | R | STAT-006/011 |
| AF054 | 7,33,35,101 | Media casual de 35,68 | R | STAT-006/011 |
| AF055 | 7,33,35,101 | Mediana casual de 17 | R | STAT-006/011 |
| AF056 | 7,33,35,101 | Media registered de 153,79 | R | STAT-006/011 |
| AF057 | 7,33,35,101 | Mediana registered de 115 | R | STAT-006/011 |
| AF058 | 7,33,35,101 | Los conteos son alquileres, no personas únicas | R | STAT-006/011 |
| AF059 | 7,33,35,101 | registered domina el total agregado | R | STAT-006/011 |
| AF060 | 7,33,35,101 | La demanda muestra alta variabilidad horaria | R | STAT-006/011 |
| AF061 | 9,25,79,93 | 76 fechas sin 24 registros | R | STAT-004, ISSUE-001 y traza |
| AF062 | 9,25,79,93 | 655 fechas con 24 registros | R | STAT-004, ISSUE-001 y traza |
| AF063 | 9,25,79,93 | Mínimo diario de cobertura de un registro | R | STAT-004, ISSUE-001 y traza |
| AF064 | 9,25,79,93 | 165 marcas horarias ausentes en la malla completa | R | STAT-004, ISSUE-001 y traza |
| AF065 | 9,25,79,93 | Todas las fechas del calendario están representadas | R | STAT-004, ISSUE-001 y traza |
| AF066 | 9,25,79,93 | La cobertura intradía es incompleta | R | STAT-004, ISSUE-001 y traza |
| AF067 | 9,25,79,93 | Los totales diarios de fechas incompletas no son estrictamente comparables con días completos | R | STAT-004, ISSUE-001 y traza |
| AF068 | 9,25,79,93 | Los datos no identifican la causa de las horas ausentes | R | STAT-004, ISSUE-001 y traza |
| AF069 | 9,25,79,93 | No se imputaron horas ni conteos ausentes | R | STAT-004, ISSUE-001 y traza |
| AF070 | 9,25,79,93 | Totales diarios y mensuales calculados sobre las horas disponibles | R | STAT-004, ISSUE-001 y traza |
| AF071 | 15,17 | El EDA usa todos los registros disponibles | R | STAT-001 a STAT-014, Readme y código registrado |
| AF072 | 15,17 | No se entrenaron modelos predictivos | R | STAT-001 a STAT-014, Readme y código registrado |
| AF073 | 15,17 | No se realizaron inferencias causales | R | STAT-001 a STAT-014, Readme y código registrado |
| AF074 | 15,17 | casual, registered y cnt son variables de demanda | R | STAT-001 a STAT-014, Readme y código registrado |
| AF075 | 15,17 | Las doce variables enumeradas aportan contexto de calendario o meteorología | R | STAT-001 a STAT-014, Readme y código registrado |
| AF076 | 15,17 | temp se conserva normalizada | R | STAT-001 a STAT-014, Readme y código registrado |
| AF077 | 15,17 | atemp se conserva normalizada | R | STAT-001 a STAT-014, Readme y código registrado |
| AF078 | 15,17 | hum se conserva normalizada | R | STAT-001 a STAT-014, Readme y código registrado |
| AF079 | 15,17 | windspeed se conserva normalizada | R | STAT-001 a STAT-014, Readme y código registrado |
| AF080 | 23,49,83 | Precipitación intensa tiene tres observaciones | R | STAT-007/009 |
| AF081 | 23,49,83 | Condiciones claras o parcialmente nubladas tienen 11413 observaciones | R | STAT-007/009 |
| AF082 | 23,49,83 | Los tamaños meteorológicos están desequilibrados | R | STAT-007/009 |
| AF083 | 23,49,83 | La categoría de tres horas no sostiene comparaciones robustas | R | STAT-007/009 |
| AF084 | 23,49,83 | holiday=1 tiene 500 observaciones | R | STAT-007/009 |
| AF085 | 23,49,83 | holiday=0 tiene 16879 observaciones | R | STAT-007/009 |
| AF086 | 25 | yr es coherente con dteday | R | STAT-004.calendar_component_mismatches |
| AF087 | 25 | mnth es coherente con dteday | R | STAT-004.calendar_component_mismatches |
| AF088 | 25 | weekday es coherente con dteday | R | STAT-004.calendar_component_mismatches |
| AF089 | 37 | Media temp de 0,497 | R | STAT-003/006 |
| AF090 | 37 | Media atemp de 0,476 | R | STAT-003/006 |
| AF091 | 37 | Media hum de 0,627 | R | STAT-003/006 |
| AF092 | 37 | Media windspeed de 0,190 | R | STAT-003/006 |
| AF093 | 37 | Mínimo temp de 0,02 | R | STAT-003/006 |
| AF094 | 37 | Máximo windspeed de 0,8507 | R | STAT-003/006 |
| AF095 | 37 | Las variables meteorológicas observadas están dentro de 0 a 1 | R | STAT-003/006 |
| AF096 | 39 | Media summer de 208,34 | R | STAT-009 contrastado con fuente |
| AF097 | 39 | Media fall de 236,02 | R | STAT-009 contrastado con fuente |
| AF098 | 39 | Media winter de 198,87 | R | STAT-009 contrastado con fuente |
| AF099 | 39 | Media yr=0 de 143,79 | R | STAT-009 contrastado con fuente |
| AF100 | 39 | Media yr=1 de 234,67 | R | STAT-009 contrastado con fuente |
| AF101 | 39 | Las medias difieren descriptivamente entre estaciones | R | STAT-009 contrastado con fuente |
| AF102 | 39 | La media del segundo año supera la del primero | R | STAT-009 contrastado con fuente |
| AF103 | 39 | Media spring de 111,12 | R | STAT-009 conserva 111,115, que el informe redondea a 111,12. Doble redondeo trazable de una estadística válida |
| AF104 | 43 | Media diaria cnt de 4504,35 | R | STAT-010.daily |
| AF105 | 43 | Mediana diaria cnt de 4548 | R | STAT-010.daily |
| AF106 | 43 | Primer cuartil diario de 3152 | R | STAT-010.daily |
| AF107 | 43 | Tercer cuartil diario de 5956 | R | STAT-010.daily |
| AF108 | 43 | Máximo diario de 8714 | R | STAT-010.daily |
| AF109 | 43 | Fecha del máximo diario 2012-09-15 | R | STAT-010.daily |
| AF110 | 43 | Mínimo diario de 22 | R | STAT-010.daily |
| AF111 | 43 | Fecha del mínimo diario 2012-10-29 | R | STAT-010.daily |
| AF112 | 43 | El mínimo diario se debe contextualizar con cobertura horaria incompleta | R | STAT-010.daily |
| AF113 | 45,61 | El perfil horario cambia entre workingday=0 y workingday=1 | R | STAT-008 y FIG-002 |
| AF114 | 45,61 | Media laboral a las 08:00 de 477,01 | R | STAT-008 y FIG-002 |
| AF115 | 45,61 | Media laboral a las 17:00 de 525,29 | R | STAT-008 y FIG-002 |
| AF116 | 45,61 | El máximo laboral es a las 17:00 | R | STAT-008 y FIG-002 |
| AF117 | 45,61 | El máximo no laboral es a las 13:00 | R | STAT-008 y FIG-002 |
| AF118 | 45,61 | Media no laboral a las 13:00 de 372,73 | R | STAT-008 y FIG-002 |
| AF119 | 45,61 | El perfil laboral tiene picos de mañana y tarde | R | STAT-008 y FIG-002 |
| AF120 | 45,61 | El perfil no laboral alcanza sus niveles más altos al mediodía y primeras horas de la tarde | R | STAT-008 y FIG-002 |
| AF121 | 47 | registered representa el 86,77 % en workingday=1 | R | STAT-011.by_workingday |
| AF122 | 47 | registered representa el 68,34 % en workingday=0 | R | STAT-011.by_workingday |
| AF123 | 47 | La composición difiere entre segmentos de calendario | R | STAT-011.by_workingday |
| AF124 | 47 | casual representa el 31,67 % en workingday=0 | R | STAT-011 conserva 0,31665, mostrado como 31,67 %. Doble redondeo trazable |
| AF125 | 49,65 | Media meteorológica despejada de 204,87 | R | STAT-009.by_weather y FIG-003 |
| AF126 | 49,65 | Media meteorológica niebla/nublado de 175,17 | R | STAT-009.by_weather y FIG-003 |
| AF127 | 49,65 | Media con precipitación ligera de 111,58 | R | STAT-009.by_weather y FIG-003 |
| AF128 | 49,65 | Media con precipitación intensa de 74,33 | R | STAT-009.by_weather y FIG-003 |
| AF129 | 49,65 | Las medias descienden entre categorías meteorológicas de peor condición | R | STAT-009.by_weather y FIG-003 |
| AF130 | 49,65 | La comparación meteorológica no ajusta por hora, estación o calendario | R | STAT-009.by_weather y FIG-003 |
| AF131 | 51,91 | Spearman cnt-temp de 0,4233 | R | STAT-012 y código de correlación |
| AF132 | 51,91 | Spearman cnt-atemp de 0,4233 | R | STAT-012 y código de correlación |
| AF133 | 51,91 | Spearman cnt-hum de -0,3596 | R | STAT-012 y código de correlación |
| AF134 | 51,91 | Spearman cnt-windspeed de 0,1266 | R | STAT-012 y código de correlación |
| AF135 | 51,91 | Las asociaciones son bivariadas y descriptivas | R | STAT-012 y código de correlación |
| AF136 | 51,91 | Las asociaciones no ajustan por hora | R | STAT-012 y código de correlación |
| AF137 | 51,91 | Las asociaciones no ajustan por calendario | R | STAT-012 y código de correlación |
| AF138 | 51,91 | Las asociaciones no ajustan por estación | R | STAT-012 y código de correlación |
| AF139 | 51,91 | Spearman temp-atemp de 0,9896 | R | STAT-012 y código de correlación |
| AF140 | 51,91 | temp y atemp tienen fuerte redundancia descriptiva | R | STAT-012 y código de correlación |
| AF141 | 53 | Se calcularon diez grupos qcut de frecuencia aproximadamente igual | R | STAT-014 comprobado independientemente |
| AF142 | 53 | Media del primer grupo qcut de 70,00 | R | STAT-014 comprobado independientemente |
| AF143 | 53 | Extremo inferior efectivo fuente del primer grupo qcut de 0,02 | R | STAT-014 comprobado independientemente |
| AF144 | 53 | Extremo superior del primer grupo qcut de 0,24 | R | STAT-014 comprobado independientemente |
| AF145 | 53 | Media del último grupo qcut de 333,22 | R | STAT-014 comprobado independientemente |
| AF146 | 53 | Extremo inferior del último grupo qcut de 0,74 | R | STAT-014 comprobado independientemente |
| AF147 | 53 | Extremo superior del último grupo qcut de 1,00 | R | STAT-014 comprobado independientemente |
| AF148 | 53 | Tamaño mínimo de grupo qcut de 1501 horas | R | STAT-014 comprobado independientemente |
| AF149 | 53 | Tamaño máximo de grupo qcut de 2013 horas | R | STAT-014 comprobado independientemente |
| AF150 | 53 | Límites, tamaños y medias de qcut están documentados reproduciblemente | R | STAT-014 comprobado independientemente |
| AF151 | 53 | La agrupación qcut no ajusta por otras variables | R | STAT-014 comprobado independientemente |
| AF152 | 57,69 | FIG-001 muestra variación de totales diarios durante los dos años | R | FIG-001/004, STAT-010 y código registrado |
| AF153 | 57,69 | FIG-001 permite localizar días con totales particularmente bajos o altos | R | FIG-001/004, STAT-010 y código registrado |
| AF154 | 57,69 | FIG-004 representa simultáneamente volumen mensual y composición por tipo de usuario | R | FIG-001/004, STAT-010 y código registrado |
| AF155 | 57,69 | registered domina el volumen de cada mes | R | FIG-001/004, STAT-010 y código registrado |
| AF156 | 57,69 | casual aporta una fracción generalmente mayor en meses de mayor actividad | R | FIG-001/004, STAT-010 y código registrado |
| AF157 | 73 | FIG-005 representa diez intervalos construidos con qcut | C | FIG-005 y traza16/88: PNG calculado con cut, no qcut. STAT-014 describe otra partición y la corrección no contiene savefig. |
| AF158 | 73 | Los límites efectivos de FIG-005 están conservados en STAT-014 | C | FIG-005 y traza16/88: PNG calculado con cut, no qcut. STAT-014 describe otra partición y la corrección no contiene savefig. |
| AF159 | 73 | Los tamaños de grupo de FIG-005 están conservados en STAT-014 | C | FIG-005 y traza16/88: PNG calculado con cut, no qcut. STAT-014 describe otra partición y la corrección no contiene savefig. |
| AF160 | 73 | Las medias de cnt de FIG-005 están conservadas en STAT-014 | C | FIG-005 y traza16/88: PNG calculado con cut, no qcut. STAT-014 describe otra partición y la corrección no contiene savefig. |
| AF161 | 73 | FIG-005 representa medias agregadas no ajustadas | R | Traza16: medias bivariadas sin ajuste de otras variables |
| AF162 | 81,95 | Cribado mediante 1,5 veces IQR | R | STAT-013, ISSUE-002 y CSV contrastado |
| AF163 | 81,95 | Límite superior IQR de 642,5 | R | STAT-013, ISSUE-002 y CSV contrastado |
| AF164 | 81,95 | 505 horas señaladas por IQR | R | STAT-013, ISSUE-002 y CSV contrastado |
| AF165 | 81,95 | Proporción señalada de 2,91 % | R | STAT-013, ISSUE-002 y CSV contrastado |
| AF166 | 81,95 | El máximo cnt corresponde a instant=14774 | R | STAT-013, ISSUE-002 y CSV contrastado |
| AF167 | 81,95 | La fecha del máximo cnt es 2012-09-12 | R | STAT-013, ISSUE-002 y CSV contrastado |
| AF168 | 81,95 | La hora del máximo cnt es 18 | R | STAT-013, ISSUE-002 y CSV contrastado |
| AF169 | 81,95 | Los extremos se clasificaron como estadísticos, no como errores | R | STAT-013, ISSUE-002 y CSV contrastado |
| AF170 | 81,95 | Los extremos conservan los rangos y la identidad de conteos | R | STAT-013, ISSUE-002 y CSV contrastado |
| AF171 | 81,95 | Todos los extremos se conservaron | R | STAT-013, ISSUE-002 y CSV contrastado |
| AF172 | 81,95 | Los extremos pueden influir en medias y correlaciones | R | STAT-013, ISSUE-002 y CSV contrastado |
| AF173 | 89 | La tabla no contiene estaciones de origen o destino | R | Esquema fuente, Readme y unidad agregada |
| AF174 | 89 | La tabla no contiene trayectos | R | Esquema fuente, Readme y unidad agregada |
| AF175 | 89 | La tabla no contiene duración | R | Esquema fuente, Readme y unidad agregada |
| AF176 | 89 | La tabla no contiene disponibilidad de bicicletas | R | Esquema fuente, Readme y unidad agregada |
| AF177 | 89 | La tabla no contiene capacidad | R | Esquema fuente, Readme y unidad agregada |
| AF178 | 89 | La tabla no contiene usuarios únicos | R | Esquema fuente, Readme y unidad agregada |
| AF179 | 89 | La tabla no contiene detalles operativos individuales | R | Esquema fuente, Readme y unidad agregada |
| AF180 | 89 | Los datos agregados no describen mecanismos individuales con precisión | R | Esquema fuente, Readme y unidad agregada |
| AF181 | 91,101 | Hora, estación y año se observan conjuntamente con la meteorología | R | STAT-009/010/012/014 y diseño observacional |
| AF182 | 91,101 | Las relaciones no identifican efectos causales | R | STAT-009/010/012/014 y diseño observacional |
| AF183 | 91,101 | Los datos no aíslan el efecto de factores no observados | R | STAT-009/010/012/014 y diseño observacional |
| AF184 | 91,101 | Las medias de los grupos qcut progresan de menor a mayor | R | STAT-009/010/012/014 y diseño observacional |
