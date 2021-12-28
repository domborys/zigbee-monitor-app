import socket, json

class ConnectionBrokenError(Exception):
    pass

def send_json(sock : socket.socket, obj) -> None:
    """Sends a dict to the socket.

    Based on: https://docs.python.org/3/howto/sockets.html
    """

    #\n is the message delimiter. It will not be confused with JSON contents, because the line feed byte cannot appear inside JSON
    msg_str = json.dumps(obj) + "\n"
    msg = msg_str.encode('utf-8')
    msglen = len(msg)
    totalsent = 0
    while totalsent < msglen:
        sent = sock.send(msg[totalsent:])
        if sent == 0:
            raise ConnectionBrokenError("Socket connection broken")
        totalsent += sent

def recv_json(sock : socket.socket, prev_data : str = ""):
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
