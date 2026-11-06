# Identificación

- **run_id:** `D2_online_retail__langgraph__r01__20260902T170409927746Z`
- **framework_id:** `langgraph`
- **dataset_id:** `D2_online_retail`
- **contract_version:** `1.0`
- **prompt_version:** `1.0`
- **Entrada prevista:** archivo XLSX, hoja seleccionada `Online Retail`.
- **Documentación consultada:** `Readme.md`, que describe transacciones de comercio electrónico de una empresa británica durante el periodo indicado por la fuente pública.

# Comprensión inicial

Según la documentación pública, la unidad de observación es una **línea de factura**: una fila registra un artículo o concepto facturado y no representa necesariamente una compra, una factura completa ni un cliente único.

Las variables documentadas son `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID` y `Country`. `InvoiceNo`, `StockCode` y `CustomerID` deben tratarse inicialmente como identificadores nominales, no como medidas numéricas. La documentación indica que un `InvoiceNo` que comienza por `C` corresponde a una cancelación.

La inspección estructural común muestra que la hoja contiene estas ocho columnas y que `InvoiceDate` se ha reconocido inicialmente como fecha-hora, mientras que algunos identificadores pueden presentarse con tipos mixtos o numéricos. El Analista deberá confirmar los tipos tras la carga reproducible, la cobertura temporal efectiva, las reglas observadas para cancelaciones y la naturaleza de códigos o conceptos no convencionales.

El alcance se limitará a análisis exploratorio descriptivo de líneas de factura, facturas agregadas, artículos, clientes identificables, países y periodos temporales. No se entrenarán modelos ni se realizarán inferencias causales.

# Preguntas analíticas

1. ¿Cuál es la estructura efectiva del archivo, qué tipo y cardinalidad tienen sus variables y qué parte de la información requiere tratamiento para análisis?
2. ¿Qué proporción de líneas carece de `Description` o `CustomerID`, y cómo condicionan esas ausencias los análisis por producto y cliente?
3. ¿Existen filas duplicadas exactas, facturas repetidas esperables por ser líneas, o combinaciones potencialmente repetidas que requieran interpretación?
4. ¿Cómo se distribuyen `Quantity`, `UnitPrice` y el importe de línea derivado, considerando signos, ceros, valores extremos y posibles cancelaciones?
5. ¿Qué cobertura temporal tienen las transacciones y cómo evolucionan los recuentos, unidades y valores monetarios agregados a lo largo del tiempo?
6. ¿Cómo difieren descriptivamente los patrones entre ventas no canceladas y cancelaciones, si la regla documentada para `InvoiceNo` puede aplicarse?
7. ¿Qué países, artículos o descripciones concentran mayor actividad o valor agregado, y cómo debe tratarse su posible alta cardinalidad?
8. Entre los registros con `CustomerID`, ¿qué patrones descriptivos aparecen al agregar por cliente, sin interpretar el identificador como una escala?
9. ¿La identidad derivada `Quantity × UnitPrice` permite construir un importe de línea coherente y cuáles son sus límites interpretativos?
10. ¿Qué problemas de calidad, decisiones de preparación y limitaciones pueden modificar la lectura de los resultados?

# Plan por etapas

## E1

**Objetivo:** cargar el archivo XLSX sin modificarlo y documentar una comprensión inicial verificable de la tabla y de su unidad de análisis.

**Comprobaciones:**
- Leer la hoja `Online Retail` y registrar ruta relativa de entrada, formato, nombres de columnas y dimensiones.
- Contrastar los campos cargados con el diccionario público.
- Examinar una muestra estructural de inicio, final y filas variadas, sin usarla para generalizar resultados.
- Confirmar que cada fila corresponde a una línea de factura y distinguir esta unidad de las posibles agregaciones por `InvoiceNo`, `CustomerID`, artículo o fecha.

**Variables o grupos:** todas las variables fuente; especialmente `InvoiceNo`, `StockCode`, `InvoiceDate` y `CustomerID` para delimitar niveles de análisis.

**Evidencia esperada:** perfil inicial reproducible en `statistics.json`, con dimensiones, columnas, tipos observados, unidad de análisis y referencia a la documentación; copia original preservada.

