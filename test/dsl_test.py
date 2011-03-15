from restfulie.dsl import Dsl
from restfulie.processor import ExecuteRequestProcessor

class dsl_test:

    def setup(self):
        self.dsl = Dsl("www.caelum.com.br")

    def should_add_a_processor(self):
        processor = ExecuteRequestProcessor()
        assert self.dsl.use(processor) == self.dsl
        assert self.dsl.processors[0] == processor

    def should_configure_the_content_type(self):
        self.dsl.as_("content")
        assert self.dsl.headers["Content-Type"] == "content"
        
    def should_configure_valid_http_methods(self):
        for verb in Dsl.HTTP_VERBS:
            method = self.dsl.__getattr__(verb)
            assert method.config == self.dsl
            assert self.dsl.verb == verb.upper()
            
    def should_parse_simple_auth_credentials(self):
        dsl = Dsl('http://test:test@caelum.com.br')
        assert dsl.credentials == "test:test"
        assert dsl.uri == "http://caelum.com.br"
    
    def should_fail_when_asked_to_use_an_invalid_http_method(self):
        try:
            self.dsl.poop
            raise AssertionError("should have failed")
        except AttributeError:
            pass

    def should_configure_the_callback_method(self):
        def callback(*args):
            pass
        
        self.dsl.async(callback)
        assert self.dsl.callback == callback
        