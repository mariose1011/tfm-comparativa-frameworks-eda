# Identificación

- **run_id:** `D1_bike_sharing__microsoft_agent_framework__r02__20260831T175750234109Z`
- **framework_id:** `microsoft_agent_framework`
- **dataset_id:** `D1_bike_sharing`
- **contract_version:** `1.0`
- **prompt_version:** `1.0`

# Comprensión inicial

El archivo de entrada es un CSV horario del dataset Bike Sharing documentado públicamente. La inspección inicial autorizada identifica 17 columnas: `instant`, `dteday`, `season`, `yr`, `mnth`, `hr`, `holiday`, `weekday`, `workingday`, `weathersit`, `temp`, `atemp`, `hum`, `windspeed`, `casual`, `registered` y `cnt`.

De acuerdo con la documentación, cada fila debe representar un intervalo horario agregado del sistema Capital Bikeshare de Washington D.C., con conteos de alquileres y condiciones calendáricas y meteorológicas asociadas. `cnt` representa el total de alquileres y, por definición documental, debe componerse de `casual` y `registered`.

El alcance será descriptivo y exploratorio: calidad, distribución temporal y por segmentos, relaciones observadas entre los conteos y las variables disponibles, y detección prudente de valores o periodos inusuales. No se entrenarán modelos predictivos ni se harán inferencias causales.

Aspectos que deberán confirmarse durante el análisis:
- Que `dteday` se convierta sin ambigüedad a fecha y que sea coherente con `yr`, `mnth`, `weekday` y `season`.
- Que la cobertura horaria sea continua y que las posibles horas ausentes, repetidas o atípicas se puedan distinguir de particularidades de calendario o horario.
- La codificación exacta de `weekday`, que la documentación describe pero no asigna explícitamente a nombres de días.
- Si los códigos de `season`, `weathersit`, indicadores binarios y variables normalizadas cumplen los dominios documentados.
- Si hay suficientes observaciones en todas las categorías de `weathersit`, especialmente en categorías menos frecuentes, para realizar comparaciones descriptivas interpretables.

# Preguntas analíticas

1. ¿La tabla conserva una secuencia temporal y una estructura de identificadores coherentes con observaciones horarias agregadas?
2. ¿Existen ausencias, filas duplicadas, identificadores repetidos, categorías fuera de dominio o incoherencias entre variables documentadas?
3. ¿Se verifica la identidad `cnt = casual + registered` en todas las filas, y cómo se tratarían eventuales incumplimientos?
4. ¿Cómo se distribuyen los alquileres horarios totales (`cnt`) y sus componentes `casual` y `registered`?
5. ¿Cómo varían los alquileres por `hr`, `workingday`, `weekday`, `holiday`, `season`, `mnth`, `yr` y `weathersit`?
6. ¿Qué diferencias descriptivas se observan entre usuarios `casual` y `registered`, incluidas sus proporciones dentro de `cnt`, según hora y tipo de día?
7. ¿Cómo evolucionan los alquileres agregados en el tiempo y qué periodos u observaciones se separan marcadamente de los patrones de su grupo comparable?
8. ¿Qué asociaciones descriptivas presentan `temp`, `atemp`, `hum` y `windspeed` con `cnt`, y qué redundancias o dependencias mecánicas deben considerarse al interpretarlas?

# Plan por etapas

## E1

**Objetivo:** Cargar el CSV sin modificar el original y consolidar la comprensión de su estructura, alcance temporal y unidad observacional.

**Comprobaciones:**
- Confirmar el archivo de entrada, formato CSV, número de filas y columnas, encabezados y muestra estructural.
- Consultar y citar operativamente la documentación pública disponible para interpretar campos, codificaciones y unidades.
- Convertir de forma controlada `dteday` para evaluar su legibilidad como fecha, sin alterar aún la fuente.
- Verificar que la combinación de `dteday` y `hr` es compatible con una observación horaria agregada.

