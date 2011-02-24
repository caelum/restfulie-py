from resources import Resource

class XMLResource(Resource):

    def __init__ (self, element_tree):
        self.element_tree = element_tree
        self.links = Links(_parse_links())
        _enhance_element_tree()     
        
    def _enhance_element_tree(self):
        for element in self.element_tree.getiterator():
            for child in list(element):
                if len(element.findall(child.tag)) > 1:
                    setattr(element, child.tag, element.findall(child.tag))
                elif len(list(child)) == 0:
                    setattr(element, child.tag, child.text)
                else:
                    setattr(element, child.tag, element.find(child.tag))

    def _parse_links(self):
        links = []
        for element in self.element_tree.getiterator('link'):
            d = {'href': element.attrib.get('href'),
                 'rel': element.attrib.get('rel'),
                 'type': element.attrib.get('type') or 'application/xml'}

            links.append(d)
            
        return links

    def links(self):
        return self.links
        
    def link(self, rel):
        return self.links().get(rel)
        
