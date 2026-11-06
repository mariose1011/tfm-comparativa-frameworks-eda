# Ficha de referencia D2 — Online Retail

**Versión:** 0.1 
**Uso:** valores y criterios de referencia para la evaluación  
**Acceso durante el experimento:** no disponible para los agentes

## 1. Identificación y procedencia

- Dataset: Online Retail.
- Repositorio: UCI Machine Learning Repository.
- Página: https://archive.ics.uci.edu/dataset/352/online+retail
- DOI del dataset: `10.24432/C5BW33`.
- Licencia indicada por UCI: CC BY 4.0.
- Fecha de recuperación: 4 de agosto de 2026.
- Archivo utilizado: `datasets/experiment_inputs/D2_online_retail/Online Retail.xlsx`.
- SHA-256: `43465A06F2CCF7C8B5BD2892BC7DEFB52F97487934FE93B16AE4C3936424676D`.
- Documentación facilitada al agente: `datasets/experiment_inputs/D2_online_retail/Readme.md`.

La página de UCI indica que el dataset no contiene valores ausentes, pero el archivo original sí los contiene en `CustomerID` y `Description`. Para el experimento prevalecen el archivo congelado, su hash y las comprobaciones reproducibles de esta ficha.

## 2. Objetivo experimental del dataset

El agente deberá realizar un EDA tabular completo sobre las líneas de factura de una empresa británica de comercio electrónico entre diciembre de 2010 y diciembre de 2011.

No se solicita entrenar modelos predictivos. El análisis deberá cubrir estructura, calidad, preparación, estadística descriptiva, evolución temporal, cancelaciones, productos, clientes, países, visualizaciones, riesgos y un informe final respaldado por las salidas generadas.

Este dataset representa el caso con mayor complejidad de calidad. No existe una única limpieza correcta: varias decisiones dependerán de si se estudian ventas positivas, valor neto, cancelaciones, facturas, clientes o productos. Se valorará que el agente declare el objetivo y cuantifique el efecto de sus decisiones.

## 3. Estructura esperada

- Filas: 541.909.
- Columnas: 8.
- Inicio: 1 de diciembre de 2010 a las 08:26.
- Fin: 9 de diciembre de 2011 a las 12:50.
- Fechas naturales con actividad: 305.
- Marcas temporales distintas: 23.260.
- Periodos mensuales presentes: 13.
- Facturas distintas: 25.900.
- Códigos de artículo o concepto distintos: 4.070.
- Descripciones distintas no nulas: 4.223.
- Clientes distintos no nulos: 4.372.
- Países distintos: 38.

Cada fila es una línea de factura. Una factura puede contener varias líneas: la mediana es 10 y el máximo es 1.114 líneas. Por tanto, contar filas no equivale a contar facturas, compras, clientes o productos.

## 4. Diccionario operativo de variables

| Variable | Papel y tratamiento esperado |
| --- | --- |
| `InvoiceNo` | Identificador nominal de factura. Debe tratarse como texto o categoría. El prefijo `C` indica cancelación. |
| `StockCode` | Identificador nominal del artículo o concepto. Algunos códigos pueden representar portes, ajustes u otros conceptos no equivalentes a mercancía. |
| `Description` | Descripción del artículo o concepto. Contiene valores ausentes y puede variar para un mismo `StockCode`. |
| `Quantity` | Cantidad de la línea. Puede ser negativa en cancelaciones y ajustes. |
| `InvoiceDate` | Fecha y hora de la transacción. Debe convertirse a tipo temporal. |
| `UnitPrice` | Precio por unidad en libras esterlinas. Contiene ceros y dos valores negativos. |
| `CustomerID` | Identificador de cliente. Debe tratarse como texto o categoría que admita valores ausentes, no como una cantidad. |
| `Country` | País asociado al cliente. Es una variable categórica con fuerte predominio del Reino Unido. |

Puede crearse `LineTotal = Quantity × UnitPrice`, pero cualquier agregado deberá indicar si incluye duplicados, cancelaciones, cantidades negativas, precios no positivos y filas sin cliente.

## 5. Calidad y situaciones conocidas

### Valores ausentes

| Situación | Filas | Porcentaje |
| --- | ---: | ---: |
| `CustomerID` ausente | 135.080 | 24,9267 % |
| `Description` ausente | 1.454 | 0,2683 % |
| Ambos ausentes | 1.454 | 0,2683 % |
| Total de celdas ausentes | 136.534 | — |

