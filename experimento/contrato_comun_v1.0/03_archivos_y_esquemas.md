# Parte 3. Archivos de salida y esquemas comunes

**Contrato:** v1.0

[← Parte 2](02_roles_coordinacion_y_finalizacion.md) · [Parte 4 →](04_herramientas.md)

Esta parte define los artefactos que debe producir cada ejecución, junto con los requisitos que permiten validarlos y evaluarlos de la misma forma en las tres implementaciones.

Para cada salida se especifican su finalidad, quién la genera, su ubicación, su formato y su contenido obligatorio. También se indican los criterios de validez, su relación con las demás salidas y cuándo se genera, actualiza y comprueba.

El Planificador y el Analista producen los contenidos que les corresponden y la capa común los guarda. Un archivo vacío, una estructura de ejemplo sin completar o un contenido ajeno al trabajo realizado no se considera una salida válida.

## 18. Directorio común de resultados
Cada ejecución dispone de una carpeta inicialmente vacía y exclusiva, identificada mediante `run_id`. En ella se generan seis archivos y una carpeta de figuras:
```text
<run_id>/
├── plan.md
├── prepared_data.csv
├── statistics.json
├── issues.json
├── figures/
├── report.md
└── trace.jsonl
```
Los nombres y la organización interna son iguales en las tres implementaciones. Los resultados se guardan dentro de esta carpeta y no se utilizan archivos de otras ejecuciones. Los archivos temporales permanecen separados de las salidas obligatorias y no sustituyen las evidencias exigidas para la evaluación.

Los archivos de texto utilizan UTF-8. Los identificadores de cada tipo de elemento, como figuras o resultados estadísticos, deben ser únicos dentro de la ejecución. Las rutas que enlazan las salidas generadas son relativas a la carpeta de la ejecución, sin depender de ubicaciones absolutas del equipo.

## 19. `plan.md`

### 19.1. Finalidad y responsable
plan.md recoge el plan elaborado por el Planificador a partir del objetivo común, la documentación pública del dataset y la inspección inicial. Describe el trabajo previsto sin anticipar los resultados del análisis.

La capa común comprueba la estructura de la respuesta y guarda su contenido antes de iniciar la intervención del Analista.

### 19.2. Estructura obligatoria
El documento debe contener exactamente los siguientes encabezados de primer nivel, escritos con # y en este orden:
1. `# Identificación`: run_id, framework_id, dataset_id, contract_version y prompt_version.
2. `# Comprensión inicial`: explica qué representa cada fila, el alcance del análisis y los aspectos que aún deben aclararse.
3. `# Preguntas analíticas`: plantea las preguntas que orientan el EDA.
4. `# Plan por etapas`: organiza el trabajo en ocho apartados, E1 a E8.
5. `# Visualizaciones previstas`: indica el objetivo de las figuras propuestas y las variables implicadas.
6. `# Supuestos y riesgos`: identifica las cuestiones que deben comprobarse durante el análisis.
7. `# Criterios de finalización`: especifica las evidencias necesarias para considerar completado el trabajo previsto.

Cada apartado de `E1` a `E8` debe incluir como mínimo:
- Objetivo de la etapa.
- Comprobaciones o análisis previstos.
- Variables o grupos relevantes.
- Evidencia que se espera generar.
- Dependencias o supuestos conocidos.

### 19.3. Reglas de validez
El archivo debe ser legible, utilizar UTF-8, contener todas las secciones y campos obligatorios y corresponder a la ejecución actual. Su contenido debe ofrecer instrucciones concretas para el Analista y estar adaptado al dataset.

No cumple el contrato si presenta resultados analíticos como ya comprobados sin respaldo en la inspección inicial, incorpora referencias privadas, amplía el alcance o se limita a repetir las instrucciones generales.

El plan original se conserva sin sobrescribirlo. Los cambios que el Analista necesite introducir durante el análisis se justifican en `statistics.json`, `issues.json` o `trace.jsonl`.

