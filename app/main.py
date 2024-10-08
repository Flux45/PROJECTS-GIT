import socket
import threading
import gzip
from sys import argv


def handle_request(conn, addr):
    data = conn.recv(1024).decode("utf-8")
    request_lines = data.split("\r\n")
    request_line = request_lines[0]
    method, path, _ = request_line.split(" ")
    headers = request_lines[1:-2]
    body = request_lines[-1]
    user_agent = ""
    accept_encoding = ""

    for header in headers:
        if header.startswith("User-Agent:"):
            user_agent = header.split(": ")[1]
        if header.startswith("Accept-Encoding:"):
            accept_encoding = header.split(": ")[1]

    if path == "/":
        response = "HTTP/1.1 200 OK\r\n\r\n"

    elif path == "/user-agent":
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}\r\n"

    elif "/files" in path:
        directory = argv[2]
        filename = path.split("/files/")[1]

        if method == "POST":
            try:
                with open(f"{directory}/{filename}", "w") as f:
                    f.write(body)
                response = "HTTP/1.1 201 Created\r\n\r\n"
            except Exception as e:
                response = "HTTP/1.1 404 Not Found\r\n\r\n"

        elif method == "GET":
            try:
                with open(f"{directory}/{filename}", "rb") as f:
                    content = f.read()
                    response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(content)}\r\n\r\n".encode()
                    response += content
            except FileNotFoundError:
                response = "HTTP/1.1 404 Not Found\r\n\r\n"
            conn.sendall(response.encode())
            conn.close()
            return

    elif path.startswith("/echo"):
        message = path.split("/echo/")[1]
        response_body = message
        headers = "Content-Type: text/plain\r\n"

        if "gzip" in accept_encoding:
            compressed_body = gzip.compress(response_body.encode())
            headers += f"Content-Encoding: gzip\r\nContent-Length: {len(compressed_body)}\r\n\r\n"
            response = f"HTTP/1.1 200 OK\r\n{headers}".encode() + compressed_body
        else:
            headers += f"Content-Length: {len(response_body)}\r\n\r\n"
            response = f"HTTP/1.1 200 OK\r\n{headers}{response_body}\r\n".encode()

    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n"

    conn.sendall(response.encode() if isinstance(response, str) else response)
    conn.close()


def main():
    server_socket = socket.create_server(("localhost", 4221))
    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_request, args=(conn, addr)).start()


if __name__ == "__main__":
    main()







# from sys import argv
# import socket
# import threading
# import gzip
#
#
#
#
# def handle_request(conn, addr):
#     data = conn.recv(1024).decode("utf-8")
#     request = data.split("\r\n")
#     method = request[0].split(" ")[0]
#     path = request[0].split(" ")[1]
#     body = request[-1]
#     user_agent = ""
#     accept_encoding = ""
#     for line in request:
#         if line.startswith("User-Agent:"):
#             user_agent = line[len("User-Agent: ") :]
#         if line.startswith("Accept-Encoding:"):
#             accept_encoding = line[len("Accept-Encoding: ") :]
#     encoding = ""
#
#
#     if "gzip" in accept_encoding:
#         encoding = "Content-Encoding: gzip\r\n"
#         body = gzip.compress(body.encode())
#
#     if path == "/":
#         conn.send(b"HTTP/1.1 200 OK\r\n\r\n")
#
#     elif path == "/user-agent":
#         response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}\r\n"
#         conn.send(response.encode())
#
#     elif "/files" in path:
#         if method == "POST":
#             directory = argv[2]
#             filename = path[7:]
#             try:
#                 with open(f"/{directory}/{filename}", "w") as f:
#                     f.write(f"{body}")
#                 response = f"HTTP/1.1 201 Created\r\n\r\n"
#             except Exception as e:
#                 response = f"HTTP/1.1 404 Not Found\r\n\r\n"
#             conn.send(response.encode())
#         elif method == "GET":
#             f_name = path.split("/")[-1]
#             try:
#                 with open(argv[2] + f_name) as f:
#                     content = f.read()
#                     response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {str(len(content))}\r\n{content}"
#             except FileNotFoundError:
#                 response = "HTTP/1.1 404 Not Found\r\n\r\n"
#             conn.send(response.encode())
#
#     elif path.startswith("/echo"):
#         random_path = path[6:]
#         response = f"HTTP/1.1 200 OK\r\n{encoding}Content-Type: text/plain\r\nContent-Length: {len(random_path)}\r\n\r\n{random_path}\r\n"
#         conn.send(response.encode())
#     else:
#         conn.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
#     conn.close()
#
#
#
# def main():
#     server_socket = socket.create_server(("localhost", 4221))
#     while True:
#         conn, addr = server_socket.accept()  # wait for client
#         threading.Thread(target=handle_request, args=(conn, addr)).start()
# if __name__ == "__main__":
#     main()









