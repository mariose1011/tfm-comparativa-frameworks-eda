# Identificación

- **run_id:** `D2_online_retail__crewai__r02__20260902T193106552358Z`
- **framework_id:** `crewai`
- **dataset_id:** `D2_online_retail`
- **contract_version:** `1.0`
- **prompt_version:** `1.0`

# Comprensión inicial

El archivo de entrada es un libro `xlsx`, con la hoja seleccionada `Online Retail`. La inspección inicial común indica ocho columnas: `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID` y `Country`.

Según la documentación pública, cada fila representa una línea de factura, no una factura completa ni necesariamente una compra completa. El alcance publicado comprende transacciones de una empresa británica de comercio electrónico, entre el 1 de diciembre de 2010 y el 9 de diciembre de 2011. `InvoiceNo` es un identificador nominal y las referencias que comienzan por `C` deben comprobarse como posibles cancelaciones, conforme a la documentación.

La inspección inicial muestra que los identificadores y códigos pueden estar representados con tipos mixtos o aparentemente numéricos pese a ser nominales; el Analista deberá preservar su semántica de identificador al preparar los datos. También deberá verificar la presencia, naturaleza y repercusión analítica de valores ausentes observables en `Description` y `CustomerID`, sin asumir que constituyen errores ni imputarlos automáticamente.

# Preguntas analíticas

1. ¿Cuál es la cobertura temporal efectiva de las líneas registradas y existen meses o periodos parciales que condicionen comparaciones temporales?
2. ¿Qué calidad presentan los tipos, valores ausentes, duplicados, categorías y rangos de las variables documentadas?
3. ¿Qué proporción de líneas e importes corresponde a transacciones regulares, cancelaciones identificables y otras operaciones que requieran interpretación cautelosa?
4. ¿Cómo se distribuyen `Quantity`, `UnitPrice` y el importe de línea derivado, considerando signos, ceros y valores extremos?
5. ¿Cómo evolucionan el número de líneas, facturas y el importe neto o bruto bajo una definición documentada a lo largo del tiempo?
6. ¿Cómo se distribuye la actividad por `Country`, distinguiendo entre número de líneas, facturas, clientes identificados e importe cuando resulte aplicable?
7. ¿Qué artículos o descripciones concentran mayor actividad o importe, evitando tratar `StockCode` o `Description` como medidas numéricas?
8. ¿Qué diferencias descriptivas se observan entre líneas con `CustomerID` disponible y no disponible?
9. ¿Existen inconsistencias entre `StockCode` y `Description`, o entre el estado inferible de `InvoiceNo` y signos de `Quantity` o importes, que deban registrarse como riesgo?
10. ¿Qué hallazgos son robustos a decisiones razonables de preparación y cuáles dependen de filtros, agregaciones o definiciones operativas?

# Plan por etapas

## E1

**Objetivo:** Cargar el archivo `xlsx` sin modificarlo, confirmar su estructura y documentar el alcance de la unidad de análisis.

**Comprobaciones:**
- Leer la hoja `Online Retail` y verificar que la carga reproduce la tabla esperada.
- Registrar dimensiones, nombres y orden de las columnas, tipos observados y una muestra estructural de inicio, final y/o posiciones diversas.
- Confrontar nombres y significado de variables con el diccionario público.
- Confirmar que la unidad de análisis es una línea de factura y aclarar que una misma `InvoiceNo` puede abarcar múltiples líneas.
- Registrar la huella o identificación disponible del archivo fuente en la trazabilidad, si la herramienta la proporciona.

**Variables o grupos:** Todas las columnas; en especial `InvoiceNo` como identificador de factura, `StockCode` como código nominal, `CustomerID` como identificador nominal e `InvoiceDate` como fecha y hora.

**Evidencia esperada:** Perfil inicial estructurado en `statistics.json` con dimensiones originales, lista de columnas, tipos observados y descripción de la unidad de análisis; registro de carga y documentación consultada en la traza.

**Supuestos o dependencias:** Se parte de que la hoja seleccionada por la inspección común es la hoja analítica pertinente. Si durante la carga aparecen diferencias de encabezados, hojas o tipos, deberán documentarse en lugar de corregirse silenciosamente.

## E2

**Objetivo:** Caracterizar la estructura, tipos y calidad de los datos originales antes de decidir transformaciones.

