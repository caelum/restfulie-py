class Converters:

    types = {}

    @staticmethod
    def register(a_type, converter):
        Converters.types[a_type] = converter

    @staticmethod
    def marshaller_for(a_type):
        if a_type in Converters.types:
            return Converters.types[a_type]
        else:
            return PlainConverter()


class XmlConverter:
    def marshal(self, content):
        """
        content eh um hash
        transforme em xml!
        e devolva transformado
        """
        pass

class PlainConverter:
    def marshal(self, content):
        return content

Converters.register("application/xml", XmlConverter())
Converters.register("text/xml", XmlConverter())
Converters.register("xml", XmlConverter())
Converters.register("text/plain", PlainConverter())

