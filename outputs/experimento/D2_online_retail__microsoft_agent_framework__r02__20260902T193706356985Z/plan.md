# Identificación

- `run_id`: `D2_online_retail__microsoft_agent_framework__r02__20260902T193706356985Z`
- `framework_id`: `microsoft_agent_framework`
- `dataset_id`: `D2_online_retail`
- `contract_version`: `1.0`
- `prompt_version`: `1.0`

# Comprensión inicial

El archivo de entrada es un libro `xlsx`, cuya hoja seleccionada es `Online Retail`. La inspección inicial autorizada indica ocho columnas: `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID` y `Country`.

Según la documentación pública, cada observación es una **línea de factura**, no una compra completa ni necesariamente una factura única. El alcance temporal documentado comprende transacciones realizadas entre el 1 de diciembre de 2010 y el 9 de diciembre de 2011 por una empresa británica de comercio electrónico. `InvoiceNo` y `CustomerID` son identificadores nominales; `StockCode` puede identificar artículos o conceptos facturados. Una factura cuyo `InvoiceNo` comienza por `C` representa una cancelación según la documentación.

La inspección inicial muestra tipos observados que deberán ser confirmados al cargar el archivo: campos nominales leídos como objeto o texto, `Quantity` como entero, `InvoiceDate` como fecha-hora, `UnitPrice` como numérico decimal y `CustomerID` como numérico pese a su naturaleza nominal. Se deberán verificar ausencias, consistencia de identificadores y categorías, signos, precios nulos o negativos, cancelaciones, duplicados y la cobertura temporal efectiva. No se asumirá que toda línea representa una venta positiva ni que todo `StockCode` sea un producto comercial convencional.

# Preguntas analíticas

1. ¿Cuál es la estructura efectiva de las líneas de factura y cómo se distribuyen entre facturas, artículos, clientes identificados y países?
2. ¿Qué calidad presentan los campos esenciales, en particular `Description` y `CustomerID`, y cómo condicionan los análisis por producto o cliente?
3. ¿Qué proporción de líneas corresponde a facturas marcadas como cancelaciones y cómo se comportan sus cantidades, precios e importes frente a las demás líneas?
4. ¿Cuál es la distribución de `Quantity`, `UnitPrice` y el importe de línea derivado, tanto en el conjunto como tras separar operaciones positivas y cancelaciones?
5. ¿Cómo evoluciona la actividad por fecha o periodo agregado, considerando que el inicio y fin documentados pueden corresponder a periodos parciales?
6. ¿Cómo se distribuyen las líneas, cantidades netas o importes por `Country`, artículos y facturas, sin interpretar identificadores como variables continuas?
7. ¿Existen relaciones descriptivas relevantes entre cantidad, precio unitario, importe, condición de cancelación, país y temporalidad?
8. ¿Qué valores extremos, conceptos no convencionales, incoherencias o limitaciones podrían afectar las conclusiones descriptivas?

# Plan por etapas

## E1

**Objetivo:** Cargar el libro de trabajo sin modificar el original y confirmar la estructura inicial, la hoja analizada y la unidad de observación.

**Comprobaciones:**
- Leer el archivo `xlsx` y confirmar la hoja `Online Retail`.
- Registrar dimensiones, nombres, orden de columnas y muestra estructural de filas.
- Contrastar nombres y significado de variables con la documentación pública.
- Confirmar que cada fila se trata como línea de factura y no agregar prematuramente a nivel de factura o cliente.
- Registrar de forma explícita cualquier diferencia entre el esquema observado y el documentado.

**Variables o grupos:** Todas las columnas; en especial `InvoiceNo` como identificador nominal de factura, `StockCode` como código nominal de artículo o concepto, y `InvoiceDate` como marca temporal.

**Evidencia esperada:** Perfil de origen en `statistics.json`, incluyendo dimensiones, tipos observados, listado de columnas y descripción de la unidad de análisis en `profile`; una entrada de análisis `E1` que documente la carga y la inspección.

**Supuestos o dependencias:** Se parte de la documentación pública proporcionada y de la hoja seleccionada por la inspección inicial. La semántica detallada de códigos especiales distintos de facturas con prefijo `C` deberá comprobarse con prudencia, pues no está completamente definida en la documentación.

## E2

