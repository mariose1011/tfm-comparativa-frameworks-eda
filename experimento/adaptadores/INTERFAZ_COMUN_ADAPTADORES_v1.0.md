# Interfaz común de los adaptadores v1.0

## 1. Finalidad y alcance
Cada framework necesita un adaptador que conecte su funcionamiento nativo con la capa común. El adaptador utiliza los agentes, tareas o nodos del framework para ejecutar los roles y conecta sus mensajes y solicitudes de herramientas con la capa común.

Las reglas que debe respetar ya están definidas en otros documentos:
| Contenido | Fuente |
| --- | --- |
| Roles, flujo y corrección | Parte 2 del contrato |
| Archivos de salida | Parte 3 |
| Herramientas | Parte 4 |
| Traza y métricas | Parte 5 |
| Prompts y respuestas | Parte 6 |
| Modelo, límites y coste | Parte 7 y configuración ejecutable |

Este documento solo define la conexión entre esas reglas y cada framework.

## 2. Reparto de responsabilidades
| Componente | Responsabilidad |
| --- | --- |
| Capa común | Preparar la ejecución, ofrecer herramientas, controlar límites, validar resultados, escribir la traza y calcular el estado final. |
| Adaptador | Ejecutar los roles con el framework y traducir mensajes, herramientas y metadatos al formato común. |
| Framework | Representar de forma nativa los agentes, tareas, nodos y transiciones. |

## 3. Entrada y resultado
Los tres adaptadores ofrecerán una operación equivalente a:
```text
ejecutar_experimento(dataset_id, repeticion, ruta_configuracion, run_id_opcional)
```
Cada adaptador tendrá fijado su `framework_id`. La entrada no permitirá cambiar el modelo, los prompts, las herramientas ni los límites.

La operación devolverá:
- Identificación de la ejecución, el framework, el dataset y la repetición.
- Estado final y código del motivo.
- Carpeta de resultados.
- Decisión del Revisor y uso de la corrección.
- Resultado de la validación de la traza.

## 4. Responsabilidades del adaptador

| Área | El adaptador debe | El adaptador no puede |
| --- | --- | --- |
| Flujo | Ejecutar Planificador, Analista y Revisor en el orden aprobado. | Crear roles adicionales, volver al Planificador o permitir más de una corrección. |
| Contexto | Crear un contexto nuevo con la información autorizada para cada intervención. | Compartir el historial completo entre roles o usar información de otras ejecuciones. |
| Prompts | Enviar los componentes comunes mediante los tipos de mensaje del framework. | Resumir, parafrasear o añadir instrucciones propias. |
| Herramientas | Conectar las herramientas disponibles para los agentes con las funciones de HerramientasComunes. | Crear versiones propias o exponer herramientas no autorizadas. |
| Modelo | Usar la integración correspondiente con OpenAI Responses y registrar cada intento de petición. | Omitir peticiones, errores o reintentos. |
| Respuestas | Entregar las respuestas finales a la capa común sin reescribirlas. | Completar, corregir o reparar silenciosamente una respuesta inválida. |
| Cierre | Solicitar la validación y el cierre comunes. | Decidir por sí mismo si el resultado es `completed`, `partial` o `failed`. |

Si una respuesta incumple el formato exigido, la capa común detecta el error y el adaptador registra la incidencia y solicita al mismo rol una reparación sin herramientas, dentro de los límites de reintentos establecidos.

## 5. Flujo y representación
```text
Inicio -> Planificador -> Analista -> Validación previa -> Revisor -> Validación final -> Cierre
Inicio -> Planificador -> Analista -> Validación previa -> Revisor -> Corrección del Analista -> Validación final -> Cierre
```
| Framework | Representación |
| --- | --- |
| LangGraph | Estado, nodos y transiciones condicionales. |
| CrewAI | Agentes y tareas secuenciales. |
| Microsoft Agent Framework | Agentes y flujo de ejecución. |

Cada adaptador organiza las intervenciones de los roles mediante los componentes de su framework y reutiliza las funciones de la capa común para construir los prompts, ejecutar las herramientas, comprobar los límites, validar los resultados, registrar la ejecución y realizar el cierre. La coordinación de los roles se mantiene en cada implementación, ya que las diferencias entre sus mecanismos forman parte de la comparación.

## 6. Criterio de aceptación

Un adaptador será válido cuando:

- Use la configuración común sin modificarla.
- Respete los roles, el flujo y la única corrección permitida.
- Utilice las instrucciones comunes y proporcione a cada rol la información y las herramientas autorizadas.
- Registre todas las peticiones y el consumo informado por el proveedor.
- Entregue las respuestas sin reescribirlas.
- Delegue la validación y el estado final en la capa común.
- Produzca una traza íntegra y resultados aislados.

## 7. Estado tras las ejecuciones definitivas

Los tres adaptadores superaron D0 y utilizaron la misma interfaz durante las dieciocho ejecuciones definitivas de D1 y D2. De ellas, dieciséis finalizaron como `completed` y dos como `partial` al alcanzar un límite del experimento, conservando resultados evaluables.

También se conservan dos ejecuciones invalidadas. Una se debió a un bloqueo de conexión anterior al proveedor y otra permitió detectar la ausencia de la reparación de formato declarada en la configuración. Esta última incidencia originó la corrección técnica común v1.0.1.

Las ejecuciones incluidas y los intentos invalidados se identifican en el [registro de las ejecuciones definitivas](../REGISTRO_EJECUCIONES_D1_D2.md). Sus archivos y trazas permiten consultar el desarrollo de cada ejecución y respaldan los resultados recogidos en la [documentación de evaluación](../evaluacion/README.md).
