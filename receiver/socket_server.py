import socket, threading
from . import socket_common

ADDRESS = '127.0.0.1'
PORT = 34567

def conn_thread_func(conn, addr):
    try:
        with conn:
            print(f"Accepted connection from {addr}")
            remaining = ""
            while True:
                obj, remaining = socket_common.recv_json(conn, remaining)
                print(f"Message from {addr}")
                print(obj)
    except socket_common.ConnectionBrokenError as err:
        print(f"Connection from {addr} broken")
        print(err)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((ADDRESS, PORT))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        conn_thread = threading.Thread(target=conn_thread_func, args=(conn, addr))
        conn_thread.start()
