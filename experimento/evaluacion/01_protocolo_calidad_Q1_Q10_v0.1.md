# Protocolo de evaluación de la calidad de los análisis

Este protocolo describe cómo se aplican las diez métricas de calidad Q1–Q10 a las dieciocho ejecuciones definitivas de D1 y D2, incluidas las dos parciales. Se complementa con las guías específicas de cada dataset y con las fichas y comprobaciones de cada ejecución.

Recoge las reglas, las puntuaciones finales y los materiales de evaluación se consultan en el [README](README.md).

## 1. Documentos de referencia

- Memoria, apartados 4.6, 6.1 y 6.2 y [rúbrica original](../../Tabla%20de%20métricas%20y%20rúbrica%20de%20evaluación.docx).
- Contrato: [etapas](../contrato_comun_v1.0/01_alcance_entradas_y_etapas.md) y [archivos](../contrato_comun_v1.0/03_archivos_y_esquemas.md).
- Referencias de [D1](../../datasets/reference_private/D1_bike_sharing/ficha_referencia_D1_bike_sharing.md) y [D2](../../datasets/reference_private/D2_online_retail/ficha_referencia_D2_online_retail.md), con sus `evaluation_spec.json` y `reference_values.json`.
- [Registro de las ejecuciones definitivas](../REGISTRO_EJECUCIONES_D1_D2.md), que identifica las ejecuciones incluidas y los intentos invalidados.

Las guías [D1](02_ficha_D1_bike_sharing.md) y [D2](02_ficha_D2_online_retail.md)  concretan las comprobaciones de cada dataset. En ellas, los códigos C identifican las comprobaciones numéricas; D, los ámbitos de preparación; R, los riesgos de referencia; V, los objetivos visuales; y U, las unidades de contenido del informe.

## 2. Reglas comunes

- Evaluar los productos finales, incluidos los cambios de la corrección solicitada por el Revisor, cuando se utiliza.
- Incluir las dos ejecuciones parciales y excluir el piloto D0 y los intentos invalidados.
- Justificar cada puntuación con evidencias localizables en el informe, las estadísticas, el registro de problemas, los datos preparados, las figuras o la traza.
- Admitir procedimientos y soluciones analíticas equivalentes cuando cumplen los criterios de la métrica.
- Valorar las ausencias y los errores en los componentes afectados. Un mismo problema puede repercutir en varias métricas si afecta a aspectos distintos, pero no se aplica una penalización global adicional.
- Realizar los cálculos de comprobación fuera de la carpeta original, sin modificar los archivos ni completar resultados ausentes.

## 3. Métricas e índice

Las diez métricas se expresan en una escala de 0 a 100.

| Métrica | Peso | Procedimiento | Intervención humana |
| --- | ---: | --- | --- |
| Q1 Cumplimiento de las etapas | 10 % | Ocho etapas puntuadas con 0, 0,5 o 1 | Confirmar si las evidencias permiten considerar cada etapa completa, incompleta o no realizada |
| Q2 Corrección numérica | 15 % | Comparación con valores de referencia, tolerancias y pesos | Confirmar la correspondencia entre resultados y comprobaciones y revisar las equivalencias |
| Q3 Validez del tratamiento de datos | 10 % | Proporción de decisiones válidas y justificadas sobre los datos | Valorar las decisiones y comprobar su justificación y aplicación |
| Q4 Detección de problemas y riesgos | 10 % | Cálculo de precisión, cobertura y F1 | Clasificar los riesgos detectados, las equivalencias y las falsas alarmas |
| Q5 Calidad y profundidad del EDA | 10 % | Rúbrica de 0 a 4 | Valoración manual |
| Q6 Profundidad de la interpretación | 10 % | Rúbrica de 0 a 4 | Valoración manual |
| Q7 Calidad de las visualizaciones | 10 % | Media de cinco objetivos puntuados de 0 a 4 | Inspeccionar las figuras y contrastarlas con los datos |
| Q8 Cobertura del informe | 10 % | Doce unidades de contenido con pesos 1 o 2 y posibilidad de puntuación parcial | Confirmar el cumplimiento de cada unidad |
| Q9 Fidelidad del informe | 10 % | Proporción de afirmaciones comprobables respaldadas | Identificar y clasificar las afirmaciones |
| Q10 Claridad y coherencia | 5 % | Rúbrica de 0 a 4 | Valoración manual |

El índice de calidad se calcula mediante la siguiente fórmula:

`Índice = 0,10 × Q1 + 0,15 × Q2 + 0,10 × (Q3 + Q4 + Q5 + Q6 + Q7 + Q8 + Q9) + 0,05 × Q10`

