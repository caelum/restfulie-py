from restfulie.converters import *
from xml.etree.ElementTree import Element

class converters_test:

    def setup(self):
        Converters.types = {}

    def test_register(self):
        converter = PlainConverter()
        Converters.register("text/plain", converter)

        assert Converters.types["text/plain"] == converter

    def test_marshaller_for(self):
        assert Converters.marshaller_for("application/xml").__class__ == PlainConverter().__class__
        converter = PlainConverter()
        Converters.register("text/plain", converter)
        assert Converters.marshaller_for("text/plain") == converter

class generic_marshaller_test:

    def test_marshal(self):
        converter = PlainConverter()
        result = converter.marshal("Hello World")
        assert result == "Hello World"

    def test_unmarshal(self):
        converter = PlainConverter()
        result = converter.unmarshal("Hello World")
        assert result == "Hello World"

class json_marshaller_test:

    def test_marshal(self):
        converter = JsonConverter()
        d = {'a': {'c':[1,2,3]}, 'b': 2}
        result = converter.marshal(d)
        assert result == '{"a": {"c": [1, 2, 3]}, "b": 2}'

    def test_unmarshal(self):
        converter = JsonConverter()
        json = '{"a": {"c": [1, 2, 3]}, "b": 2}'
        result = converter.unmarshal(json)
        assert result.a.c == [1,2,3]
        assert result.b == 2

class xml_marshaller_test:

    def test_marshal(self):
        converter = XmlConverter()
        etree = Element('html')
        etree.append(Element('img'))
        result = converter.marshal(etree)
        assert result == '<html><img /></html>'

    def test_unmarshal(self):
        converter = XmlConverter()
        result = converter.unmarshal('<html><img /></html>')
        assert result.tag == 'html'
        assert result.getchildren()[0].tag == 'img'
