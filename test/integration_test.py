from restfulie.restfulie import Restfulie
from multiprocessing import Queue


class integration_test:

    def should_perform_ordinary_requests(self):
        body = Restfulie.at("http://localhost:20144/hello").get().body
        assert "Response for" in body
        assert "/hello" in body

    def should_perform_ordinary_requests_with_simple_auth(self):
        r = Restfulie.at("http://test:test@localhost:20144/auth")
        response = r.get()
        body = response.body
        assert "worked" in body

    def should_perform_async_requests(self):
        q = Queue()

        def callback(response):
            q.put(True)
            body = response.body
            assert "Response for" in body
            assert "/hello" in body

        r = Restfulie.at("http://localhost:20144/hello").async(callback).get()
        assert q.get() == True
        assert "Response for" in r.body
        assert "/hello" in r.body

    def should_perform_async_requests_with_arguments_to_the_callback(self):
        q = Queue()

        def callback(response, extra1, extra2):
            q.put(True)
            body = response.body
            assert "Response for" in body
            assert "/hello" in body
            assert extra1 == "first"
            assert extra2 == "second"

        r = Restfulie.at("http://localhost:20144/hello")
        r = r.async(callback, args=("first", "second")).get()
        assert q.get() == True
        assert "Response for" in r.body
        assert "/hello" in r.body

    def should_perform_async_requests_without_callback(self):

        r = Restfulie.at("http://localhost:20144/hello").async().get()
        assert "Response for" in r.body
        assert "/hello" in r.body
