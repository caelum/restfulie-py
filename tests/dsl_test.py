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

    def test_configure_get(self):
        self.dsl.process_flow = mock_method_that_should_be_called_in(self.dsl)
        self.dsl.get()
        assert self.dsl.verb == "GET"
        assert self.dsl.method_was_called

    def test_configure_delete(self):
        self.dsl.process_flow = mock_method_that_should_be_called_in(self.dsl)
        self.dsl.delete()
        assert self.dsl.verb == "DELETE"
        assert self.dsl.method_was_called

    def test_configure_head(self):
        self.dsl.process_flow = mock_method_that_should_be_called_in(self.dsl)
        self.dsl.head()
        assert self.dsl.verb == "HEAD"
        assert self.dsl.method_was_called

    def test_configure_trace(self):
        self.dsl.process_flow = mock_method_that_should_be_called_in(self.dsl)
        self.dsl.trace()
        assert self.dsl.verb == "TRACE"
        assert self.dsl.method_was_called

    def test_configure_options(self):
        self.dsl.process_flow = mock_method_that_should_be_called_in(self.dsl)
        self.dsl.options()
        assert self.dsl.verb == "OPTIONS"
        assert self.dsl.method_was_called

    def test_configure_post(self):
        self.dsl.process_flow = mock_method_that_should_be_called_in(self.dsl)
        self.dsl.post({})
        assert self.dsl.verb == "POST"
        assert self.dsl.method_was_called

    def test_configure_patch(self):
        self.dsl.process_flow = mock_method_that_should_be_called_in(self.dsl)
        self.dsl.patch({})
        assert self.dsl.verb == "PATCH"
        assert self.dsl.method_was_called

    def test_configure_put(self):
        self.dsl.process_flow = mock_method_that_should_be_called_in(self.dsl)
        self.dsl.put({})
        assert self.dsl.verb == "PUT"
        assert self.dsl.method_was_called

def mock_method_that_should_be_called_in(to_be_mocked):
    to_be_mocked.method_was_called = False
    return lambda *ignored_args: setattr(to_be_mocked, 'method_was_called', True)
    
