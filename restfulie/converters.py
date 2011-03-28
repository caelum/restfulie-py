import json
from xml.etree import ElementTree
from opensearch import OpenSearchDescription
from links import Links
from resources.xml import XMLResource


class Converters(object):
    """
    Utility methods for converters.
    """

    types = {}

    @staticmethod
    def register(a_type, converter):
        "Register a converter for the given type."
        Converters.types[a_type] = converter

    @staticmethod
    def marshaller_for(a_type):
        """
        Return a converter for the given type.
        """
        return Converters.types.get(a_type) or XmlConverter()


class JsonConverter(object):
    """
    Converts objects from and to JSON.
    """

    def marshal(self, content):
        """
        Produces a JSON representation of the given content.
        """
        return json.dumps(content)

    def unmarshal(self, json_content):
        """
        Produces an object for a given JSON content.
        """
        return _dict2obj(json.loads(json_content))


class _dict2obj(object):
    def __init__(self, dict_):
        for key, value in dict_.items():
            if isinstance(value, (list, tuple)):
                d = [_dict2obj(x) if isinstance(x, dict) else x for x in value]
                setattr(self, key, d)
            else:
                d = _dict2obj(value) if isinstance(value, dict) else value
                setattr(self, key, d)


class XmlConverter(object):
    """
    Converts objects from and to XML.
    """

    def marshal(self, content):
        """
        Produces a XML representation of the given content.
        """
        return ElementTree.tostring(self._dict_to_etree(content))

    def _dict_to_etree(self, content):
        tree = ElementTree.Element(content.keys()[0])
        self._dict_to_etree_rec(content[content.keys()[0]], tree)
        return tree

    def _dict_to_etree_rec(self, content, tree):
        if type(content) == dict:
            for key, value in content.items():
                e = ElementTree.Element(key)
                self._dict_to_etree_rec(value, e)
                tree.append(e)
        else:
            tree.text = str(content)

    def unmarshal(self, content):
        """
        Produces an ElementTree object for a given XML content.
        """
        e = ElementTree.fromstring(content)
        return XMLResource(e)


class OpenSearchConverter(object):
    def marshal(self, content):
        return XmlConverter().marshal(content)

    def unmarshal(self, content):
        e_tree = ElementTree.fromstring(content)
        return OpenSearchDescription(e_tree)


class PlainConverter(object):
    def marshal(self, content):
        return content

    def unmarshal(self, content):
        return content

Converters.register('application/xml', XmlConverter())
Converters.register('text/xml', XmlConverter())
Converters.register('xml', XmlConverter())
Converters.register('text/plain', PlainConverter())
Converters.register('text/json', JsonConverter())
Converters.register('application/json', JsonConverter())
Converters.register('json', JsonConverter())
Converters.register('application/opensearchdescription+xml',
                    OpenSearchConverter())
