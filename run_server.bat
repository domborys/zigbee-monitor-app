@echo off
call .\venv\Scripts\activate.bat
pushd webserver
start "" py run_server.py
popd
start "" py -m receiver.xbee_device_server
call deactivate
echo Everything started successfully.