# Evaluación D1-LG-R2

**Índice final:** 89,13/100.  
**Evaluación cerrada:** 6 de octubre de 2026.  
**Ejecución:** `D1_bike_sharing__langgraph__r02__20260831T180229010000Z`

**Criterios:** [Protocolo de evaluación](../01_protocolo_calidad_Q1_Q10_v0.1.md) y [guía D1](../02_ficha_D1_bike_sharing.md).  
**Resultados:** [Archivos originales de la ejecución](../../../outputs/experimento/D1_bike_sharing__langgraph__r02__20260831T180229010000Z).  
**Evaluación:** [Excel de puntuaciones](../Evaluacion_calidad.xlsx) y [JSON de comprobaciones](D1-LG-R2_comprobaciones.json).

Las referencias `STAT`, `ISSUE` y `FIG` identifican análisis, problemas y figuras en los archivos de la ejecución. Las referencias a líneas corresponden a su informe original, `report.md`.

## Resumen

| Métrica | Puntuación final |
| --- | ---: |
| Q1 Cumplimiento de las etapas | 100,00 |
| Q2 Corrección numérica | 88,57 |
| Q3 Validez del tratamiento de los datos | 100,00 |
| Q4 Detección de problemas y riesgos | 92,31 |
| Q5 Calidad y profundidad del EDA | 75,00 |
| Q6 Profundidad de la interpretación | 75,00 |
| Q7 Calidad de las visualizaciones | 95,00 |
| Q8 Cobertura del informe | 84,09 |
| Q9 Fidelidad del informe | 99,54 |
| Q10 Claridad y coherencia | 75,00 |

## Q1 Cumplimiento de las etapas: 100,00

Completa las ocho etapas con resultados utilizables y coherentes. La marca temporal guardada conserva fecha y hora.

| Etapa | Puntos | Evidencia |
| --- | --- | --- |
| E1 Carga e inspección inicial | 1 | STAT-001 y profile |
| E2 Estructura, tipos y calidad | 1 | STAT-002 a STAT-005 |
| E3 Preparación y decisiones de análisis | 1 | TR-001 a TR-005, STAT-006 y CSV |
| E4 Estadística descriptiva | 1 | STAT-007/008/013 |
| E5 Variables, agregaciones y relaciones | 1 | STAT-009 a STAT-012 |
| E6 Visualizaciones | 1 | FIG-001 a FIG-005, abiertas y contrastadas |
| E7 Problemas, riesgos y anomalías | 1 | ISSUE-001/002, report 94–112 |
| E8 Informe final | 1 | Informe final estructurado y con enlaces a las figuras |

Q1 = 100 x 8 / 8 = 100,00

## Q2 Corrección numérica: 88,57

| Control | Producido | Referencia | Estado | Puntos | Evidencia |
| --- | --- | --- | --- | --- | --- |
| C01 Número de filas | 17.379 | 17.379 | correcta | 2/2 | STAT-001.rows |
| C02 Número de columnas | 17 | 17 | correcta | 2/2 | STAT-001.columns |
| C03 Fechas distintas | 731 | 731 | correcta | 1/1 | STAT-001.unique_dates |
| C04 Celdas ausentes | 0 | 0 | correcta | 2/2 | STAT-002.missing_by_column |
| C05 Filas duplicadas | 0 | 0 | correcta | 2/2 | STAT-002.full_row_duplicates |
| C06 Huecos en la secuencia horaria | 165 | 165 | correcta | 1/1 | STAT-003.missing_hour_slots |
| C07 Alquileres totales | 3.292.679 | 3.292.679 | correcta | 2/2 | STAT-013.total_cnt |
| C08 Media horaria de alquileres | 189,463088 | 189,463088 | correcta | 2/2 | STAT-007.cnt.mean |
| C09 Mediana horaria de alquileres | 142 | 142 | correcta | 1/1 | STAT-007.cnt.median |
| C10 Desviación típica muestral | 181,387599 | 181,387599 | correcta | 1/1 | STAT-007.cnt.std |
| C11 Máximo horario | 977 | 977 | correcta | 1/1 | STAT-007.cnt.max |
| C12 Total de alquileres de usuarios ocasionales | 620.017 | 620.017 | correcta | 1/1 | STAT-013.total_casual |
| C13 Total de alquileres de usuarios registrados | 2.672.662 | 2.672.662 | correcta | 1/1 | STAT-013.total_registered |
| C14 Proporción de alquileres de usuarios registrados sobre el total | 0,811698 | 0,811698 | correcta | 1/1 | STAT-013.registered_share_of_total |
| C15 Alquileres totales en 2011 | 1.243.103 | 1.243.103 | correcta | 1/1 | STAT-009.by_year[yr=0].cnt_sum |
| C16 Alquileres totales en 2012 | 2.049.576 | 2.049.576 | correcta | 1/1 | STAT-009.by_year[yr=1].cnt_sum |
| C17 Variación total de 2012 respecto a 2011 | No producido | 64,875799 | ausente | 0/2 | Variación porcentual anual no producida |
| C18 Hora con mayor media | Categoría 17, 461,452055 | 461,452055 | correcta | 2/2 | STAT-011.by_hour[hr=17].cnt_mean |
| C19 Hora con menor media | Categoría 4, 6,352941 | 6,352941 | correcta | 1/1 | STAT-011.by_hour[hr=4].cnt_mean |
| C20 Temporada con mayor media | Categoría 3, 236,016237 | 236,016237 | correcta | 1/1 | STAT-009.by_season[season=3].cnt_mean |
| C21 Media con tiempo despejado | Categoría 1, 204,869272 | 204,869272 | correcta | 1/1 | STAT-009.by_weather[weathersit=1].cnt_mean |
| C22 Media con tiempo adverso de categoría 3 | Categoría 3, 111,579281 | 111,579281 | correcta | 1/1 | STAT-009.by_weather[weathersit=3].cnt_mean |
| C23 Observaciones meteorológicas de categoría 4 | 3 | 3 | correcta | 1/1 | STAT-009.by_weather[weathersit=4].records |
| C24 Correlación de Pearson entre temperatura y cnt | No producido | 0,404772 | ausente | 0/1 | Solo Spearman, Pearson no producido |
| C25 Correlación de Pearson entre humedad y cnt | No producido | -0,322911 | ausente | 0/1 | Solo Spearman, Pearson no producido |
| C26 Inconsistencias en cnt = casual + registered | 0 | 0 | correcta | 2/2 | STAT-004.identity_cnt_equals_components_violations |

