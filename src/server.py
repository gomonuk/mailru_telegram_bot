import os
from http.server import BaseHTTPRequestHandler, HTTPServer

# Сервер нужен чтобы бот не засыпал на бесплатном тарифе хироку


class HttpGetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("<html><body>Hello</body></html>".encode())


server_address = ("0.0.0.0", int(os.environ.get("PORT", 5000)))

httpd = HTTPServer(server_address, HttpGetHandler)

if __name__ == "__main__":
    httpd.serve_forever()
