# Parte 2. Roles, coordinación, corrección y finalización

**Contrato:** v1.0

[← Parte 1](01_alcance_entradas_y_etapas.md) · [Parte 3 →](03_archivos_y_esquemas.md)

Esta parte define las responsabilidades de los roles y el orden de sus intervenciones, incluida la corrección y la finalización del flujo.

## 9. Arquitectura funcional común

Cada implementación utiliza tres roles: Planificador, Analista y Revisor, con el mismo modelo, proveedor y configuración experimental. Cada framework puede representarlos mediante agentes, nodos, tareas o componentes equivalentes, siempre que mantenga sus responsabilidades y el orden de intervención.

El flujo comienza con el Planificador y continúa con el Analista. Antes de la intervención del Revisor, una validación automática comprueba la presencia, la estructura y la coherencia básica de las salidas. Si el Revisor aprueba el trabajo, se realiza la validación final y se cierra la ejecución:

`Inicio → Planificador → Analista → Validación previa → Revisor → Validación final → Finalización`

Si el Revisor detecta un incumplimiento corregible, puede solicitar una única intervención adicional del Analista. 

`Inicio → Planificador → Analista → Validación previa → Revisor → Corrección del Analista → Validación final → Finalización`

Durante la ejecución no se permite incorporar agentes o roles adicionales ni iniciar intercambios entre roles fuera de las intervenciones previstas. La corrección es la única intervención adicional permitida para modificar el análisis.

Las adaptaciones necesarias para reproducir este funcionamiento en cada framework se documentan por separado.

## 10. Información conservada durante la ejecución
El sistema conserva la información necesaria para coordinar las intervenciones y seguir el avance de cada ejecución. Cada framework puede organizarla de forma diferente, pero debe mantener como mínimo:
- Identificador de ejecución, framework, dataset y repetición.
- Rutas autorizadas de entrada y salida.
- Versión del contrato, prompts, herramientas y configuración.
- Documentación pública del dataset.
- Plan de análisis.
- Registro de etapas iniciadas y completadas.
- Decisiones de preparación y transformaciones realizadas.
- Resultados estructurados y figuras generadas.
- Problemas, advertencias y errores registrados.
- Estado de los archivos obligatorios.
- Decisión del Revisor y correcciones solicitadas, cuando corresponda.
- Indicación de si se ha utilizado la corrección opcional.
- Estado final de la ejecución.

Esta información se incorpora a medida que avanza el flujo. Su conservación no implica que todos los roles tengan acceso a ella: cada uno recibe únicamente la información autorizada para su intervención.

## 11. Rol del Planificador

### 11.1. Objetivo
Elaborar un plan de EDA que cubra las ocho etapas a partir del objetivo común, la documentación pública del dataset y su inspección inicial, sin anticipar resultados ni utilizar referencias privadas de evaluación.

### 11.2. Entradas
- Objetivo y restricciones del contrato común.
- Ruta y formato del dataset.
- Documentación pública disponible.
- Lista de etapas y salidas obligatorias.

### 11.3. Responsabilidades
El Planificador deberá:
- Formular preguntas analíticas pertinentes para el dataset.
- Relacionar las acciones previstas con las ocho etapas obligatorias.
- Indicar qué aspectos de calidad, variables, agregaciones y relaciones se examinarán.
- Proponer visualizaciones según lo que permitan analizar o comunicar, sin exigir una cantidad determinada.
- Identificar supuestos o dudas que deban comprobarse durante el análisis.
- Ordenar el trabajo para evitar cálculos innecesarios o incoherentes.
- Producir un plan concreto que permita al Analista realizar el trabajo.

### 11.4. Límites
El Planificador no puede:
- Presentar cifras o hallazgos que no estén respaldados por la inspección inicial.
- Ejecutar código para limpiar, transformar o analizar los datos.
- Acceder a las referencias privadas de evaluación.
- Añadir tareas predictivas, conclusiones causales o actividades ajenas al alcance del contrato.
- Cambiar el modelo, los límites, las herramientas o las rutas autorizadas.

