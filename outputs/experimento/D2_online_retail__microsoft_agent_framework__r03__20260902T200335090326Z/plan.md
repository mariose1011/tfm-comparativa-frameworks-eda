# Identificación

- `run_id`: `D2_online_retail__microsoft_agent_framework__r03__20260902T200335090326Z`
- `framework_id`: `microsoft_agent_framework`
- `dataset_id`: `D2_online_retail`
- `contract_version`: `1.0`
- `prompt_version`: `1.0`

# Comprensión inicial

El archivo de entrada es un libro `xlsx` cuya hoja seleccionada es `Online Retail`. La inspección inicial común indica una tabla de ocho columnas: `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID` y `Country`.

Según la documentación pública, cada fila representa una línea de factura, no necesariamente una factura completa ni una compra agregada. El alcance publicado comprende transacciones de una empresa británica de comercio electrónico entre el 1 de diciembre de 2010 y el 9 de diciembre de 2011; comercializa principalmente artículos de regalo y parte de sus clientes son mayoristas.

La inspección inicial muestra tipos heterogéneos para los identificadores y la presencia de ausencias en al menos `Description` y `CustomerID`. El Analista deberá verificar de forma completa la lectura de la hoja, los tipos efectivos, la cobertura temporal y la naturaleza de los registros especiales. En particular, deberá confirmar si los valores de `InvoiceNo` que comienzan por `C` son cancelaciones conforme a la documentación y cómo deben tratarse en cada población analítica.

# Preguntas analíticas

1. ¿Cuál es la estructura efectiva del archivo original, qué tipos y ausencias contiene, y en qué medida es coherente con el diccionario publicado?
2. ¿Qué proporción de líneas corresponde a facturas ordinarias y a posibles cancelaciones identificadas mediante `InvoiceNo`?
3. ¿Cómo se distribuyen `Quantity`, `UnitPrice` y el importe derivado por línea (`Quantity` × `UnitPrice`), considerando signos, ceros, asimetrías y valores extremos?
4. ¿Cómo varían las líneas, unidades, facturas y/o importe neto a lo largo del tiempo, y qué cautelas requiere la posible cobertura parcial de los meses extremos?
5. ¿Qué países, artículos o descripciones concentran la actividad bajo agregaciones apropiadas y sin interpretar los identificadores como variables métricas?
6. ¿Qué diferencias descriptivas se observan entre transacciones con `CustomerID` disponible y no disponible?
7. ¿Existen duplicados exactos, categorías aparentemente inconsistentes, combinaciones inusuales de cantidad y precio, o registros de servicio/no producto que deban documentarse?
8. ¿Qué hallazgos son robustos al distinguir la población completa de la población de ventas no canceladas, y cuáles dependen de decisiones de preparación?

# Plan por etapas

## E1

**Objetivo:** Cargar el libro sin modificarlo, confirmar la hoja de trabajo y establecer la unidad de observación y el alcance del EDA.

**Comprobaciones:** Verificar la lectura correcta del archivo `xlsx` y de la hoja `Online Retail`; registrar dimensiones, nombres y orden de columnas, tipos inicialmente inferidos y una muestra estructural de filas. Contrastar los nombres con la documentación pública y confirmar que cada registro se interpretará como línea de factura. Examinar la fecha mínima y máxima observada frente al período documentado, sin asumir que todos los intervalos están completos.

**Variables o grupos:** Todas las columnas; de manera específica `InvoiceNo` para identificar líneas de factura y `InvoiceDate` para el alcance temporal.

**Evidencia esperada:** Perfil reproducible del archivo original en `statistics.json`, incluyendo dimensiones, columnas, tipos observados, unidad de análisis y una descripción del alcance; trazabilidad de la consulta a la documentación y de la carga.

**Supuestos o dependencias:** Se parte de que la hoja seleccionada por la inspección común es la fuente analítica. Debe comprobarse que no existen filas de encabezado, notas u otras estructuras no tabulares incluidas en esa hoja.

## E2

**Objetivo:** Caracterizar estructura, tipos y calidad de los datos originales antes de decidir cualquier transformación.

**Comprobaciones:** Cuantificar ausencias por columna; comprobar duplicados exactos de filas y repeticiones esperables de `InvoiceNo`, `StockCode` y `CustomerID`; revisar cardinalidades y representación de categorías. Validar que `InvoiceDate` pueda usarse como fecha-hora, que `Quantity` y `UnitPrice` sean numéricos, y que `CustomerID` se trate como identificador nominal aunque se lea numéricamente. Examinar rangos, ceros y signos de `Quantity` y `UnitPrice`; detectar posibles facturas con prefijo `C`; evaluar concordancia entre signo de `Quantity`, precio, estado de cancelación y descripción cuando sea pertinente. Revisar consistencia entre `StockCode` y `Description`, así como variantes por espacios, capitalización u otras diferencias observables. Determinar cobertura por día o mes e identificar intervalos potencialmente incompletos. Examinar extremos con reglas descriptivas robustas, sin clasificarlos automáticamente como errores.

