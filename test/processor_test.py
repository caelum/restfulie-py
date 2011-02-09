from restfulie.processor import *
from mockito import *

class request_processor_test:

    def test_execute_should_return_a_resource_without_body(self):

        http = mock()
        response = ({'status':200}, "body")
        request = mock()
        request.headers = {"Content-Type": "application/xml"}
        request.verb = "GET"
        request.uri = "http://www.caelum.com.br"

        when(http).request(request.uri, request.verb, headers=request.headers).thenReturn(response)

        processor = ExecuteRequestProcessor()
        processor.http = http
        resource = processor.execute([], request)

        assert resource.code == 200
        assert resource.body == "body"

    def test_execute_should_return_a_resource_with_body(self):

        http = mock()
        response = ({'status':404}, "anybody")
        env = {"body": "body"}
        request = mock()
        request.headers = {"Content-Type": "application/xml"}
        request.verb = "GET"
        request.uri = "http://www.caelum.com.br"

        when(http).request(request.uri, request.verb, env['body'], request.headers).thenReturn(response)

        processor = ExecuteRequestProcessor()
        processor.http = http

        resource = processor.execute([], request, env)

        assert resource.code == 404
        assert resource.body == "anybody"

class payload_processor_test:

    def test_payload_is_marshalled(self):

        request = mock()
        request.headers = {'Content-type': 'text/plain'}
        chain = mock()
        env = {'payload': {'product': 'car'}}

        processor = PayloadMarshallingProcessor()
        resource = processor.execute(chain, request, env)

        verify(chain).follow(request, {'body': '<product>car</product>'})

class redirect_201_processor_test:

    def test_redirect_on_201(self):

        http = mock()
        response = ({'status':200}, "anybody")

        request = mock()
        request.headers = {"Content-Type": "application/xml"}
        request.verb = "GET"
        request.uri = "http://www.caelum.com.br"

        result = mock()
        result.code = 201
        result.headers = {'Location': 'http://www.caelum.com.br'}

        finalresult = mock()
        result.code = 200
        result.body = "anybody"

        chain = mock()
        when(chain).follow(request, {}).thenReturn(result)

        processor = RedirectProcessor()
        processor.http = http

        processor.redirect = lambda self: response
        resource = processor.execute(chain, request)

        assert resource.code == 200
        assert resource.body == "anybody"

