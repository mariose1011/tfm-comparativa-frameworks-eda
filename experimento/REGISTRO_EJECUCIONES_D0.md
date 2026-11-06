# Registro del piloto D0 y ajustes del entorno experimental

**Fecha de revisión:** 30 de agosto de 2026  
**Finalidad:** validar el protocolo técnico antes de congelar la versión 1.0  
**Alcance:** revisión inicial de una ejecución de D0 por framework y comprobación final tras los ajustes del entorno.

## 1. Qué se está evaluando en este documento

Esta revisión comprueba que LangGraph, CrewAI y Microsoft Agent Framework pueden ejecutar el mismo contrato y producir evidencia comparable. D0 es un piloto técnico con datos sintéticos, que no forma parte de la comparación final y no permite concluir qué framework ofrece mejor rendimiento.

## 2. Ejecuciones revisadas

La revisión inicial se realizó sobre las siguientes ejecuciones de D0, una por framework. La tabla recoge sus identificadores y su estado final.

| Framework | `run_id` | Estado |
| --- | --- | --- |
| LangGraph | `D0_piloto__langgraph__r03__20260830T110121632408Z` | `completed` |
| CrewAI | `D0_piloto__crewai__r01__20260830T115300768361Z` | `completed` |
| Microsoft Agent Framework | `D0_piloto__microsoft_agent_framework__r01__20260830T122721605569Z` | `completed` |

Las tres utilizaron el mismo hash de configuración `E90F15DBA854112CF685804D0EC1693BAB8BDCAF339B7841CC1CC03AC622F4D0`, el mismo hash del dataset, los mismos componentes de prompt, el mismo modelo `gpt-5.6-terra` y los mismos parámetros de OpenAI Responses.

## 3. Métricas principales observadas

| Métrica por ejecución | LangGraph | CrewAI | Microsoft Agent Framework |
| --- | ---: | ---: | ---: |
| P1 Estado | `completed` | `completed` | `completed` |
| P2 Duración | 189,286 s | 232,009 s | 163,116 s |
| P3 Tokens de entrada | 403713 | 494025 | 304983 |
| P4 Tokens de salida | 19773 | 26218 | 18284 |
| P5 Tokens totales | 423486 | 520243 | 323267 |
| Tokens de entrada en caché | 307900 | 394679 | 220934 |
| P6 Coste estimado | 0,490482 USD | 0,592244 USD | 0,431693 USD |
| P7 Llamadas a herramientas | 13 | 16 | 10 |
| P8 Éxito de herramientas | 100 % | 75 % | 100 % |
| P9 Errores, sin advertencias | 0 | 4 | 0 |
| Advertencias por ocultación de contenido | 0 | 6 | 0 |
| Avisos de proximidad a los límites | 1 | 3 | 0
| P10 Reintentos | 0 | 0 | 0 |
| P11 Corrección utilizada | No | Sí | No |
| P12 Peticiones reales al modelo | 16 | 20 | 13 |
| P13 Límites alcanzados | 0 | 0 | 0 |
| P14 Integridad de la traza | 100 % | 100 % | 100 % |

## 4. Distribución de herramientas

La tabla desglosa las llamadas solicitadas por el modelo durante cada ejecución, según la herramienta utilizada.

| Framework | `inspect_dataset` | `execute_python` | `read_output` | `validate_outputs` | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| LangGraph | 1 | 4 | 7 | 1 | 13 |
| CrewAI | 1 | 4 | 10 | 1 | 16 |
| Microsoft Agent Framework | 1 | 2 | 6 | 1 | 10 |

## 5. Incidencias y decisiones

### 5.1. Consultas inválidas a `read_output`

CrewAI realizó tres consultas que `read_output` no admitía. Por ejemplo, solicitó una sección de `statistics.json`, aunque esa forma de consulta solo estaba disponible para el plan y el informe.

La herramienta rechazó las tres operaciones, pero su descripción no explicaba claramente qué consultas podían utilizarse con cada archivo ni cómo seleccionar un contenido concreto o continuar una lectura. Se aclararon estas indicaciones y tools.version pasó de 0.2 a 0.3, sin añadir capacidades nuevas.

### 5.2. Error con un valor `NaN`
Una llamada de CrewAI a `execute_python` falló al guardar un resultado que contenía un valor`NaN`. El código generado utilizaba `allow_nan=False`, que impide escribir ese valor en un archivo JSON y produjo un error ValueError.

El error quedó registrado y el Analista realizó una nueva llamada para completar los archivos.

### 5.3. Ocultación incorrecta de contenido en la traza de CrewAI

El mecanismo que ocultaba rutas del equipo identificó incorrectamente parte de una enumeración como una ruta de Windows. Se ajustó la detección para evitar esa coincidencia.

