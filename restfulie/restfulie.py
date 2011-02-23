from dsl import Dsl


class Restfulie(object):

    @staticmethod
    def at(uri):
        return Dsl(uri)
