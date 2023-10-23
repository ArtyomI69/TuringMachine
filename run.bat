@echo off

rem Check if venv folder exists
if not exist venv (
    echo Virtual environment does not exist. Creating...
    python -m venv venv
    echo Virtual environment created.

    rem Install packages from requirements.txt
    echo Installing packages
    .\venv\Scripts\pip.exe install -r requirements.txt
    echo Installed packages
)

rem Launch the app
echo Launching app
.\venv\Scripts\python.exe .\app\main_window.py
echo Exited app