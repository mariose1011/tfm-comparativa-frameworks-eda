# Identificación

- `run_id`: `D2_online_retail__crewai__r01__20260902T171610603875Z`
- `framework_id`: `crewai`
- `dataset_id`: `D2_online_retail`
- `contract_version`: `1.0`
- `prompt_version`: `1.0`

# Comprensión inicial

El archivo de entrada es un libro `xlsx` cuya hoja seleccionada es `Online Retail`. La inspección inicial común indica ocho columnas: `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID` y `Country`.

Según la documentación pública, cada fila representa una línea de factura, no necesariamente una factura completa ni una compra completa. El alcance temporal documentado cubre transacciones entre el 1 de diciembre de 2010 y el 9 de diciembre de 2011 de una empresa británica de comercio electrónico; parte de los clientes pueden ser mayoristas.

La documentación define `InvoiceNo`, `StockCode` y `CustomerID` como identificadores nominales. También indica que un `InvoiceNo` que comienza por `C` corresponde a una cancelación. El análisis deberá verificar cómo se materializan estos campos en la carga, si existen registros de cancelación y cómo tratarlos según el objetivo analítico, sin asumir que todo valor negativo o atípico constituye un error.

Quedan por comprobar la coherencia de tipos observados con los tipos analíticos, la presencia y patrón de ausencias, duplicados, rangos, consistencia de categorías, cobertura temporal efectiva y la relación entre líneas, facturas, clientes y artículos.

# Preguntas analíticas

1. ¿Cuál es la estructura efectiva de las líneas de factura y qué proporción corresponde a facturas, artículos, clientes y países distintos?
2. ¿Qué ausencias, duplicados, conversiones de tipo, valores no positivos o inconsistencias categóricas condicionan el análisis?
3. ¿Cómo se distribuyen `Quantity`, `UnitPrice` y el importe de línea derivado, distinguiendo adecuadamente ventas, cancelaciones y otros posibles conceptos?
4. ¿Cómo evolucionan los volúmenes de líneas, cantidades e importes por periodos temporales comparables dentro de la cobertura observada?
5. ¿Qué países, artículos o descripciones concentran la actividad, y cómo cambia esa concentración al usar métricas de líneas, cantidad o importe?
6. ¿Qué diferencias descriptivas se observan entre transacciones con y sin `CustomerID` disponible?
7. ¿Qué asociación descriptiva existe entre cantidad, precio unitario e importe de línea, y qué identidades aritméticas pueden comprobarse?
8. ¿Qué anomalías o riesgos deben advertirse para interpretar los agregados sin atribuir causalidad?

# Plan por etapas

## E1

**Objetivo**

Cargar el archivo `xlsx` sin modificarlo y confirmar la estructura básica de la hoja de trabajo.

**Comprobaciones**

- Verificar la lectura de la hoja `Online Retail`, dimensiones, encabezados, tipos cargados y una muestra de registros de distintas posiciones.
- Contrastar los campos cargados con el diccionario público.
- Registrar que la unidad de análisis es una línea de factura conforme a la documentación, distinguiéndola de una factura agregada o de un cliente.
- Confirmar la disponibilidad de las fechas y la ventana temporal observada.

**Variables o grupos**

`InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID` y `Country`; registros iniciales, finales y de muestra.

**Evidencia esperada**

Perfil original en `statistics.json` con dimensiones, columnas, tipos iniciales, ausencias y cardinalidades pertinentes; una entrada analítica de inspección inicial y trazabilidad de la carga.

**Supuestos o dependencias**

Se parte de que la hoja seleccionada contiene la tabla documentada. La semántica de cada fila proviene de la documentación pública y deberá conservarse en las salidas.

## E2

**Objetivo**

Caracterizar calidad, tipos, cobertura y riesgos analíticos antes de decidir cualquier modificación.

**Comprobaciones**

- Evaluar tipos reales frente a los tipos esperables: identificadores como nominales, fecha-hora para `InvoiceDate`, numéricos para `Quantity` y `UnitPrice`.
- Cuantificar ausencias por columna y explorar si se concentran por periodo, país, tipo de factura o cualquier grupo pertinente.
- Medir duplicados de fila completa y revisar repeticiones de combinaciones que podrían ser líneas repetidas, sin equiparar automáticamente repetición a error.
- Examinar cardinalidad, espacios, mayúsculas/minúsculas y correspondencias potencialmente múltiples entre `StockCode` y `Description`.
- Revisar valores negativos, cero y extremos de `Quantity` y `UnitPrice`; contrastarlos con cancelaciones identificables por `InvoiceNo` y con posibles conceptos no convencionales.
- Verificar el patrón temporal, mínimos y máximos, frecuencia de observación, huecos y parcialidad potencial de los extremos del periodo.
- Revisar categorías de `Country` y la plausibilidad estructural de identificadores sin inferir atributos no documentados.

