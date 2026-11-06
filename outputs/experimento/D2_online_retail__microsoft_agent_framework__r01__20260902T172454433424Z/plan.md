# Identificación

- **run_id:** `D2_online_retail__microsoft_agent_framework__r01__20260902T172454433424Z`
- **framework_id:** `microsoft_agent_framework`
- **dataset_id:** `D2_online_retail`
- **contract_version:** `1.0`
- **prompt_version:** `1.0`

# Comprensión inicial

El archivo de entrada tiene formato `xlsx` y la hoja seleccionada es `Online Retail`. La inspección inicial autorizada indica una tabla con ocho columnas documentadas: `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID` y `Country`.

Según la documentación pública, cada fila representa una **línea de factura**, no necesariamente una compra o factura completa. El alcance temporal publicado comprende transacciones entre el 1 de diciembre de 2010 y el 9 de diciembre de 2011 de una empresa británica de comercio electrónico; esta cobertura deberá verificarse directamente durante el análisis, incluyendo si los extremos temporales representan periodos parciales.

Las variables `InvoiceNo`, `StockCode` y `CustomerID` son identificadores nominales y deberán tratarse como categorías, aunque el lector del archivo haya podido representar algunos valores con apariencia numérica. `InvoiceNo` puede empezar por `C` para identificar cancelaciones conforme a la documentación. `Quantity` registra unidades de la línea y `UnitPrice` el precio unitario en libras esterlinas. La inspección inicial muestra ausencias en `Description` y `CustomerID`, que deberán caracterizarse y tratarse de forma explícita, sin asumir su causa.

Todavía deben comprobarse, entre otros aspectos, la existencia de duplicados exactos, la coherencia entre códigos y descripciones, la presencia y alcance de cancelaciones, los signos y valores cero de importes o cantidades, el uso de códigos para conceptos no equivalentes a productos, la consistencia de `Country` y la validez analítica de los posibles extremos.

# Preguntas analíticas

1. ¿Cuál es la estructura efectiva de las líneas de factura, su periodo temporal observado y la composición entre facturas ordinarias y cancelaciones identificables por `InvoiceNo`?
2. ¿Qué tipos, ausencias, duplicados, valores no positivos y posibles incoherencias presentan las variables documentadas?
3. ¿Qué proporción de líneas puede asociarse a un `CustomerID` y cómo condicionan las ausencias de ese identificador los análisis por cliente?
4. ¿Cómo se distribuyen `Quantity`, `UnitPrice` y un importe de línea derivado como `Quantity × UnitPrice`, distinguiendo la población total de subconjuntos justificadamente definidos?
5. ¿Cómo evolucionan los recuentos, unidades e importes de línea a lo largo del tiempo, y qué cautelas requiere la cobertura del primer y último mes?
6. ¿Cómo varían los indicadores descriptivos por `Country`, artículos o descripciones de mayor actividad, y por estado de cancelación cuando sea aplicable?
7. ¿Qué relación descriptiva existe entre cantidad, precio unitario e importe de línea, y qué parte de los resultados puede estar dominada por extremos o conceptos especiales?
8. ¿Qué decisiones de preparación conservan mejor la trazabilidad al archivo original y permiten comparar resultados de líneas, facturas y clientes sin confundir sus unidades de análisis?

# Plan por etapas

## E1

**Objetivo:** Cargar el archivo sin modificarlo y confirmar la estructura inicial, la unidad de observación y el alcance que permite la documentación.

**Comprobaciones:**
- Verificar el archivo `xlsx`, la hoja utilizada y la lectura correcta de sus registros.
- Confirmar dimensiones, nombres, orden de columnas y una muestra estructural de inicio, final y registros diversos.
- Contrastar las columnas observadas con el diccionario público.
- Confirmar que la unidad primaria es una línea de factura y distinguirla de posibles agregaciones posteriores por `InvoiceNo`, `CustomerID`, artículo, país o periodo.
- Registrar el periodo observado en `InvoiceDate` sin anticipar que coincida exactamente con el rango publicado.

**Variables o grupos:** Todas las columnas; en particular `InvoiceNo`, `InvoiceDate` y las claves nominales para delimitar unidades de análisis.

**Evidencia esperada:** Perfil inicial reproducible con dimensiones, esquema, muestra estructural, fuente documental consultada, unidad de análisis y rango temporal observado, conservado como análisis de etapa E1 en `statistics.json`.

