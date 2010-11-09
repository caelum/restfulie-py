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
        self.dsl.typed("content")
        assert self.dsl.headers["Content-type"] == "content"
        
    def test_configure_get(self):
        self.dsl.process_flow = lambda:[]
        self.dsl.get()
        assert self.dsl.verb == "GET"
        
    def test_configure_delete(self):
        self.dsl.process_flow = lambda:[]
        self.dsl.delete()
        assert self.dsl.verb == "DELETE"
        
    def test_configure_head(self):
        self.dsl.process_flow = lambda:[]
        self.dsl.head()
        assert self.dsl.verb == "HEAD"
        
    def test_configure_trace(self):
        self.dsl.process_flow = lambda:[]
        self.dsl.trace()
        assert self.dsl.verb == "TRACE"
        
    def test_configure_options(self):
        self.dsl.process_flow = lambda:[]
        self.dsl.options()
        assert self.dsl.verb == "OPTIONS"
        
    def test_configure_post(self):
        self.dsl.process_flow = lambda env:[]
        self.dsl.post({})
        assert self.dsl.verb == "POST"
        
    def test_configure_patch(self):
        self.dsl.process_flow = lambda env:[]
        self.dsl.patch({})
        assert self.dsl.verb == "PATCH"
        
    def test_configure_put(self):
        self.dsl.process_flow = lambda env:[]
        self.dsl.put({})
        assert self.dsl.verb == "PUT"