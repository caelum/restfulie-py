from restfulie.resource import Resource
from mockito import *

def trivial_test():
    response = mock()
    response.status = 200
    when(response).read().thenReturn("Hello")
    
    resource = Resource(response)
    assert resource.body == "Hello"
    assert resource.code == 200