**Supuestos o dependencias:** se parte de que la hoja seleccionada es la fuente analítica indicada. La interpretación de una factura completa dependerá de que los valores de `InvoiceNo` puedan agruparse de forma consistente.

## E2

**Objetivo:** caracterizar estructura, tipos y calidad de datos antes de decidir cualquier tratamiento.

**Comprobaciones:**
- Comparar tipos observados con los tipos semánticos esperados: identificadores nominales, fecha-hora, cantidades y precios.
- Cuantificar ausencias por columna y evaluar su patrón respecto de `InvoiceNo`, `Country`, fecha, estado de cancelación y otras variables pertinentes.
- Revisar duplicados exactos de fila y distinguirlos de líneas con una misma factura, artículo o cliente que puedan ser legítimas.
- Calcular cardinalidades de categorías y examinar espacios, mayúsculas/minúsculas, representaciones mixtas y posibles códigos especiales en `StockCode`, `Description` y `Country`.
- Verificar cobertura de `InvoiceDate`, orden temporal, fechas inválidas, huecos aparentes y posible incompletitud de periodos iniciales o finales.
- Describir rangos, signos, ceros y cuantiles de `Quantity` y `UnitPrice`.
- Comprobar la presencia y frecuencia de `InvoiceNo` con prefijo `C`, conforme a la definición publicada.
- Identificar valores extremos y posibles incoherencias sin clasificarlos automáticamente como errores.

**Variables o grupos:** `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID`, `Country`; grupos de cancelación potencial, mes, país y disponibilidad de `CustomerID`.

**Evidencia esperada:** análisis estructurados `STAT-NNN` de tipos, ausencias, duplicados, cardinalidad, temporalidad y rangos, junto con comprobaciones `CHK-NNN` e incidencias respaldadas en `issues.json`.

**Supuestos o dependencias:** el prefijo `C` solo se utilizará como indicador de cancelación después de verificar su representación textual. La documentación no establece umbrales para definir errores o extremos.

## E3

**Objetivo:** crear una copia preparada, separada del original, adecuada para análisis y completamente trazable.

**Comprobaciones:**
- Normalizar tipos analíticos sin alterar el significado de identificadores: conservar `InvoiceNo`, `StockCode` y `CustomerID` como categorías o cadenas cuando corresponda.
- Serializar `InvoiceDate` de forma ISO 8601 no ambigua en `prepared_data.csv`.
- Evaluar si las variaciones de formato de `StockCode`, `Description` o `Country` requieren normalización explícita y reversible.
- Decidir y documentar el tratamiento de ausencias de `Description` y `CustomerID`; evitar imputar identificadores o descripciones sin evidencia.
- Decidir el tratamiento de duplicados con base en su naturaleza, conservando los que puedan representar líneas transaccionales legítimas.
- Conservar valores negativos, ceros o extremos salvo evidencia suficiente para excluirlos; documentar filtros analíticos específicos por separado de la copia general.
- Crear, si procede, variables derivadas útiles y transparentes, como `line_amount_gbp = Quantity * UnitPrice`, indicador de cancelación basado en `InvoiceNo`, y componentes temporales derivados de `InvoiceDate`.
- Comparar dimensiones y ausencias antes y después de la preparación.

**Variables o grupos:** todas las columnas originales; posibles derivadas `line_amount_gbp`, indicador de cancelación y periodos temporales.

**Evidencia esperada:** `prepared_data.csv`, perfil de columnas finales, resumen antes-después y cambios `TR-NNN` con justificación, filas afectadas y decisiones de conservación en `statistics.json`.

**Supuestos o dependencias:** `line_amount_gbp` será un importe aritmético de línea en GBP y no debe asumirse como ingreso neto sin evaluar cancelaciones, conceptos especiales, precios nulos o reglas contables no documentadas.

## E4

**Objetivo:** obtener estadísticas descriptivas pertinentes para líneas, facturas y agregados, indicando siempre la población analizada.

