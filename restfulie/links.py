import dsl


class Link(object):
    """
    Link represents generic link. You can follow it.
    """

    def __init__(self, href, rel, content_type='application/xml'):
        self.href = href
        self.rel = rel
        self.content_type = content_type

    def follow(self):
        """
        Return a DSL object with the Content-Type
        set.
        """
        return dsl.Dsl(self.href).as_(self.content_type)


class Links:
    """
    Links a simple Link collection. There are some
    methods to put syntax sugar
    """

    def __init__(self, links):
        """
        Enable Links to access attributes with 'dot'
        """
        self.links = {}
        for link in links:
            self.links[link.rel] = link
            setattr(self, link.rel, link)

    def get(self, rel):
        """
        Checks if a Link exists. If exists returns the
        object, else returns None
        """
        return self.links.get(rel)

    def __len__(self):
        """
        The length of Links is the length of the links
        dictionary inside it
        """
        return len(self.links)
