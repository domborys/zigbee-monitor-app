import config
import base64
import logging
from xbee_device_connection import XBeeDeviceConnection
from request_response_server import SocketRequestResponseServer
from notify_server import SocketNotifyServer
from server_command import ServerCommand
from queue import Queue
import xbee_device_connection
from digi.xbee.devices import XBeeDevice              

def test_local(xbee_connection):
    command_queue = xbee_connection.command_queue
    message = base64.b64encode(b"Lubie placki").decode()
    commands = [
        ServerCommand(description={"type":"request", "name":"discover"}, response_queue=Queue()),
        ServerCommand(description={"type":"request", "name":"wait", "data":{"time":4}}, response_queue=Queue()),
        ServerCommand(description={"type":"request", "name":"send", "data":{"address64":"0013A200418D05FC", "message":message}}, response_queue=Queue())
    ]
    for command in commands:
        command_queue.put(command)
    for command in commands:
        response = command.response_queue.get()
        print("Request", command.description)
        print("Response", response)
    
    command_stop = ServerCommand(description={"type":"request", "name":"stop"}, response_queue=Queue())
    command_queue.put(command_stop)

def configure_xbee_logger(logger_name, file_name):
    dev_logger = logging.getLogger(logger_name)
    dev_logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(file_name)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    dev_logger.addHandler(handler)

def configure_xbee_loggers():
    log_file_name = "../log/xbee_lib.log"
    configure_xbee_logger("digi.xbee.devices", log_file_name)
    configure_xbee_logger("digi.xbee.sender", log_file_name)
    configure_xbee_logger("digi.xbee.reader", log_file_name)
    configure_xbee_logger("digi.xbee.recovery", log_file_name)
    configure_xbee_logger("digi.xbee.firmware", log_file_name)
    configure_xbee_logger("digi.xbee.profile", log_file_name)
    configure_xbee_logger("digi.xbee.models.zdo", log_file_name)

def configure_custom_loggers():
    conn_logger = logging.getLogger(xbee_device_connection.__name__)
    conn_logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler("../log/device.log")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    conn_logger.addHandler(handler)

def configure_loggers():
    configure_xbee_loggers()
    configure_custom_loggers()

def check_device_config():
    if(config.DEVICE_SERIAL_PORT is None):
        raise RuntimeError("Device serial port not specified")




def main():
    configure_loggers()
    check_device_config()
    device = XBeeDevice(config.DEVICE_SERIAL_PORT, config.DEVICE_BAUD_RATE)
    xbee_connection = XBeeDeviceConnection(device)
    xbee_connection.run()
    # test_local()
    request_server = SocketRequestResponseServer(config.IP_ADDRESS, config.TCP_PORT_REQUEST, xbee_connection.command_queue)
    request_server.run()
    notification_server = SocketNotifyServer(config.IP_ADDRESS, config.TCP_PORT_NOTIFY, xbee_connection.notify_queue)
    notification_server.run()

    input()


if __name__ == "__main__":
    main()