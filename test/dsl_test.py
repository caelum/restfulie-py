from restfulie.dsl import Dsl
from restfulie.processor import ExecuteRequestProcessor

class dsl_test:

    def setup(self):
        self.dsl = Dsl("www.caelum.com.br")

    def test_add_a_process_method(self):
        processor = ExecuteRequestProcessor()
        assert self.dsl.use(processor) == self.dsl
        assert self.dsl.processors[0] == processor

    def test_configure_content_type(self):
        self.dsl.as_("content")
        assert self.dsl.headers["Content-Type"] == "content"
        
    def test_configure_valid_http_methods(self):
        for verb in Dsl.HTTP_VERBS:
            method = self.dsl.__getattr__(verb)
            assert method.config == self.dsl
            assert self.dsl.verb == verb.upper()
    
    def test_not_configure_invalid_http_method(self):
        try:
            self.dsl.poop
            raise AssertionError("should have failed")
        except AttributeError:
            pass

    def test_configure_callback(self):
        def callback(*args):
            pass
        
        self.dsl.async(callback)
        assert self.dsl.callback == callback
        