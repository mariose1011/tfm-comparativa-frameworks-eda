# Identificación

- **run_id:** `D2_online_retail__langgraph__r03__20260902T200956928988Z`
- **framework_id:** `langgraph`
- **dataset_id:** `D2_online_retail`
- **contract_version:** `1.0`
- **prompt_version:** `1.0`

# Comprensión inicial

El archivo de entrada tiene formato `xlsx` y se inspeccionará en la hoja seleccionada `Online Retail`. La inspección inicial autorizada identifica ocho campos: `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID` y `Country`.

Según la documentación pública, cada fila representa una **línea de factura** de transacciones de una empresa británica de comercio electrónico; por tanto, no equivale necesariamente a una compra, cliente o factura completa. `InvoiceNo` y `CustomerID` son identificadores nominales, y los valores de `InvoiceNo` que comienzan por `C` se documentan como cancelaciones.

El alcance será descriptivo y exploratorio: calidad de registros, magnitudes por línea, facturas, artículos, clientes identificados, países y tiempo. Se podrán calcular importes de línea como `Quantity × UnitPrice` únicamente como variable derivada contable para el análisis, sin interpretarla como ingreso definitivo si existen cancelaciones, ajustes o conceptos no convencionales.

Aspectos que deberán verificarse: consistencia efectiva de los tipos observados, formatos mixtos de identificadores, ausencias de `Description` y `CustomerID`, naturaleza de cantidades o precios no positivos, presencia y tratamiento de cancelaciones, exactitud de duplicados, cobertura temporal efectiva, completitud de los extremos temporales y correspondencia entre códigos, descripciones y países.

# Preguntas analíticas

1. ¿Cuál es la estructura efectiva de la tabla y qué proporción de sus registros presenta ausencias, duplicación exacta o inconsistencias relevantes?
2. ¿Cómo se distribuyen `Quantity`, `UnitPrice` y el importe derivado de línea, y qué valores extremos requieren contextualización antes de cualquier exclusión?
3. ¿Qué diferencia descriptiva existe entre líneas asociadas a facturas regulares y líneas asociadas a cancelaciones identificadas mediante `InvoiceNo`?
4. ¿Cómo evolucionan los recuentos de líneas, facturas, unidades netas e importes de línea a lo largo del tiempo disponible?
5. ¿Qué países, artículos o descripciones concentran mayor actividad, considerando separadamente volumen de líneas, unidades e importes cuando resulte pertinente?
6. Entre los registros con `CustomerID` disponible, ¿cómo se distribuye la actividad por cliente y cuál es el efecto potencial de analizar solo esa subpoblación?
7. ¿Existen relaciones descriptivas relevantes entre cantidad, precio unitario, importe de línea, país, tipo de factura y periodo temporal?
8. ¿Qué decisiones de preparación preservan la trazabilidad sin eliminar automáticamente operaciones potencialmente válidas, como cancelaciones, devoluciones o líneas con valores atípicos?

# Plan por etapas

## E1

**Objetivo:** Cargar el archivo original sin modificarlo y confirmar la estructura básica, la hoja utilizada y la unidad de observación.

**Comprobaciones:**
- Leer el archivo `xlsx` y verificar que la hoja `Online Retail` se carga correctamente.
- Registrar dimensiones, nombres, orden de columnas, tipos observados y una muestra estructural de inicio, final y posiciones variadas.
- Contrastar los campos disponibles con el diccionario público.
- Confirmar que cada fila debe tratarse como línea de factura y no como transacción completa.

**Variables o grupos:** Todas las columnas originales; especialmente `InvoiceNo`, `InvoiceDate`, `Quantity`, `UnitPrice` y `CustomerID` para contextualizar la granularidad.

**Evidencia esperada:** Perfil original en `statistics.json`, incluyendo dimensiones, columnas y definición de unidad de análisis; copia inalterada del original y trazabilidad de la fuente en los registros de ejecución.

**Supuestos o dependencias:** Se parte de que la hoja seleccionada es la tabla analítica principal; deberá confirmarse que no contiene cabeceras adicionales, notas o filas ajenas a las líneas de factura.

