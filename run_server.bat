@echo off
call .\venv\Scripts\activate.bat
pushd webserver
start "" run_server.py
popd
start "" python -m receiver.xbee_device_server
call deactivate
echo Everything started successfully.