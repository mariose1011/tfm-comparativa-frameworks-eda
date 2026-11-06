# Identificación

- **run_id:** `D2_online_retail__crewai__r03__20260902T212422402094Z`
- **framework_id:** `crewai`
- **dataset_id:** `D2_online_retail`
- **contract_version:** `1.0`
- **prompt_version:** `1.0`

# Comprensión inicial

El archivo de entrada tiene formato `xlsx` y la hoja seleccionada es `Online Retail`. La inspección inicial común indica ocho columnas: `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID` y `Country`.

Según la documentación pública, cada fila representa una **línea de factura**, no necesariamente una factura completa ni una compra completa. El alcance temporal documentado comprende transacciones de una empresa británica de comercio electrónico entre el 1 de diciembre de 2010 y el 9 de diciembre de 2011. `InvoiceNo` es un identificador nominal y los valores que comienzan por `C` representan cancelaciones según la documentación.

La inspección común muestra tipos inicialmente heterogéneos en identificadores y campos de texto, una fecha ya interpretada como fecha-hora y valores ausentes en `Description` y `CustomerID`. Estos elementos deberán verificarse de forma completa antes de adoptar decisiones de preparación.

Aspectos aún inciertos que deberán comprobarse:

- Si los tipos observados de `InvoiceNo` y `StockCode` preservan adecuadamente su naturaleza nominal, incluidos posibles ceros iniciales, sufijos o códigos no asociados a productos.
- Si una línea con cantidad, precio o importe negativo corresponde de forma sistemática a una cancelación, devolución, ajuste u otro concepto.
- Si los valores nulos de `CustomerID` o `Description` están asociados a segmentos, fechas, países, tipos de factura o códigos concretos.
- Si hay líneas idénticas que sean duplicados técnicos o repeticiones comerciales legítimas.
- Si los extremos de `Quantity`, `UnitPrice` o del importe derivado son transacciones válidas, correcciones o posibles errores.
- Si el periodo de inicio y fin contiene meses o días parciales que deban contextualizarse en comparaciones temporales.

# Preguntas analíticas

1. ¿Cuál es la cobertura temporal efectiva del archivo y cómo se distribuyen las líneas, facturas y el valor facturado a lo largo del tiempo?
2. ¿Qué proporción de líneas corresponde a facturas identificadas como cancelaciones y cómo difieren sus cantidades, precios e importes de las demás líneas?
3. ¿Cuál es la magnitud y el patrón de las ausencias en `CustomerID` y `Description`?
4. ¿Cómo se distribuyen `Quantity`, `UnitPrice` y el importe de línea derivado, tanto en el conjunto como tras distinguir operaciones no canceladas y cancelaciones?
5. ¿Qué productos o conceptos, países y clientes identificados concentran más líneas, unidades o importe neto, usando agregaciones adecuadas sin interpretar identificadores como variables numéricas?
6. ¿Existen diferencias descriptivas relevantes entre países o periodos temporales en número de líneas, facturas, unidades e importe?
7. ¿Qué relación descriptiva existe entre `Quantity`, `UnitPrice` e importe de línea, y qué papel tienen valores extremos o importes nulos?
8. ¿Qué incidencias de tipo, rango, consistencia, duplicación o cobertura temporal pueden afectar la interpretación de los resultados?

# Plan por etapas

## E1

**Objetivo:** confirmar la carga del archivo original sin alterarlo y establecer la estructura, unidad de análisis y alcance del EDA.

**Comprobaciones:** verificar el archivo `xlsx`, la hoja utilizada, dimensiones, nombres y orden de columnas, muestra de registros de distintas posiciones y tipos inicialmente inferidos. Contrastar la unidad de análisis con la documentación pública y registrar que una fila es una línea de factura.

**Variables o grupos:** todas las columnas; atención inicial a `InvoiceNo`, `StockCode`, `InvoiceDate`, `Quantity`, `UnitPrice`, `CustomerID` y `Country`.

**Evidencia esperada:** perfil del original en `statistics.json`, incluidos dimensiones, columnas, tipos observados, ausencias y unidad de análisis; registro trazable de la fuente documental utilizada.

**Supuestos o dependencias:** se parte de que la hoja `Online Retail` es la tabla analítica principal. El Analista deberá comprobar que no existan encabezados desplazados, filas auxiliares o conversiones de lectura que distorsionen identificadores nominales.

## E2

**Objetivo:** caracterizar la calidad, estructura y riesgos analíticos antes de preparar la copia de trabajo.

