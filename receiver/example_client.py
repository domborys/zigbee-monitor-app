import socket, base64, threading
import socket_common, xbee_device_server_config as config

def main():
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

def prepare_some_requests():
    message = base64.b64encode(b"Lubie placki").decode()
    requests = [
        {"type":"request", "name":"discover"},
        {"type":"request", "name":"wait", "data":{"time":4}},
        {"type":"request", "name":"send", "data":{"address64":"0013A200418D05FC", "message":message}}
    ]
    return requests

def notifications_thread_func():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((config.IP_ADDRESS, config.TCP_PORT_NOTIFY))
        remaining = ""
        while True:
            notification, remaining = socket_common.recv_json(s, remaining)
            print("Response:", notification)

if __name__ == "__main__":
    main()