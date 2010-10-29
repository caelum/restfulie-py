from request import RequestDSL

class Restfulie:

    @staticmethod
    def at(uri):
        return RequestDSL(uri)
