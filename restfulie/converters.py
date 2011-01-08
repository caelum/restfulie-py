import json
from xml.etree import ElementTree

class Converters:

    types = {}

    @staticmethod
    def register(a_type, converter):
        Converters.types[a_type] = converter

    @staticmethod
    def marshaller_for(a_type):
        return Converters.types.get(a_type) or PlainConverter()


class JsonConverter:
    def marshal(self, content):
        return json.dumps(content)

    def unmarshal(self, json_content):
        return _dict2obj(json.loads(json_content))


class _dict2obj(object):
    #from: http://stackoverflow.com/questions/1305532/convert-python-dict-to-object
    def __init__(self, dict_):
        for key, value in dict_.items():
            if isinstance(value, (list, tuple)):
               setattr(self, key, [_dict2obj(x) if isinstance(x, dict) else x for x in value])
            else:
               setattr(self, key, _dict2obj(value) if isinstance(value, dict) else value)


class XmlConverter:
    def marshal(self, content):
        "Receives an ElementTree.Element"
        return ElementTree.tostring(content, encoding='utf-8')

    def unmarshal(self, content):
        "Returns an ElementTree Enhanced"
        e = ElementTree.fromstring(content)
        for element in e.getiterator():
            for child in element.getchildren():
                if len(element.findall(child.tag)) == 1:
                    setattr(element, child.tag, element.find(child.tag))
                else:
                    setattr(element, child.tag, element.findall(child.tag))
        return e


class PlainConverter:
    def marshal(self, content):
        return content

    def unmarshal(self, content):
        return content

Converters.register("application/xml", XmlConverter())
Converters.register("text/xml", XmlConverter())
Converters.register("xml", XmlConverter())
Converters.register("text/plain", PlainConverter())
Converters.register("text/json", JsonConverter())
Converters.register("application/json", JsonConverter())
Converters.register("json", JsonConverter())