Las filas sin `CustomerID` siguen siendo útiles para resultados globales, por país, producto o tiempo. Solo deben excluirse de análisis que necesiten identificar clientes, indicando que esa exclusión reduce la cobertura.

### Duplicados

- Duplicados exactos después de la primera aparición: 5.268, el 0,9721 % de las filas.
- Filas resultantes al eliminar duplicados exactos: 536.641.
- La eliminación de duplicados exactos reduce el valor neto en 21.740,98 libras.
- Valor neto después de deduplicar: 9.726.006,954 libras.

El archivo no permite demostrar por sí solo que toda repetición exacta sea un error. Se aceptará conservar los duplicados y analizar su impacto o eliminarlos con trazabilidad y una comprobación de sensibilidad.

### Cancelaciones, cantidades y precios

- Líneas cuyo `InvoiceNo` comienza por `C`: 9.288, pertenecientes a 3.836 facturas de cancelación.
- Todas esas líneas tienen cantidad negativa.
- Líneas con cantidad negativa: 10.624.
- Cantidades negativas sin prefijo `C`: 1.336; su importe agregado es cero y deben tratarse como ajustes que requieren interpretación.
- Líneas con cantidad igual a cero: 0.
- Líneas con precio igual a cero: 2.515.
- Líneas con precio negativo: 2.
- Facturas con prefijo `A`: 3 líneas correspondientes a 3 facturas de ajuste.

No se debe convertir el signo de las cantidades ni eliminar automáticamente cancelaciones o ajustes. Estas observaciones son necesarias para diferenciar actividad positiva, devoluciones y valor neto.

## 6. Valores descriptivos y monetarios principales

### Distribuciones

| Medida | `Quantity` | `UnitPrice` | `LineTotal` |
| --- | ---: | ---: | ---: |
| Media | 9,552250 | 4,611114 | 17,987795 |
| Mediana | 3 | 2,08 | 9,75 |
| Desviación típica muestral | 218,081158 | 96,759853 | 378,810824 |
| Primer cuartil | 1 | 1,25 | 3,40 |
| Tercer cuartil | 10 | 4,13 | 17,40 |
| Mínimo | -80.995 | -11.062,06 | -168.469,60 |
| Máximo | 80.995 | 38.970,00 | 168.469,60 |

La diferencia entre mediana, media, desviación y extremos evidencia una distribución muy asimétrica. Los gráficos y resúmenes deberán evitar que unos pocos valores oculten el comportamiento habitual.

### Definiciones monetarias de referencia

| Definición | Resultado |
| --- | ---: |
| Valor neto de todas las líneas, `Quantity × UnitPrice` | 9.747.747,934 £ |
| Líneas con `Quantity > 0` y `UnitPrice > 0` | 530.104 |
| Valor de esas ventas positivas | 10.666.684,544 £ |
| Valor de las líneas de cancelación con prefijo `C` | -896.812,490 £ |
| Valor de cantidades negativas sin `C` | 0,000 £ |
| Valor asociado a precios negativos | -22.124,120 £ |
| Valor neto después de eliminar duplicados exactos | 9.726.006,954 £ |

Ninguna de estas cifras debe denominarse simplemente “ingresos” sin explicar su definición. El valor de ventas positivas excluye cancelaciones y precios no positivos; el valor neto conserva sus signos y refleja ajustes.

## 7. Patrones de referencia

### Tiempo

- Noviembre de 2011 es el mes completo con mayor valor de ventas positivas: 1.509.496,33 £.
- Diciembre de 2011 contiene únicamente datos hasta el día 9 y no debe compararse directamente con meses completos.
- El valor de cancelaciones de diciembre de 2011 es -205.124,67 £, pero el periodo parcial y los extremos exigen prudencia.

### Países

- Reino Unido: 495.478 líneas, el 91,4320 % del dataset.
- Reino Unido concentra el 84,6113 % del valor de ventas positivas.
- Después del Reino Unido, los mayores valores positivos corresponden a Países Bajos, EIRE, Alemania y Francia.

Las comparaciones entre países deberán mostrar valores absolutos y, cuando proceda, medidas normalizadas, evitando conclusiones basadas en grupos muy pequeños.

### Productos y conceptos

