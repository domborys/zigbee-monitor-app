@echo off
pushd webserver
start "" run_server.py
popd
pushd receiver
start "" xbee_device_server.py
popd