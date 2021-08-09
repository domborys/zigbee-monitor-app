import threading
from queue import Queue
from server_command import ServerCommand

import socket, threading
import socket_common

class SocketRequestResponseServer:
    def __init__(self, address : str, port : int, command_queue : Queue) -> None:
        self.address = address
        self.port = port
        self.command_queue = command_queue

    def run(self):
        accepting_thread = threading.Thread(target=self.accepting_thread_func)
        accepting_thread.start()

    def accepting_thread_func(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.address, self.port))
            s.listen(5)
            while True:
                conn, addr = s.accept()
                conn_thread = threading.Thread(target=self.conn_thread_func, args=(conn, addr))
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
            command = ServerCommand(description=obj, response_queue=Queue())
            self.command_queue.put(command)
            response = command.response_queue.get()
            socket_common.send_json(conn, response)