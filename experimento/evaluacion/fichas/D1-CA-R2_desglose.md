# Evaluación D1-CA-R2

**Índice final:** 87,69/100.  
**Evaluación cerrada:** 6 de octubre de 2026.  
**Ejecución:** `D1_bike_sharing__crewai__r02__20260831T175303870628Z`

**Criterios:** [Protocolo de evaluación](../01_protocolo_calidad_Q1_Q10_v0.1.md) y [guía D1](../02_ficha_D1_bike_sharing.md).  
**Resultados:** [Archivos originales de la ejecución](../../../outputs/experimento/D1_bike_sharing__crewai__r02__20260831T175303870628Z).  
**Evaluación:** [Excel de puntuaciones](../Evaluacion_calidad.xlsx) y [JSON de comprobaciones](D1-CA-R2_comprobaciones.json).

Las referencias `STAT`, `ISSUE` y `FIG` identifican análisis, problemas y figuras en los archivos de la ejecución. `TR` identifica transformaciones y `CHK`, comprobaciones de calidad. Las referencias a líneas corresponden al informe original, `report.md`.

## Resumen

| Métrica | Puntuación final |
| --- | ---: |
| Q1 Cumplimiento de las etapas | 93,75 |
| Q2 Corrección numérica | 88,57 |
| Q3 Validez del tratamiento de los datos | 87,50 |
| Q4 Detección de problemas y riesgos | 92,31 |
| Q5 Calidad y profundidad del EDA | 75,00 |
| Q6 Profundidad de la interpretación | 75,00 |
| Q7 Calidad de las visualizaciones | 95,00 |
| Q8 Cobertura del informe | 88,64 |
| Q9 Fidelidad del informe | 99,34 |
| Q10 Claridad y coherencia | 75,00 |

La ejecución terminó como `completed` después de la corrección solicitada por el Revisor. Esta corrección añadió las estadísticas necesarias para respaldar la serie diaria y los promedios de alquileres por grupos de temperatura. La columna `timestamp` de la copia preparada, que había perdido la hora al guardarse, no se corrigió.

## Q1 Cumplimiento de las etapas: 93,75

| Etapa | Puntos | Evidencia |
| --- | ---: | --- |
| E1 Carga e inspección inicial | 1 | profile y STAT-001 |
| E2 Estructura, tipos y calidad | 1 | STAT-002/003/004 y CHK-001/002/003/004 |
| E3 Preparación y decisiones de análisis | 0,5 | TR-001/002/003 y `prepared_data.csv`, con la columna timestamp guardada sin hora |
| E4 Estadística descriptiva | 1 | STAT-006/007 |
| E5 Variables, agregaciones y relaciones | 1 | STAT-008/009/011/012 |
| E6 Visualizaciones | 1 | FIG-001 a FIG-004 |
| E7 Problemas, riesgos y anomalías | 1 | ISSUE-001/002 y STAT-010 |
| E8 Informe final | 1 | report completo |

`Q1 = 100 x 7,5 / 8 = 93,75`

## Q2 Corrección numérica: 88,57

Se obtienen resultados correctos en 23 de las 26 comprobaciones, que suman 31 de los 35 puntos posibles. No se calcula el crecimiento porcentual entre 2011 y 2012 ni las dos correlaciones de Pearson previstas.

