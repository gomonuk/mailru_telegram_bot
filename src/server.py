import os
from http.server import BaseHTTPRequestHandler, HTTPServer


class HttpGetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("<html><body>Был получен GET-запрос.</body></html>".encode())


try:
    port = int(os.environ.get("PORT"))
except Exception as e:
    print(e)
    port = 80

server_address = ("localhost", port)

httpd = HTTPServer(server_address, HttpGetHandler)

if __name__ == "__main__":
    httpd.serve_forever()
