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
        
    def should_perform_assynchronous_requests_with_arguments_to_the_callback_function(self):
        
        barrier = Semaphore(0)
        
        def callback(response, extra1, extra2):
            body = response.body
            try:
                assert "Response for" in body
                assert "/hello" in body
                assert extra1 == "first"
                assert extra2 == "second"
            finally:
                barrier.release()
        
        Restfulie.at("http://localhost:20144/hello").async(callback, args=("first", "second")).get()
        
        barrier.acquire()