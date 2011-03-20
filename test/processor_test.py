from base64 import encodestring
from mockito import mock, when, verify
from restfulie.processor import ExecuteRequestProcessor, PayloadMarshallingProcessor, \
    RedirectProcessor, AuthenticationProcessor


class request_processor_test:

    def test_execute_should_return_a_resource_without_body(self):

        http = mock()
        response = ({'status': 200}, "body")
        request = mock()
        request.headers = {"Content-Type": "application/xml"}
        request.verb = "GET"
        request.uri = "http://www.caelum.com.br"
        request.callback = None
        request.is_async = False
        request.credentials = None

        when(http).request(request.uri, request.verb, \
                           headers=request.headers).thenReturn(response)

        processor = ExecuteRequestProcessor()
        processor.http = http
        resource = processor.execute([], request)

        assert resource.code == 200
        assert resource.body == "body"

    def test_execute_should_return_a_resource_with_body(self):

        http = mock()
        response = ({'status': 404}, "anybody")
        env = {"body": "body"}
        request = mock()
        request.headers = {"Content-Type": "application/xml"}
        request.verb = "GET"
        request.uri = "http://www.caelum.com.br"
        request.callback = None
        request.is_async = False
        request.credentials = None

        when(http).request(request.uri, request.verb, \
                           env['body'], request.headers).thenReturn(response)

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
        processor.execute(chain, request, env)

        verify(chain).follow(request, {'body': '<product>car</product>'})


class redirect_processor_test:

    def check_redirect_on(self, code):
        http = mock()
        response = {'status': 200}, "anybody"
        request = mock()
        request.headers = {"Content-Type": "application/xml"}
        request.verb = "GET"
        request.uri = "http://www.caelum.com.br"
        result = mock()
        result.code = code
        result.headers = {'Location': 'http://www.caelum.com.br'}
        result.code = '200'
        result.body = "anybody"
        chain = mock()
        when(chain).follow(request, {}).thenReturn(result)
        processor = RedirectProcessor()
        processor.http = http
        processor.redirect = lambda self: response
        resource = processor.execute(chain, request)
        assert resource.code == '200'
        assert resource.body == "anybody"

    def test_redirect(self):
        for codex in RedirectProcessor.REDIRECT_CODES:
            self.check_redirect_on(codex)

class authentication_processor_test:
    
    def setUp(self):
        self.chain = mock()
        self.request = mock()
        self.request.headers = {}
    
    def should_add_simple_auth_credentials_to_request_headers(self):
        self.request.credentials = ('user', 'pass', 'simple')
        authprocessor = AuthenticationProcessor()
        authprocessor.execute(self.chain, self.request, {})
        assert self.request.headers.has_key('authorization')
        assert "Basic" in self.request.headers['authorization']
    
    def should_not_add_auth_credentials_if_none_is_set(self):
        self.request.credentials = None
        authprocessor = AuthenticationProcessor()
        authprocessor.execute(self.chain, self.request, {})
        assert not self.request.headers.has_key('authorization')
