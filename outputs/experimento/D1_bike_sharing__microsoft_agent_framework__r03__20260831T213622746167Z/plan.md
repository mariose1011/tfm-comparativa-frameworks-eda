# Identificación

- **run_id:** D1_bike_sharing__microsoft_agent_framework__r03__20260831T213622746167Z
- **framework_id:** microsoft_agent_framework
- **dataset_id:** D1_bike_sharing
- **contract_version:** 1.0
- **prompt_version:** 1.0

# Comprensión inicial

El archivo de entrada es un CSV correspondiente al nivel horario del dataset Bike Sharing, documentado como `hour.csv`. La inspección estructural autorizada identifica 17 columnas y una tabla de observaciones horarias, con variables de fecha y calendario, condiciones meteorológicas normalizadas y recuentos de alquileres.

Según la documentación pública, cada fila debe representar un intervalo horario agregado del sistema Capital Bikeshare de Washington D.C. durante 2011–2012, con `cnt` como total de alquileres y `casual` y `registered` como sus componentes. La documentación indica que `instant` es un índice de registro, mientras que `dteday` y `hr` deberían determinar el momento de la observación.

El alcance será descriptivo y exploratorio: calidad, distribución, estacionalidad, patrones temporales, composición de usuarios y asociaciones descriptivas con calendario y meteorología. No se entrenarán modelos ni se establecerán relaciones causales.

Aspectos que deben confirmarse durante el análisis:

- Que `dteday` pueda convertirse íntegramente a fecha y que su combinación con `hr` identifique de forma coherente cada observación horaria.
- Que los códigos de `season`, `yr`, `holiday`, `weekday`, `workingday` y `weathersit` respeten los dominios documentados.
- Que las identidades entre `casual`, `registered` y `cnt` se cumplan.
- Que la cobertura temporal sea continua o, si no lo es, que los huecos queden identificados y no se confundan con demanda cero.
- Que las variables meteorológicas estén efectivamente en sus escalas normalizadas documentadas y que no existan valores incompatibles con ellas.

# Preguntas analíticas

1. ¿Cuál es la cobertura temporal real de las observaciones horarias y existen horas, días o periodos ausentes?
2. ¿Qué calidad presentan los tipos, valores ausentes, identificadores, categorías codificadas y rangos respecto de la documentación?
3. ¿Cómo se distribuyen `cnt`, `casual` y `registered`, y cuál es la contribución relativa de los dos tipos de usuario?
4. ¿Cómo varía descriptivamente el volumen de alquileres por `hr`, `workingday`, `weekday`, `holiday`, `season`, `mnth` y `yr`?
5. ¿Qué diferencias descriptivas hay entre los patrones horarios de días laborables y no laborables?
6. ¿Cómo se asocian las condiciones meteorológicas y las variables normalizadas `temp`, `atemp`, `hum` y `windspeed` con los recuentos de alquiler?
7. ¿Existen registros temporalmente inusuales o valores extremos que requieran revisión, y hay evidencia para tratarlos como errores o deben conservarse como observaciones plausibles?
8. ¿Qué riesgos de interpretación derivan de la agregación horaria, de las variables codificadas, de la cobertura temporal y de la ausencia de información contextual externa?

# Plan por etapas

## E1

**Objetivo:** Confirmar la carga no destructiva del CSV, su estructura básica y la unidad de análisis antes de realizar transformaciones.

**Comprobaciones:**
- Registrar el archivo de entrada, formato CSV, dimensiones, nombres y orden de columnas.
- Inspeccionar una muestra inicial y final, junto con ejemplos internos, para verificar la estructura de una observación.
- Contrastar la tabla con la documentación pública, en particular la distinción entre archivos diarios y horarios.
- Confirmar que el archivo analizado contiene la variable `hr`, esperada en el nivel horario.
- Describir provisionalmente la unidad de análisis como una observación agregada por fecha y hora, dejando explícita cualquier incertidumbre que surja al validar la clave temporal.

**Variables o grupos:** Todas las columnas; especialmente `instant`, `dteday`, `hr`, `cnt`, `casual` y `registered`.

**Evidencia esperada:**
- Perfil del archivo original en `statistics.json`, con dimensiones, columnas, tipos observados y unidad de análisis.
- Una entrada de análisis E1 que documente la carga y la estructura inicial.
- Referencias trazables en el informe final.

**Supuestos o dependencias:**
- La documentación pública describe correctamente el archivo horario seleccionado.
- La inspección inicial indica que el CSV contiene las columnas esperadas, pero la coherencia semántica debe verificarse con el contenido completo.

