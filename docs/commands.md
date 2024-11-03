# Project Commands

This project uses a `Makefile` to simplify common development tasks. Commands are executed using `make <command_name>`. Activation commands for the virtual environment are OS-specific.

## Commands Overview

| Command                   | Description                                                      | Linux/macOS                              | Windows                                |
|---------------------------|------------------------------------------------------------------|------------------------------------------|----------------------------------------|
| **`make activate`**       | Activates the virtual environment.                               | `source .venv/bin/activate`              | `.venv\Scripts\activate`               |
| **`make install`**        | Installs project dependencies as listed in `requirements.txt`.   | `pip install -r requirements/requirements.txt`   | `pip install -r requirements/requirements.txt`  |
| **`make install-dev`**    | Installs development dependencies as listed in `requirements_dev.txt`. | `pip install -r requirements/requirements_dev.txt` | `pip install -r requirements/requirements_dev.txt` |
| **`make install-pre-commit`** | Installs pre-commit hooks. | `pre-commit install`                                | `pre-commit install`                               |
| **`make pre-commit`**     | Runs pre-commit hooks on all files.                      | `pre-commit run --all-files`                                | `pre-commit run --all-files`                               |
| **`make lint`**           | Runs Ruff linter to check the code quality.                      | `ruff .`                                | `ruff .`                               |
| **`make docs`**           | Starts the MkDocs development server to preview documentation locally. | `mkdocs serve`                          | `mkdocs serve`                         |
| **`make run-dev`**        | Runs the development server with automatic reloading.            | `uvicorn api.main:app --reload`         | `uvicorn api.main:app --reload`        |
| **`make run`**            | Runs the production server.                                      | `uvicorn api.main:app`                  | `uvicorn api.main:app`                 |
| **`make unit-tests`**     | Runs unit tests using pytest.                                    | `pytest -v`                             | `pytest -v`                            |
| **`make stress-tests`**   | Runs stress tests using Locust.                                  | `locust -f tests/stress/locustfile.py --host=http://127.0.0.1:8000` | `locust -f tests/stress/locustfile.py --host=http://127.0.0.1:8000` |
| **`make security-tests`** | Runs security tests using Bandit.                               | `bandit -c pyproject.toml -r .`          | `bandit -c pyproject.toml -r .`        |
| **`make build`**          | Builds the Docker image.                                        | `docker-compose up --build`              | `docker-compose up --build`            |
| **`make deploy`**         | Deploys the application using Docker Compose.                   | `docker-compose up -d`                   | `docker-compose up -d`                 |
| **`make deploy-stop`**    | Stops and removes the deployed application using Docker Compose. | `docker-compose down`                    | `docker-compose down`                  |

## Detailed Command Descriptions

### Activate Virtual Environment
**Command:** `make activate`<br>
**Description:** Activates the virtual environment.
- **Linux/macOS:** `source .venv/bin/activate`
- **Windows:** `.venv\Scripts\activate`

### Install Dependencies
**Command:** `make install`<br>
**Description:** Installs the project dependencies.
- **Linux/macOS & Windows:** `pip install -r requirements/requirements.txt`

### Install Development Dependencies
**Command:** `make install-dev`<br>
**Description:** Installs additional development dependencies.
- **Linux/macOS & Windows:** `pip install -r requirements/requirements_dev.txt`

### Install Pre-commit Hooks
**Command:** `make install-pre-commit`<br>
**Description:** Installs pre-commit hooks.
- **Linux/macOS & Windows:** `pre-commit install`

### Run Pre-commit Hooks
**Command:** `make pre-commit`<br>
**Description:** Runs pre-commit hooks on all files.
- **Linux/macOS & Windows:** `pre-commit run --all-files`

### Linting with Ruff
**Command:** `make lint`<br>
**Description:** Runs the Ruff linter to check code quality.
- **Linux/macOS & Windows:** `ruff .`

### Documentation Server
**Command:** `make docs`<br>
**Description:** Starts the MkDocs development server for local preview of documentation.
- **Linux/macOS & Windows:** `mkdocs serve`

### Development Server
**Command:** `make run-dev`<br>
**Description:** Runs the development server with automatic reloading enabled.
- **Linux/macOS & Windows:** `uvicorn api.main:app --reload`

### Production Server
**Command:** `make run`<br>
**Description:** Runs the production server.
- **Linux/macOS & Windows:** `uvicorn api.main:app`

### Unit Tests
**Command:** `make unit-tests`<br>
**Description:** Runs unit tests using pytest.
- **Linux/macOS & Windows:** `pytest -v`

### Stress Tests
**Command:** `make stress-tests`<br>
**Description:** Runs stress tests using Locust.
- **Linux/macOS & Windows:** `locust -f tests/stress/locustfile.py --host=http://127.0.0.1:8000`

### Security Tests
**Command:** `make security-tests`<br>
**Description:** Runs security tests using Bandit.
- **Linux/macOS & Windows:** `bandit -c pyproject.toml -r .`

### Build Docker Image
**Command:** `make build`<br>
**Description:** Builds the Docker image.
- **Linux/macOS & Windows:** `docker-compose up --build`

### Deploy Application
**Command:** `make deploy`<br>
**Description:** Deploys the application using Docker Compose.
- **Linux/macOS & Windows:** `docker-compose up -d`

### Stop Deployment
**Command:** `make deploy-stop`<br>
**Description:** Stops and removes the deployed application using Docker Compose.
- **Linux/macOS & Windows:** `docker-compose down`

---

### Additional Notes:
- Ensure the virtual environment is activated before running other commands.
- The `make` commands simplify and streamline repetitive tasks, aiding in efficient project management.

---

## Corresponding Makefile

```makefile
SHELL := /bin/bash

# Determine the OS and set the activation command accordingly
ifeq ($(OS),Windows_NT)
    ACTIVATE = .venv\Scripts\activate
else
    ACTIVATE = source .venv/bin/activate
endif

.PHONY: activate install lint install-dev install-pre-commit pre-commit docs run-dev run unit-tests stress-tests security-tests build deploy deploy-stop

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

docs: ## Serve documentation locally
	mkdocs serve

run-dev: activate ## Run the development server
	uvicorn api.main:app --reload

run: ## Run the production server
	uvicorn api.main:app

unit-tests: install-dev ## Run the unit tests
	pytest -v

stress-tests: install-dev ## Run the stress tests
	locust -f tests/stress/locustfile.py --host=http://127.0.0.1:8000

security-tests: install-dev ## Run the security tests
	bandit -c pyproject.toml -r .

build: ## Build the Docker image
	docker-compose up --build

deploy: build ## Deploy the app to the server
	docker-compose up -d

deploy-stop: ## Stop the app from the server
	docker-compose down
```
