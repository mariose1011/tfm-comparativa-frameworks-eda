# Evaluación D1-LG-R3

**Índice final:** 86,36/100.  
**Evaluación cerrada:** 6 de octubre de 2026.  
**Ejecución:** `D1_bike_sharing__langgraph__r03__20260831T214132905916Z`

**Criterios:** [Protocolo de evaluación](../01_protocolo_calidad_Q1_Q10_v0.1.md) y [guía D1](../02_ficha_D1_bike_sharing.md).  
**Resultados:** [Archivos originales de la ejecución](../../../outputs/experimento/D1_bike_sharing__langgraph__r03__20260831T214132905916Z).  
**Evaluación:** [Excel de puntuaciones](../Evaluacion_calidad.xlsx) y [JSON de comprobaciones](D1-LG-R3_comprobaciones.json).

Las referencias `STAT`, `ISSUE` y `FIG` identifican análisis, problemas y figuras en los archivos de la ejecución. Las referencias a líneas corresponden a su informe original, `report.md`.

## Resumen

| Métrica | Puntuación final |
| --- | ---: |
| Q1 Cumplimiento de las etapas | 93,75 |
| Q2 Corrección numérica | 80,00 |
| Q3 Validez del tratamiento de los datos | 100,00 |
| Q4 Detección de problemas y riesgos | 92,31 |
| Q5 Calidad y profundidad del EDA | 75,00 |
| Q6 Profundidad de la interpretación | 75,00 |
| Q7 Calidad de las visualizaciones | 95,00 |
| Q8 Cobertura del informe | 75,00 |
| Q9 Fidelidad del informe | 100,00 |
| Q10 Claridad y coherencia | 75,00 |

La ejecución terminó con el estado `partial` después de la corrección. Durante esta fase se sobrescribió `issues.json` y quedó vacío. Una petición posterior se bloqueó por el límite de tokens de entrada, y el archivo no llegó a recuperarse. El informe final mantiene referencias a problemas cuyo registro ha quedado vacío. Estas incidencias se valoran en las métricas correspondientes, sin añadir una penalización por el estado técnico.

## Q1 Cumplimiento de las etapas: 93,75

| Etapa | Puntos | Evidencia |
| --- | ---: | --- |
| E1 Carga e inspección inicial | 1 | STAT-001, profile y report11/13 |
| E2 Estructura, tipos y calidad | 1 | STAT-002 a STAT-005 |
| E3 Preparación y decisiones de análisis | 1 | TR-001/002 y copia utilizable de 17379 x 17 |
| E4 Estadística descriptiva | 1 | STAT-006/007/008 |
| E5 Variables, agregaciones y relaciones | 1 | STAT-009 a STAT-012 |
| E6 Visualizaciones | 1 | FIG-001 a FIG-004 abiertas y contrastadas |
| E7 Problemas, riesgos y anomalías | 0,5 | Report71–87 y STAT-013, pero registro estructurado issues vacío |
| E8 Informe final | 1 | Informe final con alcance, hallazgos, figuras y limitaciones |

E7 tiene evidencia válida, pero carece de una parte sustancial: el registro estructurado de comprobaciones y riesgos. E3 recibió la puntuación completa porque la copia preparada conservó las filas y columnas originales y documentó la preparación realizada.

`Q1 = 100 x 7,5 / 8 = 93,75`

## Q2 Corrección numérica: 80,00

