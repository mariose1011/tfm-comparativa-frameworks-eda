# Ficha de referencia D1 — Bike Sharing (datos horarios)

**Versión:** 0.1
**Uso:** valores y criterios de referencia para la evaluación 
**Acceso durante el experimento:** no disponible para los agentes

## 1. Identificación y procedencia

- Dataset: Bike Sharing.
- Repositorio: UCI Machine Learning Repository.
- Página: https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset
- DOI del dataset: `10.24432/C5W894`.
- Licencia indicada por UCI: CC BY 4.0.
- Fecha de recuperación: 4 de agosto de 2026.
- Archivo utilizado: `datasets/experiment_inputs/D1_bike_sharing/hour.csv`.
- SHA-256: `E03DE4EE4EF4DC376AC6E04BF829673C6269E8EBA5C60FA121640FA2F829504F`.
- Archivo de documentación facilitado al agente: `Readme.txt` del paquete original.

El catálogo web de UCI muestra 17.389 instancias, pero el archivo horario original y su `Readme.txt` contienen 17.379 registros. Para el experimento prevalecen el archivo congelado y su hash.

## 2. Objetivo experimental del dataset

El agente deberá realizar un EDA tabular completo sobre los alquileres horarios de bicicletas de Capital Bikeshare en Washington D. C. durante 2011 y 2012.

No se solicita entrenar ni comparar modelos predictivos. El análisis debe cubrir estructura y tipos, calidad, preparación, estadística descriptiva, relaciones, patrones temporales, visualizaciones, riesgos o anomalías y un informe final respaldado por las salidas generadas.

Este dataset representa el caso relativamente limpio del experimento. Se valorará tanto que el agente detecte sus riesgos analíticos como que evite transformaciones innecesarias.

## 3. Estructura esperada

- Filas: 17.379.
- Columnas: 17.
- Fechas distintas: 731.
- Inicio: 1 de enero de 2011 a las 00:00.
- Fin: 31 de diciembre de 2012 a las 23:00.
- Celdas ausentes: 0.
- Filas completamente duplicadas: 0.
- Identificadores `instant` duplicados: 0.
- Combinaciones fecha-hora observadas: 17.379.
- Combinaciones de una secuencia horaria completa: 17.544.
- Huecos horarios: 165; 115 en 2011 y 50 en 2012.

Los huecos horarios no son valores nulos dentro de filas existentes. No deben mezclarse ambas comprobaciones.

## 4. Diccionario operativo de variables

| Variable | Papel y tratamiento esperado |
| --- | --- |
| `instant` | Identificador secuencial de 1 a 17.379. Puede conservarse para trazabilidad u orden, pero no debe tratarse como medida explicativa. |
| `dteday` | Fecha. Debe convertirse a tipo fecha. Puede combinarse con `hr` para crear una marca temporal. |
| `season` | Categoría codificada: 1 primavera, 2 verano, 3 otoño y 4 invierno, según el `Readme.txt` congelado. |
| `yr` | Categoría temporal: 0 corresponde a 2011 y 1 a 2012. |
| `mnth` | Mes, de 1 a 12. Debe tratarse como categoría ordenada o componente temporal. |
| `hr` | Hora, de 0 a 23. Debe tratarse como categoría ordenada o componente temporal. |
| `holiday` | Indicador binario de festivo. |
| `weekday` | Día de la semana codificado de 0 a 6. Si se asignan nombres, deben verificarse contra `dteday`. |
| `workingday` | 1 cuando no es fin de semana ni festivo; 0 en caso contrario. |
| `weathersit` | Categoría meteorológica ordinal de 1, mejor tiempo, a 4, peor tiempo. No debe tratarse como magnitud continua sin justificación. |
| `temp` | Temperatura normalizada. El `Readme.txt` indica que se dividió entre 41. |
| `atemp` | Sensación térmica normalizada. El `Readme.txt` indica que se dividió entre 50. |
| `hum` | Humedad relativa normalizada, dividida entre 100. |
| `windspeed` | Velocidad del viento normalizada, dividida entre 67. |
| `casual` | Número de alquileres de usuarios ocasionales en cada hora. |
| `registered` | Número de alquileres de usuarios registrados en cada hora. |
| `cnt` | Total horario; se cumple exactamente `cnt = casual + registered`. |

Cuando exista alguna diferencia entre descripciones secundarias y el paquete descargado, se utilizará como referencia el `Readme.txt` congelado junto al archivo.

## 5. Valores descriptivos principales

