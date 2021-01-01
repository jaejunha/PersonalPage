import socket
import os
import time

PORT = 8000

list_abs_folder = []
list_abs_file = []

def getAbs():
    list_working = [os.path.abspath("../")]

    while len(list_working) > 0:
        top = list_working[0]
        del list_working[0]

        if os.path.isdir(top):
            list_abs_folder.append(top)

            for obj in os.listdir(top):
                path = top + "/" + obj
                if os.path.isdir(path):
                    list_working.append(path)
                else:
                    list_abs_file.append(path + "|" + str(os.path.getmtime(path)))
        else:
            list_abs_file.append(path + "|" + str(os.path.getmtime(path)))

    return list_abs_folder, list_abs_file

def getRel(list_abs_folder, list_abs_file):
    str_replace_from = os.path.abspath("../")
    str_replace_to = str_replace_from.split("/")[-1]
    
    list_rel_folder = []
    list_rel_file = []

    for folder in list_abs_folder:
        list_rel_folder.append(folder.replace(str_replace_from, str_replace_to))

    for file in list_abs_file:
        list_rel_file.append(file.replace(str_replace_from, str_replace_to))

    return list_rel_folder, list_rel_file

list_abs_folder, list_abs_file = getAbs()
list_rel_folder, list_rel_file = getRel(list_abs_folder, list_abs_file)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("", PORT))
server.listen()

while True:
    client, addr = server.accept()

    data = client.recv(1024).decode()
    print(data)

    if data == "check folder":
        client.sendall(" ".join(list_rel_folder).encode())

    elif data == "check file":
        client.sendall(" ".join(list_rel_file).encode())

    elif data.startswith("request"):
        file = open("../../" + data.split(" ")[1], "rb")
        data = file.read(1024)
        while data:
            client.send(data)
            data = file.read(1024)
    
    client.close()

server.close()
