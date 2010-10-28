import httplib
from resource import Resource

class RequestProcessor (object):
    pass

class ExecuteRequestProcessor (RequestProcessor):

    def execute(self, chain, request, env):
        connection = httplib.HTTPConnection(request.uri)

        # Use headers
        connection.request(request.verb, "/")

        resource = Resource(connection.getresponse())

        return resource

"""
class Redirect201Processor (RequestProcessor):

    def execute(self, chain, request, env)
        result = chain.follow(request, env)
        if request.code==201
            Restfulie.at(request.headers("Location")).get
        else
            return result
"""
