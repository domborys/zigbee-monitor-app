"""The module defining the class used for handling requests and sending responses to the client.
"""

import threading
from queue import Queue, Empty
from .server_command import ServerCommand
from . import config, socket_common
import socket, threading

class SocketRequestResponseServer:
    """A server which receives requests form the client and sends the responses.
    
    It ses a request-response model.
    It opens a socket, to which the clients can connect.
    After the clients connect they can send a request to the server.
    The server processes the requests ands sends a response to the client.

    Attributes:
        address (str): IP Address on which the socket will listen.
        port (str): TCP port on which the socket will listen.
        command_queue (Queue): The queue into which the server puts the commands for the device.
            The commands are objects of the class :class:`~receiver.server_command.ServerCommand`.
        queue_timeout (float): Maximum processing time of the request. It depends
    """

    def __init__(self, address : str, port : int, command_queue : Queue) -> None:
        """Creates a server.

        Args:
            address: IP Address on which the socket will listen.
            port: TCP port on which the socket will listen.
            notify_queue:  The queue into which the server puts the commands for the device.
        """
        self.address = address
        self.port = port
        self.command_queue = command_queue
        self.queue_timeout = config.REQUEST_TIMEOUT

    def run(self):
        """Starts the server. The server is run in another daemon thread."""

        accepting_thread = threading.Thread(target=self._accepting_thread_func, daemon=True)
        accepting_thread.start()

    def _accepting_thread_func(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.address, self.port))
            s.listen(5)
            while True:
                conn, addr = s.accept()
                conn_thread = threading.Thread(target=self._conn_thread_func, args=(conn, addr), daemon=True)
                conn_thread.start()
    
    def _conn_thread_func(self, conn, addr):
        try:
            with conn:
                self._connection_loop(conn, addr)
        except socket_common.ConnectionBrokenError as err:
            print(f"Connection from {addr} broken")
            print(err)
        except Exception as err:
            print(err)
    
    def _connection_loop(self, conn, addr):
        print(f"Accepted connection from {addr}")
        remaining = ""
        while True:
            obj, remaining = socket_common.recv_json(conn, remaining)
            print(f"Message from {addr}")
            print(obj)
            response = self._execute_command(obj)
            socket_common.send_json(conn, response)

    def _execute_command(self, obj):
        try:
            command = ServerCommand(description=obj, response_queue=Queue())
            self.command_queue.put(command)
            response = command.response_queue.get(timeout=self.queue_timeout)
            return response
        except Empty:
            print("Queue timeout!")
            return self._timeout_error_response(command)

    def _timeout_error_response(self, command : ServerCommand):
        response = {"type":"response","status":"error", "message":"Operation timed out"}
        if "name" in command.description:
            response["name"] = command.description["name"]
        return response