| Comprobación | Resultado | Referencia | Estado | Peso acreditado | Evidencia o ausencia |
| --- | --- | --- | --- | ---: | --- |
| C01 Número de filas | 17379 | 17379 | correcta | 2/2 | STAT-001.rows |
| C02 Número de columnas | 17 | 17 | correcta | 2/2 | STAT-001.columns |
| C03 Fechas distintas | 731 | 731 | correcta | 1/1 | STAT-001.distinct_dates |
| C04 Celdas ausentes | 0 | 0 | correcta | 2/2 | STAT-002.missing_by_column |
| C05 Filas duplicadas | 0 | 0 | correcta | 2/2 | STAT-002.full_row_duplicates |
| C06 Huecos en la secuencia horaria | 165 | 165 | correcta | 1/1 | STAT-004.missing_hourly_slots |
| C07 Alquileres totales | 3292679 | 3292679 | correcta | 2/2 | STAT-008.overall.total_cnt |
| C08 Media horaria de alquileres | 189,463088 | 189,463088 | correcta | 2/2 | STAT-006.cnt.mean |
| C09 Mediana horaria de alquileres | 142 | 142 | correcta | 1/1 | STAT-006.cnt.median |
| C10 Desviación típica muestral | 181,387599 | 181,387599 | correcta | 1/1 | STAT-006.cnt.std |
| C11 Máximo horario | 977 | 977 | correcta | 1/1 | STAT-006.cnt.max |
| C12 Alquileres de usuarios ocasionales | 620017 | 620017 | correcta | 1/1 | STAT-008.overall.total_casual |
| C13 Alquileres de usuarios registrados | 2672662 | 2672662 | correcta | 1/1 | STAT-008.overall.total_registered |
| C14 Proporción de alquileres de usuarios registrados | 0,811698 | 0,811698 | correcta | 1/1 | STAT-008.overall.registered_share |
| C15 Alquileres totales en 2011 | 1243103 | 1243103 | correcta | 1/1 | STAT-007.by_year[yr=0].cnt |
| C16 Alquileres totales en 2012 | 2049576 | 2049576 | correcta | 1/1 | STAT-007.by_year[yr=1].cnt |
| C17 Variación total de 2012 respecto a 2011 | No producido | 64,875799 | ausente | 0/2 | Los totales anuales no sustituyen su variación porcentual. |
| C18 Hora con mayor media | Categoría 17, 461,452055 | 461,452055 | correcta | 2/2 | STAT-007.by_hour[hr=17].mean |
| C19 Hora con menor media | Categoría 4, 6,352941 | 6,352941 | correcta | 1/1 | STAT-007.by_hour[hr=4].mean |
| C20 Temporada con mayor media | Categoría 3, 236,016237 | 236,016237 | correcta | 1/1 | STAT-007.by_season[season=3].mean |
| C21 Media con tiempo despejado | Categoría 1, 204,869272 | 204,869272 | correcta | 1/1 | STAT-008.by_weathersit[weathersit=1].mean_cnt |
| C22 Media con tiempo adverso de categoría 3 | Categoría 3, 111,579281 | 111,579281 | correcta | 1/1 | STAT-008.by_weathersit[weathersit=3].mean_cnt |
| C23 Observaciones meteorológicas de categoría 4 | 3 | 3 | correcta | 1/1 | STAT-008.by_weathersit[weathersit=4].n_hours |
| C24 Correlación de Pearson entre temperatura y cnt | No producido | 0,404772 | ausente | 0/1 | Se produce Spearman, no Pearson. |
| C25 Correlación de Pearson entre humedad y cnt | No producido | -0,322911 | ausente | 0/1 | Se produce Spearman, no Pearson. |
| C26 Inconsistencias en cnt = casual + registered | 0 | 0 | correcta | 2/2 | STAT-003.cnt_identity_mismatches |

`Q2 = 100 x 31 / 35 = 88,57`

## Q3 Validez del tratamiento de los datos: 87,50

| Decisión | Puntos | Evidencia |
| --- | ---: | --- |
| D01 Fecha-hora válida | 0 | CSV y evento 15, timestamp sin hora |
| D02 Códigos como categorías | 1 | STAT-003/007/008/009, dominios y agrupaciones |
| D03 uso de `instant` como identificador | 1 | plan 216, STAT-003 y localizadores en STAT-010 |
| D04 Sin limpieza innecesaria | 1 | STAT-002, TR-003 y contraste de 17 columnas |
| D05 No imputar huecos | 1 | STAT-004 e ISSUE-001 |
| D06 Conservar extremos válidos | 1 | STAT-010 e ISSUE-002 |
| D07 Conservar y explicar que `cnt = casual + registered` | 1 | STAT-003, report 59 |
| D08 Preservar escalas normalizadas | 1 | STAT-003/006, report 43 y 91 |

`Q3 = 100 x 7 / 8 = 87,50`

## Q4 Detección de problemas y riesgos: 92,31

