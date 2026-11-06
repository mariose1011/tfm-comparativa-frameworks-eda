# Identificación

- **run_id:** `D1_bike_sharing__microsoft_agent_framework__r01__20260831T174252477482Z`
- **framework_id:** `microsoft_agent_framework`
- **dataset_id:** `D1_bike_sharing`
- **contract_version:** `1.0`
- **prompt_version:** `1.0`

# Comprensión inicial

El archivo de entrada es un CSV correspondiente al conjunto horario documentado como `hour.csv`. La inspección estructural inicial identifica 17 columnas: `instant`, `dteday`, `season`, `yr`, `mnth`, `hr`, `holiday`, `weekday`, `workingday`, `weathersit`, `temp`, `atemp`, `hum`, `windspeed`, `casual`, `registered` y `cnt`.

De acuerdo con la documentación pública, la unidad prevista de observación es una hora agregada de uso del sistema Capital Bikeshare en Washington, D.C., con recuentos de alquileres y atributos temporales y meteorológicos. La documentación atribuye la cobertura a los años 2011 y 2012 y define `cnt` como el total de alquileres, incluyendo `casual` y `registered`.

El alcance será descriptivo y exploratorio: calidad, distribución, evolución temporal, diferencias entre segmentos temporales y meteorológicos, composición de usuarios y valores inusuales. No se entrenarán modelos predictivos ni se formularán conclusiones causales.

Aspectos que permanecen por verificar: si cada combinación de fecha y hora está representada una sola vez, si existen horas ausentes o periodos incompletos, la codificación efectiva de `weekday`, la consistencia entre las variables temporales y la fecha, y la presencia observada de todas las categorías documentadas.

# Preguntas analíticas

1. ¿La tabla presenta una estructura coherente con observaciones horarias y con las definiciones de variables de la documentación?
2. ¿Existen valores ausentes, filas duplicadas, identificadores repetidos, fechas u horas faltantes, o categorías fuera de los códigos documentados?
3. ¿Se cumple la identidad documentada `cnt = casual + registered` en todas las observaciones?
4. ¿Cómo se distribuyen los alquileres totales (`cnt`) y sus componentes `casual` y `registered`, incluyendo dispersión, asimetría y valores extremos?
5. ¿Cómo varían los alquileres por hora (`hr`), día de semana (`weekday`), condición laboral (`workingday`), mes (`mnth`), estación (`season`) y año (`yr`)?
6. ¿Cómo cambia la composición entre usuarios `casual` y `registered` según la hora y la condición `workingday`?
7. ¿Qué patrones descriptivos se observan entre alquileres y las condiciones `weathersit`, `temp`, `atemp`, `hum` y `windspeed`?
8. ¿Existen días u horas con alquileres inusualmente altos o bajos respecto de su contexto temporal, y la evidencia disponible permite distinguir un extremo válido de un posible problema de datos?

# Plan por etapas

## E1

**Objetivo:** Confirmar la carga del CSV original sin alterarlo y documentar la estructura inicial de la tabla.

**Comprobaciones:**
- Registrar archivo, formato, dimensiones, nombres y orden de columnas.
- Revisar una muestra inicial, intermedia y final para verificar el patrón de registros.
- Contrastar la estructura observada con `Readme.txt`.
- Precisar la unidad de observación a partir de `dteday`, `hr`, `instant` y las definiciones públicas.

**Variables o grupos:**
- Todas las columnas; especialmente `instant`, `dteday`, `hr`, `casual`, `registered` y `cnt`.

**Evidencia esperada:**
- Perfil estructural del archivo original en `statistics.json`.
- Descripción de la unidad de análisis en `statistics.json` y `report.md`.
- Registro trazable de la consulta de documentación y de la carga.

**Supuestos o dependencias:**
- Se asume que el CSV seleccionado corresponde al archivo horario descrito en la documentación; deberá confirmarse mediante sus columnas y granularidad observada.

## E2

**Objetivo:** Caracterizar tipos, cobertura y calidad de los datos antes de cualquier preparación.

