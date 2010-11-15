import httplib2
from resource import Resource
from converters import Converters, GenericMarshaller

class RequestProcessor:
    pass

class ExecuteRequestProcessor(RequestProcessor):

    def execute(self, chain, request, env={}):
        http = httplib2.Http()

        if "body" in env:
            response = http.request(request.uri, request.verb, env["body"], request.headers)
        else:
            response = http.request(request.uri, request.verb, headers=request.headers)

        resource = Resource(response)

        return resource

class PayloadMarshallingProcessor(RequestProcessor):

    def execute(self, chain, request, env={}):
        if "payload" in env:
            if "Content-type" in request.headers:
                marshaller = Converters.marshaller_for(request.headers["Content-type"])
            else:
                marshaller = GenericMarshaller()
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
