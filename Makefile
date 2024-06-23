
.PHONY: requirements
.PHONY: sync
.PHONY: dev
.PHONY: tests
.PHONY: build


# project specific variables

PYTHON-VERSION := 3.12
# OUTDIR := --outdir /path


# calculated variables

ifeq ($(OS),Windows_NT)
	PYTHON-SYS = py -$(PYTHON-VERSION)
	BIN-NAME = Scripts
	EXTENSION = .exe
else
	PYTHON-SYS = python$(PYTHON-VERSION)
	BIN-NAME = bin
endif

VENV-NAME:= .venv
BIN-DIR:= $(VENV-NAME)/$(BIN-NAME)

PIP-COMPILE:= $(BIN-DIR)/pip-compile$(EXTENSION)
PYTHON:= $(BIN-DIR)/python$(EXTENSION)


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



