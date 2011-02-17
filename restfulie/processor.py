import httplib2
from response import Response
from converters import Converters
import restfulie


class RequestProcessor:
    pass


class ExecuteRequestProcessor(RequestProcessor):

    def __init__(self):
        self.http = httplib2.Http()

    def execute(self, chain, request, env={}):
        if "body" in env:
            response = self.http.request(request.uri, request.verb,
                                         env.get("body"), request.headers)
        else:
            response = self.http.request(request.uri, request.verb,
                                         headers=request.headers)

        resource = Response(response)

        return resource


class PayloadMarshallingProcessor(RequestProcessor):

    def execute(self, chain, request, env={}):
        if "payload" in env:
            content_type = request.headers.get("Content-Type")
            marshaller = Converters.marshaller_for(content_type)
            env["body"] = marshaller.marshal(env["payload"])
            del(env["payload"])

        return chain.follow(request, env)


class RedirectProcessor(RequestProcessor):

    def execute(self, chain, request, env={}):
        result = chain.follow(request, env)
        if result.code == '201' or result.code == '302':
            location = (result.headers.get("Location") or
                        result.headers.get("location"))
            if location:
                return self.redirect(location,
                                     request.headers.get("Content-Type"))

        return result

    def redirect(self, location, request_type):
        return restfulie.Restfulie.at(location).as_(request_type).get()
