from restfulie.parser import Parser

from mockito import mock, when

def test_parser_follow():

    request = mock()
    processor = mock()
    resource = mock()

    parser = Parser([processor])
    when(processor).execute(parser, request, {}).thenReturn(resource)

    assert parser.follow(request, {}) == resource