**Comprobaciones:**
- Verificar tipos observados y tipos analíticos adecuados, con conversión prevista de `dteday` a fecha.
- Cuantificar valores ausentes por columna.
- Comprobar duplicados de filas completas, duplicados de `instant` y duplicados de la combinación `dteday`–`hr`.
- Examinar cardinalidades y códigos de `season`, `yr`, `mnth`, `hr`, `holiday`, `weekday`, `workingday` y `weathersit` frente a la documentación.
- Revisar rangos y signos de las variables normalizadas `temp`, `atemp`, `hum` y `windspeed`, y de los conteos `casual`, `registered` y `cnt`.
- Verificar que `dteday`, `yr`, `mnth`, `season`, `weekday`, `holiday` y `workingday` sean temporalmente consistentes en la medida comprobable.
- Evaluar continuidad de fechas, número de observaciones por fecha y secuencias de horas para localizar cobertura temporal incompleta.
- Comprobar la identidad `cnt = casual + registered`.
- Identificar extremos estadísticos de los recuentos y de las variables meteorológicas sin calificarlos automáticamente como errores.

**Variables o grupos:**
- Identificación y tiempo: `instant`, `dteday`, `yr`, `mnth`, `hr`, `weekday`.
- Categorías: `season`, `holiday`, `workingday`, `weathersit`.
- Medidas: `temp`, `atemp`, `hum`, `windspeed`, `casual`, `registered`, `cnt`.

**Evidencia esperada:**
- Resultados cuantificados de comprobaciones de calidad como análisis `STAT-NNN`.
- Lista de comprobaciones en `issues.json`, incluidas las que no detecten incidencias.
- Incidencias o riesgos documentados en `issues.json` solamente cuando estén respaldados por evidencia.

**Supuestos o dependencias:**
- La documentación define los rangos de las variables codificadas y las escalas normalizadas, pero no detalla todos los convenios operativos, como la codificación numérica concreta de `weekday`; deberá inferirse y validarse prudentemente con la fecha.

## E3

**Objetivo:** Crear una copia preparada reproducible y separada del original, aplicando solo transformaciones justificadas.

**Comprobaciones:**
- Conservar el archivo original sin sobrescritura.
- Crear `prepared_data.csv` a partir de una copia de trabajo.
- Convertir `dteday` a un tipo fecha para los cálculos y serializarlo de forma ISO no ambigua en la salida.
- Representar variables codificadas como categorías analíticas, preservando sus códigos originales para trazabilidad.
- Decidir, con base en E2, el tratamiento de ausencias, duplicados, inconsistencias, valores inválidos y extremos.
- Mantener los valores extremos que sean plausibles y documentados, salvo evidencia suficiente de error.
- Considerar variables derivadas de interpretación clara, como etiquetas descriptivas para categorías, año calendario a partir de `yr` o participación de `casual` y `registered` sobre `cnt`, solo si las validaciones de identidad y denominador lo permiten.
- Comparar dimensiones, columnas y recuentos antes y después de la preparación.

**Variables o grupos:**
- Todas las variables fuente; potencialmente etiquetas derivadas para `season`, `weathersit`, `workingday` y componentes o participaciones de usuarios.

**Evidencia esperada:**
- `prepared_data.csv` legible y separado.
- Registro de decisiones `TR-NNN` con justificación, columnas y filas afectadas en `statistics.json`.
- Comparación antes-después en `statistics.json` y explicación resumida en el informe.

**Supuestos o dependencias:**
- No se imputarán, eliminarán ni recodificarán datos automáticamente; cualquier acción depende de los hallazgos documentados en E2.
- Las variables derivadas no sustituirán columnas fuente necesarias para auditoría e interpretación.

## E4

**Objetivo:** Resumir la distribución y composición de los alquileres y de las condiciones relevantes en la población preparada.

