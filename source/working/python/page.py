# coding: utf8

import urllib

from python.account import *
from python.home import *
from python.schedule import *
from python.todo import *
from python.stock import *

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

def home_input(res):
	ip_client = res.client_address[0]
	if checkVisit(dic_visit, ip_client) is False:
		return 

	length = int(res.headers['Content-length'])
	raw_input = urllib.parse.unquote(res.rfile.read(length).decode("utf-8"))

	memo = parseHomeInput(raw_input.replace("+", " ")) 
	saveMemo(memo)
	
def todo_input(res):
	ip_client = res.client_address[0]
	if checkVisit(dic_visit, ip_client) is False:
		return

	length = int(res.headers['Content-length'])
	raw_input = urllib.parse.unquote(res.rfile.read(length).decode("utf-8"))

	dic_todo = parseTodoInput(raw_input.replace("+", " ")) 
	list_todo = getTodoList(datetime.datetime.now())
	modifyTodoList(dic_todo, list_todo)
	saveTodoList(datetime.datetime.now(), list_todo)

def stock_input(res):
    ip_client = res.client_address[0]
    if checkVisit(dic_visit, ip_client) is False:
        return

    length = int(res.headers['Content-length'])
    raw_input = urllib.parse.unquote(res.rfile.read(length).decode("utf-8"))

def root(ip_client):
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

def home(ip_client):
	if checkVisit(dic_visit, ip_client):
		access = True
		makeHomeHTML()
	else:
		access = False
		
	path = "html/home.html"

	return path, access



def logout(ip_client):
	access = True

	if checkVisit(dic_visit, ip_client):
		del dic_visit[ip_client]
			
	path = "html/login_normal.html"

	return path, access

def schedule(ip_client, path):
    if checkVisit(dic_visit, ip_client):
        access = True
        if "?date=" in path:
            str_date = path.split("?date=")[1]
            makeScheduleHTML(datetime.datetime.strptime(str_date, "%Y-%m-%d"))
        else:
            makeScheduleHTML(datetime.datetime.now())
    else:
        access = False
		
    path = "html/schedule.html"

    return path, access

def todo(ip_client, path):
    if checkVisit(dic_visit, ip_client):
        access = True
        if "?date=" in path:
            str_date = path.split("?date=")[1]
            makeTodoHTML(datetime.datetime.strptime(str_date, "%Y-%m-%d"))
        else:
            makeTodoHTML(datetime.datetime.now())
    else:
        access = False
		
    path = "html/todo.html"

    return path, access

def stock(ip_client, path):
    if checkVisit(dic_visit, ip_client):
        access = True
        if "?date=" in path:
            str_date = path.split("?date=")[1]
            makeStockHTML(datetime.datetime.strptime(str_date, "%Y-%m-%d"))
        else:
            makeStockHTML(datetime.datetime.now())
    else:
        access = False
		
    path = "html/stock.html"

    return path, access

def test(ip_client):
	if checkVisit(dic_visit, ip_client):
		access = True
	else:
		access = False
			
	path = "html/test.html"

	return path, access


