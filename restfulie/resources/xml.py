from restfulie.resources import Resource
from restfulie.links import Links, Link

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
            if root_child.tag != 'link':
                if len(self.element_tree.findall(root_child.tag)) > 1:
                    setattr(self, root_child.tag, self.element_tree.findall(root_child.tag))
                elif len(list(root_child)) == 0:
                    setattr(self, root_child.tag, root_child.text)
                else:
                    setattr(self, root_child.tag, self.element_tree.find(root_child.tag))

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
            link = Link(href=element.attrib.get('href'),
                        rel=element.attrib.get('rel'),
                        content_type=element.attrib.get('type') or 'application/xml')

            links.append(link)

        return links

    def links(self):
        return self._links

    def link(self, rel):
        return self.links().get(rel)
