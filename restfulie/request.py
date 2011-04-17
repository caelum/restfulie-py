from response import LazyResponse
from parser import Parser
from threading import Thread
from multiprocessing import Pipe


class Request(object):
    """
    HTTP request.
    """

    def __init__(self, config):
        """
        Initialize an HTTP request instance for a given configuration.
        """
        self.config = config

    def __call__(self, **kwargs):
        """
        Perform the request

        The optional payload argument is sent to the server.
        """
        if (not self.config.is_async):
            return self._process_flow(kwargs)
        else:
            return self._process_async_flow(kwargs)

    def _process_flow(self, payload):
        """
        Put payload environment and start the chain.
        """
        env = {}
        if payload:
            env = {'payload': payload}

        procs = list(self.config.processors)
        return Parser(procs).follow(self.config, env)

    def _process_async_flow(self, payload):
        """
        Starts an async chain.
        """

        self.config.pipe, child_pipe = Pipe()

        def handle_async():
            if self.config.is_async and self.config.callback is None:
                self._process_flow(payload=payload)
            else:
                self.config.callback(self._process_flow(payload=payload), \
                                     *self.config.callback_args)

        self._start_new_thread(handle_async)

        return LazyResponse(child_pipe)

    def _start_new_thread(self, target):
        thread = Thread(target=target)
        thread.start()