### 11.5. Criterio de salida
La intervención se considera completada cuando el Planificador entrega un plan con la estructura exigida, que cubre las ocho etapas e identifica las principales comprobaciones y acciones que debe realizar el Analista.

Durante el análisis, el Analista puede adaptar el plan si los datos contradicen un supuesto o requieren un procedimiento diferente. Estos cambios deben quedar justificados y registrados, sin ampliar el alcance ni solicitar una nueva intervención del Planificador.

## 12. Rol del Analista

### 12.1. Objetivo
Realizar el EDA siguiendo el plan, justificar las decisiones adoptadas y producir resultados e informes respaldados por operaciones reproducibles.

### 12.2. Entradas
- Objetivo, restricciones y etapas del contrato común.
- Dataset y documentación pública.
- Plan producido por el Planificador.
- Información y archivos autorizados de la ejecución actual.
- Herramientas y directorio de salida autorizados.

### 12.3. Responsabilidades
El Analista debe:
- Cubrir las ocho etapas y aportar evidencias de cada una.
- Utilizar las herramientas comunes para preparar los datos, realizar cálculos, generar visualizaciones, consultar archivos y comprobar las salidas.
- Conservar el archivo original sin modificaciones y guardar los datos preparados en una copia independiente.
- Justificar las decisiones de preparación y documentar su efecto sobre los datos y el análisis.
- Comprobar que los cálculos, los archivos y las visualizaciones sean coherentes entre sí antes de la revisión.
- Respaldar las interpretaciones con los resultados obtenidos.
- Elaborar un informe completo para su revisión.
- Documentar los errores relevantes, los cambios respecto al plan y los análisis que no pueda completar.

### 12.4. Autonomía permitida
El Analista puede:
- Elegir técnicas estadísticas y visuales adecuadas dentro del alcance.
- Ajustar el orden o el detalle del plan cuando los datos lo requieran, justificando los cambios.
- Conservar, transformar o excluir observaciones, dejando constancia de las decisiones y de sus efectos.
- Crear variables derivadas necesarias para responder a las preguntas analíticas.

Esta autonomía no permite cambiar las entradas, herramientas, límites, etapas ni las salidas exigidas.

### 12.5. Límites
El Analista no puede:
- Acceder a las referencias privadas de evaluación, a resultados de otras ejecuciones ni a fuentes externas.
- Sobrescribir el dataset original.
- Ocultar errores, transformaciones o resultados que contradigan los supuestos del plan.
- Inventar cifras o hallazgos sin respaldo en los datos y las operaciones realizadas.
- Solicitar nuevas intervenciones del Planificador ni continuar el análisis después de finalizar la única corrección opcional.

Durante esa corrección debe atender los problemas señalados por el Revisor y conservar el trabajo válido, sin repetir el análisis completo.

### 12.6. Criterio de salida
La intervención se considera completada cuando el Analista entrega el informe y genera los archivos analíticos exigidos, con evidencias de las ocho etapas y una explicación de las limitaciones pendientes. La creación de archivos vacíos o inválidos no satisface este criterio.

## 13. Rol del Revisor

### 13.1. Objetivo
Comprobar si el trabajo cumple el contrato y si el informe es coherente con las evidencias generadas, sin consultar las referencias privadas de evaluación.

El Revisor forma parte del sistema evaluado y no asigna las puntuaciones Q1–Q10. Estas se determinan posteriormente mediante el procedimiento de evaluación del experimento, fuera del flujo de agentes.

### 13.2. Entradas
- Objetivo, restricciones y ocho etapas comunes.
- Plan del análisis.
- Archivos y figuras generados por el Analista, incluido el informe.
- Información disponible sobre las transformaciones, los problemas y los errores de la ejecución.
- Resultado de la validación automática previa a la revisión.

