from dsl import Dsl

class Link:
    def __init__(self, link):
        self.href = link.get('href')
        self.rel = link.get('rel')
        self.type = link.get('type')

    def follow(self):
        return Dsl(href)

class Links:

    self.links = {}

    def __init__(self, links):
        for link in links:
            l = Link(link)
            self.links[l.rel] = l

    def get(self, rel):
        return self.links.get(rel)

