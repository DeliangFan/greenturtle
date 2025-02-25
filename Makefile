fmt:
	pylint * --ignore="Makefile,README.md,requirements.txt,LICENSE,TODO.md"
	flake8

unittest:
	python -m unittest discover greenturtle/tests

e2etest:
	python -m unittest discover e2e

test: unittest e2etest


experiment:
	cd experiments/future && python single.py
	cd experiments/future && python overview.py
	cd experiments/future && python multi_values.py

all: fmt test