**Supuestos o dependencias:** Se parte de que la hoja `Online Retail` es la tabla de transacciones prevista; deberá verificarse que no contiene cabeceras adicionales, notas o filas ajenas a las líneas de factura.

## E2

**Objetivo:** Caracterizar tipos, integridad, categorías, rangos y riesgos de calidad antes de tomar decisiones de preparación.

**Comprobaciones:**
- Comparar los tipos observados con los tipos semánticos esperados: identificadores nominales, texto descriptivo, fecha-hora, cantidad entera y precio monetario.
- Cuantificar valores ausentes por columna, incluidos patrones de coexistencia entre ausencia de `Description` y `CustomerID`.
- Contar duplicados de fila completa y evaluar repeticiones de combinaciones relevantes sin tratar automáticamente como duplicadas las líneas que puedan pertenecer a la misma factura.
- Calcular cardinalidades de identificadores y categorías, incluyendo `Country`; revisar espacios, mayúsculas, valores vacíos encubiertos y categorías potencialmente inconsistentes.
- Revisar el formato de `InvoiceNo`, incluido el prefijo `C`, y la composición de `StockCode` para detectar códigos alfanuméricos, especiales o no comparables directamente como números.
- Examinar rangos, ceros, signos, cuantiles y extremos de `Quantity` y `UnitPrice`; localizar si existen importes potencialmente anómalos sin presuponer que sean errores.
- Verificar el rango y orden temporal de `InvoiceDate`, fechas inválidas, frecuencia temporal y posible incompletitud de meses de borde.
- Explorar consistencia de las relaciones `StockCode`–`Description`, `CustomerID`–`Country` e `InvoiceNo`–fecha/cliente, distinguiendo evidencia de inconsistencia de variaciones legítimas.

**Variables o grupos:** `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID`, `Country`; grupos por prefijo de `InvoiceNo`, ausencia de `CustomerID` y `Country`.

**Evidencia esperada:** Resultados cuantificados de perfil y calidad en `statistics.json`, y comprobaciones documentadas en `issues.json` con referencias a estadísticas. Los riesgos detectados deberán incluir filas o posiciones de muestra solo cuando su identificación sea necesaria y trazable.

**Supuestos o dependencias:** Una repetición de valores nominales o una cantidad/precio extremo no implica por sí misma un error. La interpretación de cancelaciones se limitará a la regla documental del prefijo `C`, sin inferir otros estados no documentados.

## E3

**Objetivo:** Crear una copia de trabajo reproducible, separada del original, que preserve la información necesaria para analizar líneas, cancelaciones y agregaciones posteriores.

**Comprobaciones:**
- Mantener las columnas fuente necesarias y estandarizar los tipos analíticos sin convertir los identificadores nominales en medidas.
- Normalizar la serialización de `InvoiceDate` a un formato inequívoco y representar identificadores de forma estable, respetando posibles valores alfanuméricos.
- Decidir y registrar el tratamiento de ausencias de `Description` y `CustomerID`; conservar filas cuando sean necesarias para la población de líneas y aplicar filtros explícitos solo a análisis que requieran identificación de cliente o artículo.
- Investigar los duplicados exactos antes de decidir conservarlos, excluirlos o señalar su incertidumbre.
- Crear variables derivadas únicamente si ayudan a responder las preguntas: por ejemplo, un indicador documentado de cancelación basado en `InvoiceNo`, importe de línea firmado (`Quantity × UnitPrice`), y componentes temporales para agregación.
- Evaluar separadamente cantidades, precios y líneas extremas antes de cualquier exclusión; en ausencia de evidencia concluyente, conservarlas y usar análisis segmentados o escalas robustas.
- Comparar filas y columnas antes y después, y documentar cada decisión como transformación o conservación deliberada.

**Variables o grupos:** Todas las variables fuente; posibles derivadas `LineAmount`, indicador de cancelación y periodos derivados de `InvoiceDate`.

**Evidencia esperada:** `prepared_data.csv` en UTF-8 y un registro de cambios `TR-NNN` en `statistics.json`, con justificación, columnas afectadas, número de filas afectadas cuando sea calculable y comparación básica original-preparada.

**Supuestos o dependencias:** El importe de línea derivado representa una multiplicación contable de los campos disponibles y puede ser negativo en cancelaciones o devoluciones registradas; no se asumirá que equivale a ingreso neto definitivo fuera de la información disponible.

## E4

