#!/bin/bash
# Package script for SnakeJack
set -e

# Activate venv (different path on Windows vs Mac/Linux)
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Remove previous build/dist if present
rm -rf dist build *.egg-info

# Ensure build dependencies are installed
python -m pip install --upgrade build wheel setuptools

# Create source distribution and wheel using modern build
python -m build

echo "Package complete. Output in dist/ directory."
