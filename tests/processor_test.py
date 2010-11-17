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

    pass