**Comprobaciones:** cuantificar ausencias por columna; evaluar filas exactamente duplicadas y posibles repeticiones dentro de combinaciones relevantes; revisar cardinalidades de campos nominales; verificar tipos esperados frente a tipos observados; inspeccionar signos, ceros, mínimos, máximos y cuantiles de `Quantity` y `UnitPrice`; comprobar la sintaxis y presencia de prefijos de cancelación en `InvoiceNo`; analizar consistencia entre `StockCode` y `Description`; revisar categorías de `Country`; y establecer cobertura temporal, frecuencia de fechas y posible incompletitud de los extremos del periodo.

**Variables o grupos:** `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID`, `Country`; subgrupos de facturas con y sin prefijo `C` si el formato lo permite.

**Evidencia esperada:** análisis estructurados `STAT-NNN` sobre tipos, ausencias, duplicados, categorías, rangos y cobertura temporal; comprobaciones registradas en `issues.json`; incidencias respaldadas por evidencia, sin clasificar automáticamente los extremos como errores.

**Supuestos o dependencias:** la documentación define `InvoiceNo`, `StockCode` y `CustomerID` como identificadores nominales. La interpretación de valores negativos, nulos o códigos especiales dependerá de los patrones observados, pues la documentación no ofrece reglas exhaustivas.

## E3

**Objetivo:** generar `prepared_data.csv` como copia separada y trazable, apropiada para el EDA y sin modificar el archivo original.

**Comprobaciones:** definir y documentar conversiones necesarias, especialmente la representación textual de identificadores nominales y la serialización no ambigua de `InvoiceDate`; decidir el tratamiento de ausencias, filas duplicadas, categorías inconsistentes, precios o cantidades no positivos y cancelaciones; comparar dimensiones y ausencias antes y después; y verificar que toda exclusión, conservación o variable derivada tenga justificación explícita.

**Variables o grupos:** todas las variables fuente; potenciales derivadas como un indicador de cancelación basado en `InvoiceNo`, una unidad temporal derivada de `InvoiceDate` y un importe de línea calculado como `Quantity × UnitPrice`, si su creación es consistente con los datos.

**Evidencia esperada:** `prepared_data.csv`; perfil de columnas finales; lista de cambios `TR-NNN` con criterio, columnas y filas afectadas; y comparación antes-después en `statistics.json`.

**Supuestos o dependencias:** se conservarán las columnas fuente necesarias para contextualizar las decisiones. La creación de un importe de línea presupone que `Quantity` y `UnitPrice` son valores numéricos interpretables en la misma línea; cualquier excepción identificada se documentará. La retención o exclusión de cancelaciones dependerá del objetivo de cada análisis y deberá hacerse explícita.

## E4

**Objetivo:** obtener un resumen descriptivo reproducible de las variables y poblaciones analíticamente relevantes.

**Comprobaciones:** calcular conteos de líneas, facturas distintas, productos o códigos, clientes identificados y países; resumir ausencias; describir `Quantity`, `UnitPrice` e importe de línea mediante medidas robustas y de dispersión adecuadas; calcular frecuencias de categorías relevantes; y comparar estadísticas entre operaciones no canceladas, cancelaciones y/o otras segmentaciones justificadas.

**Variables o grupos:** `Quantity`, `UnitPrice`, importe de línea si se deriva, `InvoiceNo`, `StockCode`, `CustomerID`, `Country`, `InvoiceDate`; grupos de cancelación y disponibilidad de `CustomerID`.

**Evidencia esperada:** resultados estructurados `STAT-NNN` con población definida, método y cifras descriptivas; tablas resumidas adecuadas para respaldar el informe.

**Supuestos o dependencias:** las métricas monetarias deberán indicar si reflejan valor bruto de líneas, valor neto con signos o una población filtrada. Las medias se complementarán con medidas robustas cuando las distribuciones sean asimétricas o presenten extremos.

## E5

**Objetivo:** analizar relaciones y patrones mediante agregaciones pertinentes, sin atribuir causalidad.

**Comprobaciones:** agregar líneas, unidades, facturas distintas e importe por periodo temporal; comparar resultados por `Country`; revisar concentración por `StockCode` o `Description` cuando la cardinalidad permita una presentación legible; analizar clientes identificados mediante agregaciones y no como variable numérica; examinar la relación descriptiva entre `Quantity`, `UnitPrice` e importe de línea; y comprobar la identidad aritmética de la variable derivada cuando se haya creado.