**Variables o grupos:** `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID`, `Country`; estratos de posible cancelación y de disponibilidad de `CustomerID`.

**Evidencia esperada:** Análisis estructurados `STAT-NNN` para calidad, tipos, ausencias, duplicados, categorías, fechas y rangos; comprobaciones `CHK-NNN` e incidencias sustentadas en `issues.json`.

**Supuestos o dependencias:** Las repeticiones de `InvoiceNo` son previsibles porque la unidad es una línea de factura; no deben considerarse duplicados por sí solas. La documentación solo define el prefijo `C` como señal de cancelación y no establece otras reglas de corrección.

## E3

**Objetivo:** Crear una copia de trabajo separada y trazable, adecuada para análisis descriptivo y que preserve información suficiente para interpretar devoluciones, cancelaciones y ausencias.

**Comprobaciones:** Definir y registrar conversiones de tipo necesarias, especialmente para `InvoiceDate`, identificadores nominales y serialización consistente de fechas. Decidir el tratamiento de duplicados exactos solo después de cuantificarlos y revisar si reflejan líneas repetidas legítimas. Conservar o excluir registros únicamente con una justificación explícita. Mantener las ausencias de `CustomerID` como ausencias, salvo que se defina una categoría analítica claramente documentada; no imputar identidades. Evaluar si las ausencias de `Description` afectan las agregaciones por producto. Crear, si resulta adecuado, un indicador de cancelación basado en `InvoiceNo`, un importe por línea definido como `Quantity` × `UnitPrice`, y componentes temporales para agregaciones. Distinguir una población preparada completa de subconjuntos analíticos, por ejemplo ventas no canceladas, sin ocultar las filas excluidas de análisis específicos.

**Variables o grupos:** Todas las columnas originales; posibles derivadas como importe de línea, indicador de cancelación, período mensual y disponibilidad de `CustomerID`.

**Evidencia esperada:** `prepared_data.csv` separado del original; perfil antes-después; lista de cambios `TR-NNN` con justificación, columnas y filas afectadas; declaración explícita de las poblaciones empleadas en resultados posteriores.

**Supuestos o dependencias:** El importe derivado es una identidad aritmética útil para describir valor facturado neto por línea, pero su interpretación económica debe depender del signo y del tratamiento de cancelaciones. Los valores extremos se conservarán inicialmente salvo evidencia concreta que justifique otra decisión.

## E4

**Objetivo:** Producir estadísticas descriptivas reproducibles de las variables y poblaciones principales.

**Comprobaciones:** Calcular conteos de líneas, facturas distintas, clientes identificados, productos/códigos y países según la población definida. Resumir `Quantity`, `UnitPrice` e importe de línea mediante medidas de tendencia central, dispersión, cuantiles, mínimos y máximos adecuadas a distribuciones potencialmente asimétricas. Cuantificar la disponibilidad de `CustomerID` y `Description`. Describir proporciones de posibles cancelaciones y, si procede, de precios o cantidades no positivos. Preparar estadísticas separadas para la población completa y para ventas no canceladas cuando ello evite mezclar fenómenos distintos.

**Variables o grupos:** `Quantity`, `UnitPrice`, importe derivado, indicador de cancelación, disponibilidad de `CustomerID`, `Country`, `InvoiceDate`, `StockCode` y `Description`.

**Evidencia esperada:** Resultados `STAT-NNN` estructurados con población, método, variables y resultados tabulares o escalares; tablas compactas aptas para ser citadas en el informe.

**Supuestos o dependencias:** Las estadísticas de identificadores se limitarán a recuentos de cardinalidad o frecuencia; no se aplicarán medidas numéricas interpretativas a `InvoiceNo`, `StockCode` ni `CustomerID`.

## E5

**Objetivo:** Analizar agregaciones y relaciones descriptivas relevantes para transacciones minoristas, distinguiendo asociaciones de explicaciones causales.

**Comprobaciones:** Agregar actividad por mes, y cuando sea útil por día de semana u hora, informando la unidad agregada y el posible efecto de meses parcialmente cubiertos. Comparar países por líneas, facturas, unidades e importe según una población explícita, tratando la alta cardinalidad de manera legible. Identificar productos o descripciones de mayor frecuencia o mayor importe bajo una regla transparente y verificando correspondencia con `StockCode`. Comparar perfiles descriptivos de líneas con y sin `CustomerID`. Examinar relaciones entre `Quantity`, `UnitPrice` e importe de línea mediante resúmenes, segmentación o asociación no causal adecuados a la distribución. Verificar la identidad del importe derivado y documentar los efectos de los signos negativos.

