# Homework 8: End-to-End Test Automation — TodoMVC with Selenium and Playwright

**Student**: Pablo Portillo
**Module**: 8 — System Testing

## Description

End-to-end tests for the TodoMVC React app, written twice with the Page Object Model: once with Selenium
(Python + pytest) and once with Playwright (JavaScript), plus BDD scenarios with behave, following
[homework-8.md](../../../08-system-level-testing/homework/homework-8.md).

| Suite                                  | Tests           | Result                                                   | Run time |
| -------------------------------------- | --------------- | -------------------------------------------------------- | -------- |
| Selenium + pytest (Chrome)             | 32              | 31 passed, 1 expected failure                            | ~12 s    |
| Playwright (Chromium, Firefox, WebKit) | 32 x 3 browsers | 96 passed (1 expected failure per browser)               | ~23 s    |
| behave BDD (Selenium)                  | 9 scenarios     | 8 passed, 1 known-defect scenario skipped                | ~4 s     |
| Static analysis                        |                 | pylint 10.00/10, ESLint 0 errors (course configurations) |          |

Bonus: **B. Cross-browser testing** and **C. Performance metrics**.

### Application under test

The statement points to `https://todomvc.com/examples/react/`, which now answers **404**: the app is served from
`https://todomvc.com/examples/react/dist/`. Both suites use that URL by default; set `TODO_APP_URL` to test another
copy. The app keeps nothing in `localStorage`, so every page load starts with an empty list, which makes each test
independent without any cleanup.

### Known defect found

The TodoMVC specification says pressing **Escape** while editing discards the change. This React build ignores
Escape: the editor stays open with the new text, and clicking away then saves it
([screenshot](screenshots/05-escape-defect-editor-still-open.png)). Its key handler only reacts to Enter.

The test for it is written to the specification and marked as an expected failure in all three suites, so the
suite stays green while documenting the defect:

- pytest: `@pytest.mark.xfail(strict=True)`. _Strict_ means the run fails if the test ever passes, as a reminder to
  remove the marker once the app is fixed.
- Playwright: `test.fail()` with a "known defect" annotation shown in the HTML report.
- behave: the scenario is tagged `@known_defect` and skipped by default (`behave.ini`); run it with
  `behave --tags=@known_defect`.

## Prerequisites

- Python 3.11+ and Google Chrome (Selenium Manager downloads the matching ChromeDriver automatically)
- Node.js 22+

## Installation

```bash
# From this directory
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

cd playwright
npm install
npx playwright install chromium firefox webkit
```

## Running the Tests

```bash
# Selenium (from this directory); add HEADED=1 to watch the browser
python -m pytest -v

# BDD scenarios (from this directory)
behave

# Playwright, all three browsers (from playwright/)
npm test
npm run test:chromium        # Chromium only
npm run report               # open the HTML report of the last run

# Performance metrics, bonus C (from playwright/); rewrites PERFORMANCE_REPORT.md
npm run test:performance
```

Failures leave evidence behind: Selenium and behave save a screenshot to `artifacts/`, Playwright keeps a
screenshot and a trace in `playwright/test-results/`. Both folders are ignored by git.

The grading workflow only runs JavaScript when a `package.json` sits at the root of the submission, and it calls
`npm test -- --coverage`, a Jest option Playwright does not accept. With `package.json` inside `playwright/`, as
the statement's layout asks, the workflow grades the Selenium suite and leaves JavaScript out; the Playwright
results are in [screenshots/](screenshots/).

## Project Structure

```
homework-8/
├── selenium/
│   ├── pages/todo_page.py        # Page object with explicit waits
│   ├── tests/
│   │   ├── test_todo_crud.py     # Creation, completion, deletion, editing
│   │   └── test_todo_filter.py   # All / Active / Completed filters
│   ├── browser.py                # Headless Chrome setup, shared with behave
│   ├── conftest.py               # Driver and page fixtures, screenshot on failure
│   └── requirements.txt
├── playwright/
│   ├── pages/TodoPage.js         # Page object exposing locators for web-first assertions
│   ├── tests/
│   │   ├── todo-crud.spec.js
│   │   ├── todo-filter.spec.js
│   │   └── performance.spec.js   # Bonus C, tagged @performance
│   ├── reporters/performance-reporter.js  # Writes PERFORMANCE_REPORT.md
│   ├── fixtures.js               # todoPage fixture: a fresh page object per test
│   ├── playwright.config.js      # Chromium, Firefox and WebKit projects (bonus B)
│   └── package.json
├── features/
│   ├── todo.feature
│   ├── environment.py            # Reuses the Selenium page object and browser
│   └── steps/todo_steps.py
├── screenshots/                  # App states and test run evidence
├── COMPARISON_REPORT.md          # Part 4
├── PERFORMANCE_REPORT.md         # Bonus C, generated
├── behave.ini
├── pytest.ini
└── requirements.txt
```

