#!/bin/bash
trap 'kill $(jobs -p) && echo "Servers stopped"' EXIT
source ./venv/bin/activate
python3 -m webserver.run_server &
python3 -m receiver.xbee_device_server &
deactivate
echo "Startup complete."
wait



