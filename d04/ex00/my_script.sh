#!/bin/bash

# Create virtualenv named django_venv with python3
if ! python3 -m venv django_venv >/dev/null 2>&1; then
    python3 -m venv --without-pip django_venv || { echo "Error: failed to create virtual environment."; exit 1; }
    . django_venv/bin/activate
    curl -s https://bootstrap.pypa.io/get-pip.py | python3 || { echo "Error: failed to install pip."; exit 1; }
fi

# Activate the virtualenv
. django_venv/bin/activate

# Install requirements
pip install -r requirements.txt || { echo "Error: failed to install requirements."; exit 1; }

echo "Virtual environment 'django_venv' created and activated."
echo "Type 'deactivate' to exit the virtual environment or 'exit' to quit."

# Launch an interactive shell inside the activated virtualenv
_rc=$(mktemp)
echo ". \"$HOME/.bashrc\" 2>/dev/null; . \"$(pwd)/django_venv/bin/activate\"; rm -f \"$_rc\"" > "$_rc"
exec bash --rcfile "$_rc"

