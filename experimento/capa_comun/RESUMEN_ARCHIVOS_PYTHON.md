# Resumen de los archivos Python de la capa común

## 1. Organización de esta carpeta

Este documento explica la función de los archivos Python de la capa común y cómo se relacionan durante una ejecución. Las dependencias y los comandos de comprobación y pruebas se describen en el `README.md`.

No hay que ejecutar ni configurar cada archivo por separado. Los adaptadores de los frameworks acceden a las funciones compartidas y estas utilizan los módulos cuando corresponde.

Existen:

- 17 archivos Python que forman la capa común.
- 7 archivos dentro de `tests`: cinco contienen pruebas, uno proporciona datos y respuestas simuladas y otro identifica la carpeta como paquete Python.

## 2. Visión simplificada del funcionamiento

El recorrido normal de una ejecución es el siguiente:

```text
Adaptador del framework
        |
        v
Carga de configuración y dataset
        |
        v
Preparación de la carpeta de ejecución
        |
        v
Creación de la traza y de los contadores
        |
        v
Análisis de datos, generación y comprobación de resultados
        |
        v
Cálculo del estado final y cierre de la traza
```

Los archivos Python reparten estas responsabilidades para que el código sea más fácil de revisar y probar.

## 3. Archivos principales

### `__init__.py`

**Qué contiene:** la lista de clases y funciones que pueden utilizar los adaptadores.

**Para qué sirve:** reúne las clases y funciones que pueden utilizar los adaptadores y permite acceder a ellas desde un mismo punto.

**Quién lo utiliza:** los adaptadores de LangGraph, CrewAI y Microsoft Agent Framework.

### `herramientas.py`

**Qué contiene:** la definición y coordinación de las cuatro herramientas comunes:

- `inspect_dataset`
- `execute_python`
- `read_output`
- `validate_outputs`

También comprueba qué rol solicita cada herramienta, registra su uso y devuelve las respuestas con una estructura común.

**Para qué sirve:** garantiza que los tres frameworks proporcionen a sus agentes exactamente las mismas capacidades.

**Quién lo utiliza:** principalmente los adaptadores. Es el archivo central de la capa común.

### `configuracion.py`

**Qué contiene:** la carga y validación de `configuracion_experimento_v1.0.json`.

**Para qué sirve:** comprueba que el modelo, los límites, las rutas, las herramientas y las demás decisiones congeladas sean válidas. También impide que la configuración incluya credenciales o active comportamientos no permitidos.

**Cuándo se utiliza:** al inicio de cualquier comprobación o ejecución.

### `prompts.py`

**Qué contiene:** la construcción de los prompts comunes y la interpretación de las respuestas del Revisor y de la corrección.

**Para qué sirve:** construye los mensajes de cada rol con las instrucciones comunes y la información autorizada de la ejecución. Comprueba que no queden datos pendientes de incorporar y calcula los hashes que permiten identificar los mensajes preparados.

**Cuándo se utiliza:** antes de cada intervención y al procesar las respuestas de revisión y corrección.

### `datasets.py`

**Qué contiene:** la lectura y comprobación del registro de datasets, `datasets/manifest.json`.

**Para qué sirve:** verifica los identificadores, las rutas, el tamaño y los hashes de los archivos de entrada y de su documentación pública. También comprueba que el formato declarado sea válido y que los archivos Excel tengan indicada una hoja para su lectura.

**Cuándo se utiliza:** antes de crear una ejecución.

### `ejecucion.py`

**Qué contiene:** la creación del identificador `run_id`, el contexto de ejecución y las carpetas de resultados.

**Para qué sirve:** separa cada combinación de framework, dataset y repetición. También evita sobrescribir una ejecución anterior.

**Cuándo se utiliza:** una vez validados la configuración y el dataset.

### `traza.py`

**Qué contiene:** el escritor y el validador de `trace.jsonl`.

**Para qué sirve:** registra de forma ordenada las llamadas al modelo, las intervenciones de los roles, las herramientas, los errores, los archivos generados y el cierre de la ejecución. Antes de escribir, elimina credenciales, rutas absolutas y referencias privadas.

**Cuándo se utiliza:** durante toda la ejecución, desde el comienzo hasta el cierre.

### `limites.py`

**Qué contiene:** los contadores de consumo y las comprobaciones que permiten continuar o bloquean nuevas operaciones según los límites de tiempo, tokens, peticiones al modelo, llamadas a herramientas, reintentos y coste.

**Para qué sirve:** comprueba los límites configurados, autoriza o bloquea nuevas operaciones y registra advertencias e incumplimientos. También calcula las métricas de consumo de la misma forma para los tres frameworks.

**Cuándo se utiliza:** antes y después de cada llamada al modelo o a una herramienta.

### `validacion.py`

**Qué contiene:** las reglas que validan los siete resultados obligatorios y sus relaciones internas.