## 20. `prepared_data.csv`

### 20.1. Finalidad y responsable
`prepared_data.csv` conserva los datos resultantes de las decisiones de preparación del Analista, sin modificar el archivo original. Permite revisar qué observaciones y variables se mantienen y qué transformaciones se aplican. El Analista genera esta copia mediante `execute_python` y debe mantenerla coherente con los datos utilizados en los cálculos.

### 20.2. Formato obligatorio
- CSV con encabezado único y codificación UTF-8.
- Cada columna corresponde a una variable original o creada durante el análisis. El archivo conserva todas las filas, salvo aquellas cuya eliminación se haya justificado.
- Coma como separador. Los campos que contengan comas, comillas o saltos de línea deben escribirse siguiendo las reglas del formato CSV.
- Fechas guardadas de forma no ambigua, preferentemente con formato ISO 8601.
- Valores ausentes representados mediante campos vacíos, no se utilizarán cadenas ambiguas como `0`, `-` o `sin dato` salvo que sean valores reales.
- Sin columna de índice artificial, excepto cuando el propio análisis cree justificadamente un identificador trazable.
- Sin fórmulas destinadas a ejecutarse al abrir el archivo ni contenido externo incrustado.

El archivo puede conservar las mismas filas y columnas que el original cuando el Analista justifique que no es necesario transformar los datos. En ese caso seguirá generándose una copia separada y la decisión se documentará.

### 20.3. Reglas de validez
El archivo debe poder cargarse, contener encabezados válidos y coincidir con el número de filas, el número de columnas y los nombres declarados en statistics.json. Las diferencias respecto al original deben estar justificadas.

No cumple el contrato si está vacío, es ilegible, omite transformaciones que se declaran como aplicadas o se genera sobrescribiendo el archivo original. 

## 21. `statistics.json`

### 21.1. Finalidad y responsable
`statistics.json` reúne la descripción de los datos originales y preparados, las decisiones de preparación, los resultados de los cálculos y la información de las figuras. Es la principal fuente de evidencia numérica para comprobar el informe. 

El Analista lo genera mediante las herramientas comunes. Todas las cifras deben proceder de operaciones reproducibles y quedar acompañadas de la información necesaria para comprender cómo se obtienen.

### 21.2. Estructura obligatoria
El nivel principal del JSON debe contener los siguientes campos. Todos son obligatorios salvo  `extensions`, y no se admiten otros campos en este nivel.
| Campo | Tipo | Contenido |
| --- | --- | --- |
| `schema_version` | Texto | Versión del esquema: `1.0`. |
| `run_id` | Texto | Identificador de la ejecución. |
| `dataset_id` | Texto | `D0_piloto`, `D1_bike_sharing` o `D2_online_retail`. |
| `generated_at_utc` | Texto | Fecha y hora de generación en ISO 8601 y zona horaria UTC. |
| `profile` | objeto | Descripción del archivo original y de la copia preparada. |
| `preparation` | objeto | Resumen de las decisiones de preparación y de los cambios aplicados. |
| `analyses` | lista | Resultados de las comprobaciones de calidad, los análisis descriptivos, las agregaciones y las relaciones estudiadas. |
| `figures` | lista | Información de las figuras generadas y de los resultados que las respaldan. |
| `limitations` | lista de cadenas | Limitaciones del análisis o de los datos. |
| `extensions` | objeto opcional | Información adicional no utilizada por la evaluación común. |

#### Descripción de los datos: profile
`profile` debe tener esta estructura:
| Campo | Tipo | Contenido |
| --- | --- | --- |
| `original_rows` | entero no negativo | Número de filas del archivo original. |
| `original_columns` | entero positivo | Número de columnas del archivo original. |
| `prepared_rows` | entero no negativo | Número de filas de `prepared_data.csv`. |
| `prepared_columns` | entero positivo | Número de columnas de `prepared_data.csv`. |
| `unit_of_analysis` | cadena | Descripción de lo que representa una fila del dataset. |
| `columns` | lista | Descripción de todas las columnas de la copia preparada y de su relación con las originales. |

