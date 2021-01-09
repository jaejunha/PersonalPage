import socket
import os
import time

PORT = 8001

origin = os.path.abspath("../../")

def requestFile(path):
    client.sendall(("request %s" % path).encode())
            
    os.chdir(origin)
    list_folder = path.split("/")
    len_folder = len(path.split("/")) - 1
    file_name = list_folder[-1]

    for i in range(len_folder):
        os.chdir(list_folder[i])

    print(path)
    file = open(file_name, "wb")
    data = client.recv(1024)
    while data:
        file.write(data)
        data = client.recv(1024)
    file.close()	

def endRequest():
    client.sendall("end".encode())

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("", PORT))
server.listen()

try:
    while True:

        client, addr = server.accept()

        num = int(client.recv(1024).decode())
        for i in range(num):
            client.send("ok".encode())
            raw = client.recv(1024).decode().split("/")
            size = int(raw[-1])
            name = raw[-2]
            print(name, size)
            file = open(name, "wb")
            client.send("ok".encode())

            data = client.recv(1024)
            size -= len(data)
            while size > 0:
                file.write(data)
                data = client.recv(1024)
                size -= len(data)
            file.write(data)
            file.close()

            print("ok")
        client.close()
except KeyboardInterrupt:
    server.close()
