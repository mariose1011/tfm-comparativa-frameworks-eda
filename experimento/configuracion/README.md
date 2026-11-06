# Configuración ejecutable del experimento

## Finalidad
`configuracion_experimento_v1.0.json` contiene la versión legible por software de las decisiones aprobadas en el contrato común. Los adaptadores de LangGraph, CrewAI y Microsoft Agent Framework deberán cargar el mismo archivo.

No sustituye al contrato ni resume sus justificaciones. El contrato explica por qué se adopta cada decisión. Este archivo proporciona al programa los valores exactos que debe aplicar.

## Contenido
La configuración reúne:
- Versiones del contrato, prompts, herramientas, límites, esquemas y manifiesto de datasets.
- Frameworks y datasets autorizados.
- Modelo, API y parámetros comunes de OpenAI.
- Información y herramientas disponibles para cada rol.
- Archivos obligatorios y política de rutas.
- Límites de tiempo, llamadas, tokens, reintentos, tamaños y coste.
- Restricciones de `execute_python` y de las demás herramientas.
- Reglas de seguridad, entorno y cálculo de hashes.

Las rutas son relativas a la raíz del TFM. La configuración no contiene claves de API, rutas privadas del equipo ni valores de referencia utilizados para la evaluación.

## Uso previsto
La capa común utiliza la configuración para:
1. Cargar el JSON una sola vez al iniciar una ejecución.
2. Validar su sintaxis, versión y valores obligatorios.
3. Comprobar el manifiesto y el hash del dataset.
4. Aplicar los mismos valores al adaptador seleccionado.
5. Registrar la versión y el hash de la configuración.
6. Comprobar los límites configurados antes de autorizar nuevas operaciones y rechazar las solicitudes que los superen.


## Estado congelado
El 31 de agosto de 2026 se fijó la configuración definitiva como versión 1.0, incorporando los ajustes comprobados mediante D0. Sus valores se mantuvieron durante las ejecuciones definitivas con D1 y D2.

Los apartados siguientes describen los ajustes realizados durante D0. Las versiones 0.1, 0.2 y 0.3 corresponden a configuraciones provisionales del piloto. Tras la comprobación final, los componentes se identifican con la versión 1.0.

### Ajuste de herramientas durante D0

La primera ejecución real de D0 con LangGraph detectó que la descripción de `execute_python` no indicaba al modelo qué variables y bibliotecas estaban disponibles para ejecutar el código. El Analista intentó localizar el archivo de entrada mediante operaciones no autorizadas y no pudo generar los resultados obligatorios.

Como corrección común, `tools.version` pasó de `0.1` a `0.2`. Se añadieron a la descripción de la herramienta las variables `INPUT_PATH`, `OUTPUT_DIR`, `FIGURES_DIR`, las bibliotecas disponibles y las restricciones de acceso a archivos y de consulta del entorno. No se modificaron el objetivo analítico, el dataset, los prompts de los roles ni los límites.

### Ajuste del registro de respuestas durante D0

En la primera ejecución real se comprobó que OpenAI contabilizaba el consumo, pero las respuestas no quedaban disponibles para su consulta posterior en el panel del proveedor, ya que la configuración utilizaba `store: false`.

Se activó `store: true` de forma común para LangGraph, CrewAI y Microsoft Agent Framework para permitir la consulta posterior de las respuestas en el proveedor. Estos registros sirven como apoyo para investigar incidencias, mientras que `trace.jsonl` constituye la fuente común para calcular las métricas del experimento.

### Ajuste de `read_output` tras la revisión conjunta

Durante el piloto, CrewAI realizó tres consultas a `read_output` que la herramienta no admitía. Por ejemplo, solicitó una sección de `statistics.json`, aunque esa forma de consulta solo estaba disponible para el plan y el informe. La descripción de la herramienta enumeraba las opciones, pero no explicaba claramente cuáles podían utilizarse con cada archivo ni cómo seleccionar un contenido concreto o continuar una lectura.

Como corrección común, `tools.version` pasó de `0.2` a `0.3`. Se aclararon las consultas permitidas para cada tipo de resultado y el uso de sus parámetros, sin modificar las capacidades ni las restricciones de la herramienta.

### Ajuste de límites tras la revisión conjunta

LangGraph alcanzó el aviso del 80% del límite acumulado de tokens de entrada. CrewAI consumió 494.025 tokens de entrada, el 98,8 % del máximo inicial de 500.000. Estos resultados mostraron que el margen disponible era reducido.

Antes de repetir el piloto, se establecieron unos límites comunes de 720.000 tokens de entrada, 80.000 de salida y 800.000 en total, recogidos en la versión 
0.3 de los límites. El presupuesto máximo aumentó a 2,50 USD por ejecución. Con las tarifas del experimento, consumir todos esos tokens supondría 2,40 USD si ninguno de los tokens de entrada se recuperase de caché. Los presupuestos del piloto y de la comparación definitiva se ajustaron a 7,50 y 45 USD, respectivamente. No cambiaron los máximos de peticiones al modelo, de llamadas a herramientas ni los límites por petición.

La repetición controlada de D0 terminó en `completed` con LangGraph, CrewAI y Microsoft Agent Framework. El mayor consumo fue de 470.149 tokens totales, un 58,77% del máximo. Ninguna ejecución aceptada emitió avisos de tokens ni alcanzó límites. Por tanto, estos valores quedan publicados y congelados en la versión 1.0.

## Hash
Antes de cada ejecución, la capa común calcula el SHA-256 de los bytes exactos del archivo. El hash no se guarda dentro del propio JSON porque modificaría el archivo cuyo contenido se pretende identificar. Por ello, se registra en el evento `run_started` de `trace.jsonl`.

## Unidades exactas
Los tiempos se expresan en segundos y los costes en dólares estadounidenses. Los límites de tamaño de archivos, directorios y memoria se expresan en bytes, mientras que los límites de las respuestas de texto se expresan en caracteres. Para los tamaños indicados en MB y GB se utilizan las siguientes equivalencias:
- 1 MB igual a 1.000.000 de bytes.
- 1 GB igual a 1.000.000.000 de bytes.