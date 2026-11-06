# Parte 5. Traza común de la ejecución

**Contrato:** v1.0

[← Parte 4](04_herramientas.md) · [Parte 6 →](06_prompts_comunes.md)

Esta parte define la información que se registra en `trace.jsonl` y el formato de sus eventos. La traza permite reconstruir el desarrollo de cada ejecución y obtener las métricas de proceso P1–P14.

La capa común genera este registro automáticamente a partir de las operaciones realizadas. No depende de una descripción elaborada por el modelo ni del formato de registro propio de cada framework.

## 40. Finalidad y autoridad de la traza
La traza deberá permitir:
- Reconstruir el orden de las intervenciones de los roles, las peticiones al modelo, las llamadas a herramientas, las validaciones y la generación de archivos.
- Obtener las duraciones, el consumo de tokens, el coste estimado y los recuentos de llamadas, errores, reintentos y límites alcanzados.
- Comprobar si se realiza la corrección opcional y qué archivos se modifican.
- Identificar la configuración y las versiones utilizadas.
- Examinar las diferencias entre ejecuciones sin depender de las interfaces de seguimiento de cada framework.
- Conservar la información registrada aunque la ejecución termine como `partial` o `failed`.

La traza común es la fuente principal para calcular las métricas de proceso. Los registros propios de los frameworks y los identificadores de las peticiones de OpenAI se utilizan como apoyo para investigar incidencias.

## 41. Formato y escritura del archivo      
`trace.jsonl` utiliza JSON Lines y codificación UTF-8: cada línea contiene un objeto JSON completo que describe un evento. El archivo se crea al preparar la ejecución y se actualiza a medida que esta avanza.

La escritura debe respetar estas reglas:
1. El primer evento es `run_started`. Si la ejecución puede cerrarse de forma controlada, el último es trace_closed.
2. El campo `sequence` comienza en 1 y aumenta de uno en uno, sin repeticiones ni saltos.
3. Los eventos ya escritos no se modifican ni se eliminan. Las incidencias y aclaraciones posteriores se registran mediante nuevos eventos.
4. Cada evento incluye la fecha y hora en UTC y el tiempo transcurrido desde el inicio de la ejecución.
5. Solo se registran operaciones o solicitudes que hayan ocurrido realmente.
6. Cada llamada iniciada debe contar con un evento que indique cómo termina, salvo que una interrupción inesperada impida registrarlo.
7. Los datos no disponibles se representan mediante `null` cuando el campo lo permita. No se inventan valores ni se sustituyen por estimaciones, excepto en los campos definidos expresamente para ello.
8. El orden de los campos dentro de cada objeto JSON puede variar, pero deben respetarse sus nombres, tipos y valores permitidos.

## 42. Campos comunes de los eventos
Todos los eventos deben incluir los siguientes campos. Los detalles particulares de cada operación se guardan dentro de payload.
| Campo | Tipo | Contenido |
| --- | --- | --- |
| `schema_version` | Texto | Versión del formato de la traza: `1.0`. |
| `event_id` | Texto | Identificador único del evento, formado por `run_id` y su número de secuencia. |
| `sequence` | Entero positivo | Número de orden del evento en la traza, comenzando en 1. |
| `timestamp_utc` | Texto | Fecha y hora del evento en formato ISO 8601, en UTC y con milisegundos. |
| `elapsed_ms` | Entero no negativo | Milisegundos transcurridos desde el inicio de la traza. |
| `run_id` | Texto | Identificador de la ejecución. |
| `framework` | Texto | `langgraph`, `crewai` o `microsoft_agent_framework`. |
| `dataset_id` | Texto | `D0_piloto`, `D1_bike_sharing` o `D2_online_retail`. |
| `repetition` | Entero positivo | Número de repetición de la combinación de framework y dataset. |
| `phase` | Texto | Fase de la ejecución: `setup`, `planning`, `analysis`, `review`, `correction`, `final_validation` o `closure`. |
| `role` | Texto | Rol asociado al evento: `runtime`, `planner`, `analyst` o `reviewer`. |
| `source` | Texto | Componente al que corresponde el evento: `common_runtime`, `framework_adapter`, `model` o `tool`. |
| `event_type` | Texto | Tipo de evento, según el catálogo del apartado 43. |
| `correlation_id` | Texto o `null` | Identificador que permite agrupar eventos de una misma operación. |
| `parent_event_id` | Texto o `null` | Identificador del evento previo que da lugar al actual, cuando corresponde. |
| `payload` | objeto | Datos específicos del evento, como los argumentos de una llamada, su resultado o el consumo registrado. |

