"""An example client of the coordinator controller

It demonstrates the method of making requests to the server, receiving responses and notifications.
"""

import socket, base64, threading
from . import socket_common, config

def main() -> None:
    """The main function of the client

    It sets up the thread for receiving notifications,
    then it sequentially makes a requests and waits for response
    for every requests returned by the :func:`~receiver.example_client.prepare_some_requests`
    
    """
    threading.Thread(target=notifications_thread_func).start()
    requests = prepare_some_requests()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((config.IP_ADDRESS, config.TCP_PORT_REQUEST))
        remaining = ""
        for request in requests:
            print("Request:", request)
            socket_common.send_json(s, request)
            response, remaining = socket_common.recv_json(s, remaining)
            print("Response:", response)
        s.close()

def prepare_some_requests() -> list[dict]:
    """The function returns some example requests to the coordinator controller.

    Returns:
        A list of three request dicts.
    
    """
    message = base64.b64encode(b"Lubie placki").decode()
    requests = [
        {"type":"request", "name":"discover"},
        {"type":"request", "name":"wait", "data":{"time":4}},
        {"type":"request", "name":"send", "data":{"address64":"0013A200418D05FC", "message":message}}
    ]
    return requests

def notifications_thread_func() -> None:
    """The function for receiving notificatione, i.e. received messages from the coordinator controller.
    It should run in a separate thread.

    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((config.IP_ADDRESS, config.TCP_PORT_NOTIFY))
        remaining = ""
        while True:
            notification, remaining = socket_common.recv_json(s, remaining)
            print("Response:", notification)

if __name__ == "__main__":
    main()