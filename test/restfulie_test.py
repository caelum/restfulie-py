from restfulie import Restfulie
from restfulie.dsl import Dsl


class restfulie_test:

    def should_return_a_dsl_object(self):
        assert type(Restfulie.at("www.caelum.com.br")) == Dsl
