# Adaptador experimental de Microsoft Agent Framework
## Descripción y funcionamiento

El adaptador utiliza `agent-framework-core 1.13.0` y `agent-framework-openai 1.12.0` y se conecta con OpenAI mediante la API Responses.

Microsoft Agent Framework organiza el flujo entre el Planificador, el Analista y el Revisor. Según la decisión del Revisor, continúa directamente a la validación final o permite una única corrección del Analista antes de finalizar.

Cada fase de trabajo, incluida la corrección, comienza con un agente y una conversación nuevos. No se activan memoria, compactación, herramientas externas, llamadas paralelas ni reintentos automáticos del proveedor.

## Qué sigue siendo común

El adaptador utiliza las herramientas, los validadores y los controles de `experimento/capa_comun`:

- `inspect_dataset`
- `execute_python`
- `read_output`
- `validate_outputs`
- validadores de resultados
- control de límites y coste
- guardado de `plan.md` y `report.md`.
- determinación del estado final de la ejecución
- escritura y validación de `trace.jsonl`

`herramientas.py` conecta las solicitudes de MAF con las herramientas de la capa común. `modelo.py` configura el cliente y registra las peticiones y su consumo. También activa `strict=true` para exigir que los argumentos de las herramientas respeten los nombres, tipos y campos obligatorios definidos en el contrato común.

## Ejecutar D0
Estos comandos realizan una ejecución real y consumen crédito de la API de OpenAI.

Desde la carpeta raíz del TFM:

```powershell
.\frameworks\microsoft_agent_framework\ejecutar_experimento.cmd --dataset D0_piloto --repeticion 1
```

También puede utilizarse directamente el módulo:

```powershell
& ".\frameworks\microsoft_agent_framework\.venv\Scripts\python.exe" -m frameworks.microsoft_agent_framework.adaptador_experimento --dataset D0_piloto --repeticion 1
```

La ejecución necesita `OPENAI_API_KEY`, que puede definirse en el entorno o en el archivo local `frameworks/framework_keys.env`. Las respuestas se conservan en OpenAI mediante la configuración `store`. Los resultados y la traza también se guardan en `outputs/experimento`.

## Pruebas sin coste

```powershell
& ".\frameworks\microsoft_agent_framework\.venv\Scripts\python.exe" -m unittest frameworks.microsoft_agent_framework.test_adaptador_experimento -v
```

Estas seis pruebas utilizan respuestas simuladas para comprobar los agentes, las herramientas y el flujo de MAF, sin conectarse a OpenAI.
