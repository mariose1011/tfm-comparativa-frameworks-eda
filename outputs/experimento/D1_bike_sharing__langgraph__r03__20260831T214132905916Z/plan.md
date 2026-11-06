# Identificación

- **run_id:** `D1_bike_sharing__langgraph__r03__20260831T214132905916Z`
- **framework_id:** `langgraph`
- **dataset_id:** `D1_bike_sharing`
- **contract_version:** `1.0`
- **prompt_version:** `1.0`

# Comprensión inicial

El archivo de entrada es un CSV del dataset `D1_bike_sharing`. La inspección estructural autorizada identifica 17 columnas y una estructura compatible con registros horarios de alquiler de bicicletas. La documentación pública indica que corresponde a datos históricos de Capital Bikeshare en Washington D.C. durante 2011 y 2012, agregados a nivel horario.

La unidad de observación prevista es una hora calendario con las condiciones temporales, meteorológicas y los conteos de alquileres asociados. Las variables `casual`, `registered` y `cnt` representan, según la documentación, conteos de usuarios casuales, registrados y total, respectivamente. `instant` parece ser un índice de registro y no una medida sustantiva.

El análisis se limitará a descripción, calidad, agregaciones, asociaciones y detección prudente de observaciones inusuales. No se entrenarán modelos predictivos ni se inferirán efectos causales. El Analista deberá confirmar el parseo de `dteday`, la cobertura temporal efectiva, la continuidad horaria y la correspondencia exacta entre codificaciones documentadas y valores presentes.

# Preguntas analíticas

1. ¿La tabla tiene la estructura, tipos, fechas y categorías esperados según la documentación pública?
2. ¿Existen ausencias, duplicados, inconsistencias de identificadores, categorías fuera de dominio o interrupciones temporales que condicionen el análisis?
3. ¿Se cumple la identidad documentada entre `cnt`, `casual` y `registered`?
4. ¿Cómo se distribuyen los alquileres totales y sus componentes (`casual` y `registered`) y qué dispersión presentan?
5. ¿Cómo varían los conteos de bicicletas por hora (`hr`), día de la semana (`weekday`), condición laboral (`workingday`), mes (`mnth`), estación (`season`) y año (`yr`)?
6. ¿Qué patrones descriptivos se observan al comparar condiciones meteorológicas (`weathersit`) y variables normalizadas `temp`, `atemp`, `hum` y `windspeed` con `cnt`?
7. ¿Cómo cambia la composición de alquileres entre usuarios `casual` y `registered` según segmentos temporales y laborales?
8. ¿Qué horas, fechas o combinaciones de condiciones presentan conteos extremos o desviaciones destacables respecto de grupos comparables, y hay evidencia para considerarlos errores o valores plausibles?

# Plan por etapas

## E1

**Objetivo:** Cargar el CSV sin modificar el original y confirmar una comprensión inicial de su estructura y unidad de análisis.

**Comprobaciones:**
- Identificar el archivo de entrada, su formato y la documentación pública aplicable.
- Cargar los datos en una estructura tabular de trabajo independiente.
- Confirmar dimensiones, nombres y orden de columnas.
- Inspeccionar una muestra de inicio, final y posiciones internas para comprobar el formato de registros.
- Contrastar la presencia de `hr` y la estructura observada con la documentación del archivo horario.
- Determinar y documentar la unidad de observación sin asumir que todas las horas calendario estén necesariamente presentes.

**Variables o grupos:**
- Todas las columnas, con atención inicial a `instant`, `dteday`, `hr`, `cnt`, `casual` y `registered`.

**Evidencia esperada:**
- Perfil estructural reproducible con dimensiones, listado de columnas, tipos iniciales y muestra de registros.
- Registro de la unidad de análisis utilizada en `statistics.json` y explicación contextual en `report.md`.

**Supuestos o dependencias:**
- La documentación describe el archivo horario; el Analista deberá corroborar que el CSV suministrado corresponde a dicha granularidad.
- La interpretación de `dteday` como fecha requerirá conversión y validación explícitas.

## E2

**Objetivo:** Evaluar tipos, integridad, dominios, cobertura temporal y riesgos de calidad relevantes para un EDA horario.

