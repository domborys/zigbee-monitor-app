"""The coordinator handler package.

It handles communication with the XBee device which is the coordinator of a ZigBee network.

To start the coordinator handler, run :mod:`receiver.xbee_device_server` as module.


Windows example::

    C:\\zigbee-monitor-app> .\\venv\\Scripts\\activate.bat
    (venv) C:\\zigbee-monitor-app> py -m receiver.xbee_device_server

Linux example::

    ~/zigbee-monitor-app$ source venv/bat/activate
    (venv) ~/zigbee-monitor-app$ python3 -m receiver.xbee_device_server
"""