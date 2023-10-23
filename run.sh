#!/bin/bash

# Check if venv folder exists
if [ ! -d "venv" ]; then
    echo "Virtual environment does not exist. Creating..."
    python3 -m venv venv
    echo "Virtual environment created."
    
    # Install packages from requirements.txt
    echo "Installing packages"
    venv/bin/pip install -r requirements.txt
    echo "Installed packages"
fi

# Launch the app
echo "Launching app"
venv/bin/python app/main_window.py
echo "Exited app"