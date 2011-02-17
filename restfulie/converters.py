import json
from xml.etree import ElementTree
from opensearch import OpenSearchDescription
from links import Links


class Converters:

    types = {}

    @staticmethod
    def register(a_type, converter):
        Converters.types[a_type] = converter

    @staticmethod
    def marshaller_for(a_type):
        return Converters.types.get(a_type) or XmlConverter()


class JsonConverter:
    def marshal(self, content):
        return json.dumps(content)

    def unmarshal(self, json_content):
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


class XmlConverter:
    def marshal(self, content):
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
        'Returns an ElementTree Enhanced'
        e = ElementTree.fromstring(content)
        return self._enhance_element_tree(e)

    def _enhance_element_tree(self, e):
        for element in e.getiterator():
            for child in list(element):
                if len(element.findall(child.tag)) > 1:
                    setattr(element, child.tag, element.findall(child.tag))
                elif len(list(child)) == 0:
                    setattr(element, child.tag, child.text)
                else:
                    setattr(element, child.tag, element.find(child.tag))

        l = []
        for element in e.getiterator('link'):
            d = {'href': element.attrib.get('href'),
                 'rel': element.attrib.get('rel'),
                 'type': element.attrib.get('type') or 'application/xml'}

            l.append(d)

        e.links = lambda: Links(l)
        e.link = lambda x: e.links().get(x)

        return e


class OpenSearchConverter:
    def marshal(self, content):
        return XmlConverter().marshal(content)

    def unmarshal(self, content):
        e_tree = ElementTree.fromstring(content)
        return OpenSearchDescription(e_tree)


class PlainConverter:
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