**Comprobaciones:**
- Calcular conteos de líneas, facturas únicas, artículos/códigos, clientes identificables y países, según la copia preparada.
- Resumir `Quantity`, `UnitPrice` y, si se crea, `line_amount_gbp` con medidas de posición, dispersión, cuantiles, mínimos y máximos.
- Separar, cuando sea pertinente, la población total de líneas, ventas no canceladas y cancelaciones potenciales.
- Elaborar frecuencias de `Country`, estado de cancelación, códigos o descripciones, con estrategias explícitas para alta cardinalidad.
- Calcular estadísticas por grupos relevantes, como país, mes y estado de cancelación, evitando resultados no interpretables por tamaños muy pequeños.
- Para clientes con identificador disponible, describir agregados por cliente —por ejemplo, número de facturas, líneas, unidades o importe— aclarando el filtro de cobertura.

**Variables o grupos:** `Quantity`, `UnitPrice`, `line_amount_gbp` si procede, `Country`, periodos temporales, estado de cancelación, `CustomerID`, `StockCode` y `Description`.

**Evidencia esperada:** resultados `STAT-NNN` estructurados con población, método y tablas o resúmenes reproducibles; interpretación prudente de asimetrías y concentraciones.

**Supuestos o dependencias:** las medidas monetarias se expresarán en GBP según la documentación. Los resúmenes por cliente excluirán o identificarán explícitamente las filas sin `CustomerID`.

## E5

**Objetivo:** estudiar relaciones y patrones mediante agregaciones justificadas, sin tratar asociaciones como causalidad.

**Comprobaciones:**
- Agregar líneas por periodo temporal apropiado —por ejemplo, mes y, si aporta contexto, día de semana u hora— para describir actividad, unidades e importe de línea.
- Comparar patrones temporales entre ventas no canceladas y cancelaciones potenciales, si ambas poblaciones son analizables.
- Examinar la relación descriptiva entre `Quantity`, `UnitPrice` y `line_amount_gbp`, teniendo presente que este último se deriva de las dos primeras.
- Analizar distribuciones y agregados por `Country`, diferenciando líneas, facturas, unidades e importe cuando sea pertinente.
- Identificar artículos o descripciones con mayor frecuencia, volumen o importe agregado, aplicando filtros transparentes para conceptos no comparables, datos ausentes o alta cardinalidad.
- Examinar concentración descriptiva por cliente únicamente entre registros identificados, indicando que la ausencia de `CustomerID` limita cualquier comparación.
- Verificar identidades y redundancias: consistencia de la derivación monetaria, correspondencia potencial entre `StockCode` y `Description`, y comportamiento de `InvoiceNo` dentro de cada factura.

**Variables o grupos:** componentes de `InvoiceDate`, `InvoiceNo`, indicador de cancelación, `Quantity`, `UnitPrice`, `line_amount_gbp`, `Country`, `StockCode`, `Description` y `CustomerID`.

**Evidencia esperada:** varios `STAT-NNN` de agregaciones temporales, geográficas, por artículo y por cliente, además de comprobaciones de relaciones e identidades con interpretaciones descriptivas.

**Supuestos o dependencias:** cualquier relación entre precio, cantidad, país, producto o periodo se presentará como patrón observado. La posible mezcla de clientes minoristas y mayoristas no podrá clasificarse si no existe una variable que lo identifique.

## E6

**Objetivo:** generar figuras legibles que respondan a preguntas analíticas concretas y estén vinculadas a resultados estructurados.

**Comprobaciones:**
- Seleccionar escalas, agregaciones y categorías que permitan representar distribuciones sesgadas y alta cardinalidad sin ocultar sus limitaciones.
- Etiquetar títulos, ejes, unidades GBP, leyendas y periodos temporales cuando corresponda.
- Verificar que cada PNG sea legible, no vacío, tenga ruta relativa y esté registrado como `FIG-NNN`.
- Evitar gráficos de identificadores sin agregación significativa y evitar comparar poblaciones con filtros no declarados.

**Variables o grupos:** periodos derivados de `InvoiceDate`, `line_amount_gbp` si procede, `Quantity`, `UnitPrice`, `Country`, `StockCode` o `Description`, y estado de cancelación.