**Objetivo:** Caracterizar tipos, completitud, unicidad, categorías, fechas, rangos y riesgos de calidad antes de tomar decisiones de preparación.

**Comprobaciones:**
- Comparar tipos observados con tipos analíticos esperados; verificar que `CustomerID` se trate como identificador y no como magnitud.
- Cuantificar valores ausentes por columna y evaluar su concentración por factura, fecha, país, tipo de operación u otros grupos pertinentes.
- Contar filas completamente duplicadas y examinar duplicación de combinaciones de variables de línea sin asumir que sean errores.
- Medir cardinalidad de `InvoiceNo`, `StockCode`, `Description`, `CustomerID` y `Country`; revisar variantes textuales evidentes, espacios, diferencias de descripción para un mismo código y códigos asociados a múltiples descripciones.
- Verificar cobertura mínima y máxima de `InvoiceDate`, distribución temporal básica, orden de las fechas y posible incompletitud de los extremos temporales.
- Examinar mínimos, máximos, cuantiles, ceros y signos de `Quantity` y `UnitPrice`.
- Identificar facturas con prefijo `C` y contrastar descriptivamente esa condición con los signos de `Quantity` e importes derivados.
- Revisar la presencia de importes potencialmente atípicos o de precios nulos sin inferir automáticamente error.

**Variables o grupos:** `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID`, `Country`; grupos por condición de cancelación, periodo temporal y país cuando resulte viable.

**Evidencia esperada:** Análisis estructurados `STAT-NNN` de tipos, ausencias, duplicados, cardinalidades, cobertura temporal, rangos y coherencias; comprobaciones `CHK-NNN` e incidencias sustentadas en `issues.json`.

**Supuestos o dependencias:** Las repeticiones de líneas pueden ser transacciones legítimas; solo se tratarán como duplicados potencialmente problemáticos después de examinarlas. Los extremos deben diferenciarse de errores con la evidencia disponible, sin reglas automáticas de eliminación.

## E3

**Objetivo:** Generar una copia de trabajo trazable y apta para análisis descriptivo, manteniendo el original intacto y preservando la información necesaria para interpretar devoluciones, cancelaciones y ausencias.

**Comprobaciones:**
- Crear `prepared_data.csv` como archivo independiente y registrar su forma antes y después.
- Estandarizar los tipos requeridos para el análisis: fecha-hora para `InvoiceDate`, numéricos para `Quantity` y `UnitPrice`, y representación nominal consistente para identificadores y códigos.
- Evaluar una normalización conservadora de campos de texto, como espacios periféricos, únicamente si se cuantifica el cambio y no altera la semántica.
- Crear variables derivadas justificadas, previsiblemente `line_amount` como `Quantity * UnitPrice`, un indicador de cancelación basado en el prefijo `C` de `InvoiceNo`, y una clave temporal agregable derivada de `InvoiceDate`, si dichas variables se validan y aportan valor.
- Decidir y documentar el tratamiento de `CustomerID` y `Description` ausentes. Se conservarán las líneas salvo que exista evidencia suficiente para excluir una población de un análisis específico; los subconjuntos deberán quedar claramente definidos.
- Decidir el tratamiento de filas duplicadas, precios nulos, cantidades negativas, importes negativos y valores extremos tras la inspección de E2.
- Distinguir la población preparada general de eventuales poblaciones analíticas específicas, por ejemplo líneas no canceladas o líneas con cliente identificado.

**Variables o grupos:** Todas las columnas originales; posibles derivadas `line_amount`, indicador de cancelación y variables de periodo. Subpoblaciones por condición de cancelación y disponibilidad de `CustomerID`.

**Evidencia esperada:** `prepared_data.csv`; perfil de columnas finales; registro secuencial `TR-NNN` de decisiones, cambios, filas afectadas y justificaciones en `statistics.json`; comparación básica antes-después.

**Supuestos o dependencias:** La creación de derivadas dependerá de que los tipos y la identidad aritmética sean verificables. No se imputarán identificadores, descripciones, cantidades ni precios sin un fundamento documentado.

## E4

**Objetivo:** Describir la escala, distribución y composición de las líneas preparadas y de subpoblaciones analíticamente relevantes.

