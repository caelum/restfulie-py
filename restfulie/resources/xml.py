from restfulie.resources import Resource
from restfulie.links import Links

class XMLResource(Resource):
    """
    This resource is returned when a XML is unmarshalled.
    """

    def __init__ (self, element_tree):
        self.element_tree = element_tree
        self._links = Links(self._parse_links())
        self._enhance_element_tree()

    def _enhance_element_tree(self):
        """
        Enables access to XMLResources attributes with 'dot'.
        """
        setattr(self, "tag", self.element_tree.tag)

        for root_child in list(self.element_tree):
            setattr(self, root_child.tag, root_child)

        for element in self.element_tree.getiterator():
            for child in list(element):
                if len(element.findall(child.tag)) > 1:
                    setattr(element, child.tag, element.findall(child.tag))
                elif len(list(child)) == 0:
                    setattr(element, child.tag, child.text)
                else:
                    setattr(element, child.tag, element.find(child.tag))

    def _parse_links(self):
        """
        Find links in a ElementTree
        """
        links = []
        for element in self.element_tree.getiterator('link'):
            d = {'href': element.attrib.get('href'),
                 'rel': element.attrib.get('rel'),
                 'type': element.attrib.get('type') or 'application/xml'}

            links.append(d)

        return links

    def links(self):
        return self._links

    def link(self, rel):
        return self.links().get(rel)
