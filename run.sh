#!/bin/bash

env_active=false

# Check if venv folder exists
if [ ! -d "venv" ]; then
    echo "Virtual environment does not exist. Creating..."
    python -m venv venv
    echo "Virtual environment created."
    
    # Activate the virtual environment
    source venv/Scripts/activate
    env_active=true
    
    # Install packages from requirements.txt
    pip install -r requirements.txt
fi

if [ "$env_active" = false ]; then
    source venv/Scripts/activate
fi

# Launch the app
python3 app/main_window.py

# Deactivate the virtual environment
deactivate