**Variables o grupos:** Todas las columnas; en particular `instant`, `dteday`, `hr`, `cnt`, `casual` y `registered`.

**Evidencia esperada:** Perfil inicial reproducible en `statistics.json`, con dimensiones originales, tipos observados, columnas, muestra descriptiva y definición documentada de la unidad de análisis.

**Supuestos o dependencias:** Se parte de que el archivo seleccionado corresponde a la versión horaria documentada, algo que deberá comprobarse con la presencia y dominio de `hr`.

## E2

**Objetivo:** Evaluar estructura, tipos y calidad antes de cualquier decisión de preparación.

**Comprobaciones:**
- Revisar tipos reales frente a los esperados: fecha para `dteday`; numéricos continuos normalizados para `temp`, `atemp`, `hum` y `windspeed`; enteros categóricos para variables de calendario y tiempo; y conteos no negativos para `casual`, `registered` y `cnt`.
- Contabilizar valores ausentes por columna y verificar si existen cadenas no interpretables, conversiones fallidas o valores no finitos.
- Medir duplicados de fila, unicidad de `instant`, duplicados de combinaciones `dteday`–`hr` y orden temporal.
- Comprobar cardinalidades y dominios documentados de `season`, `yr`, `mnth`, `hr`, `holiday`, `weekday`, `workingday` y `weathersit`.
- Evaluar rangos, signos y escalas de las variables normalizadas frente a las definiciones documentadas.
- Verificar consistencia entre `dteday`, `yr`, `mnth`, `weekday`, `holiday` y `workingday` cuando sea derivable del calendario y la documentación.
- Examinar cobertura desde la primera hasta la última fecha, número de registros por día y posibles brechas temporales.
- Comprobar la identidad `cnt = casual + registered`.
- Identificar valores extremos de conteos y variables meteorológicas mediante cuantiles y comparación contextual por hora, tipo de día o periodo, sin asumir que sean errores.

**Variables o grupos:** Todas; con foco en `instant`, `dteday`, `hr`, calendarios, `weathersit`, variables meteorológicas y los tres conteos.

**Evidencia esperada:** Análisis estructurados de calidad con identificadores `STAT`, y registros de comprobaciones y problemas sustentados en `issues.json`, incluidos los resultados negativos de comprobaciones que no detecten incidencias.

**Supuestos o dependencias:** La validación de `weekday` depende de establecer su codificación observada; la detección de discontinuidades debe considerar que algunos días pueden no tener exactamente 24 registros por razones que deberán documentarse si se observan.

## E3

**Objetivo:** Crear una copia de trabajo trazable y adecuada para el EDA, preservando el archivo original y evitando limpieza automática no justificada.

**Comprobaciones:**
- Definir el criterio de retención, corrección o exclusión tras los resultados de E2.
- Convertir `dteday` a una representación de fecha no ambigua en la copia preparada.
- Tratar como categorías los códigos de calendario y `weathersit`, conservando los códigos originales y, si aporta claridad, creando etiquetas derivadas documentadas.
- Mantener `instant` como identificador trazable, sin interpretarlo como medida analítica.
- Considerar variables derivadas de bajo riesgo analítico, como una fecha-hora basada en `dteday` y `hr`, etiquetas de categoría o la proporción `casual / cnt` cuando el denominador sea positivo.
- Decidir explícitamente cómo se conservarán valores extremos válidos y cómo se gestionaría cualquier inconsistencia confirmada.
- Comparar dimensiones, ausencias y columnas antes y después.

**Variables o grupos:** `dteday`, `hr`, categorías codificadas, `instant`, `casual`, `registered` y `cnt`.

**Evidencia esperada:** `prepared_data.csv` separado y legible; registro secuencial de transformaciones `TR-NNN` en `statistics.json`, con justificación, columnas afectadas y comparación antes-después.

**Supuestos o dependencias:** Las transformaciones estarán condicionadas por la evidencia de E2. Si no se detectan errores que requieran depuración, la conservación deliberada de filas y columnas será una decisión válida y deberá quedar documentada.