**Comprobaciones:**
- Examinar tipos observados y convertir analíticamente `dteday` a fecha si el parseo es completo y no ambiguo.
- Cuantificar valores ausentes por columna y detectar representaciones no estándar de ausencia cuando sean plausibles.
- Verificar duplicados de fila completa, unicidad de `instant` y posibles duplicados de la clave temporal compuesta por fecha y hora.
- Comprobar dominios documentados: `season`, `yr`, `mnth`, `hr`, `holiday`, `weekday`, `workingday` y `weathersit`.
- Revisar coherencia entre fecha, `yr`, `mnth` y `weekday`; documentar la convención de codificación de `weekday` si puede inferirse de forma verificable.
- Evaluar rangos, no negatividad e integridad numérica de `casual`, `registered`, `cnt`, `temp`, `atemp`, `hum` y `windspeed`.
- Contrastar la identidad `cnt = casual + registered`.
- Determinar el intervalo entre la primera y última fecha, número de fechas distintas, registros por fecha y posibles huecos horarios o diarios.
- Identificar extremos estadísticos de conteos y meteorología como candidatos a revisión, sin clasificarlos automáticamente como errores.

**Variables o grupos:**
- Identificadores: `instant`, `dteday`, `hr`.
- Calendario: `season`, `yr`, `mnth`, `holiday`, `weekday`, `workingday`.
- Meteorología: `weathersit`, `temp`, `atemp`, `hum`, `windspeed`.
- Conteos: `casual`, `registered`, `cnt`.

**Evidencia esperada:**
- Resultados estructurados de ausencias, duplicados, cardinalidades, dominios, rangos, identidad y continuidad temporal.
- `issues.json` con las comprobaciones realizadas y, solo si hay evidencia, incidencias o riesgos clasificados con decisión y efecto potencial.

**Supuestos o dependencias:**
- Los límites de las variables normalizadas se contrastarán con la documentación; cualquier diferencia deberá investigarse antes de considerarla inválida.
- La falta de alguna hora puede ser un rasgo de cobertura histórica y no un error; se documentará la incertidumbre.

## E3

**Objetivo:** Crear `prepared_data.csv` como copia de trabajo trazable, conservando el original y aplicando únicamente decisiones justificadas.

**Comprobaciones:**
- Mantener una copia separada del archivo fuente sin sobrescribirlo.
- Convertir `dteday` a un tipo de fecha para análisis y serializarla de manera ISO no ambigua en la salida preparada.
- Conservar como categóricas analíticas las variables codificadas cuyo significado está documentado, sin alterar indebidamente sus códigos fuente.
- Decidir el tratamiento de ausencias, duplicados, categorías inválidas, inconsistencias de identidad y valores fuera de rango conforme a los resultados de E2.
- Distinguir extremos plausibles de errores antes de excluir filas; priorizar la conservación cuando no exista evidencia de invalidez.
- Considerar variables derivadas de bajo riesgo analítico solo si clarifican los resultados, por ejemplo etiquetas descriptivas de categorías documentadas o una proporción de composición de usuarios cuando su denominador sea válido.
- Comparar filas y columnas antes y después, y documentar cada transformación o conservación deliberada.

**Variables o grupos:**
- `dteday` para conversión de tipo.
- Categorías temporales y meteorológicas para etiquetas o interpretación.
- `casual`, `registered` y `cnt` para comprobaciones y, si procede, composición.

**Evidencia esperada:**
- `prepared_data.csv` legible y separado del original.
- Registro `preparation` en `statistics.json`, con cambios identificados como `TR-NNN`, justificación, columnas afectadas y comparación antes-después.

**Supuestos o dependencias:**
- Las decisiones dependen de los hallazgos de E2.
- Si no se justifican cambios sustantivos, la copia preparada podrá mantener todas las observaciones y columnas, explicando expresamente esa decisión.

## E4

**Objetivo:** Describir de forma reproducible la distribución y composición de los alquileres y las variables meteorológicas relevantes.

