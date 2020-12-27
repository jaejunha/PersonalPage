import sys
import random
import requests
import datetime
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

CONST_PORT = None 
CONST_8KB = 8192 

CONST_ID = 0
CONST_PWD = 1

TIME_VISIT = 240

list_account = []
dic_visit = {}
dic_alert = {}

def getPort():
	global CONST_PORT

	try:
		file = open("config/port.csv", "r")
		CONST_PORT = int(file.readlines()[0].strip())
	except FileNotFoundError:
		CONST_PORT = 80

def getAccount():
	global list_account
	
	try:
		file = open("config/password.csv", "r")
		for line in file.readlines():
			list_ele = line.split(",")
			list_account.append( (list_ele[CONST_ID].strip(), list_ele[CONST_PWD].strip()) )
	except FileNotFoundError:
		print("관리자 계정을 만드세요!")
		sys.exit(1)

def checkImage(path):
	return ".png" in path or ".jpg" in path or ".gif" in path or ".ico" in path

def checkVisit(ip):
	if (ip in dic_visit) is False:
		return False

	now = datetime.datetime.now()
	return now < dic_visit[ip]

def calVisit():
	now = datetime.datetime.now()
	return now + datetime.timedelta(minutes = TIME_VISIT)

def getMenu():
	str = ""
	file = open("config/menu.csv", "r")
	for line in file.readlines():
		if len(line) > 0:
			list_line = line.split(",")
			name = list_line[0].strip()
			link = list_line[1].strip()
			str += '<span><a href="' + link + '">' + name + "</a></span><br>"

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
	return str[:-4]

class HandlerHTTP(BaseHTTPRequestHandler):

	def setup(self):
		BaseHTTPRequestHandler.setup(self)
		self.request.settimeout(1)

	def _set_headers(self, code, type = "html"):
		self.send_response(code)
		if type == "html":
			self.send_header('Content-type', 'text/html')
		else:
			self.send_header('Content-type', 'image/' + type)
		self.end_headers()
	
	def _redirect(self, url):
		self.send_response(302)
		self.send_header("Location", url)
		self.end_headers()

	def do_POST(self):
		access = False
		if self.path == "/check":

			length = int(self.headers['Content-length'])
			raw_data = self.rfile.read(length).decode("utf-8") 
			list_data = raw_data.split("&")

			for account in list_account:
				if account[CONST_ID] == list_data[CONST_ID].split("=")[1] and account[CONST_PWD] == list_data[CONST_PWD].split("=")[1]:
					access = True

			ip_client = self.client_address[0]
			if access:
				dic_alert[ip_client] = False
				dic_visit[self.client_address[0]] = calVisit() 
			else:
				dic_alert[ip_client] = True
	
			self._redirect("/")

	def do_GET(self):
		ip_client = self.client_address[0]

		access = False
		if self.path == "/":
			access = True

			if checkVisit(ip_client):
				dic_visit[ip_client] = calVisit()
				self.path = "html/index.html"
			elif ip_client in dic_alert.keys() and dic_alert[ip_client]:
				self.path = "html/login_fail.html"
			else:
				self.path = "html/login_normal.html"

		elif self.path == "/logout":
			access = True

			if checkVisit(ip_client):
				del dic_visit[ip_client]
				
			self.path = "html/login_normal.html"	

		else:
			self.path = "." + self.path

		try:
			if checkImage(self.path):
				access = True

				self._set_headers(200, self.path.split(".")[-1])

				file = open(self.path, "rb")
				data = file.read(CONST_8KB)
				self.wfile.write(data)

				while data:
					data = file.read(CONST_8KB)
					self.wfile.write(data)
			else:
				if access is False:
					raise FileNotFoundError

				self._set_headers(200, "html")
				file = open(self.path, "r", encoding = "utf-8")
				str_data = ""
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

					str_data += line
				self.wfile.write(str_data.encode())

			file.close()

		except FileNotFoundError:
			self._set_headers(404)
			self.wfile.write(bytes(b"404 Not Found"))		
		except Exception as e:
			print(e)

if __name__ == "__main__":	
	getPort()
	getAccount()
	server_http = HTTPServer(("", CONST_PORT), HandlerHTTP)
	server_http.serve_forever()
