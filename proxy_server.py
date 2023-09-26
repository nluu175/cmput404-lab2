import socket
from threading import Thread

BYTES_TO_READ = 4096
PROXY_SERVER_HOST = "127.0.0.1"
PROXY_SERVER_PORT = 8080

# send some data (request) to host:port
def send_request(host, port, request):

    # create a new socket in with block to ensure it's closed once we're done
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:

        client_socket.connect((host, port))
        client_socket.send(request)
        client_socket.shutdown(socket.SHUT_WR)

        # assemble response (recv() blocks until it receives data)
        data = client_socket.recv(BYTES_TO_READ)
        result = b"" + data

        # keep reading data until conn is terminated
        while len(data) > 0:
            data = client_socket.recv(BYTES_TO_READ)
            result += data

        return result


# handle an incoming connection that has been accepted by the server
def handle_connection(conn, addr):
    with conn:
        print(f"Connected by {addr}")

        request = b""
        while True:
            data = conn.recv(BYTES_TO_READ)
            if not data:
                break
            print(data)
            request += data

        response = send_request("www.google.com", 80, request)
        conn.sendall(response)


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))

        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.listen(2)

        # while True:
        conn, addr = server_socket.accept()

        handle_connection(conn, addr)


start_server()