## E2

**Objetivo:** Evaluar tipos, integridad, consistencia y riesgos de calidad que puedan condicionar el análisis.

**Comprobaciones:**
- Medir valores ausentes por columna y comprobar valores vacíos o codificaciones ambiguas.
- Evaluar duplicados completos, unicidad de `instant` y duplicidad de la combinación temporal derivada de `dteday` y `hr`.
- Convertir `dteday` de forma controlada para comprobar fechas inválidas, cobertura, orden y posibles huecos temporales.
- Verificar los dominios documentados de `season`, `yr`, `mnth`, `hr`, `holiday`, `weekday`, `workingday` y `weathersit`.
- Revisar coherencia entre fecha, año, mes, día de la semana y los indicadores `holiday` y `workingday` cuando pueda evaluarse sin fuentes externas.
- Examinar rangos, signos, valores cero y distribución básica de `temp`, `atemp`, `hum`, `windspeed`, `casual`, `registered` y `cnt`.
- Comprobar la identidad documentada `cnt = casual + registered`.
- Identificar extremos mediante métodos descriptivos adecuados y revisarlos junto con el contexto temporal y los límites documentados, sin eliminarlos automáticamente.

**Variables o grupos:** `instant`, `dteday`, `yr`, `mnth`, `hr`, `season`, `weekday`, `holiday`, `workingday`, `weathersit`, `temp`, `atemp`, `hum`, `windspeed`, `casual`, `registered` y `cnt`.

**Evidencia esperada:**
- Análisis estructurados E2 para ausencias, duplicados, rangos, dominios categóricos, identidad de conteos y cobertura temporal.
- `issues.json` con todas las comprobaciones realizadas y con incidencias solamente cuando haya evidencia.
- Muestras acotadas de identificadores o filas afectadas si se detectan problemas verificables.

**Supuestos o dependencias:**
- La codificación exacta de `weekday` no se detalla en la documentación pública; deberá inferirse y contrastarse con `dteday` sin asumir nombres de días si no puede verificarse.
- La documentación define escalas normalizadas de meteorología, pero el análisis debe distinguir límites documentados de errores demostrados.
- La ausencia de registros horarios puede reflejar cobertura incompleta y no necesariamente alquileres nulos.

## E3

**Objetivo:** Construir una copia de trabajo trazable y adecuada para EDA, preservando el archivo original y evitando tratamientos automáticos injustificados.

**Comprobaciones:**
- Crear `prepared_data.csv` como copia separada del original.
- Convertir `dteday` a fecha para el análisis y serializarla de forma ISO no ambigua en la copia preparada.
- Mantener los códigos originales de las variables categóricas y, si aporta claridad, añadir variables derivadas etiquetadas o de fecha/hora sin reemplazar las columnas fuente.
- Decidir el tratamiento de ausencias, duplicados, registros inválidos y extremos en función de las verificaciones de E2.
- Conservar los extremos plausibles y todos los registros válidos; documentar expresamente una decisión de conservación si no se justifican exclusiones.
- Considerar variables derivadas interpretables, como una marca temporal basada en `dteday` y `hr`, etiquetas descriptivas de códigos documentados o proporciones de composición de usuarios, solo si no inducen divisiones inválidas ni confunden el origen de los datos.
- Comparar dimensiones y columnas antes y después, documentando toda alteración.

**Variables o grupos:** Todas las variables fuente; potencialmente una variable temporal derivada y etiquetas descriptivas para `season` y `weathersit`.

**Evidencia esperada:**
- `prepared_data.csv` legible y separado del original.
- Perfil de columnas original-preparado y dimensiones antes-después en `statistics.json`.
- Registro de transformaciones con identificadores `TR-NNN`, justificación, columnas y filas afectadas.
- Referencias a decisiones de retención, corrección o exclusión en `issues.json` cuando corresponda.

**Supuestos o dependencias:**
- La preparación dependerá de los hallazgos de E2; no se presupone que haya filas que eliminar o valores que imputar.
- Las etiquetas derivadas no deben sustituir ni alterar los códigos fuente documentados.
- `instant` debe preservarse como identificador trazable, no interpretarse como medida sustantiva.

## E4

**Objetivo:** Resumir la distribución y composición de los alquileres, las variables meteorológicas y las categorías principales sobre la población preparada.

