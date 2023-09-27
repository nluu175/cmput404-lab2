import socket

BYTES_TO_READ = 4096


def get(host, port):
    payload = b"GET / HTTP/1.1\nHost: " + host.encode("utf-8") + b"\n\n"

    # initialize a socket
    # - AF_INET: IPv4, the address (and protocol families)
    # - SOCK_STREAM: TCP, socket type
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to designated host
    s.connect((host, port))

    # request google homepage
    s.send(payload)

    # shu
    s.shutdown(socket.SHUT_WR)  # I'm done sending the request

    # recv() receives data from the socket
    # - takes bufsize (max amount of data to be received) as parameter
    # - returns a bytes object representing the data received
    result = s.recv(BYTES_TO_READ)  # Continously receiving the response
    while len(result) > 0:
        print(result)
        result = s.recv(BYTES_TO_READ)

    s.close()  # need to close the socket


# initialize the connection to www.google.com
# get("www.google.com", 80)

# initialize the connection to the localhost at port 8080
get("localhost", 8080)
