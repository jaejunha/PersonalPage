import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

from python.init import *
from python.account import *
from python.replace import *

CONST_8KB = 8192 

list_account = []
list_link = []
dic_visit = {}
dic_alert = {}

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
		access = False
		if self.path == "/check":

			if checkAccount(self, list_account):
				access = True

			ip_client = self.client_address[0]
			if access:
				dic_alert[ip_client] = False
				dic_visit[self.client_address[0]] = calSessionLength() 
			else:
				dic_alert[ip_client] = True
	
			self._redirect("/")

	def do_GET(self):
		ip_client = self.client_address[0]

		access = False
		if self.path == "/":
			access = True

			if checkVisit(dic_visit, ip_client):
				dic_visit[ip_client] = calSessionLength()
				self.path = "html/index.html"
			elif ip_client in dic_alert.keys() and dic_alert[ip_client]:
				self.path = "html/login_fail.html"
			else:
				self.path = "html/login_normal.html"

		elif self.path == "/logout":
			access = True

			if checkVisit(dic_visit, ip_client):
				del dic_visit[ip_client]
				
			self.path = "html/login_normal.html"	

		elif checkVisit(dic_visit, ip_client) and (self.path[1:] in list_link):
			access = True
			
			self.path = "html" + self.path + ".html"

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

	port = getPort()

	if getLink(list_link) is False:
		sys.exit(1)

	if getAccount(list_account) is False:
		sys.exit(1)

	server_http = HTTPServer(("", port), HandlerHTTP)
	server_http.serve_forever()