**Comprobaciones:**
- Calcular conteos, frecuencias y proporciones para categorías temporales, laborales y meteorológicas.
- Resumir `cnt`, `casual` y `registered` mediante medidas adecuadas de centralidad, dispersión, cuantiles y mínimos/máximos.
- Resumir `temp`, `atemp`, `hum` y `windspeed` respetando que son escalas normalizadas documentadas.
- Calcular estadísticas de alquileres por grupos interpretables, como `yr`, `season`, `mnth`, `hr`, `workingday`, `holiday` y `weathersit`.
- Describir la contribución relativa de `casual` y `registered` al total global y por segmentos relevantes, si la identidad de conteos se valida o se documenta cualquier discrepancia.

**Variables o grupos:**
- Conteos: `cnt`, `casual`, `registered`.
- Tiempo y calendario: `yr`, `season`, `mnth`, `hr`, `weekday`, `workingday`, `holiday`.
- Meteorología: `weathersit`, `temp`, `atemp`, `hum`, `windspeed`.

**Evidencia esperada:**
- Análisis `STAT-NNN` estructurados con población, método, resultados y una interpretación descriptiva prudente.
- Tablas o resúmenes trazables para usar en el informe.

**Supuestos o dependencias:**
- Las estadísticas se calcularán sobre la población preparada y se indicarán los filtros si hubiera exclusiones justificadas.
- Las etiquetas de estaciones y tiempo meteorológico deberán seguir la documentación disponible.

## E5

**Objetivo:** Analizar patrones temporales, diferencias entre segmentos y asociaciones descriptivas relevantes, evitando inferencias causales.

**Comprobaciones:**
- Agregar los conteos por fecha, mes, estación y año para caracterizar evolución y estacionalidad.
- Comparar perfiles horarios de `cnt`, `casual` y `registered` entre `workingday` y no laborables; considerar `weekday` o `holiday` si los tamaños de grupo permiten interpretaciones estables.
- Comparar alquileres por categorías de `weathersit` y por segmentos de calendario, indicando tamaños muestrales.
- Examinar asociaciones numéricas entre `cnt` y variables meteorológicas, con medidas y gráficos adecuados a distribuciones y escalas; revisar también la redundancia esperable entre `temp` y `atemp`.
- Verificar y cuantificar la identidad entre los tres conteos, tratándola como relación definicional y no como asociación independiente.
- Identificar fechas u horas con desviaciones respecto de agregaciones comparables, empleando reglas transparentes y conservadoras si se realiza un análisis de anomalías descriptivo.

**Variables o grupos:**
- Agregaciones temporales: `dteday`, `yr`, `mnth`, `season`, `hr`.
- Segmentos: `workingday`, `holiday`, `weekday`, `weathersit`.
- Relaciones: `cnt`, `casual`, `registered`, `temp`, `atemp`, `hum`, `windspeed`.

**Evidencia esperada:**
- Resultados `STAT-NNN` para agregaciones temporales, comparaciones de segmentos, asociaciones y comprobaciones de redundancia o identidad.
- Interpretaciones que describan diferencias observadas y eviten atribuir causalidad a calendario o clima.

**Supuestos o dependencias:**
- La interpretación de tendencias temporales depende de confirmar el orden y cobertura de fechas en E2.
- Las asociaciones meteorológicas pueden estar confundidas por estacionalidad, hora y otros factores no analizados; se explicitará esta limitación.

## E6

**Objetivo:** Producir figuras legibles que respondan a preguntas analíticas concretas y estén respaldadas por resultados estructurados.

**Comprobaciones:**
- Generar solo gráficos pertinentes a los hallazgos de E4 y E5.
- Incluir títulos, ejes, unidades o aclaraciones de escala normalizada, leyendas y codificación de categorías cuando corresponda.
- Gestionar la alta densidad de la serie horaria mediante agregación temporal o visualizaciones complementarias, sin ocultar el intervalo estudiado.
- Comprobar que los PNG se abren, no están vacíos y quedan registrados como `FIG-NNN` con vínculos a sus análisis fuente.
- Citar cada figura utilizada en el informe mediante ruta relativa e identificador.

**Variables o grupos:**
- Series y agregaciones de `dteday` con `cnt`.
- Perfiles de `hr` según `workingday`.
- `weathersit` y `cnt`.
- Variables meteorológicas frente a `cnt`.
- Composición `casual` y `registered` cuando resulte informativa y esté validada.