### 13.3. Responsabilidades
El Revisor debe comprobar:
- Que existen evidencias de las ocho etapas.
- Que las salidas obligatorias están presentes y son coherentes entre sí.
- Que las afirmaciones del informe están respaldadas por las estadísticas y visualizaciones.
- Que las decisiones de preparación están justificadas.
- Que no se presentan contradicciones, afirmaciones sin respaldo ni conclusiones causales indebidas.
- Que las limitaciones y las incertidumbres se explican con claridad.
- Que se respetan las restricciones del contrato.

Su decisión debe seguir el formato establecido y justificar los problemas señalados mediante evidencias concretas. Una valoración general como 'correcto' o 'mejorable' no es suficiente.

### 13.4. Límites
El Revisor no puede:
- Acceder a las referencias privadas, los valores esperados o los criterios privados de puntuación.
- Ejecutar código, repetir el EDA o modificar los archivos del Analista.
- Añadir objetivos ajenos al contrato ni exigir una técnica concreta cuando existen alternativas válidas.
- Solicitar cambios de estilo que no afecten a la claridad, la corrección, la trazabilidad o el cumplimiento del contrato.
- Solicitar más de una corrección ni realizar una segunda revisión después de ella.

### 13.5. Decisiones posibles
El Revisor emite una de estas decisiones:
- `approved`: no identifica incumplimientos relevantes que justifiquen solicitar una corrección.
- `correction_required`:  identifica problemas concretos que pueden corregirse y que afectan a la validez de los resultados, su trazabilidad, su coherencia o la cobertura de los requisitos.
- `cannot_review`: los resultados están ausentes, dañados o son insuficientes para realizar la revisión.

La aprobación del Revisor no garantiza que el análisis esté libre de errores ni implica una puntuación máxima. La evaluación posterior puede identificar omisiones o diferencias de calidad que no dan lugar a nuevas intervenciones de los agentes.

## 14. Política de corrección opcional

### 14.1. Activación
La corrección se activa cuando el Revisor emite correction_required y no se ha utilizado previamente.

La solicitud debe indicar, para cada problema:
- Qué incumplimiento se detecta y a qué requisito del contrato afecta.
- Qué archivo o resultado contiene la evidencia del problema.
- Qué debe revisarse.
- Qué debe comprobarse para considerar resuelto el problema.

El Revisor no proporciona valores de las referencias privadas ni código de solución. Sus indicaciones se basan en el contrato y en las evidencias disponibles durante la ejecución.

### 14.2. Ejecución
El Analista dispone de una única intervención de corrección, en la que debe:
- Resolver los problemas señalados por el Revisor y ajustar los resultados que dependan de ellos.
- Conservar y reutilizar el trabajo válido de la ejecución.
- Recalcular o regenerar los resultados afectados cuando sea necesario.
- Registrar los cambios, su justificación y las comprobaciones realizadas.
- Entregar la versión final de los resultados y del informe.

La corrección puede afectar a varios archivos cuando sea necesario para resolver los problemas señalados y mantener la coherencia entre los resultados. No permite volver al Planificador, iniciar un análisis completo ni abrir una segunda corrección, y se mantiene sujeta a los límites del experimento.

### 14.3. Cierre de la corrección
Al terminar la corrección, la capa común realiza la validación final de la presencia, la estructura y la coherencia básica de las salidas obligatorias. Después determina el estado final y cierra la ejecución, sin una segunda intervención del Revisor.

Esta validación comprueba los requisitos técnicos, pero no garantiza que los problemas analíticos se hayan resuelto. La eficacia de la corrección se evalúa posteriormente comparando los problemas señalados con los resultados finales.

