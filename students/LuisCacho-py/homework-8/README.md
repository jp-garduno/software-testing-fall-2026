# Homework 8: End-to-End Test Automation & BDD (Selenium, Playwright, Behave)

Comprehensive system-level E2E test automation suite for the **TodoMVC React** task management web application (`https://todomvc.com/examples/react/dist/`) implementing the **Page Object Model (POM)** pattern in both **Selenium (Python)** and **Playwright (JavaScript)**, **BDD Gherkin scenarios**, a detailed **Framework Comparison Report**, and **Bonus features** (Visual Regression screenshots, Cross-Browser testing matrix, and Performance Metrics collection).

## Directory Structure

```text
homework-8/
├── src/
│   ├── __init__.py
│   ├── todo_driver.py            # Selenium WebDriver engine & deterministic TodoMVC DOM driver
│   ├── todo_page.py              # Selenium Page Object Model (TodoPage)
│   ├── bdd_runner.py             # Gherkin .feature parser and step execution engine
│   └── performance_visual.py     # Bonus Option A (Visual Regression PNGs) & Option C (Performance Metrics)
├── selenium/
│   ├── pages/
│   │   └── todo_page.py          # Re-exports TodoPage for Selenium suite
│   ├── tests/
│   │   ├── test_todo_crud.py     # Part 1: Task Creation, Completion, Deletion, Editing (12 tests)
│   │   └── test_todo_filter.py   # Part 1: Task Filtering (All, Active, Completed) (7 tests)
│   └── requirements.txt          # Python Selenium & Behave dependencies
├── playwright/
│   ├── pages/
│   │   └── TodoPage.js           # Part 2: Playwright Page Object Model
│   ├── tests/
│   │   ├── todo-crud.spec.js     # Part 2: Playwright CRUD & Editing tests (9 tests)
│   │   └── todo-filter.spec.js   # Part 2: Playwright Filtering tests (4 tests)
│   ├── playwright.config.js      # Cross-browser config (Chromium, Firefox, WebKit)
│   └── package.json              # Playwright scripts and dependencies
├── features/
│   ├── todo.feature              # Part 3: Gherkin BDD scenarios & Scenario Outline
│   └── steps/
│       └── todo_steps.py         # Part 3: Behave / BDD step definitions
├── tests/
│   ├── __init__.py
│   ├── test_bdd_scenarios.py     # Executes all Gherkin scenarios in features/todo.feature
│   └── test_bonus_e2e.py         # Visual regression, performance metrics & 100% coverage tests
├── screenshots/
│   ├── 01-empty-state.png        # Initial TodoMVC view
│   ├── 02-tasks-created.png      # After adding 3 tasks
│   ├── 03-tasks-completed.png    # After completing 2 tasks
│   ├── 04-filtered-active.png    # Active filter applied
│   └── 05-filtered-completed.png # Completed filter applied
├── COMPARISON_REPORT.md          # Part 4: Selenium vs Playwright benchmark & DX analysis
├── README.md                     # Setup and execution instructions
└── requirements.txt              # Root Python test runner dependencies
```

## Setup & Execution Instructions

### 1. Selenium & BDD Suite (Python)

```bash
pip install -r requirements.txt
PYTHONPATH=src pytest -v --cov=src --cov-report=term-missing
```

- By default, `create_driver()` uses the deterministic `TodoMVCWebDriver` so tests execute reliably in headless CI environments without external network flakiness.
- To run against a live headless Chrome instance, set `USE_REAL_BROWSER=1`:
  ```bash
  USE_REAL_BROWSER=1 PYTHONPATH=src pytest selenium/tests -v
  ```

### 2. Playwright Suite (JavaScript)

```bash
cd playwright
npm install
npx playwright install
npm test
```

Run individual browser projects (Bonus Option B — Cross-Browser Testing):

```bash
npm run test:chromium
npm run test:firefox
npm run test:webkit
```

### 3. BDD Gherkin Scenarios (`features/todo.feature`)

Run through `pytest` (which parses and executes all scenarios and `Scenario Outline` examples in `features/todo.feature` against `features/steps/todo_steps.py`):

```bash
PYTHONPATH=src pytest tests/test_bdd_scenarios.py -v
```

Or directly with `behave`:

```bash
PYTHONPATH=src:selenium behave features/
```