**Objetivo:** Describir la población preparada con medidas adecuadas a variables nominales, temporales y numéricas, definiendo con claridad cada población de cálculo.

**Comprobaciones:**
- Obtener conteos de líneas, facturas distintas, clientes identificados, artículos/códigos y países, especificando los filtros aplicados.
- Resumir ausencias retenidas y la cobertura de identificación del cliente.
- Calcular frecuencias de cancelaciones según la regla documental y comparar, si procede, la actividad de líneas ordinarias y canceladas.
- Describir `Quantity`, `UnitPrice` y `LineAmount` con medidas robustas y de dispersión, cuantiles, mínimos y máximos, utilizando poblaciones separadas cuando los signos o extremos hagan engañoso un único resumen.
- Presentar frecuencias y participaciones de `Country`, y tablas de categorías o artículos relevantes seleccionadas con una regla reproducible.
- Generar resúmenes por grupos pertinentes, como país, mes, estado de cancelación o disponibilidad de `CustomerID`, sin interpretar los identificadores como variables ordinales.

**Variables o grupos:** `Quantity`, `UnitPrice`, `LineAmount` si se deriva, `Country`, `CustomerID`, `InvoiceNo`, estado de cancelación, `InvoiceDate` y `StockCode`/`Description`.

**Evidencia esperada:** Análisis estructurados `STAT-NNN` con definiciones de población, métodos y resultados tabulares o escalares reproducibles para el perfil descriptivo principal.

**Supuestos o dependencias:** Los resúmenes por cliente deberán limitarse a registros con `CustomerID` disponible y declarar la exclusión analítica que ello supone. Los resúmenes monetarios deberán indicar si incluyen cancelaciones, líneas no positivas o ambos.

## E5

**Objetivo:** Examinar patrones y relaciones descriptivas mediante agregaciones justificadas, sin atribuir causalidad.

**Comprobaciones:**
- Agregar actividad por periodo temporal apropiado, comprobando la cobertura de cada periodo antes de comparar sus totales.
- Comparar recuentos, unidades e importes de línea por `Country`, separando o complementando los análisis con la población de líneas ordinarias cuando sea pertinente.
- Examinar la concentración de actividad en artículos o descripciones mediante medidas o tablas reproducibles de participación, manejando su alta cardinalidad.
- Analizar la relación descriptiva entre `Quantity`, `UnitPrice` y `LineAmount`, con medidas robustas o gráficos transformados/segmentados cuando los extremos lo requieran.
- Comprobar si las cancelaciones, valores negativos o registros no asociados a cliente alteran sustancialmente las agregaciones principales.
- Realizar, si los datos lo sostienen, agregaciones a nivel de factura y de cliente identificado, distinguiéndolas explícitamente de la unidad original de línea.
- Revisar identidades derivadas y posibles redundancias, especialmente que el importe de línea se calcule coherentemente como producto de cantidad y precio unitario.

**Variables o grupos:** Periodos derivados de `InvoiceDate`; `Country`; `StockCode` y `Description`; `Quantity`; `UnitPrice`; `LineAmount`; `InvoiceNo`; `CustomerID`; indicador de cancelación.

**Evidencia esperada:** Varios resultados `STAT-NNN` de agregación y relación, cada uno con población, regla de agrupación, resultados y una interpretación limitada a patrones observados.

**Supuestos o dependencias:** Los comparativos entre países, clientes o artículos pueden reflejar distintas coberturas, tamaños de segmento y mezcla de cancelaciones. No se inferirá comportamiento individual de clientes sin `CustomerID`, ni se equiparará una línea con una transacción completa.

## E6

**Objetivo:** Producir visualizaciones legibles que respondan a preguntas del EDA y estén vinculadas a resultados numéricos reproducibles.

**Comprobaciones:**
- Seleccionar representaciones según distribución, cardinalidad y presencia de valores extremos.
- Etiquetar títulos, ejes, unidades monetarias en libras esterlinas cuando corresponda, leyendas, periodos y filtros aplicados.
- Aplicar escalas, límites, transformaciones o paneles justificados para mostrar extremos sin ocultar la estructura principal.
- Verificar que cada figura PNG exista, sea legible y esté registrada con un identificador `FIG-NNN`, su ruta relativa y los `STAT-NNN` de respaldo.

