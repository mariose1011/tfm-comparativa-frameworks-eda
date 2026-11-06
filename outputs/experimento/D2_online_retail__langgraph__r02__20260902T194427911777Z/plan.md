# Identificación

- **run_id:** `D2_online_retail__langgraph__r02__20260902T194427911777Z`
- **framework_id:** `langgraph`
- **dataset_id:** `D2_online_retail`
- **contract_version:** `1.0`
- **prompt_version:** `1.0`

# Comprensión inicial

El archivo de entrada tiene formato XLSX y la hoja seleccionada es `Online Retail`. La inspección estructural inicial identifica las variables `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID` y `Country`.

Según la documentación pública, cada fila representa una línea de factura, no necesariamente una factura completa, una compra individual ni un cliente. El alcance temporal documentado comprende transacciones entre diciembre de 2010 y diciembre de 2011 de una empresa británica de comercio electrónico, cuyos artículos son principalmente regalos y cuya clientela puede incluir mayoristas.

`InvoiceNo`, `StockCode` y `CustomerID` deben tratarse inicialmente como identificadores nominales, incluso si algunos valores presentan una codificación que pueda parecer numérica. La documentación indica que los valores de `InvoiceNo` que comienzan por `C` corresponden a cancelaciones; el Analista deberá comprobar cómo se manifiesta esta regla en el archivo y decidir si analiza conjuntamente líneas registradas y cancelaciones o si crea poblaciones diferenciadas.

Quedan por verificar la consistencia entre códigos y descripciones, la calidad de identificadores y categorías, la interpretación de cantidades o precios no positivos, la cobertura efectiva de los extremos temporales y la existencia de conceptos facturados que no correspondan a productos ordinarios.

# Preguntas analíticas

1. ¿Cuál es la estructura efectiva del archivo, qué tipos se requieren para cada variable y qué proporción de registros permite análisis por cliente, artículo, país y periodo?
2. ¿Cómo se distribuyen `Quantity`, `UnitPrice` y el importe de línea derivado de ambas variables, considerando separadamente las cancelaciones u otras líneas con signo o valor atípico?
3. ¿Cuál es la evolución temporal de las líneas, unidades e importes, y qué periodos deben interpretarse con cautela por posible cobertura parcial?
4. ¿Qué países, artículos y descripciones concentran mayor actividad o importe dentro de una población analítica explícitamente definida?
5. ¿Cómo difieren los patrones de compra observados entre clientes identificados, países y periodos, sin atribuir causalidad?
6. ¿Qué relación descriptiva existe entre cantidad, precio unitario e importe de línea, y qué parte de los valores extremos parece compatible con transacciones reales frente a posibles incidencias?
7. ¿Hay duplicados exactos, identificadores nominales con formatos heterogéneos, descripciones inconsistentes o valores que condicionen la interpretación de agregaciones?
8. ¿Cómo cambian los resultados principales al conservar el archivo como población completa frente a usar subconjuntos preparados para análisis específicos?

# Plan por etapas

## E1

**Objetivo:** Cargar el archivo XLSX sin modificarlo y documentar una comprensión inicial verificable de su contenido y unidad de observación.

**Comprobaciones:** Confirmar la hoja leída, dimensiones, nombres y orden de columnas, una muestra de inicio, final y posiciones intermedias, y los tipos inferidos al cargar. Contrastar el significado de las variables con el diccionario público y verificar que cada registro se interpreta como línea de factura.

**Variables o grupos:** Todas las variables originales; en particular, `InvoiceNo` para distinguir la unidad de línea frente a la factura agregada.

**Evidencia esperada:** Perfil original en `statistics.json`, descripción de la unidad de análisis, referencia al archivo y hoja de origen, y trazabilidad de la carga sin sobrescritura del XLSX.

**Supuestos o dependencias:** Se parte de que la hoja `Online Retail` contiene la tabla analítica principal. Si hubiera variaciones entre estructura observada y documentación, se registrarán en lugar de asumir equivalencia.

## E2

**Objetivo:** Caracterizar estructura, tipos y calidad de los datos antes de aplicar transformaciones.