## E2

**Objetivo:** Caracterizar tipos, calidad, cobertura y riesgos de interpretación del archivo original.

**Comprobaciones:**
- Contrastar los tipos reales con los esperados: identificadores nominales para `InvoiceNo`, `StockCode` y `CustomerID`; fecha-hora para `InvoiceDate`; numéricos para `Quantity` y `UnitPrice`; texto para `Description` y `Country`.
- Cuantificar ausencias por columna y evaluar su distribución por periodo, país, tipo de factura u otros segmentos relevantes.
- Medir duplicados exactos de fila y revisar duplicación de identificadores según su papel: repetición esperable de `InvoiceNo` en múltiples líneas, de `StockCode` en ventas distintas y de `CustomerID` en compras repetidas.
- Examinar cardinalidad, normalización de espacios, mayúsculas u otras variaciones aparentes en `Description`, `StockCode` y `Country`.
- Verificar rango temporal, periodicidad disponible, fechas inválidas, fechas repetidas y posible incompletitud de los periodos inicial y final.
- Revisar signos, ceros, mínimos, máximos y cuantiles de `Quantity` y `UnitPrice`.
- Clasificar `InvoiceNo` según el prefijo documentado de cancelación y comprobar valores no convencionales de códigos, descripciones, cantidades y precios.
- Evaluar si existe una correspondencia estable entre `StockCode` y `Description`, sin asumirla de antemano.

**Variables o grupos:** Todas las variables; grupos por tipo de `InvoiceNo`, mes o fecha, `Country`, disponibilidad de `CustomerID` y `StockCode`.

**Evidencia esperada:** Análisis estructurados `STAT-NNN` de calidad, tipos, ausencias, duplicados, rangos, categorías y temporalidad; comprobaciones en `issues.json` tanto si detectan incidencias como si no.

**Supuestos o dependencias:** Los valores negativos o extremos no se considerarán errores automáticamente: podrán representar cancelaciones, devoluciones, ajustes o transacciones legítimas. La documentación no define reglas de validación de precios, cantidades ni códigos especiales.

## E3

**Objetivo:** Generar una copia preparada y trazable para el EDA, con transformaciones mínimas y justificadas.

**Comprobaciones:**
- Preservar todas las columnas originales necesarias y crear `prepared_data.csv` como archivo separado.
- Normalizar los tipos analíticos: fecha-hora de `InvoiceDate`, texto nominal de identificadores y categorías, y formato numérico de `Quantity` y `UnitPrice`, siempre que la conversión sea verificable.
- Evaluar si resulta necesario preservar explícitamente ceros iniciales o formatos mixtos en `InvoiceNo`, `StockCode` y `CustomerID`.
- Crear una clasificación derivada transparente para distinguir facturas regulares y cancelaciones documentadas, si los valores permiten hacerlo.
- Crear un importe de línea derivado, por ejemplo `LineAmount = Quantity × UnitPrice`, y variables temporales de apoyo si facilitan agregaciones reproducibles.
- Decidir y documentar el tratamiento de ausencias de `Description` y `CustomerID`, evitando imputar identificadores o descripciones sin evidencia.
- Decidir el tratamiento de duplicados exactos y de filas con valores no positivos solo después de describirlos y contextualizarlos.
- Comparar dimensiones, columnas, ausencias y población antes y después de la preparación.

**Variables o grupos:** Variables originales; posibles derivadas como indicador de cancelación, `LineAmount`, fecha diaria, mes y componentes horarios, si se justifican.

**Evidencia esperada:** `prepared_data.csv`; perfil antes-después; listado de cambios `TR-NNN` con motivo, población afectada y criterio aplicado en `statistics.json`.

**Supuestos o dependencias:** El análisis puede requerir más de una población explícita, por ejemplo: todas las líneas preparadas, líneas regulares, y líneas con `CustomerID` disponible. Cualquier exclusión deberá conservarse como decisión trazable y no borrar la posibilidad de interpretar cancelaciones.

## E4

**Objetivo:** Obtener una descripción reproducible de la actividad registrada y de las variables cuantitativas principales.

