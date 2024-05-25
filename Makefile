
.PHONY: requirements
.PHONY: sync
.PHONY: dev
.PHONY: tests
.PHONY: build


PYTHON = 3.12
VENV := .venv
# PYTHONENV := ${VENV}/Scripts/python.exe
PYTHONENV := ${VENV}/bin/python
# LIBRARIES_DIR := path/to/libraries/directory


all: requirements

#

requirements.txt: pyproject.toml ${VENV}
	${PYTHONENV} -m piptools compile -o requirements.txt pyproject.toml

sync: requirements
	${PYTHONENV} -m piptools sync requirements.txt


requirements-dev.txt: pyproject.toml ${VENV}
	${PYTHONENV} -m piptools compile --extra dev -o requirements-dev.txt pyproject.toml

dev: requirements
	${PYTHONENV} -m piptools sync requirements-dev.txt
	${PYTHONENV} -m pip install -r requirements-dev.txt -e .[dev]


requirements-tests.txt: pyproject.toml ${VENV}
	${PYTHONENV} -m piptools compile --extra tests -o requirements-tests.txt pyproject.toml

tests: requirements
	# ${PYTHONENV} -m piptools sync requirements-tests.txt
	${PYTHONENV} -m pip install -r requirements-tests.txt -e .[tests]


requirements: requirements.txt requirements-tests.txt requirements-dev.txt 


${VENV}:
	python${PYTHON} -m venv ${VENV}
	${PYTHONENV} -m pip install --upgrade pip pip-tools

#

build:
	${PYTHONENV} -m build #--outdir ${LIBRARIES_DIR}windows_whoami




