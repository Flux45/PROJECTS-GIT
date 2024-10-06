import argparse
import os
import socket
import threading
import sys

FILE_DIR = ""

def handles_request(client, addr):
    try:
        data = client.recv(1024)
        if not data:
            return
        response = parse_request(data, client)
        client.sendall(response)
    except Exception as e:
        print(f"Error handling request: {e}")
    finally:
        client.close()


def parse_request(data, client):
    print("parsereq data:   " + data.decode())
    global FILE_DIR
    try:
        data_list = data.decode('utf-8').split("\r\n")
        # Print debug data
        print("Request Data:", data_list)
        request_line = data_list[0].split(" ")

        # method, target = data_list[0].split(" ")[:2]
        if len(request_line) < 2:
            return "HTTP/1.1 400 Bad Request\r\n\r\n".encode()

        method = request_line[0]
        target = request_line[1]

        # Initialized header dictionary
        headers = {}

        # Parse headers
        i = 1
        while data_list[i]:
            key_value = data_list[i].split(": ", 1)
            if len(key_value) == 2:
                headers[key_value[0]] = key_value[1]
            i += 1

        # Print headers for debugging
        print("Parsed Headers:", headers)
        bodyyy = ""
        # Following the headers is an empty line, then the body if it exists
        if len(data_list) > i:
            body_index = i + 1
            body = '\r\n'.join(data_list[body_index:])  # Entire body as bytes
            bodyyy = body
            # Print body for debugging
            print("Body:", body)


        if method == "GET" and target == "/":
            response: bytes = "HTTP/1.1 200 OK\r\n\r\n".encode()
        elif target.startswith("/echo"):
            content = target.split("/")[2]
            response: bytes = \
                f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(content)}\r\n\r\n{content}".encode()
        elif target.startswith("/user-agent"):
            content = data_list[2].split(": ")[1]
            response: bytes = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(content)}\r\n\r\n{content}".encode()
        elif target.startswith("/files/") and method == "GET":
            file_location = target
            file_name =  target[7:]
            try:
                with open(file_location + file_name, "r") as f:
                    body = f.read()
                response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(body)}\r\n\r\n{body}".encode()
            except Exception as e:
                response = f"HTTP/1.1 404 Not Found\r\n\r\n".encode()
        elif target.startswith("/files/") and method == "POST":
            print("1!!!!!!!!!! inside post files")
            file_location = r"C:\Users\Lenovo\Desktop\Files\Python Projects\HTTP Server\codecrafters-http-server-python\app\files"
            file_target =  target[7:]
            print("FILE TARGET:  " + file_target + "")
            extract = file_target.split("/")
            print(extract)
            dir = ""

            i = 0
            for i in range(len(extract)-1):
                dir = os.path.join(dir, extract[i])

            name =  extract[len(extract)-1]
            path = f"{file_location}{FILE_DIR}"
            print(">>>>>>>>>>>>>>>  :" + path[1:])

            print("NAME   :   " + name)
            print("DIR   :   " + dir)
            path_cleaned = os.path.join(path[1:], dir)
            file_path_cleaned = os.path.join(path_cleaned, name)
            print("PATH CLEANED   :   " + path_cleaned)
            print("FILE PATH CLEANED   :   " + file_path_cleaned)
            os.makedirs(path_cleaned, exist_ok=True)
            try:
                print("going in")
                body = bodyyy
                print("BODY   : " + body)
                with open(path_cleaned, "wb") as f:
                    print("opened")
                    f.write(name.encode())
                    print("wrote")
                response = "HTTP/1.1 201 Created\r\n\r\n".encode()
            except Exception as e:
                print(e)
                response = "HTTP/1.1 500 Internal Server Error\r\n\r\n".encode()
        else:
            response: bytes = "HTTP/1.1 404 Not Found\r\n\r\n".encode()

        return response

    except Exception as e:
        print(f"Error parsing request: {e}")
        return "HTTP/1.1 400 Bad Request\r\n\r\n"

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", default=".")
    args = parser.parse_args()

    if "directory" in args:
        global FILE_DIR
        FILE_DIR = args.directory
        print(FILE_DIR)

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 4221))
    server_socket.listen()
    try:
        while True:
            client, addr = server_socket.accept()
            print("Server is listening to port 4221...")
            thread = threading.Thread(target=handles_request, args=(client, addr))
            thread.start()

    except Exception as e:
        print(f"Server Error: {e}")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
