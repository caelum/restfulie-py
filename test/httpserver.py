from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SimpleHTTPServer import SimpleHTTPRequestHandler
from StringIO import StringIO

SimpleHTTPRequestHandler

class RequestHandler(BaseHTTPRequestHandler):
    
    def _response(self):
        return StringIO()
    
    def do_GET(self, *args, **kwargs):
        if (self.path == "/hello"):
            self.wfile.write("Hello, world!")
        if (self.path == "/stop"):
            self.send_response(200)
            httpd.socket.close()
            
            
server_address = ('', 20144)
httpd = HTTPServer(server_address, RequestHandler)
try:
    httpd.serve_forever()
except:
    pass
