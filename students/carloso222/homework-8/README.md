# Homework 8: End-to-End Test Automation — TodoMVC React

End-to-end tests for [TodoMVC React](https://todomvc.com/examples/react/dist/) written twice — with
**Selenium WebDriver (Python + pytest)** and with **Playwright (JavaScript)** — both using the
**Page Object Model**, plus **BDD scenarios** (Gherkin + Behave) and a **Selenium vs Playwright comparison**.

Bonus options implemented: **B. Cross-browser testing** and **C. Performance metrics**.

> **Note on the URL:** the URL in the assignment, `https://todomvc.com/examples/react/`, returns
> **404**. The React example lives at `https://todomvc.com/examples/react/dist/`, which is the default
> used by every suite (override it with the `BASE_URL` environment variable).

## Results at a glance

Measured on Windows 11 against the live site (25 Nov 2026), headless browsers:

| Suite                              | Tests                  | Result                                                                      | Time    |
| ---------------------------------- | ---------------------- | --------------------------------------------------------------------------- | ------- |
| Selenium + Chrome (pytest)         | 28                     | 27 passed, 1 expected failure (known defect)                                | 43.6 s  |
| Playwright, Chromium, 8 workers    | 28                     | 27 passed, 1 expected failure (known defect)                                | 20.1 s  |
| Playwright, Chrome, 1 worker       | 28                     | 27 passed, 1 expected failure (known defect)                                | 32.0 s  |
| Behave BDD                         | 9 scenarios            | 8 passed, 1 skipped (known defect, documented)                              | 9.0 s   |
| Playwright cross-browser (bonus B) | 28 × 3 browsers        | 84/84 as expected on Chromium, Firefox and WebKit                           | 128.8 s |
| Performance (bonus C)              | 10 operations × 5 runs | Playwright 2.5× faster for the whole workflow, 2.0× faster browser start-up |         |

Details: [`COMPARISON_REPORT.md`](COMPARISON_REPORT.md), [`reports/timing-summary.md`](reports/timing-summary.md),
[`bonus/cross-browser/CROSS_BROWSER_REPORT.md`](bonus/cross-browser/CROSS_BROWSER_REPORT.md) and
[`bonus/performance/PERFORMANCE_REPORT.md`](bonus/performance/PERFORMANCE_REPORT.md).

### Defect found: Escape does not cancel editing

The [TodoMVC specification](https://github.com/tastejs/todomvc/blob/master/app-spec.md#editing) says that
pressing **Escape** while editing must leave edit mode and discard the changes. In TodoMVC React,
Escape does nothing: the edit box stays open, and the typed text is saved as soon as the box loses focus.

The "Cancel edit" test documents it in every suite instead of being deleted or weakened:

- Selenium: `@pytest.mark.xfail(strict=True)`. It is reported as `xfailed`, and if the app is fixed
  it becomes `XPASS(strict)` and fails, so the test must then be updated.
- Playwright: `test.fail()`. Same idea, it passes only while the defect exists.
- Behave: scenario tagged `@known_defect`, skipped by default; run it with `behave -D run_known_defects=true`.

## Project structure

```
homework-8/
├── selenium/                      # Part 1 - Selenium + pytest + Page Object Model
│   ├── pages/todo_page.py         # Page Object (locators + actions with explicit waits)
│   ├── support/                   # settings (env vars) and WebDriver factory (chrome/firefox/edge)
│   ├── tests/test_todo_crud.py    # creation, completion, deletion, editing
│   ├── tests/test_todo_filter.py  # All / Active / Completed filters
│   ├── conftest.py                # driver + todo_page fixtures, screenshots on failure
│   └── requirements.txt
├── playwright/                    # Part 2 - Playwright Test + Page Object Model
│   ├── pages/TodoPage.js          # Page Object
│   ├── fixtures/todo-fixtures.js  # `todoPage` fixture (fresh page per test)
│   ├── tests/todo-crud.spec.js
│   ├── tests/todo-filter.spec.js
│   ├── perf/performance.spec.js   # bonus C
│   ├── playwright.config.js       # projects: chromium, firefox, webkit (bonus B), perf (bonus C)
│   └── package.json
├── features/                      # Part 3 - BDD (Behave), reuses the Selenium Page Object
│   ├── todo.feature
│   ├── environment.py
│   └── steps/todo_steps.py
├── bonus/
│   ├── cross-browser/CROSS_BROWSER_REPORT.md
│   └── performance/               # selenium_perf.py, generate_report.py, results/, PERFORMANCE_REPORT.md
├── scripts/
│   ├── setup_and_run.cmd          # Windows: install everything and run everything (double-click)
│   ├── run_cross_browser.cmd      # Windows: only the cross-browser run (bonus B)
│   ├── run_all.ps1 / run_all.sh   # run every suite and write the reports
│   └── summarize_timings.py       # builds reports/timing-summary.md
├── reports/                       # JUnit XML, Playwright JSON, console output, timing summary
├── screenshots/                   # sample: selenium/, bdd/, playwright/<browser>/ (SAVE_SCREENSHOTS=1 captures every test)
├── COMPARISON_REPORT.md           # Part 4
├── pytest.ini · behave.ini · requirements.txt
└── README.md
```

## Test scenarios

Every scenario of the assignment is implemented in both tools with the same names, plus edge cases:

| Area       | Assignment cases                                     | Extra cases                                                                                                                       |
| ---------- | ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Creation   | single task, multiple tasks, task appears in list    | text is trimmed; empty / blank text is ignored                                                                                    |
| Completion | mark complete, unmark, complete multiple             | toggle-all completes and reopens every task                                                                                       |
| Deletion   | delete single, delete completed, clear all completed | deleting one keeps the others                                                                                                     |
| Filtering  | all, active, completed                               | data-driven check of each filter + counter; completing in the Active view hides the task; clear completed from the Completed view |
| Editing    | edit text, cancel edit, save edited task             | edit keeps the completed state; edit without changes; clearing the text deletes the task                                          |

## How to run

Requirements: Python 3.11+, Node.js 18+ and Google Chrome (for Selenium).
All commands run from this folder (`students/carloso222/homework-8`).

### Everything at once (Windows)

Double-click `scripts\setup_and_run.cmd`, or run it from `cmd`. It installs the Python packages (in the
repository's `venv` when it exists), `@playwright/test` and the Playwright browsers, then runs every suite
with `scripts\run_all.ps1` and regenerates the reports. On Linux/macOS: `./scripts/run_all.sh`.

### Part 1 — Selenium

```bash
pip install -r requirements.txt
python -m pytest                      # headless Chrome
HEADLESS=0 python -m pytest           # watch the browser (PowerShell: $env:HEADLESS="0")
SELENIUM_BROWSER=firefox python -m pytest   # chrome (default), firefox or edge
```

Selenium Manager (bundled with Selenium 4.6+) downloads the matching driver automatically.

### Part 2 — Playwright

```bash
cd playwright
npm install
npx playwright install chromium firefox webkit
npm test                     # Chromium, parallel
npm run test:headed          # watch the browser
npm run test:cross-browser   # bonus B: Chromium + Firefox + WebKit (4 workers)
npm run test:perf            # bonus C
npm run report               # open the HTML report
```

### Part 3 — BDD

```bash
behave                                   # 8 scenarios + 1 known-defect scenario skipped
behave -D run_known_defects=true         # also run the known-defect scenario (fails on purpose)
```

### Bonus C — Performance

```bash
python bonus/performance/selenium_perf.py
(cd playwright && npm run test:perf)
python bonus/performance/generate_report.py
```

### Environment variables

| Variable                             | Default                                    | Used by          | Meaning                                                   |
| ------------------------------------ | ------------------------------------------ | ---------------- | --------------------------------------------------------- |
| `BASE_URL`                           | `https://todomvc.com/examples/react/dist/` | all              | app under test                                            |
| `HEADLESS`                           | `1`                                        | all              | `0` shows the browser                                     |
| `SAVE_SCREENSHOTS`                   | `0`                                        | all              | `1` saves the final state of every test in `screenshots/` |
| `SELENIUM_BROWSER`                   | `chrome`                                   | Selenium, Behave | `chrome`, `firefox` or `edge`                             |
| `SELENIUM_TIMEOUT` / `SELENIUM_POLL` | `10` / `0.1`                               | Selenium, Behave | explicit wait timeout and polling interval (s)            |
| `SELENIUM_PAGE_LOAD`                 | `eager`                                    | Selenium, Behave | page load strategy (`eager` = return at DOMContentLoaded) |
| `PW_WORKERS`                         | half the CPU cores                         | Playwright       | number of parallel workers                                |
| `PW_TIMEOUT`                         | `30000`                                    | Playwright       | test timeout in ms                                        |
| `PW_CHANNEL`                         | bundled Chromium                           | Playwright       | `chrome` or `msedge` to use an installed browser          |
| `PERF_RUNS`                          | `5`                                        | bonus C          | repetitions of each measurement                           |

## Design decisions

- **Page Object Model in both tools.** Page objects contain locators and user actions only; assertions
  live in the tests. The BDD steps reuse the Selenium page object, so there is one place to fix when the UI changes.
- **Independent tests.** TodoMVC React keeps its todos in memory, so a fresh page load is an empty list.
  Selenium reuses one browser per session and reloads the page before each test (through `about:blank`,
  because changing only the `#/route` fragment would not reload); Playwright gives each test a new browser
  context. Tests can run in any order, and Playwright runs them in parallel.
- **No `sleep()`.** Selenium uses explicit waits (`WebDriverWait`) for every action; Playwright uses
  auto-waiting and web-first assertions (`await expect(locator).toHaveText(...)`).
- **Stable selectors.** CSS classes from the TodoMVC spec (`.new-todo`, `.todo-list li`, `.toggle`,
  `.destroy`, `.clear-completed`, `a[href="#/active"]`) instead of XPath.

### Pitfalls found in the app (and how the page objects handle them)

| Pitfall                                                                                                                                                           | Handling                                                                                        |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| The delete button (`.destroy`) is `display: none` until the row is hovered                                                                                        | Selenium hovers with `ActionChains.move_to_element` first; Playwright calls `hover()`           |
| Editing starts with a double-click on the label                                                                                                                   | `ActionChains.double_click` / `dblclick()`                                                      |
| Selenium's `WebElement.clear()` blurs the field, and the app saves on blur, so clearing the edit box **deleted the todo**                                         | the text is selected with Ctrl+A (Cmd+A on macOS) and typed over                                |
| The edit box shares `data-testid="text-input"` with the new-todo box                                                                                              | located as `li.editing .edit`, not by test id                                                   |
| The toggle-all checkbox has `opacity: 0` and lies over its chevron label: clicking the label is intercepted, and Selenium reports the checkbox as "not displayed" | click the checkbox itself, waiting for presence instead of visibility                           |
| The footer counter reads `"1 item left!"` / `"2 items left!"`                                                                                                     | parsed by `get_active_count()`                                                                  |
| `WebDriverWait` polls every 0.5 s by default, so any wait that is not satisfied at once costs ≥ 0.5 s                                                             | `poll_frequency=0.1` (`SELENIUM_POLL`)                                                          |
| todomvc.com also loads Google Analytics and `learn.json`, which can delay the `load` event (a Firefox test hung for 30 s)                                         | wait for DOMContentLoaded, then for the app's input (`eager` / `waitUntil: 'domcontentloaded'`) |
| 8 parallel workers × 3 browsers overloaded the machine and 4 Firefox tests timed out                                                                              | the cross-browser run uses 4 workers                                                            |

## Continuous integration

The course's _Student Submission Validator_ runs `pytest` from this folder: `pytest.ini` points it to
`selenium/tests`, Chrome runs headless, and the folders named `selenium/` and `playwright/` have no
`__init__.py` on purpose, so they can never shadow the real `selenium`/`playwright` packages.
The Playwright suite has its own `package.json` inside `playwright/`, so it runs with `npm test` there.

## Author

Carlos Olmedo (`carloso222`) — Software Testing, Fall 2026.