Cada elemento de `profile.columns` debe incluir:
- `name`: nombre de la columna en la copia preparada.
- `origin`: `source` si procede de una columna original o `derived` si se crea durante el análisis.
- `source_name`: nombre de origen o `null` si es derivada.
- `original_type`: tipo de dato observado en la columna original o `null` si es derivada.
- `prepared_type`: tipo de dato utilizado para el análisis.
- `missing_original`: número de valores ausentes en la columna original o `null` si es derivada.
- `missing_prepared`: número de valores ausentes en la columna preparada.
- `unique_prepared`: número de valores distintos en la columna preparada, o `null` si se justifica que no se ha calculado.

#### Decisiones de preparación: preparation
`preparation` debe contener `summary`, un texto breve que explique el criterio general de preparación, y `changes`, una lista de las transformaciones y decisiones adoptadas.

Cada elemento de `changes` debe incluir:
- `id`: identificador único de la transformación, con el formato `TR-NNN`, donde `NNN` es un número secuencial de tres dígitos (por ejemplo, `TR-001`).
- `action`: tipo de transformación o decisión.
- `description`: explicación de la operación realizada o de la decisión de conservar los datos sin cambios.
- `justification`: motivo de la decisión.
- `affected_columns`: lista de columnas afectadas.
- `rows_affected`: número de filas afectadas, o `null` si no puede determinarse.
- `before`: valor o resumen de la situación anterior, o `null` cuando no corresponda.
- `after`: valor o resumen de la situación posterior, o `null` cuando no corresponda.

#### Resultados analíticos: analyses
Cada elemento de `analyses` debe incluir:
- `id`: identificador `STAT-NNN`.
- `stage`: etapa a la que corresponde el resultado, entre `E1` y `E7`.
- `analysis_type`: tipo de cálculo o análisis.
- `title`: nombre comprensible del resultado.
- `variables`: lista de variables utilizadas.
- `population`: descripción de los datos utilizados, incluidos los filtros y las agrupaciones aplicados.
- `method`: operación estadística o procedimiento utilizado.
- `result`: resultado en formato JSON, que puede recoger un valor individual, una tabla o resultados por grupos.
- `interpretation`: explicación breve, sin formular conclusiones que excedan la evidencia disponible.

#### Registro de figuras: figures
Cada elemento de `figures` debe incluir:
- `id`: identificador único con el formato `FIG-NNN`.
- `file`: ruta relativa a la carpeta de la ejecución, como `figures/fig_001_demanda_horaria.png`.
- `title`: título visible de la figura.
- `objective`: pregunta que permite examinar o patrón que representa.
- `variables`: lista de variables utilizadas.
- `source_analysis_ids`: lista de identificadores `STAT-NNN` que respaldan la figura.

### 21.3. Reglas de validez
El archivo debe utilizar JSON válido, sin comentarios, claves duplicadas, valores `NaN` ni infinitos. Cuando un dato no esté disponible o no sea aplicable, se utiliza `null` únicamente si el campo lo permite y se explica el motivo. 

Los campos `schema_version`, `run_id` y `dataset_id` deben corresponder al esquema y a la ejecución actual.

Las dimensiones y los nombres de las columnas deben coincidir con los archivos correspondientes. Los identificadores deben ser únicos dentro de cada tipo de elemento, las referencias deben apuntar a resultados existentes y las figuras registradas deben corresponder a archivos generados durante la ejecución.

La estructura común no obliga a realizar idénticos análisis en todas las ejecuciones. El campo `result` permite representar soluciones analíticas diferentes sin perder la información necesaria para reproducirlas y evaluarlas.

## 22. `issues.json`

### 22.1. Finalidad y responsable
`issues.json` registra las comprobaciones de calidad y los problemas, riesgos o anomalías identificados por el Analista. Para cada caso distingue la evidencia disponible, la decisión adoptada y su posible efecto sobre el análisis.

