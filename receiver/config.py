TCP_PORT_REQUEST = 60001
TCP_PORT_NOTIFY = 60002
IP_ADDRESS = '127.0.0.1'
DEVICE_SERIAL_PORT = None
DEVICE_BAUD_RATE = 9600
REQUEST_TIMEOUT = 25

try:
    from custom_config import *
except ImportError:
    pass