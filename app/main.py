import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server is listening to port 4221...")
    # server_socket.accept() # wait for client

    while True:
        client_socket, address = server_socket.accept()
        print(f"Accepted connection from {address}")
        client_socket.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
        client_socket.close()


if __name__ == "__main__":
    main()