**Comprobaciones:**
- Calcular conteos de líneas, facturas, artículos o conceptos, clientes identificados, países y cancelaciones según las definiciones documentadas.
- Describir `Quantity`, `UnitPrice` y `line_amount` si se deriva, con medidas adecuadas de posición, dispersión, cuantiles, mínimos, máximos y proporciones de cero o signo negativo cuando corresponda.
- Separar de forma explícita estadísticas de todas las líneas, líneas no canceladas y cancelaciones cuando esa separación permita evitar mezclas interpretativas.
- Obtener frecuencias y participación de categorías principales, usando criterios de presentación que manejen la alta cardinalidad sin ocultar el total.
- Describir la completitud de `CustomerID` y `Description` dentro de poblaciones relevantes.
- Realizar resúmenes por `Country`, por condición de cancelación y por periodos, cuando el volumen y cardinalidad permitan interpretaciones claras.

**Variables o grupos:** `Quantity`, `UnitPrice`, `line_amount` si se crea, indicador de cancelación, `Country`, `InvoiceDate`, `CustomerID`, `StockCode`, `Description`; grupos de líneas generales, no canceladas, canceladas y clientes identificados.

**Evidencia esperada:** Resultados estructurados `STAT-NNN` reproducibles con definiciones de población explícitas, tablas de frecuencias y estadísticas numéricas que puedan respaldar el informe.

**Supuestos o dependencias:** Los importes derivados describen valores registrados de línea; no se interpretarán automáticamente como ingresos realizados sin considerar cancelaciones, precios nulos u otras particularidades detectadas.

## E5

**Objetivo:** Examinar agregaciones y relaciones descriptivas pertinentes entre tiempo, geografía, artículos, clientes identificados, cantidades, precios e importes.

**Comprobaciones:**
- Agregar líneas, facturas, unidades e importes por periodo temporal apropiado, verificando la granularidad y marcando periodos parciales si los hubiera.
- Comparar actividad y composición por `Country`, distinguiendo recuentos de líneas, facturas y valores monetarios o unidades según corresponda.
- Analizar la concentración descriptiva de artículos o conceptos mediante `StockCode` y, cuando sea consistente, `Description`, sin deducir causalidad ni tratar códigos como escalas numéricas.
- En el subconjunto con `CustomerID` disponible, resumir actividad por cliente y verificar si la falta de identificador limita comparaciones con el conjunto total.
- Examinar la relación entre `Quantity`, `UnitPrice` y `line_amount`, utilizando medidas y representaciones resistentes a asimetría y extremos cuando proceda.
- Comparar cantidades, precios e importes por condición de cancelación; comprobar la identidad de cálculo del importe de línea y documentar cualquier excepción que resulte de datos inválidos o faltantes.
- Analizar asociaciones únicamente como patrones descriptivos; evitar inferir demanda, rentabilidad, recurrencia causal o comportamiento individual no observado.

**Variables o grupos:** Variables derivadas disponibles; `InvoiceDate` y periodo; `Country`; `StockCode` y `Description`; `CustomerID` solo donde esté presente; `Quantity`, `UnitPrice`, `line_amount`; condición de cancelación.

**Evidencia esperada:** Varios análisis `STAT-NNN` de agregaciones temporales, geográficas, por producto o concepto, por clientes identificados y de relaciones entre variables; interpretaciones breves y prudentes.

**Supuestos o dependencias:** La disponibilidad de `CustomerID` no se asumirá aleatoria. Las agregaciones por factura dependerán de que `InvoiceNo` sea suficientemente consistente; cualquier código o factura especial se conservará o separará según la evidencia de E2.

## E6

**Objetivo:** Crear visualizaciones legibles que respondan a preguntas analíticas y complementen las tablas y estadísticas, sin ocultar sesgos de escala, alta cardinalidad o extremos.

**Comprobaciones:**
- Seleccionar visualizaciones tras conocer la distribución y calidad final de los datos.
- Incluir títulos, ejes, unidades monetarias en libras esterlinas cuando corresponda, leyendas y notas de población o filtros.
- Usar agregaciones, escalas transformadas o recortes visuales solo si se documentan y preservan una representación alternativa o resumen de los extremos relevantes.
- Verificar que cada figura sea un PNG legible, tenga una ruta relativa válida y se registre como `FIG-NNN` con sus análisis de respaldo.

**Variables o grupos:** Periodos derivados de `InvoiceDate`, métricas de líneas/facturas/unidades/importes, `Country`, `StockCode` o `Description`, `Quantity`, `UnitPrice`, `line_amount`, condición de cancelación.

