import socket

def handles_request(client):
    # print("inside handles request")
    try:
        data = client.recv(1024)
        if not data:
            return
        response = parse_request(data)
        client.sendall(response)
    except Exception as e:
        print(f"Error handling request: {e}")
    finally:
        client.close()


def parse_request(data):
    # print("inside parse request")

    try:
        data: list[str] = data.decode().split("\r\n")
        request_data = data[0]
        method, target = request_data.split(" ")[:2]
        # print("TTTTTTTTarget: "+ target)
        # print("datasadas: "+data[3].split(": ")[1])
        if method == "GET" and target == "/":
            response: bytes = "HTTP/1.1 200 OK\r\n\r\n".encode()
        elif target.startswith("/echo"):
            content = target.split("/")[2]
            # print(content)
            response: bytes = \
                f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(content)}\r\n\r\n{content}".encode()
        elif target.startswith("/user-agent"):
            content = data[3].split(": ")[1]
            # print("CCCC: "+content)
            response: bytes = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(content)}\r\n\r\n{content}".encode()
        else:
            response: bytes = "HTTP/1.1 404 Not Found\r\n\r\n".encode()

        return response
    except Exception as e:
        print(f"Error parsing request: {e}")
        return "HTTP/1.1 400 Bad Request\r\n\r\n"

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 4221))
    server_socket.listen()
    try:
        while True:
            client, addr = server_socket.accept()
            print("Server is listening to port 4221...")
            handles_request(client)
    except Exception as e:
        print(f"Server Error: {e}")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
