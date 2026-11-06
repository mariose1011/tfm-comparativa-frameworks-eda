# Parte 4. Herramientas y operaciones disponibles

**Contrato:** v1.0

[← Parte 3](03_archivos_y_esquemas.md) · [Parte 5 →](05_traza.md)

Esta parte define las cuatro herramientas comunes que permiten inspeccionar los datos, ejecutar el análisis y consultar o validar los resultados. Las tres implementaciones utilizan el mismo código para estas operaciones. Cada adaptador conecta las herramientas con su framework, manteniendo sus nombres, parámetros, comportamiento y formato de respuesta.

Se distingue entre las herramientas que solicita el modelo y las operaciones que realiza automáticamente la capa común, como guardar las respuestas o validar las salidas antes de la revisión. Estas operaciones no requieren una decisión del modelo y se aplican de la misma forma en las tres implementaciones.

## 29. Principios comunes de las herramientas
Las herramientas deben cumplir estas reglas:
1. Mantener los mismos nombres, parámetros y requisitos en los tres frameworks.
2. Recibir de la capa común la información que identifica la ejecución y delimita los accesos permitidos. El modelo no puede modificar el identificador de ejecución, el dataset asignado, las rutas autorizadas, la semilla experimental ni el rol activo.
3. Limitar el acceso a los datos al archivo de entrada autorizado, su documentación pública y los resultados permitidos de la ejecución actual, según las funciones de cada herramienta y los permisos del rol.
4. Guardar los resultados dentro del directorio exclusivo de la ejecución.
5. Aplicar controles para impedir el acceso a Internet, referencias privadas, credenciales, otras ejecuciones y archivos del proyecto ajenos a la tarea.
6. Devolver respuestas estructuradas e informar de los errores, sin ocultarlos ni inventar resultados para completar una operación fallida.
7. Registrar en la traza los parámetros recibidos, el resultado, la duración y los archivos afectados, sin incluir secretos.
8. No aplicar correcciones analíticas por iniciativa propia. Ejecutarán o comprobarán lo solicitado por el rol.
9. Utilizar una implementación y una versión común para los tres frameworks.
10. Limitar al adaptador las diferencias de integración exigidas por cada framework, sin alterar las operaciones disponibles ni sus restricciones.

## 30. Contexto y respuesta común

### 30.1. Información asociada a cada llamada
La capa común proporciona internamente la información necesaria para ejecutar cada llamada:
- Identificador de la ejecución: `run_id`.
- Identificador del dataset: `dataset_id`.
- Rol que solicita la herramienta.
- Ruta autorizada del archivo de entrada.
- Carpeta autorizada para los resultados.
- Semilla experimental común.
- Versión de la herramienta y de su configuración.

Estos datos no se ofrecen como parámetros que el modelo pueda modificar. El modelo solo puede indicar los argumentos definidos para cada herramienta. Las solicitudes de acceso a recursos no autorizados se rechazan.

### 30.2. Formato común de respuesta
Todas las herramientas deben devolver un objeto con los siguientes campos:
| Campo | Tipo | Contenido |
| --- | --- | --- |
| `tool_call_id` | Texto | Identificador único de la llamada. |
| `tool_name` | Texto | Nombre de la herramienta ejecutada. |
| `status` | Texto | `success` o `error`. |
| `data` | Objeto o `null` | Resultado de la operación. También puede conservar información parcial o de diagnóstico cuando se produce un error. |
| `error` | Objeto o `null` | Información del fallo, o `null` si la llamada termina correctamente. |
| `duration_ms` | Entero no negativo | Duración de la llamada en milisegundos, medida por la capa común. |

Cuando se produce un error, `error` debe incluir:
- `code` (código que identifica el tipo de fallo): `INVALID_ARGUMENT`, `ACCESS_DENIED`, `NOT_FOUND`, `EXECUTION_ERROR`, `TIMEOUT`, `OUTPUT_TOO_LARGE`, `SCHEMA_ERROR` o `INTERNAL_ERROR`.
- `message`: explicación del problema, sin revelar información privada.
- `retryable`: valor `true` o `false` que indica si repetir la operación podría resolver el fallo técnico. Este campo no autoriza un reintento ni modifica los límites establecidos.

Los límites de tamaño, tiempo, llamadas y reintentos se detallan en la parte 7 del contrato. El modelo no puede ampliarlos mediante los parámetros de las herramientas.

## 31. Herramienta `inspect_dataset`

### 31.1. Finalidad
Proporcionar una inspección inicial de solo lectura. Si el dataset y la configuración no cambian, la herramienta devuelve la misma información.