**Evidencia esperada:** Archivos PNG en `figures/`, entradas correspondientes en `statistics.json` y referencias explícitas en el informe final.

**Supuestos o dependencias:** Las figuras definitivas dependerán de las distribuciones observadas y de las incidencias detectadas. Se evitarán gráficos de alta cardinalidad que no permitan lectura o que sugieran una precisión inexistente.

## E7

**Objetivo:** Consolidar y clasificar los problemas, riesgos, anomalías y limitaciones que afecten la interpretación del EDA y las decisiones tomadas.

**Comprobaciones:**
- Registrar las comprobaciones realizadas incluso cuando no detecten un problema.
- Documentar ausencias, posibles duplicados, conversiones de tipo, inconsistencias entre código y descripción, categorías inusuales, signos o rangos anómalos, cobertura temporal y posibles extremos.
- Diferenciar incidencias detectadas, sospechadas, resueltas y retenidas; no etiquetar automáticamente como error los valores extremos, las devoluciones o las cancelaciones documentadas.
- Identificar las columnas afectadas, recuentos cuando se puedan calcular, muestras limitadas de posiciones o identificadores y referencias a estadísticas de respaldo.
- Explicar para cada riesgo la decisión aplicada o recomendada, el posible efecto sobre resultados y la incertidumbre restante.

**Variables o grupos:** Todas las variables, con énfasis en `Description`, `CustomerID`, `InvoiceNo`, `StockCode`, `Quantity`, `UnitPrice`, `InvoiceDate` y variables derivadas.

**Evidencia esperada:** `issues.json` válido con `checks_performed` no vacío, identificadores `CHK-NNN` e `ISSUE-NNN`, evidencia rastreable a `STAT-NNN` y decisiones coherentes con la preparación.

**Supuestos o dependencias:** La documentación solo define explícitamente el prefijo `C` como cancelación; otros patrones deberán describirse como observaciones o riesgos, no como significados confirmados.

## E8

**Objetivo:** Elaborar un informe final reproducible y prudente que integre alcance, preparación, estadísticas, relaciones, visualizaciones, problemas y limitaciones.

**Comprobaciones:**
- Redactar `report.md` con las secciones requeridas y referencias internas válidas a `STAT-NNN`, `ISSUE-NNN` y `FIG-NNN`.
- Explicar la unidad de observación, el alcance temporal documentado, la distinción entre líneas, facturas y clientes, y las poblaciones utilizadas en cada cálculo.
- Resumir decisiones de preparación, hallazgos descriptivos principales y evidencia gráfica sin presentar asociaciones como causalidad.
- Diferenciar claramente hechos calculados, interpretaciones y explicaciones posibles.
- Incluir limitaciones relacionadas con identificadores ausentes, cancelaciones, cobertura temporal, extremos, semántica de conceptos especiales y cualquier decisión de filtrado o conservación.
- Verificar coherencia entre cifras, tablas, figuras, `prepared_data.csv`, `statistics.json` e `issues.json`.

**Variables o grupos:** Síntesis de todas las variables, poblaciones y agregaciones que resulten relevantes tras E1–E7.

**Evidencia esperada:** `report.md` estructurado, legible y trazable; referencias resolubles a las salidas analíticas; validación de coherencia con los artefactos obligatorios.

**Supuestos o dependencias:** El informe dependerá exclusivamente de los resultados generados durante la ejecución y de la documentación pública. No incorporará datos externos ni afirmaciones no respaldadas por evidencia disponible.

# Visualizaciones previstas

