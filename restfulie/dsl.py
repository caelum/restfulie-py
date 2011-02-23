from parser import Parser
from processor import RedirectProcessor, PayloadMarshallingProcessor, ExecuteRequestProcessor
from threading import Thread

def start_new_thread(target):
    thread = Thread(target=target)
    thread.start()


class Dsl:

    def __init__(self, uri):
        self.uri = uri
        self.processors = [RedirectProcessor(),
                           PayloadMarshallingProcessor(),
                           ExecuteRequestProcessor(), ]
        self.headers = {'Content-Type': 'application/xml',
                        'Accept': 'application/xml'}
        self.callback = None

    def __getattr__(self, name):
        if (self._is_verb(name) and self.callback is None):
            self.verb = name.upper()
            return self.process_flow
        elif (self._is_verb(name) and self.callback is not None):
            self.verb = name.upper()
            return self._process_async_flow
        else:
            raise AttributeError(name)

    def _is_verb(self, name):
        verbs = ["get", "delete", "trace", "head",
                 "options", "post", "put", "patch"]
        return name in verbs

    def use(self, feature):
        self.processors.insert(0, feature)
        return self

    def async(self, callback):
        self.callback = callback
        return self

    def as_(self, content_type):
        if content_type:
            self.headers["Content-Type"] = content_type
        return self

    def accepts(self, content_type):
        self.headers['Accept'] = content_type
        return self

    def process_flow(self, payload=None):
        env = {}
        if payload:
            env = {'payload': payload}

        procs = list(self.processors)
        return Parser(procs).follow(self, env)

    def _process_async_flow(self, payload=None):
        
        def handle_async():
            self.callback(self.process_flow(payload=payload))
        
        start_new_thread(handle_async)