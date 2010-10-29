import httplib
from resource import Resource
from converters import Converters, GenericMarshaller

class RequestProcessor:
    pass

class ExecuteRequestProcessor(RequestProcessor):

    def execute(self, chain, request, env={}):
        connection = httplib.HTTPConnection(request.uri)

        if "body" in env:
            connection.request(request.verb, "/", env["body"], request.headers)
        else:
            connection.request(request.verb, "/", headers=request.headers)

        resource = Resource(connection.getresponse())

        return resource

class PayloadMarshallingProcessor(RequestProcessor):

    def execute(self, chain, request, env={}):
        if "payload" in env:
            marshaller = Converters.marshaller_for(request.headers["Content-type"]) or GenericMarshaller()
            env["body"] = marshaller.marshal(env["payload"])
            del(env["payload"])

        return chain.follow(request, env)

"""
class Redirect201Processor (RequestProcessor):

    def execute(self, chain, request, env)
        result = chain.follow(request, env)
        if request.code==201
            Restfulie.at(request.headers("Location")).get
        else
            return result
"""