**Comprobaciones:**
- Calcular conteos, frecuencias y proporciones para las categorías de calendario y meteorología.
- Calcular medidas de tendencia central, dispersión, cuantiles, mínimos y máximos para `cnt`, `casual`, `registered`, `temp`, `atemp`, `hum` y `windspeed`.
- Describir la composición de `cnt` mediante sus componentes `casual` y `registered`, incluyendo agregados y proporciones calculadas de forma agregada o claramente definida.
- Preparar estadísticas estratificadas pertinentes de alquileres por `yr`, `season`, `workingday`, `holiday`, `weathersit` y `hr`.
- Explicitar la población, el tratamiento de registros y la definición de cada medida en los resultados estructurados.

**Variables o grupos:** `cnt`, `casual`, `registered`, `temp`, `atemp`, `hum`, `windspeed`; categorías `yr`, `season`, `mnth`, `hr`, `weekday`, `holiday`, `workingday` y `weathersit`.

**Evidencia esperada:**
- Análisis `STAT-NNN` de estadística descriptiva global y por grupos principales.
- Tablas o estructuras JSON reproducibles que permitan respaldar los valores citados en el informe.
- Interpretaciones prudentes de asimetría, dispersión o diferencias descriptivas, si las estadísticas las apoyan.

**Supuestos o dependencias:**
- Las variables de alquiler son recuentos horarios y pueden presentar asimetría y muchos valores bajos; se elegirán resúmenes robustos cuando sea pertinente.
- Las medias por grupos se describirán como promedios observados, no como efectos de las categorías.

## E5

**Objetivo:** Analizar agregaciones temporales y relaciones relevantes entre demanda, composición de usuarios, calendario y meteorología.

**Comprobaciones:**
- Agregar `cnt`, `casual` y `registered` por fecha para describir la evolución diaria y facilitar la detección de variaciones temporales.
- Comparar agregados o promedios horarios por `hr`, separando `workingday` de no laborables para examinar perfiles horarios.
- Comparar demanda y composición de usuarios por `season`, `mnth`, `yr`, `weekday`, `holiday` y `weathersit`.
- Examinar asociaciones numéricas entre las variables meteorológicas y los recuentos mediante medidas y representaciones adecuadas a sus distribuciones.
- Evaluar redundancia y colinealidad descriptiva entre `temp` y `atemp`, y distinguir esta relación de la asociación de estas variables con los recuentos.
- Confirmar cuantitativamente la identidad entre los componentes de usuarios y `cnt`.
- Explorar fechas u horas con desviaciones destacables respecto de referencias descriptivas apropiadas, documentando que tales desviaciones no identifican por sí solas su causa.

**Variables o grupos:** Fecha derivada de `dteday`, `hr`, `workingday`, `holiday`, `weekday`, `season`, `mnth`, `yr`, `weathersit`, `temp`, `atemp`, `hum`, `windspeed`, `casual`, `registered` y `cnt`.

**Evidencia esperada:**
- Resultados E5 sobre agregación diaria, patrones horarios por condición laboral, comparaciones por categorías meteorológicas y de calendario, y asociaciones numéricas seleccionadas.
- Una o más entradas de análisis para identidades y redundancias entre variables.
- Interpretaciones explícitamente descriptivas, sin afirmaciones causales.

**Supuestos o dependencias:**
- El análisis temporal depende de que E2 valide la interpretación de `dteday` y `hr`.
- Las diferencias por grupos pueden coexistir con confusión temporal, estacional o de calendario; no se atribuirán a una única variable.
- La falta de registros, si existiera, deberá tenerse presente en cualquier agregado temporal.

## E6

**Objetivo:** Generar figuras legibles que respondan a preguntas analíticas prioritarias y estén vinculadas a resultados estructurados.

**Comprobaciones:**
- Diseñar las figuras después de conocer la cobertura, calidad y distribución, ajustando escalas, agregaciones y anotaciones a los datos observados.
- Incluir títulos, ejes, unidades o aclaración de escala normalizada, leyendas cuando haya comparaciones y rutas relativas registradas.
- Evitar representar `instant` como variable analítica de interés.
- Manejar la densidad de la serie horaria mediante agregación razonable cuando una visualización de todas las horas no sea legible.
- Vincular cada figura a uno o varios `STAT-NNN` y explicarla en el informe sin sobreinterpretarla.

**Variables o grupos:** Fecha o agregados diarios, `hr`, `workingday`, `cnt`, `casual`, `registered`, `season`, `weathersit`, `temp`, `hum` y otras variables que los hallazgos de E4–E5 justifiquen.

