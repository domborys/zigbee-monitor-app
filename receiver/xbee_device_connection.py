import threading, time, base64
from queue import Queue
from typing import Optional
from server_command import ServerCommand
from digi.xbee.devices import XBeeDevice, XBeeNetwork, RemoteXBeeDevice
from digi.xbee.exception import XBeeException
from digi.xbee.models.address import XBee16BitAddress, XBee64BitAddress

class XBeeDeviceConnection:
    
    def __init__(self, device : XBeeDevice, command_queue : Optional[Queue] = None, notify_queue : Optional[Queue] = None) -> None:
        self.device = device
        self.command_queue = Queue() if command_queue is None else command_queue
        self.notify_queue = Queue() if notify_queue is None else notify_queue
    
    def run(self):
        self.thread = threading.Thread(target=self.thread_func)
        self.thread.start()
    
    def thread_func(self):
        try:
            self.device.open()
            self.device.add_data_received_callback(self.data_received_callback)
            self.thread_loop()
        finally:
            if self.device is not None and self.device.is_open():
                self.device.close()
    
    def thread_loop(self):
        while True:
            command = self.command_queue.get()
            if command.description["name"] == "stop":
                break
            self.execute_command_and_put_result(command)

    def execute_command_and_put_result(self, command : ServerCommand):
        try:
            result = self.execute_command(command)
            command.response_queue.put({"type":"response","status":"ok","name":command.description["name"], "data":result})
        except Exception as err:
            command.response_queue.put({"type":"response","status":"error","name":command.description["name"], "message":str(err)})

    def execute_command(self, command : ServerCommand) -> dict:
        name = command.description["name"]
        if name == "discover":
            return self.command_discover(command)
        elif name == "send":
            return self.command_send(command)
        elif name == "wait":
            return self.command_wait(command)
        else:
            raise RuntimeError(f'Unrecognized command "{name}"')
        

    def command_discover(self, command : ServerCommand) -> dict:
        print("Starting discovery...")
        xnet = self.discover_network()
        result = self.format_discovery_result(xnet)
        return result

    def discover_network(self) -> XBeeNetwork:
        xnet = self.device.get_network()
        xnet.start_discovery_process(deep=True, n_deep_scans=1)
        while xnet.is_discovery_running():
            time.sleep(0.2)
        return xnet
    
    def format_discovery_result(self, xnet : XBeeNetwork) -> dict:
        nodes = xnet.get_devices()
        devices = []
        for node in nodes:
            devices.append({"address64": str(node.get_64bit_addr()), "id": node.get_node_id()})
        return {"devices": devices}
    
    def command_send(self, command : ServerCommand) -> dict:
        data = command.description["data"]
        remote_device = RemoteXBeeDevice(self.device, XBee64BitAddress.from_hex_string(data["address64"]))
        message = base64.b64decode(data["message"])
        print("Sending message",message)
        self.device.send_data(remote_device, message)
        return {}

    def command_wait(self, command : ServerCommand) -> dict:
        data = command.description["data"]
        time.sleep(data["time"])
        return {"time":data["time"]}

    def data_received_callback(self, xbee_message):
        address = str(xbee_message.remote_device.get_64bit_addr())
        received_data = base64.b64encode(xbee_message.data).decode()
        message_data = {"address64":address, "data":received_data}
        self.notify_queue.put({"type":"notify", "name":"receive", "data":message_data})