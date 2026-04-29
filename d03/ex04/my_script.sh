#!/bin/bash

# Create virtualenv named django_venv with python3
python3 -m venv django_venv

# Activate the virtualenv
source django_venv/bin/activate

# Install requirements
pip install -r requirement.txt

echo "Virtual environment 'django_venv' created and activated."
echo "Type 'deactivate' to exit the virtual environment or 'exit' to quit."

# Launch an interactive shell inside the activated virtualenv
$SHELL
