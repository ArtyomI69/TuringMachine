#/bin/bash

# Check if venv folder exists
if [ ! -d "venv" ]; then
    echo "Virtual environment does not exist. Creating..."
    python3 -m venv venv
    echo "Virtual environment created."
    
    # Activate the virtual environment
    echo "Activating venv"
    source venv/bin/activate
    echo "Activated venv"
    
    # Install packages from requirements.txt
    echo "Installing packages"
    pip install -r requirements.txt
    echo "Installed packages"
    
    # Deactivate the virtual environment
    echo "Deactivating venv"
    deactivate
    echo "Deactivated venv"
fi

# Launch the app
echo "Launching app"
venv/bin/python app/main_window.py
echo "Exited app"