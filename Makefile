fmt:
	pylint * --ignore="Makefile,README.md,requirements.txt,LICENSE,TODO.md"
	flake8

unittest:
	python -m unittest discover greenturtle/tests

e2etest:
	python -m unittest discover e2e

test: unittest e2etest

# TODO(wsfdl), rafactor experiments to e2e test
crypto_experiment:
	cd experiments/crypto && python single.py
	cd experiments/crypto && python rsrs.py

stock_experiment:
	cd experiments/stock && python overview.py
	cd experiments/stock && python single.py
	cd experiments/stock && python stock_bond.py

future_experiment:
	cd experiments/future && python single.py
	cd experiments/future && python overview.py
	cd experiments/future && python multi_values.py

experiment: crypto_experiment stock_experiment future_experiment

all: fmt test
