"""Module defining various utilities used by other modules"""
import socket, json
from typing import Tuple

class ConnectionBrokenError(Exception):
    """An exception raised when a connection from socket is broken
    while a function is trying to receive or send some data.
    """
    pass

def send_json(sock : socket.socket, obj : dict) -> None:
    """Sends a dict to the socket. The dict is serialized into JSON string and terminated with a newline character.

    Based on: https://docs.python.org/3/howto/sockets.html

    Args:
        sock: socket to which the dict should be sent.
        obj: the dict to send.

    Raises:
        :class:`~receiver.socket_common.ConnectionBrokenError`:
            when the connection with the socket is broken while trying to send the data.
        
    """
    msg_str = json.dumps(obj) + "\n"
    msg = msg_str.encode('utf-8')
    msglen = len(msg)
    totalsent = 0
    while totalsent < msglen:
        sent = sock.send(msg[totalsent:])
        if sent == 0:
            raise ConnectionBrokenError("Socket connection broken")
        totalsent += sent

def recv_json(sock : socket.socket, prev_data : str = "") -> Tuple[dict, str]:
    """Receives a JSON object from the socket and parses it into a dict. The JSON data from the socket must be terminated by a newline character. 

    Based on: https://docs.python.org/3/howto/sockets.html

    Args:
        sock: socket from which the JSON will be received.
        prev_data: the remaining parts of a message previously received from the socket.

    Returns:
        A tuple with two elements
            - The message parsed into a dict
            - The remaining part of the message received from the socket after the terminating newline character.
              When receiving multiple JSONs from one socket the value from the previous call to the function should be supplied as the `prev_data` argument.

    Raises:
        :class:`~receiver.socket_common.ConnectionBrokenError`:
            when the connection with the socket is broken while trying to receive the data.

        :py:class:`json.JSONDecodeError`:
            when the data received is not a valid JSON.
        
    """
    CHUNK_SIZE = 4096
    data = prev_data
    while not '\n' in data:
        chunk = sock.recv(CHUNK_SIZE)
        if len(chunk) == 0:
            raise ConnectionBrokenError("Socket connection broken")
        data += chunk.decode('utf-8')
    pos = data.find('\n')
    data_json = data[:pos]
    loaded_obj = json.loads(data_json)
    remaining_data = data[pos+1:]
    return loaded_obj, remaining_data
