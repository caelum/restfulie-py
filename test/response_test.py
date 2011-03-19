from restfulie.response import Response


def trivial_test():

    response = ({'status': 200}, 'Hello')

    r = Response(response)
    assert r.body == 'Hello'
    assert r.code == 200


def resource_test():

    response = ({'status': 200, 'content-type': \
                 'text/plain; charset=utf-8'}, 'Hello')

    r = Response(response)
    assert r.resource() == 'Hello'


def link_test():

    response = ({'status': 200, 'link': '</feed>; rel="alternate"'}, 'Hello')
    r = Response(response)
    link = r.link('alternate')
    assert link.href == '/feed'
    assert link.rel == 'alternate'