## E4

**Objetivo:** Describir la distribución, composición y variabilidad de los alquileres y de las variables meteorológicas dentro de la población preparada.

**Comprobaciones:**
- Calcular recuentos, media, mediana, desviación o medidas robustas pertinentes, cuantiles, mínimos y máximos para `cnt`, `casual`, `registered`, `temp`, `atemp`, `hum` y `windspeed`.
- Resumir frecuencias y proporciones de las categorías de calendario y tiempo.
- Estimar la contribución agregada y proporción de `casual` y `registered` respecto de `cnt`, documentando el denominador aplicado.
- Obtener resúmenes de `cnt`, `casual` y `registered` por `hr`, `workingday`, `season`, `weathersit` y `yr`.
- Incluir tamaños de grupo junto con las estadísticas para no sobrerrepresentar categorías poco frecuentes.

**Variables o grupos:** `cnt`, `casual`, `registered`, `hr`, `workingday`, `weekday`, `holiday`, `season`, `mnth`, `yr`, `weathersit`, `temp`, `atemp`, `hum` y `windspeed`.

**Evidencia esperada:** Resultados tabulares y escalares reproducibles en análisis `STAT-NNN` de `statistics.json`, con poblaciones y métodos declarados.

**Supuestos o dependencias:** Por ser conteos horarios potencialmente asimétricos, se priorizarán medidas de centro y dispersión que reflejen la distribución, sin asumir normalidad.

## E5

**Objetivo:** Examinar relaciones y agregaciones relevantes para describir patrones horarios, temporales, de calendario, meteorología y composición de usuarios.

**Comprobaciones:**
- Agregar alquileres por fecha para describir la trayectoria diaria y por mes/año para comparaciones temporales comparables.
- Comparar perfiles horarios de `cnt`, `casual` y `registered`, diferenciando `workingday` y, si es pertinente, `holiday`.
- Comparar distribuciones o resúmenes de alquileres por `season` y `weathersit`, reportando el tamaño de cada grupo.
- Examinar asociaciones numéricas entre `cnt` y `temp`, `atemp`, `hum` y `windspeed` mediante medidas y representaciones adecuadas a distribuciones potencialmente no lineales.
- Cuantificar la relación entre `temp` y `atemp` como posible redundancia informativa, sin tratarlas como variables independientes por defecto.
- Contrastar sistemáticamente la identidad entre los componentes de usuarios y `cnt`.
- Detectar días u horas inusuales frente a grupos comparables —por ejemplo, misma hora y tipo de día o mediante desviaciones respecto de agregados temporales— y clasificarlos como observaciones que requieren revisión, no como errores automáticos.

**Variables o grupos:** Fecha y agregaciones temporales; `hr`, `workingday`, `holiday`, `weekday`, `season`, `weathersit`; variables normalizadas; `casual`, `registered` y `cnt`.

**Evidencia esperada:** Varios resultados `STAT-NNN` de agregaciones, comparaciones y relaciones con método, población e interpretación descriptiva explícita. Cualquier observación atípica se enlazará con `issues.json` si la evidencia justifica registrarla.

**Supuestos o dependencias:** Las asociaciones se describirán sin atribuir causalidad. El análisis temporal deberá reconocer que cambios entre años, estaciones y condiciones de calendario pueden coexistir.

## E6

**Objetivo:** Generar figuras legibles que respalden preguntas concretas y complementen las tablas estructuradas.

**Comprobaciones:**
- Construir figuras solamente después de validar la preparación y los agregados que las sustentan.
- Asegurar títulos claros, ejes con unidades o definiciones, leyendas necesarias, escalas no engañosas y archivos PNG válidos.
- Elegir agregación temporal o estratificación que evite sobrecargar las visualizaciones horarias.
- Registrar cada figura con identificador `FIG-NNN`, ruta relativa y análisis fuente en `statistics.json`.

