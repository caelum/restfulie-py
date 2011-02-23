from parser import Parser
from threading import Thread


class Request(object):
    """
    Execute HTTP requests given a configuration.
    """
    
    def __init__(self, config):
        self.config = config
        
    def __call__(self, payload=None):
        if (self.config.callback is None):
            return self._process_flow(payload)
        else:
            return self._process_async_flow(payload)
    
    def _process_flow(self, payload):
        env = {}
        if payload:
            env = {'payload': payload}

        procs = list(self.config.processors)
        return Parser(procs).follow(self.config, env)

    def _process_async_flow(self, payload):
        
        def handle_async():
            self.config.callback(self._process_flow(payload=payload))
        
        self._start_new_thread(handle_async)
    
    def _start_new_thread(self, target):
        thread = Thread(target=target)
        thread.start()