**Variables o grupos:** Períodos derivados de `InvoiceDate`; `Country`; `StockCode` y `Description`; `Quantity`; `UnitPrice`; importe derivado; estado de cancelación; disponibilidad de `CustomerID`.

**Evidencia esperada:** Varios `STAT-NNN` de agregación temporal, segmentación geográfica, concentración de artículos, comparación por disponibilidad de cliente y relación entre variables numéricas; interpretaciones explícitamente descriptivas.

**Supuestos o dependencias:** El país está asociado al cliente según la documentación, no se confirma que sea el destino de cada envío. Los rankings deberán limitarse a categorías interpretables y no extrapolarse a causalidad, rentabilidad ni comportamiento individual.

## E6

**Objetivo:** Crear visualizaciones legibles que respondan a preguntas analíticas concretas y estén vinculadas a estadísticas reproducibles.

**Comprobaciones:** Seleccionar figuras tras conocer las distribuciones y cardinalidades reales. Incluir títulos, ejes, unidades, leyendas y notas sobre población o tratamiento cuando sean necesarios. Revisar que las escalas y la agregación no oculten efectos de valores extremos, cancelaciones o períodos parciales. Guardar archivos PNG válidos en `figures/` y registrar cada uno con un identificador `FIG-NNN`.

**Variables o grupos:** Series temporales de actividad e importe; distribuciones de `Quantity`, `UnitPrice` e importe; países y artículos de frecuencia o valor relevante; posible estratificación por cancelación.

**Evidencia esperada:** Figuras PNG legibles, referencias en `statistics.json` a los `STAT-NNN` de respaldo y explicación de la pregunta que aborda cada figura.

**Supuestos o dependencias:** El tipo definitivo de gráfico dependerá de los resultados de E2–E5. Para variables muy sesgadas o categorías numerosas se aplicarán decisiones de visualización explícitas, como escalas adecuadas, filtros transparentes o paneles separados, sin eliminar la evidencia subyacente.

## E7

**Objetivo:** Consolidar problemas de calidad, riesgos analíticos y anomalías observadas, separando evidencia, incertidumbre y acción.

**Comprobaciones:** Registrar de forma estructurada ausencias, duplicados exactos, tipos ambiguos, inconsistencias de categorías, signos o precios inusuales, cancelaciones, cobertura temporal y valores extremos. Para cada situación, determinar filas o columnas afectadas cuando sea posible, cuantificar evidencia, valorar severidad respecto al análisis y especificar si se retiene, resuelve o recomienda una acción futura. Comprobar expresamente que los extremos comerciales o las devoluciones no se etiqueten como errores sin soporte adicional.

**Variables o grupos:** Todas las variables, con énfasis en `Description`, `CustomerID`, `InvoiceNo`, `Quantity`, `UnitPrice`, `InvoiceDate`, `StockCode` y `Country`.

**Evidencia esperada:** `issues.json` con comprobaciones `CHK-NNN` no vacías y entradas `ISSUE-NNN` sustentadas por `STAT-NNN`, incluyendo decisión, efecto potencial e incertidumbre.

**Supuestos o dependencias:** No se dispone de reglas externas de validación de precios, cantidades, catálogos de productos ni conciliación financiera. Las incidencias no resolubles deberán declararse como riesgos o sospechas, no como errores confirmados.

## E8

**Objetivo:** Integrar el EDA en un informe final verificable, prudente y coherente con las salidas estructuradas.

**Comprobaciones:** Redactar `report.md` con las secciones obligatorias: resumen ejecutivo, dataset y alcance, inspección/calidad/preparación, estadística descriptiva, variables/agregaciones/relaciones, visualizaciones/hallazgos, problemas/riesgos/anomalías, limitaciones/incertidumbres y conclusiones. Citar las cifras verificables mediante referencias `STAT-NNN`, los problemas mediante `ISSUE-NNN` y las figuras mediante `FIG-NNN`. Diferenciar observaciones calculadas de interpretaciones posibles y no realizar afirmaciones predictivas ni causales.

**Variables o grupos:** Los que queden justificados por los resultados de E1–E7.

**Evidencia esperada:** Informe final legible que enlace hallazgos, estadísticas, incidencias y figuras; lista explícita de limitaciones y de decisiones que puedan modificar resultados.

**Supuestos o dependencias:** El informe dependerá de que `prepared_data.csv`, `statistics.json`, `issues.json` y las figuras sean coherentes entre sí. Las conclusiones deberán limitarse a la tabla proporcionada y al período observado.

