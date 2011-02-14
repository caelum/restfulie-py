from dsl import Dsl


class Restfulie:

    @staticmethod
    def at(uri):
        return Dsl(uri)