**Comprobaciones:**
- Calcular frecuencias y proporciones de categorías temporales y meteorológicas.
- Obtener medidas de tendencia central, dispersión, cuantiles, mínimos y máximos para `cnt`, `casual`, `registered`, `temp`, `atemp`, `hum` y `windspeed`.
- Describir distribución de `cnt` con medidas robustas además de la media cuando la forma de la distribución lo aconseje.
- Calcular estadísticas de alquileres por grupos principales: `yr`, `season`, `mnth`, `hr`, `weekday`, `workingday`, `holiday` y `weathersit`.
- Resumir la composición de usuarios mediante recuentos agregados y, si se justifica, proporciones de alquileres `casual` y `registered`.

**Variables o grupos:**
- Resultados: `cnt`, `casual`, `registered`.
- Calendario: `yr`, `season`, `mnth`, `hr`, `weekday`, `workingday`, `holiday`.
- Clima: `weathersit`, `temp`, `atemp`, `hum`, `windspeed`.

**Evidencia esperada:**
- Análisis estructurados `STAT-NNN` en `statistics.json` con población, método y resultados.
- Tablas o resúmenes reproducibles para el informe.
- Referencias a estas estadísticas en las secciones descriptivas de `report.md`.

**Supuestos o dependencias:**
- Las comparaciones entre grupos se presentarán como descripciones de la muestra observada y tendrán en cuenta tamaños de grupo potencialmente desiguales.

## E5

**Objetivo:** Examinar relaciones, agregaciones temporales y patrones de segmentación pertinentes sin atribuir causalidad.

**Comprobaciones:**
- Agregar alquileres por fecha y, cuando sea útil, por mes, estación y año para examinar evolución y estacionalidad descriptiva.
- Comparar perfiles horarios de `cnt`, `casual` y `registered`, separando `workingday` cuando aporte contexto.
- Evaluar asociaciones descriptivas entre `cnt` y las variables meteorológicas continuas mediante resúmenes por intervalos o medidas de asociación adecuadas a las distribuciones.
- Comparar alquileres y composición de usuarios entre niveles de `weathersit`.
- Revisar la relación y posible redundancia entre `temp` y `atemp`.
- Verificar nuevamente que los análisis de componentes respeten la identidad entre `cnt`, `casual` y `registered`.
- Identificar observaciones o agregados con desviación notable respecto de grupos temporales comparables, describiéndolos como candidatos a revisión y no como eventos externos confirmados.

**Variables o grupos:**
- Tiempo: `dteday`, `yr`, `mnth`, `season`, `hr`, `weekday`, `workingday`, `holiday`.
- Clima: `weathersit`, `temp`, `atemp`, `hum`, `windspeed`.
- Alquileres: `cnt`, `casual`, `registered`.

**Evidencia esperada:**
- Agregaciones y relaciones respaldadas por `STAT-NNN`.
- Interpretaciones prudentes que distingan asociación, patrón descriptivo y causalidad.
- Material analítico que sustente las figuras y conclusiones del informe.

**Supuestos o dependencias:**
- Las variables meteorológicas están normalizadas según la documentación; cualquier presentación en unidades reescaladas deberá indicar expresamente la fórmula y conservar la escala fuente.
- Las asociaciones podrán estar influidas por estacionalidad, tendencia temporal y estructura horaria; no se interpretarán como efectos aislados.

## E6

**Objetivo:** Elaborar figuras legibles que respondan a preguntas analíticas prioritarias y estén vinculadas a resultados estructurados.

**Comprobaciones:**
- Seleccionar visualizaciones acordes al tipo de variable y a la densidad temporal.
- Incluir títulos, ejes, unidades o escalas, leyendas y etiquetas de categorías cuando sean necesarios.
- Usar agregaciones temporales adecuadas para que la serie no resulte ilegible.
- Mostrar extremos con contexto, sin ocultar observaciones relevantes.
- Verificar que cada figura PNG se guarde en `figures/`, esté registrada como `FIG-NNN` y se vincule a análisis `STAT-NNN`.

**Variables o grupos:**
- Series agregadas de `cnt`, perfiles por `hr` y `workingday`, categorías `weathersit` y `season`, y variables meteorológicas seleccionadas.

