# Homework 8: End-to-End Test Automation

**Student:** Carlos Rubio (`larquitoskool`)  
**Application Under Test:** TodoMVC React (`https://demo.playwright.dev/todomvc/`)

## Overview

End-to-end test automation suite for TodoMVC React implemented using **Selenium (Python + pytest)** and **Playwright (JavaScript)** with the **Page Object Model (POM)** pattern, **BDD scenarios (Gherkin + Behave)**, a **Framework Comparison Report**, and two bonus extensions (**Cross-Browser Testing** and **Performance Metrics**).

> **Note on Application URL:** During initial test execution, `https://todomvc.com/examples/react/` returned 404 (moved to `/examples/react/dist/`), and the `/dist/` build exhibited an upstream bug (`tastejs/todomvc#2309`) where pressing `Escape` failed to cancel inline editing. Both suites target the official Playwright-maintained TodoMVC mirror (`https://demo.playwright.dev/todomvc/`), which preserves identical selectors and full TodoMVC behavior.

## Test Execution Summary

| Suite | Framework | Results | Execution Time |
| --- | --- | --- | --- |
| Selenium E2E (CRUD, Editing, Filtering) | Selenium 4 + pytest (Chrome headless) | 14 / 14 passed | 75.13s |
| Playwright E2E + Cross-Browser + Performance | Playwright (Chromium, Firefox, WebKit) | 36 / 36 passed | 1.4m (~84s) |
| BDD Acceptance Scenarios | Behave (Gherkin + Selenium POM) | 6 / 6 scenarios (25 steps) passed | 8.722s (steps) |

## Project Structure

- `selenium/` - Python Selenium POM (`pages/todo_page.py`), fixtures (`tests/conftest.py`), and pytest E2E suites (`tests/test_todo_crud.py`, `tests/test_todo_filter.py`).
- `playwright/` - JavaScript Playwright POM (`pages/TodoPage.js`), cross-browser config (`playwright.config.js`), and E2E + performance specs (`tests/`).
- `features/` - Gherkin feature file (`todo.feature`), Behave hooks (`environment.py`), and step definitions (`steps/todo_steps.py`).
- `COMPARISON_REPORT.md` - Detailed execution time, LOC, developer experience, troubleshooting log, and cross-browser compatibility matrix.
- `PERFORMANCE_REPORT.md` - Page load and CRUD timing benchmarks across Chromium, Firefox, and WebKit.
- `screenshots/` - Execution evidence (`selenium-results.png`, `behave-results-1.png`, `behave-results-2.png`, `playwright-results.png`).

## Prerequisites

- Python 3.11+
- Node.js 22+
- Browser drivers are managed automatically (Selenium Manager downloads Chrome for Testing; Playwright installs Chromium, Firefox, and WebKit).

## How to Run Tests

### 1. Selenium Tests (Python)

    cd selenium
    python -m pip install -r requirements.txt
    python -m pytest -v

### 2. Playwright Tests (JavaScript + Cross-Browser)

    cd playwright
    npm install
    npx playwright install
    npm run test:all-browsers

### 3. BDD Scenarios (Behave)

From the `homework-8/` directory:

    python -m behave