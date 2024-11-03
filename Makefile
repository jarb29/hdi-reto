SHELL := /bin/bash

# Determine the OS and set the activation command accordingly
ifeq ($(OS),Windows_NT)
    ACTIVATE = .venv\Scripts\activate
else
    ACTIVATE = source .venv/bin/activate
endif

.PHONY: activate install lint

activate: ## Activate the virtual environment
	$(ACTIVATE)

install: activate    ## Install the dependencies
	uv pip install -r requirements/requirements.txt

install-dev: activate    ## Install the dev dependencies
	uv pip install -r requirements/requirements_dev.txt

install-pre-commit: install-dev ## Install pre-commit hooks
	pre-commit install

pre-commit: install-pre-commit ## Run pre-commit hooks
	pre-commit run --all-files

lint: ## Run Ruff to lint the code
	ruff .

docs:
	mkdocs serve

run-dev: activate## Run the development server
	uvicorn api.main:app --reload

run: ## Run the server
	uvicorn api.main:app

unit-tests: install-dev ## Run the unit tests
	pytest -v

stress-tests: install-dev ## Run the stresstests
	locust -f tests/stress/locustfile.py --host=http://127.0.0.1:8000

security-tests: install-dev ## Run the security tests
	bandit -c pyproject.toml -r .

build: ## Build the Docker image
	docker-compose up --build

deploy: build ## Deploy the app to the server
	docker-compose up -d

deploy-stop: ## Stop the app from the server
	docker-compose down