**Evidencia esperada:**
- Archivos PNG válidos en `figures/`.
- Registro de cada figura en `statistics.json` con objetivo, variables y `source_analysis_ids`.
- Referencias cruzadas en `report.md`.

**Supuestos o dependencias:**
- La selección final dependerá de los patrones y calidad confirmados en las etapas anteriores.
- No se representarán valores como causalidad ni se usarán agregaciones que mezclen grupos con significados incompatibles.

## E7

**Objetivo:** Consolidar riesgos, anomalías y límites de interpretación mediante evidencia cuantificada y decisiones explícitas.

**Comprobaciones:**
- Registrar todas las comprobaciones de calidad, incluso cuando no encuentren problemas.
- Evaluar incidencias detectadas o sospechadas en ausencias, duplicados, tipos, categorías, rangos, identidades y cobertura temporal.
- Distinguir observaciones extremas de `cnt` o condiciones meteorológicas de posibles errores usando contexto temporal, consistencia interna y reglas descriptivas transparentes.
- Identificar riesgos analíticos derivados de variables codificadas, datos agregados, escalas normalizadas, potenciales huecos horarios o falta de metadatos adicionales.
- Para cada incidencia respaldada, documentar columnas, recuento de filas, muestra limitada de identificadores si procede, acción, efecto potencial e incertidumbre.

**Variables o grupos:**
- Todas las variables de calidad de E2, con énfasis en `instant`, `dteday`, `hr`, `cnt`, `casual`, `registered` y las categorías codificadas.

**Evidencia esperada:**
- `issues.json` válido con `checks_performed` no vacío y referencias a los `STAT-NNN` pertinentes.
- Lista de anomalías o riesgos únicamente cuando la evidencia lo justifique; si no se confirman problemas, documentación explícita de las comprobaciones realizadas.

**Supuestos o dependencias:**
- La documentación pública no permite atribuir automáticamente un valor atípico a un evento externo; no se harán tales atribuciones.
- La ausencia de evidencia de error no demostrará que una observación sea completamente libre de incertidumbre.

## E8

**Objetivo:** Integrar el EDA en un informe reproducible, verificable y prudente, coherente con las salidas estructuradas.

**Comprobaciones:**
- Redactar `report.md` con las secciones obligatorias y referencias resolubles a `STAT-NNN`, `ISSUE-NNN` y `FIG-NNN`.
- Explicar el dataset, unidad de observación, cobertura analizada y alcance no predictivo/no causal.
- Resumir calidad, preparación y cualquier decisión de conservación, transformación o exclusión.
- Presentar los hallazgos principales con cifras, agregaciones y figuras de respaldo.
- Diferenciar resultados observados, interpretaciones descriptivas y explicaciones no verificadas.
- Declarar limitaciones de cobertura, agregación, codificaciones, escalas normalizadas y variables no disponibles cuando afecten la interpretación.
- Revisar coherencia entre dimensiones de `prepared_data.csv`, perfiles de `statistics.json`, incidencias de `issues.json`, figuras y referencias del informe.

**Variables o grupos:**
- Hallazgos seleccionados de todas las etapas, priorizando conteos de alquileres, patrones temporales, segmentos laborales y meteorología.

**Evidencia esperada:**
- `report.md` final legible y trazable.
- Conjunto coherente de `prepared_data.csv`, `statistics.json`, `issues.json`, figuras y referencias internas válidas.

**Supuestos o dependencias:**
- Depende de la finalización de E1 a E7 y de que toda cifra citada tenga respaldo estructurado.
- El informe no sustituirá los archivos de evidencia ni introducirá resultados que no consten en ellos.

# Visualizaciones previstas

