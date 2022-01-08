"""Module defining the :class:`~receiver.server_command.ServerCommand` class."""
from dataclasses import dataclass
from queue import Queue

@dataclass
class ServerCommand:
    """Class used to send commands to the :class:`~receiver.xbee_device_connection.XBeeDeviceConnection`."""

    description: dict
    """The actual request to the controller."""
    
    response_queue: Queue
    """The queue into which a response to the request sould be put."""