Se consideran correctas 23 comprobaciones y permanecen ausentes C17, C24 y C25. Estas dos últimas exigen Pearson, mientras que la ejecución presenta Spearman.

`Q2 = 100 x 31 / 35 = 88,57`

## Q3 Validez del tratamiento de los datos: 100,00

Las ocho decisiones son válidas. Conserva fuente, códigos y escalas. timestamp, etiquetas y casual_share se corresponden con sus columnas de origen.

| Decisión | Puntos | Evidencia |
| --- | --- | --- |
| D01 Fecha-hora correcta | 1 | CSV timestamp válido en las 17379 filas, TR-001/002 |
| D02 Categorías como grupos | 1 | Códigos intactos, TR-003 y agrupaciones STAT-009/011 |
| D03 instant solo identificador | 1 | Plan supuestos y report 15, no análisis explicativo de instant |
| D04 Sin limpieza innecesaria | 1 | TR-005, cero nulos/duplicados y fuente conservada |
| D05 No imputar huecos | 1 | ISSUE-001 y report 25/96 |
| D06 Extremos conservados | 1 | ISSUE-002 y CSV sin eliminación |
| D07 Identidad preservada sin evidencia independiente | 1 | STAT-004/013 y report 5/33, no interpretar correlaciones con componentes como descubrimiento independiente |
| D08 Escalas conservadas | 1 | CSV y report 46, no conversión no documentada |

`Q3 = 100 x 8 / 8 = 100,00`

## Q4 Detección de problemas y riesgos: 92,31

Seis riesgos previstos completos y tres adicionales válidos, sin falsas alarmas. Comprueba calendario, pero no aborda dependencia entre registros sucesivos, de modo que R07 queda parcial.

| Riesgo | Clasificación | Evidencia |
| --- | --- | --- |
| R01 Identificador secuencial | completo | Plan supuestos y report 15, instant sin uso explicativo |
| R02 Códigos categóricos | completo | STAT-004/008/009/011 y TR-003 |
| R03 Identidad cnt=casual+registered | completo | STAT-004/013 y report 5/33, componentes como composición |
| R04 Meteorología normalizada | completo | STAT-004 y report 46/108 |
| R05 165 huecos horarios | completo | STAT-003, ISSUE-001, report 96 |
| R06 Meteorología4 n=3 | completo | STAT-008/009 y report 68/112 |
| R07 Dependencia y derivación temporal | parcial | STAT-004 comprueba calendario. No se desarrolla dependencia entre observaciones sucesivas en plan, estadísticas, issues o report |
| A01 Redundancia temp-atemp | adicional válido | STAT-012 Spearman 0,989633 y report 70 |
| A02 Influencia de extremos válidos | adicional válido | STAT-005, ISSUE-002 y report 98 |
| A03 Límites de datos agregados e información individual | adicional válido | Profile, plan riesgos y report 104 |

**Cálculo:** K=6, A=3, F=0. Precisión=9/9. Cobertura=6/7. F1=12/13.

`Q4 = 100 x [2 x 1 x (6 / 7)] / [1 + (6 / 7)] = 92,31`

## Q5 Calidad y profundidad del EDA: 75,00

Nivel 3/4. EDA amplio y correcto, con distribuciones, grupos, asociaciones y extremos. Falta desarrollar la dependencia temporal y trasladar el perfil global calculado a la síntesis de hallazgos.

