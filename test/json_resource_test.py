import json

from restfulie.resources.json import JsonResource

def test_json_parsing():

    test_json = """
        { "order" : {
        "product" : "rails training",
        "description" : "rest training",
        "price" : "512.45",
        "link" : [
            { "rel" : "self", "href" : "http://www.caelum.com.br/orders/1"},
            { "rel" : "payment", "href" : "http://www.caelum.com.br/orders/1/payment"}
                ]
            }
        }
    """

    resource = JsonResource(json.loads(test_json))
    links = resource.links()

    assert len(links) == 2
    assert links.self.rel == "self"
    assert links.self.href == "http://www.caelum.com.br/orders/1"
    assert links.payment.rel == "payment"
    assert links.payment.href == "http://www.caelum.com.br/orders/1/payment"

def test_json_without_links():

    test_json = """
        { "order" : {
            "product" : "rails training",
            "description" : "rest training",
            "price" : "512.45"
            }
        }
    """

    resource = JsonResource(json.loads(test_json))
    links = resource.links()

    assert len(links) == 0

def test_find_dicts_in_dict():

    link = [{'rel': 'self', 'href': 'http://www.caelum.com.br/orders/1'}]
    d1 = {
            "product" : "rails training",
            "description" : "rest training",
            "price" : "512.45",
            "link" : link
         }
    d2 = {'order': d1}

    resource = JsonResource({})
    dicts = resource._find_dicts_in_dict(d2)

    assert len(dicts) == 2
    assert d1 in dicts
    assert d2 in dicts
    assert link not in dicts