| Control | Producido | Estado | Puntos | Evidencia |
| --- | --- | --- | --- | --- |
| C01 Filas | 17379 | Correcta | 2/2 | STAT-001.rows |
| C02 Columnas | 17 | Correcta | 2/2 | STAT-001.columns |
| C03 Fechas distintas | 731 | Correcta | 1/1 | STAT-004.distinct_dates |
| C04 Celdas ausentes | 0 | Correcta | 2/2 | STAT-002.missing_by_column |
| C05 Filas duplicadas | 0 | Correcta | 2/2 | STAT-002.duplicate_full_rows |
| C06 Huecos horarios | 165 | Correcta | 1/1 | STAT-004.missing_date_hour_combinations |
| C07 Total cnt | 3292679 | Correcta | 2/2 | STAT-006.cnt.sum |
| C08 Media cnt | 189,463088 | Correcta | 2/2 | STAT-006.cnt.mean |
| C09 Mediana cnt | 142 | Correcta | 1/1 | STAT-006.cnt.median |
| C10 Desviación muestral cnt | 181,387599 | Correcta | 1/1 | STAT-006.cnt.std |
| C11 Máximo horario cnt | 977 | Correcta | 1/1 | STAT-006.cnt.max |
| C12 Total casual | 620017 | Correcta | 1/1 | STAT-006.casual.sum |
| C13 Total registered | 2672662 | Correcta | 1/1 | STAT-006.registered.sum |
| C14 Cuota global registered | 0,811698316 | Correcta | 1/1 | STAT-012.overall_registered_share |
| C15 Total 2011 | 1243103 | Correcta | 1/1 | STAT-008.by_yr[yr=0].sum |
| C16 Total 2012 | 2049576 | Correcta | 1/1 | STAT-008.by_yr[yr=1].sum |
| C17 Variación porcentual anual | No producido | Ausente | 0/2 | Totales anuales no sustituyen el porcentaje |
| C18 Máximo medio global por hora | No producido | Ausente | 0/2 | Solo perfiles separados por workingday |
| C19 Mínimo medio global por hora | No producido | Ausente | 0/1 | Solo perfiles separados por workingday |
| C20 Temporada de mayor media | Season3, 236,016237 | Correcta | 1/1 | STAT-008.by_season |
| C21 Media weathersit1 | 204,869272 | Correcta | 1/1 | STAT-008.by_weathersit |
| C22 Media weathersit3 | 111,579281 | Correcta | 1/1 | STAT-008.by_weathersit |
| C23 Tamaño weathersit4 | 3 | Correcta | 1/1 | STAT-008.by_weathersit |
| C24 Pearson temp-cnt | No producido | Ausente | 0/1 | Solo Spearman de cnt con temp |
| C25 Pearson hum-cnt | No producido | Ausente | 0/1 | Solo Spearman de cnt con hum |
| C26 Inconsistencias de identidad | 0 | Correcta | 2/2 | STAT-005.mismatches |

Hay 21 controles correctos y cinco ausentes. El JSON adjunto conserva valores esperados, tolerancias y correspondencias completas.

C18 y C19 permanecen ausentes porque STAT-009 contiene medias por hora y tipo de día, pero no el tamaño de cada grupo necesario para combinarlas mediante una media ponderada.

`Q2 = 100 x 28 / 35 = 80,00`

## Q3 Validez del tratamiento de los datos: 100,00

| Decisión | Puntos | Evidencia y motivo |
| --- | ---: | --- |
| D01 Fecha y marca temporal con hora | 1 | Construye claves fecha–hora y un índice MultiIndex para detectar huecos. Traza16/116 |
| D02 Códigos como categorías | 1 | Dominios y agrupaciones categóricas STAT-003/007/008/009 |
| D03 instant como identificador | 1 | Report13 y código, sin relación explicativa con instant |
| D04 Sin limpieza innecesaria | 1 | TR-002 y todas las columnas fuente intactas |
| D05 No imputar huecos | 1 | Report71, CSV y agrupaciones sobre observaciones disponibles |
| D06 Extremos conservados | 1 | TR-002, STAT-013 y report75 |
| D07 Identidad y composición | 1 | STAT-005/012 y report23/31/45 |
| D08 Escalas conservadas | 1 | CSV, report33/83 y Readme |

`Q3 = 100 x 8 / 8 = 100,00`

## Q4 Detección de problemas y riesgos: 92,31