`Q5 = 100 x 3 / 4 = 75,00`

**Evidencia:** STAT-007 a STAT-013, report 38–70 y cinco figuras.

## Q6 Profundidad de la interpretación: 75,00

Nivel 3/4. Interpreta con prudencia cobertura, tamaños y límites causales. La frase máximo más tardío a las 13 h resulta ambigua tras citar el máximo laboral a las 17 h, lo que impide valorar la integración como plenamente coherente.

`Q6 = 100 x 3 / 4 = 75,00`

**Evidencia:** Report 54/58/62/68/70/96–112, STAT-011 y FIG-002. Las cifras de los máximos son correctas. La comparación sería válida frente al pico de las 8 h, pero no frente al máximo de las 17 h. El texto no establece el comparador. Se asigna nivel 3 por ese defecto localizado, manteniendo el reconocimiento de la interpretación prudente del resto.

## Q7 Calidad de las visualizaciones: 95,00

Se abren las cinco imágenes finales y se contrastan datos y operaciones gráficas de la traza. Se puntúan objetivos, no cantidad de PNG.

| Objetivo | Puntos de 4 | Evidencia y decisión |
| --- | --- | --- |
| V01 Evolución 2011–2012 | 4 | FIG-001 y línea 74 del informe. Serie diaria legible, con ejes y título claros y advertencia sobre la cobertura temporal. |
| V02 Perfil horario por tipo de día | 4 | FIG-002 y report 9/62/78. Dos curvas, horas completas y máximos correctos. La ambigüedad verbal de más tardío se valora en Q6/Q9/Q10, no altera el gráfico |
| V03 Patrón mensual o estacional | 3 | FIG-001 permite ver los ciclos intraanuales y report 56 compara estaciones. No hay representación categórica ni explicación del patrón estacional concreto visible en la serie. |
| V04 Meteorología y n reducido | 4 | FIG-004, report 68/86/112. Boxplot y n=3 comunicado en texto. La omisión visual de atípicos se explica y se complementa con histograma y cifras IQR |
| V05 Relación densa con temperatura/humedad | 4 | FIG-005 y report 90. Dispersión con transparencia 0,22, tamaño 10, color de humedad, escalas originales y explicación de heterogeneidad |

`Q7 = 100 x 19 / 20 = 95,00`

## Q8 Cobertura del informe: 84,09

| Contenido | Peso | Crédito | Puntos | Evidencia |
| --- | --- | --- | --- | --- |
| U01 Dimensiones y periodo | 2 | 1 | 2 | Report 3/15 |
| U02 Nulos, duplicados y huecos | 2 | 1 | 2 | Report 5/29/30/96 |
| U03 Nivel y dispersión cnt | 2 | 1 | 2 | Report 7/38 |
| U04 Proporción global registered | 2 | 1 | 2 | Report 7/44/118 |
| U05 Totales anuales y aumento 64,88% | 2 | 0,5 | 1 | Report 54 muestra ambos totales y medias, no la variación porcentual |
| U06 Máximo y mínimo medios globales por hora | 2 | 0 | 0 | STAT-011.by_hour los contiene, pero no se comunican en report ni FIG-002, que es segmentada |
| U07 Máximos 17h laborales y 13h no laborales | 2 | 1 | 2 | Report 9/62 y FIG-002, categorías y medias correctas. Más tardío no modifica las dos categorías exigidas y se registra en Q9 |
| U08 Diferencias estacionales y máximo season3 | 1 | 1 | 1 | Report 56 presenta las cuatro medias y deja identificable la mayor, fall=3. Presentación equivalente |
| U09 Meteorología y categoría4 n=3 | 2 | 1 | 2 | Report 68/112 |
| U10 Temperatura y humedad, prudencia | 2 | 1 | 2 | Report 70/90/110 |
| U11 Identidad no predictiva | 2 | 1 | 2 | Report 5/33, alcance descriptivo y composición, no presentar la suma como descubrimiento predictivo |
| U12 Dependencia, una ciudad y no causalidad | 1 | 0,5 | 0,5 | Report 13/110 identifica ciudad y límite causal. Falta dependencia entre registros horarios, confusión calendario no la sustituye |

`Q8 = 100 x 18,5 / 22 = 84,09`

## Q9 Fidelidad del informe: 99,54

Se respaldan 216 de las 217 afirmaciones revisadas. AF155 se clasifica como contradicha y no hay afirmaciones sin respaldo suficiente.

La frase "el máximo es más tardío" sitúa el máximo no laboral a las 13 h tras citar el máximo laboral a las 17 h. Se clasifica como contradicha respecto al máximo inmediatamente anterior. Las 13 h serían posteriores al pico de las 8 h, pero ese no es el comparador establecido por el texto. Las dos cifras de los máximos son correctas.

`Q9 = 100 x 216 / 217 = 99,54`