**Comprobaciones:**
- Cuantificar ausencias por columna y revisar patrones de coausencia relevantes, especialmente para `Description` y `CustomerID`.
- Comprobar duplicados exactos de filas y distinguirlos de líneas repetidas que puedan ser transacciones legítimas.
- Examinar cardinalidad, normalización visible y valores especiales de `InvoiceNo`, `StockCode`, `Description` y `Country`.
- Verificar que `InvoiceDate` pueda interpretarse como fecha-hora y obtener fechas mínima, máxima, continuidad temporal y cobertura por mes.
- Revisar rangos, signos, ceros, cuantiles y extremos de `Quantity` y `UnitPrice`.
- Identificar referencias de `InvoiceNo` que comienzan por `C` y examinar su coherencia descriptiva con signos de cantidad e importe de línea.
- Evaluar la consistencia de correspondencias `StockCode`–`Description`, sin presuponer una relación estrictamente uno a uno.
- Comprobar si `CustomerID`, aunque se haya leído como numérico, requiere tratamiento nominal para evitar interpretaciones cuantitativas erróneas.

**Variables o grupos:** `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID`, `Country`; subconjuntos de cancelaciones y de observaciones con/sin `CustomerID`.

**Evidencia esperada:** Análisis estructurados `STAT-NNN` de ausencias, duplicados, tipos, categorías, rango temporal, rangos numéricos, cancelaciones y consistencia; comprobaciones `CHK-NNN` e incidencias respaldadas en `issues.json`.

**Supuestos o dependencias:** Los valores negativos, ceros, precios inusuales o categorías poco frecuentes no se clasificarán automáticamente como errores. La documentación no define reglas completas para conceptos no estándar ni para todas las combinaciones de signos, por lo que se mantendrá incertidumbre cuando corresponda.

## E3

**Objetivo:** Crear una copia preparada, separada del original, adecuada para análisis descriptivo y con transformaciones trazables.

**Comprobaciones:**
- Crear `prepared_data.csv` sin sobrescribir el archivo de origen.
- Estandarizar representaciones de tipos cuando sea necesario: preservar `InvoiceNo`, `StockCode` y `CustomerID` como identificadores nominales; serializar `InvoiceDate` inequívocamente; conservar valores numéricos de `Quantity` y `UnitPrice`.
- Decidir y documentar explícitamente el tratamiento de espacios visibles, valores ausentes, filas duplicadas, identificadores y descripciones no disponibles.
- Conservar o excluir filas únicamente bajo criterios reproducibles y justificados; comparar dimensiones y ausencias antes y después.
- Derivar, si es útil y reproducible, variables tales como `line_amount` = `Quantity` × `UnitPrice`, un indicador de cancelación basado en `InvoiceNo`, y componentes temporales para agregación. Las derivaciones deberán conservar las columnas fuente.
- Separar conceptualmente las poblaciones de análisis cuando sea pertinente, por ejemplo, todas las líneas retenidas, líneas no canceladas y líneas con cliente identificado, sin ocultar la población usada en cada cálculo.

**Variables o grupos:** Todas las variables fuente; posibles derivadas `line_amount`, indicador de cancelación y campos temporales derivados de `InvoiceDate`.

**Evidencia esperada:** `prepared_data.csv` legible; perfil de columnas finales; resumen antes-después; registro `TR-NNN` de cada transformación, conservación deliberada, filtro o derivación en `statistics.json`.

**Supuestos o dependencias:** El importe de línea derivado presupone que `Quantity` y `UnitPrice` son multiplicables según su definición publicada. La interpretación económica de valores negativos, nulos o de operaciones con códigos especiales deberá mantenerse cautelosa y reflejarse en los filtros analíticos, no eliminarse indiscriminadamente.

## E4

**Objetivo:** Generar estadísticas descriptivas reproducibles de las variables relevantes y de las poblaciones analíticas definidas.

