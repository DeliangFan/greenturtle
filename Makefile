fmt:
	pylint * --ignore="Makefile,README.md,requirements.txt,LICENSE,TODO.md"
	flake8

unittest:
	python -m unittest discover greenturtle/tests

e2etest:
	python -m unittest discover e2e

test: unittest e2etest


experiment:
	cd experiments && python single.py
	cd experiments && python overview.py
	cd experiments && python multi_values.py

all: fmt test