`correlation_id` permite reunir los eventos relacionados con una operación, mientras que `parent_event_id` señala una relación directa entre dos eventos. Por ejemplo, el evento que registra el resultado de una llamada a herramienta puede señalar como origen el evento de inicio de esa llamada.

El valor de `framework` identifica la implementación utilizada, pero no cambia el formato de la traza. Para calcular duraciones se utiliza principalmente `elapsed_ms` y `timestamp_utc`, que permiten situar los eventos en el tiempo y contrastarlos con otros registros.

## 43. Tipos de eventos permitidos
El campo `event_type` debe utilizar uno de los siguientes valores:
| Grupo | Eventos |
| --- | --- |
| Ejecución | `run_started`, `run_finished`, `trace_closed` |
| Flujo | `state_transition`, `role_started`, `role_finished`, `role_failed` |
| Modelo | `model_call_started`, `model_call_finished`, `model_call_failed` |
| Herramientas | `tool_call_started`, `tool_call_finished`, `tool_call_failed` |
| Resultados | `artifact_written`, `validation_completed` |
| Revisión | `review_decision`, `correction_started`, `correction_finished` |
| Incidencias | `error_recorded`, `retry_recorded`, `limit_warning`, `limit_reached` |

`run_finished` registra el resultado final de la ejecución, mientras que `trace_closed` deja constancia del cierre de la traza y de las comprobaciones de su integridad.

Los tres frameworks deben utilizar estos mismos tipos de eventos. Si es necesario conservar información técnica adicional, puede incluirse en el campo opcional `extensions`, dentro de `payload`, sin sustituir los campos obligatorios.

## 44. Eventos de ejecución y flujo

### 44.1. `run_started`
Este evento se registra una sola vez, al iniciar la traza. Identifica las condiciones de la ejecución e incluye:
- Versiones del contrato, la traza, los prompts, las herramientas y los esquemas de salida.
- Versión del framework, de Python y de las dependencias.
- Proveedor, modelo solicitado, API, modalidad de servicio, esfuerzo de razonamiento y parámetros del modelo.
- Hash del dataset y versión del registro que identifica los conjuntos de datos.
- Rutas relativas y hashes de la documentación pública utilizada.
- Semilla experimental.
- Versión de los límites e identificador de la tabla de precios.
- Tarifas por categoría de tokens, moneda, fecha de consulta y fuente.
- Hash de la configuración y hashes de los prompts.
- `started_at_utc`: fecha y hora de inicio.

No debe incluir credenciales, valores de variables de entorno ni rutas absolutas del equipo. Los archivos se identifican mediante rutas relativas autorizadas o identificadores.

### 44.2. `state_transition`
Registra un cambio de estado de la ejecución. Contiene:
- `from_state`: estado anterior o `null` cuando no corresponde.
- `to_state`: nuevo estado.
- `reason`: motivo del cambio.
- `trigger_event_id`:  identificador del evento que provoca la transición, o `null` cuando no se establece esa relación.

Las transiciones deben respetar el recorrido y las reglas de cierre definidos en la parte 2.

### 44.3. `role_started`, `role_finished` y `role_failed`
Estos eventos registran el inicio y el resultado de cada intervención de un rol. Comparten:
- `role_execution_id`:  identificador de la intervención.
- `role_name`: `planner`, `analyst` o `reviewer`.
- `attempt`: comienza en 1 para la intervención inicial del rol y en 2 para la corrección del Analista. Si se solicita una reparación de formato, este valor aumenta en 1.

