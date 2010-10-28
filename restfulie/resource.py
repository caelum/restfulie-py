class Resource (object):

    def __init__(self, response):
        self.response = response

        self.body = self.response.read()
        self.code = self.response.status

