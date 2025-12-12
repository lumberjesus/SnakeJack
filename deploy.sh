#!/bin/bash
# Deploy script for SnakeJack
set -e

VM_USER=jack
VM_IP=40.82.178.116
REMOTE_DIR="/home/jack/snakejack_deploy"

# Build and package locally
./build.sh
./package.sh

# Create remote directory and copy files (combine with a single SSH connection using ControlMaster)
ssh -o ControlMaster=auto -o ControlPath=~/.ssh/cm-%r@%h:%p -o ControlPersist=10m ${VM_USER}@${VM_IP} "mkdir -p ${REMOTE_DIR}"
scp -o ControlPath=~/.ssh/cm-%r@%h:%p -r dist src setup.py README.md setup.sh src/snakejack/web/templates src/snakejack/web/static ${VM_USER}@${VM_IP}:${REMOTE_DIR}/

# Install prerequisites, kill any process on port 5000, and run on remote VM
ssh -o ControlPath=~/.ssh/cm-%r@%h:%p ${VM_USER}@${VM_IP} "
  cd /home/jack/snakejack_deploy && \
  bash setup.sh && \
  fuser -k 5000/tcp || true && \
  python3 -m venv venv && \
  source venv/bin/activate && \
  rm -rf venv/lib/python*/site-packages/snakejack* src/snakejack.egg-info && \
  pip install --upgrade pip && \
  pip install --force-reinstall dist/*.whl && \
  nohup python3 -m snakejack.web > web.log 2>&1 < /dev/null &
  sleep 2
  if pgrep -f 'python3 -m snakejack.web' > /dev/null; then
    echo 'SnakeJack deployed and running on port 5000.'
  else
    echo 'ERROR: SnakeJack did not start. Check web.log for details:'
    tail -20 web.log
    exit 1
  fi
  exit 0
"
# Close the SSH master connection
ssh -O exit -o ControlPath=~/.ssh/cm-%r@%h:%p ${VM_USER}@${VM_IP}
