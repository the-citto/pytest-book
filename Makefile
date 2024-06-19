
.PHONY: requirements
.PHONY: sync
.PHONY: dev
.PHONY: tests
.PHONY: build

#

PYTHON-SYS:= python3.12

VENV:= .venv
# OUTDIR:= --outdir /path

BIN-DIR:= $(VENV)/bin
PIP-COMPILE:= $(BIN-DIR)/pip-compile
PYTHON:= $(BIN-DIR)/python


#

all: requirements

#

requirements.txt: pyproject.toml $(PIP-COMPILE)
	$(PYTHON) -m piptools compile -o requirements.txt pyproject.toml

sync: requirements
	$(PYTHON) -m piptools sync requirements.txt


requirements-dev.txt: pyproject.toml $(PIP-COMPILE)
	$(PYTHON) -m piptools compile --extra dev -o requirements-dev.txt pyproject.toml

dev: requirements
	$(PYTHON) -m piptools sync requirements-dev.txt
	$(PYTHON) -m pip install -e .[dev]


requirements-tests.txt: pyproject.toml $(PIP-COMPILE)
	$(PYTHON) -m piptools compile --extra tests -o requirements-tests.txt pyproject.toml

tests: requirements
	$(PYTHON) -m piptools sync requirements-tests.txt
	$(PYTHON) -m pip install -e .[tests]


requirements: requirements.txt requirements-tests.txt requirements-dev.txt 


$(PIP-COMPILE):
	$(PYTHON-SYS) -m venv $(VENV)
	$(PYTHON) -m pip install --upgrade pip pip-tools

#

build: sync
	$(PYTHON) -m build $(OUTDIR)
	@echo
	@echo run make dev to continue development
	@echo




