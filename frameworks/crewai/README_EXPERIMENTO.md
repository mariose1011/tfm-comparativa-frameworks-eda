# Adaptador experimental de CrewAI

## Estado

CrewAI 1.15.11 está instalado en el entorno virtual de esta carpeta. El adaptador utiliza la API Responses de OpenAI y crea un contexto nuevo para cada rol.

## Qué aporta CrewAI

CrewAI crea y ejecuta un agente y una tarea para cada intervención del Planificador, Analista y Revisor. El proceso es secuencial y no activa memoria, planificación adicional, delegación, caché, ejecución paralela ni reintentos nativos.

## Qué sigue siendo común

El adaptador utiliza las herramientas, los validadores y los controles de `experimento/capa_comun`:

- `inspect_dataset`
- `execute_python`
- `read_output`
- `validate_outputs`
- validadores de resultados
- control de límites y coste
- guardado de `plan.md` y `report.md`
- cálculo de `completed`, `partial` o `failed`
- escritura y validación de `trace.jsonl`

`herramientas.py` conecta las solicitudes de CrewAI con las herramientas de la capa común. `modelo.py` sustituye las instrucciones añadidas por CrewAI por las del contrato y proporciona las mismas definiciones de herramientas que las otras implementaciones. Durante cada fase se conserva el historial de solicitudes de herramientas y sus respuestas.

Estos comandos realizan una ejecución real y consumen crédito de la API de OpenAI.

## Ejecutar D0

Desde la carpeta raíz del TFM:

```powershell
.\frameworks\crewai\ejecutar_experimento.cmd --dataset D0_piloto --repeticion 1
```

También puede utilizarse directamente el módulo:

```powershell
& ".\frameworks\crewai\.venv\Scripts\python.exe" -m frameworks.crewai.adaptador_experimento --dataset D0_piloto --repeticion 1
```

La ejecución carga `OPENAI_API_KEY` desde `frameworks/framework_keys.env`. Las respuestas se guardan en OpenAI porque la configuración mantiene `store` activado. La traza completa y los resultados se guardan además en `outputs/experimento`.

## Pruebas sin coste

```powershell
& ".\frameworks\crewai\.venv\Scripts\python.exe" -m unittest frameworks.crewai.test_adaptador_experimento -v
```

Estas seis pruebas utilizan respuestas simuladas para comprobar los agentes, las tareas y las herramientas de CrewAI, sin conectarse a OpenAI.
