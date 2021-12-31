import threading
from queue import Queue, Empty
from .server_command import ServerCommand
from . import config, socket_common
import socket, threading

class SocketRequestResponseServer:
    def __init__(self, address : str, port : int, command_queue : Queue) -> None:
        self.address = address
        self.port = port
        self.command_queue = command_queue
        self.queue_timeout = config.REQUEST_TIMEOUT

    def run(self):
        accepting_thread = threading.Thread(target=self.accepting_thread_func, daemon=True)
        accepting_thread.start()

    def accepting_thread_func(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.address, self.port))
            s.listen(5)
            while True:
                conn, addr = s.accept()
                conn_thread = threading.Thread(target=self.conn_thread_func, args=(conn, addr), daemon=True)
                conn_thread.start()
    
    def conn_thread_func(self, conn, addr):
        try:
            with conn:
                self.connection_loop(conn, addr)
        except socket_common.ConnectionBrokenError as err:
            print(f"Connection from {addr} broken")
            print(err)
        except Exception as err:
            print(err)
    
    def connection_loop(self, conn, addr):
        print(f"Accepted connection from {addr}")
        remaining = ""
        while True:
            obj, remaining = socket_common.recv_json(conn, remaining)
            print(f"Message from {addr}")
            print(obj)
            # command = ServerCommand(description=obj, response_queue=Queue())
            # self.command_queue.put(command)
            # response = command.response_queue.get(timeout=self.queue_timeout)
            response = self.execute_command(obj)
            socket_common.send_json(conn, response)

    def execute_command(self, obj):
        try:
            command = ServerCommand(description=obj, response_queue=Queue())
            self.command_queue.put(command)
            response = command.response_queue.get(timeout=self.queue_timeout)
            return response
        except Empty:
            print("Queue timeout!")
            return self.timeout_error_response(command)

    def timeout_error_response(self, command : ServerCommand):
        response = {"type":"response","status":"error", "message":"Operation timed out"}
        if "name" in command.description:
            response["name"] = command.description["name"]
        return response