Identifica seis de los siete riesgos previstos y tres adicionales, sin falsas alarmas. R07 queda parcial: comprueba relaciones del calendario, pero no desarrolla la dependencia entre observaciones temporales.

| Riesgo | Clasificación | Evidencia |
| --- | --- | --- |
| R01 Identificador secuencial | Completo | plan 216, STAT-003 y uso de instant solo como localizador |
| R02 Códigos categóricos/binarios | Completo | STAT-003 y agrupaciones STAT-007/008/009 |
| R03 Identidad de componentes | Completo | STAT-003 y report 59, el total es la suma de ambos tipos de alquileres |
| R04 Normalización | Completo | STAT-003/006 y report 91 |
| R05 Huecos horarios | Completo | STAT-004, ISSUE-001 y report 81 |
| R06 Meteorología 4, n = 3 | Completo | STAT-008 y report 55/93 |
| R07 Dependencia y redundancia temporal | Parcial | plan 117/130 y STAT-003 verifican calendario. No desarrollan dependencia entre horas sucesivas |
| A01 Redundancia temp-atemp | Adicional válido | STAT-009 y report 59 |
| A02 Sensibilidad a extremos altos | Adicional válido | ISSUE-002, STAT-010 y comparación media-mediana |
| A03 Agregación horaria sin información individual | Adicional válido | profile y report 89 |

K = 6, A = 3 y F = 0. Precisión = 1 y cobertura = 6/7. F1 = 12/13.

`Q4 = 100 x [2 x 1 x (6 / 7)] / [1 + (6 / 7)] = 92,31`

## Q5 Calidad y profundidad del EDA: 75,00

El análisis examina distribuciones, calendario, perfiles horarios, meteorología y extremos, y reconoce las limitaciones de cobertura. Recibe 3 de 4 puntos por el error en la marca temporal guardada y el tratamiento incompleto de la dependencia entre observaciones temporales.


**Evidencia:** STAT-006 a STAT-012, cuatro PNG, report 39–59, 81–94 y CSV.

`Q5 = 100 x 3 / 4 = 75,00`

## Q6 Profundidad de la interpretación: 75,00

La interpretación relaciona los hallazgos con los tamaños de los grupos, la cobertura y las limitaciones para establecer relaciones causales. Recibe 3 de 4 puntos porque describe la columna temporal guardada como una combinación de fecha y hora, aunque el CSV conserva únicamente la fecha.


**Evidencia:** Report 33, 35, 53–59, 65–77, 89–98. CSV y código del evento 15.

`Q6 = 100 x 3 / 4 = 75,00`

## Q7 Calidad de las visualizaciones: 95,00

| Objetivo | Nota 0–4 | Evidencia y criterio |
| --- | ---: | --- |
| V01 Evolución de 2011 y 2012 | 4 | FIG-001, suma diaria de 731 fechas, eje temporal legible y cobertura explicada. STAT-011 y report 65 |
| V02 Perfil horario por tipo de día | 4 | FIG-002, 24 horas y dos curvas contrastadas. STAT-009 y report 69 |
| V03 Patrón mensual o estacional | 3 | FIG-001 permite apreciar ciclos estacionales en ambos años, con meses ordenados en el eje. El texto de la figura no integra explícitamente ese patrón. Report 45 sí describe medias por mes y season |
| V04 Meteorología y grupo pequeño | 4 | FIG-003, medias correctas y advertencia n = 3 en report 73. STAT-008 |
| V05 Relación entre temperatura y alquileres | 4 | FIG-004, puntos semitransparentes y guía por deciles. STAT-009/012 y report 77 |

`Q7 = 100 x 19 / 20 = 95,00`

## Q8 Cobertura del informe: 88,64

El informe cubre plenamente nueve unidades y parcialmente tres. Falta cuantificar el crecimiento anual, identificar expresamente las 4 h como mínimo global y explicar la dependencia temporal. Peso acreditado 19,5 de 22.

