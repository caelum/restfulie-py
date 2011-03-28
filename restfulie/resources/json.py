from restfulie.resources import Resource
from restfulie.links import Links

class JsonResource(Resource):

    def __init__(self, dict_):
        links = self._parse_links(dict_)
        self._links = Links(links)

        for key, value in dict_.items():
            if isinstance(value, (list, tuple)):
                d = [JsonResource(x) if isinstance(x, dict) else x for x in value]
                setattr(self, key, d)
            else:
                d = JsonResource(value) if isinstance(value, dict) else value
                setattr(self, key, d)

    def _find_dicts_in_dict(self, structure):
        dicts = []
        if isinstance(structure, dict):
            dicts.append(structure)
            for k, v in structure.items():
                dicts.extend(self._find_dicts_in_dict(v))
        return dicts

    def _parse_links(self, dict_):
        for d in self._find_dicts_in_dict(dict_):
            if 'link' in d:
                return d['link']
        return []

    def links(self):
        return self._links

    def link(self, rel):
        return self.links().get(rel)

