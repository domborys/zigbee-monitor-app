"""A module which sets up the coordinator handler. It is intended to run as main."""

import logging, logging.config, signal, sys, time, json
from digi.xbee.devices import XBeeDevice   
from . import config
from .xbee_device_connection import XBeeDeviceConnection
from .request_response_server import SocketRequestResponseServer
from .notify_server import SocketNotifyServer

def _configure_loggers():
    with open("receiver/logconfig.json", "r") as fp:
        logging.config.dictConfig(json.load(fp))

def _check_device_config():
    if(config.DEVICE_SERIAL_PORT is None):
        logging.getLogger(__name__).error("Device serial port not specified in receiver/custom_config.py.")
        raise RuntimeError("Device serial port not specified")

def _sigint_handler(signum, frame):
    print("XBee server exits.")
    sys.exit(0)

def main():
    """The main function of the coordinator handler. It is executed automatically when the module is run as main.

    The function opens a serial port for communication with the XBee coordinator device and starts two servers:
    one for handling request-response communitaions and the other one for sending notifications of the received messages.

    Internally, it setups and starts the following objects:
    - one :class:`~receiver.xbee_device_connection.XBeeDeviceConnection`
    - one :class:`~receiver.request_response_server.SocketRequestResponseServer`
    - one :class:`~receiver.notify_server.SocketNotifyServer`

    """
    signal.signal(signal.SIGINT, _sigint_handler)
    _configure_loggers()
    _check_device_config()
    device = XBeeDevice(config.DEVICE_SERIAL_PORT, config.DEVICE_BAUD_RATE)
    xbee_connection = XBeeDeviceConnection(device)
    xbee_connection.start()
    xbee_connection.connection_startup_finished.wait()
    if not xbee_connection.connection_startup_successful.is_set():
        print("Couldn't connect to the XBee device.")
        return
    print("Successfully connected to the XBee device.")
    request_server = SocketRequestResponseServer(config.IP_ADDRESS, config.TCP_PORT_REQUEST, xbee_connection.command_queue)
    request_server.run()
    notification_server = SocketNotifyServer(config.IP_ADDRESS, config.TCP_PORT_NOTIFY, xbee_connection.notify_queue)
    notification_server.run()
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()