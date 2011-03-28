from base64 import encodestring
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self, *args, **kwargs):
        if (self.path == "/stop"):
            self.send_response(200)
            httpd.socket.close()
        else:
            if not self.path == "/auth":
                self.wfile.write("Response for %s %s" % \
                                (self.path, str(self.headers)))
            else:
                auth = self.headers.getheader('authorization')
                if auth == "Basic %s" % encodestring('test:test')[:-1]:
                    self.wfile.write('worked')

server_address = ('', 20144)
httpd = HTTPServer(server_address, RequestHandler)
try:
    httpd.serve_forever()
except:
    pass
