import socket, threading
from queue import Queue
from . import socket_common

class SocketNotifyServer:
    def __init__(self, address : str, port : int, notify_queue : Queue) -> None:
        self.address = address
        self.port = port
        self.notify_queue = notify_queue
        self.connections = []
        self.connection_list_lock = threading.Lock()

    def run(self):
        print("Notify server: starting")
        accepting_thread = threading.Thread(target=self.accepting_thread_func, daemon=True)
        accepting_thread.start()
    
    def accepting_thread_func(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.address, self.port))
            s.listen(5)
            notify_thread = threading.Thread(target=self.notify_thread_func, daemon=True)
            notify_thread.start()
            while True:
                print("Notify server: waiting for accept")
                conn, addr = s.accept()
                self.add_connection(conn)

    def notify_thread_func(self):
        while True:
            notification = self.notify_queue.get()
            self.notify_all(notification)

    def add_connection(self, connection):
        with self.connection_list_lock:
            self.connections.append(connection)

    def remove_connection(self, connection):
        with self.connection_list_lock:
            self.remove_connection_no_lock(connection)

    def remove_connections(self, connections):
        with self.connection_list_lock:
            self.remove_connections_no_lock(connections)

    def remove_connections_no_lock(self, connections):
        for connection in connections:
            self.remove_connection_no_lock(connection)
    
    def remove_connection_no_lock(self, connection):
        for i, conn in enumerate(self.connections):
            if conn is connection:
                self.connections.pop(i)
    
    def notify_all(self, notification):
        with self.connection_list_lock:
            connections_to_remove = []
            for conn in self.connections:
                success = self.send_notification_to_connection(notification, conn)
                if not success:
                    connections_to_remove.append(conn)
            self.remove_connections_no_lock(connections_to_remove)

    def send_notification_to_connection(self, notification, connection) -> bool:
        try:
            socket_common.send_json(connection, notification)
            return True
        except Exception as err:
            print(err)
            return False