**Variables o grupos**

Todas las variables; grupos por prefijo o estado derivado de `InvoiceNo`, periodos calendarios, `Country`, presencia de `CustomerID` y, si procede, combinaciones `StockCode`–`Description`.

**Evidencia esperada**

Resultados `STAT-NNN` de calidad cuantificada, comprobaciones `CHK-NNN` en `issues.json` y una lista estructurada de incidencias o riesgos respaldados por evidencia.

**Supuestos o dependencias**

La documentación solo confirma que el prefijo `C` señala cancelación; no proporciona reglas para otros formatos de código, precios, cantidades o descripciones. Cualquier criterio adicional deberá declararse como operativo y prudente.

## E3

**Objetivo**

Crear una copia de trabajo trazable, apta para EDA, preservando el archivo original y evitando exclusiones automáticas.

**Comprobaciones**

- Convertir de forma controlada `InvoiceDate` a una serialización ISO 8601 y preservar los identificadores como valores nominales, incluidos posibles ceros iniciales o sufijos.
- Crear una variable derivada de importe de línea, definida explícitamente como `Quantity × UnitPrice`, tras verificar que ambas variables sean interpretables.
- Crear, si resulta útil y verificable, indicadores de cancelación según el prefijo documentado y de presencia de `CustomerID`; crear periodos temporales derivados para agregaciones.
- Definir el tratamiento de ausencias de `Description` y `CustomerID`, distinguiendo entre conservar líneas para totales transaccionales y restringir análisis que requieran identificación de cliente o artículo.
- Decidir con evidencia si se conservan, anotan o excluyen duplicados exactos, líneas de cancelación, precios/cantidades no positivos y extremos; documentar la población de cada cálculo posterior.
- Comparar dimensiones, columnas y recuentos antes y después de la preparación.

**Variables o grupos**

Campos originales y, si se justifican, `LineAmount`, indicador de cancelación, indicador de `CustomerID` presente y variables de calendario.

**Evidencia esperada**

`prepared_data.csv` separado del original, perfil final de columnas y cambios `TR-NNN` en `statistics.json`, con comparativa antes-después y justificación de cada decisión.

**Supuestos o dependencias**

La creación de `LineAmount` representa un cálculo contable de línea, no una confirmación de ingreso neto. Si se retienen cancelaciones, deberán distinguirse explícitamente en agregados e interpretaciones.

## E4

**Objetivo**

Describir las variables principales mediante estadísticas apropiadas para líneas de factura y poblaciones analíticas declaradas.

**Comprobaciones**

- Obtener conteos de líneas, facturas, artículos, descripciones, clientes identificados y países, sin interpretar identificadores como magnitudes.
- Resumir `Quantity`, `UnitPrice` y, si procede, `LineAmount` mediante medidas robustas y de dispersión, cuantiles, mínimos y máximos.
- Calcular frecuencias y proporciones de cancelaciones, líneas con `CustomerID` ausente y otros estados definidos durante la preparación.
- Producir resúmenes por grupos relevantes: `Country`, periodo, estado de cancelación y disponibilidad de `CustomerID`.
- Separar, cuando sea pertinente, poblaciones de todas las líneas, líneas no canceladas y análisis basados exclusivamente en clientes identificados.

**Variables o grupos**

`Quantity`, `UnitPrice`, `LineAmount` si se deriva, `Country`, periodos, indicador de cancelación, `CustomerID` presente/ausente, `InvoiceNo` y `StockCode`.

**Evidencia esperada**

Entradas `STAT-NNN` reproducibles con definición de población, método, medidas y tablas agregadas pertinentes en `statistics.json`.

**Supuestos o dependencias**

La elevada asimetría o presencia de valores extremos puede hacer más informativos los cuantiles que la media por sí sola. La selección de medidas deberá responder a la distribución observada.

## E5

**Objetivo**

Analizar relaciones y agregaciones relevantes sin convertir asociaciones descriptivas en explicaciones causales.

**Comprobaciones**

