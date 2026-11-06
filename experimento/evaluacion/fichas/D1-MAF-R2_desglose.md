# Evaluación D1-MAF-R2

**Índice final:** 88,52/100.  
**Evaluación cerrada:** 6 de octubre de 2026.  
**Ejecución:** `D1_bike_sharing__microsoft_agent_framework__r02__20260831T175750234109Z`

**Criterios:** [Protocolo de evaluación](../01_protocolo_calidad_Q1_Q10_v0.1.md) y [guía D1](../02_ficha_D1_bike_sharing.md).  
**Resultados:** [Archivos originales de la ejecución](../../../outputs/experimento/D1_bike_sharing__microsoft_agent_framework__r02__20260831T175750234109Z).  
**Evaluación:** [Excel de puntuaciones](../Evaluacion_calidad.xlsx) y [JSON de comprobaciones](D1-MAF-R2_comprobaciones.json).

Las referencias `STAT`, `ISSUE` y `FIG` identifican análisis, problemas y figuras en los archivos de la ejecución. `TR` identifica transformaciones y `CHK`, comprobaciones de calidad. Las referencias a líneas corresponden al informe original, `report.md`.

## Resumen

| Métrica | Puntuación final |
| --- | ---: |
| Q1 Cumplimiento de las etapas | 100,00 |
| Q2 Corrección numérica | 94,29 |
| Q3 Validez del tratamiento de los datos | 100,00 |
| Q4 Detección de problemas y riesgos | 92,31 |
| Q5 Calidad y profundidad del EDA | 75,00 |
| Q6 Profundidad de la interpretación | 75,00 |
| Q7 Calidad de las visualizaciones | 85,00 |
| Q8 Cobertura del informe | 79,55 |
| Q9 Fidelidad del informe | 99,41 |
| Q10 Claridad y coherencia | 75,00 |

La ejecución terminó como `partial` porque se bloqueó una consulta después de que el Revisor agotara sus ocho lecturas permitidas. El Revisor emitió `approved` y no solicitó una corrección; los archivos finales se conservaron.

## Q1 Cumplimiento de las etapas: 100,00

| Etapa | Puntos | Evidencia |
| --- | ---: | --- |
| E1 Carga e inspección inicial | 1 | STAT-001 y profile |
| E2 Estructura, tipos y calidad | 1 | STAT-002/003/004 y CHK |
| E3 Preparación y decisiones de análisis | 1 | TR-001 a TR-004, CSV contrastado |
| E4 Estadística descriptiva | 1 | STAT-005/006/007/008 |
| E5 Variables, agregaciones y relaciones | 1 | STAT-009/010/011 |
| E6 Visualizaciones | 1 | FIG-001 a FIG-005 |
| E7 Problemas, riesgos y anomalías | 1 | STAT-012 e ISSUE-001/002/003 |
| E8 Informe final | 1 | report completo |

`Q1 = 100 x 8 / 8 = 100,00`

## Q2 Corrección numérica: 94,29

Se obtienen resultados correctos en 25 de las 26 comprobaciones, que suman 33 de los 35 puntos posibles. Solo permanece ausente el crecimiento porcentual entre los totales de alquileres de 2011 y 2012.

