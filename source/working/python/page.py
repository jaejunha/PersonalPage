# coding: utf8

import urllib
import os

from python.account import *
from python.home import *
from python.bucketlist import *
from python.schedule import *
from python.todo import *
from python.stock import *

dic_visit = {}
dic_alert = {}

def saveFile(res, length):
    dic = {}

    raw = res.rfile.read(length)
    boundary = "------WebKitFormBoundary".encode()
    if boundary in raw:
        list_raw = raw.split("\r\n\r\n".encode())
        type = list_raw[0].decode().split("/")[1].strip()
        name = list_raw[2].decode().split("\n")[0].strip()
        data = list_raw[1][:list_raw[1].find(boundary)]
        if type.endswith("jpeg") or type.endswith("jpg") or type.endswith("png") or type.endswith("gif") or type.endswith("bmp"): 
            os.system("rm output/stock/screenshot/%s*" % name)
            file = open("output/stock/screenshot/%s.%s" % (name, type), "wb")
            file.write(data)

        list_date = name.split("-")
        date = datetime.date(int(list_date[0]), int(list_date[1]), int(list_date[2]))

        return date, True

    else:
        utf8 = raw.decode("utf-8")
        utf8_treat = utf8.replace("+", " ")

        list_input = utf8_treat.split("&")
        for input in list_input:
            key = urllib.parse.unquote(input.split("=")[0])
            value = urllib.parse.unquote(input.split("=")[1])
            dic[key] = value

        return dic, False

def parseUTF8(res, length):
    dic = {}

    utf8 = res.rfile.read(length).decode("utf-8")
    utf8_treat = utf8.replace("+", " ")

    list_input = utf8_treat.split("&")
    for input in list_input:
        key = urllib.parse.unquote(input.split("=")[0])
        value = urllib.parse.unquote(input.split("=")[1])
        dic[key] = value

    return dic 

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
    dic_input = parseUTF8(res, length)
    
    memo = parseHomeInput(dic_input) 
    saveMemo(memo)

def schedule_input(res):
    ip_client = res.client_address[0]
    if checkVisit(dic_visit, ip_client) is False:
        return ""

    length = int(res.headers['Content-length'])
    dic_input = parseUTF8(res, length) 

    ym, day, content = parseScheduleInput(dic_input) 
    saveSchedule(ym, day, content)
    str = "?date=%4d-%02d-%02d" % ((ym / 100), ym % 100, day)
    
    return str

def todo_input(res):
    ip_client = res.client_address[0]
    if checkVisit(dic_visit, ip_client) is False:
        return

    length = int(res.headers['Content-length'])
    dic_input = parseUTF8(res, length) 

    dic_todo, date = parseTodoInput(dic_input) 
    list_todo = getTodoList(date)
    modifyTodoList(dic_todo, list_todo)
    saveTodoList(date, list_todo)

    str = date.strftime("?date=%Y-%m-%d")

    return str

def stock_input(res):
    ip_client = res.client_address[0]
    if checkVisit(dic_visit, ip_client) is False:
        return

    length = int(res.headers['Content-length'])
    ret, is_file = saveFile(res, length)
    if is_file:
        return ret.strftime("?date=%Y-%m-%d")
    else:
        return "?date=" + saveStockDic(ret)

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

def bucketlist(ip_client):
	if checkVisit(dic_visit, ip_client):
		access = True
		makeBucketHTML()
	else:
		access = False
		
	path = "html/bucketlist.html"

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