Los cálculos conservan su precisión completa y los resultados se presentan con dos decimales. Q5, Q6 y Q10 utilizan niveles enteros de 0 a 4, sin medios puntos.

## 4. Q1 Cumplimiento de las etapas

Q1 valora si se realiza cada una de las ocho etapas.

| Etapa | Evidencia para 1 punto |
| --- | --- |
| E1 Carga e inspección | Lectura del dataset, identificación de sus dimensiones y columnas y explicación de qué representa cada fila. Si esta información no puede determinarse, deben indicarse el motivo y las limitaciones que supone para el análisis. |
| E2 Tipos y calidad | Inspección documentada de tipos, valores ausentes, duplicados y otros aspectos pertinentes del contrato, con resultados cuantificados |
| E3 Preparación | Copia preparada utilizable, decisiones justificadas y comparación básica antes y después, también cuando se decide conservar los datos |
| E4 Descripción | Resultados estructurados y reproducibles de las variables principales, con medidas apropiadas y población identificable |
| E5 Relaciones | Varias relaciones o agregaciones pertinentes, acompañadas de cifras e interpretación, sin exigir una técnica concreta |
| E6 Visualización | Figuras válidas e identificables, vinculadas a los análisis y con una representación interpretable |
| E7 Riesgos | Registro estructurado de comprobaciones o riesgos, evidencias, decisiones y consecuencias. |
| E8 Informe | Informe final que integra alcance, preparación, hallazgos, evidencias y limitaciones de forma evaluable |

Cada etapa recibe:
- **1 punto:** evidencia completa. 
- **0,5 puntos:** trabajo válido con una carencia sustancial. 
**0 puntos:** sin evidencia válida, archivo vacío o actuación fallida.

`Q1 = 100 × suma de las ocho puntuaciones / 8`

Un objetivo visual ausente se valora en Q7 y no reduce automáticamente la puntuación de E6. Del mismo modo, los riesgos descritos en el informe pueden contar en Q4 aunque falte el registro estructurado exigido para completar E7.

## 5. Q2 Corrección numérica

Q2 compara las comprobaciones previstas con sus valores de referencia y tolerancias. D1 contiene 26 comprobaciones con un peso total de 35 y D2 contiene 32 con un peso total de 47.

Cada comprobación recibe:
- **1:** resultado correcto. 
- **0:** resultado incorrecto, ausente o no verificable tras la revisión, indicando el motivo. 

`Q2 = 100 × suma de los pesos de las comprobaciones correctas / suma de los pesos previstos`

Se aplican las siguientes reglas:
- Registrar el resultado obtenido, el valor de referencia, los datos sobre los que se calcula, qué mide, su unidad de medida cuando corresponda, el margen de diferencia permitido y la evidencia utilizada.
- Buscar primero en `statistics.json`. También se admiten resultados del informe, las figuras o las respuestas de las herramientas cuando puede identificarse claramente qué miden y a qué datos corresponden.
- Se permite obtener un resultado mediante operaciones sencillas con cifras ya generadas por la ejecución, siempre que correspondan a los datos exigidos y tengan precisión suficiente. Deben registrarse los valores utilizados y la operación realizada.
- Se pueden convertir las unidades para comparar resultados equivalentes, por ejemplo de horas a minutos.
- El resultado debe calcularse sobre los mismos datos y con la medida exigida en la referencia. Si una comprobación exige la correlación de Pearson, presentar Spearman no la completa, aunque su uso pueda estar justificado en el análisis.
- Si el cálculo estructurado es correcto y el informe lo transcribe mal, valorar ese error en Q9. Si existen resultados estructurados finales incompatibles y no puede identificarse cuál constituye la corrección, asignar 0 a la comprobación.
- Comprobar que un filtro corresponde a la población de referencia no autoriza a calcular un resultado ausente. Para admitir una resta, las salidas deben demostrar qué elementos incluyen los conjuntos utilizados
- Los cálculos adicionales no aportan puntos extra ni amplían el denominador.

## 6. Q3 Validez del tratamiento de datos

Q3 valora los ámbitos de preparación definidos en las referencias, ocho en D1 y doce en D2, todos con el mismo peso.

Cada ámbito recibe:
- **1:** decisión válida, justificada y aplicada. 
- **0:** decisión perjudicial, injustificada, ausente o incompleta.

Para D1:
`Q3 = 100 × ámbitos correctamente resueltos / 8`

Para D2:
`Q3 = 100 × ámbitos correctamente resueltos / 12`, para D2.

