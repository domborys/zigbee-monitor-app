"""The web server package.

It provides static files from the webserver/static folder and API written using the FastApi framework.

To start the Uvicorn server which runs the application run :mod:`webserver.run_server` as module.


Windows example::

    C:\\zigbee-monitor-app> .\\venv\\Scripts\\activate.bat
    (venv) C:\\zigbee-monitor-app> py -m webserver.run_server

Linux example::

    ~/zigbee-monitor-app$ source venv/bat/activate
    (venv) ~/zigbee-monitor-app$ python3 -m webserver.run_server
"""