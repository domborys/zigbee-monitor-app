@echo off
call .\venv\Scripts\activate.bat
start "Uvicorn" py -m webserver.run_server
start "Coordinator handler" py -m receiver.xbee_device_server
call deactivate
echo Startup complete.