**Variables o grupos:** Series temporales derivadas de `InvoiceDate`; distribución de `Quantity`, `UnitPrice` y/o `LineAmount`; `Country`; productos o descripciones seleccionados mediante regla reproducible; estado de cancelación.

**Evidencia esperada:** Directorio `figures/` con PNG válidos y registro completo de cada figura en `statistics.json`; referencias cruzadas utilizables en el informe final.

**Supuestos o dependencias:** La elección final de figuras dependerá de los hallazgos de calidad y distribución. Las categorías de alta cardinalidad no deberán representarse íntegramente si comprometen legibilidad; el criterio de selección deberá quedar documentado.

## E7

**Objetivo:** Consolidar los problemas, riesgos y anomalías respaldados por comprobaciones, separando detección, incertidumbre y decisión de análisis.

**Comprobaciones:**
- Registrar todas las comprobaciones de calidad realizadas, incluso cuando no generen incidencias.
- Documentar ausencias, duplicados, tipos o formatos ambiguos, categorías inconsistentes, valores no positivos, extremos, posibles identidades no cumplidas y riesgos temporales si se confirman.
- Evaluar si las líneas con prefijo `C`, precios o cantidades atípicas, códigos especiales, descripciones ausentes y clientes no identificados son errores, casos de negocio o situaciones indeterminadas.
- Indicar población y variables afectadas, evidencia, decisión, acción aplicada o recomendada, efectos potenciales e incertidumbre.
- Asegurar coherencia entre las incidencias, la preparación, las estadísticas y las limitaciones del informe.

**Variables o grupos:** Todas las columnas, con foco en `Description`, `CustomerID`, `InvoiceNo`, `StockCode`, `Quantity`, `UnitPrice`, `InvoiceDate` y variables derivadas.

**Evidencia esperada:** `issues.json` válido con `checks_performed` no vacío, incidencias `ISSUE-NNN` solo cuando haya evidencia, y referencias a los análisis `STAT-NNN` pertinentes.

**Supuestos o dependencias:** La ausencia de un valor esperado o un extremo estadístico no probará un error de captura. Cuando la documentación no permita resolver el significado, el estado deberá reflejar incertidumbre y conservar el dato salvo una razón analítica explícita.

## E8

**Objetivo:** Integrar los resultados en un informe final verificable, prudente y coherente con la evidencia producida.

**Comprobaciones:**
- Describir dataset, fuente documental disponible, unidad de observación, periodo observado y alcance.
- Resumir las decisiones de preparación y diferenciar las poblaciones de líneas, facturas, clientes identificados, artículos y cancelaciones cuando aparezcan en los resultados.
- Presentar hallazgos descriptivos, agregaciones y relaciones con cifras y referencias `STAT-NNN`, `ISSUE-NNN` y `FIG-NNN`.
- Insertar o enlazar las visualizaciones existentes mediante rutas relativas.
- Exponer riesgos, incertidumbres, decisiones que pueden cambiar resultados y limitaciones de representatividad o identificación.
- Revisar que no haya afirmaciones causales ni conclusiones que excedan la documentación y los cálculos disponibles.

**Variables o grupos:** Todas las variables y resultados finales pertinentes; especial atención a poblaciones filtradas y a la distinción entre líneas de factura y agregaciones.

**Evidencia esperada:** `report.md` en español, estructurado con las secciones exigidas, referencias internas resolubles y afirmaciones cuantitativas trazables a `statistics.json`, `issues.json` y figuras existentes.

**Supuestos o dependencias:** El informe dependerá de que los resultados estructurados y las figuras hayan sido generados y validados. Las explicaciones posibles deberán presentarse como hipótesis o contexto documental, no como hechos establecidos por el análisis.

# Visualizaciones previstas

