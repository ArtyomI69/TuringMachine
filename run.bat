@echo off

set env_active=false

rem Check if venv folder exists
if not exist venv (
    echo Virtual environment does not exist. Creating...
    python -m venv venv
    echo Virtual environment created.
    
    rem Activate the virtual environment
    venv\Scripts\activate.bat
    set env_active=true
    rem Install packages from requirements.txt
    pip install -r requirements.txt
)

if not %env_active%(
    venv\Scripts\activate.bat
)

rem Launch the app
python3 app\main_window.py

rem Deactivate the virtual environment
deactivate