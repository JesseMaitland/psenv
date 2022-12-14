#!/bin/bash

export REQ_FILE = requirements/development.txt
export PROJECT_DIR = psenv
export TEST_DIR = tests

.PHONY: help
help:          ## Show help messages and exit.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'


######################### MANAGE PYTHON ENVIRONMENT ####################################

.PHONY: init-dev
init-dev:         ## Create local python venv for development
	if [[ -d ./venv ]]; then rm -rf venv; fi
	python -m venv venv
	. venv/bin/activate \
	&& pip install --upgrade pip setuptools wheel \
	&& pip install -r ${REQ_FILE} --progress-bar off

.PHONY: install-dev
install-dev:
	pip install -e ".[dev]"

.PHONY: install
install:
	pip install -e .

######################### RUN TESTS AND LINTER ####################################

.PHONY: format
format:     ## Run black python linter
	black ${PROJECT_DIR} ${TEST_DIR}

.PHONY: check-format
check-format:
	black --check ${PROJECT_DIR} ${TEST_DIR}

.PHONY: test
test:     ## Run project tests using pytest
	pytest ${TEST_DIR} -p no:warnings -s
