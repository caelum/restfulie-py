# RESTFULIE-PY

# SETUP

PYTHON="`pwd`/env/bin/python"
EASYINSTALL="`pwd`/env/bin/easy_install"
NOSETESTS="`pwd`/env/bin/nosetests"

# TARGETS

test:
	${PYTHON} test/httpserver.py > /dev/null 2> /dev/null &
	${NOSETESTS} test
	curl http://localhost:20144/stop > /dev/null 2> /dev/null

deps:
	${EASYINSTALL} httplib2
	${EASYINSTALL} nose
	${EASYINSTALL} mockito
	${EASYINSTALL} lxml

.PHONY: deps test