**Evidencia esperada:**
- Figuras PNG válidas bajo rutas relativas `figures/fig_NNN_<descripcion_breve>.png`.
- Metadatos de cada figura en `statistics.json`.
- Inserciones o enlaces relativos y discusión de su propósito en `report.md`.

**Supuestos o dependencias:**
- La elección final dependerá de los patrones y de la calidad observados en E2–E5; se evitarán gráficos redundantes o que sugieran inferencia causal.

## E7

**Objetivo:** Consolidar problemas, riesgos y anomalías con evidencia, decisión y consecuencias interpretativas explícitas.

**Comprobaciones:**
- Registrar los resultados de todas las verificaciones de calidad, incluso cuando no hallen problemas.
- Clasificar incidencias confirmadas o sospechadas en categorías tales como ausencia, duplicación, tipo, categoría, rango, identidad, temporalidad o valores extremos.
- Para cada extremo relevante, contrastarlo con las reglas documentadas, el contexto temporal y la distribución del grupo antes de determinar si se retiene o requiere tratamiento.
- Documentar filas o identificadores de ejemplo solo cuando sean necesarios y trazables.
- Indicar la acción aplicada o recomendada, el efecto potencial y la incertidumbre remanente.

**Variables o grupos:**
- Todas las variables sujetas a validación; en especial `instant`, `dteday`, `hr`, categorías codificadas y la identidad de `cnt`, `casual` y `registered`.

**Evidencia esperada:**
- `issues.json` con comprobaciones `CHK-NNN` y, si corresponde, incidencias `ISSUE-NNN`.
- Análisis `STAT-NNN` que respalden los resultados de calidad.
- Referencias cruzadas coherentes en el informe final.

**Supuestos o dependencias:**
- La falta de información sobre acontecimientos externos impide confirmar explicaciones para picos o caídas de alquileres; dichos casos se tratarán como patrones internos o candidatos de revisión.

## E8

**Objetivo:** Integrar los resultados en un informe final verificable, prudente y trazable.

**Comprobaciones:**
- Redactar las secciones obligatorias de `report.md`: resumen ejecutivo, dataset y alcance, inspección/calidad/preparación, estadística descriptiva, relaciones, visualizaciones, problemas, limitaciones y conclusiones.
- Referenciar cada afirmación cuantitativa o verificable mediante `STAT-NNN`, `ISSUE-NNN` o `FIG-NNN`.
- Explicar decisiones de preparación y conservar la distinción entre hechos observados, interpretaciones y posibles explicaciones.
- Declarar que el análisis es descriptivo, que no se entrenaron modelos y que no se establecen relaciones causales.
- Verificar coherencia entre informe, `prepared_data.csv`, `statistics.json`, `issues.json` y figuras.

**Variables o grupos:**
- Los resultados seleccionados de todas las etapas, con énfasis en alquileres, composición de usuarios, patrones temporales y contexto meteorológico.

**Evidencia esperada:**
- `report.md` estructurado, con referencias internas resolubles.
- Conclusiones respaldadas por estadísticas, figuras e incidencias registradas.
- Limitaciones explícitas sobre agregación horaria, variables disponibles, escalas normalizadas y alcance no causal.

**Supuestos o dependencias:**
- El informe dependerá de que las salidas estructuradas y las figuras hayan sido generadas y validadas previamente.
- No se incorporará información externa ni se atribuirán anomalías a eventos concretos no presentes en las entradas autorizadas.

# Visualizaciones previstas

