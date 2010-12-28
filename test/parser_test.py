from restfulie.parser import Parser
from restfulie.processor import ExecuteRequestProcessor

from mockito import *

def test_parser_follow():

    request = mock()
    processor = mock()
    resource = mock()

    parser = Parser([processor])
    when(processor).execute(parser, request, {}).thenReturn(resource)

    assert parser.follow(request, {}) == resource
