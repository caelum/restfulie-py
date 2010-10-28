from processor import ExecuteRequestProcessor
from parser import Parser

class RequestDSL (object):

    def __init__ (self, uri):
        self.uri = uri
        self.processors = [ExecuteRequestProcessor()]

    def use(feature):
        self.processor.append(feature)

    def get(self):
        self.verb = "GET"
        return self.process_flow()

    def delete(self):
        self.verb = "DELETE"
        return self.process_flow()

    def process_flow(self):
        procs = list(self.processors)
        return Parser(procs).follow(self, {})
