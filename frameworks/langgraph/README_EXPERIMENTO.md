# Adaptador experimental de LangGraph

El adaptador utiliza LangGraph 1.2.10 para organizar el flujo de roles y la API Responses de OpenAI para las peticiones al modelo. Cada fase comienza con una conversación nueva y recibe la información autorizada por el contrato común.

## Organización del adaptador

El grafo define el paso entre el Planificador, el Analista y el Revisor, así como la corrección opcional y el cierre. Durante cada fase, el adaptador gestiona las peticiones al modelo y las solicitudes de herramientas.

La implementación se organiza en cinco módulos:

- `adaptador_experimento.py`: carga la configuración, prepara los componentes e inicia la ejecución.
- `cliente_openai.py`: configura el acceso a OpenAI y recoge las respuestas y el consumo de tokens.
- `grafo.py`: define los nodos y las transiciones entre roles, incluida la corrección opcional.
- `sesion.py`: gestiona las conversaciones, las herramientas, la reparación de formato y el cierre.
- `registro_modelo.py`: comprueba los límites y registra peticiones, consumo, errores y reintentos.

## Componentes comunes

El adaptador reutiliza las funciones de [la capa común](../../experimento/capa_comun/README.md):

- Las herramientas `inspect_dataset`, `execute_python`, `read_output` y `validate_outputs`.
- La construcción de los prompts y la comprobación del formato de las respuestas.
- El guardado de `plan.md` y `report.md`.
- Los controles de tiempo, tokens, peticiones, herramientas, reintentos y coste.
- La validación de los resultados y la determinación del estado final.
- La escritura y validación de `trace.jsonl`.

Las solicitudes de herramientas se ejecutan mediante estas funciones compartidas, no mediante una implementación alternativa de LangGraph.

## Ejecutar D0

La instalación de las dependencias se explica en el [README general](../README.md).

Desde PowerShell, situado en la raíz del proyecto:

```powershell
& ".\frameworks\langgraph\.venv\Scripts\python.exe" -m frameworks.langgraph.adaptador_experimento --dataset D0_piloto --repeticion 1
```

Este comando realiza una ejecución real y consume crédito de la API de OpenAI.

Se necesita la variable `OPENAI_API_KEY`, que puede definirse en el entorno o en el archivo local `frameworks/framework_keys.env`.

Los resultados y la traza se guardan en una carpeta exclusiva dentro de `outputs/experimento`.

## Pruebas simuladas

Desde la raíz del proyecto:

```powershell
& ".\frameworks\langgraph\.venv\Scripts\python.exe" -m unittest -v frameworks.langgraph.test_adaptador_experimento
```

Las nueve pruebas utilizan respuestas simuladas y archivos temporales, sin enviar peticiones a OpenAI. Comprueban la aprobación directa, la corrección opcional, los límites, los fallos, el reintento técnico, la reparación de formato y la exclusión del contenido de razonamiento cifrado de la traza.