### 31.2. Roles autorizados
El Planificador es el único rol que puede solicitar esta herramienta. El resultado se calcula una vez por ejecución, se conserva y se entrega al Analista junto con el plan, sin repetir la llamada.

### 31.3. Parámetros
La llamada se realiza mediante `inspect_dataset({})` y no admite parámetros elegidos por el modelo. El archivo, la hoja de cálculo cuando corresponda, el tamaño de las muestras y la semilla utilizada proceden de la configuración común.

### 31.4. Respuesta específica
El campo `data` contiene:
- `dataset_id`: identificador del dataset.
- `file_format`: formato del archivo, `csv` o `xlsx`.
- `selected_sheet`: hoja utilizada en un libro Excel, o `null` en CSV.
- `rows`: número de filas.
- `columns`: número de columnas.
- `column_profile`: descripción ordenada de las columnas, con su nombre, posición, tipo de dato observado, número de valores presentes, número de ausencias y número de valores distintos.
- `head_sample`: primeras filas, según el tamaño configurado.
- `tail_sample`: últimas filas.
- `random_sample`: muestra seleccionada con la semilla común entre las filas no incluidas en las muestras anteriores.
- `public_documentation`: documentación pública autorizada del dataset, con su nombre, contenido y hash.
- `warnings`: advertencias detectadas durante la lectura o inspección. Puede ser una lista vacía.
- `source_sha256`: hash del archivo inspeccionado.

Las muestras tienen un tamaño limitado para evitar enviar el dataset completo al modelo. La herramienta lee los datos e identifica sus tipos, pero no aplica limpieza, imputaciones ni transformaciones analíticas y no modifica el archivo original. Tampoco decide qué resultados son relevantes para el análisis.

### 31.5. Fallos relevantes
La herramienta devuelve un error si el archivo no coincide con el tamaño o el hash registrados, no puede cargarse, sus dimensiones no coinciden con las previstas o no puede leerse la hoja configurada.

Si el fallo impide cargar el dataset autorizado, la ejecución no puede continuar con el análisis y se cierra como `failed`, según las reglas comunes de finalización.

## 32. Herramienta `execute_python`

### 32.1. Finalidad
Ejecutar el código Python propuesto por el Analista para preparar los datos, calcular estadísticas y generar visualizaciones y archivos de resultados. Es la única herramienta que permite ejecutar código producido por el modelo, sujeto a las restricciones del entorno experimental.

### 32.2. Roles autorizados
El Analista puede utilizar esta herramienta durante su intervención inicial y durante la corrección opcional. El Planificador y el Revisor no tienen acceso a ella.

### 32.3. Parámetros
La llamada debe incluir dos parámetros:
| Parámetro | Tipo | Regla |
| --- | --- | --- |
| `purpose` | Texto | Explicación breve de lo que se pretende calcular o generar. |
| `code` | Texto | Código Python completo que debe ejecutarse. |

Ambos campos son obligatorios y no pueden estar vacíos. La llamada no admite parámetros adicionales para cambiar los límites, instalar dependencias, proporcionar credenciales o habilitar conexiones.

### 32.4. Entorno de ejecución
Cada llamada se ejecuta en un proceso nuevo. Las variables y los resultados que permanecen únicamente en memoria no se conservan para la llamada siguiente. Para reutilizar un resultado, el Analista debe guardarlo en un archivo autorizado.

El entorno proporciona estas variables, que el código debe utilizar sin modificar:
- `INPUT_PATH`: ruta del dataset original.
- `OUTPUT_DIR`: carpeta de resultados de la ejecución.
- `FIGURES_DIR`: carpeta de figuras.
- `RUN_ID`: identificador de la ejecución.
- `DATASET_ID`: identificador del dataset.
- `EXPERIMENT_SEED`: semilla común.

La descripción de la herramienta informa al Analista de estas variables. El entorno proporciona la ubicación del dataset mediante la variable INPUT_PATH. El código debe utilizarla para abrir el archivo, en lugar de escribir o buscar su ruta.

El entorno incluye bibliotecas y utilidades de Python ya cargadas, que el Analista puede utilizar mediante los siguientes nombres:
 `pd`, `np`, `scipy`, `plt`, `sns`, `openpyxl`, `json`, `csv`, `math`, `statistics`, `datetime`, `decimal`, `itertools`, `random`, `re`, `warnings` y `Counter`. 

También se permiten importaciones compatibles con las restricciones del entorno. Las versiones de las dependencias se conservan en los archivos de requisitos.