## Test Scenarios

Both frameworks run the same 32 tests, with the same names:

| Area       | Tests                                                                                                                                                                                              |
| ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Creation   | single task, several tasks in order, items-left counter, spaces trimmed, blank text ignored, markup shown as text                                                                                  |
| Completion | mark complete, unmark, several tasks, singular counter, toggle all, toggle all twice                                                                                                               |
| Deletion   | delete one task, delete a completed task, clear completed, clear completed hidden when nothing is completed                                                                                        |
| Editing    | editor shows current text, save new text, spaces trimmed, empty text deletes the task, completed state kept, Escape cancels (known defect)                                                         |
| Filtering  | All / Active / Completed show the right tasks and highlight their link, completing a task under Active hides it, a new task is not listed under Completed, back to All, counter ignores the filter |

The BDD feature covers the statement's scenarios (add, complete, delete, the filter outline) plus editing, clearing
completed tasks and the Escape defect.

### Page Object Model

Tests never touch selectors: they call `TodoPage` methods with the same names in both languages (`add_todo` /
`addTodo`, `toggle_todo` / `toggleTodo`, `filter_by` / `filterBy`, ...). The two page objects differ where the
frameworks differ:

- **Selenium** methods wait for the effect of each action themselves (the input clearing after a new todo, the
  item's class changing after a toggle, the element disappearing after a delete), because Selenium does not wait
  on its own.
- **Playwright** methods only perform the action and expose locators; tests assert with `expect(...)`, which
  retries until the page matches or the timeout expires.

The behave steps reuse the Selenium page object, so the BDD layer adds readable scenarios without a third copy of
the selectors.

## Bonus Features

### B. Cross-browser testing

`playwright.config.js` defines a project per browser engine, and `npm test` runs every test on each of them.

| Area (tests)                                          | Chromium     | Firefox      | WebKit       |
| ----------------------------------------------------- | ------------ | ------------ | ------------ |
| Creation (6)                                          | pass         | pass         | pass         |
| Completion (6)                                        | pass         | pass         | pass         |
| Deletion (4)                                          | pass         | pass         | pass         |
| Editing (5)                                           | pass         | pass         | pass         |
| Escape cancels an edit (1)                            | known defect | known defect | known defect |
| Filtering (10)                                        | pass         | pass         | pass         |
| Browser start (launch, context and page, median of 5) | 143 ms       | 1349 ms      | 618 ms       |

No functional difference showed up: every test behaves the same in all three engines, including the Escape defect,
which is in the app's own code rather than in a browser. The differences are in speed: Firefox takes the longest
to start, and WebKit is the slowest at bulk operations (see [PERFORMANCE_REPORT.md](PERFORMANCE_REPORT.md)).
WebKit here is Playwright's build of the engine behind Safari, not Safari itself.

### C. Performance metrics

`tests/performance.spec.js` loads the app 5 times per browser, each in a new browser context so every load is a
first visit with an empty cache. It records Navigation Timing (DOMContentLoaded, load event) and the time to add 1
and 50 todos, toggle all, switch filter and clear completed. It fails if the median page load exceeds 5 s or adding
50 todos exceeds 15 s. A custom reporter writes the medians to [PERFORMANCE_REPORT.md](PERFORMANCE_REPORT.md). It
is tagged `@performance` and left out of `npm test`, because timing runs belong in a quiet, sequential run
(`--workers=1`).

## Screenshots

| File                                                                       | Shows                                                   |
| -------------------------------------------------------------------------- | ------------------------------------------------------- |
| `01-all-filter.png`, `02-active-filter.png`, `03-completed-filter.png`     | The filter test data under each filter                  |
| `04-editing-a-task.png`                                                    | A task in edit mode                                     |
| `05-escape-defect-editor-still-open.png`                                   | The known defect: the editor is still open after Escape |
| `06-playwright-html-report.png`                                            | Playwright HTML report: 96 of 96 passed                 |
| `07-selenium-pytest-run.png`, `08-playwright-run.png`, `09-behave-run.png` | Terminal output of each suite                           |

## Author

Pablo Portillo — Software Testing, Fall 2026