La presencia de un valor extremo no basta para considerarlo un error: debe examinarse su contexto y justificarse el tratamiento aplicado.

### 22.2. Estructura obligatoria
El nivel principal del JSON debe contener exactamente los siguientes campos:
| Campo | Tipo | Contenido |
| --- | --- | --- |
| `schema_version` | Texto | Versión del esquema: `1.0`. |
| `run_id` | Texto | Identificador de la ejecución. |
| `dataset_id` | Texto | Identificador del dataset. |
| `checks_performed` | lista | Comprobaciones de calidad realizadas, aunque no detecten problemas. |
| `issues` | lista | Problemas, riesgos o anomalías respaldados por evidencia. |

Cada elemento de `checks_performed` debe incluir:
- `id`: identificador único con el formato `CHK-NNN`.
- `category`: aspecto de calidad comprobado.
- `description`: comprobación realizada.
- `outcome`: resumen del resultado.
- `evidence_ids`: lista de identificadores `STAT-NNN` relacionados.

Cada elemento de `issues` debe incluir:
- `id`: identificador con el formato `ISSUE-NNN`.
- `category`: categoría del problema: `missing`, `duplicate`, `type`, `category`, `range`, `identity`, `temporal`, `outlier` u `other`.
- `status`:  estado del problema: `detected`, `suspected`, `resolved`, `retained` o `unresolved`.
- `severity`:  importancia de su posible efecto sobre el análisis: `info`, `low`, `medium` o `high`.
- `title`: denominación breve del problema o riesgo.
- `description`: explicación del problema o riesgo.
- `evidence`: evidencia numérica o descriptiva que lo respalda.
- `affected_columns`: lista de columnas afectadas.
- `affected_row_count`: número de filas afectadas, o null si no puede determinarse.
- `sample_row_ids`: muestra de identificadores o posiciones de las filas afectadas. Puede ser una lista vacía.
- `decision`: decisión adoptada y criterio utilizado.
- `action`: actuación aplicada o recomendada.
- `potential_effect`: posible consecuencia sobre el análisis.
- `uncertainty`: dudas o limitaciones para interpretar el problema. Puede ser `null` cuando no corresponda.
- `evidence_ids`: lista de identificadores `STAT-NNN` de los resultados relacionados.

### 22.3. Reglas de validez
El archivo debe utilizar JSON válido, incluir los campos obligatorios y corresponder a la ejecución y al dataset actuales. Los identificadores deben ser únicos dentro de cada tipo de elemento y las referencias STAT-NNN deben existir en `statistics.json`.

`checks_performed` no puede estar vacío, porque debe quedar constancia de las comprobaciones de calidad realizadas. La lista `issues` puede estar vacía si esas comprobaciones no aportan evidencias de ningún problema.

No se deben inventar incidencias para completar el archivo ni omitir comprobaciones por haber obtenido un resultado sin problemas.

## 23. Directorio `figures/`

### 23.1. Finalidad y responsable
El directorio `figures/` contiene las visualizaciones creadas por el Analista mediante `execute_python`. Cada figura debe responder a una pregunta o ayudar a interpretar un resultado. No se exige una lista cerrada de gráficos ni se premia su cantidad.

La configuración establece un máximo de 12 figuras por ejecución, junto con límites de tamaño por archivo y para el conjunto. Estos máximos restringen el uso de recursos, pero no indican cuántas figuras necesita el análisis.

### 23.2. Formato obligatorio
Las figuras deben cumplir los siguientes requisitos:
- Guardarse como archivos PNG válidos y no vacíos.
- Utilizar nombres con el formato `fig_NNN_<descripcion_breve>.png`. La descripción utiliza letras sin tildes, números, guiones o guiones bajos, sin espacios.
- Disponer de un identificador `FIG-NNN` y de un registro correspondiente en `statistics.json`.
- Incluir título, ejes, unidades, leyendas y etiquetas cuando sean necesarios para interpretarlas.
- Aparecer insertadas o enlazadas en `report.md` mediante rutas relativas a la carpeta de la ejecución.
- Respetar los límites de cantidad y tamaño establecidos en la configuración.

