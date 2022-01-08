"""The module defining the class used for sending notifications to the client.
"""

import socket, threading
from queue import Queue
from . import socket_common

class SocketNotifyServer:
    """A server which sends notifications of the messages received from the coordinator.
    
    It uses a publish-subscribe model.
    It opens a socket, to which the clients can connect.
    Whenever a message is received, the server sends a notification to all of the clients connected to the socket.

    Attributes:
        address (str): IP Address on which the socket will listen.
        port (str): TCP port on which the socket will listen.
        notify_queue (Queue): the queue from which the server gets the notifications (received messages),
            which will be sent to the clients.
    """

    def __init__(self, address : str, port : int, notify_queue : Queue) -> None:
        """Creates a server.

        Args:
            address: IP Address on which the socket will listen.
            port: TCP port on which the socket will listen.
            notify_queue: the queue from which the server gets the notifications,
                which will be sent to the clients.
        """
        self.address = address
        self.port = port
        self.notify_queue = notify_queue
        self._connections = []
        self._connection_list_lock = threading.Lock()

    def run(self):
        """Starts the server. The server is run in another daemon thread."""

        print("Notify server: starting")
        accepting_thread = threading.Thread(target=self._accepting_thread_func, daemon=True)
        accepting_thread.start()
    
    def _accepting_thread_func(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.address, self.port))
            s.listen(5)
            notify_thread = threading.Thread(target=self._notify_thread_func, daemon=True)
            notify_thread.start()
            while True:
                print("Notify server: waiting for accept")
                conn, addr = s.accept()
                self._add_connection(conn)

    def _notify_thread_func(self):
        while True:
            notification = self.notify_queue.get()
            self._notify_all(notification)

    def _add_connection(self, connection):
        with self._connection_list_lock:
            self._connections.append(connection)

    def _remove_connection(self, connection):
        with self._connection_list_lock:
            self._remove_connection_no_lock(connection)

    def _remove_connections(self, connections):
        with self._connection_list_lock:
            self._remove_connections_no_lock(connections)

    def _remove_connections_no_lock(self, connections):
        for connection in connections:
            self._remove_connection_no_lock(connection)
    
    def _remove_connection_no_lock(self, connection):
        for i, conn in enumerate(self._connections):
            if conn is connection:
                self._connections.pop(i)
    
    def _notify_all(self, notification):
        print(f"Sending notification {notification}")
        with self._connection_list_lock:
            connections_to_remove = []
            for conn in self._connections:
                success = self._send_notification_to_connection(notification, conn)
                if not success:
                    connections_to_remove.append(conn)
            self._remove_connections_no_lock(connections_to_remove)

    def _send_notification_to_connection(self, notification, connection) -> bool:
        try:
            print(f"\t to {connection.getpeername()}")
            socket_common.send_json(connection, notification)
            print(f"\t(sent successfully)")
            return True
        except Exception as err:
            print(err)
            return False