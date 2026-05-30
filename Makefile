PYTHON ?= python3
VENV_DIR ?= .venv
VENV_PYTHON := $(VENV_DIR)/bin/python
ZENSICAL := $(VENV_DIR)/bin/zensical
OPENAPI_SPEC := docs/api/openapi.json

.PHONY: docs-bootstrap docs docs-serve docs-check docs-openapi-check

docs-bootstrap:
	$(PYTHON) -m venv $(VENV_DIR)
	$(VENV_PYTHON) -m pip install --upgrade pip zensical

docs-openapi-check:
	$(PYTHON) scripts/docs/check_openapi.py $(OPENAPI_SPEC)

docs: docs-bootstrap docs-openapi-check
	$(ZENSICAL) build --config-file zensical.toml --clean

docs-serve: docs-bootstrap docs-openapi-check
	$(ZENSICAL) serve --config-file zensical.toml

docs-check: docs-bootstrap docs-openapi-check
	$(ZENSICAL) build --config-file zensical.toml --clean
