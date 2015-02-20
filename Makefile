PYTHON=python


all: pep8 test


test:
	cd examples && \
	for example in *.py; do \
		PYTHONPATH=.. $(PYTHON) $$example; \
	done


pep8:
	flake8 gletools


install:
	$(PYTHON) ./setup.py install
