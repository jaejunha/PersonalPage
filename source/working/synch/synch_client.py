import socket
import os

HOST = SERVER_IP
PORT = 8000       

origin = os.getcwd()

def checkFolder():
	str_folder = ""

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((HOST, PORT))
	client.sendall("check folder".encode())
	while True:
		data = client.recv(1024)
		if not data:
			break

		str_folder += data.decode()
	client.close()

	return str_folder

def makeFolder(str_folder):
	for path in str_folder.split(" "):
		os.chdir(origin)
		for folder in path.split("/"):
			if os.path.isdir(folder) is False:
				os.system("mkdir %s" % folder)
			os.chdir(folder)
	os.chdir(origin)

def checkFile():
	str_file = ""
	
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((HOST, PORT))
	client.sendall("check file".encode())
	while True:
		data = client.recv(1024)
		if not data:
			break

		str_file += data.decode()
	client.close()

	return str_file

def updateFile(str_file):
	for ele in str_file.split(" "):
		path = ele.split("|")[0]
		timestamp = float(ele.split("|")[1])
		if os.path.isfile(path) is False:
			requestFile(path)
		elif os.path.getmtime(path) < timestamp:
			requestFile(path)

def requestFile(path):
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((HOST, PORT))
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
	os.chdir(origin)
	client.close()

str_folder = checkFolder()
makeFolder(str_folder)
str_file = checkFile()
updateFile(str_file)