- **Evolución temporal de la actividad:** representar por un periodo adecuado los recuentos de líneas o facturas y, si es válido, unidades o importes netos. El objetivo es identificar patrones temporales descriptivos y advertir posibles periodos parciales. Variables: `InvoiceDate`, periodo derivado, `Quantity`, `line_amount`, `InvoiceNo`.
- **Distribución de importes o variables de línea:** mostrar la distribución de `Quantity`, `UnitPrice` o `line_amount` mediante una forma adecuada a asimetría y extremos. El objetivo es comunicar concentración, dispersión y colas, sin confundir valores extremos con errores. Variables: `Quantity`, `UnitPrice`, `line_amount`.
- **Comparación entre operaciones no canceladas y cancelaciones:** representar cantidades o importes por condición derivada de `InvoiceNo`. El objetivo es mostrar por qué la separación de poblaciones puede ser necesaria. Variables: `InvoiceNo`, indicador de cancelación, `Quantity`, `line_amount`.
- **Composición geográfica:** visualizar países con mayor participación mediante una métrica claramente definida y una selección transparente de categorías si la cardinalidad impide mostrar todas con legibilidad. El objetivo es describir concentración geográfica, no explicar sus causas. Variables: `Country`, recuentos de líneas o facturas, unidades o importes.
- **Concentración por artículo o concepto:** visualizar los artículos o conceptos principales por cantidad o importe bajo una población definida, evitando gráficos ilegibles de todos los códigos. El objetivo es describir concentración y heterogeneidad del catálogo facturado. Variables: `StockCode`, `Description`, `Quantity`, `line_amount`.
- **Relación cantidad-precio o cantidad-importe:** si los resultados de E5 la justifican, mostrar una relación agregada o de líneas con tratamiento visual explícito de la densidad y los extremos. El objetivo es describir asociación y estructura de los registros. Variables: `Quantity`, `UnitPrice`, `line_amount`, condición de cancelación.

# Supuestos y riesgos

- `InvoiceNo` y `CustomerID` son identificadores nominales; sus valores numéricos aparentes no deberán resumirse como medidas continuas ni emplearse para correlaciones numéricas.
- El prefijo `C` de `InvoiceNo` se documenta como cancelación, pero deberán verificarse su frecuencia y coherencia con signos e importes antes de definir poblaciones analíticas.
- `StockCode` puede abarcar artículos o conceptos facturados; no se asumirá que cada código corresponda inequívocamente a un producto físico sin comprobar su relación con `Description`.
- La falta de `CustomerID` o `Description` puede limitar análisis por cliente o producto. No se imputará su contenido, y se cuantificará cualquier sesgo potencial de trabajar con subconjuntos completos.
- Repeticiones exactas de una línea no son necesariamente duplicados erróneos: podrían corresponder a registros legítimos. Cualquier eliminación requerirá evidencia y registro.
- Cantidades negativas, precios cero, importes negativos o valores muy altos pueden ser parte de cancelaciones, ajustes o registros válidos; deberán evaluarse contextualmente.
- El periodo documentado puede incluir meses iniciales o finales incompletos y no debe compararse sin advertencia con meses completos.
- Los importes derivados de `Quantity * UnitPrice` reflejan el valor registrado en una línea y no bastan, por sí solos, para afirmar ingresos, pagos o rentabilidad.
- Los países, clientes y artículos pueden presentar concentración elevada; las comparaciones deberán declarar denominadores, filtros y criterios de selección.
- El análisis será descriptivo. Las relaciones temporales, geográficas, de producto o cliente no se interpretarán como efectos causales.

# Criterios de finalización

- Se habrá preservado el archivo original y se habrá generado una copia `prepared_data.csv` legible, con columnas, filas y transformaciones coherentemente documentadas.
- `statistics.json` será válido, incluirá el perfil original y preparado, columnas finales, decisiones `TR-NNN`, análisis `STAT-NNN`, limitaciones y registro de todas las figuras.
- Se habrá cubierto E1–E7 mediante resultados reproducibles: carga, estructura, calidad, preparación, descripción, agregaciones o relaciones, y riesgos.
- Las ausencias, duplicados, tipos, cardinalidad, temporalidad, signos, rangos, cancelaciones y extremos se habrán comprobado cuando sean evaluables y quedarán trazados mediante estadísticas o incidencias.
- `issues.json` contendrá comprobaciones `CHK-NNN` no vacías y cualquier incidencia respaldada con evidencia, decisión, efecto potencial e incertidumbre.
- Se habrán generado visualizaciones pertinentes, legibles y registradas como PNG, con correspondencia entre sus identificadores, rutas y análisis de respaldo.
- `report.md` incluirá todas las secciones obligatorias, citará resultados y figuras mediante referencias válidas, distinguirá observación de interpretación y expondrá limitaciones.
- Las dimensiones y referencias internas entre `prepared_data.csv`, `statistics.json`, `issues.json`, figuras e informe serán coherentes; no quedarán afirmaciones cuantitativas sin evidencia estructurada ni solicitudes de corrección pendientes.