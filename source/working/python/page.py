import os
from python.account import *

CONST_WEEK = ["월", "화", "수", "목", "금", "토", "일"]

dic_visit = {}
dic_alert = {}

def check(res, list_account):
	access = False
	if checkAccount(res, list_account):
		access = True

	ip_client = res.client_address[0]
	if access:
		dic_alert[ip_client] = False
		dic_visit[ip_client] = calSessionLength() 
	else:
		dic_alert[ip_client] = True
	
def home(ip_client):
	path = None
	access = True

	if checkVisit(dic_visit, ip_client):
		dic_visit[ip_client] = calSessionLength()
		path = "html/index.html"
	elif ip_client in dic_alert.keys() and dic_alert[ip_client]:
		path = "html/login_fail.html"
	else:
		path = "html/login_normal.html"

	return path, access

def logout(ip_client):
	access = True

	if checkVisit(dic_visit, ip_client):
		del dic_visit[ip_client]
			
	path = "html/login_normal.html"

	return path, access

def todo(ip_client):
	if checkVisit(dic_visit, ip_client):
		access = True
	else:
		access = False
	
	now = datetime.datetime.now()
	week = CONST_WEEK[now.weekday()]
	name = now.strftime("todo/data/%Y-%m-%d.csv")
	if os.path.isfile(name) is False:
		os.system("touch " + name)

		list_todo = []
		file = open("todo/frame/frame.csv", "r")
		for line in file.readlines():
			list_line = line.split(",")
			priority = int(list_line[0].strip())
			item = list_line[1].strip()
			possible = list_line[2].strip()
			if week in possible:
				list_todo.append( (priority, item) )

		list_todo.sort(reverse = True)
		for todo in list_todo:
			os.system('echo "' + todo[1] + ', 0">> ' + name)
		
	path = "html/todo.html"

	return path, access

def test(ip_client):
	if checkVisit(dic_visit, ip_client):
		access = True
	else:
		access = False
			
	path = "html/test.html"

	return path, access


