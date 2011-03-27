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

    def do_POST(self, *args, **kwargs):
        content_size = int(self.headers.getheader('content-length'))
        body = self.rfile.read(content_size)
        self.wfile.write('This is a test.')
        if '<action>' in body:
            if body.split('<action>') == 'test':
                self.wfile.write('This is a test.')
        else:
            self.wfile.write('Fail.')

server_address = ('', 20144)
httpd = HTTPServer(server_address, RequestHandler)
try:
    httpd.serve_forever()
except:
    pass
