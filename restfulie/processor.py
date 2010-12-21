import httplib2
from resource import Resource
from converters import Converters, PlainConverter
import restfulie

class RequestProcessor:
    pass

class ExecuteRequestProcessor(RequestProcessor):

    def __init__(self):
        self.http = httplib2.Http()

    def execute(self, chain, request, env={}):
        if "body" in env:
            response = self.http.request(request.uri, request.verb, env.get("body"), request.headers)
        else:
            response = self.http.request(request.uri, request.verb, headers=request.headers)

        resource = Resource(response)

        return resource

class PayloadMarshallingProcessor(RequestProcessor):

    def execute(self, chain, request, env={}):
        if "payload" in env:
            marshaller = Converters.marshaller_for(request.headers.get("Content-type"))
            env["body"] = marshaller.marshal(env["payload"])
            del(env["payload"])

        return chain.follow(request, env)

class RedirectProcessor(RequestProcessor):

    def execute(self, chain, request, env={}):
        result = chain.follow(request, env)
        if result.code == 201:
            location = result.headers["Location"] or result.headers["location"]
            if location:
                return self.redirect(location)

        return result

    def redirect(self, location):
        return restfulie.Restfulie.at_(location).get()
