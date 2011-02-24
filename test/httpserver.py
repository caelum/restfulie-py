from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SimpleHTTPServer import SimpleHTTPRequestHandler
from StringIO import StringIO

SimpleHTTPRequestHandler

class RequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self, *args, **kwargs):
        if (self.path == "/stop"):
            self.send_response(200)
            httpd.socket.close()
        else:
            self.wfile.write("Response for %s" % self.path)
            
            
server_address = ('', 20144)
httpd = HTTPServer(server_address, RequestHandler)
try:
    httpd.serve_forever()
except:
    pass
