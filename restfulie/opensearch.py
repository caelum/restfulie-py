import dsl


class OpenSearchDescription:

    def __init__(self, element_tree):
        self.url_type = 'application/rss+xml'
        self.element_tree = element_tree

    def use(self, url_type):
        self.url_type = url_type
        return self

    def search(self, searchTerms, startPage):
        tag = '{http://a9.com/-/spec/opensearch/1.1/}Url'
        urls = self.element_tree.findall(tag)
        for url in urls:
            if url.get('type') == self.url_type:
                template = url.get('template')
                template = template.replace('{searchTerms}', searchTerms)
                template = template.replace('{startPage?}', str(startPage))
                return dsl.Dsl(template).accepts(self.url_type).get()
