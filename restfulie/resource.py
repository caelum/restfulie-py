class Resource:

    def __init__(self, response):

        self.response = response

        self.code = self.response[0]['status']
        self.body = self.response[1]