| Unidad | Puntos relativos | Peso | Evidencia o carencia |
| --- | ---: | ---: | --- |
| U01 | 1 | 2 | Report 3, 13, 27, estructura y periodo |
| U02 | 1 | 2 | Report 29/33, sin nulos ni duplicados, con huecos |
| U03 | 1 | 2 | Report 39, nivel, cuartiles y heterogeneidad |
| U04 | 1 | 2 | Report 41, cuota global 81,2 % |
| U05 | 0,5 | 2 | Report 47, totales de ambos años, sin variación porcentual |
| U06 | 0,5 | 2 | Report 51, máximo 17 h y valor 4 h, sin identificarlo como mínimo |
| U07 | 1 | 2 | FIG-002 y report 53/69, máximos visibles 17/13 h |
| U08 | 1 | 1 | Report 45, estaciones y meses |
| U09 | 1 | 2 | Report 55/73, medias y n = 3 |
| U10 | 1 | 2 | Report 57, temperatura/humedad y cautela |
| U11 | 1 | 2 | Report 59, relación mecánica |
| U12 | 0,5 | 1 | Report 3/89/92, ciudad y límites causales. No explica dependencia temporal |

`Q8 = 100 x 19,5 / 22 = 88,64`

## Q9 Fidelidad del informe: 99,34

De las 152 afirmaciones evaluadas, 151 tienen respaldo. La afirmación AF092, que describe la columna timestamp de la copia preparada como una combinación de fecha y hora, contradice el contenido del CSV. Este error de guardado no invalida los cálculos realizados previamente con la marca temporal correcta en memoria.

El inventario situado al final de esta ficha recoge las afirmaciones revisadas, su clasificación y las evidencias utilizadas.

`Q9 = 100 x 151 / 152 = 99,34`

## Q10 Claridad y coherencia: 75,00

El informe está organizado y conecta los hallazgos con las figuras y las limitaciones. Recibe 3 de 4 puntos por la contradicción sobre timestamp, algunas repeticiones y nombres de variables que no se explican suficientemente.


**Evidencia:** Report completo, especialmente 35 y 98, y contraste de prepared_data.csv.

`Q10 = 100 x 3 / 4 = 75,00`

## Inventario de afirmaciones

R = respaldada; C = contradicha; S = sin respaldo suficiente.

