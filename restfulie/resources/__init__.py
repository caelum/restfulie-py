class Resource:

    def links(self):
        raise NotImplementedError('Subclasses must implement this method')
        
    def link(self, rel):
        raise NotImplementedError('Subclasses must implement this method')