| Control | Peso | Resultado | Valor | Evidencia |
| --- | ---: | --- | --- | --- |
| C01 Número de filas | 2 | Correcta | 17379 | STAT-001.rows |
| C02 Número de columnas | 2 | Correcta | 17 | STAT-001.columns |
| C03 Fechas distintas | 1 | Correcta | 731 | STAT-004.days |
| C04 Celdas ausentes | 2 | Correcta | 0 | STAT-002.missing_by_column |
| C05 Filas duplicadas | 2 | Correcta | 0 | STAT-002.full_row_duplicates |
| C06 Huecos en la secuencia horaria | 1 | Correcta | 165 | STAT-004.missing_hour_slots |
| C07 Alquileres totales | 2 | Correcta | 3292679 | STAT-007.total_cnt |
| C08 Media horaria de alquileres | 2 | Correcta | 189,463088 | STAT-005.cnt.mean |
| C09 Mediana horaria de alquileres | 1 | Correcta | 142 | STAT-005.cnt.median |
| C10 Desviación típica muestral | 1 | Correcta | 181,387599 | STAT-005.cnt.std |
| C11 Máximo horario | 1 | Correcta | 977 | STAT-005.cnt.max |
| C12 Alquileres de usuarios ocasionales | 1 | Correcta | 620017 | STAT-007.total_casual |
| C13 Alquileres de usuarios registrados | 1 | Correcta | 2672662 | STAT-007.total_registered |
| C14 Proporción de alquileres de usuarios registrados | 1 | Correcta | 0,811698316 | STAT-007.registered_share_of_all_rentals |
| C15 Alquileres totales en 2011 | 1 | Correcta | 1243103 | STAT-010.monthly. Suma de los doce totales mensuales de 2011 |
| C16 Alquileres totales en 2012 | 1 | Correcta | 2049576 | STAT-010.monthly. Suma de los doce totales mensuales de 2012 |
| C17 Variación total de 2012 respecto a 2011 | 2 | Ausente | — | No se emitió el resultado exigido. |
| C18 Hora con mayor media | 2 | Correcta | 17, 461,452055 | STAT-009. Media conjunta de las 17 h, ponderada por el número de observaciones de cada tipo de día. |
| C19 Hora con menor media | 1 | Correcta | 4, 6,35294118 | STAT-009. Media conjunta de las 4 h, ponderada por el número de observaciones de cada tipo de día |
| C20 Temporada con mayor media | 1 | Correcta | 3, 236,016237 | STAT-008.by_season[season=3].cnt_mean |
| C21 Media con tiempo despejado | 1 | Correcta | 1, 204,869272 | STAT-008.by_weathersit[weathersit=1].cnt_mean |
| C22 Media con tiempo adverso de categoría 3 | 1 | Correcta | 3, 111,579281 | STAT-008.by_weathersit[weathersit=3].cnt_mean |
| C23 Observaciones meteorológicas de categoría 4 | 1 | Correcta | 3 | STAT-008.by_weathersit[weathersit=4].cnt_count |
| C24 Correlación de Pearson entre temperatura y cnt | 1 | Correcta | 0,404772 | STAT-011.pearson.cnt.temp |
| C25 Correlación de Pearson entre humedad y cnt | 1 | Correcta | -0,322911 | STAT-011.pearson.cnt.hum |
| C26 Inconsistencias en cnt = casual + registered | 2 | Correcta | 0 | STAT-003.identity_violations |

`Q2 = 100 x 33 / 35 = 94,29`

## Q3 Validez del tratamiento de los datos: 100,00

| Decisión | Puntos | Evidencia |
| --- | ---: | --- |
| D01 Fecha-hora correcta | 1 | TR-001/002 y CSV date_hour válido |
| D02 Códigos como categorías | 1 | STAT-003/006/008/009, agrupaciones y códigos intactos |
| D03 instant solo identificador | 1 | STAT-002, report 17 y variables analíticas seleccionadas |
| D04 Sin limpieza innecesaria | 1 | STAT-002, TR-004 y 17 columnas conservadas |
| D05 No imputar huecos | 1 | STAT-004, ISSUE-001, report 83 |
| D06 Extremos conservados | 1 | STAT-012, ISSUE-002 y contraste CSV |
| D07 Identidad preservada e interpretada | 1 | STAT-003/007, report 5/15/29 y no correlacionar cnt con componentes como evidencia independiente |
| D08 Escalas normalizadas conservadas | 1 | CSV, STAT-003/005 y report 94 |

`Q3 = 100 x 8 / 8 = 100,00`

## Q4 Detección de problemas y riesgos: 92,31

| Riesgo | Clasificación | Evidencia |
| --- | --- | --- |
| R01 Identificador secuencial | Completo | STAT-002 y report 17/25, uso de instant solo como índice |
| R02 Códigos categóricos/binarios | Completo | STAT-003/006 y agrupaciones STAT-008/009 |
| R03 Identidad de componentes | Completo | STAT-003/007, report 5/15/29, composición y no presentar correlaciones entre componentes como evidencia independiente |
| R04 Meteorología normalizada | Completo | STAT-003/005 y report 27/41/94 |
| R05 Huecos horarios | Completo | STAT-004, ISSUE-001 y report 83/95 |
| R06 Meteorología 4, n = 3 | Completo | STAT-006/008 y report 45/71/96 |
| R07 Dependencia y derivación temporal | Parcial | STAT-003 reconoce calendario derivado. Report 98 habla de confusión temporal, no de dependencia entre observaciones sucesivas |
| A01 Redundancia temp-atemp | Adicional válido | STAT-011, Spearman 0,989633 y Pearson 0,987672. Report 55/75 |
| A02 Extremos contextuales influyen en resúmenes | Adicional válido | STAT-012, ISSUE-002 y report 85 |
| A03 Falta de información individual y exposición | Adicional válido | profile y report 79/93 |
| A04 Riesgo de sustituir season por una clasificación mensual no justificada | Adicional válido | STAT-003, ISSUE-003 y report 33/87 |

