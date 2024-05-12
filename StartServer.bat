@echo off
setlocal

rem Setze den Pfad zur virtuellen Umgebung (venv)
set "VENV_PATH=.venv\Scripts"

rem Führe das Streamlit-Skript aus
"%VENV_PATH%\streamlit" run "Webapp.py"

endlocal
