from restfulie.restfulie import Restfulie
from threading import Semaphore


class integration_test:

    def should_perform_ordinary_requests(self):
        body = Restfulie.at("http://localhost:20144/hello").get().body
        assert "Response for" in body
        assert "/hello" in body

    def should_perform_requests_with_parameters_as_kwargs(self):
        response = Restfulie.at("http://localhost:20144").post(action="test")
        print response.body
        body = response.body
        assert "This is a test" in body

    def should_perform_ordinary_requests_with_simple_auth(self):
        r = Restfulie.at("http://localhost:20144/auth").auth('test', 'test')
        response = r.get()
        body = response.body
        assert "worked" in body

    def should_perform_async_requests(self):
        barrier = Semaphore(0)

        def callback(response):
            body = response.body
            assert "Response for" in body
            assert "/hello" in body
            barrier.release()

        r = Restfulie.at("http://localhost:20144/hello").async(callback).get()
        barrier.acquire()
        assert "Response for" in r.body
        assert "/hello" in r.body

    def should_perform_async_requests_with_arguments_to_the_callback(self):
        barrier = Semaphore(0)

        def callback(response, extra1, extra2):
            body = response.body
            assert "Response for" in body
            assert "/hello" in body
            assert extra1 == "first"
            assert extra2 == "second"
            barrier.release()

        r = Restfulie.at("http://localhost:20144/hello")
        r = r.async(callback, args=("first", "second")).get()
        barrier.acquire()
        assert "Response for" in r.body
        assert "/hello" in r.body

    def should_perform_async_requests_without_callback(self):

        r = Restfulie.at("http://localhost:20144/hello").async().get()
        assert "Response for" in r.body
        assert "/hello" in r.body