**Evidencia esperada:** archivos PNG en `figures/` y metadatos de figuras en `statistics.json`, cada uno enlazado a uno o más `STAT-NNN`; referencias posteriores en el informe.

**Supuestos o dependencias:** la selección final dependerá de los patrones observados y de la calidad de las variables. Se documentará cualquier transformación de escala, truncamiento visual o selección de categorías.

## E7

**Objetivo:** consolidar riesgos, anomalías y limitaciones detectados, separando evidencia, incertidumbre y decisión analítica.

**Comprobaciones:**
- Registrar resultados de todas las comprobaciones de calidad, incluso cuando no se detecte una incidencia.
- Documentar ausencias, duplicados, problemas de tipo, categorías inconsistentes, rangos inusuales, riesgos temporales e identidades no verificadas.
- Distinguir explícitamente entre cancelaciones documentadas, valores extremos plausibles, valores sospechosos y errores confirmados.
- Incluir muestras limitadas de posiciones de fila solo si ayudan a trazabilidad y si pueden identificarse de forma segura.
- Especificar para cada incidencia la acción aplicada o recomendada, el efecto potencial sobre los resultados y el grado de incertidumbre.

**Variables o grupos:** todas las columnas, con énfasis en `InvoiceNo`, `Description`, `CustomerID`, `Quantity`, `UnitPrice`, `InvoiceDate` y las derivadas.

**Evidencia esperada:** `issues.json` con `checks_performed` no vacío, incidencias `ISSUE-NNN` sustentadas por referencias `STAT-NNN`, y decisiones coherentes con la preparación.

**Supuestos o dependencias:** no se introducirá una incidencia solo para completar el registro. Si no puede determinarse si un valor es erróneo, se conservará esa incertidumbre.

## E8

**Objetivo:** elaborar un informe final trazable, comprensible y prudente que integre los resultados de las etapas anteriores.

**Comprobaciones:**
- Explicar dataset, fuente documental, unidad de análisis, periodo observado tras verificarlo y alcance no causal.
- Resumir calidad, preparación y población de cada análisis relevante.
- Presentar estadísticas, agregaciones y figuras con referencias válidas a `STAT-NNN`, `ISSUE-NNN` y `FIG-NNN`.
- Distinguir datos observados, interpretación descriptiva y explicaciones no verificadas.
- Incluir limitaciones relacionadas con líneas frente a facturas, cancelaciones, faltantes de identificadores, cobertura temporal y reglas de negocio no documentadas.
- Verificar coherencia entre el informe, `prepared_data.csv`, `statistics.json`, `issues.json` y las figuras.

**Variables o grupos:** todos los resultados seleccionados como relevantes tras E1–E7.

**Evidencia esperada:** `report.md` con las secciones obligatorias, referencias internas resolubles y conclusiones ajustadas a la evidencia disponible.

**Supuestos o dependencias:** el informe dependerá de que las salidas estructuradas y figuras se hayan validado. No se presentarán explicaciones de comportamiento comercial como hechos si el dataset no las permite comprobar.

# Visualizaciones previstas

- **Evolución temporal agregada:** representar por un periodo apropiado la actividad de líneas, facturas, unidades y/o importe de línea en GBP. Objetivo: describir cambios temporales y evaluar visualmente si los límites del periodo requieren cautela. Variables: `InvoiceDate`, `InvoiceNo`, `Quantity`, `line_amount_gbp` si procede.
- **Distribución de cantidades y/o precios:** mostrar distribuciones de `Quantity`, `UnitPrice` o importe de línea mediante una representación robusta ante asimetría y extremos. Objetivo: comunicar concentración, dispersión, signos y colas sin confundir extremos con errores. Variables: `Quantity`, `UnitPrice`, `line_amount_gbp`.
- **Actividad por país:** comparar los países con mayor actividad agregada, usando una selección transparente de categorías y una métrica claramente definida. Objetivo: describir concentración geográfica. Variables: `Country`, `InvoiceNo`, `Quantity` y/o `line_amount_gbp`.
- **Artículos o descripciones principales:** visualizar los productos o conceptos más relevantes según frecuencia, unidades o importe agregado, solo si la consistencia entre `StockCode` y `Description` permite una interpretación razonable. Objetivo: resumir concentración de catálogo sin representar toda la alta cardinalidad. Variables: `StockCode`, `Description`, `Quantity`, `line_amount_gbp`.
- **Ventas y cancelaciones potenciales:** si se confirma el indicador documentado, comparar su peso o evolución con una visualización basada en agregados. Objetivo: contextualizar la coexistencia de líneas de distinta naturaleza transaccional. Variables: `InvoiceNo`, indicador de cancelación, `InvoiceDate`, `Quantity`, `line_amount_gbp`.

