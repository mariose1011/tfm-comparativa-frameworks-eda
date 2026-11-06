@echo off
setlocal
cd /d "%~dp0\..\.."
".\frameworks\crewai\.venv\Scripts\python.exe" -m frameworks.crewai.adaptador_experimento %*
endlocal