| Riesgo | Clasificación | Evidencia |
| --- | --- | --- |
| R01 Identificador instant | Completo | Report13 y uso como índice |
| R02 Códigos numéricos categóricos | Completo | Report13/19, dominios y análisis agrupados |
| R03 Identidad cnt y componentes | Completo | Report23, STAT-005 |
| R04 Escalas normalizadas | Completo | Report33/83 |
| R05 Huecos horarios | Completo | Report71/87, STAT-004 |
| R06 Grupo meteorológico n=3 | Completo | Report47/73, STAT-007/008 |
| R07 Dependencia temporal y calendario | Parcial | Comprueba calendario, pero no dependencia entre observaciones sucesivas |
| A01 Redundancia temp-atemp | Adicional válido | Report49, STAT-011 |
| A02 Sensibilidad de la media a picos válidos | Adicional válido | Report75, STAT-006/013 |
| A03 Límites de agregación y variables no disponibles | Adicional válido | Report81, unidad y esquema fuente |

K=6, A=3 y F=0. La precisión es 1 y la cobertura es 6/7. Su media armónica F1 es aproximadamente 0,9231, que corresponde a una puntuación Q4 de 92,31.

`Q4 = 100 x [2 x 1 x (6 / 7)] / [1 + (6 / 7)] = 92,31`

## Q5 Calidad y profundidad del EDA: 75,00

Se asigna el nivel **3/4**. El análisis examina distribuciones, frecuencias, segmentos, composición, asociaciones y extremos con reglas reproducibles. STAT-006 a STAT-013 enlazan etapas y conservan la población.

No alcanza 4/4 porque no desarrolla la dependencia temporal y no relaciona el mínimo diario de 22 alquileres con su cobertura de una sola hora. No se reduce la nota por elegir Spearman ni por el estado partial.

`Q5 = 100 x 3 / 4 = 75,00`

## Q6 Profundidad de la interpretación: 75,00

Se asigna el nivel **3/4**. Report45/47/49/67/75/81/85 interpreta correctamente composición, dispersión, grupo meteorológico pequeño y límites de las asociaciones. No afirma causas ni exige atribuir extremos a eventos externos.

Falta integrar la cobertura concreta del mínimo diario con su interpretación. El informe advierte de los huecos en general, pero presenta los extremos diarios sin contextualizar esa diferencia de exposición. La cifra 22 es correcta y no se afirma que proceda de un día completo, por lo que no constituye una contradicción en Q9.

`Q6 = 100 x 3 / 4 = 75,00`

## Q7 Calidad de las visualizaciones: 95,00

| Objetivo | Nota | Evidencia y motivo |
| --- | ---: | --- |
| V01 Evolución temporal | 4 | FIG-001 muestra los 24 meses ordenados, sin saturación y con suma mensual explícita |
| V02 Perfil horario | 4 | FIG-002 muestra ambas condiciones laborales, las 24 horas y escalas claras |
| V03 Patrón mensual o estacional | 4 | FIG-001 y report41/55 describen máximos mensuales y diferencias entre años |
| V04 Meteorología y grupo pequeño | 4 | FIG-003 combina boxplot con todos los puntos. Report63/73 advierte n=3 |
| V05 Relación ambiental densa | 3 | FIG-004 muestra asociación y variabilidad, pero la superposición dificulta distinguir los grupos laborales que comenta report67 |

Cuatro imágenes pueden cubrir cinco objetivos. V01 y V03 comparten una figura que responde a ambos.

En el gráfico por situación meteorológica, los puntos superpuestos al diagrama de cajas mostraron también los valores extremos. En el gráfico de alquileres frente a temperatura se aprecia la tendencia general y la variabilidad, aunque la superposición de puntos dificulta distinguir los días laborables de los no laborables.

`Q7 = 100 x 19 / 20 = 95,00`

## Q8 Cobertura del informe: 75,00

