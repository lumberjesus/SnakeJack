#!/bin/bash
# Package script for SnakeJack
set -e

# Remove previous build/dist if present
rm -rf dist build *.egg-info

# Create source distribution and wheel
python3 setup.py sdist bdist_wheel

echo "Package complete. Output in dist/ directory."
