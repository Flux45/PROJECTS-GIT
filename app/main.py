import socket  # noqa: F401

def parse_request(request_data):
    lines = request_data.split("\r\n")


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221))
    client, addr = server_socket.accept()
    print("Server is listening to port 4221...")

    with client:
        while True:
            data = client.recv(1024)
            request_data = data.decode().split("\r\n")
            response = b"HTTP/1.1 200 OK\r\n\r\n"
            #  ['GET / HTTP/1.1', 'Host: localhost:4221', '', '']
            if not data:
                break
            client.send(b"HTTP/1.1 200 OK\r\n\r\n")
            if request_data[0].split(" ")[1] != "/":
                response = b"HTTP/1.1 404 Not Found\r\n\r\n"
            client.send(response)

    # data: str = client.recv(1024).decode()
    # request_data: list[str] = data.split("\r\n")
    # response: bytes = "HTTP/1.1 200 OK\r\n\r\n".encode()
    # if request_data[0].split(" ")[1] != '/':
    #     response: bytes = "HTTP/1.1 404 Not Found\r\n\r\n".encode()
    # client.send(response)
    #
    # client.close()
    # server_socket.close()


    # server_socket.accept() # wait for client

    # while True:
    #     client_socket, address = server_socket.accept()
    #     print(f"Accepted connection from {address}")
    #
    #     client_socket.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
    #     client_socket.close()





if __name__ == "__main__":
    main()
