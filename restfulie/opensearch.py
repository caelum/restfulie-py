import dsl


class OpenSearchDescription(object):
    """
    OpenSearchDescription object wraps the OpenSearch logic
    """

    def __init__(self, element_tree):
        self.url_type = 'application/rss+xml'
        self.element_tree = element_tree

    def use(self, url_type):
        """
        Set the OpenSearch type
        """
        self.url_type = url_type
        return self

    def search(self, searchTerms, startPage):
        """
        Make a search with 'searchTerms'
        It will find the url_type URL that you have chosen
        """
        tag = '{http://a9.com/-/spec/opensearch/1.1/}Url'
        urls = self.element_tree.findall(tag)
        for url in urls:
            if url.get('type') == self.url_type:
                template = url.get('template')
                template = template.replace('{searchTerms}', searchTerms)
                template = template.replace('{startPage?}', str(startPage))
                return dsl.Dsl(template).accepts(self.url_type).get()
