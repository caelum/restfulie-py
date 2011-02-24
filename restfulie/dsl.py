from processor import RedirectProcessor, PayloadMarshallingProcessor, \
    ExecuteRequestProcessor
from request import Request

class Dsl(object):
    
    HTTP_VERBS = ["get", "delete", "trace", "head", "options", "post", "put", "patch"]

    def __init__(self, uri):
        self.uri = uri
        self.processors = [RedirectProcessor(),
                           PayloadMarshallingProcessor(),
                           ExecuteRequestProcessor(), ]
        self.headers = {'Content-Type': 'application/xml',
                        'Accept': 'application/xml'}
        self.callback = None
        self.callback_args = ()

    def __getattr__(self, name):
        if (self._is_verb(name)):
            self.verb = name.upper()
            return Request(self)
        else:
            raise AttributeError(name)

    def _is_verb(self, name):
        return name in self.HTTP_VERBS

    def use(self, feature):
        self.processors.insert(0, feature)
        return self

    def async(self, callback, args=()):
        self.callback = callback
        self.callback_args = args
        return self

    def as_(self, content_type):
        if content_type:
            self.headers["Content-Type"] = content_type
        return self

    def accepts(self, content_type):
        self.headers['Accept'] = content_type
        return self
    