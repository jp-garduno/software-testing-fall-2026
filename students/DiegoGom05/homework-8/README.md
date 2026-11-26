# Homework 8: End-to-End Test Automation

End-to-end tests for TodoMVC (React) written with **Selenium** (Python + pytest), **Playwright** (JavaScript) and **BDD** (Behave), all using the Page Object Model. A comparison of both frameworks is in [COMPARISON_REPORT.md](COMPARISON_REPORT.md).

## Application under test

`https://todomvc.com/examples/react/dist/`

> **Important:** the URL in the assignment (`/examples/react/`) no longer serves the app, and the tests time out waiting for `.new-todo`. The working URL is the one above (`/dist/`).
>
> To test another URL without editing code, set the `TODO_URL` environment variable (see each section below).

## Project structure

```
homework-8/
├── selenium/
│   ├── conftest.py              # driver and todo_page fixtures
│   ├── pages/todo_page.py       # Page Object
│   ├── tests/
│   │   ├── test_todo_crud.py    # create, complete, delete, edit (14 tests)
│   │   └── test_todo_filter.py  # all / active / completed (5 tests)
│   └── requirements.txt
├── playwright/
│   ├── playwright.config.js
│   ├── package.json
│   ├── pages/TodoPage.js        # Page Object
│   └── tests/
│       ├── todo-crud.spec.js    # 14 tests
│       └── todo-filter.spec.js  # 5 tests
├── features/
│   ├── todo.feature             # 3 scenarios + 1 outline (6 runs)
│   ├── environment.py           # Behave hooks (browser per scenario)
│   └── steps/todo_steps.py
├── screenshots/                 # execution evidence
├── COMPARISON_REPORT.md
└── README.md
```

## Requirements

- Python 3.10+ and Google Chrome (Selenium 4.6+ downloads the driver automatically)
- Node.js 18+ and npm
- Git Bash, PowerShell or any terminal

## How to run

### Selenium

```bash
cd selenium
python -m venv venv
source venv/Scripts/activate        # Windows (Git Bash). On macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
pytest -v
```

Useful options:

```bash
pytest -v --durations=5             # slowest tests and setup times
pytest tests/test_todo_filter.py    # a single file
```

Use another URL:

```bash
TODO_URL="https://example.com/" pytest -v           # Git Bash / macOS / Linux
$env:TODO_URL="https://example.com/"; pytest -v     # PowerShell
```

> The Selenium suite uses headless Chrome (configured in `conftest.py`). To watch the browser, remove the `--headless=new` argument.

### Playwright

```bash
cd playwright
npm install
npx playwright install chromium
npx playwright test
```

Useful options:

```bash
npx playwright test --headed        # watch the browser
npx playwright test --ui            # interactive UI mode
npx playwright show-report          # open the HTML report of the last run
```

### BDD (Behave)

Run from the project root. Behave reuses the Selenium Page Object, so the Selenium dependencies must be installed (activate the same virtual environment).

```bash
pip install behave                  # if it is not installed yet
behave features/
```

## Test coverage

| Area            | Scenarios                                                                         |
| --------------- | --------------------------------------------------------------------------------- |
| Task creation   | single task, multiple tasks, task appears in list, empty task is not created      |
| Task completion | complete, uncomplete, complete multiple                                           |
| Task deletion   | delete one, delete a completed task, clear completed                              |
| Task filtering  | all, active, completed, filter reflected in URL, completing a task in Active view |
| Task editing    | edit text, cancel edit (Escape), save edit, edit to empty deletes the task        |

Each test starts from a fresh browser or page, so tests are independent and can run in any order.

## Results

| Suite             | Tests       | Result               | Time               |
| ----------------- | ----------- | -------------------- | ------------------ |
| Selenium (pytest) | 19          | 18 passed, 1 xfailed | 88.32 s            |
| Playwright        | 19          | 19 passed            | 15.7 s (2 workers) |
| BDD (Behave)      | 6 scenarios | all passed           | ~4.4 s             |

### Known issue: `test_cancel_edit` in Selenium

After pressing Escape while editing a task, the item stays in the `editing` state in Selenium, both with `send_keys` and with `ActionChains`. The same scenario **passes in Playwright**. I did not determine the cause, so the Selenium test is marked `@pytest.mark.xfail` with the reason documented. See the comparison report for details.

## Bonus

_Fill in the two options you chose:_

- [ ] A. Visual regression
- [ ] B. Cross-browser testing
- [ ] C. Performance metrics
- [ ] D. CI/CD pipeline

## Screenshots

Execution evidence is stored in [`screenshots/`](screenshots/):

- Selenium run (`pytest -v`)
- Playwright run and HTML report
- Behave run

## Git workflow

Branch: `homework-8-solution` (conventional commits: `feat:`, `test:`, `docs:`, `chore:`).
