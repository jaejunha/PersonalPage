CONST_WEEK = ["월", "화", "수", "목", "금", "토", "일"]

def parseTodoInput(raw_input):
	dic_todo = {}
	for line in raw_input.split("&"):
		list_line = line.split("=")
		list_name = list_line[0]
		name = list_name.split("_")[0]
		if list_name.split("_")[1][0] == "r":
			dic_todo[name] = {}
			dic_todo[name]["status"] = int(list_line[1].strip())
		else:
			dic_todo[name]["reason"] = list_line[1].strip()

	return dic_todo

def modifyTodoList(dic_todo, list_todo):
	for name in dic_todo.keys():
		for todo in list_todo:
			if todo[1]["name"] == name:
				todo[1]["status"] = dic_todo[name]["status"]
				todo[1]["reason"] = dic_todo[name]["reason"]
				break

def getTodoList(now):
	list_todo = []
	file_name = now.strftime("todo/data/%Y-%m-%d.csv")
	
	try:
		file = open(file_name, "r")
		for line in file.readlines():
			list_line = line.split(",")
			priority = int(list_line[0].strip())
			name = list_line[1].strip()
			status = int(list_line[2].strip())
			reason = ""
			if len(list_line) > 3:
				reason = list_line[3].strip()

			list_todo.append( (priority, {"name": name, "status": status, "reason": reason}) )

		list_todo.sort(key = lambda x: (x[1]["status"], -x[0]) )		

		file.close()
	except FileNotFoundError:
		"""
		파일이 없는 경우
		"""
		week = CONST_WEEK[now.weekday()]

		file = open("todo/frame/frame.csv", "r")
		for line in file.readlines():
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

def saveTodoList(now, list_todo):
	file_name = now.strftime("todo/data/%Y-%m-%d.csv")

	file = open(file_name, "w")
	for todo in list_todo:
		file.write("%d, %s, %d, %s\n" % (todo[0], todo[1]["name"], todo[1]["status"], todo[1]["reason"]) )
	
	file.close()

def makeTodoHTML(now):
	list_todo = getTodoList(now)

	tab = -1
	file = open("html/todo.html", "w")
	file.write('<meta charset="utf-8">\n')
	file.write('<form action="/todo" method="post">\n')
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
	file.write('<button type="submit">적용하기</button>\n')
	file.write("</form>\n")
	file.close()
