from dataclasses import dataclass
from queue import Queue

@dataclass
class ServerCommand:
    description: dict
    response_queue: Queue