**Comprobaciones:**
- Calcular conteos de líneas, facturas distintas, productos o códigos distintos, clientes identificados y países, aclarando la población de cada medida.
- Resumir `Quantity`, `UnitPrice` y `LineAmount` mediante medidas robustas y de dispersión apropiadas, cuantiles, extremos y proporciones de valores negativos, nulos o positivos cuando existan.
- Describir frecuencias de categorías de `Country`, tipo de factura, disponibilidad de `CustomerID` y códigos o descripciones de producto, con tratamiento adecuado de alta cardinalidad.
- Calcular estadísticas separadas para todas las líneas y, si es pertinente, para líneas regulares y cancelaciones.
- Resumir la concentración de la actividad en grupos relevantes sin interpretar identificadores nominales como variables métricas.

**Variables o grupos:** `Quantity`, `UnitPrice`, `LineAmount`; `Country`; tipo de `InvoiceNo`; `CustomerID` disponible/no disponible; `StockCode`; `Description`.

**Evidencia esperada:** Resultados `STAT-NNN` estructurados con población, método y resultados escalares o tabulares; referencias reutilizables en el informe final.

**Supuestos o dependencias:** La media puede ser sensible a importes o cantidades extremos; se complementará con mediana, cuantiles u otras medidas resistentes cuando la distribución lo requiera.

## E5

**Objetivo:** Examinar agregaciones y asociaciones descriptivas pertinentes entre tiempo, artículos, clientes, países, cantidades, precios e importes.

**Comprobaciones:**
- Agregar actividad por fecha o mes para describir evolución de líneas, facturas, unidades, importes y cancelaciones, diferenciando métricas brutas y netas cuando sea necesario.
- Comparar países por número de líneas, facturas, clientes identificados, unidades e importes, indicando el efecto de la concentración o de la falta de `CustomerID`.
- Identificar artículos, códigos o descripciones con mayor actividad bajo métricas justificadas y con selección limitada a categorías más frecuentes o de mayor importe, sin usar rankings extensos sin contexto.
- Describir la distribución de actividad por cliente únicamente entre `CustomerID` observados, por ejemplo facturas, líneas o importe agregado por cliente.
- Explorar relaciones entre `Quantity`, `UnitPrice` y `LineAmount` mediante resúmenes, correlaciones o representaciones adecuadas, con filtros o escalas explícitas si los extremos dominan la lectura.
- Comprobar identidades derivadas, como la correspondencia aritmética de `LineAmount` con sus componentes, y evaluar relaciones entre `StockCode` y `Description`.
- Comparar patrones temporales y por país o tipo de factura únicamente como asociaciones descriptivas.

**Variables o grupos:** Fecha y mes derivados de `InvoiceDate`; `InvoiceNo`; indicador de cancelación; `Quantity`; `UnitPrice`; `LineAmount`; `Country`; `CustomerID`; `StockCode`; `Description`.

**Evidencia esperada:** Varios `STAT-NNN` de agregaciones temporales, segmentación geográfica, actividad de artículos, actividad de clientes identificados y asociaciones numéricas; interpretación prudente de cada resultado.

**Supuestos o dependencias:** Las facturas con múltiples líneas requieren agregación por `InvoiceNo` para métricas a nivel factura. No se inferirá que importes positivos representen ventas definitivas ni que diferencias entre países o clientes tengan una causa específica.

## E6

**Objetivo:** Producir visualizaciones legibles que respondan a preguntas analíticas centrales y estén vinculadas a resultados estructurados.

**Comprobaciones:**
- Seleccionar gráficos según distribución, temporalidad, concentración o comparación de grupos.
- Incorporar títulos, ejes, unidades monetarias cuando corresponda, leyendas y notas de población o filtros cuando sean necesarias.
- Evaluar escalas lineales, logarítmicas, recortes visuales o paneles complementarios para no ocultar la estructura por valores extremos.
- Registrar cada figura válida en `statistics.json` y citarla en el informe.

**Variables o grupos:** Agregaciones temporales de `InvoiceDate`, métricas derivadas de `Quantity` y `UnitPrice`, `Country`, tipo de factura y categorías de artículos seleccionadas por una regla documentada.

