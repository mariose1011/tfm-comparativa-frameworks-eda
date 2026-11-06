@echo off
setlocal
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
cd /d "%~dp0\..\.."
".\frameworks\microsoft_agent_framework\.venv\Scripts\python.exe" -m frameworks.microsoft_agent_framework.adaptador_experimento %*
endlocal

