#!/bin/bash
# Build script for SnakeJack
set -e

# Detect Python command (python3 on Mac/Linux, python on Windows)
# On Windows with Git Bash, bypass App Execution Aliases by using python.exe directly
if command -v python.exe &> /dev/null; then
    PYTHON=python.exe
elif command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    PYTHON=python
else
    echo "Error: Python not found. Please install Python 3.7+"
    exit 1
fi

echo "Using Python: $PYTHON"

$PYTHON -m venv venv

# Activate venv (different path on Windows vs Mac/Linux)
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Use python -m pip to avoid permission issues on Windows
python -m pip install --upgrade pip || true
python -m pip install -e .
python -m pip install -e ".[dev]" || true
echo "Build complete."
