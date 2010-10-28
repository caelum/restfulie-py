from restfulie import Restfulie

resource = Restfulie.at("www.google.com").get()
print resource.code
print resource.body