El código puede leer el dataset original y los resultados autorizados de la ejecución actual. Puede generar o actualizar `prepared_data.csv`, `statistics.json`, `issues.json`, las imágenes dentro de `figures/` y los archivos temporales permitidos. No puede modificar el dataset de entrada ni escribir `plan.md`, `report.md` o `trace.jsonl`, que se gestionan desde la capa común.

Se prohíben las siguientes operaciones:
- Acceso a Internet o servicios externos.
- Instalar paquetes.
- Iniciar otros procesos o ejecutar comandos del sistema.
- Consultar variables de entorno o credenciales.
- Acceder a archivos ajenos a las rutas autorizadas.
- Solicitar información interactiva al usuario.
- Utilizar módulos de exploración del sistema y de rutas, como `os`, `pathlib` o `glob`.
- Utilizar funciones como `globals`, `locals`, `vars` para inspeccionar el entorno interno de ejecución, o acceder a nombres y atributos internos no autorizados.

Estas restricciones se aplican mediante comprobaciones del código y controles sobre funciones y accesos a archivos en Python.

### 32.5. Respuesta específica
El campo `data` contiene, cuando está disponible el resultado de la ejecución:
- `execution_id`: identificador de la ejecución de código.
- `exit_status`: `success`, `error` o `timeout`.
- `stdout`: texto producido por el código.
- `stderr`: mensajes de error o advertencia capturados.
- `truncated`: indica si se ha recortado alguna de las salidas de texto.
- `files_created`: archivos nuevos, con su ruta relativa, tamaño y hash SHA-256.
- `files_modified`: archivos actualizados, con esa misma información.

La herramienta ejecuta el código, pero no interpreta sus resultados ni incorpora automáticamente el texto de `stdout` a `statistics.json` o `issues.json`. El Analista debe guardar los resultados relevantes en los archivos correspondientes.

Un error no provoca una repetición automática oculta. Las nuevas llamadas quedan registradas y consumen los límites aplicables.

## 33. Herramienta `read_output`

### 33.1. Finalidad
Permitir que el Analista consulte sus resultados y que el Revisor examine las salidas de la ejecución actual, sin disponer de acceso general al sistema de archivos.

### 33.2. Roles autorizados
- Analista.
- Revisor.

### 33.3. Parámetros
La llamada debe incluir los cuatro campos siguientes, utilizando `null` en los que no correspondan a la consulta:
| Parámetro | Tipo | Regla |
| --- | --- | --- |
| `artifact` | Texto | Salida que se consulta: `plan`, `prepared_data`, `statistics`, `issues`, `figures` o `report`. |
| `query` | Texto | Tipo de consulta: `summary`, `full`, `id`, `section` o `next`. |
| `selector` | Texto o `null` | Elemento concreto que se quiere consultar, como STAT-001, FIG-002 o el encabezado Conclusiones. Se utiliza con `id` y `section`. |
| `cursor` | Texto o `null` | Código proporcionado por la herramienta para continuar una lectura dividida en fragmentos. Sen  utiliza con `next`. |

El modelo no proporciona rutas. La herramienta identifica el archivo a partir de `artifact`.

### 33.4. Consultas permitidas
Cada tipo de consulta tiene una función:
- `summary`: devuelve un resumen de la salida.
- `full`: solicita el contenido completo, dividido en fragmentos si supera el tamaño permitido.
- `id`: busca un elemento por su identificador.
- `section`: devuelve una sección de un documento Markdown.
- `next`: continúa una lectura dividida en fragmentos.

Las consultas disponibles dependen de la salida que se quiera leer:

| Salida | Consultas permitidas |
| --- | --- |
| `plan` y `report` | Resumen (`summary`), contenido completo (`full`), sección concreta (`section`) y continuación de una lectura (`next`). |
| `statistics` e `issues` | Resumen (`summary`), contenido completo (`full`), elemento por identificador (`id`) y continuación de una lectura (`next`). |
| `prepared_data` | Resumen y muestra de los datos (`summary`). |
| `figures` | Información del conjunto de figuras (`summary`) o de una figura concreta (`id`). |

Para consultar un resultado concreto, se utiliza query = "id" y se indica su identificador en `selector`, por ejemplo, "STAT-001". Para leer una sección del plan o del informe, se utiliza query = "section" y se escribe su encabezado en `selector`, por ejemplo, "Conclusiones". En ambos casos, cursor debe ser `null`.

Cuando el contenido no cabe en una sola respuesta, la herramienta lo divide en fragmentos y devuelve en `next_cursor` un código para continuar la lectura. La siguiente consulta debe mantener el mismo artifact, utilizar query = "next" y copiar ese código en cursor, con `selector` = `null`. Si la respuesta contiene next_cursor = `null`, no quedan fragmentos por leer.

