from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)

    def do_GET(self):
        img = self.rfile.read(int(self.headers.get('Content-Length')))
        with open ('img.png', 'wb') as f:
            f.write(img)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, World!')
    
    def do_POST(self):
        print('posted on' + self.path)

httpd = HTTPServer(('', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()