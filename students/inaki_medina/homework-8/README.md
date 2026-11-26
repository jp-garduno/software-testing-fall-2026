# Homework 8: Selenium and Playwright

The shared Behave features and pytest tests are in `features/` and `tests/`.
They exercise the same `TodoPage` interface against both browser backends.

## Install

From this directory, create and activate a virtual environment, then install
the shared dependencies and Playwright's Chromium browser:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
```

Chrome or Chrome for Testing must also be available for Selenium. Selenium
Manager locates or downloads the matching driver.

## Run all tests

From this directory:

```powershell
python run_tests.py
```

The runner executes the Selenium and Playwright groups concurrently. Each
group runs the shared pytest suite and Behave feature, then reports elapsed
time and page-object line coverage.
