from restfulie.lxml_converter import LXMLConverter

class lxml_converter_test:

    def test_marshal(self):
        converter = LXMLConverter()
        d = {'html': {'img': ''}}
        result = converter.marshal(d)
        assert result == "<html><img></img></html>"

    def test_unmarshal(self):
        converter = LXMLConverter()
        result = converter.unmarshal('<html><img><link href="http://google.com" rel="alternative" type="application/xml">A Link</link><link href="http://yahoo.com" rel="self" type="application/xml" /></img></html>')
        assert result.html is not None
        assert result.html.tag == "img"
        assert result.html.link[0].tag == "link"
        assert result.html.link[0] == "A Link"
        assert result.html.link[1].tag == "link"
        assert result.html.link[1] == ""
        assert len(result.html.getchildren()) == 2