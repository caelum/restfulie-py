from converters import Converters
import re

from links import Links, Link


class Response(object):
    """
    Handle and parse a HTTP response
    """

    def __init__(self, response):
        self.response = response
        self.headers = self.response[0]
        self.code = self.response[0]['status']
        self.body = self.response[1]

    def resource(self):
        """
        Returns the unmarshalled object of the response body
        """
        if 'content-type' in self.response[0]:
            contenttype = self.response[0]['content-type'].split(';')[0]
        else:
            contenttype = None

        converter = Converters.marshaller_for(contenttype)
        return converter.unmarshal(self.body)

    def links(self):
        """
        Returns the Links of the header
        """
        r = self._link_header_to_array()
        return Links(r)

    def link(self, rel):
        """
        Get a link with 'rel' from header
        """
        return self.links().get(rel)

    def _link_header_to_array(self):
        """
        Split links in headers and return a list of dicts
        """
        values = self.headers['link'].split(',')
        links = []
        for link_string in values:
            links.append(self._string_to_link(link_string))

        return links

    def _string_to_link(self, l):
        """
        Parses a link header string to a dictionary
        """
        uri = re.search('<([^>]*)', l) and re.search('<([^>]*)', l).group(1)
        rest = re.search('.*>(.*)', l) and re.search('.*>(.*)', l).group(1)
        rel = (re.search('rel=(.*)', rest) and
               re.search('rel="(.*)"', rest).group(1))
        tpe = (re.search('type=(.*)', rest) and
               re.search('type="(.*)"', rest).group(1))

        return Link(href=uri, rel=rel, content_type=tpe)


class LazyResponse(object):
    """
    Lazy response for async calls
    """

    def __init__(self, response_pipe):
        self._response_pipe = response_pipe

    def __getattr__(self, attr):
        if self._response_pipe is not None:
            self._response = self._response_pipe.recv()
            self._response_pipe = None
        return getattr(self._response, attr)
