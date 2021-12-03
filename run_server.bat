@echo off
call .\venv\Scripts\activate.bat
pushd webserver
start "" run_server.py
popd
pushd receiver
start "" xbee_device_server.py
popd
call deactivate
echo Everything started successfully.