Se aplican las siguientes reglas:
- Conservar los datos puede ser una decisión válida. No se exige transformarlos ni ejecutar literalmente el procedimiento sugerido en las referencias.
- Contrastar las decisiones con los datos y las operaciones realizadas, no solo con las declaraciones del informe.

## 7. Q4 Detección de problemas y riesgos

Q4 compara los riesgos detectados con los siete previstos en D1 o los diez previstos en D2.

Se aplican las siguientes reglas:
- Contar una vez cada riesgo explícito, correcto y respaldado. Registrar la afirmación, la evidencia y su correspondencia con la referencia.
- Cuando un riesgo incluye varios aspectos exigidos por la referencia, deben identificarse todos para obtener puntuación. Si solo se detecta una parte correctamente, se registra como detección parcial, sin puntos y sin considerarla un problema inventado.
- Se considera falsa alarma un problema que la ejecución presenta como existente, pero que es falso o no cuenta con evidencias suficientes.
- Informar correctamente de que un problema no existe no suma como riesgo detectado ni cuenta como falsa alarma.

Para el cálculo se utilizan:
- **K:** riesgos conocidos detectados por completo. 
- **A:** otros riesgos no incluidos en la lista de referencia cuya validez y respaldo son comprobados
- **F:** falsas alarmas. 
- **R:** riesgos conocidos previstos, siete en D1 o diez en D2.

`Precisión = (K + A) / (K + A + F)`

`Cobertura = K / R`

`Q4 = 100 × 2 × Precisión × Cobertura / (Precisión + Cobertura)`

Si no se detecta ningún riesgo, la precisión es 0. Si la precisión y la cobertura son 0, Q4 es 0.

Registrar K, A, F, precisión y cobertura. Los riesgos adicionales no aumentan la cobertura de los riesgos conocidos ni amplían R.

## 8. Q5 Calidad y profundidad del EDA

Q5 valora la selección y profundidad de los análisis realizados.

| Nivel | Criterio de la rúbrica |
| ---: | --- |
| 0 | No hay EDA válido o los análisis son incorrectos |
| 1 | Análisis superficial que enumera resultados básicos y omite relaciones o problemas importantes |
| 2 | EDA básico correcto, con pocas relaciones o profundidad limitada |
| 3 | Análisis correcto de variables, relaciones, distribuciones y anomalías relevantes, con omisiones menores |
| 4 | EDA completo y coherente que prioriza hallazgos, relaciona etapas y considera explicaciones alternativas o limitaciones |

`Q5 = 25 × nivel obtenido`

Justificar el nivel mediante las fortalezas y carencias observadas y explicar qué impide alcanzar el nivel superior, cuando corresponde. Revisar las estadísticas, la preparación y las figuras.

No se exige una cantidad determinada de análisis ni se premian las listas de cifras por su extensión. Un fallo localizado no invalida automáticamente todo el EDA.

## 9. Q6 Profundidad de la interpretación

Q6 valora el significado que se extrae de los resultados. Q5 evalúa el análisis realizado y Q6, su interpretación.

| Nivel | Criterio de la rúbrica |
| ---: | --- |
| 0 | No interpreta los resultados o las interpretaciones son incorrectas |
| 1 | Describe valores sin explicar su significado o realiza inferencias débiles |
| 2 | Interpreta correctamente los resultados principales, de forma superficial o incompleta |
| 3 | Explica los hallazgos relevantes y los relaciona correctamente con cálculos, tablas y figuras |
| 4 | Ofrece una interpretación integrada, prudente y respaldada, diferenciando evidencia, posibles explicaciones y limitaciones |

`Q6 = 25 × nivel obtenido`

Revisar la población, el periodo, los tamaños de los grupos y la incertidumbre. Una hipótesis explícita no equivale a una conclusión demostrada. Las explicaciones sin respaldo presentadas como hechos no reciben crédito.

## 10. Q7 Calidad de las visualizaciones

Q7 valora los cinco objetivos visuales de cada dataset.

| Nivel | Criterio de la rúbrica |
| ---: | --- |
| 0 | El objetivo no está representado o la representación es inválida, incorrecta o engañosa |
| 1 | Presenta problemas graves de selección, legibilidad, escalas, etiquetas o correspondencia con los datos |
| 2 | Visualización utilizable con carencias de etiquetado, explicación o elección del gráfico |
| 3 | Representación clara, adecuada y etiquetada que respalda el análisis, con deficiencias menores |
| 4 | Representación técnicamente correcta, clara, adecuada y bien integrada en la interpretación |

`Q7 = 100 × suma de las cinco puntuaciones / 20`

