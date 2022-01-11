"""An example client of the coordinator controller used for testing and debugging purposes.

Usage: From the main directory of the project activate the venv and call
`py -m receiver.example_client` (Windows) or `python3 -m receiver.example_client` (Linux)
At the end -p switch may be added. If it's present the script will execute requests from the :func:`~receiver.example_client.prepare_parallel_requests` function,
otherwise it will execute the requests from :func:`~receiver.example_client.prepare_sequential_requests`.
"""

import socket, base64, threading, time, sys
from . import socket_common, config


def prepare_sequential_requests() -> list[dict]:
    """The function returns some example requests to the coordinator controller which should be executed sequentially.

    Returns:
        A list of requests.
    
    """
    message = base64.b64encode(b"Lubie placki").decode()
    requests = [
        {"type":"request", "name":"discover"},
        {"type":"request", "name":"wait", "data":{"time":4}},
        {"type":"request", "name":"send", "data":{"address64":"0013A200418D05FC", "message":message}}
    ]
    return requests

def prepare_parallel_requests() -> list[list[dict]]:
    """The function returns some example requests to the coordinator controller.

    Returns:
        A list with a list of requests.
        The items of the outer lists are called groups. All requests from the previous group should be executed before the requests from the next group.
        Inside each group there is a list of requests. Requests from one group should be exetuted parallelly.
    
    """
    message_ledon = base64.b64encode(b"ledon").decode()
    message_ledoff = base64.b64encode(b"ledoff").decode()
    message_getpot = base64.b64encode(b"getpot").decode()
    requests = [
        [
            {"type":"request", "name":"send", "data":{"address64":"0013A200418D05FC", "message":message_ledon}},
            {"type":"request", "name":"send", "data":{"address64":"0013A200418D05FC", "message":message_getpot}},
            {"type":"request", "name":"discover"},
        ],
        [
            {"type":"request", "name":"wait", "data":{"time":1}},
        ],
        [
            {"type":"request", "name":"send", "data":{"address64":"0013A200418D05FC", "message":message_ledoff}},
            {"type":"request", "name":"get_parameter", "data":{"address64":"0013A200418D05FC","at_command":"NI", "value":None, "apply_changes":True}},
        ],

    ]
    return requests

def execute_sequential_requests(requests : list[dict]) -> None:
    """Executes the requests sequentially.
    
    Args:
        requests: the requests to execute
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((config.IP_ADDRESS, config.TCP_PORT_REQUEST))
        remaining = ""
        for request in requests:
            print("Request:", request)
            socket_common.send_json(s, request)
            response, remaining = socket_common.recv_json(s, remaining)
            print("Response:", response)
        s.close()



def execute_parallel_requests(requests : list[list[dict]]) -> None:
    """Executes the requests in a sequential-parallel way.
    
    Args:
        requests: A list with a list of requests.
            The items of the outer lists are called groups. All requests from the previous group are executed before the requests from the next group.
            Inside each group there is a list of requests. Requests from one group are exetuted parallelly.
    """

    id = 1
    for group in requests:
        threads : list[threading.Thread] = []
        for req in group:
            thread = threading.Thread(target=execute_one_request, args=(req, id), daemon=True)
            threads.append(thread)
            thread.start()
            id += 1
        for thread in threads:
            thread.join()

def execute_one_request(request : dict, id : int) -> None:
    """Executes one request.
    
    Args:
        request: the request to execute.
        id: id of the request.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((config.IP_ADDRESS, config.TCP_PORT_REQUEST))
        remaining = ""
        print(f"Request ({id}):", request)
        socket_common.send_json(s, request)
        response, remaining = socket_common.recv_json(s, remaining)
        print(f"Response ({id}):", response)
        s.close()

def notifications_thread_func() -> None:
    """The function for receiving notifications, i.e. received messages from the coordinator controller.
    It should run in a separate thread.

    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((config.IP_ADDRESS, config.TCP_PORT_NOTIFY))
        remaining = ""
        while True:
            notification, remaining = socket_common.recv_json(s, remaining)
            print("Notification:", notification)


def main() -> None:
    """The main function of the client

    It sets up the thread for receiving notifications,
    then it makes some requests sequentially or in sequential-parallel way depending on the presence of -p switch.
    
    """
    parallel = "-p" in sys.argv
    threading.Thread(target=notifications_thread_func, daemon=True).start()
    if parallel:
        requests = prepare_parallel_requests()
        execute_parallel_requests(requests)
    else:
        requests = prepare_sequential_requests()
        execute_sequential_requests(requests)
    
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()