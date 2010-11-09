from processor import ExecuteRequestProcessor, PayloadMarshallingProcessor
from parser import Parser

class RequestDSL:

    def __init__ (self, uri):
        self.uri = uri
        self.processors = [PayloadMarshallingProcessor(), ExecuteRequestProcessor()]
        self.headers = {}

    def use(self, feature):
        self.processor.append(feature)
        return self

    def typed(self, content_type):
        self.headers["Content-type"] = content_type
        return self

    def get(self):
        self.verb = "GET"
        return self.process_flow()

    def delete(self):
        self.verb = "DELETE"
        return self.process_flow()

    def post(self, payload):
        self.verb = "POST"
        return self.process_flow(env={'payload':payload})
    
    def patch(self, payload):
        self.verb = "PATCH"
        return self.process_flow(env={'payload':payload})
    
    def put(self, payload):
        self.verb = "PUT"
        return self.process_flow(env={'paylaod':payload})

    def process_flow(self, env={}):
        procs = list(self.processors)
        return Parser(procs).follow(self, env)
