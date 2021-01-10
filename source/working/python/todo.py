import datetime

CONST_WEEK = ["월", "화", "수", "목", "금", "토", "일"]

def parseTodoInput(dic_input):
    list_date = dic_input["date"].split("-")
    date = datetime.date(int(list_date[0]), int(list_date[1]), int(list_date[2]))

    dic_todo = {}
    for key in dic_input.keys():
        if key == "date":
            continue
        name = key.split("_")[0]
        if key.split("_")[1] == "r":
            dic_todo[name] = {}
            dic_todo[name]["status"] = int(dic_input[key])
        else:
            dic_todo[name]["reason"] = dic_input[key]

    return dic_todo, date

def modifyTodoList(dic_todo, list_todo):
	for name in dic_todo.keys():
		for todo in list_todo:
			if todo[1]["name"] == name:
				todo[1]["status"] = dic_todo[name]["status"]
				todo[1]["reason"] = dic_todo[name]["reason"]
				break

def getTodoList(date):
    list_todo = []
    file_name = date.strftime("output/todo/data/%Y-%m-%d.csv")
	
    try:
        file = open(file_name, "r")
        for line in file.readlines():
            list_line = line.split(",")
            priority = int(list_line[0].strip())
            name = list_line[1].strip()
            status = int(list_line[2].strip())
            reason = ""
            if len(list_line) > 3:
                reason = list_line[3].replace("%2C", ",").strip()

            list_todo.append( (priority, {"name": name, "status": status, "reason": reason}) )

        list_todo.sort(key = lambda x: (x[1]["status"], -x[0]) )		

        file.close()
    except FileNotFoundError:
        """
        파일이 없는 경우
        """
        week = CONST_WEEK[date.weekday()]

        file = open("output/todo/frame/frame.csv", "r")
        for line in file.readlines():
            if line.strip() == "":
                continue

            list_line = line.split(",")
            priority = int(list_line[0].strip())
            name = list_line[1].strip()
            possible = list_line[2].strip()
            if week in possible:
                list_todo.append( (priority, {"name": name, "status": 0, "reason": ""}) )
		
        file.close()

        list_todo.sort(reverse = True, key = lambda x: x[0])
        file = open(file_name, "w")
        for todo in list_todo:
            file.write("%d, %s, 0\n" % (todo[0], todo[1]["name"]) )
        file.close()

    return list_todo

def saveTodoList(date, list_todo):
	file_name = date.strftime("output/todo/data/%Y-%m-%d.csv")

	file = open(file_name, "w")
	for todo in list_todo:
		file.write("%d, %s, %d, %s\n" % (todo[0], todo[1]["name"], todo[1]["status"], todo[1]["reason"].replace(",", "%2C")) )
	
	file.close()

