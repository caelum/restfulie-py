from restfulie.restfulie import Restfulie
from threading import Semaphore

class integration_test:
    
    def should_perform_ordinary_requests(self):
        body = Restfulie.at("http://localhost:20144/hello").get().body
        assert "Response for" in body
        assert "/hello" in body

    
    def should_perform_assynchronous_requests(self):
        
        def callback(response):
            body = response.body
            assert "Response for" in body
            assert "/hello" in body
        
        r = Restfulie.at("http://localhost:20144/hello").async(callback).get()
        assert "Response for" in r.body
        assert "/hello" in r.body

        
    def should_perform_assynchronous_requests_with_arguments_to_the_callback_function(self):
        
        def callback(response, extra1, extra2):
            body = response.body
            assert "Response for" in body
            assert "/hello" in body
            assert extra1 == "first"
            assert extra2 == "second"
        
        r = Restfulie.at("http://localhost:20144/hello").async(callback, args=("first", "second")).get()
        assert "Response for" in r.body
        assert "/hello" in r.body

        
    def should_perform_assynchronous_requests_with_arguments_to_the_callback_function(self):
        pass