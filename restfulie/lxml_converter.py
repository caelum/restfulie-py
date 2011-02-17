from lxml import objectify
from converters import Converters


class LXMLConverter(object):

    def marshal(self, dictionary):
        '''from dictionary'''
        output = ""
        for key, value in dictionary.iteritems():
            output += "<%s>" % key
            if isinstance(value, dict):
                output += self.marshal(value)
            else:
                output += str(value)
            output += "</%s>" % key
        return output

    def unmarshal(self, xml_content):
        '''to object'''
        BlankSlate = type('object', (object,), {})
        result = BlankSlate()
        xml = objectify.fromstring(xml_content)
        child_tag = xml.iterchildren().next().tag
        setattr(result, xml.tag, getattr(xml, child_tag))
        return result

Converters.register("application/xml", LXMLConverter())
