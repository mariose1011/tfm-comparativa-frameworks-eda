# Parte 7. Límites cuantitativos y condiciones técnicas

**Contrato:** v1.0  

[← Parte 6](06_prompts_comunes.md) · [Índice →](../contrato_comun_v1.0.md)

Esta parte establece los límites de ejecución y consumo y las condiciones técnicas comunes. Recoge la configuración fijada tras el piloto D0 para las ejecuciones definitivas de D1 y D2.

## 64. Finalidad y principios
Los límites tienen cuatro objetivos:
- Evitar ejecuciones indefinidas o un consumo excesivo.
- Establecer los mismos máximos de tiempo, peticiones y recursos para las tres implementaciones.
- Permitir la comparación del consumo y de las incidencias bajo condiciones comunes.
- Conservar resultados parciales y trazas cuando una ejecución no pueda continuar.

Estos valores son máximos permitidos, no objetivos que deban alcanzarse. Cada implementación puede finalizar utilizando menos recursos, y el consumo observado se incluye en la evaluación.

Los mismos valores se mantienen para LangGraph, CrewAI y Microsoft Agent Framework en todas las repeticiones de D1 y D2.

## 65. Configuración fija del modelo y la API

Las tres implementaciones utilizan la siguiente configuración:

| Elemento | Valor común |
| --- | --- |
| Proveedor | OpenAI |
| Modelo solicitado | `gpt-5.6-terra` |
| API | Responses |
| Modalidad | Standard mediante `service_tier: default` |
| Esfuerzo de razonamiento | `medium` |
| Límite de salida por petición | Hasta 32.000 tokens mediante `max_output_tokens` |
| Selección de herramientas | `tool_choice: auto` |
| Llamadas paralelas a herramientas | `parallel_tool_calls: false` |
| Truncamiento automático del contexto | Desactivado mediante `truncation: disabled` |
| Procesamiento en segundo plano | Desactivado |
| Respuesta en streaming | Desactivada |
| Almacenamiento de respuestas en el proveedor | Activado mediante `store: true` |
| `temperature` y `top_p` | No se enviarán. Se utilizará el comportamiento predeterminado del modelo |
| Modo Pro | Desactivado |
| Sustitución automática de modelo | Desactivada |
| Herramientas integradas del proveedor | Desactivadas. Solo se proporcionan las herramientas de la Parte 4 |

El experimento establece un máximo de 32.000 tokens de salida por petición. Este límite incluye tanto la respuesta visible como los tokens de razonamiento, por lo que no equivale a permitir 32.000 tokens de texto visible. El valor puede reducirse según el presupuesto restante, como se explica en el apartado 69.

El parámetro `store: true` solicita el almacenamiento de las respuestas en OpenAI para su consulta posterior. Estos registros sirven como apoyo para investigar incidencias, mientras que trace.jsonl constituye el registro común del experimento.

No se utiliza el modo Batch. El flujo requiere recibir la respuesta del modelo, ejecutar las herramientas solicitadas y devolver sus resultados antes de continuar. Por ello, las peticiones se realizan mediante Responses, de forma secuencial y en modalidad Standard.

Fuentes técnicas:

