@echo off
call .\venv\Scripts\activate.bat
start "" py -m webserver.run_server
start "" py -m receiver.xbee_device_server
call deactivate
echo Everything started successfully.