- Agregar actividad por mes u otra unidad temporal apropiada, diferenciando conteos de líneas, facturas, cantidades e importe de línea según las poblaciones definidas.
- Comparar contribuciones de países mediante métricas coherentes y tratar la alta cardinalidad mediante selección explícita de categorías principales y agrupación transparente del resto si resulta necesaria.
- Identificar artículos o descripciones predominantes usando medidas separadas de frecuencia, cantidad e importe, comprobando previamente la consistencia entre `StockCode` y `Description`.
- Describir la relación entre `Quantity`, `UnitPrice` y `LineAmount`; comprobar la identidad de cálculo de la variable derivada y evitar correlaciones engañosas por signos, ceros o extremos.
- Comparar descriptivamente transacciones con y sin `CustomerID`, indicando que la ausencia impide atribución individual y puede alterar los análisis por cliente.
- Si los datos lo permiten, construir agregados a nivel de factura o cliente identificado para caracterizar distribución de líneas, cantidades o importes, manteniendo clara la diferencia con la unidad original.

**Variables o grupos**

Periodos derivados de `InvoiceDate`, `Country`, `StockCode`, `Description`, `InvoiceNo`, `CustomerID`, `Quantity`, `UnitPrice`, `LineAmount` e indicador de cancelación.

**Evidencia esperada**

Múltiples resultados `STAT-NNN` de agregación temporal, segmentación geográfica o de producto, comprobaciones de identidad y relaciones descriptivas, todos con población y método declarados.

**Supuestos o dependencias**

Las facturas pueden contener varias líneas y los clientes pueden no estar identificados. No se asumirá que `Description` identifica de forma unívoca un producto ni que un importe positivo equivale necesariamente a ingreso realizado.

## E6

**Objetivo**

Generar figuras legibles que respondan a preguntas analíticas concretas y estén respaldadas por resultados estructurados.

**Comprobaciones**

- Elegir escalas, agregaciones y filtros coherentes con distribuciones potencialmente sesgadas y con cancelaciones o importes negativos si existen.
- Incluir títulos, ejes, unidades, periodos, leyendas y notas de población cuando sean necesarias.
- Verificar que cada PNG sea legible, no vacío, tenga un nombre conforme al contrato y esté registrado como `FIG-NNN`.

**Variables o grupos**

Series temporales, `Country`, `StockCode` o `Description`, `Quantity`, `UnitPrice`, `LineAmount` e indicadores derivados que resulten validados.

**Evidencia esperada**

Archivos PNG en `figures/` y entradas vinculadas en `statistics.json`, cada una con objetivo, variables y referencias a los análisis que la sustentan.

**Supuestos o dependencias**

Las visualizaciones definitivas dependerán de la calidad y distribución observadas en E2–E5. No se generarán gráficos de categorías de alta cardinalidad sin una regla de selección o agregación claramente expuesta.

## E7

**Objetivo**

Consolidar problemas, anomalías y riesgos que afecten la interpretación o reproducibilidad del EDA.

**Comprobaciones**

- Registrar de forma estructurada hallazgos sobre ausencias, duplicados, tipos, categorías, rangos, identidades, cobertura temporal y extremos.
- Distinguir cancelaciones documentadas, valores extremos plausibles, posibles errores y casos cuya naturaleza no pueda determinarse.
- Asociar cada incidencia con evidencia, columnas o filas afectadas cuando sea posible, decisión aplicada o recomendada y efecto potencial.
- Incorporar también comprobaciones que no revelen una incidencia, para mostrar cobertura de control de calidad.

**Variables o grupos**

Todas las variables, con atención a `InvoiceNo`, `Description`, `CustomerID`, `Quantity`, `UnitPrice`, `InvoiceDate`, `StockCode` y `Country`.

**Evidencia esperada**

`issues.json` válido con `checks_performed` no vacío, incidencias `ISSUE-NNN` respaldadas por resultados `STAT-NNN` y decisiones consistentes con la copia preparada.

**Supuestos o dependencias**

La falta de reglas externas sobre valores esperados impide clasificar definitivamente algunos registros. La incertidumbre deberá documentarse en vez de convertir sospechas en errores confirmados.

## E8

**Objetivo**

Integrar el EDA en un informe final reproducible, prudente y trazable a estadísticas, figuras e incidencias.

**Comprobaciones**

- Explicar fuente documental disponible, alcance temporal, unidad de análisis y diferencia entre líneas y facturas.
- Resumir inspección, calidad, preparación y poblaciones empleadas en los cálculos.
- Presentar estadísticas, agregaciones, relaciones y figuras con referencias internas `STAT-NNN`, `FIG-NNN` e `ISSUE-NNN`.
- Distinguir datos observados, interpretación descriptiva y explicaciones no verificadas; no formular afirmaciones causales.
- Indicar limitaciones de cobertura, identificación de clientes, tratamiento de cancelaciones, valores no convencionales y demás incertidumbres validadas.

**Variables o grupos**

Resultados y decisiones de E1–E7; variables centrales `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID`, `Country` y derivadas justificadas.

