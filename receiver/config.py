# Please DO NOT modify this file. It's a default config file.
# Instead, copy the setting you want to change into custom_config.py and edit it there.

"""A module providing the configuration for the modules of the :mod:`receiver` package.

.. note::
    All the values provided in this documentation are the default values. The defaults may be overridden by the values from :mod:`~receiver.custom_config`.
    This module file should not be modified by the users. Custom values can be provided in :mod:`~receiver.custom_config`.
"""
 
#: TCP port for the socket used for making request to the coordinator handler.
TCP_PORT_REQUEST = 9020

#: TCP port for the socket used for sending notifications from coordinator handler.
TCP_PORT_NOTIFY = 9021

#: IP address on which the sockets are listening.
IP_ADDRESS = '127.0.0.1'

#: Serial port used for communication with the coordinator.
#: This value must be set in the custom_config.py.
#: The default value (None) will cause an error on the startup of coordinator handler.
DEVICE_SERIAL_PORT = None

#: Baud rate for the serial port used for communication with the coordinator.
DEVICE_BAUD_RATE = 9600

#: Timeout for processing requests arriving at the TCP_PORT_REQUEST port.
REQUEST_TIMEOUT = 25

try:
    from .custom_config import *
except ImportError:
    pass