def getMenu():
    str = ""
    file = open("config/menu.csv", "r")
    idx = 1 
    for line in file.readlines():
        if len(line) > 0:
            list_line = line.split(",")
            name = list_line[0].strip()
            if name == "---":
                str += "<hr>"
            else:
                link = list_line[1].strip()
                str += "<div><span><a onclick='loadHTML(%d, " % idx + '"' + link + '");' + "'>" + name + "</a></span></div>"
                idx += 1

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