**Comprobaciones:**
- Calcular conteos de líneas, facturas distintas, clientes identificados, artículos o códigos y países para poblaciones claramente especificadas.
- Resumir `Quantity`, `UnitPrice` y `line_amount` mediante medidas apropiadas de posición, dispersión, cuantiles, mínimos y máximos, atendiendo a distribuciones posiblemente asimétricas.
- Obtener frecuencias y participaciones para categorías principales, incluyendo `Country` y, si es interpretable, los artículos o códigos más frecuentes.
- Describir la cobertura y distribución temporal mediante agregaciones coherentes con el rango observado.
- Comparar descriptivamente poblaciones relevantes, como transacciones identificables como cancelaciones frente a otras, o líneas con y sin `CustomerID`, evitando extrapolaciones a clientes no identificados.

**Variables o grupos:** `Quantity`, `UnitPrice`, `line_amount`, `InvoiceNo`, `CustomerID`, `StockCode`, `Description`, `Country`, `InvoiceDate`; grupos por estado de cancelación, disponibilidad de `CustomerID`, país y periodo.

**Evidencia esperada:** Resultados `STAT-NNN` estructurados con población, método, unidades y resultados numéricos; tablas compactas de frecuencias, cuantiles y estadísticas por grupos en `statistics.json`.

**Supuestos o dependencias:** Las sumas de importes solo se interpretarán bajo la definición de población indicada. Las estadísticas de `CustomerID` estarán limitadas a registros donde el identificador esté disponible y no se presentarán como cobertura completa de la clientela.

## E5

**Objetivo:** Examinar agregaciones y relaciones descriptivas pertinentes entre fecha, artículos, geografía, cantidades, precios e importes.

**Comprobaciones:**
- Agregar actividad por periodos temporales adecuados, utilizando conteos de líneas, facturas y una suma de importe con definición explícita.
- Comparar `Country` mediante métricas de volumen, número de facturas, clientes identificados e importe, utilizando tablas ordenadas y evitando conclusiones basadas solo en identificadores.
- Examinar concentración de actividad por `StockCode` y/o `Description`, comprobando si los artículos más frecuentes difieren de los de mayor importe.
- Analizar la relación descriptiva entre `Quantity`, `UnitPrice` y `line_amount`, reconociendo la identidad matemática de la variable derivada y evitando presentar esa identidad como descubrimiento independiente.
- Comparar patrones temporales o geográficos entre líneas regulares y cancelaciones cuando la clasificación basada en `InvoiceNo` sea suficientemente verificable.
- Evaluar la asociación entre ausencia de `CustomerID` y otras características observables, como país, importe o tipos de transacción, sin atribuir causas a la ausencia.

**Variables o grupos:** Componentes temporales de `InvoiceDate`, `Country`, `StockCode`, `Description`, `Quantity`, `UnitPrice`, `line_amount`, indicador de cancelación y disponibilidad de `CustomerID`.

**Evidencia esperada:** Varios resultados `STAT-NNN` de agregaciones temporales, comparación geográfica, concentración de artículos, asociaciones descriptivas y validaciones de identidad; interpretaciones prudentes trazables a los resultados.

**Supuestos o dependencias:** Las diferencias entre grupos son descriptivas y pueden depender de cobertura, composición de facturas, clientes sin identificar y periodos incompletos. No se inferirá causalidad ni rentabilidad empresarial a partir de importes de línea.

## E6

**Objetivo:** Crear visualizaciones legibles que respondan a preguntas analíticas y estén respaldadas por análisis estructurados.

**Comprobaciones:**
- Seleccionar escalas y agregaciones que muestren tendencias sin que extremos o categorías de alta cardinalidad oculten el patrón.
- Etiquetar títulos, ejes, unidades monetarias cuando corresponda, leyendas y notas de población o filtros necesarios.
- Verificar que cada PNG sea legible, no vacío, tenga ruta relativa y figure con un identificador `FIG-NNN` en `statistics.json`.
- Explicar en el informe la pregunta que responde cada figura y sus límites de interpretación.

**Variables o grupos:** Agregaciones temporales de `InvoiceDate`; `Country`; `Quantity`, `UnitPrice` y `line_amount`; estado de cancelación; `StockCode` o `Description` agregados.

**Evidencia esperada:** Directorio `figures/` con figuras PNG válidas y registro de cada una con objetivo, variables y `STAT-NNN` de respaldo.

**Supuestos o dependencias:** La forma exacta de los gráficos se decidirá tras conocer distribuciones, cardinalidades y periodos efectivos. Si un gráfico previsto no es legible o aporta poca información, podrá sustituirse por otra representación justificada y documentada.

## E7

