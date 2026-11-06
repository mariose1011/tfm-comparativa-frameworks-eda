# Evaluación D1-MAF-R1

**Índice final:** 86,40/100.  
**Evaluación cerrada:** 6 de octubre de 2026.  
**Ejecución:** `D1_bike_sharing__microsoft_agent_framework__r01__20260831T174252477482Z`

**Criterios:** [Protocolo de evaluación](../01_protocolo_calidad_Q1_Q10_v0.1.md) y [guía D1](../02_ficha_D1_bike_sharing.md).  
**Resultados:** [Archivos originales de la ejecución](../../../outputs/experimento/D1_bike_sharing__microsoft_agent_framework__r01__20260831T174252477482Z).  
**Evaluación:** [Excel de puntuaciones](../Evaluacion_calidad.xlsx) y [JSON de comprobaciones](D1-MAF-R1_comprobaciones.json).

Las referencias `STAT`, `ISSUE` y `FIG` identifican análisis, problemas y figuras en los archivos de la ejecución. `TR` identifica transformaciones y `CHK`, comprobaciones de calidad. Las referencias a líneas corresponden al informe original, `report.md`.

## Resumen

| Métrica | Puntuación final |
| --- | ---: |
| Q1 Cumplimiento de las etapas | 100,00 |
| Q2 Corrección numérica | 85,71 |
| Q3 Validez del tratamiento de los datos | 87,50 |
| Q4 Detección de problemas y riesgos | 92,31 |
| Q5 Calidad y profundidad del EDA | 75,00 |
| Q6 Profundidad de la interpretación | 75,00 |
| Q7 Calidad de las visualizaciones | 90,00 |
| Q8 Cobertura del informe | 79,55 |
| Q9 Fidelidad del informe | 98,61 |
| Q10 Claridad y coherencia | 75,00 |

## Q1 Cumplimiento de las etapas: 100,00

| Etapa | Nota | Justificación | Evidencia |
| --- | --- | --- | --- |
| E1 Carga e inspección inicial | 1 | Carga, dimensiones y unidad horaria identificadas. | STAT-001, profile y report, líneas 13–15 |
| E2 Estructura, tipos y calidad | 1 | Dominios, rangos, ausencias, duplicados y calendario comprobados. Fallo localizado en conclusión de season. | STAT-002/003/004 |
| E3 Preparación y decisiones de análisis | 1 | Copia utilizable y decisiones antes/después documentadas. D01 se valora aparte en Q3. | preparation, STAT-005 y contraste CSV |
| E4 Estadística descriptiva | 1 | Descriptivos reproducibles de las variables principales. | STAT-006/007 |
| E5 Variables, agregaciones y relaciones | 1 | Agregaciones y asociaciones pertinentes. | STAT-008 a STAT-013 |
| E6 Visualizaciones | 1 | Seis PNG legibles con datos trazables. | FIG-001 a FIG-006 |
| E7 Problemas, riesgos y anomalías | 1 | Problemas estructurados, decisiones y consecuencias. | issues.json, CHK-001 a CHK-005, ISSUE-001/002 |
| E8 Informe final | 1 | Informe evaluable con alcance, hallazgos y limitaciones. | report.md completo |

`Q1 = 100 x 8 / 8 = 100,00`

## Q2 Corrección numérica: 85,71

Se obtienen resultados correctos en 22 de las 26 comprobaciones, que suman 30 de los 35 puntos posibles. Permanecen ausentes la proporción global de alquileres de usuarios registrados, el crecimiento porcentual anual y las dos correlaciones de Pearson previstas.

