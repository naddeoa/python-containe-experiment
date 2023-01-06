.PHONY: server
.PHONY: lint format format-fix test setup version_metadata help requirements default help

default:help

server: ## Run the dev server
	uvicorn src.ai.whylabs.container.main:app --reload

requirements: requirements.txt

requirements.txt: pyproject.toml
	poetry export -f requirements.txt > requirements.txt

lint: ## Check for type issues with mypy
	poetry run mypy src/

format: ## Check for formatting issues
	poetry run black --check --line-length 120 src

format-fix: ## Fix formatting issues
	poetry run black --line-length 120 src

setup:
	poetry install

test: ## Run unit tests
	pytest

help: ## Show this help message.
	@echo 'usage: make [target] ...'
	@echo
	@echo 'targets:'
	@egrep '^(.+)\:(.*) ##\ (.+)' ${MAKEFILE_LIST} | sed -s 's/:\(.*\)##/: ##/' | column -t -c 2 -s ':#'