| Medida | Referencia |
| --- | ---: |
| Alquileres totales (`cnt`) | 3.292.679 |
| Media horaria | 189,463088 |
| Mediana horaria | 142 |
| Desviación típica muestral | 181,387599 |
| Primer cuartil | 40 |
| Tercer cuartil | 281 |
| Mínimo | 1 |
| Máximo | 977 |
| Alquileres de usuarios ocasionales | 620.017, el 18,8302 % |
| Alquileres de usuarios registrados | 2.672.662, el 81,1698 % |

### Comparación anual

| Año | Filas | Total `cnt` | Media horaria | Mediana |
| --- | ---: | ---: | ---: | ---: |
| 2011 (`yr = 0`) | 8.645 | 1.243.103 | 143,794448 | 109 |
| 2012 (`yr = 1`) | 8.734 | 2.049.576 | 234,666361 | 191 |

El total de 2012 supera al de 2011 en un 64,875799 %. La media horaria aumenta un 63,195704 %. Estas diferencias son descriptivas y no demuestran causalidad.

### Patrones de referencia

- La mayor media por hora corresponde a las 17:00: 461,452055.
- La segunda mayor corresponde a las 18:00: 425,510989.
- La menor media corresponde a las 04:00: 6,352941.
- En días laborables, el máximo medio se produce a las 17:00: 525,290581.
- En días no laborables, el máximo medio se produce a las 13:00: 372,731602.
- La temporada 3 presenta la mayor media: 236,016237.
- Septiembre presenta la mayor media mensual: 240,773138; junio es muy próximo, con 240,515278.
- `weathersit = 1` presenta una media de 204,869272.
- `weathersit = 3` presenta una media de 111,579281.
- `weathersit = 4` contiene únicamente tres observaciones; su media no debe generalizarse.
- Correlación de Pearson entre `temp` y `cnt`: 0,404772.
- Correlación de Pearson entre `hum` y `cnt`: -0,322911.

Las correlaciones sirven como comprobaciones reproducibles, pero no obligan a utilizar Pearson como única medida ni justifican inferencias causales.

## 6. Reglas de tolerancia para Q2

- Conteos, fechas, categorías extremas e identidades: coincidencia exacta.
- Medias, medianas y desviaciones: tolerancia absoluta de 0,01, salvo que se indique 0,05 para medias agrupadas.
- Correlaciones: tolerancia absoluta de 0,005.
- Proporciones expresadas entre 0 y 1: tolerancia absoluta de 0,001.
- Porcentajes: tolerancia de 0,1 puntos porcentuales.
- Se admiten redondeos y resultados obtenidos mediante operaciones sencillas con cifras ya generadas por la ejecución, conforme al protocolo de evaluación.

Las 26 comprobaciones y sus pesos están definidos en `evaluation_spec.json`. Los valores completos se encuentran en `reference_values.json`.

## 7. Decisiones válidas de preparación y limpieza

Se consideran adecuadas las siguientes decisiones, siempre que queden registradas:

1. Combinar `dteday` y `hr` para disponer de la fecha y hora de cada observación. Puede utilizarse una marca temporal o un índice equivalente construido en memoria, sin exigir una columna adicional en el CSV.
2. Tratar `season`, `yr`, `mnth`, `hr`, `holiday`, `weekday`, `workingday` y `weathersit` como variables categóricas, binarias u ordenadas según su significado.
3. Conservar `instant` únicamente como identificador o índice de orden.
4. No eliminar filas por nulos o duplicados, porque no existen.
5. No imputar los 165 huecos horarios. Se permite reindexar para estudiar continuidad si los nuevos huecos quedan marcados explícitamente como ausentes.
6. Mantener los valores altos de demanda salvo evidencia específica de error; pueden representar horas reales de alta actividad.
7. Conservar `cnt`, `casual` y `registered`, señalando su relación determinista y evitando tratarlos como evidencias independientes.
8. Mantener las variables ambientales normalizadas o convertirlas mediante los factores documentados, dejando registrada la transformación.

También podrán aceptarse soluciones equivalentes que preserven los datos y estén justificadas.

## 8. Decisiones incorrectas o perjudiciales

- Eliminar automáticamente valores altos de `cnt` por superar un umbral IQR o z-score.
- Tratar códigos de estación, día o meteorología como medidas continuas.
- Presentar variables normalizadas como grados, porcentajes o velocidad original sin convertirlas.
- Utilizar la correlación entre `registered` y `cnt` como hallazgo sustantivo, ignorando que `registered` forma parte de `cnt`.
- Rellenar horas ausentes con cero o interpolación sin advertirlo y justificarlo.
- Eliminar columnas o filas sin mantener trazabilidad de la decisión.
- Afirmar relaciones causales a partir del EDA observacional.

## 9. Problemas y riesgos analíticos conocidos para Q4