| Control | Peso | Resultado | Valor | Evidencia |
| --- | ---: | --- | --- | --- |
| C01 Número de filas | 2 | Correcta | 17379 | STAT-001.rows |
| C02 Número de columnas | 2 | Correcta | 17 | STAT-001.columns |
| C03 Fechas distintas | 1 | Correcta | 731 | STAT-004.unique_dates |
| C04 Celdas ausentes | 2 | Correcta | 0 | STAT-002.missing_by_column |
| C05 Filas duplicadas | 2 | Correcta | 0 | STAT-002.full_row_duplicates |
| C06 Huecos en la secuencia horaria | 1 | Correcta | 165 | STAT-004.slots_not_represented |
| C07 Alquileres totales | 2 | Correcta | 3292679 | STAT-008.by_year. Suma de los totales anuales: 1.243.103 + 2.049.576 |
| C08 Media horaria de alquileres | 2 | Correcta | 189,4631 | STAT-006.cnt.mean |
| C09 Mediana horaria de alquileres | 1 | Correcta | 142 | STAT-006.cnt.median |
| C10 Desviación típica muestral | 1 | Correcta | 181,3876 | STAT-006.cnt.std |
| C11 Máximo horario | 1 | Correcta | 977 | STAT-006.cnt.max |
| C12 Alquileres de usuarios ocasionales | 1 | Correcta | 620017 | STAT-008.by_year. Suma de los alquileres ocasionales: 247.252 + 372.765 |
| C13 Alquileres de usuarios registrados | 1 | Correcta | 2672662 | STAT-008.by_year. Suma de los alquileres de registrados: 995.851 + 1.676.811 |
| C14 Proporción de alquileres de usuarios registrados | 1 | Ausente | — | No se emitió el resultado exigido. |
| C15 Alquileres totales en 2011 | 1 | Correcta | 1243103 | STAT-008.by_year[2011].cnt_sum |
| C16 Alquileres totales en 2012 | 1 | Correcta | 2049576 | STAT-008.by_year[2012].cnt_sum |
| C17 Variación total de 2012 respecto a 2011 | 2 | Ausente | — | No se emitió el resultado exigido. |
| C18 Hora con mayor media | 2 | Correcta | 17, 461,4521 | STAT-008.by_hour[hr=17].cnt_mean |
| C19 Hora con menor media | 1 | Correcta | 4, 6,3529 | STAT-008.by_hour[hr=4].cnt_mean |
| C20 Temporada con mayor media | 1 | Correcta | 3, 236,0162 | STAT-008.by_season[season=3].cnt_mean |
| C21 Media con tiempo despejado | 1 | Correcta | 1, 204,869272 | STAT-011.by_weathersit[1].cnt_mean |
| C22 Media con tiempo adverso de categoría 3 | 1 | Correcta | 3, 111,579281 | STAT-011.by_weathersit[3].cnt_mean |
| C23 Observaciones meteorológicas de categoría 4 | 1 | Correcta | 3 | STAT-011.by_weathersit[4].n_hours |
| C24 Correlación de Pearson entre temperatura y cnt | 1 | Ausente | — | No se emitió el resultado exigido. |
| C25 Correlación de Pearson entre humedad y cnt | 1 | Ausente | — | No se emitió el resultado exigido. |
| C26 Inconsistencias en cnt = casual + registered | 2 | Correcta | 0 | STAT-003.cnt_identity_failures |

`Q2 = 100 x 30 / 35 = 85,71`

## Q3 Validez del tratamiento de los datos: 87,50

| ID | Nota | Justificación | Evidencia |
| --- | --- | --- | --- |
| D01 | 0 |Convierte `dteday` a fecha, pero no la combina con `hr` para construir una marca temporal o un índice equivalente. Ambas columnas originales se conservan. CSV, STAT-005 y eventos 16 y 29 de la traza. | CSV, STAT-005 y traza eventos 16/29 |
| D02 | 1 | Usa los códigos como grupos categóricos o binarios y añade etiquetas sin alterar códigos. | STAT-003/007/008/010/011 y traza |
| D03 | 1 | instant se conserva como índice, no como medida explicativa. | report línea 15, STAT-002 y variables de STAT-006/012 |
| D04 | 1 | Conserva todas las filas al no existir nulos ni duplicados. | STAT-002/005 y CSV |
| D05 | 1 | No imputa las 165 horas ausentes ni crea observaciones sintéticas. | ISSUE-001, report línea 93 y contraste CSV |
| D06 | 1 | Conserva extremos válidos y justifica no asumir que son errores. | ISSUE-002, STAT-014 y CSV |
| D07 | 1 | Conserva cnt y componentes y explica su partición exacta. | STAT-003, STAT-010, report línea 35 y CSV |
| D08 | 1 | Mantiene escalas normalizadas y no las presenta como unidades físicas. | CSV y report líneas 37/103 |

Q3 = 100 x 7 / 8 = 87,50

## Q4 Detección de problemas y riesgos: 92,31

