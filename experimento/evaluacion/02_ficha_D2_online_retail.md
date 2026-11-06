# Guía de evaluación D2 Online Retail

**Versión:** 0.1 ; **Uso:** criterios específicos de D2

Esta guía recoge los criterios específicos para evaluar D2. No se completa para cada ejecución. Las puntuaciones finales se registran en el [Excel](Evaluacion_calidad.xlsx), mientras que las justificaciones y evidencias se detallan en la ficha de cada ejecución.

Los apartados siguientes detallan las comprobaciones numéricas, las decisiones de preparación, los riesgos, los objetivos visuales y los contenidos del informe específicos de este dataset, correspondientes a Q2, Q3, Q4, Q7 y Q8. Las demás métricas utilizan criterios comunes a los dos datasets. Las fórmulas, escalas y reglas generales de puntuación se consultan en el [protocolo de evaluación](01_protocolo_calidad_Q1_Q10_v0.1.md).

Referencias del dataset: [especificación](../../datasets/reference_private/D2_online_retail/evaluation_spec.json), [valores de referencia](../../datasets/reference_private/D2_online_retail/reference_values.json) y [ficha privada](../../datasets/reference_private/D2_online_retail/ficha_referencia_D2_online_retail.md).

## Q2 Comprobaciones numéricas

32 comprobaciones, con peso total 47. Los valores deben corresponder a la población y definición indicadas en la referencia.

Los importes se expresan en libras esterlinas y se calculan como Quantity x UnitPrice. Las ventas positivas incluyen únicamente filas con Quantity > 0 y UnitPrice > 0, las cancelaciones corresponden a las filas cuyo InvoiceNo comienza por C.

| ID | Comprobación | Referencia y tolerancia | Peso |
| --- | --- | --- | --- |
| C01 | Número de filas | 541909 ; Exacto | 2 |
| C02 | Número de columnas | 8 ; Exacto | 2 |
| C03 | Primera fecha y hora | 2010-12-01T08:26:00 ; Exacto | 1 |
| C04 | Última fecha y hora | 2011-12-09T12:50:00 ; Exacto | 1 |
| C05 | Celdas ausentes totales | 136534 ; Exacto | 2 |
| C06 | CustomerID ausentes | 135080 ; Exacto | 2 |
| C07 | Description ausentes | 1454 ; Exacto | 2 |
| C08 | Filas con CustomerID y Description ausentes | 1454 ; Exacto | 1 |
| C09 | Filas duplicadas después de la primera | 5268 ; Exacto | 2 |
| C10 | Filas después de eliminar duplicados exactos | 536641 ; Exacto | 1 |
| C11 | Facturas distintas | 25900 ; Exacto | 1 |
| C12 | StockCode distintos | 4070 ; Exacto | 1 |
| C13 | Clientes distintos con identificador disponible | 4372 ; Exacto | 1 |
| C14 | Países distintos | 38 ; Exacto | 1 |
| C15 | Líneas de cancelación | 9288 ; Exacto | 2 |
| C16 | Facturas de cancelación distintas | 3836 ; Exacto | 1 |
| C17 | Cantidades negativas | 10624 ; Exacto | 2 |
| C18 | Cantidades negativas sin prefijo C | 1336 ; Exacto | 2 |
| C19 | Precios iguales a cero | 2515 ; Exacto | 2 |
| C20 | Precios negativos | 2 ; Exacto | 2 |
| C21 | Suma de Quantity, incluidas las cantidades negativas | 5176450 ; Exacto | 1 |
| C22 | Cantidad mínima | -80995 ; Exacto | 1 |
| C23 | Cantidad máxima | 80995 ; Exacto | 1 |
| C24 | Valor neto de todas las líneas | 9747747.934 ; ± 0.01 | 2 |
| C25 | Líneas de venta positiva | 530104 ; Exacto | 1 |
| C26 | Valor de ventas positivas | 10666684.544 ; ± 0.01 | 2 |
| C27 | Valor de las cancelaciones | -896812.49 ; ± 0.01 | 2 |
| C28 | Valor neto después de eliminar duplicados exactos | 9726006.954 ; ± 0.01 | 1 |
| C29 | Proporción de líneas del Reino Unido | 0.914319563 ; ± 0.001 | 1 |
| C30 | Mes completo con mayor venta positiva | Categoría 2011-11, valor 1509496.33 ; ± 0.01 | 2 |
| C31 | StockCode con varias descripciones normalizadas | 647 ; Exacto | 1 |
| C32 | Mediana de líneas por factura | 10 ; ± 0.01 | 1 |

Para C31, las descripciones se comparan después de eliminar los espacios iniciales y finales y convertirlas a mayúsculas.

## Q3 Tratamiento de datos

Doce decisiones sobre la preparación y conservación de los datos.