Las capturas de tablas o de texto no sustituyen a las visualizaciones analíticas exigidas. El directorio debe contener al menos una figura PNG válida.

## 24. `report.md`

### 24.1. Finalidad y responsable
`report.md` presenta los resultados, las decisiones y las conclusiones del análisis. El Analista elabora su primera versión y puede modificarla durante la única corrección solicitada por el Revisor.

La capa común comprueba la estructura de la respuesta y guarda el informe, tanto en la intervención inicial como en la corrección. El Revisor no modifica directamente su contenido.

### 24.2. Estructura obligatoria
El documento debe incluir los siguientes encabezados de primer nivel, escritos con # y en este orden:
1. `# Resumen ejecutivo`.
2. `# Dataset y alcance`.
3. `# Inspección, calidad y preparación`.
4. `# Estadística descriptiva`.
5. `# Variables, agregaciones y relaciones`.
6. `# Visualizaciones y hallazgos`.
7. `# Problemas, riesgos y anomalías`.
8. `# Limitaciones e incertidumbres`.
9. `# Conclusiones`.

Las afirmaciones cuantitativas o verificables deben acompañarse de referencias próximas al texto que permitan localizar su respaldo:
- `[STAT-NNN]` para resultados de `statistics.json`.
- `[ISSUE-NNN]` para problemas o riesgos de `issues.json`.
- `[FIG-NNN]` para visualizaciones en `statistics.json`.

El informe debe incluir referencias a resultados estadísticos y a figuras. Las referencias a problemas se incorporan cuando corresponda.

Las figuras deben insertarse o enlazarse mediante su ruta relativa, como `figures/fig_001_demanda_horaria.png`. El informe debe distinguir los resultados calculados de sus interpretaciones y de las posibles explicaciones. No debe presentar asociaciones como relaciones causales ni utilizar información ajena a las entradas autorizadas.

### 24.3. Reglas de validez
El archivo debe ser legible, utilizar UTF-8, contener todas las secciones obligatorias con contenido y utilizar referencias que existan en los resultados de la ejecución.

El informe debe explicar el trabajo realizado en las ocho etapas y mantener la coherencia con las estadísticas, los problemas registrados y las figuras. La presencia de los encabezados no basta para cumplir estos requisitos si las secciones carecen de contenido analítico o contradicen las evidencias.

## 25. `trace.jsonl`

### 25.1. Finalidad y responsable
`trace.jsonl` conserva el registro cronológico de la ejecución. Incluye las intervenciones de los roles, las peticiones al modelo, las llamadas a herramientas, los errores, las validaciones, la decisión del Revisor, la posible corrección y el cierre.

La capa común genera y actualiza este archivo automáticamente. Los agentes no redactan ni modifican la traza.

### 25.2. Formato y contenido
El archivo utiliza el formato JSON Lines y la codificación UTF-8: cada línea contiene un objeto JSON que representa un evento. Se crea al preparar la ejecución y se actualiza a medida que esta avanza, conservando los eventos registrados aunque el flujo termine como `partial` o `failed`.

La traza debe permitir reconstruir:
- La identificación y la configuración de la ejecución.
- Las transiciones entre estados y las intervenciones de los roles.
- Las peticiones al modelo y el consumo comunicado por el proveedor.
- Las solicitudes y respuestas de las herramientas, sin incluir credenciales ni secretos.
- La duración de las operaciones, los errores, las advertencias y los reintentos.
- Los archivos generados y las comprobaciones de validación.
- La decisión del Revisor y los problemas señalados.
- La activación y el resultado de la corrección opcional.
- El estado final y el motivo de cierre.

La parte 5 del contrato, dedicada a la traza de ejecución, define los eventos que se registran, sus campos obligatorios y las comprobaciones de integridad. Las tres implementaciones utilizan ese mismo esquema para permitir el seguimiento y la comparación de las ejecuciones.

