import sys
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
            check(self, list_account)
            self._redirect("/")
        elif self.path == "/home":
            home_input(self)
            self._redirect("/home")
        elif self.path == "/todo":
            todo_input(self)
            self._redirect("/todo")
        elif self.path == "/stock":
            stock_input(self)
            self._redirect("/stock")

    def do_GET(self):
        print(self.path)
        if self.path == "/":
            self.path, access = root(self.client_address[0])
        elif self.path == "/home":
            self.path, access = home(self.client_address[0])
        elif self.path == "/logout":
            self.path, access = logout(self.client_address[0])
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
            if checkImage(self.path):
                self._set_headers(200, self.path.split(".")[-1])
                writeImage(self)
	
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

    server_http = HTTPServer(("", port), HandlerHTTP)
    server_http.serve_forever()
