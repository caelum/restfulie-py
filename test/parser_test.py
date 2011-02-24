from restfulie.parser import Parser

from mockito import mock, when

class parser_test:

    def should_execute_processor(self):
    
        request = mock()
        processor = mock()
        resource = mock()
    
        parser = Parser([processor])
        when(processor).execute(parser, request, {}).thenReturn(resource)
    
        assert parser.follow(request, {}) == resource
