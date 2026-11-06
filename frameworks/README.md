# Entornos de frameworks del TFM

El experimento utiliza tres entornos virtuales independientes, uno por framework. Las dieciocho ejecuciones definitivas se realizaron con Python 3.12.13. Las comprobaciones locales descritas en este documento no envían peticiones al modelo ni consumen crédito de la API.

## Entornos y versiones utilizadas

| Framework | Entorno | Paquetes principales |
|---|---|---|
| LangGraph | `langgraph/.venv` | `langgraph 1.2.10`, `langchain 1.3.14`, `langchain-openai 1.4.1` |
| CrewAI | `crewai/.venv` | `crewai 1.15.11` con integración de OpenAI |
| Microsoft Agent Framework | `microsoft_agent_framework/.venv` | `agent-framework-core 1.13.0`, `agent-framework-openai 1.12.0` |

Se utiliza Python 3.12 porque la versión de CrewAI seleccionada para el experimento no admite Python 3.14, instalado inicialmente en el equipo. Esta elección permite emplear una misma versión de Python en los tres entornos.

## Comprobar las instalaciones

Desde PowerShell, situándose en la carpeta `TFM`:

```powershell
.\frameworks\verify_installations.cmd
```

La comprobación es local: importa los tres frameworks, crea un grafo mínimo de LangGraph y revisa que las dependencias instaladas sean coherentes. No necesita una clave de OpenAI.

## Trabajar con un entorno

No es necesario activar los entornos. Se puede utilizar directamente el ejecutable de Python de cada uno, desde la raíz del proyecto:

```powershell
& ".\frameworks\langgraph\.venv\Scripts\python.exe" --version
& ".\frameworks\crewai\.venv\Scripts\python.exe" --version
& ".\frameworks\microsoft_agent_framework\.venv\Scripts\python.exe" --version
```

Si se desea activar uno, la política puede habilitarse únicamente para la ventana actual de PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\frameworks\langgraph\.venv\Scripts\Activate.ps1
```

Solo debe activarse un entorno cada vez. Para salir:

```powershell
deactivate
```

## Instalación de entornos

Cada framework dispone de un archivo `requirements.txt` con las versiones fijadas de sus dependencias directas. Estos archivos incluyen también las dependencias de la capa común.

Para crear los entornos, se necesita una instalación de Python 3.12. Para reproducir la versión utilizada en el experimento, debe emplearse Python 3.12.13.

Desde la raíz del proyecto, se ejecutan los siguientes comandos:

```powershell
py -3.12 -m venv frameworks\langgraph\.venv
py -3.12 -m venv frameworks\crewai\.venv
py -3.12 -m venv frameworks\microsoft_agent_framework\.venv

& ".\frameworks\langgraph\.venv\Scripts\python.exe" -m pip install -r frameworks\langgraph\requirements.txt
& ".\frameworks\crewai\.venv\Scripts\python.exe" -m pip install -r frameworks\crewai\requirements.txt
& ".\frameworks\microsoft_agent_framework\.venv\Scripts\python.exe" -m pip install -r frameworks\microsoft_agent_framework\requirements.txt
```

## OpenAI

La configuración experimental utiliza la API Responses de OpenAI con el modelo `gpt-5.6-terra` y el esfuerzo de razonamiento medium. Las ejecuciones reales necesitan la variable `OPENAI_API_KEY`, que puede definirse en el entorno o en el archivo local `frameworks/framework_keys.env`.

## Adaptadores experimentales

Los tres adaptadores utilizan la misma capa común y mantienen la organización propia de cada framework. Su funcionamiento y sus comandos de ejecución y pruebas se explican en:

- [LangGraph](langgraph/README_EXPERIMENTO.md).
- [CrewAI](crewai/README_EXPERIMENTO.md).
- [Microsoft Agent Framework](microsoft_agent_framework/README_EXPERIMENTO.md).