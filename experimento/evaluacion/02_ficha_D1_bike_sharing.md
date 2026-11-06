# Guía de evaluación D1 Bike Sharing

**Versión:** 0.1 ; **Uso:** criterios específicos de D1

Esta guía recoge los criterios específicos para evaluar D1. No se completa para cada ejecución. Las puntuaciones finales se registran en el [Excel](Evaluacion_calidad.xlsx), mientras que las justificaciones y evidencias se detallan en la ficha de cada ejecución.

Los apartados siguientes detallan las comprobaciones numéricas, las decisiones de preparación, los riesgos, los objetivos visuales y los contenidos del informe específicos de este dataset, correspondientes a Q2, Q3, Q4, Q7 y Q8. Las demás métricas utilizan criterios comunes a los dos datasets. Las fórmulas, escalas y reglas generales de puntuación se consultan en el [protocolo de evaluación](01_protocolo_calidad_Q1_Q10_v0.1.md).

Referencias del dataset: [especificación](../../datasets/reference_private/D1_bike_sharing/evaluation_spec.json), [valores de referencia](../../datasets/reference_private/D1_bike_sharing/reference_values.json) y [ficha de referencia](../../datasets/reference_private/D1_bike_sharing/ficha_referencia_D1_bike_sharing.md).

## Q2 Comprobaciones numéricas

26 comprobaciones, con peso total 35. Los valores deben corresponder a la población y definición indicadas en la referencia.

| ID | Comprobación | Referencia y tolerancia | Peso |
| --- | --- | --- | --- |
| C01 | Número de filas | 17379 ; Exacto | 2 |
| C02 | Número de columnas | 17 ; Exacto | 2 |
| C03 | Fechas distintas | 731 ; Exacto | 1 |
| C04 | Celdas ausentes | 0 ; Exacto | 2 |
| C05 | Filas duplicadas | 0 ; Exacto | 2 |
| C06 | Huecos en la secuencia horaria | 165 ; Exacto | 1 |
| C07 | Alquileres totales | 3292679 ; Exacto | 2 |
| C08 | Media horaria de alquileres | 189.463088 ; ± 0.01 | 2 |
| C09 | Mediana horaria de alquileres | 142 ; ± 0.01 | 1 |
| C10 | Desviación típica muestral | 181.387599 ; ± 0.01 | 1 |
| C11 | Máximo horario | 977 ; Exacto | 1 |
| C12 | Total de alquileres de usuarios ocasionales | 620017 ; Exacto | 1 |
| C13 | Total de alquileres de usuarios registrados | 2672662 ; Exacto | 1 |
| C14 | Proporción de alquileres de usuarios registrados sobre el total | 0.811698316 ; ± 0.001 | 1 |
| C15 | Alquileres totales en 2011 | 1243103 ; Exacto | 1 |
| C16 | Alquileres totales en 2012 | 2049576 ; Exacto | 1 |
| C17 | Variación total de 2012 respecto a 2011 | 64.875799 % ; ± 0.1 puntos porcentuales | 2 |
| C18 | Hora con mayor media | Categoría 17, valor 461.452055 ; ± 0.05 | 2 |
| C19 | Hora con menor media | Categoría 4, valor 6.352941 ; ± 0.05 | 1 |
| C20 | Temporada con mayor media | Categoría 3, valor 236.016237 ; ± 0.05 | 1 |
| C21 | Media con tiempo despejado | Categoría 1, valor 204.869272 ; ± 0.05 | 1 |
| C22 | Media con tiempo adverso de categoría 3 | Categoría 3, valor 111.579281 ; ± 0.05 | 1 |
| C23 | Observaciones meteorológicas de categoría 4 | 3 ; Exacto | 1 |
| C24 | Correlación de Pearson entre temperatura y cnt | 0.404772 ; ± 0.005 | 1 |
| C25 | Correlación de Pearson entre humedad y cnt | -0.322911 ; ± 0.005 | 1 |
| C26 | Inconsistencias en cnt = casual + registered | 0 ; Exacto | 2 |