| Unidad | Peso | Crédito | Puntos | Evidencia y motivo |
| --- | ---: | ---: | ---: | --- |
| U01 Estructura y periodo | 2 | 1 | 2 | Report3/11/19 |
| U02 Calidad y huecos | 2 | 1 | 2 | Report7/19/21/71 |
| U03 Nivel y dispersión cnt | 2 | 1 | 2 | Report5/29 |
| U04 Cuota global registered | 2 | 0 | 0 | Report31 comunica componentes, no su cuota global. |
| U05 Cambio anual | 2 | 0,5 | 1 | Report39 comunica totales y dirección del cambio, no el porcentaje |
| U06 Máximo y mínimo horario global | 2 | 0 | 0 | Los perfiles de report45 y FIG-002 están segmentados, no son globales |
| U07 Máximos por condición laboral | 2 | 1 | 2 | Report45 y FIG-002, 17h laboral y 13h no laboral |
| U08 Diferencias mensuales o estacionales | 1 | 1 | 1 | Report41 incluye las cuatro medias, season3 mayor, y máximos mensuales |
| U09 Meteorología y n=3 | 2 | 1 | 2 | Report47/63/73 |
| U10 Temperatura y humedad | 2 | 1 | 2 | Report49/67/95, Spearman y cautela causal |
| U11 Identidad y redundancia de conteos | 2 | 1 | 2 | Report13/23/31 |
| U12 Dependencia, ciudad y no causalidad | 1 | 0,5 | 0,5 | Report3/11/85 identifica ciudad y límites causales, no dependencia serial |


STAT-012 contiene la proporción de alquileres de usuarios registrados, que se valora en Q2, pero el informe no la comunica y por eso U04 recibe 0. El informe tampoco identifica las horas con mayor y menor media del conjunto completo, sino que presenta los resultados separados entre días laborables y no laborables. Los datos disponibles únicamente en las estadísticas no completan los contenidos ausentes del informe.

`Q8 = 100 x 16,5 / 22 = 75,00`

## Q9 Fidelidad del informe: 100,00

Se revisan **154 afirmaciones distintas, todas respaldadas, sin afirmaciones contradichas ni carentes de respaldo suficiente.** Se revisa report.md, con figuras y conclusiones. Las repeticiones se agrupan y las cifras independientes se separan.

No implica cobertura o claridad máximas. Las citas ISSUE no resuelven, pero los hechos a los que remiten tienen respaldo inequívoco en STAT-004/007/008/013 finales. La falta del registro se valora en Q1 y el defecto de referencias en Q10, sin tratar esos hechos como falsos por el enlace roto.

`Q9 = 100 x 154 / 154 = 100,00`

## Q10 Claridad y coherencia: 75,00

Se asigna **3/4**. El informe está ordenado, integra figuras y permite seguir los análisis. Quedan referencias ISSUE-001/002/003 sin destino por el archivo vacío. Algunos códigos y las diferencias entre tipos de usuario se explican poco. Son defectos concretos, no una invalidación global del informe ni una penalización por su longitud.

`Q10 = 100 x 3 / 4 = 75,00`

## Anexo Q9: inventario completo

Las 154 afirmaciones, localizadores y evidencias se reproducen a continuación desde el JSON de comprobaciones. R significa respaldada.

