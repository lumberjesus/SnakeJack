#!/bin/bash
# Deploy script for SnakeJack
set -e

VM_USER=jack
VM_IP=40.82.178.116
REMOTE_DIR="/home/jack/snakejack_deploy"

# Build and package locally
./build.sh
./package.sh

echo "Connecting to VM to create directory..."
ssh ${VM_USER}@${VM_IP} "mkdir -p ${REMOTE_DIR}"

echo "Copying files to VM..."
scp -r dist src setup.py README.md setup.sh ${VM_USER}@${VM_IP}:${REMOTE_DIR}/

echo "Installing and starting SnakeJack on VM..."
ssh ${VM_USER}@${VM_IP} << 'ENDSSH'
cd /home/jack/snakejack_deploy
fuser -k 5000/tcp || true
python3 -m venv venv
source venv/bin/activate
rm -rf venv/lib/python*/site-packages/snakejack* src/snakejack.egg-info
pip install --upgrade pip
pip install --force-reinstall dist/*.whl
nohup python3 -m snakejack.web > web.log 2>&1 < /dev/null &
sleep 2
if pgrep -f 'python3 -m snakejack.web' > /dev/null; then
    echo 'SnakeJack deployed and running on port 5000.'
else
    echo 'ERROR: SnakeJack did not start. Check web.log:'
    tail -20 web.log
    exit 1
fi
ENDSSH

# echo ""
# echo "Deploy complete!"
# echo "Press Enter to close this window..."
# read
