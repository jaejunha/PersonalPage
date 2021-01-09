import socket
import os
import time

HOST = SERVER_IP  
PORT = 8001    

PATH_TARGET = "upload"
     
if __name__ == "__main__":
    list_file = os.listdir(PATH_TARGET)
    len_list = len(list_file)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    client.sendall(str(len(list_file)).encode())
    
    for i in range(len_list):
        client.recv(1024)
        size = os.path.getsize(PATH_TARGET + "/" + list_file[i])
        client.send((PATH_TARGET + "/" + list_file[i] + "/" + str(size)).encode())
        client.recv(1024)
        file = open(PATH_TARGET + "/" + list_file[i], "rb")
        data = file.read(1024)
        while data:
            client.send(data)
            data = file.read(1024)
        file.close()
        client.send("ok".encode())
    client.close()
