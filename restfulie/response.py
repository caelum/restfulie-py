from converters import Converters
import re

from links import Links


class Response:

    def __init__(self, response):

        self.response = response
        self.headers = self.response[0]
        self.code = self.response[0]['status']
        self.body = self.response[1]

    def resource(self):

        if 'content-type' in self.response[0]:
            contenttype = self.response[0]['content-type'].split(';')[0]
        else:
            contenttype = None

        converter = Converters.marshaller_for(contenttype)
        return converter.unmarshal(self.body)

    def links(self):
        r = self._link_header_to_array()
        return Links(r)

    def link(self, rel):
        return self.links().get(rel)

    def _link_header_to_array(self):
        values = self.headers['link'].split(',')
        links = []
        for link in values:
            links.append(self._string_to_hash(link))

        return links

    def _string_to_hash(self, l):
        uri = re.search('<([^>]*)', l) and re.search('<([^>]*)', l).group(1)
        rest = re.search('.*>(.*)', l) and re.search('.*>(.*)', l).group(1)
        rel = (re.search('rel=(.*)', rest) and
               re.search('rel="(.*)"', rest).group(1))
        tpe = (re.search('type=(.*)', rest) and
               re.search('type="(.*)"', rest).group(1))

        return {'href': uri, 'rel': rel, 'type': tpe}