| ID | Líneas del informe | Afirmación | Estado | Evidencia |
| --- | --- | --- | --- | --- |
| AF001 | 3,11 | Fuente Bike Sharing horario de Capital Bikeshare | R | STAT-001, profile y Readme, Data Set |
| AF002 | 3,11 | El sistema documentado corresponde a Washington D.C. | R | STAT-001, profile y Readme, Data Set |
| AF003 | 3,11 | La cobertura corresponde a 2011–2012 | R | STAT-001, profile y Readme, Data Set |
| AF004 | 3,25 | La copia preparada conserva 17379 filas | R | profile, TR-001/002 y CSV contrastado |
| AF005 | 3,25 | La copia conserva las 17 columnas fuente | R | profile, TR-001/002 y CSV contrastado |
| AF006 | 3,25 | La única normalización es validar dteday y serializarla ISO | R | profile, TR-001/002 y CSV contrastado |
| AF007 | 3,25 | No se eliminaron observaciones, incluidos los extremos | R | profile, TR-001/002 y CSV contrastado |
| AF008 | 5,29,31 | Total cnt de 3292679 alquileres | R | STAT-006.cnt |
| AF009 | 5,29,31 | Media horaria cnt de 189,5 | R | STAT-006.cnt |
| AF010 | 5,29,31 | Mediana horaria cnt de 142 | R | STAT-006.cnt |
| AF011 | 5,29,31 | Desviación estándar muestral cnt de 181,4 | R | STAT-006.cnt |
| AF012 | 5,29,31 | La media supera a la mediana | R | STAT-006.cnt |
| AF013 | 5,29,31 | Los conteos son heterogéneos y presentan picos horarios | R | STAT-006.cnt |
| AF014 | 5,39,93 | La media de yr=1 es 234,7 | R | STAT-008.by_yr |
| AF015 | 5,39,93 | La media de yr=0 es 143,8 | R | STAT-008.by_yr |
| AF016 | 5,39,93 | La media del segundo año supera la del primero | R | STAT-008.by_yr |
| AF017 | 5,45,93 | Los días laborables presentan un pico a las 08:00 | R | STAT-009.means y FIG-002 |
| AF018 | 5,45,93 | Los días laborables presentan un pico a las 17:00–18:00 | R | STAT-009.means y FIG-002 |
| AF019 | 7,21,77,91 | No hay celdas ausentes | R | STAT-002 |
| AF020 | 7,21,77,91 | No hay filas completas duplicadas | R | STAT-002 |
| AF021 | 7,21,77,91 | No hay valores de instant duplicados | R | STAT-002 |
| AF022 | 7,21,77,91 | No hay claves dteday-hr duplicadas | R | STAT-002 |
| AF023 | 7,23,77,91 | cnt = casual + registered se cumple en todas las filas | R | STAT-005 |
| AF024 | 7,71,87,97 | Faltan 165 combinaciones fecha-hora frente a la malla completa | R | STAT-004 |
| AF025 | 7,71,87,97 | La malla completa abarca 731 días con 24 horas por día | R | STAT-004 |
| AF026 | 7,35,47,63,73 | weathersit=4 tiene tres registros | R | STAT-007.weathersit |
| AF027 | 11,91 | El CSV contiene hr | R | STAT-001 y profile |
| AF028 | 11,91 | La entrada tiene 17 columnas | R | STAT-001 y profile |
| AF029 | 11,91 | La entrada tiene 17379 registros | R | STAT-001 y profile |
| AF030 | 11,91 | La estructura coincide con la documentación del archivo horario | R | STAT-001 y profile |
| AF031 | 11,13,81 | Los registros son agregados horarios, no alquileres individuales | R | profile, Readme y esquema fuente |
| AF032 | 11,13,81 | La tabla integra información temporal y meteorológica | R | profile, Readme y esquema fuente |
| AF033 | 11,13,81 | La unidad observada combina fecha y hora | R | profile, Readme y esquema fuente |
| AF034 | 11,13,81 | Incluye códigos de calendario y variables meteorológicas normalizadas | R | profile, Readme y esquema fuente |
| AF035 | 13 | casual y registered son los componentes de cnt | R | Readme, STAT-005 y traza execute_python |
| AF036 | 13 | instant se usa solo como índice de trazabilidad y orden | R | Readme, STAT-005 y traza execute_python |
| AF037 | 15 | El trabajo examina estructura y calidad | R | STAT-001 a STAT-013, figuras y código registrado |
| AF038 | 15 | El trabajo examina distribuciones y agregaciones temporales | R | STAT-001 a STAT-013, figuras y código registrado |
| AF039 | 15 | El trabajo examina composición y asociaciones meteorológicas bivariadas | R | STAT-001 a STAT-013, figuras y código registrado |
| AF040 | 15 | No se entrenaron modelos predictivos | R | STAT-001 a STAT-013, figuras y código registrado |
| AF041 | 15 | No se realizaron inferencias causales | R | STAT-001 a STAT-013, figuras y código registrado |
| AF042 | 19,77,91 | El parseo explícito %Y-%m-%d fue completo | R | STAT-003.date_parse_failures, traza y CSV |
| AF043 | 19 | La primera fecha es 2011-01-01 | R | STAT-004 |
| AF044 | 19 | La última fecha es 2012-12-31 | R | STAT-004 |
| AF045 | 19 | Hay 731 fechas distintas | R | STAT-004 |
| AF046 | 19 | No hay días enteros ausentes | R | STAT-004 |
| AF047 | 19 | yr es coherente con la fecha | R | STAT-003.calendar_mismatches |
| AF048 | 19 | mnth es coherente con la fecha | R | STAT-003.calendar_mismatches |
| AF049 | 19 | weekday es coherente con la fecha bajo la convención domingo=0 | R | STAT-003.calendar_mismatches |
| AF050 | 19,77 | Los ocho códigos categóricos enumerados están en los dominios documentados | R | STAT-003.domains y Readme |
| AF051 | 21 | Las 17379 filas son completas | R | STAT-002 |
| AF052 | 21 | instant sigue la secuencia 1 a 17379 | R | STAT-002 |
| AF053 | 23 | La identidad se comprobó en 17379 filas | R | STAT-005 |
| AF054 | 23 | La diferencia mínima entre cnt y sus componentes es cero | R | STAT-005 |
| AF055 | 23 | La diferencia máxima entre cnt y sus componentes es cero | R | STAT-005 |
| AF056 | 23 | La composición se calculó tras validar la identidad, sin reconciliación ni imputación | R | STAT-005 |
| AF057 | 25,75,87 | Los extremos conservados mantienen la identidad de conteos | R | STAT-003/005/013, TR-002 y CSV |
| AF058 | 25,75,87 | Los extremos conservados no tienen conteos negativos | R | STAT-003/005/013, TR-002 y CSV |
| AF059 | 25,75,87 | Los extremos conservados no presentan categorías fuera de dominio | R | STAT-003/005/013, TR-002 y CSV |
| AF060 | 25 | La decisión de preparación y su justificación constan en TR-001 y TR-002 | R | statistics.preparation.changes |
| AF061 | 29 | Mínimo horario cnt de 1 | R | STAT-006.cnt |
| AF062 | 29 | Primer cuartil cnt de 40 | R | STAT-006.cnt |
| AF063 | 29 | Tercer cuartil cnt de 281 | R | STAT-006.cnt |
| AF064 | 29 | Máximo horario cnt de 977 | R | STAT-006.cnt |
| AF065 | 29 | Una media horaria aislada no resume la dispersión observada | R | STAT-006.cnt |
| AF066 | 31 | Total casual de 620017 | R | STAT-006.casual/registered |
| AF067 | 31 | Total registered de 2672662 | R | STAT-006.casual/registered |
| AF068 | 31 | Mediana casual de 17 | R | STAT-006.casual/registered |
| AF069 | 31 | Mediana registered de 115 | R | STAT-006.casual/registered |
| AF070 | 33,83 | Las cuatro variables meteorológicas se mantienen en la escala normalizada fuente | R | CSV, STAT-006 y Readme |
| AF071 | 33,83 | Los valores fuente no son directamente unidades físicas desnormalizadas | R | CSV, STAT-006 y Readme |
| AF072 | 33 | Media temp de 0,497 | R | STAT-006.temp |
| AF073 | 33 | Mínimo temp de 0,02 | R | STAT-006.temp |
| AF074 | 33 | Máximo temp de 1,00 | R | STAT-006.temp |
| AF075 | 33 | Media hum de 0,627 | R | STAT-006.hum |
| AF076 | 33 | Mínimo hum de 0 | R | STAT-006.hum |
| AF077 | 33 | Máximo hum de 1,00 | R | STAT-006.hum |
| AF078 | 33 | Media windspeed de 0,190 | R | STAT-006.windspeed |
| AF079 | 33 | Mediana windspeed de 0,194 | R | STAT-006.windspeed |
| AF080 | 33 | Máximo windspeed de 0,8507 | R | STAT-006.windspeed |
| AF081 | 35 | weathersit=1 es la categoría más frecuente | R | STAT-007.weathersit |
| AF082 | 35 | weathersit=1 tiene 11413 registros | R | STAT-007.weathersit |
| AF083 | 35 | weathersit=2 tiene 4544 registros | R | STAT-007.weathersit |
| AF084 | 35 | weathersit=3 tiene 1419 registros | R | STAT-007.weathersit |
| AF085 | 35 | workingday=1 tiene 11865 registros | R | STAT-007.workingday |
| AF086 | 35 | workingday=0 tiene 5514 registros | R | STAT-007.workingday |
| AF087 | 39 | Total yr=0 de 1243103 | R | STAT-008.by_yr |
| AF088 | 39 | Total yr=1 de 2049576 | R | STAT-008.by_yr |
| AF089 | 39 | El volumen anual del segundo año supera al primero | R | STAT-008.by_yr |
| AF090 | 41 | Media season=1 de 111,1 | R | STAT-008.by_season |
| AF091 | 41 | Media season=2 de 208,3 | R | STAT-008.by_season |
| AF092 | 41 | Media season=3 de 236,0 | R | STAT-008.by_season |
| AF093 | 41 | Media season=4 de 198,9 | R | STAT-008.by_season |
| AF094 | 41 | Cada mes de yr=1 supera su mes homólogo de yr=0 | R | STAT-010.monthly_totals y FIG-001 |
| AF095 | 41 | El máximo mensual yr=1 es 218573 | R | STAT-010.monthly_totals y FIG-001 |
| AF096 | 41 | El máximo mensual yr=1 corresponde a septiembre | R | STAT-010.monthly_totals y FIG-001 |
| AF097 | 41 | El máximo mensual yr=0 es 143512 | R | STAT-010.monthly_totals y FIG-001 |
| AF098 | 41 | El máximo mensual yr=0 corresponde a junio | R | STAT-010.monthly_totals y FIG-001 |
| AF099 | 43 | La suma diaria máxima es 8714 | R | STAT-010.highest_daily_total/lowest_daily_total |
| AF100 | 43 | La fecha de la suma diaria máxima es 2012-09-15 | R | STAT-010.highest_daily_total/lowest_daily_total |
| AF101 | 43 | La suma diaria mínima es 22 | R | STAT-010.highest_daily_total/lowest_daily_total |
| AF102 | 43 | La fecha de la suma diaria mínima es 2012-10-29 | R | STAT-010.highest_daily_total/lowest_daily_total |
| AF103 | 45,59,93 | El perfil horario difiere entre condiciones laborales | R | STAT-009.means y FIG-002 |
| AF104 | 45,59,93 | Media cnt laboral a las 08:00 de 477,0 | R | STAT-009.means y FIG-002 |
| AF105 | 45,59,93 | Media cnt laboral a las 17:00 de 525,3 | R | STAT-009.means y FIG-002 |
| AF106 | 45,59,93 | Media cnt laboral a las 18:00 de 492,2 | R | STAT-009.means y FIG-002 |
| AF107 | 45,59,93 | Máximo medio no laboral de 372,7 | R | STAT-009.means y FIG-002 |
| AF108 | 45,59,93 | El máximo no laboral ocurre a las 13:00 | R | STAT-009.means y FIG-002 |
| AF109 | 45,59,93 | Los no laborables tienen una meseta más amplia al mediodía y por la tarde | R | STAT-009.means y FIG-002 |
| AF110 | 45,59,93 | registered domina los picos laborales | R | STAT-009.means y FIG-002 |
| AF111 | 45,59,93 | Media registered laboral a las 08:00 de 454,7 | R | STAT-009.means y FIG-002 |
| AF112 | 45,59,93 | Media casual laboral a las 08:00 de 22,3 | R | STAT-009.means y FIG-002 |
| AF113 | 47,95 | Las medias cnt descienden entre los códigos meteorológicos 1, 2 y 3 | R | STAT-008.by_weathersit |
| AF114 | 47,95 | Media cnt weathersit=1 de 204,9 | R | STAT-008.by_weathersit |
| AF115 | 47,95 | Media cnt weathersit=2 de 175,2 | R | STAT-008.by_weathersit |
| AF116 | 47,95 | Media cnt weathersit=3 de 111,6 | R | STAT-008.by_weathersit |
| AF117 | 47,95 | Media cnt weathersit=4 de 74,3 | R | STAT-008.by_weathersit |
| AF118 | 47,63,73,87,97 | El grupo meteorológico 4 no permite una comparación estable por n=3 | R | STAT-007/008 y FIG-003 |
| AF119 | 47,63,73,87,97 | Sus medias, medianas y distribución son sensibles a casos individuales | R | STAT-007/008 y FIG-003 |
| AF120 | 49,95 | Spearman cnt-temp de 0,423 | R | STAT-011.spearman_correlation_matrix |
| AF121 | 49,95 | Spearman cnt-hum de -0,360 | R | STAT-011.spearman_correlation_matrix |
| AF122 | 49,95 | Spearman cnt-windspeed de 0,127 | R | STAT-011.spearman_correlation_matrix |
| AF123 | 49,85 | Las correlaciones son bivariadas y no están ajustadas por hora, estación ni año | R | STAT-011.method y código registrado |
| AF124 | 49 | Pearson temp-atemp de 0,988 | R | STAT-011 |
| AF125 | 49 | Spearman temp-atemp aproximadamente 0,990 | R | STAT-011 |
| AF126 | 49 | temp y atemp presentan redundancia elevada | R | STAT-011 |
| AF127 | 55 | La figura 1 sintetiza la evolución mensual 2011–2012 | R | FIG-001 y STAT-010 |
| AF128 | 55 | Se observa variación dentro de cada año | R | FIG-001 y STAT-010 |
| AF129 | 59 | La figura 2 separa workingday=0 y workingday=1 | R | FIG-002 y STAT-009 |
| AF130 | 59 | En las horas centrales el nivel no laboral es más alto y sostenido que el laboral | R | FIG-002 y STAT-009 |
| AF131 | 63 | La figura 3 representa dispersión y densidad de observaciones por weathersit | R | FIG-003 y traza evento16, boxplot + stripplot sin muestreo |
| AF132 | 67 | La figura 4 muestra una asociación positiva general entre temp y cnt | R | FIG-004 y STAT-011 |
| AF133 | 67 | La figura 4 muestra amplia variabilidad de cnt a temperaturas similares | R | FIG-004 y STAT-011 |
| AF134 | 67 | La figura 4 diferencia las condiciones laborales | R | FIG-004 y STAT-011 |
| AF135 | 67 | La temperatura aislada no resume el comportamiento horario observado | R | FIG-004 y STAT-011 |
| AF136 | 71 | La malla teórica tiene 17544 combinaciones fecha-hora | R | STAT-004 |
| AF137 | 71 | El mínimo de registros por día es 1 | R | STAT-004 |
| AF138 | 71 | El máximo de registros por día es 24 | R | STAT-004 |
| AF139 | 71 | Se conservan los datos observados sin imputación | R | TR-002, CSV y código de agregación |
| AF140 | 71 | Las agregaciones utilizan la población disponible | R | TR-002, CSV y código de agregación |
| AF141 | 73 | weathersit=4 pertenece al dominio documentado y no es inválido | R | Readme y STAT-003.domains.weathersit |
| AF142 | 75 | El cribado IQR global señala 505 registros | R | STAT-013 y código registrado |
| AF143 | 75 | Los 505 registros señalados están por encima del umbral superior | R | STAT-013 y código registrado |
| AF144 | 75 | Los extremos estadísticos no se clasificaron como errores | R | STAT-013 y código registrado |
| AF145 | 75 | Retener los picos implica que la media es sensible a ellos | R | STAT-006/013 y TR-002 |
| AF146 | 81 | La tabla no contiene trayectos | R | profile.column_names y STAT-001.column_order |
| AF147 | 81 | La tabla no contiene estaciones de origen o destino | R | profile.column_names y STAT-001.column_order |
| AF148 | 81 | La tabla no contiene duración de los alquileres | R | profile.column_names y STAT-001.column_order |
| AF149 | 81 | La tabla no contiene disponibilidad de bicicletas | R | profile.column_names y STAT-001.column_order |
| AF150 | 81 | La tabla no contiene atributos individuales de usuarios | R | profile.column_names y STAT-001.column_order |
| AF151 | 81 | El alcance no permite describir desplazamientos individuales | R | Unidad agregada y esquema de columnas |
| AF152 | 81 | El alcance no permite separar demanda de restricciones de oferta | R | Unidad agregada y esquema de columnas |
| AF153 | 85 | Las variables comparadas se relacionan con el tiempo calendario | R | STAT-003.calendar_mismatches y método de STAT-008/011 |
| AF154 | 87 | Los huecos limitan la comparabilidad estricta de algunas medias horarias | R | STAT-004 y denominadores observados |
