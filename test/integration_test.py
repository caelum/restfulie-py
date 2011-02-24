from restfulie.restfulie import Restfulie
from threading import Semaphore

def test_simple_request():
    body = Restfulie.at("http://localhost:20144/hello").get().body
    assert "Response for" in body
    assert "/hello" in body

def test_async_request_will_invoke_its_callback():
    
    barrier = Semaphore(0)
    
    def callback(response):
        body = response.body
        try:
            assert "Response for" in body
            assert "/hello" in body
        finally:
            barrier.release()
    
    Restfulie.at("http://localhost:20144/hello").async(callback).get()
    
    barrier.acquire()
    
