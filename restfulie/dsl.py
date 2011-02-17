from parser import Parser
from processor import RedirectProcessor, PayloadMarshallingProcessor, ExecuteRequestProcessor


class Dsl:

    def __init__(self, uri):
        self.uri = uri
        self.processors = [RedirectProcessor(),
                           PayloadMarshallingProcessor(),
                           ExecuteRequestProcessor(), ]
        self.headers = {'Content-Type': 'application/xml',
                        'Accept': 'application/xml'}

    def __getattr__(self, name):
        if self._is_verb(name):
            self.verb = name.upper()
            return self.process_flow
        else:
            raise AttributeError(name)

    def _is_verb(self, name):
        verbs = ["get", "delete", "trace", "head",
                 "options", "post", "put", "patch"]
        return name in verbs

    def use(self, feature):
        self.processors.insert(0, feature)
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
