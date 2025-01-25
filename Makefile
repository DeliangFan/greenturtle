fmt:
	pylint * --ignore="Makefile,README.md,requirements.txt,LICENSE"
	flake8

test:
	python -m unittest

all: fmt test