`role_started`incluye además `started_at_utc`, con la fecha y hora de inicio.

`role_finished` y `role_failed` incluyen:
- `finished_at_utc`: fecha y hora de finalización.
- `duration_ms`: duración en milisegundos.
- `outcome`: `success`, si la intervención termina correctamente o `failed` si falla.
- `output_artifact`: archivo producido, como `plan.md` o `report.md`, o `null` cuando no corresponde.
- `error_id`: identificador del error asociado, o `null` si no existe.

La intervención inicial utiliza `attempt: 1` y la corrección del Analista comienza con `attempt: 2`. Una corrección de formato incrementa también este valor. Por ello, para distinguir una corrección de un reintento deben consultarse la fase y los eventos relacionados, no únicamente `attempt`.

La corrección mantiene role_name = "analyst" y se realiza en la fase correction.

### 44.4. `run_finished`
Este evento se registra una vez durante el cierre controlado de la ejecución. Contiene:
- `final_status`: `completed`, `partial` o `failed`.
- `reason_code`: código del motivo de finalización.
- `reason`: explicación de ese motivo.
- `started_at_utc`, `finished_at_utc` y `duration_ms`: inicio, final y duración de la ejecución.
- `final_validation_id`: identificador de la validación final.
- `totals`: resumen de peticiones al modelo, tokens, coste estimado, llamadas a herramientas, errores, reintentos y demás contadores comunes.
- `correction_used`: indica si se utiliza la corrección opcional. 
- `correction_request_id`: identificador de la solicitud de corrección, o `null` si no existe.
- `limits_reached`: límites alcanzados.
- `artifacts`: estado de las salidas, con su tamaño, validez de estructura y hash cuando corresponde.

Los totales proceden de los contadores de la capa común y deben ser coherentes con los eventos registrados. Si se detecta una discrepancia, se investiga y documenta antes de utilizar la medida afectada.

Si el dataset se ha cargado pero `report.md` está ausente o no supera la validación mínima, se asigna `final_status = "failed"` con el código `REPORT_MISSING_OR_INVALID`.

Una interrupción que impida realizar el cierre puede dejar la traza sin este evento.

### 44.5. `trace_closed`
Es el último evento de una traza cerrada de forma controlada. Contiene:
- `event_count`: número total de eventos, incluido el propio cierre.
- `last_sequence`: número de orden del último evento.
- `events_by_type`: número de eventos de cada tipo.
- `integrity_status`: `valid`, `incomplete` o `invalid`, según las comprobaciones de integridad.
- `required_fields_expected`: número de campos obligatorios esperados.
- `required_fields_valid`: número de campos obligatorios presentes.
- `required_fields_missing_or_invalid`: número de campos obligatorios ausentes.
- `failed_integrity_checks`: comprobaciones de integridad que no se cumplen.

Este evento no contiene el hash final del propio `trace.jsonl`, porque añadirlo modificaría el archivo y cambiaría su hash. Para identificar la traza completa, el hash se calcula después del cierre y se conserva en un registro externo.

## 45. Llamadas al modelo, tokens y coste

### 45.1. `model_call_started`
Registra el inicio de un intento de petición al proveedor. Contiene:
- `model_call_id`: identificador de la petición.
- `role_execution_id`: intervención del rol a la que pertenece.
- `attempt`: número de intento.
- `retry_of`: identificador de la petición que se repite, o `null` si no es un reintento.
- Proveedor, modelo, API y modalidad de servicio solicitados.
- Esfuerzo de razonamiento y parámetros activos.
- Versión y hash del prompt del rol.
- Número de mensajes y herramientas incluidos.
- `visible_messages`: mensajes enviados, representados en un formato común y sin información sensible. 
- `tool_schema_sha256`: hash de las definiciones de herramientas enviadas.
- `provider_request_id`: identificador del proveedor, si ya está disponible.

El registro de mensajes permite revisar las instrucciones y el contexto de la petición. Debe excluir credenciales, cabeceras de autenticación y razonamiento interno no visible. Cuando un contenido se representa mediante una referencia, esta debe permitir localizarlo y comprobar su identidad.

