# Homework 8: End-to-End Test Automation - TodoMVC

## Description

The same 41 end-to-end scenarios for the TodoMVC React app, automated twice (Selenium + pytest in Python, and
Playwright in JavaScript), both with the Page Object Model, plus Gherkin scenarios run with behave on the Selenium
page object. The tests cover creating, completing, deleting, editing and filtering tasks.

Bonus work: **A, visual regression** (Playwright screenshot baselines) and **C, performance metrics**.

## Application under test

`https://todomvc.com/examples/react/dist/`

The assignment gives `https://todomvc.com/examples/react/`, but that URL now answers **404**; the app moved to
`/dist/`. Set `TODOMVC_URL` to test another copy (for example one served from localhost). Both suites read it.

## Prerequisites

- Python 3.9+ (the course asks for 3.11+; nothing here needs a version-specific feature) and Google Chrome
- Node.js 22+ (developed with Node 26)
- Selenium drives Chrome through Selenium Manager, which downloads a matching chromedriver (needs network access)

## Installation

```bash
# Selenium + behave (from this directory)
pip install -r selenium/requirements.txt

# Playwright
cd playwright
npm ci
npx playwright install chromium   # add firefox webkit for the other browsers
```

## Running the tests

```bash
# Selenium (from homework-8/; pytest.ini points at selenium/tests)
pytest -v

# Playwright (from homework-8/playwright/)
npm test                      # Chromium
npm run test:all-browsers     # Chromium, Firefox and WebKit
npm run report                # open the HTML report

# BDD scenarios (from homework-8/)
behave

# Visual regression (from homework-8/playwright/), Chromium on the machine that made the baselines
npm run visual
npm run visual:update         # accept new baselines after an intended UI change

# Performance measurements and the Selenium/Playwright benchmark
node playwright/perf/measure.js 10        # from homework-8/playwright
python tools/benchmark.py 5               # from homework-8/
```

Environment variables: `TODOMVC_URL` (app address), `HEADLESS=0` (Selenium shows the browser), `CI=1` (adds the
`--no-sandbox` flags Selenium needs on CI containers).

## Results

All numbers are from this machine against the live site; see `COMPARISON_REPORT.md` for the full comparison.

| Suite                 | Tests | Result                                                   |
| --------------------- | ----: | -------------------------------------------------------- |
| Selenium (pytest)     |    41 | 40 pass, 1 expected failure (see below)                  |
| Playwright (Chromium) |    41 | 40 pass, 1 expected failure (see below)                  |
| BDD (behave)          |    10 | 9 scenarios pass, 1 excluded (`@known-defect`)           |
| Visual regression     |     5 | 5 pass against the committed baselines                   |
| WebKit (Playwright)   |    41 | 41 pass (1 of them the expected failure), live and local |
| Firefox (Playwright)  |     - | **could not be run here**, see Limitations               |

## Project structure

```
homework-8/
├── selenium/
│   ├── pages/todo_page.py          Page Object (explicit waits, no sleeps)
│   ├── tests/test_todo_crud.py     create, complete, delete, edit
│   ├── tests/test_todo_filter.py   All / Active / Completed
│   ├── conftest.py                 shared Chrome, clean state per test, screenshot on failure
│   └── requirements.txt
├── playwright/
│   ├── pages/TodoPage.js           Page Object (locators, auto-waiting)
│   ├── tests/todo-crud.spec.js
│   ├── tests/todo-filter.spec.js
│   ├── visual/visual.spec.js       bonus A, with committed baselines in visual/baselines/
│   ├── perf/                       bonus C: measure.js, report.js and the raw results
│   ├── playwright.config.js
│   └── package.json
├── features/
│   ├── todo.feature                Gherkin scenarios
│   ├── steps/todo_steps.py         step definitions (use the Selenium page object)
│   └── environment.py              starts Chrome, one TodoPage per scenario
├── tools/                          count_loc.py, benchmark.py, render_terminal.js
├── benchmark/                      raw benchmark output
├── screenshots/                    test execution and report screenshots
├── COMPARISON_REPORT.md            Selenium vs Playwright (part 4)
├── PERFORMANCE_REPORT.md           bonus C
├── pytest.ini  behave.ini  .coveragerc
└── README.md
```

## Design notes

- **Independence.** Selenium shares one Chrome for speed and gives each test a clean page by clearing browser
  storage and reloading. Playwright gets a new browser context (empty storage) per test.
- **Synchronisation.** Selenium page-object actions wait for the DOM to reflect what they did (for example `add_todo`
  waits for the row to appear). A blank task adds no row, so those tests add a second real task afterwards and assert on
  the result instead of sleeping. Playwright relies on auto-waiting locators and web-first assertions.
- **The toggle-all chevron** is a `<label>` that the checkbox sits on top of; clicking the label is intercepted in both
  Selenium and Playwright. The page objects click the `.toggle-all` input, which is also what a user's click reaches.

## Known defect of the app and how it is handled

In this build of TodoMVC, **pressing Escape while editing a task does not cancel the edit**: the task stays in edit mode.
I confirmed it in the app's source (`app.bundle.js`): the edit field's only `keydown` handler returns unless the key
is Enter, and there is no Escape handling anywhere in the bundle. The TodoMVC specification says Escape should cancel.

The "cancel edit" scenario is therefore an **expected failure** in each suite: `xfail(strict=True)` in pytest,
`test.fail()` in Playwright, and `@known-defect` (excluded by `behave.ini`) in behave. Strict means that if the app is
ever fixed these turn red and have to be updated; they never hide a regression silently. Each was checked to fail for
the right reason (the task stays in edit mode).

## How the tests were checked

Passing against the live site only shows the tests agree with the app, not that they would notice a defect. So the
suites were also run against a local copy of the app with five one-line mutations of its code (the active filter shows
everything, the new-task field does not trim, the items-left counter is off by one, "clear completed" keeps the completed
tasks, delete keeps only the deleted task). Both suites failed on every mutation. The first pass found a weakness in my
own Playwright tests: `toHaveText` ignores surrounding whitespace, so the trim test could not detect the missing trim;
it now compares exact text.

## Limitations

- **Firefox could not be run in this environment**: the browser exits with "Could not find profile folder" even when
  launched by hand with a profile directory I created. So the cross-browser bonus (B) is not claimed, and the results
  table has no Firefox row. `npm run test:all-browsers` is configured for it.
- The tests depend on the live site and the network; Selenium also downloads chromedriver on first use.
- Visual baselines are platform-specific (`*-visual-darwin.png`), made with Chromium on macOS. Regenerate them with
  `npm run visual:update` on another OS.
- **Interaction with the course repository's Jest setup**: the repository's root `package.json` makes Jest pick up every
  `*.spec.js`, so `npm test` at the repository root also tries to run these Playwright specs under Jest, where they
  cannot run. The course CI marks that step `continue-on-error`. The file names follow the assignment, so I left them.
- The `*-test-execution.png` screenshots are console output rendered to images, not photos of a terminal; see
  `screenshots/README.md`.
- Timings depend on the network and on the machine; `COMPARISON_REPORT.md` explains why the live-site numbers
  differ from the local-copy ones.
