class Parser:

    def __init__(self, processors):
        self.processors = processors

    def follow(self, request, env={}):
        processor = self.processors.pop(0)
        result = processor.execute(self, request, env)
        return result