| ID | Clasificación | Hallazgo | Evidencia |
| --- | --- | --- | --- |
| R01 | Completo | Índice de registro secuencial, no medida explicativa. | report línea 15, STAT-002 y selección de variables |
| R02 | Completo | Códigos numéricos tratados como categorías o binarios. | plan E2/E3, STAT-003/007/008/010/011 |
| R03 | Completo | Identidad cnt y sus componentes reconocida. | STAT-003 y report líneas 25/35 |
| R04 | Completo | Normalización explícita y sin confundir unidades. | Readme.txt y report líneas 37/103 |
| R05 | Completo | 165 huecos y efecto sobre agregaciones documentados. | STAT-004, ISSUE-001 y report líneas 91–93 |
| R06 | Completo | Categoría meteorológica 4 con tres filas y advertencia. | STAT-011 y report línea 83 |
| R07 | Parcial correcto | Reconoce estructura de calendario y confusión temporal, pero no explica dependencia entre observaciones horarias. | calendar_year derivado, STAT-003 y report línea 105 |
| A01 | Adicional válido | Redundancia térmica temp–atemp. | STAT-013 y report línea 55 |
| A02 | Adicional válido | Sensibilidad a extremos válidos, sin calificarlos como errores. | STAT-014, ISSUE-002 y report línea 95 |
| A03 | Adicional válido | Agregación horaria y falta de información de mecanismos operativos limitan las explicaciones. | report línea 101 y columnas de STAT-001 |

Se identifican seis riesgos previstos y tres adicionales, sin falsas alarmas. La precisión es 1, la cobertura es 6/7 y F1 es 12/13.

`Q4 = 100 x [2 x 1 x (6 / 7)] / [1 + (6 / 7)] = 92,31`

## Q5 Calidad y profundidad del EDA: 75,00

El análisis examina distribuciones, composición, agregaciones temporales, asociaciones y extremos. Recibe 3 de 4 puntos por la contradicción en la comprobación de `season` y la ausencia de algunos resúmenes del conjunto completo.

Evidencia: STAT-006/008/009/010/012/014 y STAT-003.season_date_mismatches.

`Q5 = 100 x 3 / 4 = 75,00`

## Q6 Profundidad de la interpretación: 75,00

La interpretación relaciona los hallazgos con sus estadísticas y reconoce las limitaciones causales y los tamaños muestrales pequeños. Recibe 3 de 4 puntos porque afirma que `season` es coherente con la fecha, aunque la comprobación registra diferencias que no se explican.

Evidencia: report.md, líneas 25, 51, 55, 57, 83 y 101–109.

`Q6 = 100 x 3 / 4 = 75,00`

## Q7 Calidad de las visualizaciones: 90,00

| Objetivo | Nota 0–4 | Justificación | Evidencia |
| --- | --- | --- | --- |
| V01 | 4 | Evolución mensual 2011–2012 agregada, sin saturación. | FIG-001 y STAT-009 |
| V02 | 4 | Medias horarias de ambas condiciones, horas ordenadas y leyenda clara. | FIG-002 y STAT-010 |
| V03 | 4 | Patrón mensual correctamente ordenado y comparación anual. | FIG-001 y STAT-009 |
| V04 | 3 | Comparación meteorológica clara y n = 3 advertido en el texto. El boxplot oculta extremos sin aclararlo. | FIG-005, report línea 83 y traza evento 16, showfliers=False |
| V05 | 3 | La agregación por intervalos es válida y legible. No muestra variabilidad interna ni tamaños desiguales de los cinco grupos. | FIG-006 y STAT-012.temp_bins |

`Q7 = 100 x 18 / 20 = 90,00`

## Q8 Cobertura del informe: 79,55