**Evidencia esperada:** Archivos PNG legibles en `figures/` y registros `FIG-NNN` conectados a los análisis `STAT-NNN` que los respaldan.

**Supuestos o dependencias:** Las figuras dependerán de los hallazgos de calidad y de la distribución efectiva. Se evitarán gráficos de miles de categorías individuales o nubes ilegibles sin agregación, muestreo o transformación justificada.

## E7

**Objetivo:** Consolidar problemas, anomalías, riesgos analíticos y decisiones pendientes de incertidumbre.

**Comprobaciones:**
- Registrar las pruebas de calidad efectuadas aunque no arrojen incidencias.
- Documentar ausencias, duplicados exactos, incoherencias de tipo o categoría, valores no positivos, extremos, correspondencias ambiguas entre código y descripción, y riesgos temporales.
- Distinguir incidencias resueltas de valores retenidos deliberadamente y de situaciones cuyo significado no pueda verificarse con la documentación disponible.
- Describir filas o poblaciones afectadas, evidencias, acciones adoptadas, posibles efectos sobre resultados y nivel de incertidumbre.
- Comprobar que las exclusiones o transformaciones de E3 están reflejadas coherentemente en los riesgos y decisiones.

**Variables o grupos:** Todas las columnas; especial atención a `Description`, `CustomerID`, `InvoiceNo`, `Quantity`, `UnitPrice`, `InvoiceDate`, `StockCode` y `Country`.

**Evidencia esperada:** `issues.json` con comprobaciones `CHK-NNN` e incidencias `ISSUE-NNN` respaldadas por referencias a `STAT-NNN`; sección de limitaciones consistente en `statistics.json`.

**Supuestos o dependencias:** La ausencia de documentación operativa detallada impide determinar con certeza el significado de todo código especial, ajuste o importe extremo; esa incertidumbre deberá quedar explícita.

## E8

**Objetivo:** Integrar el EDA en un informe final verificable, prudente y coherente con los artefactos generados.

**Comprobaciones:**
- Explicar fuente disponible, periodo documentado, unidad de observación y alcance estrictamente exploratorio.
- Resumir inspección, calidad, decisiones de preparación y poblaciones analizadas.
- Presentar estadísticas y relaciones principales con referencias a `STAT-NNN`, incidencias con `ISSUE-NNN` y figuras con `FIG-NNN`.
- Diferenciar hechos calculados, interpretación descriptiva y explicaciones que no puedan verificarse.
- Incluir limitaciones ligadas a ausencias, cancelaciones, representatividad de clientes identificados, periodos potencialmente incompletos, extremos y semántica limitada de códigos.
- Verificar consistencia de dimensiones, identificadores, rutas relativas y referencias entre `prepared_data.csv`, JSON, figuras e informe.

**Variables o grupos:** Resultados consolidados de todas las variables y subpoblaciones definidas en E1–E7.

**Evidencia esperada:** `report.md` con las secciones requeridas y referencias internas válidas, coherentes con `statistics.json`, `issues.json` y las figuras.

**Supuestos o dependencias:** Toda afirmación cuantitativa deberá ser trazable a un resultado conservado. No se presentarán asociaciones observadas como relaciones causales ni se entrenarán modelos predictivos.

# Visualizaciones previstas

- **Evolución temporal de la actividad:** representar por fecha o mes el número de líneas, facturas y/o importe de línea para describir cambios en el volumen registrado y contextualizar la cobertura temporal.
- **Distribución de cantidades, precios e importes de línea:** mostrar la forma de las distribuciones y la influencia de extremos mediante una escala, panel o filtro visual claramente declarado; el objetivo es distinguir concentración central de colas sin eliminar datos por la visualización.
- **Comparación entre facturas regulares y cancelaciones:** visualizar recuentos, cantidades o importes agregados por tipo de factura para describir diferencias registradas conforme al prefijo documentado de `InvoiceNo`.
- **Actividad por países:** comparar los países más relevantes bajo una métrica seleccionada y declarada, como facturas, importe o líneas, evitando una representación ilegible de todas las categorías si la concentración lo desaconseja.
- **Concentración de artículos o descripciones:** representar un conjunto limitado de productos seleccionado por una regla reproducible, para mostrar qué categorías concentran actividad según unidades, líneas o importe.
- **Relación entre `Quantity` y `UnitPrice`:** utilizar una visualización adecuada para explorar asociación descriptiva y heterogeneidad, con tratamiento explícito de alta densidad, importes extremos o subpoblaciones de cancelación.