| ID | Ámbito de decisión |
| --- | --- |
| D01 | Tratar InvoiceNo, StockCode y CustomerID como identificadores, sin utilizarlos como cantidades. Se pueden representar como texto o categorías que admitan valores ausentes |
| D02 | Convertir InvoiceDate a fecha y hora |
| D03 | Crear LineTotal = Quantity × UnitPrice y documentar la definición de cada agregado |
| D04 | Distinguir línea de factura, factura, cliente y producto como unidades de análisis diferentes |
| D05 | Conservar e identificar las cancelaciones por prefijo C. Analizarlas por separado o incorporarlas al valor neto |
| D06 | Mantener filas sin CustomerID en análisis globales y excluirlas solo de análisis por cliente, informando la cobertura |
| D07 | Mantener Description ausente o sustituirla por una etiqueta explícita de desconocido, sin inventar el texto |
| D08 | Conservar los duplicados y analizar sensibilidad, o eliminar solo duplicados exactos dejando trazabilidad e impacto |
| D09 | Separar cantidades negativas sin C, precios cero y precios negativos como ajustes que requieren investigación |
| D10 | Mantener valores extremos y realizar análisis de sensibilidad o escalas robustas antes de decidir su exclusión |
| D11 | Excluir diciembre de 2011 de comparaciones entre meses completos o marcarlo claramente como parcial |
| D12 | Agrupar categorías poco frecuentes cuando facilite la lectura de los gráficos, conservando el detalle original. |

## Q4 Riesgos previstos

Diez riesgos de referencia. El tratamiento de riesgos adicionales, detecciones parciales y falsas alarmas se establece en el protocolo.

| ID | Riesgo conocido |
| --- | --- |
| R01 | CustomerID y Description contienen valores ausentes |
| R02 | Existen 5268 duplicados exactos, pero su eliminación requiere justificación |
| R03 | Las facturas con prefijo C representan cancelaciones y tienen cantidades negativas |
| R04 | Hay 1336 cantidades negativas sin prefijo C asociadas a ajustes |
| R05 | Existen precios cero y dos precios negativos |
| R06 | Cada fila es una línea de factura y los identificadores son categóricos de alta cardinalidad |
| R07 | Diciembre de 2011 solo contiene datos hasta el día 9 |
| R08 | El Reino Unido concentra más del 91 % de las filas del archivo original. |
| R09 | Quantity, UnitPrice e importe presentan asimetría y valores extremos muy elevados |
| R10 | Los resultados monetarios cambian según se midan ventas positivas, valor neto, cancelaciones o datos deduplicados |

Para considerar completo R08, la ejecución debe identificar la concentración de filas del archivo original en el Reino Unido. Si solo describe su predominio en los importes, se registra una detección parcial, aunque las tablas también incluyan recuentos de filas.

## Q7 Objetivos visuales

Cinco objetivos, que pueden cubrirse con distintos tipos o combinaciones de gráficos.

| ID | Objetivo |
| --- | --- |
| V01 | Mostrar por semana o mes ventas positivas, valor neto o cancelaciones con definición clara y advertencia sobre diciembre de 2011 |
| V02 | Representar la frecuencia o magnitud de cancelaciones, cantidades negativas y precios no positivos |
| V03 | Mostrar la distribución de Quantity, UnitPrice o LineTotal sin ocultar asimetrías, valores negativos o extremos relevantes. Basta con representar una de estas variables |
| V04 | Comparar la concentración geográfica sin permitir que el Reino Unido o categorías pequeñas oculten la lectura |
| V05 | Mostrar concentración en productos, conceptos o clientes mediante un top limitado y una métrica claramente definida |

## Q8 Contenidos del informe

Doce contenidos esperados, con peso total 22.

| ID | Contenido esperado | Peso |
| --- | --- | --- |
| U01 | Indicar 541909 líneas, 8 columnas y el periodo desde 2010-12-01 hasta 2011-12-09 | 2 |
| U02 | Cuantificar CustomerID y Description ausentes y explicar su impacto | 2 |
| U03 | Distinguir líneas, facturas, clientes y productos | 2 |
| U04 | Detectar 5268 duplicados exactos y justificar si se conservan o eliminan | 2 |
| U05 | Reconocer el prefijo C, las cantidades negativas y su magnitud | 2 |
| U06 | Identificar precios cero, negativos y cantidades negativas sin C | 2 |
| U07 | Diferenciar valor neto, ventas positivas, cancelaciones y efecto de eliminar duplicados | 2 |
| U08 | Describir la evolución y señalar que diciembre de 2011 es parcial. Noviembre de 2011 es el mayor mes completo en ventas positivas | 2 |
| U09 | Mostrar el predominio del Reino Unido y evitar comparaciones engañosas por tamaños muy distintos | 2 |
| U10 | Explicar que los identificadores contienen numerosos valores distintos y que algunos códigos StockCode representan gastos de envío o ajustes, en lugar de productos | 1 |
| U11 | Reconocer la fuerte asimetría y los extremos de Quantity, UnitPrice o LineTotal | 2 |
| U12 | Explicar cobertura temporal, datos de una sola empresa, ausencias e incertidumbre sobre ajustes y duplicados | 1 |