Se identifican seis riesgos previstos y cuatro adicionales, sin falsas alarmas. La precisión es 1, la cobertura es 6/7 y F1 es 12/13.

`Q4 = 100 x [2 x 1 x (6 / 7)] / [1 + (6 / 7)] = 92,31`

## Q5 Calidad y profundidad del EDA: 75,00

El análisis examina distribuciones, composición, diferencias entre grupos, asociaciones y extremos diarios contextualizados. Recibe 3 de 4 puntos porque no presenta el perfil horario del conjunto completo ni desarrolla la dependencia entre observaciones temporales.

**Evidencia:** STAT-005 a STAT-012, report 37–57, 83–98 y figuras. No hay agrupación global por hr.

`Q5 = 100 x 3 / 4 = 75,00`

## Q6 Profundidad de la interpretación: 75,00

La interpretación relaciona los perfiles, las escalas y los tamaños de los grupos con las limitaciones del análisis. Recibe 3 de 4 puntos porque la línea 71 afirma que FIG-003 muestra las medias mediante puntos, aunque estos no aparecen en la imagen.

**Evidencia:** Report71, FIG-003 final y AF152, junto con el resto de interpretaciones de report31–33, 43–55 y 83–98.

`Q6 = 100 x 3 / 4 = 75,00`

## Q7 Calidad de las visualizaciones: 85,00

| Objetivo | Nota 0–4 | Justificación y evidencia |
| --- | ---: | --- |
| V01 Evolución 2011–2012 | 4 | FIG-001 muestra suma diaria y media móvil centrada de 28 días, con eje temporal claro y cobertura explicada. STAT-010 y evento 20 |
| V02 Horas por tipo de día | 4 | FIG-002 compara las 24 horas con dos curvas y máximos explicados. STAT-009 y report 49/67 |
| V03 Patrón mensual o estacional | 3 | FIG-001 permite ver ciclos estacionales y meses ordenados. Su explicación no desarrolla expresamente ese patrón. STAT-010 y report 53/63 |
| V04 Meteorología y n pequeño | 3 | FIG-003 permite comparar las distribuciones y el informe advierte que la categoría 4 tiene tres observaciones. El gráfico oculta los valores extremos sin explicarlo y no muestra los puntos de las medias anunciados en el texto |
| V05 Relación meteorológica legible | 3 | FIG-004 usa diez intervalos de igual anchura, con medias trazables. No muestra variabilidad interna ni tamaños desiguales |

`Q7 = 100 x 17 / 20 = 85,00`

## Q8 Cobertura del informe: 79,55

| Unidad | Puntuación | Peso | Evidencia o carencia |
| --- | ---: | ---: | --- |
| U01 | 1 | 2 | Report 3, estructura y periodo |
| U02 | 1 | 2 | Report 5/11/25, nulos y duplicados distintos de huecos |
| U03 | 1 | 2 | Report 37, nivel, dispersión y cuantiles |
| U04 | 1 | 2 | Report 9/39, cuota 81,2 % |
| U05 | 0 | 2 | Report 43 compara medias horarias anuales, no totales ni su crecimiento |
| U06 | 0 | 2 | Las líneas 49 y 67 presentan máximos separados para días laborables y no laborables, pero no identifican el máximo y el mínimo del conjunto completo |
| U07 | 1 | 2 | Report 49/67 y FIG-002, picos 17 h laborable y 13 h no laborable |
| U08 | 1 | 1 | Report 53 comunica las cuatro medias estacionales, con máximo inequívoco en código 3 |
| U09 | 1 | 2 | Report 45/71/96, diferencias y n = 3 |
| U10 | 1 | 2 | Report 55/98, temperatura/humedad y prudencia |
| U11 | 1 | 2 | Report 5/15/29, identidad y composición, sin descubrimiento predictivo |
| U12 | 0,5 | 1 | Report 15/93/98, ciudad y ausencia de base causal. No explica dependencia entre horas |

`Q8 = 100 x 17,5 / 22 = 79,55`

## Q9 Fidelidad del informe: 99,41

Se respaldan 168 de las 169 afirmaciones evaluadas. AF152 está contradicha porque el informe afirma que FIG-003 señala la media de cada grupo mediante un punto, pero esos puntos no aparecen en la imagen. El símbolo rojo solo figura en la leyenda.