La presencia de `model_call_started` no demuestra por sí sola que el proveedor haya recibido o procesado la petición, ya que el intento puede fallar durante la conexión.

### 45.2. `model_call_finished`
Registra la respuesta recibida del modelo. Contiene:
- `model_call_id` y `provider_response_id`: identificadores de la petición y de la respuesta.
- `reported_service_tier`: modalidad de servicio informada por el proveedor, cuando está disponible.
- `outcome`: resultado registrado por el adaptador. Las implementaciones utilizan `success` cuando procesan la respuesta sin una excepción.
- `finish_reason`: motivo por el que termina la respuesta del modelo, cuando está disponible.
- `visible_output`: Contenido visible devuelto por el modelo.
- `requested_tool_calls`: herramientas solicitadas, con sus identificadores, nombres y argumentos.
- `input_tokens`, `output_tokens` y `total_tokens`: consumo de tokens.
- `cached_input_tokens`: tokens de entrada recuperados de caché.
- `reasoning_output_tokens`: tokens de razonamiento comunicados por el proveedor.
- `usage_extensions`: información adicional, como el modelo comunicado por el proveedor y otros detalles del consumo.
- `estimated_cost`: importe estimado de la petición.
- `started_at_utc`, `finished_at_utc` y `duration_ms`: inicio, final y duración.

El valor `success` indica que se ha procesado una respuesta, no que su contenido sea correcto o cumpla el contrato. Esa comprobación se realiza posteriormente.

El consumo de tokens se obtiene de la información proporcionada por el proveedor. El coste se calcula con las tarifas fijadas para el experimento, diferenciando los tokens de entrada no recuperados de caché, los recuperados de caché y los de salida. La moneda y las tarifas quedan identificadas en `run_started`.

### 45.3. `model_call_failed`
Registra un intento de petición que termina con un error. Contiene:
- `model_call_id`: identificador de la petición.
- `provider_request_id` y `provider_response_id`: identificadores del proveedor, cuando existen.
- `duration_ms`: duración del intento.
- `error_id`: referencia al error registrado.
- `partial_usage`: información de consumo disponible pese al fallo, o `null`.
- `retry_planned`: indica si se prevé un reintento.

El intento fallido se incluye en el recuento de peticiones y su error se contabiliza una sola vez.

### 45.4. Recuento común de peticiones
El número de peticiones al modelo se obtiene contando los eventos `model_call_started`, incluidos los intentos fallidos y los reintentos.

Este recuento no utiliza el número de mensajes internos de cada framework, porque una petición puede incluir varios mensajes y cada integración puede organizarlos de forma diferente.

## 46. Herramientas, errores y reintentos

### 46.1. `tool_call_started`
Registra el inicio del procesamiento de una solicitud de herramienta. Contiene:
- `tool_call_id`: identificador de la llamada.
- `tool_name`: nombre de la herramienta.
- `model_call_id`: petición del modelo que solicita la operación.
- `role_execution_id`: intervención del rol correspondiente.
- `arguments`: argumentos recibidos.
- `attempt`: número de intento.
- `retry_of`: llamada anterior que se repite, o `null`.
- `tool_version`: versión de la herramienta.

Cada evento tool_call_started se incluye en el recuento de llamadas a herramientas. Si la solicitud se rechaza por argumentos incorrectos o falta de permisos, se registra como fallida con `INVALID_ARGUMENT` o `ACCESS_DENIED`, aunque la operación sobre los datos no llegue a ejecutarse.

Este recuento incluye únicamente las llamadas solicitadas por el modelo. Las validaciones que la capa común realiza automáticamente antes de la revisión y al cierre se registran por separado y no se suman.

### 46.2. `tool_call_finished` y `tool_call_failed`
Registran cómo termina una llamada a herramienta. Contienen:
- `tool_call_id`, `tool_name` y `duration_ms`.
- `outcome`: resultado de la llamada, como `success`, `error` o `timeout`.
- `response`: respuesta estructurada definida en la Parte 4.
- `affected_files`: archivos creados o modificados, con sus rutas relativas, tamaños y hashes.
- `error_id`: identificador del error, o `null`.
- `retry_planned`: indica si se prevé repetir la operación.