**Comprobaciones:** Revisar tipos observados frente a los semánticos esperados; cuantificar ausencias por variable; detectar filas completamente duplicadas y duplicados bajo combinaciones razonables de columnas sin confundir líneas legítimas repetidas con errores; medir cardinalidad y normalización aparente de categorías. Examinar signos, ceros, rangos y cuantiles de `Quantity` y `UnitPrice`; comprobar los formatos de `InvoiceNo`, `StockCode` y `CustomerID`; validar el parseo, mínimo, máximo y continuidad temporal de `InvoiceDate`. Verificar la regla documentada de prefijo `C` para cancelaciones y explorar su correspondencia con signos e importes.

**Variables o grupos:** `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID` y `Country`; grupos de cancelación/no cancelación, país y mes cuando proceda.

**Evidencia esperada:** Análisis estructurados de calidad con identificadores `STAT-NNN`, comprobaciones en `issues.json`, recuentos de ausencias, duplicidad, cardinalidad, cobertura temporal y revisiones de rango.

**Supuestos o dependencias:** Los valores extremos no se clasificarán como errores únicamente por su magnitud. La identificación de una cancelación se basará inicialmente en la regla publicada y se comprobará contra los registros.

## E3

**Objetivo:** Crear una copia de trabajo trazable, conservando la población original cuando sea posible y definiendo subpoblaciones analíticas explícitas cuando sea necesario.

**Comprobaciones:** Convertir `InvoiceDate` a una representación temporal no ambigua si fuera necesario; asegurar que los identificadores se preservan como categorías o cadenas nominales y no como medidas; evaluar el tratamiento de ausencias de `Description` y `CustomerID`; decidir el tratamiento de duplicados exactos tras revisar su contexto; y conservar por defecto valores extremos plausibles. Crear variables derivadas justificadas, previsiblemente `line_amount = Quantity * UnitPrice`, un indicador de cancelación basado en `InvoiceNo` y componentes temporales adecuados para agregaciones.

**Variables o grupos:** Todas las columnas fuente y las derivadas que sean necesarias, especialmente `line_amount`, estado de cancelación y periodo derivado de `InvoiceDate`.

**Evidencia esperada:** `prepared_data.csv` separado del original; perfil antes-después; registro de transformaciones `TR-NNN` que incluya tanto cambios como decisiones deliberadas de conservación; y una comparación de dimensiones, ausencias y columnas entre original y copia preparada.

**Supuestos o dependencias:** No se imputará `CustomerID` ni `Description` sin fundamento verificable. La decisión de incluir o excluir cancelaciones de un análisis dependerá de su objetivo y deberá documentarse; no se eliminarán globalmente sin justificación.

## E4

**Objetivo:** Resumir de forma reproducible las variables, líneas y agregados relevantes en poblaciones claramente definidas.

**Comprobaciones:** Obtener conteos de líneas, facturas, clientes identificados, artículos y países; frecuencias de categorías relevantes; y medidas de centro, dispersión, cuantiles, mínimos y máximos para `Quantity`, `UnitPrice` y `line_amount`. Calcular resúmenes separados, cuando sean pertinentes, para líneas ordinarias, cancelaciones y población completa. Incorporar estadísticas por país, periodo y condición de identificación de cliente, evitando interpretar identificadores como variables métricas.

**Variables o grupos:** `Quantity`, `UnitPrice`, `line_amount`, indicador de cancelación, `Country`, periodos de `InvoiceDate`, `StockCode`, `Description` y disponibilidad de `CustomerID`.

**Evidencia esperada:** Resultados `STAT-NNN` estructurados que indiquen población, filtros, método y unidades monetarias en libras esterlinas cuando corresponda.

**Supuestos o dependencias:** El importe de línea será una identidad derivada verificable de cantidad por precio unitario; su interpretación como ventas netas dependerá de cómo se traten cancelaciones y otros conceptos especiales.

## E5

**Objetivo:** Examinar agregaciones y relaciones descriptivas útiles entre artículos, tiempo, geografía, facturas y clientes identificados.

**Comprobaciones:** Agregar actividad por mes o una granularidad temporal respaldada por la cobertura observada; comparar líneas, unidades, importes y facturas entre países; identificar artículos o descripciones con mayor presencia o importe bajo reglas explícitas; y resumir comportamiento por cliente únicamente entre `CustomerID` disponibles. Explorar la asociación descriptiva entre `Quantity`, `UnitPrice` y `line_amount`, con métodos robustos o estratificaciones si la distribución lo requiere. Comprobar la identidad de `line_amount` y si un mismo `StockCode` se vincula con varias `Description` o precios.

**Variables o grupos:** Periodos de `InvoiceDate`, `Country`, `InvoiceNo`, `StockCode`, `Description`, `CustomerID`, `Quantity`, `UnitPrice`, `line_amount` e indicador de cancelación.

