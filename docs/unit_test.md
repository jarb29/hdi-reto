# Unit Tests

This document details the unit testing strategy and implementation for the HDI Claims Prediction API.

---

## Framework

We use the **`pytest`** framework for writing and running unit tests. `pytest` is known for its simplicity and powerful features.

---

## Test Suite Structure

Unit tests reside in the `tests/` directory. Each tested module or function typically has a corresponding test file (e.g., `test_<module_name>.py` or `test_<function_name>.py`).

---

## Running Unit Tests

Execute unit tests using:
```bash
make unit-tests
```
This uses the Makefile to run `pytest` with verbose output (`-v`).

### Installing Development Dependencies
Before running unit tests, install development dependencies:
```bash
make install-dev
```

---

## Test Coverage

We strive for high test coverage. Generate a coverage report using:
```bash
pytest --cov=./ --cov-report=html -v tests/
```
This creates an HTML report in the `htmlcov/` directory.

---

## Test Functions

The following functions are tested:

<details>
<summary><b>`full_pipeline`</b></summary>
<p>This test ensures that the `full_pipeline` function correctly preprocesses data and handles missing values. It checks for the presence of the `log_total_piezas` column and ensures no null values remain after imputation.</p>
</details>

<details>
<summary><b>`load_model`</b></summary>
<p>This test verifies that the `load_model` function successfully loads the trained machine learning model.</p>
</details>

<details>
<summary><b>`/api/v1/predict/` endpoint</b></summary>
<p>This test sends a POST request to the `/api/v1/predict/` endpoint and checks for a successful response (200 OK) and the presence of the `prediccion` field in the JSON response. It uses `fastapi.testclient.TestClient`.</p>
</details>

---

## Continuous Integration

Unit tests are integrated into our CI/CD pipeline for automatic testing on code changes.

---

### Summary of Enhancements:

- **Consistent Formatting**: Improved Markdown formatting for better readability.
- **Detailed Sectioning**: Clear sections with titles, subsections, and horizontal separators.
- **Command Blocks**: Used code blocks to highlight commands.
- **Expandable Sections**: Used `<details>` tags for expandable test function descriptions.
- **Organizational Enhancements**: Grouped related information together for a logical flow.

This improved version should be clearer and more user-friendly, making it easier to understand the unit testing strategy and execution.