- [GPT-5.6 Terra](https://developers.openai.com/api/docs/models/gpt-5.6-terra)
- [Creación de una respuesta con la API Responses](https://developers.openai.com/api/reference/cli/resources/responses/methods/create)
- [Controles de datos de OpenAI](https://developers.openai.com/api/docs/guides/your-data)

## 66. Ámbitos y aplicación de los límites
Los límites se definen para cuatro ámbitos:
1. **Petición u operación:** una solicitud al modelo o una llamada a una herramienta.
2. **Rol:**  el trabajo del Planificador, del Analista inicial, del Revisor o del Analista durante la corrección.
3. **Ejecución:** una combinación concreta de framework, dataset y repetición.
4. **Campaña:** el conjunto de ejecuciones del piloto o del experimento definitivo.

La capa común y los adaptadores aplican los controles correspondientes a cada operación. Los contadores de peticiones al modelo, tokens, llamadas a herramientas, reintentos y tiempo acumulado de Python generan una advertencia limit_warning al alcanzar el 80 % del máximo correspondiente.

Cuando un límite impide continuar, se registra `limit_reached` y se bloquean las nuevas operaciones afectadas. El bloqueo puede producirse antes de agotar el consumo registrado si la estimación de una nueva petición supera el margen disponible.

## 67. Límites de tiempo
La configuración establece los siguientes tiempos máximos:
| Ámbito u operación | Máximo |
| --- | ---: |
| Ejecución completa | 45 minutos |
| Planificador | 5 minutos |
| Analista inicial | 25 minutos |
| Revisor | 10 minutos |
| Corrección opcional | 15 minutos |
| Petición individual al modelo | 300 segundos |
| `inspect_dataset` | 120 segundos |
| `execute_python` por llamada | 180 segundos |
| `read_output` | 30 segundos |
| `validate_outputs` | 60 segundos |
| Espera de finalización del proceso de Python tras ordenar su terminación | 10 segundos |

El máximo global de la ejecución prevalece sobre los máximos de cada rol. Estos no se suman para ampliar los 45 minutos disponibles, y la corrección solo consume tiempo cuando se activa.

La duración total se mide desde `run_started` hasta `run_finished`. Incluye las peticiones al modelo, las herramientas, las validaciones, las esperas y los reintentos.

## 68. Peticiones al modelo
| Ámbito | Máximo de peticiones reales al modelo |
| --- | ---: |
| Planificador | 3 |
| Analista inicial | 20 |
| Revisor | 10 |
| Corrección opcional | 12 |
| Ejecución completa | 45 |

Se contabiliza cada intento de petición registrado mediante `model_call_started`, incluidos los fallidos y los reintentos. Las solicitudes bloqueadas antes de iniciar la llamada no generan este evento.

Los máximos por rol no son transferibles. Que el Planificador utilice menos peticiones no permite aumentar el máximo del Analista. El conjunto de las intervenciones tampoco puede superar el límite global de 45 peticiones.

## 69. Tokens y tamaño del contexto
| Límite | Máximo provisional |
| --- | ---: |
| Entrada estimada de una petición | 100.000 tokens |
| Salida máxima de una petición | 32.000 tokens |
| Entrada acumulada máxima de una ejecución | 720.000 tokens |
| Salida acumulada máxima de una ejecución | 80.000 tokens |
| Total acumulado máximo de una ejecución | 800.000 tokens |
| Reserva mínima para iniciar una nueva petición | 4.000 tokens |

Los consumos acumulados se calculan con los datos informados por OpenAI. Los tokens de entrada recuperados de caché forman parte del total de entrada. Los tokens de razonamiento se registran por separado cuando están disponibles, pero no se suman de nuevo al total de salida.

Antes de iniciar una petición, la capa común estima los tokens de entrada para comprobar el máximo por petición y el margen disponible de tokens y coste de la ejecución. Esta estimación se utiliza para autorizar o bloquear la llamada.

## 70. Llamadas a herramientas
Los siguientes máximos se aplican a las llamadas solicitadas por el modelo:

| Rol | `inspect_dataset` | `execute_python` | `read_output` | `validate_outputs` |
| --- | ---: | ---: | ---: | ---: |
| Planificador | 1 | 0 | 0 | 0 |
| Analista inicial | 0 | 10 | 6 | 2 |
| Revisor | 0 | 0 | 8 | 2 |
| Corrección opcional | 0 | 5 | 5 | 2 |

El máximo global es de 40 llamadas a herramientas solicitadas por el modelo. Los máximos por rol y herramienta deben respetarse junto con este límite global.

La inspección inicial se reutiliza sin volver a ejecutar inspect_dataset. Las validaciones automáticas de la capa común no consumen el cupo de llamadas a herramientas solicitadas por el modelo, aunque su duración forma parte del tiempo total.

Las herramientas se ejecutan de forma secuencial. Las llamadas rechazadas por argumentos incorrectos o falta de permisos se contabilizan y se registran como fallidas.

## 71. Recursos de `execute_python`
Cada llamada a `execute_python` se ejecuta en un proceso nuevo, sin conservar las variables en memoria de llamadas anteriores. Se aplican las siguientes condiciones:
- Tiempo máximo de 180 segundos por llamada.
- Tiempo acumulado máximo de 900 segundos por ejecución.
- Memoria máxima de 4 GB por proceso.
- Una sola llamada de Python activa.
- Controles para impedir el acceso a Internet y la creación de procesos secundarios.
- Escritura limitada a los archivos y directorios autorizados de la ejecución.
- Dependencias instaladas previamente, sin permitir instalaciones durante la ejecución.
- Salidas de texto `stdout` y `stderr` limitadas a 30.000 caracteres cada una.

Las bibliotecas numéricas se configuran para utilizar un único hilo cuando sea posible. Las versiones de Python y de las dependencias se documentan junto con la configuración del entorno.

Si se supera el tiempo permitido o se detecta una operación no autorizada, la herramienta devuelve un error. Los archivos que hayan quedado guardados se conservan.

## 72. Tamaño de respuestas y archivos
| Elemento | Máximo |
| --- | ---: |
| Filas mostradas por `inspect_dataset` | 20 |
| Respuesta textual de una herramienta | 60.000 caracteres |
| Fragmento de `read_output` | 50.000 caracteres |
| `plan.md` | 1 MB |
| `report.md` | 1 MB |
| `statistics.json` | 20 MB |
| `issues.json` | 20 MB |
| Número de figuras PNG | 12 |
| Tamaño de una figura | 10 MB |
| Tamaño total de `figures/` | 100 MB |
| `trace.jsonl` | 100 MB |
| Directorio completo de una ejecución | 1 GB |

La muestra de `inspect_dataset` combina hasta cinco primeras filas, cinco últimas filas y diez filas seleccionadas mediante la semilla común 20260808.

Si el contenido solicitado supera el tamaño permitido y la consulta admite continuación, `read_output` devuelve un fragmento y un código para solicitar el siguiente. En `execute_python`, los textos de `stdout` y `stderr` que superan sus límites se recortan y se identifican como truncados.

Si la respuesta completa de una herramienta supera el tamaño máximo admitido, se devuelve el error OUTPUT_TOO_LARGE. Los excesos de tamaño de los archivos se detectan durante su guardado o validación, según el archivo, y se registran como incumplimientos.

El máximo de doce figuras limita la generación excesiva de archivos. No se exige alcanzar esa cantidad ni se concede una puntuación mayor por producir más gráficos.

## 73. Reintentos y reparaciones de formato
Se aplican las siguientes reglas:
- Una petición al modelo puede repetirse una vez ante un error transitorio de conexión, un tiempo de espera agotado o una respuesta de error 429 o 5xx del proveedor.
- Si la respuesta final de un rol incumple el formato exigido, se le puede solicitar una sola vez que la presente de nuevo con la estructura correcta, sin repetir el análisis ni utilizar herramientas.
- El máximo global es de cuatro reintentos por ejecución, incluyendo los técnicos y los de formato.
- Las herramientas no tendrán reintentos automáticos. El Analista puede solicitar otra llamada dentro de sus permisos y límites.
- Una nueva llamada a herramienta no se contabiliza automáticamente como reintento técnico por estar precedida de un error.
- La corrección solicitada por el Revisor no se contabiliza como reintento.

Los reintentos se incluyen en la duración y en el número de peticiones de la ejecución. La traza conserva el error original y permite relacionarlo con el nuevo intento.

## 74. Corrección y ausencia de intervención manual
La corrección solo puede activarse cuando el Revisor emite `correction_required` y todavía no se ha utilizado esta fase. No se permite una segunda corrección ni una nueva intervención del Revisor.

Durante una ejecución no se permite:
- Responder preguntas del agente.
- Editar archivos manualmente.
- Modificar prompts, límites o herramientas.
- Reiniciar un rol para mejorar su respuesta.
- Cambiar el modelo o el proveedor.

Las ejecuciones parciales o fallidas producidas durante el funcionamiento normal del sistema se conservan como resultados del experimento.

Una ejecución solo puede invalidarse cuando una incidencia externa o un defecto del entorno o de la implementación impiden aplicar las condiciones previstas en el contrato.

La causa debe documentarse y resolverse antes de repetir la misma combinación de framework, dataset y repetición.

## 75. Tratamiento de límites y fallos externos
Cuando un límite impide continuar, se bloquean las operaciones afectadas y se conservan los archivos y registros disponibles. El cierre determina el estado final según las reglas de las partes 2 y 3:
- `failed` cuando no se puede cargar el dataset, no existe un report.md final válido o no se dispone del mínimo de resultados analíticos exigido.
- `partial` cuando existe un informe válido y resultados evaluables, pero el flujo queda incompleto, se alcanza un límite o permanecen incumplimientos técnicos.
- `completed` cuando se completa el flujo previsto, las salidas superan la validación conjunta y no se cumplen las condiciones que obligan a clasificar la ejecución como parcial o fallida.

Estos estados describen la finalización técnica. No sustituyen la evaluación posterior de la calidad del análisis.

## 76. Control del coste
El coste estimado se calcula con las tarifas conservadas en la configuración del experimento, consultadas el 22 de agosto de 2026:
| Categoría | Precio por un millón de tokens |
| --- | ---: |
| Entrada no recuperada de caché | 2,00 USD |
| Entrada recuperada de caché | 0,20 USD |
| Salida | 12,00 USD |

La configuración definitiva establece:

- Aviso de coste por ejecución en 0,75 USD.
- Máximo estimado por ejecución de 2,50 USD.
- Presupuesto máximo del piloto completo de 7,50 USD.
- Presupuesto de las dieciocho ejecuciones definitivas de 45,00 USD.

Estos importes son límites presupuestarios, no previsiones de gasto.

## 77. Entorno común de ejecución
Las ejecuciones deben cumplir las siguientes condiciones:
- Se realizan de forma secuencial, sin ejecutar dos frameworks simultáneamente.
- Se utiliza el mismo equipo Windows.
- Se evitan tareas intensivas ajenas al experimento durante las ejecuciones.
- Cada ejecución comienza con una carpeta nueva y sin reutilizar procesos ni resultados de la anterior.
- Las versiones de Python, los frameworks, el SDK de OpenAI y las dependencias quedan fijadas después del piloto.
- La identidad del dataset se comprueba mediante su hash antes de comenzar.
- Las herramientas incorporan controles para impedir el acceso a Internet.
- Las credenciales se leen desde variables de entorno y no deben incorporarse a los prompts, las salidas ni las trazas.
- La semilla común es 20260808.
- Las ejecuciones definitivas se concentran en un periodo temporal corto para reducir la exposición a cambios del proveedor o del entorno.

## 78. Archivo de configuración
Los valores definitivos de la configuración se conservan en [`experimento/configuracion/configuracion_experimento_v1.0.json`](../configuracion/configuracion_experimento_v1.0.json).

---

[← Parte 6](06_prompts_comunes.md) · [Índice →](../contrato_comun_v1.0.md)
