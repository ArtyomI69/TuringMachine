@echo off

rem Check if venv folder exists
if not exist venv (
    echo Virtual environment does not exist. Creating...
    python -m venv venv
    echo Virtual environment created.
    
    rem Activate the virtual environment
    echo Activating venv
    venv\Scripts\activate.bat
    echo Activated venv

    set env_active=true
    rem Install packages from requirements.txt
    echo Installing packages
    pip install -r requirements.txt
    echo Installed packages
    
    echo Deactivating venv
    deactivate
    echo Deactivated venv
)

rem Launch the app
echo Launching app
.\venv\Scripts\python.exe .\app\main_window.py
echo Exited app