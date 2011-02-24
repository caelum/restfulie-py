from restfulie.restfulie import Restfulie
from threading import Semaphore

class integration_test:
    
    def should_perform_ordinary_requests(self):
        body = Restfulie.at("http://localhost:20144/hello").get().body
        assert "Response for" in body
        assert "/hello" in body
    
    def should_perform_assynchronous_requests(self):
        
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
        
