import socket
import json


def parse_request(request):
    parsed_request = {}

    request_lines = request.split("\r\n")

    parsed_metadata = request_lines[0].split(" ")

    parsed_request["method"] = parsed_metadata[0]
    parsed_request["route"] = parsed_metadata[1]

    return parsed_request





server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = "0.0.0.0"
PORT = 8080
server_socket.bind((HOST, PORT))

server_socket.listen()


client_socket, client_address = server_socket.accept()

while 1:
    data = client_socket.recv(4096).decode('utf-8')

    print(data)

    users = {"users": []}

    parsed = parse_request(data)

    if parsed["method"] == "GET":
        user = parsed["route"].split("user=")[-1]

        users["users"].append(user)
        
        body = json.dumps(users)

        response = f"""HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{body}"""

        print(response)

        client_socket.sendall(response.encode("utf-8"))
        client_socket.close()
        break
    else:
        response = """HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/plain"""

        client_socket.sendall(response.encode("utf-8"))
        client_socket.close()
        break




