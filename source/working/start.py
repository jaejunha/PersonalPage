import sys
import ssl

from http.server import HTTPServer, BaseHTTPRequestHandler

from python.init import *
from python.page import *
from python.data import *

list_account = []

class HandlerHTTP(BaseHTTPRequestHandler):

    def setup(self):
        BaseHTTPRequestHandler.setup(self)
        self.request.settimeout(1)

    def _set_headers(self, code, type = "html"):
        self.send_response(code)
        if type == "html" or type == "css" or type == "js":
            self.send_header('Content-type', 'text/' + type)
        elif type == "ttf":
            self.send_header('Content-type', 'application/x-font-' + type)
        else:
            self.send_header('Content-type', 'image/' + type)
        self.end_headers()
	
    def _redirect(self, url):
        self.send_response(302)
        self.send_header("Location", url)
        self.end_headers()

    def do_POST(self):
        if self.path == "/check":
            check(self, list_account)
            self._redirect("/")
        elif self.path == "/home":
            home_input(self)
            self._redirect("/home")
        elif self.path == "/schedule":
            para = schedule_input(self)
            self._redirect("/schedule" + para)
        elif self.path == "/todo":
            para = todo_input(self)
            self._redirect("/todo" + para)
        elif self.path == "/stock":
            para = stock_input(self)
            self._redirect("/stock" + para)

    def do_GET(self):
        print(self.path)
        if self.path == "/":
            self.path, access = root(self.client_address[0])
        elif self.path == "/home":
            self.path, access = home(self.client_address[0])
        elif self.path == "/logout":
            self.path, access = logout(self.client_address[0])
        elif self.path == "/logout_inner":
            self.path, access = logout(self.client_address[0])
            self.path = "html/logout.html"
        elif self.path.startswith("/bucketlist"):
            self.path, access = bucketlist(self.client_address[0])
        elif self.path.startswith("/schedule"):
            self.path, access = schedule(self.client_address[0], self.path)
        elif self.path.startswith("/todo"):
            self.path, access = todo(self.client_address[0], self.path)
        elif self.path.startswith("/stock"):
            self.path, access = stock(self.client_address[0], self.path)
        elif self.path == "/test":
            self.path, access = test(self.client_address[0])
        else:
            access = False
            self.path = "." + self.path

        try:
            if checkObject(self.path):
                self._set_headers(200, self.path.split(".")[-1])
                writeObject(self)
	
            else:
                if access is False:
                    raise FileNotFoundError

                self._set_headers(200, "html")
                writeHTML(self)

        except FileNotFoundError:
            self._set_headers(404)
            self.wfile.write(bytes(b"404 Not Found"))		
        except Exception as e:
            print(e)

if __name__ == "__main__":	

    port = getPort()

    if getAccount(list_account) is False:
        sys.exit(1)

    removeNohup()

    server_http = HTTPServer(("", port), HandlerHTTP)
    server_http.socket = ssl.wrap_socket(server_http.socket, server_side = True, certfile = "server.pem", ssl_version = ssl.PROTOCOL_TLS)
    server_http.serve_forever()
