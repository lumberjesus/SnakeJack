#!/bin/bash
# Setup prerequisites for Ubuntu server for SnakeJack deployment
set -e

sudo apt update
sudo apt install -y python3 python3-pip python3-venv build-essential

echo "System prerequisites installed. You can now run deploy.sh."