def makeTodoHTML(date):
    now = datetime.datetime.now()

    list_todo = getTodoList(date)

    tab = -1
    file = open("html/todo.html", "w")
    file.write('<meta charset="utf-8">\n')
    file.write("<html>\n")
    file.write('<link rel="stylesheet" type="text/css" href="css/no_drag.css">\n')
    file.write('<script src="js/logout.js"></script>\n')
    file.write('<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>\n')
    file.write('<body style="margin: 10px">\n')
    file.write('<div id="dialog" style="display: none; z-index: 1; position: absolute; left: 0; top: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.5);">\n')
    file.write('<div style="position: absolute; top: 20%; left: 20%; width: 60%; height: 60%; z-index: 2; background: #fff;">\n')
    file.write('<a onclick="$(\'#dialog\').css(\'display\', \'none\');" style="display: inline-block; width: 100%; text-align: right; font-weight: bold; color: #f00;">X</a>\n')
    file.write("</div>\n")
    file.write("</div>\n")
    file.write('<div style="display: table; text-align: center; width: 100%;">\n')
    file.write('<form action="/todo" method="get" target="inner">\n')
    file.write('<input type="hidden" name="date" value="%s"/>\n' % ((date - datetime.timedelta(days = 1)).strftime("%Y-%m-%d")))
    file.write('<button style="display: table-cell; width:0; height:0; border-style:solid; border-width:20px;border-color:transparent #555 transparent transparent; background-color: rgba(0, 0, 0, 0); cursor: pointer;"></button>\n')
    file.write("</form>\n")
    file.write('<span style="display: table-cell; font-size: 30px; vertical-align: middle; width: 30%%;">%s</span>\n' % date.strftime("%Y-%m-%d"))
    file.write('<form action="/todo" method="get" target="inner">\n')
    if now <= (date + datetime.timedelta(days = 1)):
    	file.write('<input type="hidden" name="date" value="%s"/>\n' % (now.strftime("%Y-%m-%d")))
    else:
    	file.write('<input type="hidden" name="date" value="%s"/>\n' % ((date + datetime.timedelta(days = 1)).strftime("%Y-%m-%d")))
    file.write('<button style="display: table-cell; width:0; height:0; border-style:solid; border-width:20px;border-color:transparent transparent transparent #555; background-color: rgba(0, 0, 0, 0); cursor: pointer;"></button>\n')
    file.write("</form>\n")
    file.write("</div>\n")
    if len(list_todo) > 0:
        file.write('<form action="/todo" method="post" target="inner" style="position: absolute; bottom: 0; width: calc(100% - 20px); height: calc(100% - 80px);">\n')
        file.write('<div style="overflow-y: auto; height: calc(100% - 40px);">\n')
        for todo in list_todo:
            priority = todo[0]
            status = todo[1]["status"]
            name = todo[1]["name"]
            reason = todo[1]["reason"]

            if tab != status:
                tab = status
			
                if status == 0:
                    file.write("미진행<br>\n")
                elif status == 1:
                    file.write("<br>\n")
                    file.write("진행연기<br>\n")
                else:
                    file.write("<br>\n")
                    file.write("진행완료<br>\n")

            file.write('<div style="margin: 10px; padding: 5px; border: 1px solid #bcbcbc; background-color: rgba(255, 255, 255, 0.6); border-radius: 2px;">\n')
            file.write("%s%s" % ("★" * priority, "☆" * (5 - priority)))
            file.write(" %s\n" % name)
            file.write('<ele style="display: flex;">\n')
            if status == 2:
                file.write('<input name="%s_r" type="radio" value="2" checked="checked">진행완료&nbsp;\n' % name)
            else:
                file.write('<input name="%s_r" type="radio" value="2">진행완료&nbsp;\n' % name)
            if status == 1:
                file.write('<input name="%s_r" type="radio" value="1" checked="checked">진행연기&nbsp;\n' % name)
            else:
                file.write('<input name="%s_r" type="radio" value="1">진행연기&nbsp;\n' % name)
            if status == 0:
                file.write('<input name="%s_r" type="radio" value="0" checked="checked">미진행&nbsp;\n' % name)
            else:
                file.write('<input name="%s_r" type="radio" value="0">미진행&nbsp;\n' % name)
            if reason == "":
                file.write('<input type="text" placeholder="연기시 사유" name="%s_t" style="width: calc(100%%-10px); flex-grow: 1;">\n' % name)
            else:
                file.write('<input type="text" placeholder="연기시 사유" name="%s_t" style="width: calc(100%%-10px); flex-grow: 1;" value="%s">\n' % (name, reason) )
            file.write("</ele>\n")
            file.write("</div>\n")
        file.write("</div>\n")
        file.write('<div style="width: 100%; text-align: right; margin-top: 10px">\n')
        file.write('<button type="submit">적용하기</button>\n')
        file.write('<button type="button" onclick="$(\'#dialog\').css(\'display\',\'block\');">향목편집</button>\n')
        file.write("</div>\n")
        file.write('<input type="hidden" name="date" value="%s"/>\n' % (date.strftime("%Y-%m-%d")))
        file.write("</form>\n")
    file.write("</body>\n")
    file.write("</html>\n")
    file.close()