Una llamada se considera ejecutada correctamente cuando termina con `tool_call_finished` y `outcome = "success"`. Una llamada que produce resultados parciales pero termina con un error no cuenta como éxito.

### 46.3. `error_recorded`
Cada error registrado dispone de un identificador `error_id`. El evento contiene:
- `category`: categoría del error: `model`, `tool`, `code`, `format`, `framework` o `environment`.
- `code`: código del error.
- `message`: explicación sin información sensible.
- `severity`: `warning`, `recoverable` o `fatal`.
- `related_event_id`: evento relacionado con el problema.
- `operation`: operación afectada.
- `retryable`: indica si un reintento podría resolver el fallo.
- `retry_triggered`: indica si se activa un reintento.
- `exception_type`: tipo de excepción, cuando está disponible.
- `technical_trace`: detalles técnicos del error, sin información sensible, cuando están disponibles.

Las advertencias también se registran mediante `error_recorded`, con `severity = "warning"`, pero se contabilizan por separado. P9 cuenta únicamente los identificadores únicos cuya gravedad sea distinta de warning.

Los eventos de llamadas fallidas deben remitir al mismo `error_id` del problema que describen, para no contabilizarlo dos veces.

### 46.4. `retry_recorded`
Registra un intento adicional autorizado tras un fallo. Contiene:
- `retry_id`: identificador del reintento.
- `target_type`: tipo de operación que se repite. Las implementaciones utilizan `model_call` para las peticiones al modelo y `role_output` para la reparación del formato de una respuesta.
- `failed_operation_id`: identificador de la operación fallida.
- `new_operation_id`: identificador del nuevo intento, cuando se conoce.
- `reason`: motivo del reintento.
- `attempt`: número del nuevo intento.
- `authorized`: indica si el reintento está permitido por los límites comunes.

Un reintento es la repetición de una llamada o intervención después de un error técnico, de formato o de ejecución, y queda identificado como tal en la traza. La corrección solicitada por el Revisor se registra por separado, porque permite modificar los resultados analíticos y no se limita a resolver un fallo técnico o de formato.

### 46.5. `limit_warning` y `limit_reached`
Estos eventos registran los avisos y bloqueos relacionados con los límites. Contienen:
- `limit_type`:  límite afectado, como tiempo, tokens, peticiones al modelo, llamadas a herramientas, reintentos, tiempo de Python o coste.
- `configured_value`: valor establecido.
- `unit`: unidad de medida.
- `observed_value`: valor registrado al realizar la comprobación.
- `scope`: ámbito al que se aplica, como petición, rol o ejecución.
- `action`: actuación adoptada, como emitir una advertencia o bloquear una nueva operación.

`limit_warning` informa de la proximidad a un límite y no implica por sí solo detener el flujo.

`limit_reached` registra que un límite impide continuar una operación y sirve para identificar los límites alcanzados. El bloqueo puede ser preventivo: una petición puede rechazarse porque su consumo previsto supera el margen disponible, aunque el consumo acumulado todavía esté por debajo del máximo.

## 47. Resultados, validación, revisión y corrección

### 47.1. `artifact_written`
Este evento registra el guardado o la modificación de un archivo de resultados. Debe incluir:
- `artifact_name`: nombre del archivo.
- `relative_path`: ruta relativa a la carpeta de la ejecución.
- `writer`: responsable del contenido, identificado como `planner`, `analyst` o `common_runtime`.
- `phase_written`: `initial` o `correction`, según el momento en que se guarda.
- `bytes`, `sha256` y `format`: tamaño, hash y formato del archivo.
- `replaces_sha256`: hash de la versión anterior, o `null` si no sustituye un archivo existente.
- `origin_event_id`: identificador del evento relacionado con la generación del contenido.

Cada archivo creado o modificado se registra por separado, incluidas las figuras.

