def getMenu():
    str = ""
    file = open("config/menu.csv", "r")
    for line in file.readlines():
        if len(line) > 0:
            list_line = line.split(",")
            name = list_line[0].strip()
            if name == "---":
                str += '<hr style="margin-top: 4px; margin-bottom: 4px;">'
            else:
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

def getBucketlist():
    str = ""

    find = False # <div> 구분선 넣어주기 용
    num_ele = None

    str = ""
    file = open("bucketlist.csv", "r")
    for line in file.readlines():
        if len(line) > 0:
            list_line = line.split(",")
            if len(list_line) == 1:
                if find:
                    str += "</table>\n"
                    str += "</div>\n"
                    str += "<br>\n"
                find = True
                num_ele = 0

                str += '<div>\n'
                str += '<span style="font-size:20px;">%s</span>\n' % list_line[0]
                str += '<table style="border: 1px solid #bcbcbc; width: 100%;">\n'
    
            else:
                num_ele += 1
                if num_ele == 1:
                    str += '<tr style="font-weight: bold;">\n'
                    for ele in list_line:
                        str += '<td>%s</td>' % ele.strip()
                    str += '</tr>\n'
                else:
                    str += '<tr style="background-color: rgba(255, 255, 255, 0.6);">\n'
                    for i, ele in enumerate(list_line):
                        if i == 0:
                            str += '<td style="text-align: center;"><img src="img/%s"/></td>' % ele.strip()
                        else:
                            str += '<td>%s</td>' % ele.strip()
                    str += '</tr>\n'

    str += "</table>\n"
    str += "</div>\n"

    return str

def makeHomeHTML():
    content = loadMemo()
	
    file = open("html/home.html", "w")
    file.write('<html style="overflow-x: hidden;">\n')
    file.write('<link rel="stylesheet" type="text/css" href="css/no_drag.css">\n')
    file.write('<script src="js/logout.js"></script>\n')
    file.write('<body style="margin: 10px;">\n')
    file.write('<meta charset="utf-8">\n')
    file.write('<div style="width: 100%; height: 40%; text-align: center;">\n')
    file.write('<img src="img/main.gif" style="width: 100%; height: 100%; object-fit: contain;"/>\n')
    file.write('</div>')
    file.write('<div style="width: 100%; height: 20%; overflow-y: auto;">\n')
    """
    file.write('<span style="font-size:30px;">Bucket List</span>')
    file.write(getBucketlist())
    """
    file.write("</div>\n")
    file.write('<form action="/home" method="post" target="inner" style="margin-top: 10px; margin-bottom: 0; width: 100%; height: calc(40% - 10px);">\n')
    file.write('<span style="font-size:30px;">Memo</span>')
    file.write('<textarea name="home" rows="10" style="width: 100%%; height: calc(100%% - 90px); resize: none;">%s</textarea>' % content)
    file.write('<div style="width: 100%; text-align: right; margin-top: 10px;">\n')
    file.write('<button type="submit">적용하기</button>\n')
    file.write("</div>\n")
    file.write("</form>\n")
    file.write("</body>\n")
    file.write("</html>")
    file.close()
	