# Visualizaciones previstas

- **Evolución temporal de la actividad:** representar por período la cantidad de líneas, facturas y/o importe neto para describir patrones temporales. Variables: componentes temporales de `InvoiceDate`, `InvoiceNo` e importe derivado. La población deberá indicarse y advertir, si aplica, intervalos parcialmente cubiertos.
- **Distribución de cantidades, precios o importes:** mostrar la concentración, asimetría y valores extremos de `Quantity`, `UnitPrice` y/o importe de línea mediante una representación elegida según los rangos observados. Podrá separarse por cancelación o limitarse visualmente con cuantiles documentados, preservando el análisis de extremos.
- **Comparación geográfica:** representar los países con mayor actividad o importe mediante una selección transparente de categorías y una escala legible. Variables: `Country` y métricas agregadas de líneas, facturas, unidades o importe.
- **Concentración de artículos:** mostrar artículos o descripciones más frecuentes o de mayor importe después de comprobar la relación entre `StockCode` y `Description`. Variables: `StockCode`, `Description` y métricas agregadas.
- **Relación cantidad-precio:** explorar visualmente la asociación descriptiva entre `Quantity` y `UnitPrice`, usando estratificación, transparencia, escala o agregación apropiada para evitar sobreposición y distorsión por extremos. Variables: `Quantity`, `UnitPrice`, estado de cancelación e importe derivado cuando corresponda.

La generación definitiva se ajustará a los resultados de calidad, distribución y cardinalidad. Se omitirán figuras redundantes o no interpretables y se documentará cualquier cambio justificado respecto de estas propuestas.

# Supuestos y riesgos

- `InvoiceNo`, `StockCode` y `CustomerID` son identificadores nominales; sus formatos aparentes no autorizan interpretaciones ordinales o métricas.
- El prefijo `C` en `InvoiceNo` señala una cancelación según la documentación, pero deberá verificarse el patrón real de esos registros y distinguirse de cualquier otro valor atípico.
- Un importe de línea calculado como `Quantity` × `UnitPrice` describe el valor registrado y puede ser negativo en devoluciones o cancelaciones; no debe equipararse automáticamente a ingresos, beneficio, ventas cobradas ni margen.
- Las ausencias de `CustomerID` pueden condicionar análisis a nivel de cliente; excluirlas de esos análisis puede cambiar la población y deberá reportarse.
- Las ausencias de `Description` y posibles correspondencias no uno-a-uno con `StockCode` pueden afectar rankings y agrupaciones por producto.
- Filas idénticas o líneas con mismos identificadores pueden ser transacciones legítimas; cualquier deduplicación requerirá revisión y justificación.
- Precios, cantidades y facturas extremas pueden corresponder a transacciones comerciales válidas, ajustes o errores; no existe un catálogo externo autorizado para confirmarlo.
- La cobertura publicada empieza y termina en fechas concretas; los primeros o últimos meses podrían no representar meses completos y se deberán interpretar con cautela.
- `Country` se documenta como país asociado al cliente; no se asumirá que representa necesariamente el país de consumo, entrega o facturación final.
- El análisis será descriptivo del archivo entregado. No se inferirán mecanismos causales, comportamiento general fuera del período ni resultados predictivos.

# Criterios de finalización

- Se habrá documentado la carga del archivo original `xlsx`, la hoja analizada, la estructura, los tipos y la unidad de observación, sin modificar la fuente.
- El plan de calidad habrá producido comprobaciones cuantificadas de ausencias, duplicados, cardinalidades, tipos, rangos, signos, fechas, categorías y extremos cuando sean aplicables.
- Existirá `prepared_data.csv` como copia de trabajo válida, con comparación antes-después y transformaciones o conservaciones deliberadas registradas mediante `TR-NNN`.
- `statistics.json` contendrá el perfil original y preparado, estadísticas descriptivas, agregaciones y relaciones relevantes mediante identificadores `STAT-NNN`, junto con el registro de figuras.
- `issues.json` contendrá comprobaciones `CHK-NNN` e incidencias sustentadas, o documentará explícitamente que una comprobación no detectó problema.
- El directorio `figures/` contendrá al menos una figura PNG válida, legible, pertinente y registrada como `FIG-NNN`, con respaldo en resultados estructurados.
- `report.md` cubrirá las ocho etapas, citará resultados, incidencias y figuras existentes, y mantendrá un lenguaje descriptivo y no causal.
- Las dimensiones, identificadores, rutas relativas y referencias internas de todas las salidas deberán ser coherentes con el contrato, y se declararán las limitaciones que impidan confirmar una decisión o interpretación.