| ID | Peso | Nota | Justificación | Evidencia |
| --- | --- | --- | --- | --- |
| U01 | 2 | 1 | Filas, columnas y periodo comunicados. | report líneas 3/13/91 |
| U02 | 2 | 1 | Distingue cero nulos/duplicados de los huecos horarios. | report líneas 5/23/91 |
| U03 | 2 | 1 | Nivel y dispersión con cifras correctas. | report línea 33 |
| U04 | 2 | 0 | No comunica la cuota global 81,17 %. Las proporciones por hora no expresan la proporción del conjunto completo | report línea 53 y FIG-003 |
| U05 | 2 | 0,5 | Totales de ambos años y dirección correctos, falta 64,88 %. | report líneas 49/115 |
| U06 | 2 | 0,5 | Máximo global 17 h explícito. 4 h se cita como ejemplo bajo, no se identifica como mínimo. | report línea 51, FIG-002 es perfil separado, no global |
| U07 | 2 | 1 | Los máximos de laborables 17 h y no laborables 13 h se identifican inequívocamente en la figura incorporada. | report líneas 71–73 y FIG-002 |
| U08 | 1 | 1 | Diferencias mensuales/estacionales y season 3 máxima. | report líneas 39/49 y FIG-001 |
| U09 | 2 | 1 | Peor tiempo con menor demanda y n = 3 advertido. | report línea 83 |
| U10 | 2 | 1 | Asociaciones temperatura/humedad interpretadas sin causalidad. | report líneas 55/57 |
| U11 | 2 | 1 | Identidad exacta y partición de componentes reconocidas, sin hallazgo predictivo. | report líneas 25/35 |
| U12 | 1 | 0,5 | Una ciudad y ausencia de causalidad explicadas. Falta dependencia entre observaciones. | report líneas 15/101/105 |

`Q8 = 100 x 17,5 / 22 = 79,55`

## Q9 Fidelidad del informe: 98,61

Se respaldan 142 de las 144 afirmaciones evaluadas. AF066 afirma que season es coherente con la fecha, aunque STAT-003 registra 3.922 diferencias al aplicar una regla que asigna una estación a cada mes. Esa regla no está justificada por la documentación, por lo que las diferencias no demuestran errores en los datos. El problema consiste en dar por superada una comprobación cuyo resultado queda sin explicar.

AF141 afirma que las entradas no contienen información sobre eventos externos específicos, aunque el Readme menciona Hurricane Sandy como ejemplo. Esa mención no demuestra que el huracán explique los extremos observados, pero contradice la ausencia de información que declara el informe.

El inventario situado al final de esta ficha recoge las afirmaciones revisadas, su clasificación y las evidencias utilizadas.

`Q9 = 100 x 142 / 144 = 98,61`

## Q10 Claridad y coherencia: 75,00

El informe tiene estructura clara, figuras accesibles y referencias a sus cálculos. Repite algunos hallazgos y declara coherencia de season aunque sus estadísticas registran diferencias que no explica. Se asigna 3/4 porque la incoherencia es localizada y las conclusiones principales siguen siendo comprensibles.

Evidencia: report.md y STAT-003.

`Q10 = 100 x 3 / 4 = 75,00`

## Inventario de afirmaciones

R = respaldada; C = contradicha; S = sin respaldo suficiente.

Detalle de Q9 para comprobar el recuento. Se conserva íntegro el inventario de 144 afirmaciones y sus clasificaciones. Las líneas remiten al informe original, no a esta ficha.

