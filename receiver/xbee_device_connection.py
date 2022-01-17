"""Module defining the class communicating with the device."""

import threading, time, base64, logging, json
from queue import Queue
from typing import Callable, Optional
from .server_command import ServerCommand
from digi.xbee.devices import XBeeDevice, XBeeNetwork, RemoteXBeeDevice
from digi.xbee.models.address import XBee64BitAddress

class XBeeDeviceConnection:
    """Connection object which manages the communication with a XBee device.

    Attributes:
        device (digi.xbee.devices.XBeeDevice): the device on which the commands will be executed.
        command_queue (queue.Queue): the queue from which the object will get the commands to execute on the device.
        notify_queue (queue.Queue): the queue to which the connection object will send the received messages.
        connection_startup_finished (threading.Event): an event which is set when the device startup procedure is finished.
            It may be set when the device is properly configured but it may be set when an error occurs during startup.
            To check if the startup was successful check the `connection_startup_finished` event.
        connection_startup_successful (threading.Event): an event set after a successful startup of the device.

    """

    def __init__(self, device : XBeeDevice, command_queue : Optional[Queue] = None, notify_queue : Optional[Queue] = None) -> None:
        """Creates the connection object.

        Args:
            device: the device on which the commands will be executed.
            command_queue: the queue from which the object will get the commands to execute on the device.
                If set to None, the queue will be created automatically.
            notify_queue: the queue to which the connection object will send the received messages.
                If set to None, the queue will be created automatically.
        """
        self.device = device
        self.command_queue = Queue() if command_queue is None else command_queue
        self.notify_queue = Queue() if notify_queue is None else notify_queue
        self._configure_logger()
        self.connection_startup_finished = threading.Event()
        self.connection_startup_successful = threading.Event()
    
    def start(self) -> None:
        """Starts the handler.
        
        When this method is called, the serial connection will be opened.
        After that, the handler will start to:
        - process commands from the command_queue
        - put received messages into notify_queue
        """
        self.thread = threading.Thread(target=self._thread_func, daemon=True)
        self.thread.start()
    
    def _thread_func(self) -> None:
        self.logger.debug("Device connection thread started.")
        try:
            self.device.open()
            self.logger.info("Device connection opened.")
            self.device.add_data_received_callback(self._data_received_callback)
            self.connection_startup_successful.set()
            self.connection_startup_finished.set()
            self._thread_loop()
        except Exception as err:
            self.logger.error("Error in device thread: %s", err)
        finally:
            if self.device is not None and self.device.is_open():
                self.device.close()
                self.logger.info("Device connection closed.")
            self.logger.debug("Device connection thread stopped.")
            self.connection_startup_finished.set()
    
    def _thread_loop(self):
        while True:
            command = self.command_queue.get()
            if command.description["name"] == "stop":
                self._log_command_begin(command)
                break
            self._execute_command_and_put_result(command)

    def _execute_command_and_put_result(self, command : ServerCommand):
        try:
            self._log_command_begin(command)
            result = self._execute_command(command)
            command.response_queue.put({"type":"response","status":"ok","name":command.description["name"], "data":result})
            self._log_command_successful(command, result)
        except Exception as err:
            command.response_queue.put({"type":"response","status":"error","name":command.description["name"], "message":str(err)})
            self._log_command_error(command, err)

    def _execute_command(self, command : ServerCommand) -> dict:
        name = command.description["name"]
        if name == "discover":
            return self._command_discover(command)
        elif name == "send":
            return self._command_send(command)
        elif name == "get_parameter":
            return self._command_get_parameter(command)
        elif name == "set_parameter":
            return self._command_set_parameter(command)
        elif name == "execute_command":
            return self._command_execute_command(command)
        elif name == "wait":
            return self._command_wait(command)
        else:
            raise RuntimeError(f'Unrecognized command "{name}"')
        

    def _command_discover(self, command : ServerCommand) -> dict:
        xnet = self._discover_network()
        result = self._format_discovery_result(xnet)
        return result

    def _discover_network(self) -> XBeeNetwork:
        xnet = self.device.get_network()
        xnet.set_deep_discovery_options(del_not_discovered_nodes_in_last_scan=True)
        xnet.start_discovery_process(deep=True, n_deep_scans=1)
        while xnet.is_discovery_running():
            time.sleep(0.2)
        return xnet
    
    def _format_discovery_result(self, xnet : XBeeNetwork) -> dict:
        nodes = xnet.get_devices()
        devices = []
        for node in nodes:
            devices.append(self._format_device_data(node))
        return {"devices": devices}

    def _format_device_data(self, device : XBeeDevice) -> dict:
        return {
            "address64": str(device.get_64bit_addr()),
            "address16": str(device.get_16bit_addr()),
            "id": device.get_node_id(),
            "role": device.get_role().description
        }
    
    def _command_send(self, command : ServerCommand) -> dict:
        data = command.description["data"]
        remote_device = RemoteXBeeDevice(self.device, XBee64BitAddress.from_hex_string(data["address64"]))
        message = base64.b64decode(data["message"])
        self.device.send_data(remote_device, message)
        return {}

    def _command_wait(self, command : ServerCommand) -> dict:
        data = command.description["data"]
        time.sleep(data["time"])
        return {"time":data["time"]}

    def _command_get_parameter(self, command : ServerCommand) -> dict:
        remote_device = RemoteXBeeDevice(self.device, XBee64BitAddress.from_hex_string(command.description["data"]["address64"]))
        return self._at_related_command(command, remote_device.get_parameter)

    def _command_set_parameter(self, command : ServerCommand) -> dict:
        remote_device = RemoteXBeeDevice(self.device, XBee64BitAddress.from_hex_string(command.description["data"]["address64"]))
        return self._at_related_command(command, remote_device.set_parameter)

    def _command_execute_command(self, command : ServerCommand) -> dict:
        remote_device = RemoteXBeeDevice(self.device, XBee64BitAddress.from_hex_string(command.description["data"]["address64"]))
        return self._at_related_command(command, remote_device.execute_command)

    def _at_related_command(self, command : ServerCommand, method : Callable) -> dict:
        data = command.description["data"]
        at_command = data["at_command"]
        value = None if data["value"] is None else base64.b64decode(data["value"])
        apply_changes = data["apply_changes"]
        result = method(at_command, value, apply_changes)
        if result is None:
            return {"result":None}
        else:
            return {"result":base64.b64encode(result).decode()}

    def _data_received_callback(self, xbee_message):
        address = str(xbee_message.remote_device.get_64bit_addr())
        received_data = base64.b64encode(xbee_message.data).decode()
        message_data = {"address64":address, "message":received_data}
        self.notify_queue.put({"type":"notify", "name":"receive", "data":message_data})
        self._log_received_message(message_data)

    def _configure_logger(self):
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.NullHandler())
    
    def _log_command_begin(self, command : ServerCommand):
        self.logger.debug("Started executing command %s", json.dumps(command.description))

    def _log_command_successful(self, command : ServerCommand, result : dict):
        self.logger.info("Executed command %s. Result: %s", json.dumps(command.description), json.dumps(result))

    def _log_command_error(self, command : ServerCommand, error : str):
        self.logger.error("Error while executing command %s: %s", json.dumps(command.description), error)

    def _log_received_message(self, message_data : dict):
        self.logger.info("Received message: %s", json.dumps(message_data))