- 647 `StockCode` tienen más de una descripción normalizada; el máximo observado es siete.
- El código `23843` encabeza la cantidad positiva por una observación extrema de 80.995 unidades.
- El código `DOT`, cuya descripción representativa es `DOTCOM POSTAGE`, encabeza el valor positivo por código con 206.248,77 £.

Por tanto, los rankings de “productos” deben distinguir mercancía, portes, ajustes y observaciones extremas. No todo `StockCode` representa un artículo ordinario.

## 8. Reglas de tolerancia para Q2

- Conteos, identificadores de categorías, fechas y signos: coincidencia exacta.
- Importes: tolerancia absoluta de 0,01 libras.
- Medias y medidas descriptivas: tolerancia absoluta de 0,01.
- Proporciones entre 0 y 1: tolerancia absoluta de 0,001.
- Porcentajes: tolerancia de 0,1 puntos porcentuales.
- Se admiten redondeos y resultados obtenidos mediante operaciones sencillas con cifras ya generadas por la ejecución, conforme al protocolo de evaluación.

Las 32 comprobaciones y sus pesos se definen en `evaluation_spec.json`. `reference_values.json` conserva los valores completos y varias agregaciones para validar soluciones equivalentes.

## 9. Decisiones válidas de preparación y limpieza

1. Convertir `InvoiceNo`, `StockCode` y `CustomerID` a identificadores de texto o categorías que admitan valores ausentes.
2. Convertir `InvoiceDate` a fecha y hora.
3. Crear `LineTotal`, documentando siempre la definición del agregado monetario.
4. Distinguir líneas, facturas, productos y clientes como unidades de análisis diferentes.
5. Conservar las cancelaciones e identificarlas mediante el prefijo `C`; pueden estudiarse separadas o incorporarse al valor neto.
6. Mantener filas sin `CustomerID` en análisis globales y excluirlas solo cuando el análisis requiera cliente, informando la cobertura.
7. Mantener `Description` ausente o utilizar una etiqueta explícita como “desconocido”, sin inventar descripciones.
8. Conservar duplicados y realizar sensibilidad, o eliminar solo duplicados exactos dejando trazabilidad e impacto.
9. Separar cantidades negativas sin `C`, precios cero y precios negativos como ajustes o incidencias que requieren investigación.
10. Mantener los extremos y utilizar escalas robustas o análisis de sensibilidad antes de decidir su exclusión.
11. Excluir diciembre de 2011 de comparaciones de meses completos o marcarlo claramente como parcial.
12. Agrupar categorías poco frecuentes cuando facilite la lectura de los gráficos, conservando el detalle original. También se admite mantenerlas sin agrupar si los gráficos son legibles y la decisión está justificada.

También se aceptarán alternativas equivalentes si preservan la trazabilidad, explican la población analizada y cuantifican el efecto de la decisión.

## 10. Decisiones incorrectas o perjudiciales

- Eliminar todas las filas sin `CustomerID` antes de calcular resultados globales.
- Convertir cantidades negativas en positivas o tratarlas como ventas normales.
- Eliminar cancelaciones sin informar su magnitud.
- Contar filas como facturas, clientes o productos distintos.
- Tratar los identificadores como variables numéricas continuas.
- Imputar clientes o descripciones concretas sin evidencia.
- Eliminar duplicados sin documentar el criterio ni cuantificar el impacto.
- Comparar diciembre de 2011 con meses completos sin indicar su cobertura parcial.
- Presentar un único importe como “ventas” o “ingresos” sin definirlo.
- Afirmar relaciones causales o crear visualizaciones ilegibles con miles de categorías.

## 11. Problemas y riesgos analíticos conocidos para Q4

1. Valores ausentes en `CustomerID` y `Description`.
2. Existencia de 5.268 duplicados exactos con interpretación no concluyente.
3. Cancelaciones identificadas mediante el prefijo `C` y cantidades negativas.
4. Cantidades negativas sin `C`, asociadas a ajustes.
5. Precios cero y dos precios negativos.
6. Diferencia entre línea de factura y factura, junto con identificadores de alta cardinalidad.
7. Cobertura parcial de diciembre de 2011.
8. Predominio geográfico del Reino Unido.
9. Asimetría y valores extremos de cantidades, precios e importes.
10. Dependencia de los resultados monetarios respecto a la definición y limpieza adoptadas.

Un riesgo contará como detectado cuando exista una afirmación explícita, correcta y trazable en `issues.json`, `report.md` u otra salida. Las falsas alarmas se incorporarán a la precisión de Q4.