**Evidencia esperada:**
- Archivos PNG válidos bajo `figures/`, registrados como `FIG-NNN` en `statistics.json`.
- Títulos visibles, etiquetas interpretables y trazabilidad desde cada figura a análisis numéricos.
- Referencias de las figuras en la sección correspondiente de `report.md`.

**Supuestos o dependencias:**
- La selección final dependerá de los resultados de E4 y E5; no se generarán visualizaciones redundantes.
- Una figura no se utilizará como única evidencia de una cifra; sus resultados de respaldo se conservarán en `statistics.json`.

## E7

**Objetivo:** Consolidar problemas, riesgos y anomalías sustentados por comprobaciones, separando errores confirmados de valores extremos o patrones aún inciertos.

**Comprobaciones:**
- Registrar en `issues.json` todas las verificaciones de calidad efectuadas, incluso aquellas sin incidencias.
- Documentar, si se detectan, ausencias, filas duplicadas, identificadores repetidos, conversiones de tipo fallidas, categorías fuera de dominio, fechas u horas faltantes, rangos incompatibles e incumplimientos de identidades.
- Evaluar registros extremos de `cnt`, `casual`, `registered` o condiciones meteorológicas en su contexto temporal y documental.
- Distinguir valores extremos plausibles de posibles errores y documentar la decisión de conservar, corregir, excluir o recomendar revisión.
- Registrar riesgos analíticos aunque no impliquen una corrección de datos, como la agregación horaria, la normalización de variables, la posible cobertura incompleta y la falta de contexto externo para atribuir eventos.

**Variables o grupos:** Todas las variables de calidad; énfasis en `instant`, `dteday`, `hr`, las categorías codificadas, variables meteorológicas y recuentos de usuarios.

**Evidencia esperada:**
- `issues.json` con `checks_performed` no vacío, referencias a `STAT-NNN` y una lista de incidencias sustentadas.
- Para cada incidencia: evidencia, columnas y filas afectadas cuando proceda, decisión, acción, efecto potencial e incertidumbre.
- Análisis E7 que respalden anomalías temporales o extremas cuando se reporten.

**Supuestos o dependencias:**
- Un extremo estadístico no se clasificará automáticamente como un error.
- No se atribuirán anomalías a acontecimientos externos sin evidencia disponible dentro de las entradas autorizadas.
- Las incidencias deberán ser coherentes con las transformaciones documentadas en E3.

## E8

**Objetivo:** Integrar los resultados en un informe final reproducible, prudente y trazable a estadísticas, incidencias y figuras.

**Comprobaciones:**
- Redactar `report.md` con las secciones obligatorias y una descripción clara de la unidad de análisis, alcance y fuente documental.
- Resumir carga, calidad, preparación y comparación antes-después.
- Presentar estadísticas y relaciones principales con referencias cercanas a `STAT-NNN`.
- Incluir y explicar las figuras mediante referencias `FIG-NNN` y rutas relativas válidas.
- Referenciar problemas o riesgos con `ISSUE-NNN`.
- Diferenciar observaciones calculadas, interpretaciones descriptivas y explicaciones posibles.
- Declarar limitaciones, incertidumbres y decisiones analíticas que podrían condicionar la generalización de los resultados.
- Verificar coherencia entre el informe, `prepared_data.csv`, `statistics.json`, `issues.json` y las figuras.

**Variables o grupos:** Todas las variables y resultados que hayan sido seleccionados y respaldados en E1–E7.

**Evidencia esperada:**
- `report.md` estructurado, legible y con referencias internas resolubles.
- Lista de limitaciones en `statistics.json` y consistencia con `issues.json`.
- Resultados obligatorios completos y coherentes para validación conjunta.

**Supuestos o dependencias:**
- El informe dependerá exclusivamente de resultados calculados durante esta ejecución y de la documentación pública proporcionada.
- No se introducirán explicaciones externas como hechos ni se formularán conclusiones causales.

# Visualizaciones previstas

Las figuras se seleccionarán por utilidad analítica tras las verificaciones de calidad, no por una cuota fija.

