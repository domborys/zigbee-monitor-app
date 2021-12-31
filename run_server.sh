#!/bin/bash
source ./venv/bin/activate
cd webserver
python3 run_server.py &
cd ..
python3 -m receiver.xbee_device_server &
deactivate
echo "Everything started successfully."

