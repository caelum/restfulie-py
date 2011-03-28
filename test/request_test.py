from restfulie.dsl import Dsl
from restfulie.request import Request
from mockito import mock
from threading import Semaphore


class callable_mock():

    def __init__(self):
        self.called = 0

    def __call__(self, *args, **kwargs):
        self.called = self.called + 1


class http_method_test:

    def setup(self):
        self.dsl = mock(Dsl)
        self.request = Request(self.dsl)

    def should_make_synchronous_invocations_with_simple_auth(self):
        self.dsl.credentials = 'test:test'
        self.dsl.callback = None
        self.dsl.is_async = False
        self.request._process_flow = callable_mock()
        self.request()
        assert self.request._process_flow.called == 1

    def should_make_synchronous_invocations_if_callback_isnt_configured(self):
        self.dsl.callback = None
        self.dsl.is_async = False
        self.request._process_flow = callable_mock()
        self.request()
        assert self.request._process_flow.called == 1

    def should_make_asynchronous_invocations_if_callback_is_configured(self):
        self.dsl.callback = lambda: None
        self.dsl.is_async = True
        self.request._process_async_flow = callable_mock()
        self.request()
        assert self.request._process_async_flow.called == 1

    def should_call_callback_function_on_asynchronous_request(self):
        barrier = Semaphore(0)

        def callback(request):
            barrier.release()

        self.dsl.is_async = True
        self.dsl.callback = callback
        self.dsl.callback_args = ()
        self.request._process_flow = lambda payload: None
        self.request()

        barrier.acquire()

    def should_call_callback_on_async_request_and_pass_arguments(self):
        barrier = Semaphore(0)

        def callback(request, arg1, arg2, arg3):
            assert (arg1, arg2, arg3) == (1, 2, 3)
            barrier.release()

        self.dsl.is_async = True
        self.dsl.callback = callback
        self.dsl.callback_args = (1, 2, 3)
        self.request._process_flow = lambda payload: None
        self.request()

        barrier.acquire()