**Objetivo:** Consolidar problemas, riesgos, anomalías y limitaciones que puedan afectar la interpretación o reproducibilidad.

**Comprobaciones:**
- Registrar todas las comprobaciones realizadas, incluso las que no detecten incidencias.
- Distinguir entre ausencias, duplicados, inconsistencias de tipo o categoría, riesgos de rango, periodos temporales parciales, valores extremos y señales de operaciones especiales.
- Documentar evidencia, columnas afectadas, conteos o muestras de posiciones cuando sean pertinentes, decisión tomada y efecto potencial.
- Diferenciar incidencias resueltas mediante una transformación de riesgos retenidos intencionadamente o no resueltos por falta de información.
- Revisar que ningún valor extremo se etiquete como error sin evidencia adicional y que los filtros empleados en análisis estén explícitos.

**Variables o grupos:** Todas las variables; énfasis en `Description`, `CustomerID`, `InvoiceNo`, `Quantity`, `UnitPrice`, `InvoiceDate`, `StockCode` y `Country`.

**Evidencia esperada:** `issues.json` válido con `checks_performed` no vacío, referencias a análisis `STAT-NNN`, e incidencias `ISSUE-NNN` solo cuando estén respaldadas por evidencia.

**Supuestos o dependencias:** La documentación no aporta valores de referencia ni reglas exhaustivas de validación. Por ello, ciertos casos podrán quedar como sospechas o riesgos de interpretación, no como errores confirmados.

## E8

**Objetivo:** Integrar el EDA en un informe final verificable, prudente y coherente con las salidas generadas.

**Comprobaciones:**
- Redactar `report.md` con las secciones obligatorias y referencias cercanas a estadísticas, incidencias y figuras.
- Explicar dataset, unidad de observación, cobertura, preparación y poblaciones analíticas.
- Presentar hallazgos descriptivos relevantes con cifras, tablas o figuras de respaldo.
- Separar hechos observados de interpretaciones y explicaciones posibles.
- Incluir limitaciones de ausencia de clientes, cancelaciones, conceptos especiales, posibles periodos parciales, alta concentración o asimetría y cualquier otro riesgo confirmado.
- Verificar coherencia de identificadores, rutas relativas, dimensiones y referencias internas entre todos los artefactos.

**Variables o grupos:** Todos los resultados consolidados de las etapas anteriores.

**Evidencia esperada:** `report.md` con las nueve secciones requeridas, referencias existentes `[STAT-NNN]`, `[ISSUE-NNN]` y `[FIG-NNN]`, y conclusiones circunscritas al análisis descriptivo.

**Supuestos o dependencias:** El informe dependerá de las decisiones finales de preparación y de las evidencias efectivamente obtenidas. Cualquier desviación justificada respecto de este plan deberá quedar registrada en los artefactos estructurados o en la trazabilidad.

# Visualizaciones previstas

- **Evolución temporal de la actividad:** representar por mes o por otra granularidad justificada el número de líneas, facturas y/o importe bajo una población claramente definida. Objetivo: identificar la evolución descriptiva, estacionalidad visible y posibles efectos de cobertura parcial. Variables: `InvoiceDate`, `InvoiceNo`, `line_amount`, indicador de cancelación si se aplica.

- **Distribución de importes o de variables numéricas:** utilizar una representación adecuada para distribuciones asimétricas y valores extremos, potencialmente con escalas, cuantiles o paneles complementarios. Objetivo: mostrar la concentración y dispersión de `Quantity`, `UnitPrice` o `line_amount` sin ocultar valores relevantes. Variables: `Quantity`, `UnitPrice`, `line_amount`.

- **Comparación por países:** representar los países con mayor actividad mediante una métrica explícita y un tratamiento legible de la alta concentración potencial. Objetivo: comparar descriptivamente volumen, facturas o importe por `Country`. Variables: `Country`, `InvoiceNo`, `line_amount`, `CustomerID` cuando proceda.

- **Concentración por artículo o descripción:** visualizar una selección justificada de artículos principales por frecuencia y/o importe, sin intentar representar todas las categorías. Objetivo: contrastar la concentración de la actividad y diferenciar métricas de volumen e importe. Variables: `StockCode`, `Description`, `Quantity`, `line_amount`.

