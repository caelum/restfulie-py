from xml.etree import ElementTree

from restfulie.converters import XmlConverter
from restfulie.resources.xml import XMLResource

def test_xml_parsing():

    test_xml = """
        <order>
          <product>rails training</product>
          <description>rest training</description>
          <price>512.45</price>
          <links>
            <link href="http://www.caelum.com.br/orders/1" rel="self"/>
            <link href="http://www.caelum.com.br/orders/1/payment" rel="payment"/>
          </links>
        </order>
    """

    e = ElementTree.fromstring(test_xml)
    order = XMLResource(e)
    links = order.links()

    assert len(order.order) == 4
    assert order.order.product == 'rails training'
    assert links.self.rel == "self"
    assert links.self.href == "http://www.caelum.com.br/orders/1"
    assert links.payment.rel == "payment"
    assert links.payment.href == "http://www.caelum.com.br/orders/1/payment"

def test_xml_without_links():

    test_xml = """
        <order>
          <product>rails training</product>
          <description>rest training</description>
          <price>512.45</price>
        </order>
    """

    e = ElementTree.fromstring(test_xml)
    order = XMLResource(e)
    links = order.links()

    assert len(links) == 0

def test_find_xml_resource_in_xml_resource():

    test_xml = """
      <xml>
        <order>
          <product>
            <name>rails training</name>
            <description>rest training</description>
            <price>512.45</price>
          </product>
        </order>
      </xml>
    """

    e = ElementTree.fromstring(test_xml)
    resource = XMLResource(e)

    assert resource.order.product.name == "rails training"
    assert resource.order.product.description == "rest training"
    assert resource.order.product.price == "512.45"
