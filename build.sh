#!/bin/bash
# Build script for SnakeJack
set -e

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -e .
pip install -e ".[dev]"
echo "Build complete."
