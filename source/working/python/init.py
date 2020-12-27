def getPort():
	port = None
	try:
		file = open("config/port.csv", "r")
		port = int(file.readlines()[0].strip())
	except FileNotFoundError:
		port = 80

	return port

def getLink(list_link):
	try:
		file = open("config/menu.csv", "r")
		for line in file.readlines():
			if len(line) > 0:
				list_link.append( line.split(",")[1].strip() )

		return True

	except FileNotFoundError:
		print("메뉴를 만들어주세요!")
		return False

