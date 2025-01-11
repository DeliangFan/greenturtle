fmt:
	pylint * --ignore="Makefile,README.md,requirements.txt"
	flake8 --disable-noqa