- **Evolución temporal agregada de alquileres:** representar la evolución de `cnt` agregado por fecha para contextualizar variación temporal, estacionalidad y posibles periodos destacados. Variables: `dteday` y `cnt`, con agregación diaria. Se verificará previamente la continuidad temporal.
- **Perfil horario por condición laboral:** comparar el promedio o distribución resumida de `cnt` por `hr` entre `workingday` y no laborables, para describir diferencias de patrones horarios. Variables: `hr`, `workingday`, `cnt`.
- **Composición de usuarios por hora o tipo de día:** mostrar el comportamiento de `casual` y `registered` en una agregación temporal o por `hr` adecuada, para contextualizar la composición de `cnt`. Variables: `casual`, `registered`, `cnt`, `hr` y posiblemente `workingday`.
- **Distribución de recuentos:** representar la distribución de `cnt` y, si es legible y pertinente, de `casual` y `registered`, para comunicar dispersión, asimetría y extremos sin ocultarlos. Variables: `cnt`, `casual`, `registered`.
- **Demanda por condiciones meteorológicas:** comparar `cnt` por categorías `weathersit` mediante una visualización que haga visibles tamaño de grupo, tendencia central y dispersión. Variables: `weathersit`, `cnt`.
- **Relación descriptiva con meteorología:** representar la asociación entre `cnt` y una o más variables continuas normalizadas, como `temp`, `hum` o `windspeed`, usando transparencia, agregación o suavizado descriptivo solo si mejora la legibilidad. Variables: `cnt` y variables meteorológicas seleccionadas.
- **Estacionalidad o comparación interanual:** mostrar agregaciones de `cnt` por `mnth`, `season` o `yr` para describir patrones de calendario y variación entre años. Variables: `mnth` o `season`, `yr`, `cnt`.

# Supuestos y riesgos

- La documentación indica que el archivo horario debe representar 2011–2012; el Analista debe verificar la cobertura observada sin asumir que todas las horas esperables están presentes.
- Los valores `temp`, `atemp`, `hum` y `windspeed` están documentados como normalizados. Sus coeficientes de conversión pueden utilizarse para interpretar escalas si procede, pero el análisis debe conservar y declarar claramente la escala empleada.
- Los códigos de `season` y `weathersit` tienen descripciones públicas; deberán conservarse los valores fuente y verificarse que no aparezcan códigos no documentados.
- `weekday` tiene siete categorías, pero la correspondencia precisa entre cada código y el nombre del día debe comprobarse contra `dteday` antes de etiquetarla.
- `workingday` se documenta como un indicador construido a partir de fin de semana y festivo; puede validarse en la medida en que las codificaciones disponibles lo permitan, pero no se deben introducir calendarios externos.
- `cnt` está documentado como total de `casual` y `registered`; cualquier discrepancia debe registrarse como una comprobación de identidad, no resolverse mediante recalcular silenciosamente el total.
- Los recuentos excepcionalmente altos o bajos pueden reflejar demanda real, estacionalidad, hora del día o condiciones no recogidas; no se eliminarán sin evidencia de invalidez.
- Las asociaciones observadas entre meteorología, calendario y alquileres pueden estar confundidas entre sí y por tendencias temporales. Se describirán como asociaciones, no como efectos.
- El dataset agregado no contiene rutas, estaciones, duración de trayectos ni contexto de eventos suficiente para explicar causalmente variaciones concretas.
- La capacidad de detectar eventos específicos está limitada a las variables y documentación suministradas; no se usarán fuentes externas para etiquetar observaciones.

# Criterios de finalización

El plan se considerará cubierto cuando el Analista deje las siguientes evidencias:

1. Carga no destructiva documentada del CSV y perfil inicial que identifique dimensiones, columnas, tipos observados y unidad de análisis.
2. Verificaciones cuantificadas de ausencias, duplicados, identificadores, dominios categóricos, rangos, fechas, cobertura temporal e identidad `cnt = casual + registered`, con resultados trazables.
3. `prepared_data.csv` separado del original, con comparación antes-después y transformaciones o decisiones de conservación registradas como `TR-NNN`.
4. Estadísticas descriptivas globales y por grupos relevantes para recuentos, componentes de usuarios, calendario y meteorología, guardadas como resultados `STAT-NNN`.
5. Agregaciones temporales y varias relaciones descriptivas pertinentes, incluyendo comparación horaria por condición laboral y análisis de composición de usuarios.
6. Figuras PNG válidas, legibles, registradas como `FIG-NNN` y vinculadas a preguntas analíticas y resultados estructurados.
7. `issues.json` con comprobaciones de calidad realizadas e incidencias respaldadas, o una lista de incidencias vacía justificada por comprobaciones documentadas.
8. Informe final con todas las secciones requeridas, referencias resolubles a estadísticas, figuras e incidencias, lenguaje no causal y limitaciones explícitas.
9. Coherencia de `run_id`, `dataset_id`, dimensiones, identificadores, rutas relativas y referencias entre todos los archivos obligatorios.