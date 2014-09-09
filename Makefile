all: test

test:
	nosetests --with-coverage --cover-package sacrud_deform --cover-erase --with-doctest --nocapture

coverage: test
	coverage html