**Variables o grupos:** periodos derivados de `InvoiceDate`; `Country`; `StockCode` y `Description`; `CustomerID` no nulo; `Quantity`, `UnitPrice`, importe de línea; indicador de cancelación.

**Evidencia esperada:** varios `STAT-NNN` con agregaciones temporales, geográficas, por producto o concepto y por clientes identificados, con poblaciones y definiciones explícitas; interpretación descriptiva prudente de asociaciones y concentración.

**Supuestos o dependencias:** los resultados por cliente estarán limitados a filas con `CustomerID` disponible y no representarán necesariamente a toda la clientela. Las comparaciones territoriales deberán considerar la posible concentración en un país y los tamaños desiguales de grupo. Los identificadores no se tratarán como escalas numéricas.

## E6

**Objetivo:** generar figuras legibles que respondan a preguntas analíticas y estén vinculadas a resultados calculados.

**Comprobaciones:** seleccionar gráficos según distribución, agregación y cardinalidad; incorporar título, ejes, unidades, leyendas y periodos; decidir escalas o segmentaciones que muestren extremos sin ocultar la estructura principal; y registrar cada figura con su referencia a los análisis `STAT-NNN` que la respaldan.

**Variables o grupos:** series temporales derivadas de `InvoiceDate`; distribución de `Quantity`, `UnitPrice` e importe de línea; `Country`; productos o conceptos más relevantes; indicador de cancelación cuando sea pertinente.

**Evidencia esperada:** archivos PNG válidos en `figures/`, registros `FIG-NNN` en `statistics.json` y referencias explícitas a dichas figuras en `report.md`.

**Supuestos o dependencias:** las figuras finales dependerán de la calidad observada y de la dispersión efectiva. Si una representación de alta cardinalidad no resulta interpretable, se utilizarán agregaciones o subconjuntos justificados y se documentará el criterio.

## E7

**Objetivo:** consolidar de manera estructurada los problemas, anomalías, decisiones y riesgos que condicionan el EDA.

**Comprobaciones:** registrar resultados de controles sobre ausencias, duplicados, tipos, categorías, rangos, coherencia entre variables, fechas y extremos; distinguir un dato confirmado como inconsistente de un caso solo sospechoso o retenido; incluir muestras de posiciones de fila únicamente cuando sean necesarias y trazables; y describir efectos potenciales de cada incidencia sobre las métricas.

**Variables o grupos:** todas las columnas, con foco en `CustomerID`, `Description`, `InvoiceNo`, `StockCode`, `Quantity`, `UnitPrice`, `InvoiceDate` e importe derivado si existe.

**Evidencia esperada:** `issues.json` con comprobaciones `CHK-NNN` no vacías e incidencias `ISSUE-NNN` respaldadas por `STAT-NNN`, incluyendo decisión, acción, efecto potencial e incertidumbre.

**Supuestos o dependencias:** no se catalogará una observación extrema como error por su magnitud aislada. La ausencia de reglas de negocio completas limita la atribución definitiva de algunos casos a error, devolución, ajuste o actividad comercial válida.

## E8

**Objetivo:** integrar los resultados en un informe final verificable, comprensible y prudente.

**Comprobaciones:** redactar el alcance y unidad de análisis; resumir calidad y preparación; presentar estadística, agregaciones y relaciones principales; enlazar visualizaciones; diferenciar hechos observados de interpretaciones y explicaciones posibles; declarar limitaciones; y verificar que las referencias `STAT-NNN`, `ISSUE-NNN` y `FIG-NNN` existan y no contradigan las salidas estructuradas.

**Variables o grupos:** resultados consolidados de todas las variables y segmentaciones finalmente seleccionadas.

**Evidencia esperada:** `report.md` con las secciones obligatorias, referencias internas válidas y conclusiones descriptivas respaldadas por `statistics.json`, `issues.json` y las figuras.

**Supuestos o dependencias:** el informe no deberá extrapolar fuera del periodo, la empresa o las líneas observadas, ni establecer efectos causales. Toda diferencia entre poblaciones preparadas deberá explicarse cerca de la cifra correspondiente.

# Visualizaciones previstas

