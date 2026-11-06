$ErrorActionPreference = "Stop"

$frameworksRoot = $PSScriptRoot
$previousCrewAIStorage = $env:CREWAI_STORAGE_DIR
$previousLocalAppData = $env:LOCALAPPDATA

try {
    $crewAIStorage = Join-Path $frameworksRoot "crewai\.storage"
    $crewAITemporaryData = Join-Path ([System.IO.Path]::GetTempPath()) "tfm-crewai-verification"
    New-Item -ItemType Directory -Force -Path $crewAIStorage, $crewAITemporaryData | Out-Null

    $env:CREWAI_STORAGE_DIR = $crewAIStorage
    $env:LOCALAPPDATA = $crewAITemporaryData

    Write-Output "=== LangGraph ==="
    $langGraphPython = Join-Path $frameworksRoot "langgraph\.venv\Scripts\python.exe"
    & $langGraphPython -c "import importlib.metadata as m; from langgraph.graph import StateGraph, MessagesState, START, END; g=StateGraph(MessagesState); g.add_node('hello', lambda s: {'messages':[{'role':'ai','content':'ok'}]}); g.add_edge(START,'hello'); g.add_edge('hello',END); result=g.compile().invoke({'messages':[{'role':'user','content':'test'}]}); print(m.version('langgraph'), result['messages'][-1].content)"
    if ($LASTEXITCODE -ne 0) { throw "Fallo al importar LangGraph" }
    & $langGraphPython -m pip check
    if ($LASTEXITCODE -ne 0) { throw "Dependencias incorrectas en LangGraph" }

    Write-Output "=== CrewAI ==="
    $crewAIPython = Join-Path $frameworksRoot "crewai\.venv\Scripts\python.exe"
    & $crewAIPython -c "import importlib.metadata as m; from crewai import Agent, Crew, Task, Process, LLM; print(m.version('crewai'), 'imports OK')"
    if ($LASTEXITCODE -ne 0) { throw "Fallo al importar CrewAI" }
    & $crewAIPython -m pip check
    if ($LASTEXITCODE -ne 0) { throw "Dependencias incorrectas en CrewAI" }

    Write-Output "=== Microsoft Agent Framework ==="
    $mafPython = Join-Path $frameworksRoot "microsoft_agent_framework\.venv\Scripts\python.exe"
    & $mafPython -c "import importlib.metadata as m; from agent_framework import Agent; from agent_framework.openai import OpenAIChatClient; print('core',m.version('agent-framework-core'),'openai',m.version('agent-framework-openai'),'imports OK')"
    if ($LASTEXITCODE -ne 0) { throw "Fallo al importar Microsoft Agent Framework" }
    & $mafPython -m pip check
    if ($LASTEXITCODE -ne 0) { throw "Dependencias incorrectas en Microsoft Agent Framework" }

    Write-Output "ALL_OK"
}
finally {
    $env:CREWAI_STORAGE_DIR = $previousCrewAIStorage
    $env:LOCALAPPDATA = $previousLocalAppData
}