## 26. Responsabilidad sobre las salidas
La generación del contenido y su guardado se distribuyen de la siguiente forma:
| Salida | Quién genera el contenido | Cómo se guarda |
| --- | --- | --- |
| `plan.md` | Planificador | La capa común guarda su respuesta. |
| `prepared_data.csv` | Analista | Mediante `execute_python`. |
| `statistics.json` | Analista | Mediante `execute_python`. |
| `issues.json` | Analista | Mediante `execute_python`. |
| `figures/` | Analista | Mediante `execute_python`. |
| `report.md` | Analista | La capa común guarda su respuesta. |
| `trace.jsonl` | Capa común, a partir de los eventos de ejecución | Registro automático y progresivo. |

El Revisor no modifica ninguna salida. Sus decisiones y observaciones quedan registradas automáticamente en la traza.

Durante la corrección opcional, el Analista puede actualizar los resultados afectados por los problemas señalados y entregar una versión corregida del informe. El plan original se conserva y la traza registra la solicitud de corrección, las modificaciones y las validaciones realizadas.

La capa común guarda las respuestas de los roles sin completar ni modificar su contenido analítico. Si una respuesta incumple el formato exigido, se aplica el mecanismo de reparación previsto en el contrato, sin corregirla silenciosamente.

## 27. Validación conjunta y coherencia
La capa común realiza comprobaciones automáticas sobre las salidas y sus relaciones. Estas incluyen:
1. Presencia y tamaño de los archivos obligatorios.
2. Lectura del CSV y de los documentos Markdown.
3. Sintaxis válida de los archivos JSON y JSONL.
4. Comprobar que los campos `run_id` y `dataset_id`, cuando sean obligatorios, coincidan con los de la ejecución actual.
5. Coincidencia de las dimensiones y los nombres de las columnas entre `prepared_data.csv` y `statistics.json`.
6. Unicidad de los identificadores de cada tipo y existencia de los resultados a los que apuntan las referencias.
7. Comprobar que las figuras tengan el formato y tamaño permitidos, estén registradas en `statistics.json` y aparezcan insertadas o enlazadas en `report.md`, sin referencias a imágenes inexistentes.
8. Presencia de las etapas `E1` a `E8` en el plan y de las secciones obligatorias en el informe.
9. Comprobar si el Revisor ha solicitado una corrección que todavía no se ha realizado.
10. Conservación del archivo de entrada mediante la comprobación de su hash.

Las restricciones de escritura se aplican durante la ejecución de las herramientas para impedir que generen resultados fuera de las ubicaciones autorizadas.

Estas comprobaciones verifican requisitos técnicos y la coherencia básica entre archivos. No determinan por sí solas si las cifras son correctas o si el análisis es completo, ni asignan las puntuaciones Q1–Q10.

La validación final se combina con el estado del flujo, los límites alcanzados y la información de la revisión y la corrección para determinar si la ejecución termina como completed, partial o failed, según los criterios del apartado 16.

## 28. Condiciones comunes y libertad analítica
La estructura y los campos obligatorios de los archivos de salida deben ser iguales en las tres implementaciones. Ningún framework puede sustituirlos por un formato propio ni exigir campos adicionales exclusivos. La información específica de cada implementación puede registrarse en los campos previstos de la traza o en el campo opcional `extensions` de `statistics.json`, sin sustituir la información obligatoria ni aportar puntuación adicional.

El contrato establece cómo guardar y documentar los resultados, pero no exige obtener una conclusión determinada. Dentro del alcance establecido, el Analista puede elegir las técnicas, las transformaciones, las agrupaciones, las relaciones y las visualizaciones que considere adecuadas. Debe justificar sus decisiones y respaldar sus interpretaciones con los resultados obtenidos, reconociendo las limitaciones del análisis.

---

[← Parte 2](02_roles_coordinacion_y_finalizacion.md) · [Parte 4 →](04_herramientas.md)
