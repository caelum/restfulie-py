from restfulie import Restfulie
import time

def search(what):
    description = Restfulie.at("http://localhost:3000/products/opensearch.xml").accepts('application/opensearchdescription+xml').get().resource()
    items = description.use("application/xml").search(searchTerms = what, startPage = 1)
    return items


def my_order():
    return {"order": {"address": "R. Vergueiro 3185, Sao Paulo, Brazil"}}


def pay(result):
    card = {'payment': {'card_holder': "guilherme silveira", 'card_number': 4444, 'value': result.order.price}}
    result = result.order.links().payment.follow().post(card).resource


def wait_payment_success(attempts, result):

    while result.order.state == "processing_payment":
        time.sleep(10)
        print("Checking order status at #{result.order.links.self.href}")
        result = result.order.refresh.resource()

    if result.order.state == "unpaid" and attempts > 0:
        print("Ugh! Payment rejected! Get some credits my boy... I am trying it again.")
        result = pay(result)
        wait_payment_success(attempts-1, result)
    else:
        return result


def should_be_able_to_search_items():
    items = search("20")
    assert len(items.resource().product) == 2


def should_be_able_to_create_an_empty_order():
    response = search("20")
    response = response.resource().links().order.follow().post(my_order())
    print response.body
    assert response.resource().address == my_order()['order']['address']


def should_be_able_to_add_an_item_to_an_order():
    results = search("20")

    product = results.resource().entries[0]
    selected = {'order': {'product': product.id, 'quantity': 1}}

    result = results.resource().links().order.follow().post(my_order).resource()
    result = result.order.links().self.follow().put(selected).resource()

    assert result.order.price == product.price


def should_be_able_to_pay():
    results = search("20")

    product = results.resource.entries[0]
    selected = {'order': {'product': product.id, 'quantity': 1}}

    result = results.resource().links().order.follow().post(my_order).resource()
    result = result.order.links().self.follow().put(selected).resource()

    result = pay(result)
    assert result.order.state == "processing_payment"


def should_try_and_pay_for_it():
    results = search("20")

    product = results.resource().entries[0]
    selected = {'order': {'product': product.id, 'quantity': 1}}

    result = results.resource().links().order.follow().post(my_order).resource()
    result = result.order.links().self.follow().put(selected).resource()

    result = pay(result)

    result = wait_payment_success(1, result)
    assert result.order.state == "preparing"
