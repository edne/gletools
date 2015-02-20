PYTHON=python


all: pep8 coverage


test:
	cd examples && \
	for example in *.py; do \
		PYTHONPATH=.. $(PYTHON) $$example; \
	done
	cd examples/blur && PYTHONPATH=../.. $(PYTHON) app.py
	cd examples/game_of_life && PYTHONPATH=../.. $(PYTHON) app.py
	cd examples/ripples && PYTHONPATH=../.. $(PYTHON) main.py


coverage:
	export COVERAGE_FILE=`pwd`/.coverage
	coverage erase
	make test \
		PYTHON="\
		COVERAGE_FILE=../../.coverage\
		$(PYTHON) -m\
		coverage run --source=gletools -a"
	coverage report


pep8:
	flake8 gletools


install:
	$(PYTHON) ./setup.py install
