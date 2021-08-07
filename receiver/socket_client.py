import socket
import socket_common
import time

ADDRESS = '127.0.0.1'
PORT = 34567

data1 = {"type":"foo", "numbers":[1,2,3]}
data2 = {"type":"bar", "numbers":[4,5]}

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ADDRESS, PORT))
        socket_common.send_json(s, data1)
        socket_common.send_json(s, data2)
        s.close()
        time.sleep(3)