- **Evolución temporal de la actividad:** representar por mes o por otra frecuencia justificada el número de líneas, unidades y/o importe de línea. Objetivo: describir la evolución observada y hacer visible la cobertura parcial de periodos si se confirma. Variables: `InvoiceDate`, `Quantity`, `LineAmount` derivado y, si procede, estado de cancelación.
- **Distribución de medidas de línea:** usar una representación adecuada de `Quantity`, `UnitPrice` o `LineAmount` que haga visibles tanto la concentración principal como los extremos, mediante segmentación, escala alternativa o panel complementario si resulta necesario. Objetivo: evaluar asimetría, signos, ceros y valores extremos sin clasificarlos automáticamente como errores.
- **Actividad por país:** mostrar una comparación legible de países seleccionados con una regla reproducible, por ejemplo según recuento o importe dentro de una población declarada. Objetivo: describir concentración y heterogeneidad geográfica. Variables: `Country`, recuento de líneas, `Quantity` y/o `LineAmount`.
- **Productos o descripciones de mayor actividad:** visualizar un conjunto limitado y reproduciblemente seleccionado de `StockCode` o `Description`. Objetivo: mostrar concentración por artículo sin sobrecargar una categoría de alta cardinalidad. Variables: `StockCode`, `Description`, recuentos, unidades o importes.
- **Relación entre cantidad y precio:** emplear dispersión, hexbin, agregación o alternativa equivalente según densidad y extremos. Objetivo: explorar la asociación descriptiva entre `Quantity` y `UnitPrice`, con separación de cancelaciones u otros subconjuntos si ello mejora la interpretación. Variables: `Quantity`, `UnitPrice`, estado de cancelación y/o `LineAmount`.

La selección final podrá ajustarse si las comprobaciones de distribución, cardinalidad, cobertura temporal o calidad muestran que otra representación es más informativa y legible.

# Supuestos y riesgos

- La documentación establece que una fila es una línea de factura; por ello, cualquier métrica de factura, cliente o producto requerirá una agregación explícita y no podrá confundirse con la unidad original.
- `InvoiceNo`, `StockCode` y `CustomerID` son identificadores nominales aunque algunos valores se presenten como numéricos; deberán preservarse como categorías estables.
- El prefijo `C` de `InvoiceNo` se utilizará únicamente como criterio documentado para identificar cancelaciones. No presupone por sí solo el mecanismo completo de devolución, compensación o reversión contable.
- Las ausencias inicialmente observables en `Description` y `CustomerID` requieren cuantificación, análisis de patrones y tratamiento por objetivo. Excluirlas de toda la copia preparada sin justificación podría sesgar el análisis de líneas.
- `Quantity` y `UnitPrice` pueden contener valores no positivos o extremos cuyo significado no puede decidirse solo por su rareza estadística. La conservación, filtrado o segmentación deberá ser explícita y justificada.
- La multiplicación `Quantity × UnitPrice` será una variable derivada útil para descripción de líneas, pero no deberá presentarse sin matices como resultado financiero auditado o ingreso neto.
- La consistencia uno-a-uno entre código, descripción, cliente, país o factura no está garantizada por la documentación y deberá evaluarse empíricamente antes de imponerse como regla.
- Los meses inicial y final del rango publicado pueden estar incompletos; las comparaciones temporales deberán señalarlo si la inspección lo confirma.
- Las comparaciones entre países, artículos y clientes pueden estar dominadas por segmentos grandes, clientes mayoristas, líneas sin cliente identificado o valores extremos; se requerirán denominadores y poblaciones claramente declarados.
- El análisis será descriptivo y asociativo. No se realizarán modelos predictivos ni inferencias causales.

# Criterios de finalización

- El archivo original se habrá leído sin modificación y se habrá documentado la hoja, estructura, unidad de análisis y documentación pública utilizada.
- Existirá `prepared_data.csv` legible, separado del original, con encabezados únicos, tipos y fechas serializados de forma inequívoca, y transformaciones o decisiones de conservación registradas.
- `statistics.json` será válido, contendrá las dimensiones original y preparada coherentes, el perfil de todas las columnas finales, cambios `TR-NNN`, análisis `STAT-NNN` de E1 a E7 pertinentes, figuras registradas y limitaciones explícitas.
- Las estadísticas incluirán calidad cuantificada, descripción de variables y poblaciones relevantes, además de varias agregaciones o relaciones justificadas entre tiempo, país, artículos, importes, cantidades, precios, cancelaciones o clientes identificados según permitan los datos.
- `issues.json` documentará comprobaciones realizadas y todas las incidencias sustentadas, con decisiones, efectos potenciales, incertidumbre y referencias trazables.
- Existirá al menos una figura PNG válida y legible en `figures/`; cada figura estará registrada, vinculada a estadísticas y explicada en el informe.
- `report.md` cubrirá las ocho secciones obligatorias, citará resultados y figuras mediante identificadores existentes, distinguirá hechos de interpretaciones y expondrá limitaciones sin afirmaciones causales.
- Las dimensiones, identificadores, rutas relativas y referencias internas serán consistentes entre los resultados, y la traza automática permitirá reconstruir las operaciones realizadas.