from restfulie.converters import *

class converters_test:

    def setup(self):
        Converters.types = {}

    def test_register(self):
        converter = PlainConverter()
        Converters.register("text/plain", converter)

        assert Converters.types["text/plain"] == converter

    def test_marshaller_for(self):
        print Converters.marshaller_for("text/plain")

        assert Converters.marshaller_for("text/plain") == None
        converter = PlainConverter()
        Converters.register("text/plain", converter)
        assert Converters.marshaller_for("text/plain") == converter

class generic_marshaller_test:

    def test_marshal(self):
        converter = PlainConverter()
        result = converter.marshal("Hello World")
        assert result == "Hello World"