La selección final dependerá de las comprobaciones de calidad, de la cardinalidad efectiva y de la legibilidad; cada figura deberá responder a una pregunta analítica y estar respaldada por resultados estructurados.

# Supuestos y riesgos

- La documentación pública establece que las filas son líneas de factura y que un prefijo `C` en `InvoiceNo` indica cancelación; deberán verificarse las variantes de formato efectivamente presentes.
- `InvoiceNo`, `StockCode` y `CustomerID` son identificadores nominales, aunque el archivo pueda representarlos con tipos numéricos o mixtos. No deberán emplearse como magnitudes continuas.
- La presencia de ausencias en `Description` o `CustomerID` deberá cuantificarse y analizarse antes de decidir exclusiones. Los resultados centrados en clientes solo serán representativos de líneas con identificador disponible.
- Cantidades, precios o importes negativos, nulos o extremos pueden ser transacciones legítimas, devoluciones, cancelaciones, gastos, ajustes u otros conceptos; sin evidencia adicional no deben etiquetarse como errores.
- Las líneas aparentemente duplicadas pueden ser repeticiones comerciales válidas. Solo los duplicados exactos se considerarán candidatos a tratamiento, tras documentar su alcance.
- La asociación entre `StockCode` y `Description` puede no ser uno a uno por variaciones de descripción, códigos especiales o cambios de catálogo; deberá comprobarse antes de agrupar por una de esas variables.
- El intervalo temporal documentado puede incluir periodos parciales en los extremos o variación por días no operativos; cualquier patrón de calendario se interpretará con cautela.
- El importe derivado `Quantity × UnitPrice` es una medida descriptiva de línea y no prueba por sí misma cobro, rentabilidad, ingreso neto ni valor final de una compra.
- Las comparaciones entre países, clientes o productos estarán condicionadas por la composición de facturas, disponibilidad de identificadores y posibles cancelaciones; no respaldarán explicaciones causales.
- Las transformaciones deberán ser mínimas, reproducibles, registradas con identificadores `TR-NNN` y no modificarán el archivo original.

# Criterios de finalización

- Se habrá dejado evidencia de carga correcta del archivo `xlsx`, hoja utilizada, estructura, columnas y unidad de análisis.
- El perfil original y preparado declarará dimensiones coherentes, todos los campos finales, tipos, ausencias y cardinalidad calculada cuando corresponda.
- Se habrán realizado y registrado comprobaciones de tipos, ausencias, duplicados, categorías, rangos, fechas, cancelaciones, extremos e identidades pertinentes.
- Existirá `prepared_data.csv` separado del original, con las transformaciones, conservaciones y exclusiones justificadas en `statistics.json`.
- `statistics.json` tendrá estructura válida, identificadores únicos, análisis reproducibles de E1–E7, limitaciones y referencias correctas a figuras.
- Se habrán producido estadísticas descriptivas, agregaciones y relaciones relevantes para tiempo, tipo de factura, países, productos y clientes identificados, según lo permitan los datos.
- Existirá al menos una figura PNG legible y cada visualización registrada responderá a un objetivo analítico, tendrá ruta relativa válida y estará vinculada a análisis `STAT-NNN`.
- `issues.json` incluirá comprobaciones realizadas y las incidencias o riesgos respaldados, con decisiones, efectos potenciales e incertidumbre.
- `report.md` cubrirá las ocho etapas con las secciones requeridas, incluirá referencias resolubles a estadísticas, incidencias y figuras, y distinguirá descripción, interpretación y limitaciones.
- Se comprobará la coherencia final entre dimensiones, archivos, rutas, identificadores y referencias, preservando en todo momento el archivo original.