**Variables o grupos:** Series temporales basadas en `dteday`; perfiles de `hr`; `workingday`; `casual`, `registered`, `cnt`; `season`, `weathersit`; y variables meteorológicas seleccionadas.

**Evidencia esperada:** Directorio `figures/` con figuras PNG válidas y registro trazable en `statistics.json`; referencias cruzadas a dichas figuras en el informe final.

**Supuestos o dependencias:** La selección final dependerá de los patrones y tamaños de grupo comprobados en E4 y E5. No se incluirán gráficos cuya densidad o escasa cobertura impida una lectura fiable.

## E7

**Objetivo:** Consolidar los problemas de calidad, riesgos interpretativos y observaciones inusuales con evidencia, decisión y efecto potencial.

**Comprobaciones:**
- Registrar por separado resultados de controles de ausencias, duplicados, tipos, categorías, rangos, identidad y cobertura temporal.
- Distinguir entre incidencias confirmadas, riesgos retenidos y sospechas que no puedan resolverse con el archivo y documentación disponibles.
- Documentar cualquier incumplimiento de dominios, relación de componentes, continuidad temporal o coherencia calendario-fecha.
- Evaluar extremos de `cnt` y de las variables meteorológicas en contexto; conservarlos salvo evidencia de invalidez.
- Identificar limitaciones inherentes: datos agregados por hora, variables meteorológicas normalizadas, ausencia de información sobre estación, trayecto o exposición, y cobertura limitada al periodo contenido en el archivo.

**Variables o grupos:** Todas, con especial atención a `instant`, fecha-hora, variables calendario, meteorología normalizada y conteos.

**Evidencia esperada:** `issues.json` con comprobaciones `CHK-NNN` y, si procede, incidencias `ISSUE-NNN` que incluyan evidencia, columnas/filas afectadas cuando puedan identificarse, decisión, acción, incertidumbre y efecto potencial.

**Supuestos o dependencias:** La ausencia de contexto externo impide confirmar explicaciones para variaciones temporales inusuales; estas se describirán como anomalías estadísticas o riesgos, no como eventos concretos.

## E8

**Objetivo:** Integrar los resultados en un informe final verificable, prudente y coherente con los artefactos producidos.

**Comprobaciones:**
- Redactar las secciones obligatorias del informe: resumen, dataset y alcance, calidad y preparación, estadística descriptiva, relaciones, visualizaciones, problemas, limitaciones y conclusiones.
- Referenciar junto a cada afirmación comprobable los identificadores `STAT-NNN`, `ISSUE-NNN` o `FIG-NNN` correspondientes.
- Distinguir resultados observados de interpretaciones y de posibles explicaciones no verificadas.
- Declarar la población utilizada, las decisiones de preparación y sus posibles efectos sobre la interpretación.
- Comprobar coherencia final entre el informe, `prepared_data.csv`, `statistics.json`, `issues.json` y las figuras.

**Variables o grupos:** Todos los resultados seleccionados de etapas anteriores.

**Evidencia esperada:** `report.md` estructurado, trazable y consistente con los resultados; artefactos obligatorios completos y referencias internas resolubles.

**Supuestos o dependencias:** El informe no extrapolará más allá de los registros del archivo ni sustituirá el análisis descriptivo por predicción o por conclusiones causales.

# Visualizaciones previstas

- **Evolución temporal agregada de los alquileres:** mostrar cómo cambia `cnt` a lo largo de `dteday`, con una agregación temporal que preserve legibilidad. Permitirá contextualizar variación, tendencia y posibles periodos inusuales.
- **Perfil horario por tipo de día:** comparar el resumen de `cnt` por `hr` para `workingday` frente a no laborable; de ser útil, descomponer o acompañar la comparación con `casual` y `registered`. Permitirá describir patrones horarios y diferencias de composición.
- **Distribución o comparación por condiciones meteorológicas:** representar `cnt` por `weathersit`, indicando tamaños de grupo y una escala apropiada. Permitirá evaluar heterogeneidad descriptiva entre categorías sin inferir efectos.
- **Relación entre condiciones meteorológicas continuas y alquileres:** representar `cnt` frente a una o más variables entre `temp`, `hum` y `windspeed`, mediante dispersión con resumen por intervalos u otra técnica legible. Permitirá visualizar asociaciones y posible no linealidad sin sobrecargar puntos.
- **Composición de usuarios por periodo o segmento:** representar la participación de `casual` y `registered` en el total para un agrupamiento temporal o horario seleccionado. Permitirá describir cambios en la mezcla de usuarios.