**Evidencia esperada**

`report.md` con las nueve secciones requeridas, conclusiones trazables y referencias resueltas a `statistics.json`, `issues.json` y `figures/`.

**Supuestos o dependencias**

El informe dependerá de que las salidas estructuradas y figuras hayan superado comprobaciones de coherencia. No deberá incorporar información no contenida en el dataset o la documentación pública proporcionada.

# Visualizaciones previstas

- **Evolución temporal de actividad:** representar por mes los conteos de líneas o facturas y, cuando sea apropiado, cantidades e importe de línea. El objetivo es describir variación temporal y advertir posibles periodos parciales; variables: `InvoiceDate`, `InvoiceNo`, `Quantity`, `LineAmount` e indicador de cancelación si se deriva.
- **Distribución de métricas de línea:** mostrar la distribución de `Quantity`, `UnitPrice` o `LineAmount` con una escala o recorte visual explícitamente justificado que permita observar la masa principal sin ocultar extremos. El objetivo es evaluar asimetría y magnitud de valores inusuales.
- **Concentración por `Country`:** comparar las categorías principales mediante una métrica claramente indicada, como importe, cantidad o líneas. El objetivo es describir concentración geográfica sin presentar los países como causas.
- **Artículos o descripciones principales:** visualizar una selección transparente de `StockCode` o `Description` por frecuencia, cantidad o importe. El objetivo es contrastar que las clasificaciones pueden cambiar según la métrica y exponer la alta cardinalidad.
- **Relación entre precio, cantidad e importe:** usar una representación adecuada a la densidad y a posibles signos no positivos para explorar la asociación descriptiva entre `Quantity`, `UnitPrice` y `LineAmount`. El objetivo es complementar la comprobación de identidad y detectar patrones que requieran cautela.

La selección final dependerá de los resultados de calidad y de la legibilidad conseguida; cada figura deberá responder a una de estas preguntas y vincularse con análisis estructurados.

# Supuestos y riesgos

- `InvoiceNo`, `StockCode` y `CustomerID` son identificadores nominales; no deben tratarse como variables numéricas continuas aunque su representación cargada parezca numérica.
- El prefijo `C` en `InvoiceNo` está documentado como cancelación, pero deberán verificarse su presencia, sus signos, su peso y el tratamiento adecuado para cada población analítica.
- `CustomerID` puede estar ausente; los análisis por cliente deberán limitarse a registros identificados o declarar otro tratamiento explícito, sin imputar identificadores.
- `Description` puede estar ausente o no corresponder uno a uno con `StockCode`; cualquier agregación de producto deberá comprobar esta consistencia y declarar la clave utilizada.
- Cantidades o precios negativos, ceros y valores extremos pueden corresponder a cancelaciones, ajustes, servicios u otros registros válidos. No se eliminarán solo por ser inusuales.
- La cobertura documentada empieza y termina dentro de meses calendario; los agregados temporales de los extremos podrían no ser comparables con meses completos y deberán identificarse.
- El importe `Quantity × UnitPrice`, si se crea, es una variable derivada de línea y no permite por sí sola confirmar pagos, rentabilidad, devoluciones consolidadas ni causalidad.
- Los resultados describirán el archivo disponible y no deben generalizarse más allá de su periodo, empresa, población de clientes o calidad de identificación observada.
- La documentación pública disponible define variables, pero no proporciona valores de referencia, taxonomías de artículos ni reglas de validación adicionales; esas limitaciones deberán mantenerse visibles.

# Criterios de finalización

- `plan.md` conserva este plan y cubre explícitamente E1–E8.
- El archivo original permanece sin cambios y existe `prepared_data.csv` legible, con encabezados, dimensiones conciliadas y transformaciones justificadas.
- `statistics.json` es JSON válido, contiene el perfil original y preparado, cambios `TR-NNN`, análisis `STAT-NNN`, limitaciones y registro de todas las figuras.
- Las estadísticas incluyen evidencia de carga, estructura, calidad, preparación, descripción, agregaciones y relaciones para poblaciones claramente definidas.
- `issues.json` es válido, contiene comprobaciones de calidad realizadas e incidencias respaldadas o una lista vacía justificada si no se detectan problemas.
- Existe al menos una figura PNG legible y todas las figuras registradas tienen rutas relativas, identificadores `FIG-NNN` y vínculos a análisis existentes.
- `report.md` incluye las secciones obligatorias, cita resultados y figuras mediante identificadores válidos, diferencia descripción de causalidad y declara limitaciones.
- Las dimensiones, identificadores, referencias internas, rutas y nombres de archivo son coherentes entre todas las salidas obligatorias y la traza automática.