## Q3 Tratamiento de datos

Ocho decisiones sobre la preparación y conservación de los datos.

| ID | Ámbito de decisión |
| --- | --- |
| D01 | Convertir dteday a fecha y crear una marca con hr o un índice combinado equivalente utilizado en el análisis |
| D02 | Tratar season, yr, mnth, hr, holiday, weekday, workingday y weathersit como categóricas o binarias cuando corresponda |
| D03 | Conservar instant únicamente como identificador u orden |
| D04 | No eliminar filas por valores ausentes o duplicados porque no existen |
| D05 | No imputar los 165 huecos horarios. Se permite reindexar solo si quedan marcados como ausentes |
| D06 | Mantener valores extremos de cnt salvo evidencia concreta de error |
| D07 | Mantener cnt y sus componentes, señalando la identidad exacta y evitando usarlos como evidencia independiente |
| D08 | Mantener las variables normalizadas o convertirlas solo mediante los factores documentados |

Para D01, la combinación de fecha y hora puede construirse en memoria y utilizarse durante el análisis. No es obligatorio guardarla como una columna adicional en prepared_data.csv.

## Q4 Riesgos previstos

Siete riesgos de referencia. El tratamiento de riesgos adicionales, detecciones parciales y falsas alarmas se establece en el protocolo.

| ID | Riesgo conocido |
| --- | --- |
| R01 | instant es un identificador secuencial, no una medida analítica |
| R02 | Ocho variables categóricas o binarias están almacenadas como números |
| R03 | cnt es exactamente la suma de casual y registered |
| R04 | temp, atemp, hum y windspeed están normalizadas |
| R05 | Faltan 165 combinaciones fecha-hora en la secuencia completa |
| R06 | weathersit = 4 solo tiene tres observaciones |
| R07 | Existe dependencia temporal y varias variables de calendario son derivadas entre sí |

## Q7 Objetivos visuales

Cinco objetivos, que pueden cubrirse con distintos tipos o combinaciones de gráficos.

| ID | Objetivo |
| --- | --- |
| V01 | Mostrar la evolución agregada de la demanda a lo largo de 2011 y 2012 sin saturar el gráfico |
| V02 | Comparar la demanda media por hora entre días laborables y no laborables |
| V03 | Mostrar un patrón mensual o estacional con categorías ordenadas correctamente |
| V04 | Comparar cnt por situación meteorológica e indicar el bajo tamaño de la categoría 4 |
| V05 | Representar la relación de cnt con temperatura o humedad mediante una técnica legible para datos densos |

## Q8 Contenidos del informe

Doce contenidos esperados, con peso total 22.

| ID | Contenido esperado | Peso |
| --- | --- | --- |
| U01 | Indicar 17379 filas, 17 columnas y el periodo 2011-2012 | 2 |
| U02 | Indicar que no hay celdas ausentes ni filas duplicadas y distinguirlo de los huecos horarios | 2 |
| U03 | Resumir nivel y dispersión de cnt con cifras correctas | 2 |
| U04 | Explicar que los alquileres de usuarios registrados representan aproximadamente el 81,17 % del total | 2 |
| U05 | Mostrar que el total de 2012 supera al de 2011 en aproximadamente un 64,88 %, sin atribuir causalidad | 2 |
| U06 | Identificar el máximo medio a las 17 h y el mínimo a las 4 h | 2 |
| U07 | Distinguir perfiles: máximo a las 17 h en laborables y a las 13 h en no laborables | 2 |
| U08 | Describir diferencias mensuales o estacionales. La temporada 3 tiene la mayor media | 1 |
| U09 | Relacionar peor tiempo con menor demanda y advertir que la categoría 4 solo contiene tres filas | 2 |
| U10 | Describir asociaciones de temperatura y humedad con cnt de forma prudente | 2 |
| U11 | Reconocer que cnt = casual + registered y evitar presentarlo como descubrimiento predictivo | 2 |
| U12 | Mencionar dependencia temporal, datos de una sola ciudad y ausencia de base causal | 1 |