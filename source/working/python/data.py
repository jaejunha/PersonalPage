from python.home import *

CONST_8KB = 8192 

def checkObject(path):
    return (".png" in path) or (".jpg" in path) or (".gif" in path) or (".ico" in path) or (".css" in path) or (".js" in path)

def writeObject(res):
	file = open(res.path, "rb")
	data = file.read(CONST_8KB)
	res.wfile.write(data)

	while data:
		data = file.read(CONST_8KB)
		res.wfile.write(data)

	file.close()
				
def writeHTML(res):
	file = open(res.path, "r", encoding = "utf-8")
	for line in file.readlines():
		if ":)menu.csv&" in line:
			start = line.find(":)")
			end = line.find("&")
			content = getMenu()
			line = line.replace(line[start: end + 1], content)

		elif ":)favorite.csv&" in line:
			start = line.find(":)")
			end = line.find("&")
			content = getFavorite()
			line = line.replace(line[start: end + 1], content)

		res.wfile.write(line.encode())

	file.close()

