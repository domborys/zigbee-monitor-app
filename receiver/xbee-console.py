import threading
import time
from queue import Queue
from digi.xbee.devices import XBeeDevice, XBeeNetwork, RemoteXBeeDevice
from digi.xbee.exception import XBeeException
from digi.xbee.models.address import XBee16BitAddress, XBee64BitAddress

class ConsoleCommand:
    def __init__(self, command : str):
        self.parse_command(command)
    def parse_command(self, command : str):
        split_result = command.split()
        self.name = split_result[0]
        self.arguments = None
        self.parse_arguments(split_result)
        
    def parse_arguments(self, split_result : list):
        com = self.name
        if com == "discover":
            self.arguments = None
        elif com == "send":
            self.arguments = {
                "addr": split_result[1],
                "msg" : " ".join(split_result[2::])
            }
        elif com == "quit":
            self.arguments = None
    def get_name(self):
        return self.name
    def get_arguments(self):
        return self.arguments


def console_thread_func(command_queue : Queue):
    while True:
        line = input()
        command = ConsoleCommand(line)
        command_queue.put(command)

def xbee_thread_func(command_queue : Queue):
    device = XBeeDevice("COM3", 9600)
    try:
        device.open()
        device.add_data_received_callback(data_received_callback)
        xbee_thread_loop(command_queue, device)
    except XBeeException as err:
        print(err)
    finally:
        if device is not None and device.is_open():
            device.close()

def data_received_callback(xbee_message):
    address = xbee_message.remote_device.get_64bit_addr()
    data = xbee_message.data.decode("utf8")
    print("Received data from %s: %s" % (address, data))

def xbee_thread_loop(command_queue : Queue, device : XBeeDevice):
    
    while True:
        command = command_queue.get()
        name = command.get_name()
        arguments = command.get_arguments()
        if name == "quit":
            return
        elif name == "discover":
            execute_discover_command(device)
        elif name == "send":
            execute_send_command(device, arguments)

def execute_discover_command(device : XBeeDevice):
    print("Starting discovery...")
    xnet = discover_network(device)
    print_network(xnet)

def discover_network(device : XBeeDevice):
    xnet = device.get_network()
    xnet.start_discovery_process(deep=True, n_deep_scans=1)
    while xnet.is_discovery_running():
        time.sleep(0.5)
    return xnet

def print_network(xnet : XBeeNetwork):
    nodes = xnet.get_devices()
    print("Discovered nodes:")
    for node in nodes:
        print("{} {}".format(node.get_64bit_addr(), node.get_node_id()))

def execute_send_command(device : XBeeDevice, arguments):
    try:
        remote_device = RemoteXBeeDevice(device, XBee64BitAddress.from_hex_string(arguments["addr"]))
        device.send_data(remote_device, arguments["msg"])
        print("Data successfully sent.")
    except TimeoutError as err:
        print(err)
    except XBeeException as err:
        print(err)

if __name__ == "__main__":
    command_queue = Queue()
    console_thread = threading.Thread(target=console_thread_func, args=(command_queue,), daemon=True)
    xbee_thread = threading.Thread(target=xbee_thread_func, args=(command_queue,))
    console_thread.start()
    xbee_thread.start()
    xbee_thread.join()
    print("Bye bye!")
    