**Para qué sirve:** comprueba la estructura de `plan.md`, `prepared_data.csv`, `statistics.json`, `issues.json`, `figures/`, `report.md` y `trace.jsonl`. También verifica que el informe cite estadísticas y figuras realmente generadas.

Este archivo determina, junto con el cierre, si el resultado puede considerarse `completed`, `partial` o `failed`.

**Cuándo se utiliza:** Cuando el Analista o el Revisor solicitan una validación y automáticamente antes de la revisión, después de la corrección y durante el cierre.

### `cierre.py`

**Qué contiene:** la operación final común de la ejecución.

**Para qué sirve:** realiza la última validación, calcula el estado terminal, registra los totales y cierra `trace.jsonl`.

**Cuándo se utiliza:** al finalizar el flujo o cuando un error o un límite obliga a realizar un cierre controlado.

## 4. Archivos que apoyan a las herramientas

### `ejecutor_python.py`

**Qué contiene:** el controlador que revisa el código solicitado por el Analista y pone en marcha un proceso nuevo de Python.

**Para qué sirve:** aplica los límites de tiempo, memoria y tamaño de respuesta. También comprueba qué archivos han sido creados o modificados y protege el dataset y los documentos reservados.

**Relación con otros archivos:** `herramientas.py` lo utiliza cuando el Analista llama a `execute_python`.

### `worker_python.py`

**Qué contiene:** el proceso separado que ejecuta realmente el código autorizado.

**Para qué sirve:** ejecuta el código con las bibliotecas autorizadas y aplica controles para impedir el acceso a la red, la creación de otros procesos y el acceso a archivos no permitidos.

**Relación con otros archivos:** solamente lo inicia `ejecutor_python.py`.

### `lectura.py`

**Qué contiene:** la lógica interna de `read_output`.

**Para qué sirve:** permite consultar Markdown, JSON, el CSV preparado y las figuras sin cargar archivos demasiado grandes de una sola vez. Puede devolver resúmenes, secciones, elementos concretos y páginas sucesivas.

**Relación con otros archivos:** `herramientas.py` lo utiliza cuando un rol llama a `read_output`.

### `artefactos.py`

**Qué contiene:** la creación controlada de `plan.md` y `report.md`.

**Para qué sirve:** comprueba y guarda las respuestas finales del Planificador como plan.md y del Analista como report.md. Verifica su estructura antes de guardarlas e impide las sobrescrituras no permitidas.

**Cuándo se utiliza:** al terminar el Planificador y el Analista, incluida la actualización del informe durante la corrección opcional.

## 5. Archivos auxiliares pequeños

### `utilidades.py`

**Qué contiene:** funciones genéricas para leer JSON, detectar claves duplicadas, calcular hashes, validar identificadores y resolver rutas seguras.

**Para qué sirve:** evita repetir estas operaciones en varios módulos.

**Quién lo utiliza:** configuración, datasets y otros componentes internos.

### `errores.py`

**Qué contiene:** los tipos de error propios de la capa común.

**Para qué sirve:** permite distinguir un error de configuración, de rutas, del manifiesto, de hash o de preparación de una ejecución.

**Quién lo utiliza:** todos los módulos cuando necesitan comunicar un fallo controlado.

### `__main__.py`

**Qué contiene:** dos comandos de consola, `validar` y `preparar`.

**Para qué sirve:** permite comprobar manualmente la configuración y los datasets o preparar una carpeta de ejecución. Es una utilidad para desarrollo y diagnóstico, no forma parte de la interacción entre agentes.

## 6. Archivos de pruebas

Los archivos de `tests` comprueban el funcionamiento de la capa común y proporcionan datos simulados para probar los adaptadores. Se ejecutan durante el desarrollo y después de introducir cambios en el código. No intervienen en las ejecuciones experimentales reales.

### `tests/__init__.py`

Identifica la carpeta de pruebas como un paquete Python. No contiene lógica experimental.

### `tests/test_nucleo.py`

Comprueba la configuración, los hashes, las rutas, los datasets, el `run_id` y la preparación de carpetas.

### `tests/test_traza_limites.py`

Comprueba la integridad de `trace.jsonl`, la ocultación de información sensible, el cálculo de costes y los controles de los límites.

### `tests/test_inspeccion.py`

Comprueba que `inspect_dataset` produzca la misma inspección para los tres frameworks y que respete los permisos de los roles.

### `tests/test_execute_python.py`

Comprueba que Python se ejecute en un proceso aislado, que pueda generar análisis y figuras y que no pueda importar módulos de sistema ni modificar `report.md`.

### `tests/test_salidas.py`

Comprueba `read_output`, la creación de `plan.md` y `report.md`, la validación de todos los resultados, el cierre y los estados `completed`, `partial` y `failed`.

### `tests/fixtures_adaptadores.py`

Proporciona planes, informes, decisiones del Revisor y respuestas de corrección simuladas para comprobar los adaptadores sin realizar llamadas a OpenAI.