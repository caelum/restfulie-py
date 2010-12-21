from restfulie.resource import Resource
from mockito import *

def trivial_test():

    response = ({'status': 200}, "Hello")

    resource = Resource(response)
    assert resource.body == "Hello"
    assert resource.code == 200

def resource_test():

    response = ({'status': 200, 'content-type':'text/plain; charset=utf-8'}, "Hello")

    r = Resource(response)
    assert r.resource() == "Hello"
