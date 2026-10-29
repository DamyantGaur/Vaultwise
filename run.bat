@echo off
rem Vaultwise launcher: checks Python, packages, Ollama and models, starts the app and opens the browser.
rem Usage:  run.bat            or   run.bat -Port 8001   or   run.bat -NoBrowser
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0run.ps1" %*