### 47.2. `validation_completed`
Este evento recoge el resultado de una comprobación realizada mediante `validate_outputs`. Debe incluir:
- `trigger`:  indica si la validación corresponde al Analista (`analyst`), al Revisor (`reviewer`), a la comprobación previa a la revisión (`pre_review`) o a la validación final (`final`).
- `automatic`: indica si la validación se realiza como parte del flujo de la capa común (true) o responde a una solicitud del modelo (false).
- `validation_id`: identificador de la validación.
- `validation_status`: resultado general de la comprobación.
- `response`: respuesta completa de la herramienta.

Las validaciones automáticas se registran, pero no se incluyen en el recuento de llamadas a herramientas solicitadas por el modelo.

### 47.3. `review_decision`
Este evento registra la decisión del Revisor y los problemas en los que se basa. Debe incluir:
- `review_decision_id`: identificador de la decisión
- `decision`: `approved`, `correction_required` o `cannot_review`.
- `summary`: explicación breve de la decisión.
- `findings`: lista de problemas identificados.
- `correction_allowed`: indica si la corrección está permitida.
- `correction_requested`: indica si el Revisor solicita utilizarla.
- `reviewed_artifact_hashes`: hashes que identifican las versiones de los resultados disponibles para la revisión.

Cada problema de findings debe indicar su identificador (`finding_id`), categoría, gravedad, descripción, archivos o resultados afectados, evidencias y condición que debe cumplirse para considerarlo corregido.

### 47.4. `correction_started` y `correction_finished`
`correction_started` registra el comienzo de la corrección del Analista. Incluye el identificador de la solicitud, los problemas que debe atender, los archivos que pueden verse afectados y los hashes de los resultados antes de la corrección.

`correction_finished` recoge:
- `correction_request_id`: identificador de la solicitud.
- `outcome`: `success` si el Analista no declara problemas pendientes, o `partial` si declara alguno sin resolver.
- `declared_changes`: cambios que el Analista indica haber realizado.
- `modified_files`: lista de archivos modificados.
- `post_validation_id`: identificador de la validación posterior.
- `addressed_findings` y `unresolved_findings`: problemas que el Analista declara atendidos y pendientes, respectivamente.

Los hashes anteriores y posteriores de los archivos modificados se consultan en los eventos `artifact_written`.

Estos registros permiten comprobar si se utiliza la corrección y qué archivos cambian, pero no garantizan que los problemas estén realmente resueltos.

## 48. Cálculo de las métricas de ejecución
La siguiente tabla relaciona cada métrica con los eventos utilizados para calcularla. Los códigos P1 a P14 identifican las medidas y no son campos de la traza.

| Métrica | Fuente y cálculo|
| --- | --- |
| P1. Estado de la ejecución | Se obtiene de `final_status` en `run_finished`. Los valores `completed`, `partial` y `failed` corresponden a los criterios técnicos de finalización definidos en el contrato. |
| P2. Duración | Se obtiene de `duration_ms` en `run_finished` y comprende el tiempo desde el inicio hasta la finalización o interrupción controlada. |
| P3. Tokens de entrada | Suma de los tokens de entrada informados en las respuestas del modelo. |
| P4. Tokens de salida | Suma de los tokens de salida informados en las respuestas del modelo. |
| P5. Tokens totales | Suma de los tokens totales informados. Los tokens recuperados de caché y los de razonamiento no se añaden de nuevo, porque ya forman parte de las categorías correspondientes. |
| P6. Coste | Suma del coste estimado de las peticiones mediante las tarifas fijadas para el experimento. |
| P7. Llamadas a herramientas | Número de eventos `tool_call_started` y distribución por herramienta. No incluye las validaciones automáticas de la capa común. |
| P8. Éxito de las herramientas | Número de llamadas que terminan con `tool_call_finished` y `outcome = "success"`, dividido entre las llamadas iniciadas y multiplicado por 100. |
| P9. Errores | Número de identificadores `error_id` distintos en `error_recorded`, excluyendo los de gravedad `warning`. |
| P10. Reintentos | Número de reintentos registrados mediante `retry_recorded`. No incluye la corrección solicitada por el Revisor. |
| P11. Corrección solicitada por el Revisor | Los eventos de revisión y corrección indican si se utiliza esta fase. |
| P12. Peticiones al modelo | Número de eventos `model_call_started`, incluidos los intentos fallidos y los reintentos. |
| P13. Límites alcanzados | Presencia y tipo de límites registrados mediante `limit_reached`. |
| P14. Integridad de la traza | Se obtiene de la comprobación de `trace.jsonl`. El porcentaje de campos obligatorios presentes debe interpretarse junto con el estado de validación y las incidencias detectadas, según se explica en el apartado siguiente. |

