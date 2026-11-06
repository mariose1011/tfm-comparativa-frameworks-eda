@echo off
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0verify_installations.ps1"
exit /b %errorlevel%
