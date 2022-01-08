"""A module which sets up the coordinator handler. It is intended to run as main."""

import base64, logging, signal, sys, time
from pathlib import Path
from queue import Queue
from digi.xbee.devices import XBeeDevice   
from . import config, xbee_device_connection
from .xbee_device_connection import XBeeDeviceConnection
from .request_response_server import SocketRequestResponseServer
from .notify_server import SocketNotifyServer

def _configure_xbee_logger(logger_name, file_name):
    dev_logger = logging.getLogger(logger_name)
    dev_logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(file_name)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    dev_logger.addHandler(handler)

def _configure_xbee_loggers():
    log_file_name = str(Path(__file__).parent.parent / "log" / "xbee_lib.log")
    _configure_xbee_logger("digi.xbee.devices", log_file_name)
    _configure_xbee_logger("digi.xbee.sender", log_file_name)
    _configure_xbee_logger("digi.xbee.reader", log_file_name)
    _configure_xbee_logger("digi.xbee.recovery", log_file_name)
    _configure_xbee_logger("digi.xbee.firmware", log_file_name)
    _configure_xbee_logger("digi.xbee.profile", log_file_name)
    _configure_xbee_logger("digi.xbee.models.zdo", log_file_name)

def _configure_custom_loggers():
    conn_logger = logging.getLogger(xbee_device_connection.__name__)
    conn_logger.setLevel(logging.DEBUG)
    logger_file_path = str(Path(__file__).parent.parent / "log" / "device.log")
    handler = logging.FileHandler(logger_file_path)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    conn_logger.addHandler(handler)

def _configure_loggers():
    _configure_xbee_loggers()
    _configure_custom_loggers()

def _check_device_config():
    if(config.DEVICE_SERIAL_PORT is None):
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
        print("Couldn't connect to the device")
        return
    request_server = SocketRequestResponseServer(config.IP_ADDRESS, config.TCP_PORT_REQUEST, xbee_connection.command_queue)
    request_server.run()
    notification_server = SocketNotifyServer(config.IP_ADDRESS, config.TCP_PORT_NOTIFY, xbee_connection.notify_queue)
    notification_server.run()
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()