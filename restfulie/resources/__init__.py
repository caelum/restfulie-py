class Resource:

    def links(self):
        """
        Returns a list of all links.
        """
        raise NotImplementedError('Subclasses must implement this method')

    def link(self, rel):
        """
        Return a Link with rel.
        """
        raise NotImplementedError('Subclasses must implement this method')