**Evidencia esperada:** Agregaciones temporales, geográficas, por producto y por cliente identificable; análisis de consistencia código-descripción; y resultados de relaciones descriptivas en `statistics.json`.

**Supuestos o dependencias:** Las agrupaciones por cliente excluirán o separarán registros sin `CustomerID`, no los asignarán a un cliente genérico. Las asociaciones se reportarán como patrones descriptivos, sin inferir mecanismos causales ni rentabilidad.

## E6

**Objetivo:** Generar visualizaciones legibles que respondan a preguntas analíticas y complementen las tablas estructuradas.

**Comprobaciones:** Evaluar escalas, concentración, alta cardinalidad y presencia de valores extremos antes de elegir el diseño final. Usar filtros, escala logarítmica, paneles o resúmenes agregados únicamente cuando ayuden a representar distribuciones sin ocultar la población ni la regla aplicada.

**Variables o grupos:** Series temporales derivadas de `InvoiceDate`; agregados por `Country`; productos representados por `StockCode` y/o `Description`; y variables monetarias y de cantidad.

**Evidencia esperada:** Archivos PNG válidos en `figures/`, con títulos, ejes, unidades y leyendas necesarios; y entradas `FIG-NNN` que referencien los `STAT-NNN` de respaldo.

**Supuestos o dependencias:** La selección final dependerá de los resultados de calidad y concentración. No se usarán gráficos de identificadores de alta cardinalidad sin una agregación interpretables.

## E7

**Objetivo:** Consolidar problemas, riesgos y anomalías observados, separando evidencia, decisión y posible efecto sobre la interpretación.

**Comprobaciones:** Registrar resultados de todas las revisiones de ausencias, duplicados, tipos, categorías, rangos, identidades, tiempo y extremos, incluso si no detectan una incidencia. Para cada hallazgo, cuantificar el alcance, aportar muestra limitada de posiciones si es pertinente, establecer su incertidumbre y documentar la acción aplicada o recomendada.

**Variables o grupos:** Todas las columnas, con prioridad para ausencias de `CustomerID` y `Description`, potenciales duplicados, codificaciones de `InvoiceNo` y `StockCode`, cancelaciones, valores no positivos y extremos de `Quantity`, `UnitPrice` y `line_amount`.

**Evidencia esperada:** `issues.json` con comprobaciones `CHK-NNN` no vacías e incidencias `ISSUE-NNN` respaldadas por análisis `STAT-NNN`; limitaciones coherentes en `statistics.json` y el informe.

**Supuestos o dependencias:** Un hallazgo puede quedar con estado retenido, sospechado o no resuelto si la documentación no permite confirmar error. No se presentarán como errores los valores infrecuentes que sean compatibles con la operación comercial.

## E8

**Objetivo:** Integrar el EDA en un informe final trazable, prudente y coherente con los artefactos generados.

**Comprobaciones:** Redactar el alcance, unidad de análisis, decisiones de preparación, estadísticas, agregaciones, relaciones, figuras, problemas y limitaciones. Verificar que toda afirmación cuantitativa tenga referencias `STAT-NNN`, `ISSUE-NNN` o `FIG-NNN` válidas y que las figuras enlazadas existan. Distinguir resultados observados de interpretaciones y explicaciones posibles.

**Variables o grupos:** Los elementos relevantes identificados en las etapas previas; no se incorporarán datos externos ni análisis predictivos.

**Evidencia esperada:** `report.md` con las secciones obligatorias, referencias internas resolubles y conclusiones limitadas a los resultados calculados.

**Supuestos o dependencias:** El informe dependerá de la consistencia final entre `prepared_data.csv`, `statistics.json`, `issues.json` y `figures/`. Si una decisión del plan no resulta aplicable tras la inspección, el cambio se justificará en los artefactos de análisis.

# Visualizaciones previstas