Para comparar las repeticiones se calculan frecuencias y porcentajes de los estados, medianas y valores mínimo y máximo de las medidas numéricas, y distribuciones por categoría de los errores. También se presenta el coste acumulado cuando corresponde.

## 49. Integridad y validación de `trace.jsonl`
El validador de la traza comprueba:
1. Que cada línea pueda leerse como un objeto JSON.
2. Que estén presentes los campos comunes y los campos obligatorios del tipo de evento.
3. Que la versión del esquema, el tipo de evento, la fase, el rol y el origen tengan valores admitidos.
4. Que los números de secuencia sean consecutivos y el tiempo transcurrido no disminuya.
5. Que los identificadores de los eventos no se repitan y los datos de identificación de la ejecución sean coherentes.
6. Que existan los eventos de inicio, finalización y cierre de la traza, y que el inicio y el cierre ocupen las posiciones previstas.
7. Que las intervenciones de los roles, las peticiones al modelo y las llamadas a herramientas iniciadas tengan un evento de finalización o fallo.
8. Que las referencias a eventos anteriores y a errores registrados sean válidas.
9. Que el número total de eventos y su distribución por tipo coincidan con el resumen de trace_closed.

El resultado de estas comprobaciones indica si la traza es válida, incompleta o inválida y detalla los problemas detectados. También se calcula el porcentaje de campos obligatorios presentes, dividiendo su número entre el total esperado y multiplicando por 100. Este porcentaje puede alcanzar el 100 % aunque existan incoherencias, por lo que debe interpretarse junto con el resultado de la validación.

Durante el piloto, estas comprobaciones se aplican a las trazas de las tres implementaciones para verificar que utilizan la misma estructura y contienen la información necesaria para revisar las ejecuciones y calcular las métricas automáticas.

## 50. Contenido excluido y protección de información
La traza no debe incluir:
- Claves de API, cabeceras de autenticación, cookies ni variables de entorno.
- Contenido de `datasets/reference_private/` ni valores de referencia de la evaluación.
- Razonamiento interno no visible del modelo.
- El dataset completo ni muestras mayores que las permitidas.
- Rutas absolutas del equipo cuando baste una ruta relativa o un identificador.
- Respuestas completas del proveedor que dupliquen innecesariamente la información ya registrada.

Se conservan el código Python ejecutado, los argumentos de las herramientas, los mensajes visibles necesarios para reconstruir el flujo, las respuestas de las herramientas con los límites de tamaño establecidos y los identificadores de las llamadas.

Antes de escribir cada evento, la capa común revisa los campos de texto y los objetos mediante reglas de detección de información sensible. Los valores detectados se sustituyen por `[REDACTED]` y se registra una advertencia sin conservar el contenido original.

## 51. Relación con los registros propios de los frameworks y de OpenAI
Los registros propios de cada framework y de OpenAI pueden utilizarse para investigar incidencias durante el desarrollo. Son información complementaria y no sustituyen a trace.jsonl, porque no ofrecen necesariamente los mismos datos ni los organizan de la misma forma.

Cuando estén disponibles, sus identificadores pueden incorporarse a `extensions` en el evento correspondiente. Su ausencia no invalida una ejecución si la traza común contiene la información exigida.

---

[← Parte 4](04_herramientas.md) · [Parte 6 →](06_prompts_comunes.md)