| ID | Líneas | Afirmación | Estado | Evidencia |
| --- | --- | --- | --- | --- |
| AF001 | 3, 13 | 17379 observaciones | R | profile y STAT-001, Readme.txt |
| AF002 | 3, 13 | Observaciones agregadas por hora | R | profile y STAT-001, Readme.txt |
| AF003 | 3, 13 | Datos de Capital Bikeshare | R | profile y STAT-001, Readme.txt |
| AF004 | 3, 13 | Periodo 2011-01-01 a 2012-12-31 | R | profile y STAT-001, Readme.txt |
| AF005 | 3, 13 | 17 columnas originales | R | profile y STAT-001, Readme.txt |
| AF006 | 3, 13 | Calendario, meteorología normalizada y recuentos en la tabla | R | profile y STAT-001, Readme.txt |
| AF007 | 5, 29, 85, 98 | Sin celdas ausentes en las 17 columnas fuente | R | STAT-002/003, entrada y contraste |
| AF008 | 5, 29, 85, 98 | Sin filas completas duplicadas en entrada | R | STAT-002/003, entrada y contraste |
| AF009 | 5, 29, 85, 98 | instant sin duplicados | R | STAT-002/003, entrada y contraste |
| AF010 | 5, 29, 85, 98 | Clave dteday + hr sin duplicados en entrada y cálculo en memoria | R | STAT-002/003, entrada y contraste |
| AF011 | 5, 29, 85, 98 | Identidad cnt = casual + registered en todas las filas | R | STAT-002/003, entrada y contraste |
| AF012 | 5, 33, 81, 90, 102 | 165 huecos horarios | R | STAT-004/011, ISSUE-001 |
| AF013 | 5, 33, 81, 90, 102 | 17544 posiciones horarias esperadas | R | STAT-004/011, ISSUE-001 |
| AF014 | 5, 33, 81, 90, 102 | 76 fechas con menos de 24 registros | R | STAT-004/011, ISSUE-001 |
| AF015 | 5, 33, 81, 90, 102 | Las sumas temporales reflejan registros disponibles, no necesariamente calendarios completos | R | STAT-004/011, ISSUE-001 |
| AF016 | 5, 33, 81, 90, 102 | Cobertura desigual puede reducir totales en periodos incompletos | R | STAT-004/011, ISSUE-001 |
| AF017 | 7, 39 | Media cnt 189,5 | R | STAT-006.cnt |
| AF018 | 7, 39 | Mediana cnt 142 | R | STAT-006.cnt |
| AF019 | 7, 39 | Q1 cnt 40 | R | STAT-006.cnt |
| AF020 | 7, 39 | Q3 cnt 281 | R | STAT-006.cnt |
| AF021 | 7, 39 | Máximo cnt 977 | R | STAT-006.cnt |
| AF022 | 7, 39 | Mínimo cnt 1 | R | STAT-006.cnt |
| AF023 | 7, 39 | Recuentos horarios con alta heterogeneidad | R | STAT-006.cnt |
| AF024 | 7, 41, 100 | Total cnt 3292679 | R | STAT-006/008 |
| AF025 | 7, 41, 100 | Total registrados 2672662 | R | STAT-006/008 |
| AF026 | 7, 41, 100 | Total ocasionales 620017 | R | STAT-006/008 |
| AF027 | 7, 41, 100 | Cuota registrados 81,2 % | R | STAT-006/008 |
| AF028 | 7, 41, 100 | Cuota ocasionales 18,8 % | R | STAT-006/008 |
| AF029 | 7, 41, 100 | Predominio de registrados | R | STAT-006/008 |
| AF030 | 7, 41, 100 | Media registrados 153,8 | R | STAT-006/008 |
| AF031 | 7, 41, 100 | Media ocasionales 35,7 | R | STAT-006/008 |
| AF032 | 9, 51 | Máxima media global a las 17 h | R | STAT-007.by_hour |
| AF033 | 9, 51 | Media global a las 17 h 461,5 | R | STAT-007.by_hour |
| AF034 | 9, 51 | Media global a las 4 h 6,4 | R | STAT-007.by_hour |
| AF035 | 9, 51 | Media global a las 8 h 359,0 | R | STAT-007.by_hour |
| AF036 | 9, 51 | Media global a las 18 h 425,5 | R | STAT-007.by_hour |
| AF037 | 9, 51 | Demanda global crece de madrugada hacia la mañana | R | STAT-007.by_hour |
| AF038 | 9, 53, 69, 100 | Media laborables a las 8 h 477,0 | R | STAT-009.hourly_workingday_profile y FIG-002 |
| AF039 | 9, 53, 69, 100 | Media laborables a las 17 h 525,3 | R | STAT-009.hourly_workingday_profile y FIG-002 |
| AF040 | 9, 53, 69, 100 | Perfil no laborable elevado en las horas centrales | R | STAT-009.hourly_workingday_profile y FIG-002 |
| AF041 | 9, 53, 69, 100 | Media no laborables a las 13 h 372,7 | R | STAT-009.hourly_workingday_profile y FIG-002 |
| AF042 | 9, 53, 69, 100 | Media no laborables a las 14 h 364,6 | R | STAT-009.hourly_workingday_profile y FIG-002 |
| AF043 | 9, 53, 69, 100 | Perfil horario diferente según tipo de día | R | STAT-009.hourly_workingday_profile y FIG-002 |
| AF044 | 9, 53, 69, 100 | Picos matutino y vespertino más concentrados en laborables | R | STAT-009.hourly_workingday_profile y FIG-002 |
| AF045 | 9, 53, 69, 100 | El perfil no identifica el motivo individual de viaje | R | STAT-009.hourly_workingday_profile y FIG-002 |
| AF046 | 9, 55, 73 | Media meteorología 1 204,9 | R | STAT-008.by_weathersit y FIG-003 |
| AF047 | 9, 55, 73 | Media meteorología 2 175,2 | R | STAT-008.by_weathersit y FIG-003 |
| AF048 | 9, 55, 73 | Media meteorología 3 111,6 | R | STAT-008.by_weathersit y FIG-003 |
| AF049 | 9, 55, 73 | Media meteorología 4 74,3 | R | STAT-008.by_weathersit y FIG-003 |
| AF050 | 9, 55, 73 | Descenso de la media entre los códigos meteorológicos 1 a 4 | R | STAT-008.by_weathersit y FIG-003 |
| AF051 | 9, 55, 73 | Meteorología 1 con 11413 observaciones | R | STAT-008.by_weathersit y FIG-003 |
| AF052 | 9, 55, 73 | Meteorología 4 con 3 observaciones | R | STAT-008.by_weathersit y FIG-003 |
| AF053 | 9, 55, 73 | Promedio de categoría 4 con soporte muestral muy limitado | R | STAT-008.by_weathersit y FIG-003 |
| AF054 | 9, 23, 57, 77, 92, 100 | Las comparaciones bivariadas no identifican efectos causales aislados | R | Métodos STAT-007/008/009/012 y ausencia de análisis causal en la traza |
| AF055 | 9, 23, 57, 77, 92, 100 | EDA descriptivo, sin modelado predictivo | R | Métodos STAT-007/008/009/012 y ausencia de análisis causal en la traza |
| AF056 | 9, 23, 57, 77, 92, 100 | Hora, estación, año y meteorología pueden variar conjuntamente | R | Métodos STAT-007/008/009/012 y ausencia de análisis causal en la traza |
| AF057 | 17–21 | cnt es el recuento total horario | R | Readme.txt y profile, selección de variables STAT |
| AF058 | 17–21 | casual y registered son componentes por tipo de usuario | R | Readme.txt y profile, selección de variables STAT |
| AF059 | 17–21 | dteday, yr, mnth, hr, weekday, holiday y workingday describen calendario | R | Readme.txt y profile, selección de variables STAT |
| AF060 | 17–21 | season es categórica | R | Readme.txt y profile, selección de variables STAT |
| AF061 | 17–21 | weathersit es categórica | R | Readme.txt y profile, selección de variables STAT |
| AF062 | 17–21 | temp, atemp, hum y windspeed son variables meteorológicas normalizadas | R | Readme.txt y profile, selección de variables STAT |
| AF063 | 27 | 731 fechas distintas | R | STAT-001/003 |
| AF064 | 27 | Inicio de clave temporal en memoria 2011-01-01 00 h | R | STAT-001/003 |
| AF065 | 27 | Final de clave temporal en memoria 2012-12-31 23 h | R | STAT-001/003 |
| AF066 | 27 | hr tiene 24 categorías | R | STAT-001/003 |
| AF067 | 27 | mnth tiene 12 categorías | R | STAT-001/003 |
| AF068 | 27 | season tiene 4 categorías | R | STAT-001/003 |
| AF069 | 27 | weathersit tiene 4 categorías | R | STAT-001/003 |
| AF070 | 27 | yr es binaria | R | STAT-001/003 |
| AF071 | 27 | holiday es binaria | R | STAT-001/003 |
| AF072 | 27 | workingday es binaria | R | STAT-001/003 |
| AF073 | 29 | mnth coincide con el mes de dteday | R | STAT-003 y contraste de calendario |
| AF074 | 29 | yr coincide con el año codificado de dteday | R | STAT-003 y contraste de calendario |
| AF075 | 29 | weekday usa domingo 0 y sábado 6 | R | STAT-003 y contraste de calendario |
| AF076 | 29 | workingday distingue días que no son festivos ni fin de semana | R | STAT-003 y contraste de calendario |
| AF077 | 31, 85 | Recuentos sin negativos | R | STAT-003.range_summary y controles |
| AF078 | 31, 85 | temp está en el rango 0–1 | R | STAT-003.range_summary y controles |
| AF079 | 31, 85 | atemp está en el rango 0–1 | R | STAT-003.range_summary y controles |
| AF080 | 31, 85 | hum está en el rango 0–1 | R | STAT-003.range_summary y controles |
| AF081 | 31, 85 | windspeed máximo aproximadamente 0,8507 | R | STAT-003.range_summary y controles |
| AF082 | 31, 85 | Sin categorías fuera de los dominios documentados | R | STAT-003.range_summary y controles |
| AF083 | 31, 85 | No hay incompatibilidades de tipos en las columnas fuente | R | STAT-003.range_summary y controles |
| AF084 | 33 | El 2011-01-18 tiene 12 registros | R | STAT-004.incomplete_date_examples |
| AF085 | 33, 35, 81, 98 | No se imputaron huecos horarios | R | TR-001/003, CSV y operación del evento 15 |
| AF086 | 33, 35, 81, 98 | No se eliminaron filas | R | TR-001/003, CSV y operación del evento 15 |
| AF087 | 33, 35, 81, 98 | Copia preparada separada de la entrada | R | TR-001/003, CSV y operación del evento 15 |
| AF088 | 33, 35, 81, 98 | dteday se interpretó como fecha y se serializó como fecha ISO | R | TR-001/003, CSV y operación del evento 15 |
| AF089 | 33, 35, 81, 98 | Copia preparada con 17379 filas | R | TR-001/003, CSV y operación del evento 15 |
| AF090 | 33, 35, 81, 98 | Conservación de las 17 columnas fuente | R | TR-001/003, CSV y operación del evento 15 |
| AF091 | 33, 35, 81, 98 | Copia preparada con 18 columnas | R | TR-001/003, CSV y operación del evento 15 |
| AF092 | 35, 98 | La copia preparada añade una marca que combina fecha y hora para reproducir la cobertura | C | prepared_data.csv y traza evento 15, date_format='%Y-%m-%d' |
| AF093 | 43, 91 | Media temp 0,497 | R | STAT-006 y alcance de informe |
| AF094 | 43, 91 | Media atemp 0,476 | R | STAT-006 y alcance de informe |
| AF095 | 43, 91 | Media hum 0,627 | R | STAT-006 y alcance de informe |
| AF096 | 43, 91 | Media windspeed 0,190 | R | STAT-006 y alcance de informe |
| AF097 | 43, 91 | No se convierten las variables normalizadas a unidades físicas | R | STAT-006 y alcance de informe |
| AF098 | 45 | Temporada 1 con menor media | R | STAT-007.by_season |
| AF099 | 45 | Media temporada 1 111,1 | R | STAT-007.by_season |
| AF100 | 45 | Temporada 3 con mayor media | R | STAT-007.by_season |
| AF101 | 45 | Media temporada 3 236,0 | R | STAT-007.by_season |
| AF102 | 45 | Media temporada 2 208,3 | R | STAT-007.by_season |
| AF103 | 45 | Media temporada 4 198,9 | R | STAT-007.by_season |
| AF104 | 45 | Media de enero 94,4 | R | STAT-007.by_month |
| AF105 | 45 | Media de junio cercana a 240 | R | STAT-007.by_month |
| AF106 | 45 | Media de septiembre cercana a 240 | R | STAT-007.by_month |
| AF107 | 45 | Media de diciembre 142,3 | R | STAT-007.by_month |
| AF108 | 45 | Patrón mensual con demanda más alta en meses intermedios que al principio y final | R | STAT-007.by_month |
| AF109 | 47 | Total 2011 1243103 | R | STAT-007.by_year |
| AF110 | 47 | Total 2012 2049576 | R | STAT-007.by_year |
| AF111 | 47 | Cuota casual 2011 19,9 % | R | STAT-007.by_year |
| AF112 | 47 | Cuota casual 2012 18,2 % | R | STAT-007.by_year |
| AF113 | 47 | La cuota casual baja entre 2011 y 2012 | R | STAT-007.by_year |
| AF114 | 57 | Spearman cnt-temp 0,423 | R | STAT-009.spearman_correlation/temp_quintiles |
| AF115 | 57 | Asociación cnt-temp positiva moderada | R | STAT-009.spearman_correlation/temp_quintiles |
| AF116 | 57 | Spearman cnt-hum −0,360 | R | STAT-009.spearman_correlation/temp_quintiles |
| AF117 | 57 | Asociación cnt-hum negativa | R | STAT-009.spearman_correlation/temp_quintiles |
| AF118 | 57 | Spearman cnt-windspeed 0,127 | R | STAT-009.spearman_correlation/temp_quintiles |
| AF119 | 57 | Asociación cnt-windspeed positiva débil | R | STAT-009.spearman_correlation/temp_quintiles |
| AF120 | 57 | Media cnt quintil inferior temp 84,4 | R | STAT-009.spearman_correlation/temp_quintiles |
| AF121 | 57 | Media cnt quintil superior temp 306,7 | R | STAT-009.spearman_correlation/temp_quintiles |
| AF122 | 57 | Media cnt aumenta entre quintiles extremos temp | R | STAT-009.spearman_correlation/temp_quintiles |
| AF123 | 59 | Spearman temp-atemp 0,990 | R | STAT-009 y STAT-003 |
| AF124 | 59 | temp y atemp son prácticamente redundantes como descriptores monotónicos | R | STAT-009 y STAT-003 |
| AF125 | 59 | Relaciones cnt-componentes parcialmente mecánicas por identidad | R | STAT-009 y STAT-003 |
| AF126 | 65 | FIG-001 muestra sumas diarias cnt | R | FIG-001 y STAT-011, código de gráficos evento 15 |
| AF127 | 65 | La agregación diaria conserva número de horas disponibles | R | FIG-001 y STAT-011, código de gráficos evento 15 |
| AF128 | 65 | La agregación diaria conserva suma casual | R | FIG-001 y STAT-011, código de gráficos evento 15 |
| AF129 | 65 | La agregación diaria conserva suma registered | R | FIG-001 y STAT-011, código de gráficos evento 15 |
| AF130 | 65 | Serie diaria permite ver variación a corto plazo | R | FIG-001 y STAT-011, código de gráficos evento 15 |
| AF131 | 65 | Serie diaria permite ver cambios de nivel entre años | R | FIG-001 y STAT-011, código de gráficos evento 15 |
| AF132 | 77 | FIG-004 muestra dispersión horaria de cnt frente a temp | R | FIG-004 y STAT-009/012, código evento 15 |
| AF133 | 77 | La guía de FIG-004 usa diez grupos de frecuencia aproximadamente igual | R | FIG-004 y STAT-009/012, código evento 15 |
| AF134 | 77 | La guía agregada de FIG-004 es ascendente | R | FIG-004 y STAT-009/012, código evento 15 |
| AF135 | 77 | La dispersión muestra que temp por sí sola no resume toda la variación cnt | R | FIG-004 y STAT-009/012, código evento 15 |
| AF136 | 83 | 505 observaciones sobre cerca IQR superior | R | STAT-010 e ISSUE-002 |
| AF137 | 83 | Cerca IQR superior 642,5 | R | STAT-010 e ISSUE-002 |
| AF138 | 83 | Extremos altos equivalen al 2,91 % de filas | R | STAT-010 e ISSUE-002 |
| AF139 | 83 | Máximo 977 en fecha 2012-09-12 | R | STAT-010 e ISSUE-002 |
| AF140 | 83 | Máximo 977 a las 18 h | R | STAT-010 e ISSUE-002 |
| AF141 | 83 | Valores extremos conservados | R | STAT-010 e ISSUE-002 |
| AF142 | 83 | Extremos respetan identidad de componentes | R | STAT-010 e ISSUE-002 |
| AF143 | 83 | Extremos no vulneran dominios revisados | R | STAT-010 e ISSUE-002 |
| AF144 | 83 | No hay evidencia interna que confirme los extremos como errores | R | STAT-010 e ISSUE-002 |
| AF145 | 83 | Extremos considerados altos descriptivamente, sin atribuir causa concreta | R | STAT-010 e ISSUE-002 |
| AF146 | 89 | Datos agregados no permiten estudiar viajes individuales | R | Readme.txt, profile y lista de columnas fuente |
| AF147 | 89 | Sin duración de viaje | R | Readme.txt, profile y lista de columnas fuente |
| AF148 | 89 | Sin origen de viaje | R | Readme.txt, profile y lista de columnas fuente |
| AF149 | 89 | Sin destino de viaje | R | Readme.txt, profile y lista de columnas fuente |
| AF150 | 89 | Sin estaciones del sistema | R | Readme.txt, profile y lista de columnas fuente |
| AF151 | 89 | Sin capacidad del sistema | R | Readme.txt, profile y lista de columnas fuente |
| AF152 | 89 | Sin exposición de usuarios | R | Readme.txt, profile y lista de columnas fuente |