- **Evolución temporal agregada:** representar líneas, unidades y/o importe de línea por periodo para describir la actividad registrada y revisar visualmente posibles tramos de cobertura parcial. Variables: `InvoiceDate`, `Quantity`, `line_amount`, indicador de cancelación.
- **Distribución de importes y cantidades:** mostrar la forma, concentración y extremos de `Quantity`, `UnitPrice` o `line_amount`, aplicando una escala o partición justificada si los extremos impiden la lectura. Variables: `Quantity`, `UnitPrice`, `line_amount`.
- **Comparación geográfica agregada:** comparar países mediante una métrica seleccionada y una regla explícita para categorías de baja frecuencia, evitando gráficos ilegibles por cardinalidad. Variables: `Country`, `InvoiceNo`, `Quantity`, `line_amount`.
- **Productos o descripciones principales:** visualizar los artículos con mayor actividad o importe dentro de la población definida, usando una selección limitada y documentada. Variables: `StockCode`, `Description`, `Quantity`, `line_amount`.
- **Relación precio-cantidad o precio-importe:** representar la asociación descriptiva entre variables de línea, diferenciando o filtrando cancelaciones cuando ello sea necesario para la interpretación. Variables: `Quantity`, `UnitPrice`, `line_amount`, indicador de cancelación.

La necesidad, métrica exacta y diseño final de cada figura se decidirán según los resultados de las etapas E2 a E5; se generarán solo las visualizaciones que aporten evidencia legible y pertinente.

# Supuestos y riesgos

- `InvoiceNo`, `StockCode` y `CustomerID` son identificadores nominales; su apariencia numérica no autoriza operaciones aritméticas sobre ellos.
- La documentación establece una regla para cancelaciones basada en el prefijo `C` de `InvoiceNo`; deberá contrastarse con los datos y no sustituirse por inferencias basadas solo en el signo de una variable.
- Las líneas sin `CustomerID` pueden limitar análisis por cliente y no deben imputarse sin fuente autorizada.
- Una misma factura puede contener múltiples líneas y una misma línea repetida puede ser legítima; por ello, los duplicados exactos y los duplicados por claves parciales requieren interpretaciones distintas.
- `StockCode` podría incluir códigos para conceptos distintos de productos ordinarios; el Analista deberá verificar esta posibilidad antes de interpretar rankings de productos.
- Un mismo `StockCode` puede potencialmente asociarse a diferentes descripciones, y una descripción a distintos códigos; se deberá medir antes de usar cualquiera como definición única de producto.
- Cantidades negativas, precios nulos o negativos, e importes extremos pueden reflejar cancelaciones, ajustes u operaciones válidas, además de posibles errores. Se conservarán o excluirán solo bajo reglas explícitas.
- Los extremos iniciales y finales del periodo documentado podrían no representar meses completos; las comparaciones temporales deberán comprobar la cobertura efectiva.
- Las ventas o importes calculados a partir de `Quantity * UnitPrice` describen líneas registradas y no garantizan medidas contables completas, margen, pago, entrega ni comportamiento causal.
- El dataset no aporta variables para medir inventario, costes, campañas, canales, devoluciones confirmadas, causalidad o representatividad fuera de las transacciones registradas.

# Criterios de finalización

- Se habrá preservado el XLSX original y cargado una copia de trabajo verificable.
- `prepared_data.csv` existirá, será legible, tendrá encabezados y sus filas, columnas, tipos y diferencias respecto al origen estarán documentados.
- `statistics.json` cumplirá su esquema, incluirá el perfil original y preparado, transformaciones `TR-NNN`, análisis `STAT-NNN`, figuras `FIG-NNN` y limitaciones.
- Se habrán realizado comprobaciones cuantificadas de estructura, ausencias, duplicados, categorías, tipos, fechas, rangos, cancelaciones, identidades y extremos cuando resulten evaluables.
- `issues.json` incluirá comprobaciones `CHK-NNN` y, cuando exista evidencia, incidencias `ISSUE-NNN` con decisión, acción, incertidumbre y efecto potencial.
- Las estadísticas descriptivas y agregaciones cubrirán poblaciones claramente definidas, incluida una consideración explícita de las cancelaciones y de la ausencia de identificador de cliente.
- Se habrán examinado varias relaciones o agregaciones pertinentes entre tiempo, país, producto, cliente identificado, cantidad, precio e importe, sin entrenamiento predictivo ni inferencias causales.
- El directorio `figures/` contendrá al menos una figura PNG válida, legible y registrada, y cada figura responderá a una pregunta analítica identificable.
- `report.md` incluirá todas las secciones obligatorias, describirá unidad y alcance, resumirá decisiones y hallazgos respaldados, y usará referencias internas válidas.
- Los artefactos finales serán coherentes entre sí: dimensiones, identificadores, rutas relativas, citas y poblaciones analíticas deberán poder rastrearse sin recurrir a información externa.