La elección definitiva, la estratificación y el número final de figuras dependerán de los resultados de calidad, distribución y tamaño de grupos. Cada figura deberá estar respaldada por análisis estructurados y registrada con ruta relativa.

# Supuestos y riesgos

- La documentación atribuye el archivo horario a alquileres agregados de Capital Bikeshare en Washington D.C. durante 2011 y 2012; se comprobará que la cobertura y los campos observados sean compatibles con esa descripción.
- `instant` es un índice de registro y no debe utilizarse como variable sustantiva para correlaciones o comparaciones.
- `season`, `yr`, `mnth`, `hr`, `holiday`, `weekday`, `workingday` y `weathersit` son códigos numéricos que deben analizarse primordialmente como categorías o indicadores, no como magnitudes continuas.
- `weekday` requiere verificación de su convención numérica antes de asignar etiquetas de días.
- `temp`, `atemp`, `hum` y `windspeed` están normalizadas según la documentación; cualquier conversión a unidades originales deberá documentarse con cuidado o evitarse si no añade valor.
- `temp` y `atemp` pueden contener información redundante; se evaluará su asociación antes de interpretar comparaciones separadas.
- La identidad documental entre `cnt`, `casual` y `registered` es una comprobación crítica de integridad y debe verificarse antes de calcular composiciones.
- Una hora, día o conteo extremo puede ser válido por estacionalidad, patrón horario, festivo, clima u otros factores no observados. No se eliminará ni se etiquetará como error sin evidencia.
- La agregación horaria oculta variabilidad dentro de la hora, trayectos, disponibilidad de bicicletas y estaciones; ello limita la interpretación.
- Las asociaciones entre alquileres, calendario y meteorología serán descriptivas. El dataset no permite aislar causas, controlar todos los factores ni confirmar eventos externos.

# Criterios de finalización

El plan se considerará cubierto cuando el Analista deje evidencia trazable de lo siguiente:

1. Carga preservada del CSV, perfil inicial, consulta documental y definición explícita de la unidad de análisis.
2. Verificación cuantificada de tipos, ausencias, duplicados, identificadores, dominios categóricos, rangos, cobertura temporal e identidad `cnt = casual + registered`.
3. Creación de `prepared_data.csv` como copia separada, con comparación antes-después y transformaciones o decisiones de conservación documentadas mediante `TR-NNN`.
4. Estadísticas descriptivas reproducibles de conteos, variables meteorológicas y categorías principales, incluyendo resúmenes por grupos pertinentes y tamaños de grupo.
5. Agregaciones temporales y análisis de relaciones relevantes entre uso, hora, calendario, composición de usuarios y meteorología, con interpretaciones no causales.
6. Al menos una figura PNG legible y pertinente, con título, ejes y registro `FIG-NNN` vinculado a análisis `STAT-NNN`; se generarán las adicionales que resulten justificadas.
7. `issues.json` no vacío en su lista de comprobaciones, con incidencias solo cuando estén respaldadas, y con decisiones y efectos potenciales documentados.
8. `statistics.json` válido con dimensiones coherentes, perfiles de columnas, preparación, análisis, figuras y limitaciones.
9. `report.md` con todas las secciones requeridas, afirmaciones trazables mediante referencias internas y limitaciones explícitas.
10. Coherencia final entre todos los archivos obligatorios y conservación intacta del archivo original.