- **Evolución temporal agregada de `cnt`:** mostrar la trayectoria de alquileres a una granularidad temporal legible para examinar variación, estacionalidad y posibles periodos destacados sin sobrecargar una serie horaria completa. Variables: `dteday`, `cnt`, y opcionalmente `yr`.
- **Perfil horario de alquileres por condición laboral:** comparar el patrón de `cnt` a través de `hr` entre `workingday` y no laborables; si es útil, complementar con la composición de `casual` y `registered`. Variables: `hr`, `workingday`, `cnt`, `casual`, `registered`.
- **Distribución o comparación de `cnt` por `weathersit`:** describir diferencias entre categorías meteorológicas, mostrando dispersión y tamaños de grupo de una forma adecuada. Variables: `weathersit`, `cnt`.
- **Relación entre alquileres y una o más variables meteorológicas:** representar asociaciones descriptivas de `cnt` con `temp`, `hum` o `windspeed`, usando transparencia, agregación o estratificación si la densidad lo exige. Variables: `cnt`, `temp`, `hum`, `windspeed`, y opcionalmente `workingday` o `season`.
- **Composición de usuarios en segmentos temporales seleccionados:** si la identidad entre conteos se confirma, mostrar cómo se distribuyen `casual` y `registered` por hora, estación o año para contextualizar el total. Variables: `casual`, `registered`, `cnt` y un segmento temporal validado.

La selección final deberá basarse en los resultados obtenidos: podrán omitirse figuras redundantes, sustituirse por opciones más legibles o añadirse una visualización específica de calidad si se detecta un riesgo relevante.

# Supuestos y riesgos

- La documentación pública describe el dataset horario; el Analista deberá verificar que la granularidad observada, fechas y variable `hr` son consistentes con esa descripción.
- `dteday` se observa inicialmente como texto y deberá convertirse con validación de parseo completo antes de usarla en cálculos temporales.
- Las variables `season`, `yr`, `holiday`, `weekday`, `workingday` y `weathersit` son códigos numéricos con significado categórico; no deben tratarse automáticamente como escalas continuas.
- La documentación establece escalas normalizadas para `temp`, `atemp`, `hum` y `windspeed`; los análisis deberán aclarar esas unidades y no suponer medidas físicas directas sin transformación documentada.
- La identidad `cnt = casual + registered` debe comprobarse en todas las filas antes de usar proporciones o composición.
- `instant` es un índice de registro y no debe utilizarse como variable explicativa sustantiva; solo podrá servir para trazabilidad, orden o comprobaciones de unicidad.
- Una cobertura temporal aparentemente completa o incompleta deberá verificarse mediante fechas y horas realmente presentes, no solo mediante el tamaño de la tabla.
- Picos o valores extremos de alquileres pueden ser comportamientos reales. No se eliminarán ni se atribuirán a eventos concretos sin evidencia interna suficiente.
- Las comparaciones de alquileres por clima, calendario o condición laboral son asociaciones descriptivas. Factores temporales correlacionados y variables no observadas limitan cualquier interpretación explicativa.
- Los datos están agregados por hora y no incluyen trayectos, estaciones de bicicletas, duración de alquiler ni atributos individuales; estas ausencias restringen el alcance de las conclusiones.

# Criterios de finalización

- Se ha cargado el CSV original sin modificarlo y se ha documentado su estructura, archivo, unidad de análisis y relación con la documentación pública.
- Se han evaluado y cuantificado tipos, ausencias, duplicados, identificadores, categorías, rangos, fechas, continuidad temporal e identidad de conteos, dejando resultados `STAT-NNN` y comprobaciones `CHK-NNN`.
- Existe `prepared_data.csv` válido, separado del original, con fecha serializada de forma no ambigua y todas las diferencias respecto a la fuente justificadas mediante `TR-NNN`.
- `statistics.json` cumple el esquema requerido, perfila todas las columnas finales, registra la preparación y conserva estadísticas descriptivas, agregaciones, relaciones y figuras trazables.
- Se han descrito conteos, dispersión, cuantiles y frecuencias de las variables y grupos pertinentes, indicando población, filtro o agrupación.
- Se han analizado varias relaciones o agregaciones relevantes: al menos patrones temporales, segmentación por condición laboral o calendario, comparación meteorológica e identidad/composición de conteos cuando sea válida.
- Existe al menos una figura PNG legible y pertinente; todas las figuras están registradas y referenciadas de forma consistente.
- `issues.json` documenta comprobaciones de calidad y cualquier incidencia respaldada, con decisiones y efectos potenciales; no etiqueta extremos como errores sin evidencia.
- `report.md` incluye todas las secciones obligatorias, presenta los resultados principales con referencias válidas y diferencia descripción, interpretación y limitaciones.
- Las dimensiones, identificadores, rutas relativas, referencias y archivos obligatorios son coherentes entre sí y respetan el contrato de salida.