Durante la siguiente ejecución de CrewAI apareció un segundo caso. Un fragmento de código Python con un salto de línea representado como \n se interpretó como una ruta de la unidad F:. Se modificó la detección y se añadieron pruebas para conservar esos fragmentos sin dejar de ocultar las rutas y la información sensible previstas.

### 5.4. Bloques cifrados en la traza de LangGraph

LangGraph conservó bloques cifrados de razonamiento dentro de algunos mensajes anteriores. No eran texto visible, no aportaban evidencia evaluable y aumentaron el tamaño de la traza.

El adaptador se ha ajustado para registrar únicamente el texto visible y las llamadas a herramientas.

### 5.5. Margen de tokens

LangGraph alcanzó el aviso del 80 por ciento del límite acumulado de entrada. CrewAI terminó con 494025 tokens, un 98,8 por ciento del máximo anterior de 500000. Microsoft Agent Framework quedó en 304983.

Tras la revisión inicial, se establecieron unos máximos de 720.000 tokens de entrada, 80.000 de salida y 800.000 en total, correspondientes a la versión 0.3 de los límites. La comprobación final del piloto se realizó con estos valores y un presupuesto máximo de 2,50 USD por ejecución.

### 5.6. Corrección opcional

El Revisor de CrewAI detectó que una figura citada no estaba enlazada mediante su ruta relativa. Solicitó la única corrección permitida y la validación final quedó en estado válido.

## 6. Repetición ejecutada antes de congelar la versión 1.0

Los cambios de herramientas y límites modificaron la configuración común. Se realizó una nueva ejecución de D0 con cada framework antes de congelar la versión 1.0.

La configuración provisional corregida es válida y tiene el hash `F3CAA9D16A00BE6B7C55C13EA1D0CDCF3BEE2DC48625731455E76FFCA981D9AC`. Las tres ejecuciones aceptadas registran este mismo hash, `tools.version: 0.3` y `versions.limits: 0.3`.

### 6.1. Ejecuciones aceptadas

| Framework | `run_id` | Estado | Validación | Traza |
| --- | --- | --- | --- | --- |
| LangGraph | `D0_piloto__langgraph__r05__20260830T184440324169Z` | `completed` | `valid` | `valid` |
| CrewAI | `D0_piloto__crewai__r03__20260830T185922808777Z` | `completed` | `valid` | `valid` |
| Microsoft Agent Framework | `D0_piloto__microsoft_agent_framework__r02__20260830T185253640246Z` | `completed` | `valid` | `valid` |

Un error de conexión local con la API interrumpió la cuarta ejecución de LangGraph antes de iniciar el análisis. La traza registró cero tokens y esa ejecución quedó fuera de la comprobación final. En CrewAI se descartó el segundo intento, que había completado el análisis, al detectarse otra ocultación incorrecta de un fragmento de código en la traza. Tras ajustar el mecanismo de detección y superar las pruebas locales, se realizó una tercera ejecución de CrewAI, que es la incluida en la comprobación final.

### 6.2. Consumo observado con los límites corregidos

| Métrica | LangGraph | CrewAI | Microsoft Agent Framework |
| --- | ---: | ---: | ---: |
| Duración | 222,821 s | 252,216 s | 179,375 s |
| Tokens de entrada | 428896 | 445137 | 340986 |
| Tokens de salida | 25638 | 25012 | 18703 |
| Tokens totales | 454534 | 470149 | 359689 |
| Porcentaje del máximo total | 56,82 % | 58,77 % | 44,96 % |
| Peticiones al modelo | 17 | 20 | 15 |
| Llamadas a herramientas | 13 | 16 | 12 |
| Coste estimado | 0,583746 USD | 0,596715 USD | 0,434367 USD |
| Corrección opcional | Sí | Sí | No |
| Avisos de tokens | 0 | 0 | 0 |
| Límites alcanzados | 0 | 0 | 0 |

CrewAI y Microsoft Agent Framework emitieron un aviso al alcanzar 8 de las 10 peticiones permitidas al Revisor. El aviso no corresponde a tokens, no interrumpió la ejecución y dejó dos peticiones de margen en ambos casos.

### 6.3. Comprobación de los criterios de aceptación

- Las tres ejecuciones utilizaron las mismas versiones de los componentes comunes y el mismo hash de configuración.
- Las tres ejecuciones terminaron en `completed` con los siete resultados válidos.
- Las tres trazas alcanzaron integridad `valid`.
- La revisión de las trazas aceptadas no detectó nuevas ocultaciones incorrectas de contenido.
- Los hashes de los esquemas de herramientas coinciden entre frameworks para Planificador, Analista y Revisor.
- Ninguna ejecución emitió avisos de tokens ni alcanzó límites de tokens, coste, tiempo o llamadas.

## 7. Decisión

Tras la comprobación final del piloto, se aceptó la configuración utilizada en las tres ejecuciones y se formalizó como versión 1.0 para las ejecuciones definitivas con D1 y D2.