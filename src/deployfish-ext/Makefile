RAWVERSION = $(filter-out __version__ = , $(shell grep __version__ deployfish_ext/__init__.py))
VERSION = $(strip $(shell echo $(RAWVERSION)))
PACKAGE = deployfish
VENV_ENV_PY27 := $(PACKAGE)-py27
VENV_DIR_PY27 := .venv/$(VENV_ENV_PY27)
LOG_DIR := .venv/install.log

clean:
	rm -rf *.tar.gz dist *.egg-info *.rpm
	find . -name "*.pyc" -exec rm '{}' ';'

version:
	@echo $(VERSION)

dist: clean
	@python setup.py sdist
	@python setup.py bdist_wheel --universal


mkvenv-py27:
ifeq "$(wildcard $(VENV_DIR_PY27))" ""
	@mkdir -p $(VENV_DIR_PY27)
	@virtualenv --python=python2.7 $(VENV_DIR_PY27) > $(LOG_DIR) 2>&1
	@( \
		. $(VENV_DIR_PY27)/bin/activate; \
		pip install -Ur ./requirements.txt >> $(LOG_DIR) 2>&1; \
		pip install -U pylint; \
		pip install -e ./ >> $(LOG_DIR) 2>&1; \
	)
endif
	@echo ". $(VENV_DIR_PY27)/bin/activate"
