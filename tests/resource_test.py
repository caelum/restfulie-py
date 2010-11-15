from restfulie.resource import Resource
from mockito import *

def trivial_test():

    response = ({'status': 200}, "Hello")

    resource = Resource(response)
    assert resource.body == "Hello"
    assert resource.code == 200
