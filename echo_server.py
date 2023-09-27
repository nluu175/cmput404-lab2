import socket
from threading import Thread

BYTES_TO_READ = 4096
HOST = "127.0.0.1"
PORT = 8080


def handle_connection(conn, addr):
    with conn:
        print(f"Connected by {addr}")
        while True:
            # wait for a request then receive it
            data = conn.recv(BYTES_TO_READ)

            # if receiving an empty byte string ==> b""
            if not data:
                break
            print(data)

            # send all data back to the client
            conn.sendall(data)


def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))

        # setsockop() is used to set socket options
        # - SOL_SOCKET: socket option level
        # - SO_REUSEADDR: immediately reuse previous sockets which were bound
        # on the same address
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # allows backlog of up to 2 connections (queue up to 2 conn)
        s.listen(2)

        while True:
            conn, addr = s.accept()
            thread = Thread(target=handle_connection, args=(conn, addr))
            thread.run()


start_threaded_server()
