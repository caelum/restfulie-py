from converters import Converters

class Resource:

    def __init__(self, response):

        self.response = response
        self.headers = self.response[0]
        self.code = self.response[0]['status']
        self.body = self.response[1]

    def resource(self):

        if 'content-type' in self.response[0]:
            contenttype = self.response[0]['content-type'].split(';')[0]
        else:
            contenttype = None

        converter = Converters.marshaller_for(contenttype)
        return converter.unmarshal(self.body)