- **Evolución temporal de actividad y valor:** mostrar por periodos comparables el número de líneas, facturas distintas, unidades y/o importe de línea, según la población que se defina. Variables: `InvoiceDate`, `InvoiceNo`, `Quantity` e importe derivado. Permitirá examinar patrones temporales y contextualizar periodos extremos o parciales.
- **Distribución de cantidades, precios e importes:** representar la forma de las distribuciones y la presencia de valores negativos, nulos o extremos sin confundirlos automáticamente con errores. Variables: `Quantity`, `UnitPrice` e importe derivado. La escala, transformación o paneles se elegirán tras la inspección de rangos.
- **Comparación geográfica de la actividad:** comparar países mediante líneas, facturas, unidades o importe, limitando la visualización a categorías que puedan leerse e indicando el criterio de agrupación o selección. Variables: `Country`, `InvoiceNo`, `Quantity` e importe derivado.
- **Concentración por productos o conceptos:** representar los `StockCode` o `Description` con mayor contribución bajo una métrica definida, como unidades o importe. Variables: `StockCode`, `Description`, `Quantity` e importe derivado. Se tratará como una agregación de categorías nominales, no como una relación numérica.
- **Relación descriptiva entre cantidad y precio:** explorar visualmente la asociación entre `Quantity` y `UnitPrice`, con posible segmentación por tipo de operación o tratamiento adecuado de densidad y extremos. Variables: `Quantity`, `UnitPrice` e indicador de cancelación si se deriva. No se interpretará como causalidad.
- **Composición de cancelaciones frente a otras facturas:** si los patrones observados y el volumen lo justifican, comparar conteos o importes por estado de cancelación. Variables: `InvoiceNo`, `Quantity`, `UnitPrice` e importe derivado.

# Supuestos y riesgos

- La documentación pública identifica las filas como líneas de factura; por tanto, los recuentos de filas no equivalen automáticamente a compras, clientes o facturas.
- `InvoiceNo`, `StockCode` y `CustomerID` son identificadores nominales. Deberán preservarse como tales, aunque la lectura inicial pueda mostrar valores numéricos o mixtos.
- Las facturas cuyo `InvoiceNo` empieza por `C` se tratarán como cancelaciones conforme a la documentación; el Analista deberá definir con precisión si se incluyen en métricas netas, se describen por separado o se excluyen de análisis de ventas brutas.
- Los valores faltantes de `CustomerID` y `Description` requerirán cuantificación y análisis de patrón. No deben imputarse automáticamente, en particular un identificador de cliente.
- Una coincidencia exacta de filas no demuestra por sí sola un error, pues podría representar líneas comerciales repetidas. La decisión dependerá de la evidencia y deberá registrarse.
- Cantidades, precios o importes con signos inesperados, valor cero o gran magnitud pueden reflejar operaciones válidas, devoluciones, descuentos, ajustes o errores; su tratamiento requerirá evidencia contextual.
- `StockCode` puede incluir códigos para conceptos no equivalentes a artículos físicos. La consistencia con `Description` y los patrones de precio o cantidad deberán comprobarse antes de interpretar rankings de productos.
- La concentración por `Country`, producto o cliente puede ser alta y dificultar gráficos o comparaciones; se usarán agregaciones legibles y se documentarán los filtros de presentación.
- El periodo documentado puede incluir fracciones de mes al inicio o final, por lo que las comparaciones mensuales exigirán contextualización.
- El dataset describe transacciones de una única empresa y periodo. Sus patrones no permiten inferencias causales ni generalizaciones garantizadas a otros negocios o periodos.

# Criterios de finalización

El plan se considerará cubierto cuando el Analista haya dejado evidencia reproducible de lo siguiente:

1. Carga preservada del archivo original, identificación de la hoja, dimensiones, columnas, muestra estructural y unidad de análisis documentada.
2. Perfil de tipos, ausencias, duplicados, cardinalidades, rangos, signos, fechas, categorías y extremos, con controles registrados en `statistics.json` e `issues.json`.
3. Creación de `prepared_data.csv` como copia separada, con transformaciones o decisiones de conservación documentadas mediante `TR-NNN` y comparación antes-después.
4. Estadística descriptiva con poblaciones explícitas para las principales variables numéricas, nominales, temporales y de identificación de facturas.
5. Varias agregaciones o relaciones pertinentes —temporales y por grupos disponibles— con interpretación descriptiva respaldada por resultados `STAT-NNN`.
6. Figuras PNG válidas, legibles y registradas como `FIG-NNN`, cada una vinculada a una pregunta analítica y a análisis estructurados.
7. Registro de comprobaciones de calidad no vacío y de incidencias respaldadas, con decisión, acción o recomendación, efecto potencial e incertidumbre.
8. Informe `report.md` con las secciones obligatorias, referencias internas resolubles y conclusiones prudentes que no hagan afirmaciones causales.
9. Coherencia entre dimensiones, identificadores, rutas relativas, archivos obligatorios y cifras citadas en todas las salidas del contrato.