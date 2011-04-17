import dsl


class Link(object):
    """
    Link represents generic link. You can follow it.
    """

    def __init__(self, link):
        self.href = link.get('href')
        self.rel = link.get('rel')
        self.type = link.get('type')

    def follow(self):
        """
        Return a DSL object with the Content-Type
        set.
        """
        return dsl.Dsl(self.href).as_(self.type)


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
            l = Link(link)
            self.links[l.rel] = l
            setattr(self, l.rel, l)

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