Las consultas de resumen (`summary`) y contenido completo (`full`) no necesitan seleccionar un elemento ni continuar una lectura anterior, por lo que `selector` y `cursor` deben ser null.

La consulta de `figures` devuelve información sobre los archivos y su registro en `statistics.json`, pero no muestra las imágenes al modelo. El Revisor puede comprobar su existencia y su relación con las estadísticas y el informe, mientras que la legibilidad y la calidad visual se evalúan posteriormente, fuera del flujo de agentes.

### 33.5. Respuesta específica
El campo `data` contiene:
- `artifact`: salida consultada.
- `query`: tipo de consulta aplicada.
- `content_type`: tipo de contenido devuelto: `markdown`, `json`, `table_summary` o `figure_metadata`.
- `content`: texto, objeto o lista con la información solicitada.
- `sha256`: hash del archivo consultado, o `null` para un directorio.
- `truncated`: indica si la respuesta se ha dividido por tamaño.
- `next_cursor`: valor para solicitar el siguiente fragmento, o `null` si no quedan fragmentos.

Para un mismo contenido y una misma configuración, el orden y el tamaño de los fragmentos se mantienen. La herramienta solo permite consultar, no modifica los archivos ni corrige referencias inválidas.

## 34. Herramienta `validate_outputs`

### 34.1. Finalidad
Comprobar mediante reglas automáticas la presencia, la estructura y la coherencia básica de los seis archivos y la carpeta de figuras definidos en la parte 3. La herramienta no evalúa la calidad analítica ni asigna puntuaciones Q1–Q10.

### 34.2. Roles autorizados
- Analista.
- Revisor.

La capa común también ejecuta la validación automáticamente antes del Revisor y durante el cierre. La traza distingue estas comprobaciones de las solicitadas por el modelo.

### 34.3. Parámetros
La llamada se realiza mediante `validate_outputs({})`, sin parámetros elegidos por el modelo.

### 34.4. Respuesta específica
El campo `data` contiene:
- `validation_id`: identificador de la validación.
- `validation_status`: resultado general de la comprobación
    - `valid`: las salidas cumplen las comprobaciones técnicas aplicadas.
    - `incomplete`: faltan salidas obligatorias y no se detectan otros errores que determinen un resultado `invalid`.
    - `invalid`:  alguna salida presente incumple los requisitos o se detectan errores en las comprobaciones entre archivos.
- `artifacts`: información de cada salida, incluido su nombre, existencia, tamaño, posibilidad de lectura, cumplimiento de la estructura exigida, hash cuando corresponda, errores y advertencias.
- `cross_checks`: resultados de las comprobaciones entre archivos, como la coincidencia de dimensiones, la existencia de las referencias y la correspondencia de las figuras.
- `pending_correction`: indica si el Revisor ha solicitado una corrección que todavía no se ha realizado.
- `error_count`: número de errores detectados.
- `warning_count`:  número de advertencias.
- `summary`: explicación breve del resultado de la validación.

Una advertencia no invalida por sí sola las salidas. El resultado de esta herramienta tampoco determina por sí solo si la ejecución termina como `completed`, `partial` o `failed` : el cierre considera además el desarrollo del flujo y los límites alcanzados, según el apartado 16.

La herramienta no corrige los archivos analíticos. Devuelve las incidencias detectadas y registra la validación en la traza.

## 35. Operaciones automáticas de la capa común
La capa común realiza las siguientes operaciones sin que el modelo tenga que solicitarlas como herramientas:
1. Verificar las entradas y preparar la carpeta exclusiva de la ejecución.
2. Comprobar la estructura de la respuesta del Planificador y guardarla como `plan.md`.
3. Comprobar la respuesta inicial del Analista y guardarla como `report.md`.
4. Durante la corrección, extraer el informe del bloque `REPORT_MD`, comprobarlo y actualizar `report.md`.
5. Crear y actualizar progresivamente `trace.jsonl`.
6. Calcular y registrar los hashes de los archivos correspondientes.
7. Realizar la validación previa al Revisor y la validación final.
8. Determinar y registrar el estado final y cerrar la traza.

El formato de las respuestas de los roles, incluido el informe actualizado tras la corrección, se detalla en la parte 6 del contrato. Cuando se modifica una salida, la traza conserva los hashes que identifican su versión anterior y la nueva.

La capa común no completa ni corrige el contenido analítico de las respuestas. Si una respuesta incumple el formato exigido, registra el error y se aplica el procedimiento de reparación previsto en el contrato, que solicita al mismo rol que presente de nuevo el contenido con la estructura requerida.

