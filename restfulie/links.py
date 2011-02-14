import dsl


class Link:

    def __init__(self, link):
        self.href = link.get('href')
        self.rel = link.get('rel')
        self.type = link.get('type')

    def follow(self):
        return dsl.Dsl(self.href).as_(self.type)


class Links:

    def __init__(self, links):
        self.links = {}
        for link in links:
            l = Link(link)
            self.links[l.rel] = l
            setattr(self, l.rel, l)

    def get(self, rel):
        return self.links.get(rel)