1. `instant` es un identificador secuencial.
2. Ocho variables categóricas o binarias están almacenadas como números.
3. `cnt` es exactamente la suma de `casual` y `registered`.
4. Las cuatro variables ambientales están normalizadas.
5. Existen 165 huecos en la secuencia fecha-hora, aunque no haya celdas nulas.
6. La categoría meteorológica 4 solo tiene tres observaciones.
7. Las observaciones presentan dependencia temporal y varias variables de calendario derivan de la misma fecha.

Para considerar detectado un elemento, deberá existir una afirmación explícita y correcta en `issues.json`, `report.md` o en otra salida trazable. Las falsas alarmas se contabilizarán en la precisión de Q4.

## 10. Unidades de información esperadas para Q8

| Código | Peso | Contenido esperado |
| --- | ---: | --- |
| U01 | 2 | Estructura de 17.379 × 17 y periodo 2011-2012. |
| U02 | 2 | Ausencia de nulos y duplicados, distinguiéndola de los 165 huecos horarios. |
| U03 | 2 | Nivel y dispersión general de `cnt` con cifras correctas. |
| U04 | 2 | Los alquileres de usuarios registrados representan aproximadamente el 81,17 % del total. |
| U05 | 2 | Total de 2012 aproximadamente un 64,88 % superior al de 2011, sin explicación causal no respaldada. |
| U06 | 2 | Máximo medio a las 17 h y mínimo a las 4 h. |
| U07 | 2 | Diferencia del perfil laborable: máximo a las 17 h frente a las 13 h en no laborables. |
| U08 | 1 | Patrón mensual o estacional; la temporada 3 presenta la mayor media. |
| U09 | 2 | Menor demanda con peor situación meteorológica y cautela por las tres filas de categoría 4. |
| U10 | 2 | Asociación positiva moderada con temperatura y negativa con humedad, formulada con prudencia. |
| U11 | 2 | Identidad `cnt = casual + registered` y su implicación para el análisis. |
| U12 | 1 | Limitaciones: dependencia temporal, una sola ciudad y ausencia de base causal. |

La cobertura se calculará como suma de pesos correctamente cubiertos dividida entre la suma total de pesos. Un contenido parcialmente correcto recibirá la mitad de su peso. Una unidad incorrecta no se considerará cubierta y podrá afectar además a Q9.

Los análisis adicionales no aumentarán Q8, aunque sí podrán mejorar Q5 o Q6 cuando sean pertinentes y estén respaldados.

## 11. Objetivos visuales para Q7

1. **Evolución temporal:** mostrar la evolución agregada durante 2011 y 2012 sin generar una serie ilegible de 17.379 puntos.
2. **Perfil horario:** comparar la demanda media por hora entre días laborables y no laborables.
3. **Estacionalidad:** representar el patrón mensual o por temporadas, manteniendo el orden natural de las categorías.
4. **Meteorología:** comparar la demanda entre situaciones meteorológicas y advertir el tamaño mínimo de la categoría 4.
5. **Relaciones ambientales:** mostrar la relación de la demanda con temperatura o humedad mediante dispersión con transparencia, agregación, binning, hexbin u otra solución legible.

No se exige un tipo concreto de gráfico. Se aceptarán alternativas equivalentes si cumplen el objetivo, utilizan datos correctos y están bien integradas en el informe.

## 12. Etapas y archivos obligatorios

Las ocho etapas del EDA deberán dejar evidencia en las trazas o salidas:

1. Carga e inspección inicial.
2. Estructura, tipos y calidad.
3. Preparación y decisiones de análisis.
4. Estadística descriptiva.
5. Variables, agregaciones y relaciones.
6. Visualizaciones.
7. Problemas, riesgos y anomalías.
8. Informe final.

Salidas previstas por el contrato común:

- `plan.md`.
- `prepared_data.csv`.
- `statistics.json`.
- `issues.json`.
- Directorio `figures/`.
- `report.md`.
- `trace.jsonl`.

## 13. Aplicación de las métricas

- **Q1:** evidencias de las ocho etapas y archivos obligatorios.
- **Q2:** comprobaciones de `evaluation_spec.json` contra `reference_values.json`.
- **Q3:** decisiones de preparación comparadas con las secciones 7 y 8.
- **Q4:** precisión, cobertura y F1 respecto a los siete riesgos de la sección 9.
- **Q5 y Q6:** rúbrica manual sobre profundidad del EDA e interpretación.
- **Q7:** media de las puntuaciones de los cinco objetivos visuales, multiplicada por 25 para expresarla de 0 a 100.
- **Q8:** cobertura ponderada de las doce unidades de información.
- **Q9:** fidelidad de las afirmaciones comprobables respecto a datos, estadísticas, gráficos y trazas.
- **Q10:** claridad y coherencia del informe.