- **Evolución temporal agregada de `cnt`:** mostrar la variación de los alquileres a lo largo de la cobertura mediante una agregación temporal legible; permitirá contextualizar cambios de nivel, estacionalidad y posibles fechas candidatas a revisión.
- **Perfil horario de alquileres según `workingday`:** comparar el patrón de `cnt` por `hr` entre días laborables y no laborables, con una representación que permita apreciar diferencias de forma sin asumir causalidad.
- **Composición de usuarios por hora y condición laboral:** representar `casual` y `registered`, ya sea mediante perfiles separados o proporciones respaldadas por la identidad de componentes, para describir cómo cambia la mezcla de alquileres.
- **Distribución de `cnt`:** emplear una visualización adecuada para observar concentración, dispersión, asimetría y valores extremos de los alquileres horarios.
- **Alquileres por `weathersit` o `season`:** comparar distribuciones o resúmenes de `cnt` entre condiciones categóricas documentadas, señalando el tamaño de los grupos cuando resulte necesario.
- **Relación descriptiva entre `cnt` y condiciones meteorológicas:** representar una o varias relaciones seleccionadas entre `cnt` y `temp`, `hum` o `windspeed`, usando agregación, transparencia o intervalos si la densidad lo requiere.

La selección final y el formato concreto dependerán de los hallazgos de calidad, de la cobertura efectiva de categorías y de la legibilidad de los resultados.

# Supuestos y riesgos

- La documentación pública describe el archivo horario; debe verificarse que el archivo cargado tenga una observación por hora y que no existan omisiones, repeticiones o irregularidades de cobertura.
- `instant` se documenta como índice de registro y se utilizará para trazabilidad y controles de unicidad, no como medida sustantiva.
- Los códigos de `season`, `yr`, `holiday`, `workingday` y `weathersit` deberán validarse contra los valores documentados. La codificación de `weekday` requiere una comprobación de consistencia con `dteday`.
- `temp`, `atemp`, `hum` y `windspeed` están normalizadas. Debe evitarse comunicarlas como unidades físicas directas sin explicar una conversión sustentada en la documentación.
- La identidad `cnt = casual + registered` es una regla documental central y debe verificarse antes de calcular o interpretar participaciones de tipo de usuario.
- Los días con 23 o 25 horas, si los hubiera, pueden reflejar particularidades de cobertura horaria o cambios de horario y no deben etiquetarse automáticamente como errores.
- Los valores altos o bajos de alquileres, clima o viento pueden ser observaciones reales; se conservarán salvo evidencia de inconsistencia o invalidez.
- Las diferencias por hora, temporada, clima o condición laboral son asociaciones descriptivas en datos observacionales agregados y pueden estar confundidas por otros factores temporales disponibles o no disponibles.
- No se dispone en las entradas autorizadas de información detallada sobre estaciones, trayectos, capacidad operativa, eventos locales ni causas de interrupciones; esto limita la interpretación de patrones y anomalías.

# Criterios de finalización

- Se habrá documentado la carga del CSV original, su estructura, la consulta de `Readme.txt` y una definición prudente de la unidad de análisis.
- Se habrán evaluado y cuantificado tipos, ausencias, duplicados, categorías, rangos, continuidad temporal, coherencia temporal e identidad de los recuentos, registrando las comprobaciones en resultados trazables.
- Existirá `prepared_data.csv` como copia separada, con toda transformación, conservación deliberada o exclusión justificada mediante cambios `TR-NNN` y comparación antes-después.
- `statistics.json` tendrá el esquema requerido, dimensiones coherentes, perfil completo de columnas, análisis `STAT-NNN` reproducibles, decisiones de preparación, limitaciones y registro de figuras.
- Se habrán producido estadísticas descriptivas y varias agregaciones o relaciones pertinentes para los alquileres, su composición, el calendario y las condiciones meteorológicas.
- Existirá al menos una figura PNG válida, legible, registrada como `FIG-NNN`, relacionada con una pregunta analítica y citada en el informe.
- `issues.json` incluirá comprobaciones `CHK-NNN` no vacías y solo incidencias `ISSUE-NNN` sustentadas por evidencia, con decisión, acción, efecto potencial e incertidumbre.
- `report.md` cubrirá todas las secciones obligatorias, citará las evidencias internas pertinentes y presentará conclusiones descriptivas sin modelos predictivos ni afirmaciones causales.
- Las rutas de figuras serán relativas, los identificadores serán únicos y las referencias entre artefactos se resolverán dentro de la ejecución.