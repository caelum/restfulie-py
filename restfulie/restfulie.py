from request import RequestDSL

class Restfulie (object):

    @staticmethod
    def at(uri):
        return RequestDSL(uri)