El inventario situado al final de esta ficha recoge las afirmaciones revisadas, su clasificación y las evidencias utilizadas.

`Q9 = 100 x 168 / 169 = 99,41`

## Q10 Claridad y coherencia: 75,00

El informe está bien organizado y enlaza sus evidencias. Recibe 3 de 4 puntos por repeticiones y códigos de season/weathersit cuyo significado no explica. Los hallazgos principales son comprensibles.

**Evidencia:** report.md, especialmente 17, 23, 45, 53, 71, 102–108.

`Q10 = 100 x 3 / 4 = 75,00`

## Inventario de afirmaciones

R = respaldada, C = contradicha, S = sin respaldo suficiente. Las líneas remiten al informe original. Se incluyen las 169 afirmaciones distintas.

| ID | Líneas | Afirmación | Estado | Evidencia |
| --- | --- | --- | --- | --- |
| AF001 | 3, 15, 17 | CSV horario de Bike Sharing | R | STAT-001, profile y Readme.txt |
| AF002 | 3, 15, 17 | 17379 registros | R | STAT-001, profile y Readme.txt |
| AF003 | 3, 15, 17 | 17 variables fuente | R | STAT-001, profile y Readme.txt |
| AF004 | 3, 15, 17 | Inicio 2011-01-01 | R | STAT-001, profile y Readme.txt |
| AF005 | 3, 15, 17 | Final 2012-12-31 | R | STAT-001, profile y Readme.txt |
| AF006 | 3, 15, 17 | Cada fila es un agregado de alquileres de una hora | R | STAT-001, profile y Readme.txt |
| AF007 | 3, 15, 17 | dteday y hr sitúan la observación temporalmente | R | STAT-001, profile y Readme.txt |
| AF008 | 3, 15, 17 | Datos de Capital Bikeshare | R | STAT-001, profile y Readme.txt |
| AF009 | 3, 15, 17 | Datos de Washington D.C. | R | STAT-001, profile y Readme.txt |
| AF010 | 3, 15, 17 | Calendario y estación asociados a cada observación | R | STAT-001, profile y Readme.txt |
| AF011 | 3, 15, 17 | Meteorología normalizada en la tabla | R | STAT-001, profile y Readme.txt |
| AF012 | 3, 15, 17 | casual corresponde a usuarios ocasionales | R | STAT-001, profile y Readme.txt |
| AF013 | 3, 15, 17 | registered corresponde a usuarios registrados | R | STAT-001, profile y Readme.txt |
| AF014 | 3, 15, 17 | cnt es el total horario | R | STAT-001, profile y Readme.txt |
| AF015 | 3, 15, 17 | instant es un índice trazable | R | STAT-001, profile y Readme.txt |
| AF016 | 5, 25, 89, 102 | Sin valores ausentes en columnas fuente | R | STAT-002 y contraste fuente |
| AF017 | 5, 25, 89, 102 | Sin fechas no convertibles | R | STAT-002 y contraste fuente |
| AF018 | 5, 25, 89, 102 | Sin filas completas duplicadas | R | STAT-002 y contraste fuente |
| AF019 | 5, 25, 89, 102 | Sin instant duplicados | R | STAT-002 y contraste fuente |
| AF020 | 5, 25, 89, 102 | Sin combinaciones dteday-hr duplicadas | R | STAT-002 y contraste fuente |
| AF021 | 5, 25, 89, 102 | instant está ordenado | R | STAT-002 y contraste fuente |
| AF022 | 5, 25, 89, 102 | instant no presenta saltos consecutivos | R | STAT-002 y contraste fuente |
| AF023 | 5, 29, 89, 102 | cnt = casual + registered en todas las filas | R | STAT-003.identity_violations y contraste |
| AF024 | 7, 31, 63, 83, 102, 108 | Se conservan todas las observaciones | R | preparation, CSV y evento 20 |
| AF025 | 7, 31, 63, 83, 102, 108 | Se añaden únicamente dos variables derivadas | R | preparation, CSV y evento 20 |
| AF026 | 7, 31, 63, 83, 102, 108 | date_hour combina fecha y hora | R | preparation, CSV y evento 20 |
| AF027 | 7, 31, 63, 83, 102, 108 | casual_share = casual / cnt | R | preparation, CSV y evento 20 |
| AF028 | 7, 31, 63, 83, 102, 108 | No hay filas con cnt = 0 | R | preparation, CSV y evento 20 |
| AF029 | 7, 31, 63, 83, 102, 108 | casual_share no introduce ausencias | R | preparation, CSV y evento 20 |
| AF030 | 7, 31, 63, 83, 102, 108 | dteday se convierte a fecha y se serializa ISO | R | preparation, CSV y evento 20 |
| AF031 | 7, 31, 63, 83, 102, 108 | Se conservan las 17 columnas fuente | R | preparation, CSV y evento 20 |
| AF032 | 7, 31, 63, 83, 102, 108 | Se conservan los extremos | R | preparation, CSV y evento 20 |
| AF033 | 7, 31, 63, 83, 102, 108 | Se conservan los códigos fuente | R | preparation, CSV y evento 20 |
| AF034 | 7, 31, 63, 83, 102, 108 | No se imputan horas ausentes | R | preparation, CSV y evento 20 |
| AF035 | 7, 31, 63, 83, 102, 108 | No se recortan valores ni se excluyen filas | R | preparation, CSV y evento 20 |
| AF036 | 7, 31, 63, 83, 102, 108 | La copia preparada contiene derivadas trazables | R | preparation, CSV y evento 20 |
| AF037 | 9, 37, 104 | Media cnt 189,5 | R | STAT-005.cnt |
| AF038 | 9, 37, 104 | Mediana cnt 142 | R | STAT-005.cnt |
| AF039 | 9, 37, 104 | Mínimo cnt 1 | R | STAT-005.cnt |
| AF040 | 9, 37, 104 | Máximo cnt 977 | R | STAT-005.cnt |
| AF041 | 9, 37, 104 | Desviación estándar cnt 181,4 | R | STAT-005.cnt |
| AF042 | 9, 37, 104 | Percentil 25 cnt 40 | R | STAT-005.cnt |
| AF043 | 9, 37, 104 | Percentil 75 cnt 281 | R | STAT-005.cnt |
| AF044 | 9, 37, 104 | Percentil 95 cnt 563,1 | R | STAT-005.cnt |
| AF045 | 9, 37, 104 | Percentil 99 cnt 782,2 | R | STAT-005.cnt |
| AF046 | 9, 37, 104 | Distribución cnt con cola superior relevante | R | STAT-005.cnt |
| AF047 | 9, 37, 104 | Demanda horaria variable | R | STAT-005.cnt |
| AF048 | 9, 39, 104 | Total cnt 3292679 | R | STAT-007 y contraste global |
| AF049 | 9, 39, 104 | Total registrados 2672662 | R | STAT-007 y contraste global |
| AF050 | 9, 39, 104 | Total ocasionales 620017 | R | STAT-007 y contraste global |
| AF051 | 9, 39, 104 | Cuota global registrados 81,2 % | R | STAT-007 y contraste global |
| AF052 | 9, 39, 104 | Cuota global ocasionales 18,8 % | R | STAT-007 y contraste global |
| AF053 | 9, 39, 104 | Predominio agregado de usuarios registrados | R | STAT-007 y contraste global |
| AF054 | 11, 57, 83, 95, 108 | Rejilla temporal esperada 17544 horas | R | STAT-004, ISSUE-001 y código de cobertura |
| AF055 | 11, 57, 83, 95, 108 | 165 posiciones horarias sin registro | R | STAT-004, ISSUE-001 y código de cobertura |
| AF056 | 11, 57, 83, 95, 108 | 731 fechas con observaciones | R | STAT-004, ISSUE-001 y código de cobertura |
| AF057 | 11, 57, 83, 95, 108 | 76 fechas con distinto número de registros de 24 | R | STAT-004, ISSUE-001 y código de cobertura |
| AF058 | 11, 57, 83, 95, 108 | Sumas de periodos con fechas incompletas pueden quedar subestimadas | R | STAT-004, ISSUE-001 y código de cobertura |
| AF059 | 11, 57, 83, 95, 108 | Extremo temporal inicial 2011-01-01 00 h | R | STAT-004, ISSUE-001 y código de cobertura |
| AF060 | 11, 57, 83, 95, 108 | Extremo temporal final 2012-12-31 23 h | R | STAT-004, ISSUE-001 y código de cobertura |
| AF061 | 11, 57, 83, 95, 108 | Existen fechas incompletas con 12 registros | R | STAT-004, ISSUE-001 y código de cobertura |
| AF062 | 11, 57, 83, 95, 108 | Existen fechas incompletas con 8 registros | R | STAT-004, ISSUE-001 y código de cobertura |
| AF063 | 11, 57, 83, 95, 108 | Existen fechas incompletas con 18 registros | R | STAT-004, ISSUE-001 y código de cobertura |
| AF064 | 11, 57, 83, 95, 108 | Existen fechas incompletas con 17 registros | R | STAT-004, ISSUE-001 y código de cobertura |
| AF065 | 11, 57, 83, 95, 108 | Existe una fecha incompleta con 1 registro | R | STAT-004, ISSUE-001 y código de cobertura |
| AF066 | 11, 57, 83, 95, 108 | Existe una fecha incompleta con 11 registros | R | STAT-004, ISSUE-001 y código de cobertura |
| AF067 | 11, 57, 83, 95, 108 | El archivo no acredita la causa de los huecos ni los recuentos ausentes | R | STAT-004, ISSUE-001 y código de cobertura |
| AF068 | 17 | season es un código categórico | R | STAT-003/006/008/009 y selección de operaciones |
| AF069 | 17 | yr es un código de calendario | R | STAT-003/006/008/009 y selección de operaciones |
| AF070 | 17 | mnth es un código de calendario | R | STAT-003/006/008/009 y selección de operaciones |
| AF071 | 17 | holiday es un código categórico o de calendario | R | STAT-003/006/008/009 y selección de operaciones |
| AF072 | 17 | weekday es un código categórico o de calendario | R | STAT-003/006/008/009 y selección de operaciones |
| AF073 | 17 | workingday es un código categórico o de calendario | R | STAT-003/006/008/009 y selección de operaciones |
| AF074 | 17 | weathersit es categórica | R | STAT-003/006/008/009 y selección de operaciones |
| AF075 | 17 | Los códigos no se tratan como escalas numéricas sustantivas | R | STAT-003/006/008/009 y selección de operaciones |
| AF076 | 19 | Alcance exploratorio y descriptivo | R | Traza del Analista y métodos STAT-001 a STAT-012 |
| AF077 | 19 | No se entrenan modelos predictivos | R | Traza del Analista y métodos STAT-001 a STAT-012 |
| AF078 | 19 | No se realizan inferencias causales | R | Traza del Analista y métodos STAT-001 a STAT-012 |
| AF079 | 23 | hr contiene 24 categorías | R | STAT-006 y STAT-001 |
| AF080 | 23 | season contiene 4 códigos | R | STAT-006 y STAT-001 |
| AF081 | 23 | weathersit contiene 4 códigos | R | STAT-006 y STAT-001 |
| AF082 | 23 | yr distingue los dos años codificados | R | STAT-006 y STAT-001 |
| AF083 | 27, 89 | Los ocho códigos categóricos están dentro de sus dominios documentados | R | STAT-003 |
| AF084 | 27, 89 | temp permanece en 0–1 | R | STAT-003 |
| AF085 | 27, 89 | atemp permanece en 0–1 | R | STAT-003 |
| AF086 | 27, 89 | hum permanece en 0–1 | R | STAT-003 |
| AF087 | 27, 89 | windspeed permanece en 0–1 | R | STAT-003 |
| AF088 | 27, 89 | temp mínimo 0,02 | R | STAT-003 |
| AF089 | 27, 89 | temp máximo 1 | R | STAT-003 |
| AF090 | 27, 89 | windspeed mínimo 0 | R | STAT-003 |
| AF091 | 27, 89 | windspeed máximo 0,8507 | R | STAT-003 |
| AF092 | 27, 89 | Sin conteos negativos | R | STAT-003 |
| AF093 | 29 | yr coincide con el año de dteday codificado | R | STAT-003.calendar_mismatches |
| AF094 | 29 | mnth coincide con el mes de dteday | R | STAT-003.calendar_mismatches |
| AF095 | 29 | weekday coincide con dteday al usar domingo = 0 | R | STAT-003.calendar_mismatches |
| AF096 | 33, 53, 87, 108 | 3922 filas difieren de la regla mensual simplificada de season | R | STAT-003, ISSUE-003 y actualización de evento 37 |
| AF097 | 33, 53, 87, 108 | season no equivale siempre a bloques rígidos de meses | R | STAT-003, ISSUE-003 y actualización de evento 37 |
| AF098 | 33, 53, 87, 108 | La discrepancia no demuestra códigos season inválidos | R | STAT-003, ISSUE-003 y actualización de evento 37 |
| AF099 | 33, 53, 87, 108 | Se conserva season como clasificación de la fuente | R | STAT-003, ISSUE-003 y actualización de evento 37 |
| AF100 | 39 | Media casual 35,7 | R | STAT-005 |
| AF101 | 39 | Mediana casual 17 | R | STAT-005 |
| AF102 | 39 | Media registered 153,8 | R | STAT-005 |
| AF103 | 39 | Mediana registered 115 | R | STAT-005 |
| AF104 | 41, 94 | Media temp 0,497 | R | STAT-005, CSV y operaciones evento 20 |
| AF105 | 41, 94 | Media atemp 0,476 | R | STAT-005, CSV y operaciones evento 20 |
| AF106 | 41, 94 | Media hum 0,627 | R | STAT-005, CSV y operaciones evento 20 |
| AF107 | 41, 94 | Media windspeed 0,190 | R | STAT-005, CSV y operaciones evento 20 |
| AF108 | 41, 94 | Mediana temp 0,500 | R | STAT-005, CSV y operaciones evento 20 |
| AF109 | 41, 94 | Mediana atemp 0,4848 | R | STAT-005, CSV y operaciones evento 20 |
| AF110 | 41, 94 | Mediana hum 0,630 | R | STAT-005, CSV y operaciones evento 20 |
| AF111 | 41, 94 | Mediana windspeed 0,194 | R | STAT-005, CSV y operaciones evento 20 |
| AF112 | 41, 94 | No se convierten variables meteorológicas a unidades físicas | R | STAT-005, CSV y operaciones evento 20 |
| AF113 | 43 | Media horaria cnt 2011 143,8 | R | STAT-008.by_year |
| AF114 | 43 | Media horaria cnt 2012 234,7 | R | STAT-008.by_year |
| AF115 | 43 | La media horaria aumenta entre ambos códigos anuales | R | STAT-008.by_year |
| AF116 | 45, 71, 96 | Media cnt con weathersit 1 204,9 | R | STAT-008.by_weathersit y STAT-006 |
| AF117 | 45, 71, 96 | Media cnt con weathersit 2 175,2 | R | STAT-008.by_weathersit y STAT-006 |
| AF118 | 45, 71, 96 | Media cnt con weathersit 3 111,6 | R | STAT-008.by_weathersit y STAT-006 |
| AF119 | 45, 71, 96 | Media cnt con weathersit 4 74,3 | R | STAT-008.by_weathersit y STAT-006 |
| AF120 | 45, 71, 96 | weathersit 4 contiene 3 observaciones | R | STAT-008.by_weathersit y STAT-006 |
| AF121 | 45, 71, 96 | El promedio de categoría 4 tiene soporte muy reducido y es inestable | R | STAT-008.by_weathersit y STAT-006 |
| AF122 | 49, 67 | Máxima media no laborable a las 13 h | R | STAT-009 y FIG-002 |
| AF123 | 49, 67 | Máxima media no laborable 372,7 | R | STAT-009 y FIG-002 |
| AF124 | 49, 67 | Máxima media laborable a las 17 h | R | STAT-009 y FIG-002 |
| AF125 | 49, 67 | Máxima media laborable 525,3 | R | STAT-009 y FIG-002 |
| AF126 | 49, 67 | Pico medio laborable mayor que el pico no laborable | R | STAT-009 y FIG-002 |
| AF127 | 49, 67 | Perfil horario difiere según workingday | R | STAT-009 y FIG-002 |
| AF128 | 49, 67 | Los perfiles no aíslan las diferencias simultáneas de clima, año y estación | R | STAT-009 y FIG-002 |
| AF129 | 51, 79, 104 | Composición porcentual por hora calculada desde sumas casual y registered | R | FIG-005 y código de composición evento 20 |
| AF130 | 51, 79, 104 | Mezcla entre casual y registered variable a lo largo del día | R | FIG-005 y código de composición evento 20 |
| AF131 | 51, 79, 104 | La composición horaria representa proporciones de alquileres, no personas únicas | R | FIG-005 y código de composición evento 20 |
| AF132 | 51, 79, 104 | La composición horaria no es una medida de exposición | R | FIG-005 y código de composición evento 20 |
| AF133 | 53 | Media cnt temporada 1 111,1 | R | STAT-008.by_season |
| AF134 | 53 | Media cnt temporada 2 208,3 | R | STAT-008.by_season |
| AF135 | 53 | Media cnt temporada 3 236,0 | R | STAT-008.by_season |
| AF136 | 53 | Media cnt temporada 4 198,9 | R | STAT-008.by_season |
| AF137 | 55 | Spearman cnt-temp 0,423 | R | STAT-011.spearman |
| AF138 | 55 | Spearman cnt-atemp 0,423 | R | STAT-011.spearman |
| AF139 | 55 | Spearman cnt-hum −0,360 | R | STAT-011.spearman |
| AF140 | 55 | Spearman cnt-windspeed 0,127 | R | STAT-011.spearman |
| AF141 | 55 | Las correlaciones de rango describen asociación monotónica | R | STAT-011.spearman |
| AF142 | 55 | temp y atemp presentan elevada similitud y potencial redundancia | R | STAT-011.spearman |
| AF143 | 55, 75, 98, 106 | Asociaciones bivariadas no prueban efectos causales meteorológicos | R | STAT-011 Pearson/Spearman y alcance de métodos |
| AF144 | 55, 75, 98, 106 | Clima, calendario y demanda pueden estar entrelazados con estacionalidad y tendencia anual | R | STAT-011 Pearson/Spearman y alcance de métodos |
| AF145 | 57, 63 | Se agregan las horas a 731 fechas | R | STAT-010 y código de agregación/figura evento 20 |
| AF146 | 57, 63 | Se producen resúmenes mensuales por año y mes | R | STAT-010 y código de agregación/figura evento 20 |
| AF147 | 57, 63 | FIG-001 representa sumas diarias de cnt | R | STAT-010 y código de agregación/figura evento 20 |
| AF148 | 57, 63 | FIG-001 representa media móvil de 28 días | R | STAT-010 y código de agregación/figura evento 20 |
| AF149 | 57, 63 | FIG-001 permite distinguir fluctuaciones diarias y variaciones más persistentes | R | STAT-010 y código de agregación/figura evento 20 |
| AF150 | 57, 63 | Días incompletos se mantienen visibles en la serie | R | STAT-010 y código de agregación/figura evento 20 |
| AF151 | 71 | FIG-003 representa distribuciones cnt por weathersit | R | FIG-003, STAT-008 y código de gráfico evento 20 |
| AF152 | 71 | FIG-003 señala la media de cada categoría con un punto | C | FIG-003 final: los puntos de las medias no son visibles, solo su símbolo en la leyenda |
| AF153 | 71 | FIG-003 incluye categoría weathersit 4 | R | FIG-003, STAT-008 y código de gráfico evento 20 |
| AF154 | 71 | Distribuciones meteorológicas muestran heterogeneidad | R | FIG-003, STAT-008 y código de gráfico evento 20 |
| AF155 | 75 | FIG-004 representa medias cnt por intervalos de temperatura | R | FIG-004, STAT-011.cnt_by_temp_bin y evento 20 |
| AF156 | 75 | FIG-004 evita superponer los 17379 puntos individuales | R | FIG-004, STAT-011.cnt_by_temp_bin y evento 20 |
| AF157 | 85, 97, 108 | Ocho días cuyo total de alquileres se aleja al menos tres desviaciones estándar de la media de su mes y año | R | STAT-012 e ISSUE-002 |
| AF158 | 85, 97, 108 | La regla compara cada suma diaria con la media de su mes-año | R | STAT-012 e ISSUE-002 |
| AF159 | 85, 97, 108 | La regla usa desviación estándar de su mes-año | R | STAT-012 e ISSUE-002 |
| AF160 | 85, 97, 108 | Señales estadísticas no son errores de captura confirmados | R | STAT-012 e ISSUE-002 |
| AF161 | 85, 97, 108 | Se conservan los ocho días señalados | R | STAT-012 e ISSUE-002 |
| AF162 | 85, 97, 108 | Se usan medianas y cuantiles además de medias sensibles a extremos | R | STAT-012 e ISSUE-002 |
| AF163 | 85, 97, 108 | No se atribuyen los extremos a eventos específicos sin evidencia | R | STAT-012 e ISSUE-002 |
| AF164 | 93 | Sin identificación de personas únicas | R | Lista de columnas fuente STAT-001 y Readme.txt |
| AF165 | 93 | Sin trayectos individuales | R | Lista de columnas fuente STAT-001 y Readme.txt |
| AF166 | 93 | Sin duración de viaje | R | Lista de columnas fuente STAT-001 y Readme.txt |
| AF167 | 93 | Sin estaciones del sistema | R | Lista de columnas fuente STAT-001 y Readme.txt |
| AF168 | 93 | Sin disponibilidad de bicicletas | R | Lista de columnas fuente STAT-001 y Readme.txt |
| AF169 | 93 | Sin capacidad del sistema | R | Lista de columnas fuente STAT-001 y Readme.txt |