- **Relación entre cantidad, precio e importe:** utilizar una visualización agregada o con tratamiento de densidad/sobreposición si el volumen de líneas lo requiere. Objetivo: describir patrones y extremos observados entre `Quantity`, `UnitPrice` y `line_amount`, dejando explícita la identidad matemática cuando intervenga el importe derivado. Variables: `Quantity`, `UnitPrice`, `line_amount`, indicador de cancelación.

- **Comparación de poblaciones de transacción:** si las comprobaciones confirman que es interpretable, representar diferencias entre líneas con `InvoiceNo` de cancelación y otras, o entre registros con y sin `CustomerID`. Objetivo: hacer visible el alcance de estas poblaciones y sus diferencias descriptivas. Variables: `InvoiceNo`, indicador de cancelación, `CustomerID`, `Quantity`, `line_amount`.

# Supuestos y riesgos

- La documentación establece que una fila es una línea de factura; no debe interpretarse cada fila como cliente único, pedido completo o compra independiente.
- `InvoiceNo`, `StockCode` y `CustomerID` son identificadores nominales, aunque su lectura técnica pueda sugerir formatos numéricos o mixtos.
- El prefijo `C` de `InvoiceNo` se documenta como cancelación, pero el Analista deberá comprobar cómo se manifiesta en los valores y no asumir reglas no publicadas para otros prefijos o códigos.
- `Quantity` y `UnitPrice` permiten derivar un importe de línea para fines descriptivos, pero dicho importe no incorpora información externa sobre impuestos, descuentos, envíos, divisas, márgenes ni rentabilidad.
- Los valores ausentes de `CustomerID` pueden limitar agregaciones por cliente y sesgar comparaciones basadas solo en clientes identificados; no deberán imputarse sin fundamento.
- Las ausencias de `Description` pueden estar asociadas a códigos o conceptos especiales; deberán preservarse o tratarse según evidencia, no reemplazarse por una categoría inventada.
- Las líneas exactamente duplicadas podrían ser registros legítimos de transacciones repetidas. La decisión de deduplicar exigirá evidencia y comparación antes-después.
- Cantidades negativas, precios nulos o extremos pueden corresponder a cancelaciones, ajustes, conceptos especiales o errores. Su clasificación deberá permanecer incierta cuando la evidencia disponible no permita resolverla.
- La cobertura temporal publicada comienza y termina en fechas concretas; los meses de borde u otros intervalos incompletos deberán identificarse antes de comparar totales temporales.
- La alta cardinalidad de `StockCode`, `Description`, `InvoiceNo` y `CustomerID` exige agregación o selección documentada para tablas y gráficos legibles.
- Todas las asociaciones serán descriptivas. El EDA no entrenará modelos predictivos, no establecerá causalidad y no utilizará información externa al archivo y la documentación pública proporcionada.

# Criterios de finalización

- Se habrá cargado el archivo original `xlsx` y se habrá documentado su hoja, estructura, variables y unidad de observación conforme a la documentación pública.
- `prepared_data.csv` existirá como copia de trabajo UTF-8 separada del original, con dimensiones y columnas reconciliables con `statistics.json`.
- `statistics.json` será JSON válido, incluirá el perfil original y preparado, transformaciones `TR-NNN`, análisis `STAT-NNN`, figuras `FIG-NNN` y limitaciones.
- Las etapas E1 a E7 tendrán evidencias analíticas reproducibles, con poblaciones, filtros, unidades y métodos explícitos cuando correspondan.
- `issues.json` incluirá comprobaciones de calidad documentadas y, cuando proceda, incidencias sustentadas con evidencia, decisiones y efectos potenciales.
- Las figuras generadas serán PNG válidos, legibles, con rutas relativas, títulos y etiquetas adecuadas, y estarán vinculadas a análisis estructurados.
- `report.md` incluirá todas las secciones obligatorias, resumirá hallazgos respaldados y referenciará identificadores existentes de estadísticas, problemas y figuras.
- Se habrán distinguido datos retenidos, datos excluidos y transformaciones aplicadas; cualquier exclusión estará justificada y cuantificada.
- Las conclusiones se limitarán a descripciones y asociaciones observadas, con limitaciones e incertidumbres explícitas.
- Todos los artefactos obligatorios serán coherentes entre sí, utilizarán los identificadores de esta ejecución y respetarán las rutas y nombres exigidos por el contrato.