Se aplican las siguientes reglas:
- Revisar las imágenes y contrastar datos, filtros y agregaciones utilizados.
- Puntuar el conjunto de figuras que cubre cada objetivo, sin elegir únicamente la mejor cuando existen contradicciones.
- Una figura puede cubrir varios objetivos.
- Los objetivos no representados reciben 0.
- Si una figura existe, se revisa aunque su enlace en el informe no funcione o no esté explicada. Estas carencias se valoran según cómo dificultan comprenderla o relacionarla con el análisis, sin dar por hecho que la imagen falta o contiene datos incorrectos.

## 11. Q8 Cobertura del informe

Q8 valora las doce unidades de contenido previstas, con un peso total de 22.

Cada unidad recibe:
- **1:** todos los aspectos exigidos están cubiertos correctamente.
- **0,5:** cobertura sustancial pero incompleta, sin afirmaciones falsas sobre los contenidos exigidos.
- **0:** unidad ausente o con algún componente exigido incorrecto. Otro componente correcto no compensa el falso.

`Q8 = 100 × suma de cada peso multiplicado por 0, 0,5 o 1 / 22`

Utilizar el informe y las tablas y figuras que incorpora o explica. Las estadísticas que no se comunican en él no completan Q8.

## 12. Q9 Fidelidad del informe

Q9 contrasta todas las afirmaciones comprobables del informe, incluidas las contenidas en tablas, figuras y conclusiones.

Se aplican las siguientes reglas:
- Separar los hechos que pueden comprobarse de forma independiente. '100 filas y ningún valor ausente' contiene dos afirmaciones.
- Contar una sola vez las repeticiones de una afirmación sobre la misma población. Si cambia el valor, la población o el significado, registrar las afirmaciones por separado.
- Incluir cifras, tendencias, comparaciones, decisiones de preparación y conclusiones empíricas. Excluir títulos, preguntas, planes y recomendaciones que no contengan afirmaciones de hecho.
- En las hipótesis explícitas, comprobar las afirmaciones que les sirven de base, sin exigir que la hipótesis quede demostrada.

Cada afirmación se clasifica como:
- **Respaldada:** las evidencias válidas de la ejecución sostienen la afirmación y corresponden a la población indicada.
- **Contradicha:** las evidencias muestran que es falsa. 
- **Sin respaldo:** no existen evidencias suficientes para sostenerla.

`Q9 = 100 × afirmaciones respaldadas / afirmaciones comprobables distintas`

Se admiten redondeos que proceden de resultados válidos, incluidos los realizados en varios pasos si pueden comprobarse.

Cada afirmación debe contar con evidencias válidas de la propia ejecución. Coincidir con el valor de referencia no basta si la ejecución no aporta respaldo.

Registrar las afirmaciones revisadas, dónde aparecen y su clasificación. Las incorrectas y las que carecen de respaldo se incluyen en el total utilizado para calcular Q9. Si no existe informe o no contiene afirmaciones comprobables, Q9 es 0. Todas las afirmaciones tienen el mismo peso.

## 13. Q10 Claridad y coherencia

Q10 valora la claridad, la organización y la coherencia del informe.

| Nivel | Criterio de la rúbrica |
| ---: | --- |
| 0 | Informe incomprensible, contradictorio o sin estructura |
| 1 | Organización deficiente, ambigüedades o contradicciones importantes |
| 2 | Informe comprensible con repeticiones, saltos lógicos o explicaciones poco claras |
| 3 | Informe bien estructurado y claro, con problemas menores |
| 4 | Informe claro, conciso y coherente que conecta evidencias, conclusiones y limitaciones |

`Q10 = 25 × nivel obtenido`

Valorar el informe completo. Una contradicción localizada no obliga a asignar 0. Si no existe un informe evaluable, Q10 es 0.

## 14. Revisión y presentación

- Evaluar las ejecuciones parciales con los resultados que conservan, sin completarlos ni combinar versiones.
- Conservar en el Excel la propuesta inicial, la puntuación final y el motivo de los cambios. Las justificaciones, las evidencias y los cálculos deben permitir comprender la puntuación vigente.
- Mantener un criterio común. Si surge una ambigüedad, documentar su resolución y revisar todas las ejecuciones afectadas.
- Para cada combinación de framework y dataset, presentar las tres repeticiones, la mediana y los valores mínimo y máximo. El resumen de cada framework se obtiene mediante la media de sus medianas de D1 y D2, con igual peso para ambos datasets.
- Analizar la calidad por separado del tiempo, los tokens, el coste y la finalización técnica.