# msdkfmlskdmflkaa













# import socket
# import os
#
#
# def get_text_plain_ok_response(text, extra_headers=None):
#     response = (
#         "HTTP/1.1 200 OK\r\n"
#         "Content-Type: text/plain\r\n"
#         f"Content-Length: {len(text)}\r\n"
#     )
#     if extra_headers:
#         response += (
#             "\r\n".join([f"{key}: {value}" for key, value in extra_headers.items()])
#             + "\r\n"
#         )
#     response += f"\r\n{text}"
#     return response
#
#
#
# def main():
#     # You can use print statements as follows for debugging, they'll be visible when running tests.
#     print("Logs from your program will appear here!")
#     server_socket = socket.create_server(("localhost", 4221))
#     # Read the flag --directory from the command line if it exists
#     directory_value = None
#     if "--directory" in os.sys.argv:
#         directory_value = os.sys.argv[os.sys.argv.index("--directory") + 1]
#     print(f"Directory value: {directory_value}")
#     while True:
#         client_socket, address = server_socket.accept()
#         print(f"Connection from {address}")
#         data = client_socket.recv(1024).decode("utf-8")
#         # Obtain the request line
#         request_line = data.split("\r\n")[0]
#         method = request_line.split(" ")[0]
#         path = request_line.split(" ")[1]
#         # Obtain the headersas
#         headers = data.split("\r\n")[1:-2]
#         headers_dict = {
#             header.split(": ")[0].lower(): header.split(": ")[1]
#             for header in headers
#             if header
#         }
#         # Obtain the body
#         body = data.split("\r\n")[-1]
#         print(f"Request line: {request_line}")
#         print(f"Method: {method}")
#         print(f"Path: {path}")
#         print(f"Headers: {headers}")
#         print(f"Headers dict: {headers_dict}")
#         print(f"Body: {body}")
#         print(f"Data: {data}")
#
#         # Default response is 404
#         response = "HTTP/1.1 404 Not Found\r\n\r\n"
#         encode_response = True
#
#         # Check different paths
#         if path == "/":
#             response = "HTTP/1.1 200 OK\r\n\r\n"
#
#         elif path.startswith("/echo/"):
#             # Send a response
#             response_data = path.split("/echo/")[1]
#             # Check if there is an Accept-Encoding header
#             extra_headers = None
#             if "gzip" in headers_dict.get("accept-encoding", "").lower().split(", "):
#                 extra_headers = {"Content-Encoding": "gzip"}
#             response = get_text_plain_ok_response(
#                 response_data, extra_headers=extra_headers
#             )
#         elif path.startswith("/user-agent"):
#             response_data = headers_dict.get("user-agent", "")
#             response = get_text_plain_ok_response(response_data)
#         elif path.startswith("/files/") and method == "GET":
#             file_route = os.path.join(directory_value, path.split("/files/")[1])
#             print("File route:", file_route)
#             if os.path.exists(file_route):
#                 print("File exists")
#                 file_bytes = open(file_route, "rb").read()
#                 response = (
#                     "HTTP/1.1 200 OK\r\n"
#                     "Content-Type: application/octet-stream\r\n"
#                     f"Content-Length: {len(file_bytes)}\r\n"
#                     "\r\n"
#                 ).encode()
#                 response += file_bytes
#                 encode_response = False
#         elif path.startswith("/files/") and method == "POST":
#             file_route = os.path.join(directory_value, path.split("/files/")[1])
#             print("File route:", file_route)
#             file_bytes = body.encode()
#             with open(file_route, "wb") as file:
#                 file.write(file_bytes)
#             response = "HTTP/1.1 201 Created\r\n\r\n"
#         print(f"Response: {response}")
#         client_socket.sendall(response.encode() if encode_response else response)
#         client_socket.close()
#         # Close the loop after one request
#         # break
# if __name__ == "__main__":
#     main()