El apartado 'Anexo Q9' recoge las afirmaciones revisadas del informe, incluidas las figuras, las limitaciones y las conclusiones, junto con su clasificación y las evidencias utilizadas.

## Q10 Claridad y coherencia: 75,00

Nivel 3/4. Informe ordenado con referencias y figuras integradas. La ambigüedad de más tardío y algunas etiquetas inglesas limitan la claridad plena, sin impedir entender el conjunto.

`Q10 = 100 x 3 / 4 = 75,00`

**Evidencia:** Report, en especial 15/56/62/68 y enlaces FIG-001 a FIG-005.

## Anexo Q9: inventario completo de afirmaciones

Los localizadores corresponden a las líneas del informe original. R significa afirmación respaldada y C, afirmación contradicha.

| ID | Línea | Afirmación | Estado | Evidencia |
| --- | --- | --- | --- | --- |
| AF001 | 3 | 17379 registros horarios | R | STAT-001 y documentación Readme |
| AF002 | 3 | Inicio 2011-01-01 | R | STAT-001 y documentación Readme |
| AF003 | 3 | Fin 2012-12-31 | R | STAT-001 y documentación Readme |
| AF004 | 3 | Agregados horarios de Capital Bikeshare | R | STAT-001 y documentación Readme |
| AF005 | 3 | Contiene variables de calendario | R | STAT-001 y documentación Readme |
| AF006 | 3 | Contiene condiciones meteorológicas normalizadas | R | STAT-001 y documentación Readme |
| AF007 | 3 | Contiene casual, registered y cnt | R | STAT-001 y documentación Readme |
| AF008 | 5 | Cero valores ausentes en columnas fuente | R | STAT-002/003/004, ISSUE-001 |
| AF009 | 5 | Cero filas duplicadas | R | STAT-002/003/004, ISSUE-001 |
| AF010 | 5 | Cero instant repetidos | R | STAT-002/003/004, ISSUE-001 |
| AF011 | 5 | Cero claves fecha-hora repetidas | R | STAT-002/003/004, ISSUE-001 |
| AF012 | 5 | Cero incumplimientos de cnt=casual+registered | R | STAT-002/003/004, ISSUE-001 |
| AF013 | 5 | 165 huecos horarios teóricos | R | STAT-002/003/004, ISSUE-001 |
| AF014 | 5 | 76 fechas con menos de 24 observaciones | R | STAT-002/003/004, ISSUE-001 |
| AF015 | 5 | Cobertura desigual limita interpretar sumas como totales de horas completas | R | STAT-002/003/004, ISSUE-001 |
| AF016 | 7 | Media cnt 189,5 | R | STAT-007/009/013 |
| AF017 | 7 | Mediana cnt 142 | R | STAT-007/009/013 |
| AF018 | 7 | Desviación típica cnt 181,4 | R | STAT-007/009/013 |
| AF019 | 7 | Máximo cnt 977 | R | STAT-007/009/013 |
| AF020 | 7 | Registered representa 81,2% del total acumulado | R | STAT-007/009/013 |
| AF021 | 7 | Casual representa 18,8% del total acumulado | R | STAT-007/009/013 |
| AF022 | 7 | Media cnt 2012 234,7 | R | STAT-007/009/013 |
| AF023 | 7 | Media cnt 2011 143,8 | R | STAT-007/009/013 |
| AF024 | 7 | Media cnt mayor en 2012 que en 2011 | R | STAT-007/009/013 |
| AF025 | 9 | Perfiles horarios difieren por workingday | R | STAT-011/009 y FIG-002 |
| AF026 | 9 | Máximo medio laboral a las 17 h | R | STAT-011/009 y FIG-002 |
| AF027 | 9 | Máximo medio laboral 525,3 | R | STAT-011/009 y FIG-002 |
| AF028 | 9 | Máximo medio no laboral a las 13 h | R | STAT-011/009 y FIG-002 |
| AF029 | 9 | Máximo medio no laboral 372,7 | R | STAT-011/009 y FIG-002 |
| AF030 | 9 | Media meteorología 1 204,9 | R | STAT-011/009 y FIG-002 |
| AF031 | 9 | Media meteorología 2 175,2 | R | STAT-011/009 y FIG-002 |
| AF032 | 9 | Media meteorología 3 111,6 | R | STAT-011/009 y FIG-002 |
| AF033 | 13 | CSV corresponde al archivo horario del Bike Sharing Dataset | R | STAT-001, columnas CSV y Readme |
| AF034 | 13 | Sistema de Washington D.C. | R | STAT-001, columnas CSV y Readme |
| AF035 | 13 | No son viajes individuales | R | STAT-001, columnas CSV y Readme |
| AF036 | 13 | No contiene estaciones | R | STAT-001, columnas CSV y Readme |
| AF037 | 13 | No contiene trayectos | R | STAT-001, columnas CSV y Readme |
| AF038 | 13 | No identifica usuarios únicos | R | STAT-001, columnas CSV y Readme |
| AF039 | 15 | Fuente tiene 17 columnas | R | STAT-001, columnas fuente y Readme |
| AF040 | 15 | instant es identificador | R | STAT-001, columnas fuente y Readme |
| AF041 | 15 | dteday es fecha | R | STAT-001, columnas fuente y Readme |
| AF042 | 15 | season es calendario | R | STAT-001, columnas fuente y Readme |
| AF043 | 15 | yr es calendario | R | STAT-001, columnas fuente y Readme |
| AF044 | 15 | mnth es calendario | R | STAT-001, columnas fuente y Readme |
| AF045 | 15 | hr es calendario | R | STAT-001, columnas fuente y Readme |
| AF046 | 15 | holiday es calendario | R | STAT-001, columnas fuente y Readme |
| AF047 | 15 | weekday es calendario | R | STAT-001, columnas fuente y Readme |
| AF048 | 15 | workingday es calendario | R | STAT-001, columnas fuente y Readme |
| AF049 | 15 | weathersit es condición meteorológica | R | STAT-001, columnas fuente y Readme |
| AF050 | 15 | temp está normalizada | R | STAT-001, columnas fuente y Readme |
| AF051 | 15 | atemp está normalizada | R | STAT-001, columnas fuente y Readme |
| AF052 | 15 | hum está normalizada | R | STAT-001, columnas fuente y Readme |
| AF053 | 15 | windspeed está normalizada | R | STAT-001, columnas fuente y Readme |
| AF054 | 15 | casual es un recuento | R | STAT-001, columnas fuente y Readme |
| AF055 | 15 | registered es un recuento | R | STAT-001, columnas fuente y Readme |
| AF056 | 15 | cnt es un recuento | R | STAT-001, columnas fuente y Readme |
| AF057 | 17 | Se examinó estructura | R | STAT-001 a STAT-013, figuras y código registrado en traza |
| AF058 | 17 | Se examinó calidad | R | STAT-001 a STAT-013, figuras y código registrado en traza |
| AF059 | 17 | Se examinaron distribuciones | R | STAT-001 a STAT-013, figuras y código registrado en traza |
| AF060 | 17 | Se realizaron agregaciones temporales | R | STAT-001 a STAT-013, figuras y código registrado en traza |
| AF061 | 17 | Se examinaron perfiles horarios | R | STAT-001 a STAT-013, figuras y código registrado en traza |
| AF062 | 17 | Se examinó composición | R | STAT-001 a STAT-013, figuras y código registrado en traza |
| AF063 | 17 | Se calcularon asociaciones bivariadas | R | STAT-001 a STAT-013, figuras y código registrado en traza |
| AF064 | 17 | No se entrenaron modelos predictivos | R | STAT-001 a STAT-013, figuras y código registrado en traza |
| AF065 | 17 | No se realizó estimación causal | R | STAT-001 a STAT-013, figuras y código registrado en traza |
| AF066 | 21 | dteday validada ISO sin fallos | R | STAT-006, preparación TR-001 a TR-004 y contraste CSV |
| AF067 | 21 | Se conservan todas las filas originales | R | STAT-006, preparación TR-001 a TR-004 y contraste CSV |
| AF068 | 21 | Se añaden cuatro columnas | R | STAT-006, preparación TR-001 a TR-004 y contraste CSV |
| AF069 | 21 | timestamp corresponde a fecha más hora | R | STAT-006, preparación TR-001 a TR-004 y contraste CSV |
| AF070 | 21 | Se añade season_label | R | STAT-006, preparación TR-001 a TR-004 y contraste CSV |
| AF071 | 21 | Se añade weathersit_label | R | STAT-006, preparación TR-001 a TR-004 y contraste CSV |
| AF072 | 21 | Se añade casual_share | R | STAT-006, preparación TR-001 a TR-004 y contraste CSV |
| AF073 | 21 | Copia preparada tiene 21 columnas | R | STAT-006, preparación TR-001 a TR-004 y contraste CSV |
| AF074 | 23 | Etiquetas season respaldadas por códigos documentados | R | TR-003/004, CSV y Readme |
| AF075 | 23 | Etiquetas weathersit respaldadas por códigos documentados | R | TR-003/004, CSV y Readme |
| AF076 | 23 | Las etiquetas no reemplazan los códigos originales | R | TR-003/004, CSV y Readme |
| AF077 | 23 | casual_share es casual/cnt | R | TR-003/004, CSV y Readme |
| AF078 | 23 | casual_share no contiene ausencias | R | TR-003/004, CSV y Readme |
| AF079 | 23 | Mínimo cnt es 1 | R | TR-003/004, CSV y Readme |
| AF080 | 25 | No se eliminan filas | R | TR-005, STAT-005, ISSUE-001/002 y contraste CSV |
| AF081 | 25 | No se imputan horas | R | TR-005, STAT-005, ISSUE-001/002 y contraste CSV |
| AF082 | 25 | Se conservan extremos | R | TR-005, STAT-005, ISSUE-001/002 y contraste CSV |
| AF083 | 25 | Se conservan irregularidades temporales | R | TR-005, STAT-005, ISSUE-001/002 y contraste CSV |
| AF084 | 25 | Las anomalías no se acreditan como errores de medición | R | TR-005, STAT-005, ISSUE-001/002 y contraste CSV |
| AF085 | 31 | season dentro de dominio | R | STAT-004.invalid_domain_by_column |
| AF086 | 31 | yr dentro de dominio | R | STAT-004.invalid_domain_by_column |
| AF087 | 31 | mnth dentro de dominio | R | STAT-004.invalid_domain_by_column |
| AF088 | 31 | hr dentro de dominio | R | STAT-004.invalid_domain_by_column |
| AF089 | 31 | holiday dentro de dominio | R | STAT-004.invalid_domain_by_column |
| AF090 | 31 | weekday dentro de dominio | R | STAT-004.invalid_domain_by_column |
| AF091 | 31 | workingday dentro de dominio | R | STAT-004.invalid_domain_by_column |
| AF092 | 31 | weathersit dentro de dominio | R | STAT-004.invalid_domain_by_column |
| AF093 | 32 | temp dentro de [0,1] | R | STAT-004.normalized_ranges |
| AF094 | 32 | atemp dentro de [0,1] | R | STAT-004.normalized_ranges |
| AF095 | 32 | hum dentro de [0,1] | R | STAT-004.normalized_ranges |
| AF096 | 32 | windspeed dentro de [0,1] | R | STAT-004.normalized_ranges |
| AF097 | 32 | Máximo windspeed 0,8507 | R | STAT-004.normalized_ranges |
| AF098 | 33 | Casual sin negativos | R | STAT-004.negative_counts |
| AF099 | 33 | Registered sin negativos | R | STAT-004.negative_counts |
| AF100 | 33 | Cnt sin negativos | R | STAT-004.negative_counts |
| AF101 | 34 | yr coherente con fecha | R | STAT-004 y fechas fuente |
| AF102 | 34 | mnth coherente con fecha | R | STAT-004 y fechas fuente |
| AF103 | 34 | weekday coherente con fecha | R | STAT-004 y fechas fuente |
| AF104 | 34 | workingday coherente con fecha y holiday | R | STAT-004 y fechas fuente |
| AF105 | 34 | weekday utiliza domingo=0 | R | STAT-004 y fechas fuente |
| AF106 | 38 | Cnt suma 3292679 | R | STAT-007.cnt y FIG-003 |
| AF107 | 38 | Cnt cuartil 1 40 | R | STAT-007.cnt y FIG-003 |
| AF108 | 38 | Cnt cuartil 3 281 | R | STAT-007.cnt y FIG-003 |
| AF109 | 38 | Cnt percentil 99 782,2 | R | STAT-007.cnt y FIG-003 |
| AF110 | 38 | Distribución cnt con valores altos relevantes | R | STAT-007.cnt y FIG-003 |
| AF111 | 42 | Casual suma 620017 | R | STAT-007.casual |
| AF112 | 42 | Casual media 35,7 | R | STAT-007.casual |
| AF113 | 42 | Casual mediana 17 | R | STAT-007.casual |
| AF114 | 42 | Casual mínimo 0 | R | STAT-007.casual |
| AF115 | 42 | Casual máximo 367 | R | STAT-007.casual |
| AF116 | 43 | Registered suma 2672662 | R | STAT-007.registered |
| AF117 | 43 | Registered media 153,8 | R | STAT-007.registered |
| AF118 | 43 | Registered mediana 115 | R | STAT-007.registered |
| AF119 | 43 | Registered mínimo 0 | R | STAT-007.registered |
| AF120 | 43 | Registered máximo 886 | R | STAT-007.registered |
| AF121 | 46 | Meteorología conserva escala normalizada | R | STAT-007 y CSV |
| AF122 | 46 | Media temp 0,497 | R | STAT-007 y CSV |
| AF123 | 46 | Media atemp 0,476 | R | STAT-007 y CSV |
| AF124 | 46 | Media hum 0,627 | R | STAT-007 y CSV |
| AF125 | 46 | Media windspeed 0,190 | R | STAT-007 y CSV |
| AF126 | 48 | 2011 yr=0 | R | STAT-008 |
| AF127 | 48 | 2012 yr=1 | R | STAT-008 |
| AF128 | 48 | 2011 contiene 8645 registros | R | STAT-008 |
| AF129 | 48 | 2012 contiene 8734 registros | R | STAT-008 |
| AF130 | 48 | Reparto de registros casi equilibrado entre años | R | STAT-008 |
| AF131 | 48 | Workingday=1 representa 68,3% de registros | R | STAT-008 |
| AF132 | 48 | Holiday=1 contiene 500 registros | R | STAT-008 |
| AF133 | 48 | Holiday=1 representa 2,9% | R | STAT-008 |
| AF134 | 48 | Weathersit=1 contiene 11413 registros | R | STAT-008 |
| AF135 | 48 | Weathersit=1 representa 65,7% | R | STAT-008 |
| AF136 | 48 | Weathersit=4 contiene 3 registros | R | STAT-008 |
| AF137 | 54 | Total cnt 2011 1243103 | R | STAT-009.by_year |
| AF138 | 54 | Total cnt 2012 2049576 | R | STAT-009.by_year |
| AF139 | 54 | Comparar medias complementa las sumas cuando la cobertura difiere | R | STAT-009.by_year |
| AF140 | 56 | Media season1 spring 111,1 | R | STAT-009.by_season |
| AF141 | 56 | Media season2 summer 208,3 | R | STAT-009.by_season |
| AF142 | 56 | Media season3 fall 236,0 | R | STAT-009.by_season |
| AF143 | 56 | Media season4 winter 198,9 | R | STAT-009.by_season |
| AF144 | 56 | Casual cuota summer 22,2% | R | STAT-009.by_season |
| AF145 | 56 | Casual cuota fall 21,3% | R | STAT-009.by_season |
| AF146 | 56 | Casual cuota spring 12,9% | R | STAT-009.by_season |
| AF147 | 56 | Casual cuota mayor en summer que spring | R | STAT-009.by_season |
| AF148 | 56 | Casual cuota mayor en fall que spring | R | STAT-009.by_season |
| AF149 | 58 | Máximo total diario registrado 8714 | R | STAT-010.daily_max_rows/min y STAT-003 |
| AF150 | 58 | Fecha máximo diario 2012-09-15 | R | STAT-010.daily_max_rows/min y STAT-003 |
| AF151 | 58 | Máximo diario corresponde a 24 registros | R | STAT-010.daily_max_rows/min y STAT-003 |
| AF152 | 58 | Mínimo total diario registrado 22 | R | STAT-010.daily_max_rows/min y STAT-003 |
| AF153 | 58 | El mínimo diario puede tener cobertura incompleta | R | STAT-010.daily_max_rows/min y STAT-003 |
| AF154 | 62 | Media laboral a las 8 h 477,0 | R | STAT-011.by_hour_workingday y FIG-002 |
| AF155 | 62 | El máximo no laboral de las 13 h es más tardío | C | STAT-011 y FIG-002: las 13 h son anteriores al máximo laboral de las 17 h citado inmediatamente antes |
| AF156 | 64 | Laboral hr17 registered suma 233729 | R | STAT-011.by_hour_workingday |
| AF157 | 64 | Laboral hr17 casual suma 28391 | R | STAT-011.by_hour_workingday |
| AF158 | 64 | No laboral hr13 registered suma 54587 | R | STAT-011.by_hour_workingday |
| AF159 | 64 | No laboral hr13 casual suma 31514 | R | STAT-011.by_hour_workingday |
| AF160 | 64 | Registered domina la composición del pico laboral | R | STAT-011.by_hour_workingday |
| AF161 | 64 | La composición difiere entre ambos segmentos | R | STAT-011.by_hour_workingday |
| AF162 | 68 | Medias cnt disminuyen de meteorología1 a 4 | R | STAT-009.by_weather |
| AF163 | 68 | Weathersit=2 contiene 4544 registros | R | STAT-009.by_weather |
| AF164 | 68 | Weathersit=3 contiene 1419 registros | R | STAT-009.by_weather |
| AF165 | 68 | Weathersit=4 media cnt 74,3 | R | STAT-009.by_weather |
| AF166 | 68 | Weathersit=4 tiene base insuficiente para comparación robusta | R | STAT-009.by_weather |
| AF167 | 70 | Spearman cnt-temp 0,423 | R | STAT-012 y métodos registrados |
| AF168 | 70 | Spearman cnt-atemp 0,423 | R | STAT-012 y métodos registrados |
| AF169 | 70 | Spearman cnt-hum −0,360 | R | STAT-012 y métodos registrados |
| AF170 | 70 | Spearman cnt-windspeed 0,127 | R | STAT-012 y métodos registrados |
| AF171 | 70 | Temp y atemp tienen Spearman elevada | R | STAT-012 y métodos registrados |
| AF172 | 70 | Temp y atemp aportan información redundante | R | STAT-012 y métodos registrados |
| AF173 | 70 | Correlaciones bivariadas sin ajuste multivariable | R | STAT-012 y métodos registrados |
| AF174 | 74 | FIG-001 representa sumas diarias registradas | R | FIG-001, STAT-003/010 |
| AF175 | 74 | FIG-001 muestra variación en ambos años | R | FIG-001, STAT-003/010 |
| AF176 | 78 | Máximos laborales de tarde frente a no laborales de mediodía | R | FIG-002 y STAT-011 |
| AF177 | 82 | FIG-003 muestra concentración en valores bajos y medios | R | FIG-003, STAT-005 y ISSUE-002 |
| AF178 | 82 | FIG-003 muestra cola alta | R | FIG-003, STAT-005 y ISSUE-002 |
| AF179 | 82 | 505 registros por encima del límite IQR | R | FIG-003, STAT-005 y ISSUE-002 |
| AF180 | 82 | Límite superior IQR 642,5 | R | FIG-003, STAT-005 y ISSUE-002 |
| AF181 | 82 | Ser extremo IQR no acredita error | R | FIG-003, STAT-005 y ISSUE-002 |
| AF182 | 86 | FIG-004 compara distribuciones cnt por meteorología | R | FIG-004, STAT-009, código trace event37 y CSV |
| AF183 | 86 | Se ocultan valores atípicos del boxplot | R | FIG-004, STAT-009, código trace event37 y CSV |
| AF184 | 86 | Ocultar extremos visuales no elimina filas del CSV | R | FIG-004, STAT-009, código trace event37 y CSV |
| AF185 | 86 | Extremos documentados por separado | R | FIG-004, STAT-009, código trace event37 y CSV |
| AF186 | 90 | FIG-005 representa cnt frente a temp | R | FIG-005, STAT-012 y código registrado |
| AF187 | 90 | Color FIG-005 representa hum | R | FIG-005, STAT-012 y código registrado |
| AF188 | 90 | FIG-005 muestra dispersión sustancial | R | FIG-005, STAT-012 y código registrado |
| AF189 | 90 | Asociación positiva moderada cnt-temp | R | FIG-005, STAT-012 y código registrado |
| AF190 | 90 | Heterogeneidad no se resume por una única relación determinista | R | FIG-005, STAT-012 y código registrado |
| AF191 | 96 | Inicio temporal 2011-01-01 00:00:00 | R | STAT-003 y ISSUE-001 |
| AF192 | 96 | Fin temporal 2012-12-31 23:00:00 | R | STAT-003 y ISSUE-001 |
| AF193 | 96 | 17544 espacios horarios teóricos | R | STAT-003 y ISSUE-001 |
| AF194 | 96 | Totales diarios pueden reflejar cobertura desigual | R | STAT-003 y ISSUE-001 |
| AF195 | 96 | Totales mensuales pueden reflejar cobertura desigual | R | STAT-003 y ISSUE-001 |
| AF196 | 98 | Fecha máximo cnt 2012-09-12 | R | STAT-005/004/007 y ISSUE-002 |
| AF197 | 98 | Hora máximo cnt 18 | R | STAT-005/004/007 y ISSUE-002 |
| AF198 | 98 | Los extremos retenidos son no negativos | R | STAT-005/004/007 y ISSUE-002 |
| AF199 | 98 | Los extremos retenidos respetan la identidad | R | STAT-005/004/007 y ISSUE-002 |
| AF200 | 98 | La media es sensible a valores altos | R | STAT-005/004/007 y ISSUE-002 |
| AF201 | 104 | No contiene duración de viaje | R | STAT-001, profile, Readme y columnas CSV |
| AF202 | 104 | No contiene origen individual | R | STAT-001, profile, Readme y columnas CSV |
| AF203 | 104 | No contiene destino individual | R | STAT-001, profile, Readme y columnas CSV |
| AF204 | 104 | No contiene disponibilidad de bicicletas | R | STAT-001, profile, Readme y columnas CSV |
| AF205 | 104 | No permite analizar comportamiento espacial | R | STAT-001, profile, Readme y columnas CSV |
| AF206 | 106 | El archivo no determina la causa de los huecos | R | ISSUE-001 y columnas fuente |
| AF207 | 108 | No incorpora contraste meteorológico externo | R | STAT-012, limitations, herramientas y código de la traza |
| AF208 | 108 | No incorpora políticas operativas | R | STAT-012, limitations, herramientas y código de la traza |
| AF209 | 108 | No incorpora infraestructura | R | STAT-012, limitations, herramientas y código de la traza |
| AF210 | 108 | No incorpora eventos | R | STAT-012, limitations, herramientas y código de la traza |
| AF211 | 108 | No incorpora precios | R | STAT-012, limitations, herramientas y código de la traza |
| AF212 | 108 | No incorpora cambios de cobertura del servicio | R | STAT-012, limitations, herramientas y código de la traza |
| AF213 | 110 | Correlaciones no ajustan simultáneamente por hora | R | STAT-012, limitations y métodos registrados |
| AF214 | 110 | Correlaciones no ajustan simultáneamente por tipo de día | R | STAT-012, limitations y métodos registrados |
| AF215 | 110 | Correlaciones no ajustan simultáneamente por año | R | STAT-012, limitations y métodos registrados |
| AF216 | 110 | Correlaciones no ajustan simultáneamente por temporada | R | STAT-012, limitations y métodos registrados |
| AF217 | 112 | La composición de meteorología4 tiene gran incertidumbre por n=3 | R | STAT-008/009 y tamaño grupo |
