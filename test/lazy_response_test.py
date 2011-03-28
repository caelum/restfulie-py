from multiprocessing import Pipe
from restfulie.response import LazyResponse, Response
from mockito import mock, verify


class lazy_response_test:
    
    def forwarding_attrs_from_real_response_test(self):
    
        response = mock()
        response.code = 200
        response.body = 'Hello'
    
        child_pipe = None
        lazy_response = LazyResponse(child_pipe)
        lazy_response._response = response
    
        assert lazy_response.code == 200
        assert lazy_response.body == 'Hello'
        verify(response).code
        verify(response).body
    
    
    def simple_test(self):
    
        response = ({'status': 200}, 'Hello')
        r = Response(response)
    
        pipe, child_pipe = Pipe()
        lazy_response = LazyResponse(child_pipe)
        pipe.send(r)
    
        assert lazy_response.code == 200
        assert lazy_response.body == 'Hello'
    
    
    def resource_test(self):
    
        response = ({'status': 200, 'content-type': 'text/plain; charset=utf-8'}, \
                     'Hello')
        r = Response(response)
    
        pipe, child_pipe = Pipe()
        lazy_response = LazyResponse(child_pipe)
        pipe.send(r)
    
        assert lazy_response.resource() == 'Hello'
    
    
    def link_test(self):
    
        response = ({'status': 200, 'link': '</feed>; rel="alternate"'}, 'Hello')
        r = Response(response)
    
        pipe, child_pipe = Pipe()
        lazy_response = LazyResponse(child_pipe)
        pipe.send(r)
    
        link = lazy_response.link('alternate')
        assert link.href == '/feed'
        assert link.rel == 'alternate'