## 15. Estados y transiciones
Los estados lógicos comunes serán:
| Estado | Significado | Siguiente estado del recorrido ordinario |
| --- | --- | --- |
| `initialized` | Entradas, configuración y directorio preparados. | `planning` |
| `planning` | El Planificador elabora el plan. | `analysis` |
| `analysis` | El Analista realiza el EDA y genera los resultados iniciales. | `review` |
| `review` | El Revisor comprueba el cumplimiento del contrato y la coherencia de los resultados. | `correction` o `final_validation` |
| `correction` | El Analista realiza la única corrección permitida. | `final_validation` |
| `final_validation` | La capa común comprueba las salidas y determina el estado final. | `completed`, `partial` o `failed` |
| `completed` | El flujo y las salidas cumplen los requisitos técnicos de finalización. | Ninguno: Estado final |
| `partial` | Se conservan un informe válido y resultados analíticos evaluables, pero algún requisito técnico o del flujo queda sin cumplir. | Ninguno: Estado final |
| `failed` | No se cumplen las condiciones mínimas para disponer de resultados evaluables. | Ninguno: Estado final |

Entre `analysis` y `review` se realiza la validación previa.

Si un error o un límite interrumpe el recorrido, se aplica el procedimiento de cierre sobre los resultados disponibles. El estado final se determina según los criterios del apartado 16.

No se vuelve al Planificador ni se realiza una segunda revisión. El paso de `review` a `correction` permite una única intervención adicional del Analista. Los errores y los límites alcanzados se conservan en la traza, cualquiera que sea el estado final.

## 16. Condiciones de finalización
El estado final describe el cumplimiento técnico del flujo y de las salidas.

Una ejecución termina como `completed` cuando:
- El dataset se carga correctamente y el flujo de roles concluye. 
- Las salidas obligatorias superan las comprobaciones automáticas de presencia, estructura y coherencia básica. 
- No se alcanza ningún límite obligatorio.
- El Revisor emite una decisión distinta de `cannot_review`.
- Si se solicita una corrección, esta se realiza y no quedan problemas declarados como pendientes en su respuesta ni incumplimientos detectados por la validación final.

Una ejecución termina como `partial` cuando existe un `report.md` válido y al menos una salida analítica válida, pero ocurre alguna de estas situaciones:
- Falta una salida obligatoria o no supera la validación.
- El flujo de roles no concluye.
- El Revisor no emite una decisión o indica `cannot_review`.
- Queda una corrección pendiente o se declaran problemas sin resolver al finalizarla.
- Se alcanza un límite del experimento.

Para comprobar el mínimo de resultados analíticos, el cierre examina `statistics.json`, `issues.json` y `figures/`. Al menos uno de estos elementos debe superar la validación correspondiente.

Una ejecución termina como `failed` cuando no puede cargarse el dataset, no existe un informe final válido o ninguna de esas salidas analíticas supera la validación. La existencia de estadísticas o figuras no permite clasificar la ejecución como `partial` si el informe está ausente, vacío, dañado o no cumple su estructura mínima.

Tras determinar el estado final, la capa común lo registra junto con su motivo y cierra la traza. Los errores u omisiones detectados después, durante la evaluación de calidad, se documentan por separado y no modifican el estado técnico asignado al finalizar la ejecución.

Los requisitos de los archivos y las comprobaciones automáticas se detallan en las partes correspondientes del contrato.

## 17. Igualdad entre frameworks
Las tres implementaciones mantienen:
- Los mismos roles, responsabilidades y orden de intervención.
- Las mismas reglas sobre la información que puede recibir cada rol.
- Una única decisión del Revisor y, como máximo, una corrección del Analista.
- Los mismos estados finales y criterios de cierre.
- La prohibición de incorporar agentes adicionales o repetir etapas fuera del flujo previsto.
- El mismo modelo, proveedor, configuración y límites de ejecución.

El contenido recibido por cada rol puede variar según los resultados de las fases anteriores, pero las reglas que determinan qué información se le proporciona son comunes.

Cuando un framework requiere una representación técnica diferente, su adaptador debe conservar el comportamiento establecido en el contrato, sin añadir herramientas, información ni intervenciones. Estas adaptaciones se documentan para examinar las diferencias de implementación entre frameworks.

---

[← Parte 1](01_alcance_entradas_y_etapas.md) · [Parte 3 →](03_archivos_y_esquemas.md)
