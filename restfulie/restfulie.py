from dsl import Dsl


class Restfulie(object):
    """
    Restfulie DSL entry point.
    """

    @staticmethod
    def at(uri):
        """
        Create a new entry point for executing requests to the given uri.
        """
        return Dsl(uri)
