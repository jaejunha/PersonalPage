import os

def getPort():
	port = None
	try:
		file = open("config/port.csv", "r")
		port = int(file.readlines()[0].strip())
	except FileNotFoundError:
		port = 80

	return port

def removeNohup():
    try:
        os.remove("nohup.out")
    except FileNotFoundError:
        pass