El guardado de `plan.md` y `report.md` se realiza automáticamente a partir de las respuestas de los roles, siguiendo el mismo procedimiento en las tres implementaciones.

## 36. Matriz de permisos
| Operación | Planificador | Analista | Revisor | Función de la capa común |
| --- | --- | --- | --- | --- |
| Solicitar `inspect_dataset` | Sí | No | No |Ejecuta la inspección y conserva su resultado. |
| Solicitar `execute_python` | No | Sí | No | Ejecuta el código en un proceso separado. |
| Solicitar `read_output` | No | Sí | Sí | Lee únicamente las salidas autorizadas. |
| Solicitar `validate_outputs` | No | Sí | Sí | Realiza la comprobación, también la ejecuta automáticamente antes de la revisión y al cierre. |
| Generar el contenido de `plan.md` | Sí | No | No | Comprueba su estructura y lo guarda. |
| Generar el contenido de `report.md` | No | Sí | No | Comprueba su estructura y lo guarda. |
| Escribir `trace.jsonl` | No | No | No | Registra automáticamente los eventos. |

## 37. Secuencia operativa común
El recorrido ordinario sigue estos pasos:
1. La capa común comprueba la configuración y la identidad del dataset, prepara la carpeta de resultados e inicia la traza.
2. El Planificador solicita la inspección inicial y elabora el plan.
3. La capa común comprueba la estructura de su respuesta y guarda `plan.md`.
4. El Analista recibe el plan y la inspección inicial. Utiliza las herramientas autorizadas para realizar el análisis, consultar los archivos y comprobar las salidas.
5. La capa común comprueba y guarda el informe del Analista y realiza la validación previa.
6. El Revisor recibe el resultado de esa validación y puede consultar las salidas mediante `read_output` y `validate_outputs`.
7. El sistema registra su decisión. Si solicita una corrección, el Analista recibe los problemas señalados y los resultados disponibles para modificar únicamente lo necesario.
8. Si hay corrección, la capa común guarda el informe actualizado. Después realiza la validación final, determina el estado de la ejecución y cierra la traza.

Los errores o límites que interrumpen este recorrido se gestionan conforme a las reglas de cierre del apartado 16. Los máximos de llamadas y recursos se detallan en la parte 7 del contrato.

## 38. Aislamiento, errores y reproducibilidad
Las restricciones de acceso se aplican mediante comprobaciones de rutas, permisos y operaciones, además de las instrucciones recibidas por los roles. Cada llamada a `execute_python` utiliza un proceso nuevo y cada ejecución dispone de una carpeta propia, sin reutilizar los resultados de otras ejecuciones.

Cuando el código realiza operaciones basadas en el azar, debe utilizar `EXPERIMENT_SEED` para que puedan repetirse. Si una biblioteca requiere una semilla específica, esta debe obtenerse a partir de ese valor común. Las versiones de Python y de las dependencias se documentan en los archivos del entorno. La configuración y la traza identifican las versiones de los componentes del experimento.

Los errores permanecen registrados aunque una operación posterior los resuelva. Los intentos adicionales deben respetar los límites y quedar reflejados en la traza. No se permiten reintentos ocultos, cambios silenciosos de archivos ni sustituciones del modelo.

Si la respuesta de una herramienta supera el tamaño permitido, se devuelve el error `OUTPUT_TOO_LARGE`. El rol puede reformular la operación dentro de sus permisos y del presupuesto restante. Los demás excesos de tamaño o recursos se tratan según el límite afectado.

## 39. Equivalencia entre frameworks
LangGraph, CrewAI y Microsoft Agent Framework pueden utilizar mecanismos diferentes para ofrecer las herramientas al modelo y gestionar sus solicitudes, pero deben ejecutar las mismas funciones de la capa común.

En la integración de herramientas, cada adaptador se encarga de:
- Convertir la solicitud del framework al formato común, sin cambiar los argumentos elegidos por el modelo.
- Asociar la llamada con el rol y la ejecución correspondientes.
- Entregar la respuesta común al modelo mediante el formato requerido por su framework.
- Registrar los datos técnicos necesarios para relacionar la llamada con su respuesta y con la traza.

El adaptador no puede añadir herramientas, ampliar la información devuelta, corregir silenciosamente los argumentos ni conceder accesos adicionales.

Las adaptaciones que puedan afectar al comportamiento se documentan y comprueban durante el piloto.

---

[← Parte 3](03_archivos_y_esquemas.md) · [Parte 5 →](05_traza.md)
