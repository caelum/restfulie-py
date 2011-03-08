import httplib2
from response import Response
from converters import Converters
import restfulie


class RequestProcessor(object):
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
        if request.is_async:
            request.pipe.send(resource)

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
    """
    A processor responsible for redirecting a client to another URI when the server
    returns the location header and a response code related to redirecting.
    """
    REDIRECT_CODES = ['201', '301', '302']

    def redirect_location_for(self, result):
        if (result.code in self.REDIRECT_CODES):
            return (result.headers.get("Location") or
                    result.headers.get("location"))
        return None

    def execute(self, chain, request, env={}):
        result = chain.follow(request, env)
        location = self.redirect_location_for(result)
        if location:
            return self.redirect(location,
                                 request.headers.get("Content-Type"))
            
        return result

    def redirect(self, location, request_type):
        return restfulie.Restfulie.at(location).as_(request_type).get()
