from restfulie.restfulie import Restfulie
from threading import Semaphore

def test_simple_request():
    assert Restfulie.at("http://caelum.com.br/").get().body is not None



def test_async_request_will_invoke_its_callback():
    
    barrier = Semaphore(0)
    
    def callback(response):
        barrier.release()
    
    Restfulie.at("http://caelum.com.br/cursos").calling_back(callback).get()
    
    barrier.acquire()
    