Para considerar completo R08, debe identificarse el predominio del Reino Unido en el número de filas del archivo original. Si solo se describe su concentración en los importes, se registra una detección parcial.

## 12. Unidades de información esperadas para Q8

| Código | Peso | Contenido esperado |
| --- | ---: | --- |
| U01 | 2 | Estructura de 541.909 × 8 y periodo del 01/12/2010 al 09/12/2011. |
| U02 | 2 | Cuantificación de ausencias en `CustomerID` y `Description` y su efecto. |
| U03 | 2 | Distinción entre líneas, facturas, clientes y productos. |
| U04 | 2 | Detección de 5.268 duplicados y justificación de su tratamiento. |
| U05 | 2 | Cancelaciones con prefijo `C`, cantidades negativas y su magnitud. |
| U06 | 2 | Precios cero o negativos y cantidades negativas sin `C`. |
| U07 | 2 | Diferencia entre ventas positivas, valor neto, cancelaciones y resultado deduplicado. |
| U08 | 2 | Evolución temporal, noviembre de 2011 como máximo completo y diciembre de 2011 parcial. |
| U09 | 2 | Predominio del Reino Unido y cautela en comparaciones geográficas. |
| U10 | 1 | Alta cardinalidad y presencia de portes o ajustes entre los `StockCode`. |
| U11 | 2 | Asimetría y valores extremos de `Quantity`, `UnitPrice` o `LineTotal`. |
| U12 | 1 | Limitaciones de cobertura, una sola empresa, ausencias e incertidumbre sobre duplicados y ajustes. |

La cobertura se calculará como peso correctamente cubierto dividido entre el peso total. Una unidad parcialmente correcta recibirá la mitad de su peso. Una afirmación incorrecta no contará y podrá afectar a Q9.

Los hallazgos adicionales solo podrán mejorar Q5 o Q6 cuando sean relevantes y estén respaldados.

## 13. Objetivos visuales para Q7

1. **Evolución temporal:** ventas positivas, valor neto o cancelaciones por semana o mes, con definición clara y advertencia sobre diciembre de 2011.
2. **Cancelaciones y ajustes:** frecuencia o magnitud de cancelaciones, cantidades negativas y precios no positivos.
3. **Distribuciones:** `Quantity`, `UnitPrice` o `LineTotal` mediante escalas, recortes visuales, paneles o transformaciones que conserven negativos y no oculten extremos.
4. **Países:** concentración geográfica con un diseño que permita leer tanto Reino Unido como los siguientes países relevantes.
5. **Productos o clientes:** concentración mediante un top limitado, una métrica definida y exclusión o identificación de portes y ajustes cuando proceda.

No se exige un tipo de gráfico concreto. Se aceptarán soluciones equivalentes que cumplan el objetivo y mantengan coherencia con las decisiones de preparación.

## 14. Etapas y archivos obligatorios

Las ocho etapas del EDA deberán dejar evidencia:

1. Carga e inspección inicial.
2. Estructura, tipos y calidad.
3. Preparación y decisiones de análisis.
4. Estadística descriptiva.
5. Variables, agregaciones y relaciones.
6. Visualizaciones.
7. Problemas, riesgos y anomalías.
8. Informe final.

Salidas previstas por el contrato común:

- `plan.md`.
- `prepared_data.csv`.
- `statistics.json`.
- `issues.json`.
- Directorio `figures/`.
- `report.md`.
- `trace.jsonl`.

## 15. Aplicación de las métricas

- **Q1:** evidencias de las ocho etapas y archivos obligatorios.
- **Q2:** comprobaciones de `evaluation_spec.json` contra `reference_values.json`.
- **Q3:** decisiones de preparación comparadas con las secciones 9 y 10; se aceptan varias poblaciones si están justificadas.
- **Q4:** precisión, cobertura y F1 respecto a los diez riesgos de la sección 11.
- **Q5 y Q6:** rúbrica manual sobre profundidad del EDA e interpretación.
- **Q7:** media de las puntuaciones de los cinco objetivos visuales, multiplicada por 25 para expresarla de 0 a 100.
- **Q8:** cobertura ponderada de las doce unidades de información.
- **Q9:** fidelidad de las afirmaciones respecto a datos, estadísticas, gráficos y trazas.
- **Q10:** claridad y coherencia del informe.