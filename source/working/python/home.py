def getMenu():
	str = ""
	file = open("config/menu.csv", "r")
	for line in file.readlines():
		if len(line) > 0:
			list_line = line.split(",")
			name = list_line[0].strip()
			link = list_line[1].strip()
			str += "<span><a onclick='loadHTML(" + '"' + link + '");' + "'>" + name + "</a></span><br>"

	return str[:-4]

def getFavorite():
	
	str = ""
	file = open("config/favorite.csv", "r")
	for line in file.readlines():
		if len(line) > 0:
			list_line = line.split(",")
			icon = list_line[0].strip()
			name = list_line[1].strip()
			link = list_line[2].strip()
			str += '<div><a href="' + link + '" target="_blank"><img src="' + icon + '"/>&nbsp;<span>' + name + "</span></a></div>"
	file.close()

	file = open("config/favorite_private.csv", "r")
	for line in file.readlines():
		if len(line) > 0:
			list_line = line.split(",")
			icon = list_line[0].strip()
			name = list_line[1].strip()
			link = list_line[2].strip()
			str += '<div><a href="' + link + '" target="_blank"><img src="' + icon + '"/>&nbsp;<span>' + name + "</span></a></div>"
	return str

def parseHomeInput(raw_input):
	memo = raw_input.split("=")[1]

	return memo 

def saveMemo(content):
	file = open("memo.txt", "w")
	file.write(content)
	file.close()

def loadMemo():
	content = ""

	file = open("memo.txt", "r")
	for line in file.readlines():
		content += line
	file.close()

	return content

def makeHomeHTML():
	content = loadMemo()
	
	file = open("html/home.html", "w")
	file.write('<html style="overflow-x: hidden;">\n')
	file.write('<body style="margin: 10px;">\n')
	file.write('<meta charset="utf-8">\n')
	file.write('<form action="/home" method="post" target="inner" style="position: absolute; bottom: 0; width: calc(100% - 20px)";>\n')
	file.write('<textarea name="home" rows="10" style="width: 100%%;">%s</textarea>' % content)
	file.write('<div style="width: 100%; text-align: right; margin-top: 10px;">\n')
	file.write('<button type="submit">적용하기</button>\n')
	file.write("</div>\n")
	file.write("</form>\n")
	file.write("</body>\n")
	file.write("</html>")
	file.close()
	
