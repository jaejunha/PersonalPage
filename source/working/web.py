import sys
import random
import requests
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

CONST_PORT = None 
CONST_8KB = 8192 

list_account = []
list_visit = []

def getPort():
	global CONST_PORT

	try:
		file = open("port.csv", "r")
		CONST_PORT = int(file.readlines()[0].strip())
	except FileNotFoundError:
		CONST_PORT = 80

def getAccount():
	global list_account
	
	try:
		file = open("password.csv", "r")
		for line in file.readlines():
			list_ele = line.split(",")
			list_account.append( (list_ele[0].strip(), list_ele[1].strip()) )
	except FileNotFoundError:
		print("관리자 계정을 만드세요!")
		sys.exit(1)

def checkImage(path):
	return ".png" in path or ".jpg" in path or ".gif" in path or ".ico" in path

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
		if self.path == "/check":
			global list_visit
			access = False
			length = int(self.headers['Content-length'])
			raw_data = self.rfile.read(length).decode("utf-8") 
			list_data = raw_data.split("&")
			for account in list_account:
				if account[0] == list_data[0].split("=")[1] and account[1] == list_data[1].split("=")[1]:
					access = True
			if access:
				list_visit.append(self.client_address[0])
		
			self.send_response(302)
			self.send_header('Location', "/")
			self.end_headers()

	def do_GET(self):
		ip_client = self.client_address[0]

		access = False
		if self.path == "/":
			access = True
			if ip_client in list_visit:
				self.path = "index.html"
			else:
				self.path = "login.html"

		elif self.path == "/logout":
			access = True
			global last_visit

			for i, ip in enumerate(list_visit[:]):
				if ip == ip_client:
					del list_visit[i]
					break
				
			self.path = "login.html"	

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
					"""
					if ":)" in line:
						start = line.find(":)")
						end = line.find("&")
						path = "_post/" + line[start + 2: end] + ".txt"
						content = getContent(path)
						line = line.replace(line[start: end + 1], content)
					"""	
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
