# Homework 8: End-to-End Test Automation

**Student**: Rogelio Sosa (Rro0O)

System tests for the TodoMVC React application, written twice (Selenium + Python and Playwright + JavaScript)
with the Page Object Model, plus Gherkin scenarios run by Behave.

## Application under test

<https://todomvc.com/examples/react/dist/>

The URL given in the assignment (`https://todomvc.com/examples/react/`) answers **404**; the same application
is served from `dist/`. Set `TODO_URL` to test another deployment.

## Results

| Suite                          | Result                          |
| ------------------------------ | ------------------------------- |
| Selenium (Chrome)              | 19 passed, 1 expected failure   |
| BDD (Behave, 8 scenarios)      | 8 scenarios / 35 steps passed   |
| Playwright (Chromium)          | 20 passed (includes 1 expected) |
| Playwright (Firefox)           | 20 passed (includes 1 expected) |
| Playwright (WebKit)            | 20 passed (includes 1 expected) |
| Performance (3 browsers)       | 3 passed                        |

Full console output is in [`reports/`](reports/).

### Defect found

**Escape does not cancel an edit.** The [TodoMVC specification](https://github.com/tastejs/todomvc/blob/master/app-spec.md)
says that pressing Escape leaves edit mode and discards the changes. This version only handles Enter and blur, so the
field stays open and the new text is saved as soon as it loses focus.

The test `escape cancels edit` states the correct behaviour and is marked as an expected failure (`xfail(strict=True)`
in pytest, `test.fail` in Playwright), so both suites will turn red when the application is fixed. The part of
"cancel edit" that does work (leaving the field without changes) is tested separately.

## Setup

Requirements: Python 3.11+, Node.js 22+ and Google Chrome (Selenium Manager downloads a driver, and Chrome for
Testing if no Chrome is installed). All commands run from this folder.

```bash
python -m venv venv
source venv/bin/activate
pip install -r selenium/requirements.txt
```

```bash
cd playwright
npm install
npx playwright install
cd ..
```

## Running the tests

### Selenium and BDD

```bash
pytest -v                 # 20 Selenium tests + the BDD scenarios
behave features           # BDD scenarios alone, with readable output
pytest --cov=.            # with coverage
```

Set `HEADED=1` to watch the browser.

### Playwright

Run these inside `playwright/`.

```bash
npm test                       # Chromium
npm run test:cross-browser     # Chromium, Firefox and WebKit
npm run test:perf              # performance measurements
npm run report                 # HTML report of the last run
```

On macOS 27, Playwright's Firefox failed to start with `Could not find profile folder`. Pointing it to an empty
user folder fixed it:

```bash
CFFIXED_USER_HOME="$(mktemp -d)" npx playwright test --project=firefox
```

### Measurements and screenshots

```bash
python scripts/benchmark.py            # writes reports/benchmark.json
python scripts/capture_screenshots.py  # writes screenshots/
```

## Structure

```text
homework-8/
├── selenium/
│   ├── driver_factory.py          # WebDriver configuration
│   ├── pages/todo_page.py         # Page Object
│   └── tests/                     # conftest.py, test_todo_crud.py, test_todo_filter.py
├── playwright/
│   ├── pages/TodoPage.js          # Page Object
│   ├── tests/                     # fixtures.js, todo-crud.spec.js, todo-filter.spec.js
│   ├── perf/performance.spec.js   # bonus C
│   └── playwright.config.js       # chromium, firefox, webkit (bonus B)
├── features/                      # todo.feature, environment.py, steps/todo_steps.py
├── tests/test_bdd.py              # runs Behave inside pytest, so CI covers the scenarios
├── scripts/                       # benchmark and screenshot scripts
├── reports/                       # console output and measurement data
├── screenshots/
├── COMPARISON_REPORT.md
├── COMPATIBILITY_MATRIX.md        # bonus B
└── PERFORMANCE_REPORT.md          # bonus C
```

## Design decisions

- **Same 20 test cases in both tools**, with matching names, so the comparison is like for like.
- **Assertions stay in the tests.** Page objects only act and report state.
- **Selenium uses explicit waits only** (no implicit waits, no `sleep`): each action waits for its visible effect.
- **Playwright asserts on locators** (`toHaveText`, `toHaveCount`), which retry automatically.
- **Waiting for the final layout**: `navigate` waits for the sidebar, which arrives late and moves the list; without
  this, a click could be lost.
- **Isolation**: a new WebDriver per Selenium test and a new browser context per Playwright test. The application
  keeps no data between page loads, so there is nothing else to clean up.
- **Editing in Selenium** selects the text and types over it. `WebElement.clear()` blurs the field, which in this
  application saves the empty value and deletes the todo.

## Bonus

| Option                    | Where                                                    |
| ------------------------- | -------------------------------------------------------- |
| B. Cross-browser testing  | [COMPATIBILITY_MATRIX.md](COMPATIBILITY_MATRIX.md)       |
| C. Performance metrics    | [PERFORMANCE_REPORT.md](PERFORMANCE_REPORT.md)           |