| ID | Líneas report | Afirmación distinta | Estado | Evidencia |
| --- | --- | --- | --- | --- |
| AF001 | 3,13,23,27,33,65,91 | Se conservan 17379 filas originales y preparadas. | R | STAT-001.rows, STAT-005 y contraste CSV |
| AF002 | 3,13,23,27 | Se conservan las 17 columnas fuente. | R | STAT-001.column_order, STAT-005 y contraste CSV |
| AF003 | 3,27 | Se añaden cinco variables derivadas. | R | STAT-005.derived_columns y contraste CSV |
| AF004 | 3,29,93,119 | No se imputaron observaciones ni valores. | R | preparation, traza eventos 16/29 y contraste CSV |
| AF005 | 3,27,29,95,119 | No se eliminaron filas, extremos o fechas incompletas. | R | STAT-005.rows_removed y contraste CSV |
| AF006 | 3,15 | Los datos son horarios agregados de Capital Bikeshare, Washington D.C. | R | Readme.txt, Data Set y Files |
| AF007 | 3,91 | El periodo empieza en 2011-01-01. | R | STAT-004.date_min |
| AF008 | 3,91 | El periodo termina en 2012-12-31. | R | STAT-004.date_max |
| AF009 | 5,23,97,113 | No hay celdas ausentes en las columnas originales. | R | STAT-002.missing_by_column y contraste fuente |
| AF010 | 5,23,97,113 | No hay filas completas duplicadas. | R | STAT-002.full_row_duplicates |
| AF011 | 5,23 | No hay duplicados de instant. | R | STAT-002.duplicate_instant |
| AF012 | 5,23 | No hay duplicados de la clave dteday y hr. | R | STAT-002.duplicate_dteday_hr |
| AF013 | 5,25,35,95,97,113 | cnt = casual + registered en todas las filas, sin fallos. | R | STAT-003.cnt_identity_failures |
| AF014 | 5,91,107,119 | Faltan 165 combinaciones fecha-hora frente a la malla completa. | R | STAT-004.slots_not_represented |
| AF015 | 5,91 | Están presentes las 731 fechas del periodo. | R | STAT-004.unique_dates y dates_absent |
| AF016 | 5,93,107,119 | Los huecos limitan la interpretación de agregaciones temporales. | R | STAT-004, ISSUE-001.potential_effect y grupos de STAT-008/009 |
| AF017 | 7,33,115 | Media de cnt = 189,46. | R | STAT-006.cnt.mean |
| AF018 | 7,33,115 | Mediana de cnt = 142. | R | STAT-006.cnt.median |
| AF019 | 7 | Mínimo de cnt = 1. | R | STAT-006.cnt.min |
| AF020 | 7,33 | Máximo de cnt = 977. | R | STAT-006.cnt.max |
| AF021 | 7,33,115 | Hay dispersión elevada y valores altos que separan media y mediana. | R | STAT-006 y FIG-004 |
| AF022 | 7,39,115 | Media de cnt en 2012 = 234,67. | R | STAT-008.by_year[2012].cnt_mean |
| AF023 | 7,39,115 | Media de cnt en 2011 = 143,79. | R | STAT-008.by_year[2011].cnt_mean |
| AF024 | 7,39,115 | La media horaria observada de 2012 supera la de 2011. | R | STAT-008.by_year |
| AF025 | 9,51,115 | La demanda se concentra más en horas diurnas. | R | STAT-008.by_hour y FIG-002 |
| AF026 | 9,53 | Los registrados tienen picos horarios especialmente en laborables. | R | STAT-010.profile y FIG-002/003 |
| AF027 | 9,53,77,117 | La composición de usuarios cambia por hora y condición laboral. | R | STAT-010.profile y FIG-003 |
| AF028 | 9,83,115 | Las categorías meteorológicas más severas tienen medias de cnt menores. | R | STAT-011.by_weathersit |
| AF029 | 9,17,51,55,71,105,117 | El análisis es descriptivo y bivariado, no identifica efectos causales independientes. | R | Métodos STAT-008/010/012 y código registrado |
| AF030 | 13 | cnt representa el total de alquileres. | R | Readme.txt, Dataset characteristics |
| AF031 | 13 | casual cuenta alquileres de usuarios no registrados | R | Readme.txt, Dataset characteristics |
| AF032 | 13 | registered cuenta alquileres de usuarios registrados | R | Readme.txt, Dataset characteristics |
| AF033 | 13,15 | La tabla contiene variables de calendario y meteorología. | R | STAT-001.column_order y Readme.txt |
| AF034 | 15 | dteday registra la fecha. | R | Readme.txt y STAT-001.column_order |
| AF035 | 15 | hr registra la hora. | R | Readme.txt y STAT-001.column_order |
| AF036 | 15,23 | instant es el índice del registro. | R | Readme.txt y STAT-002 |
| AF037 | 17 | No se entrenaron modelos predictivos. | R | Análisis STAT-001 a STAT-014 y operaciones de traza |
| AF038 | 21 | season tiene 4 códigos distintos. | R | STAT-003.observed_codes.season |
| AF039 | 21 | weathersit tiene 4 códigos distintos. | R | STAT-003.observed_codes.weathersit |
| AF040 | 21 | yr tiene 2 códigos distintos. | R | STAT-003.observed_codes.yr |
| AF041 | 21 | holiday tiene 2 códigos distintos. | R | STAT-003.observed_codes.holiday |
| AF042 | 21 | workingday tiene 2 códigos distintos. | R | STAT-003.observed_codes.workingday |
| AF043 | 21 | mnth tiene 12 códigos distintos. | R | STAT-003.observed_codes.mnth |
| AF044 | 21 | hr tiene 24 códigos distintos. | R | STAT-003.observed_codes.hr |
| AF045 | 21 | El CSV se cargó correctamente. | R | STAT-001, archivo preparado y traza |
| AF046 | 23 | instant es secuencial de 1 a 17379. | R | STAT-002.instant_values_matching_1_to_n |
| AF047 | 25,97,113 | Los códigos de season pertenecen al dominio documentado. | R | STAT-003.observed_codes.season y Readme.txt |
| AF048 | 25,97,113 | Los códigos de yr pertenecen al dominio documentado. | R | STAT-003.observed_codes.yr y Readme.txt |
| AF049 | 25,97,113 | Los códigos de mnth pertenecen al dominio documentado. | R | STAT-003.observed_codes.mnth y Readme.txt |
| AF050 | 25,97,113 | Los códigos de hr pertenecen al dominio documentado. | R | STAT-003.observed_codes.hr y Readme.txt |
| AF051 | 25,97,113 | Los códigos de holiday pertenecen al dominio documentado. | R | STAT-003.observed_codes.holiday y Readme.txt |
| AF052 | 25,97,113 | Los códigos de weekday pertenecen al dominio documentado. | R | STAT-003.observed_codes.weekday y Readme.txt |
| AF053 | 25,97,113 | Los códigos de workingday pertenecen al dominio documentado. | R | STAT-003.observed_codes.workingday y Readme.txt |
| AF054 | 25,97,113 | Los códigos de weathersit pertenecen al dominio documentado. | R | STAT-003.observed_codes.weathersit y Readme.txt |
| AF055 | 25 | temp cumple el rango normalizado comprobado. | R | STAT-003.out_of_documented_range.temp |
| AF056 | 25 | atemp cumple el rango normalizado comprobado. | R | STAT-003.out_of_documented_range.atemp |
| AF057 | 25 | hum cumple el rango normalizado comprobado. | R | STAT-003.out_of_documented_range.hum |
| AF058 | 25 | windspeed cumple el rango normalizado comprobado. | R | STAT-003.out_of_documented_range.windspeed |
| AF059 | 25,95 | Los recuentos de cnt son no negativos. | R | STAT-003.out_of_documented_range.cnt |
| AF060 | 25,95 | Los recuentos de casual son no negativos. | R | STAT-003.out_of_documented_range.casual |
| AF061 | 25,95 | Los recuentos de registered son no negativos. | R | STAT-003.out_of_documented_range.registered |
| AF062 | 25 | yr cumple la regla temporal comprobada. | R | STAT-003 y contraste independiente |
| AF063 | 25 | mnth cumple la regla temporal comprobada. | R | STAT-003 y contraste independiente |
| AF064 | 25 | weekday cumple la regla temporal comprobada. | R | STAT-003 y contraste independiente |
| AF065 | 25 | workingday cumple la regla temporal comprobada. | R | STAT-003 y contraste independiente |
| AF066 | 25 | season es coherente con la fecha bajo la regla comprobada. | C | STAT-003.season_date_mismatches = 3922, interpretación de STAT-003 y CHK-003 incoherentes |
| AF067 | 27 | La copia preparada se creó separada del original. | R | prepared_data.csv y preparation |
| AF068 | 27 | dteday se convirtió a fecha para los cálculos. | R | Traza evento 16, pd.to_datetime |
| AF069 | 27 | dteday se serializó como fecha ISO YYYY-MM-DD. | R | Traza evento 16 y prepared_data.csv |
| AF070 | 27 | La copia añade calendar_year. | R | STAT-005.derived_columns y prepared_data.csv |
| AF071 | 27 | La copia añade season_label. | R | STAT-005.derived_columns y prepared_data.csv |
| AF072 | 27 | La copia añade weathersit_label. | R | STAT-005.derived_columns y prepared_data.csv |
| AF073 | 27 | La copia añade casual_share. | R | STAT-005.derived_columns y prepared_data.csv |
| AF074 | 27 | La copia añade registered_share. | R | STAT-005.derived_columns y prepared_data.csv |
| AF075 | 27 | Las proporciones derivadas no tienen ausencias. | R | STAT-005.share_missing_due_to_zero_cnt y contraste CSV |
| AF076 | 27 | No existen filas con cnt = 0. | R | STAT-006.cnt.min = 1 y fuente |
| AF077 | 29,95 | Los extremos conservados no demuestran errores por sí solos. | R | STAT-003, STAT-014 e ISSUE-002 |
| AF078 | 33 | Desviación típica de cnt = 181,39. | R | STAT-006.cnt.std |
| AF079 | 33,95 | Primer cuartil de cnt = 40. | R | STAT-006.cnt.q1 y STAT-014.cnt_q1 |
| AF080 | 33,95 | Tercer cuartil de cnt = 281. | R | STAT-006.cnt.q3 y STAT-014.cnt_q3 |
| AF081 | 35 | mean de casual = 35,68. | R | STAT-006.casual.mean |
| AF082 | 35 | median de casual = 17. | R | STAT-006.casual.median |
| AF083 | 35 | mean de registered = 153,79. | R | STAT-006.registered.mean |
| AF084 | 35 | median de registered = 115. | R | STAT-006.registered.median |
| AF085 | 35 | max de casual = 367. | R | STAT-006.casual.max |
| AF086 | 35 | max de registered = 886. | R | STAT-006.registered.max |
| AF087 | 35 | La composición es una partición consistente del total. | R | STAT-003.cnt_identity_failures y STAT-010 |
| AF088 | 37,103 | Las variables meteorológicas se mantienen en escala normalizada. | R | prepared_data.csv, preparation y Readme.txt |
| AF089 | 37 | Media de temp = 0,497. | R | STAT-006.temp.mean |
| AF090 | 37 | Media de atemp = 0,476. | R | STAT-006.atemp.mean |
| AF091 | 37 | Media de hum = 0,627. | R | STAT-006.hum.mean |
| AF092 | 37 | Media de windspeed = 0,190. | R | STAT-006.windspeed.mean |
| AF093 | 39 | La menor media entre temporadas corresponde a season = 1. | R | STAT-008.by_season |
| AF094 | 39 | Media de cnt para season = 1 = 111,11. | R | STAT-008.by_season[1].cnt_mean |
| AF095 | 39,115 | La mayor media entre temporadas corresponde a season = 3. | R | STAT-008.by_season |
| AF096 | 39 | Media de cnt para season = 3 = 236,02. | R | STAT-008.by_season[3].cnt_mean |
| AF097 | 39 | Los tamaños de los grupos estacionales no son iguales. | R | STAT-008.by_season.n_hours |
| AF098 | 41 | El histograma incluye referencias de media y mediana. | R | FIG-004 abierta y código de traza |
| AF099 | 49,65 | La agregación mensual utiliza año calendario y mes. | R | STAT-009.monthly_totals y código de traza |
| AF100 | 49 | Total de alquileres en 2011 = 1243103. | R | STAT-008.by_year[2011].cnt_sum |
| AF101 | 49 | Total de alquileres en 2012 = 2049576. | R | STAT-008.by_year[2012].cnt_sum |
| AF102 | 49 | La variación mensual es relevante y la diferencia anual no es uniforme. | R | STAT-009.monthly_totals y FIG-001 |
| AF103 | 51 | Media de cnt a las 4 h = 6,35. | R | STAT-008.by_hour[4].cnt_mean |
| AF104 | 51,115 | La media global máxima ocurre a las 17 h. | R | STAT-008.by_hour |
| AF105 | 51 | La media global de cnt a las 17 h = 461,45. | R | STAT-008.by_hour[17].cnt_mean |
| AF106 | 51,71,115 | Los perfiles horarios laborable y no laborable tienen formas diferentes. | R | STAT-010.profile y FIG-002 |
| AF107 | 53 | La cuota de registrados es alta en franjas de picos laborables. | R | STAT-010.profile y FIG-003 |
| AF108 | 53 | Las cuotas agrupadas son razones de sumas, no medias de porcentajes individuales. | R | Código evento 16 y contraste STAT-010.profile |
| AF109 | 55,117 | Spearman de temp con cnt = 0,423. | R | STAT-012.spearman_with_cnt.temp |
| AF110 | 55,117 | Spearman de atemp con cnt = 0,423. | R | STAT-012.spearman_with_cnt.atemp |
| AF111 | 55,117 | Spearman de hum con cnt = −0,360. | R | STAT-012.spearman_with_cnt.hum |
| AF112 | 55,117 | Spearman de windspeed con cnt = 0,127. | R | STAT-012.spearman_with_cnt.windspeed |
| AF113 | 55 | temp y atemp presentan una asociación muy alta. | R | STAT-013.spearman_temp_atemp = 0,9896 |
| AF114 | 55 | temp y atemp aportan información parcialmente redundante. | R | STAT-013 y definición meteorológica, no es dependencia temporal |
| AF115 | 57 | Media de cnt en temp hasta 0,2 = 65,07. | R | STAT-012.temp_bins[0].cnt_mean |
| AF116 | 57 | Media de cnt en temp superior a 0,8 = 326,28. | R | STAT-012.temp_bins[4].cnt_mean |
| AF117 | 57 | La media de cnt aumenta entre los cinco intervalos de temperatura. | R | STAT-012.temp_bins y FIG-006 |
| AF118 | 57,105 | Calendario y horario pueden contribuir a las asociaciones observadas. | R | STAT-008/010/012 y limitación bivariada, posibilidad explícita no causa probada |
| AF119 | 65 | La agregación mensual reduce la saturación de la serie horaria. | R | FIG-001, 24 puntos de meses frente a 17379 filas |
| AF120 | 83 | Media de cnt con weathersit = 1: 204,87. | R | STAT-011.by_weathersit[1].cnt_mean |
| AF121 | 83 | Número de horas con weathersit = 1: 11413. | R | STAT-011.by_weathersit[1].n_hours |
| AF122 | 83 | Media de cnt con weathersit = 2: 175,17. | R | STAT-011.by_weathersit[2].cnt_mean |
| AF123 | 83 | Número de horas con weathersit = 2: 4544. | R | STAT-011.by_weathersit[2].n_hours |
| AF124 | 83 | Media de cnt con weathersit = 3: 111,58. | R | STAT-011.by_weathersit[3].cnt_mean |
| AF125 | 83 | Número de horas con weathersit = 3: 1419. | R | STAT-011.by_weathersit[3].n_hours |
| AF126 | 83 | Media de cnt con weathersit = 4: 74,33. | R | STAT-011.by_weathersit[4].cnt_mean |
| AF127 | 83 | Número de horas con weathersit = 4: 3. | R | STAT-011.by_weathersit[4].n_hours |
| AF128 | 83 | La categoría meteorológica 4 es demasiado pequeña para generalizar. | R | STAT-011.by_weathersit[4].n_hours = 3 y advertencia explícita |
| AF129 | 91 | La malla teórica de 24 horas por fecha contiene 17544 franjas. | R | STAT-004.expected_24h_slots |
| AF130 | 93,107,119 | La documentación y el CSV no permiten atribuir un mecanismo a los huecos. | R | Readme.txt, columnas fuente e ISSUE-001.uncertainty |
| AF131 | 95 | La regla de Tukey 1,5xIQR identifica 505 extremos de cnt. | R | STAT-014.hourly_outlier_count y contraste independiente |
| AF132 | 95 | Se acompañan los extremos de mediana y cuartiles. | R | STAT-006, report líneas 33/95 y FIG-004 |
| AF133 | 101 | No hay información de estación física en las entradas. | R | Readme.txt y STAT-001.column_order |
| AF134 | 101 | No hay información de trayecto en las entradas. | R | Readme.txt y STAT-001.column_order |
| AF135 | 101 | No hay información de capacidad en las entradas. | R | Readme.txt y STAT-001.column_order |
| AF136 | 101 | No hay información de disponibilidad en las entradas. | R | Readme.txt y STAT-001.column_order |
| AF137 | 101 | No hay información de mantenimiento en las entradas. | R | Readme.txt y STAT-001.column_order |
| AF138 | 101 | No hay información de operaciones del sistema en las entradas. | R | Readme.txt y STAT-001.column_order |
| AF139 | 101 | El dataset agregado no permite explicar por sí solo los cambios de demanda. | R | Unidad horaria y ausencia de información de mecanismos, STAT-001 |
| AF140 | 103 | No se comunicaron magnitudes meteorológicas físicas sin conversión. | R | Report completo y CSV fuente/preparado, escalas normalizadas |
| AF141 | 109 | Las entradas no incluyen información de eventos externos específicos. | C | Readme, Event and Anomaly Detection, menciona una fecha y Hurricane Sandy. La ausencia absoluta de información es falsa |
| AF142 | 109 | No se atribuyeron los extremos a eventos externos. | R | Report completo e ISSUE-002 |
| AF143 | 115 | Hay diferencias de demanda por condición laboral. | R | STAT-008.by_workingday y STAT-010 |
| AF144 | 119 | Las transformaciones de la copia están documentadas. | R | preparation.changes, STAT-005 y traza |
