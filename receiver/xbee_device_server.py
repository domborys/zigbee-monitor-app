import xbee_device_server_config as config
import base64
from xbee_device_connection import XBeeDeviceConnection
from request_response_server import SocketRequestResponseServer
from notify_server import SocketNotifyServer
from server_command import ServerCommand
from queue import Queue
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

def main():
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