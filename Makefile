PYTHON=python


all: pep8 test


test:
	cd examples && \
	for example in *.py; do \
		PYTHONPATH=.. $(PYTHON) $$example; \
	done
	cd examples/blur && PYTHONPATH=../.. $(PYTHON) app.py
	cd examples/environment_texture && PYTHONPATH=../.. $(PYTHON) main.py
	cd examples/game_of_life && PYTHONPATH=../.. $(PYTHON) app.py
	cd examples/ripples && PYTHONPATH=../.. $(PYTHON) main.py


pep8:
	flake8 gletools


install:
	$(PYTHON) ./setup.py install
