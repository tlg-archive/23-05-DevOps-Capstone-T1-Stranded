#!/bin/bash

# Specify the desired Python version
desired_python_version="3.9.6"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install it."
    exit 1
fi

# Get the installed Python 3 version
installed_python_version=$(python3 --version 2>&1 | awk '{print $2}')

# Compare the installed Python version with the desired version
if [ "$installed_python_version" != "$desired_python_version" ]; then
    echo "Python $desired_python_version is not installed or not the default Python version."
    exit 1
fi

# Install Python packages from requirements.txt
python3 -m pip install -r requirements.txt

# Run stranded.py with Python 3
python3 stranded.py