La elección definitiva, el número de figuras y la forma gráfica se ajustarán a los resultados de calidad y a la legibilidad; cada figura deberá responder a una pregunta y enlazarse con estadísticas reproducibles.

# Supuestos y riesgos

- `InvoiceNo` puede repetirse de forma legítima porque el archivo contiene líneas de factura; el Analista deberá evitar tratar esta repetición como duplicado automáticamente.
- La regla publicada para valores de `InvoiceNo` que comienzan por `C` debe verificarse sobre la representación cargada antes de crear un indicador de cancelación.
- `CustomerID` es un identificador nominal y su disponibilidad puede ser incompleta; los análisis por cliente podrían no representar todas las líneas.
- `StockCode` puede incluir códigos alfanuméricos, numéricos o conceptos no equivalentes a productos convencionales. Cualquier conversión a número sería potencialmente destructiva y deberá evitarse salvo justificación.
- `Description` puede no identificar unívocamente un `StockCode`, contener diferencias de formato o estar ausente. La consistencia deberá evaluarse antes de agregar por descripción.
- Cantidades negativas, precios cero, importes negativos o valores muy altos pueden ser compatibles con cancelaciones, ajustes o reglas comerciales no documentadas; no deben eliminarse por defecto.
- La multiplicación `Quantity × UnitPrice` proporciona un importe de línea aritmético, pero no acredita impuestos, descuentos, devoluciones netas, costes ni reconocimiento contable de ingresos.
- El intervalo temporal publicado tiene posibles bordes parciales; las comparaciones entre periodos deben considerar cobertura efectiva y no asumir estacionalidad completa.
- Los resultados por país, artículo o cliente pueden estar fuertemente concentrados; deberán mostrarse tamaños de población y no extrapolarse a entidades ausentes.
- La documentación disponible define campos, pero no especifica reglas de negocio completas ni valores esperados; la clasificación de anomalías conservará incertidumbre cuando corresponda.

# Criterios de finalización

- Se habrá cargado el XLSX original sin sobrescribirlo y se habrá documentado la hoja utilizada, dimensiones, columnas y unidad de análisis.
- `prepared_data.csv` existirá como copia de trabajo legible, con encabezados, fechas no ambiguas y transformaciones o decisiones de conservación justificadas.
- `statistics.json` cumplirá el esquema requerido, reflejará las dimensiones original y preparada, perfilará todas las columnas finales y contendrá análisis reproducibles de E1 a E7.
- La preparación incluirá cambios `TR-NNN` trazables, con comparación antes-después y explicación de filtros o poblaciones analíticas.
- Se habrán realizado comprobaciones cuantificadas de ausencias, duplicados, tipos, categorías, rangos, temporalidad, cancelaciones potenciales y valores extremos cuando sean evaluables.
- `issues.json` incluirá comprobaciones `CHK-NNN` y solo incidencias `ISSUE-NNN` apoyadas por evidencia, decisión, acción, posible efecto e incertidumbre.
- Se habrán producido estadísticas descriptivas y varias agregaciones o relaciones pertinentes entre tiempo, transacciones, países, artículos, clientes identificables y variables monetarias o de cantidad, según permita la calidad observada.
- Existirá al menos una figura PNG legible y pertinente; todas las figuras estarán registradas en `statistics.json` con rutas relativas y referencias a resultados.
- `report.md` contendrá todas las secciones requeridas, citará resultados y figuras mediante identificadores válidos, no incluirá afirmaciones causales y declarará limitaciones.
- Las referencias entre archivos, identificadores, dimensiones y rutas se habrán comprobado para asegurar trazabilidad y coherencia antes del cierre.