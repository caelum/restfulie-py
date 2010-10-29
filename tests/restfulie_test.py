from restfulie import Restfulie

def test_restfulie_at():
    """
    Running Restfulie.at("www.caelum.com.br") should return
    a Request object with this URI
    """

    assert Restfulie.at("www.caelum.com.br")


