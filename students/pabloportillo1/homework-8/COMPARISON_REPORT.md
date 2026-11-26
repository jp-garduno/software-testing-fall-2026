# Comparison Report: Selenium vs Playwright

Both suites run the same 32 tests against the TodoMVC React app, through page objects with matching method names:
Selenium 4.48 with Python and pytest, Playwright 1.62 with JavaScript. All numbers below were measured on one
MacBook (Apple Silicon, macOS), headless browsers, the same day. Wall-clock times include starting Python or Node,
and are the median of 3 runs.

## 1. Execution Time Comparison

The two suites are not configured the same way, and that matters more than the framework:

- The **Selenium** suite starts Chrome once and reuses it for every test (a session-scoped fixture), reloading the
  page between tests. That is fast, but the tests share one browser: its cache, its cookies, its history.
- **Playwright** gives every test a new browser context, an isolated profile with an empty cache, and runs tests
  in parallel workers by default.

So the table compares each suite as written, and also each one with the same isolation, one test at a time.

| Metric                                                  | Selenium (Chrome)                   | Playwright (Chromium)            |
| ------------------------------------------------------- | ----------------------------------- | -------------------------------- |
| Total execution time, as configured                     | 12.1 s (shared browser, sequential) | 6.0 s (5 parallel workers)       |
| Total, one test at a time, fresh browser state          | 42.1 s (new Chrome per test)        | 18.8 s (new context per test)    |
| Average per test, as configured                         | 0.38 s                              | 0.19 s                           |
| Average per test, fresh browser state                   | 1.32 s                              | 0.59 s                           |
| Setup time: start browser and open a page (median of 5) | 0.61 s (ChromeDriver + Chrome)      | 0.14 s (launch + context + page) |
| All three browser engines                               | -                                   | 23.0 s for 96 tests              |

What the numbers say:

- **With the same isolation, Playwright is about 2.2x faster one test at a time** (18.8 s vs 42.1 s). A new
  Playwright context costs a fraction of a new Chrome process started through ChromeDriver.
- **Reusing one Selenium browser is the cheapest setup of all** (0.38 s per test, against 0.59 s for Playwright
  with a fresh context), because a reload with a warm cache beats a cold first visit. The price is isolation: a
  test that left a cookie or a stored value behind would affect the next one. This app stores nothing, which is
  the only reason that trade-off is safe here.
- **Parallelism is where Playwright pulls away.** Running in parallel is one config line and costs nothing in
  test design, which is how it runs 96 tests on three engines in less time than Selenium needs for 32 tests in
  isolation. Selenium can run in parallel too (pytest-xdist, Selenium Grid), but every worker then needs its own
  driver.
- The behave suite (9 scenarios on the Selenium page object) takes 4.2 s.

## 2. Code Comparison

Non-blank lines, for equivalent functionality:

| Part                     | Selenium (Python)           | Lines   | Playwright (JavaScript)               | Lines   |
| ------------------------ | --------------------------- | ------- | ------------------------------------- | ------- |
| Page object              | `pages/todo_page.py`        | 108     | `pages/TodoPage.js`                   | 75      |
| Browser setup / fixtures | `browser.py`, `conftest.py` | 34      | `fixtures.js`, `playwright.config.js` | 27      |
| CRUD tests               | `test_todo_crud.py`         | 95      | `todo-crud.spec.js`                   | 138     |
| Filter tests             | `test_todo_filter.py`       | 36      | `todo-filter.spec.js`                 | 40      |
| **Total**                |                             | **273** |                                       | **280** |

The totals are almost equal, but the lines are in different places, and that says more than the totals:

- **The Selenium page object is 44% longer because it has to wait.** It has 11 explicit waits, one per action whose
  effect is not immediate, plus a helper for an element that disappears mid-wait. The Playwright page object has
  none: its methods are one or two lines each.
- **The Playwright tests are longer** because every call needs `await`, and because I wrote one web-first
  assertion per fact (`toHaveText`, `toHaveClass`, `toHaveCount`) instead of comparing a tuple, so each failure
  names exactly which fact broke.
- **Complexity lives in different places.** Selenium's complexity is synchronisation: three bugs during development
  were timing or interaction problems, not app problems (below). Playwright's is asynchronous JavaScript: forgetting
  one `await` produces a test that passes without checking anything. ESLint does not catch that with the course
  configuration.

The three Selenium problems, each fixed in the page object:

1. _Element click intercepted._ The "toggle all" label is covered by its own invisible checkbox, so Selenium
   refused to click the label; the fix is to click the checkbox.
2. _Stale element reference._ Toggling a task while the Active filter is on removes that task from the page,
   while the page object was still waiting for its class to change.
3. _`clear()` deleted a todo._ WebDriver's clear blurs the field afterwards, and this app saves on blur, so
   clearing the editor saved an empty title, which deletes the todo. The page object selects all and types over
   the text instead.

Playwright avoided all three without special handling: `click()` waits for the element to be actionable,
locators are re-resolved on every use, and `fill()` replaces the value without leaving the field.

## 3. Developer Experience

| Aspect                | Selenium | Playwright | Notes                                                                                                                                                                                                                                                                                                                                                 |
| --------------------- | -------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Setup difficulty      | Easy     | Easy       | `pip install selenium` was enough: Selenium Manager downloaded ChromeDriver for the installed Chrome. Playwright needs `npm install` plus `npx playwright install` to download its own browsers (77 MB for WebKit alone).                                                                                                                             |
| Auto-waiting          | Manual   | Built in   | 11 explicit waits in the Selenium page object, none in Playwright's. Web-first assertions retry until they pass or time out.                                                                                                                                                                                                                          |
| Debugging             | Basic    | Strong     | Playwright records a trace with DOM snapshots, network and console for every failure, and the HTML report links to it. For Selenium I wrote a pytest hook to save a screenshot on failure. `HEADED=1` and `--headed` show the browser in both.                                                                                                        |
| Documentation quality | Good     | Very good  | Both are complete. Playwright's API pages each carry a short example; Selenium's site shows several languages side by side, so finding the Python version of an example takes a little more searching.                                                                                                                                                |
| Error messages        | Mixed    | Clear      | Selenium's "click intercepted" message names the element that took the click, which solved bug 1 immediately; but "stale element reference" comes with about 20 lines of ChromeDriver native stack and no hint of which step caused it. Playwright prints a call log of what it was waiting for and why ("element is not visible", retried 58 times). |
| IDE support           | Good     | Very good  | Python tooling (pytest discovery, type hints) works for Selenium as for any library. Playwright adds a VS Code extension to run single tests, pick locators on the live page and record actions.                                                                                                                                                      |

## 4. Recommendations

**When would I choose Selenium?**

- When the team writes tests in a language Playwright does not support, such as Ruby, or already has a large
  Selenium suite and Grid infrastructure.
- When tests must drive real branded browsers through the standard WebDriver protocol, for example a certification
  on real Safari or on remote device farms built around WebDriver.
- When the BDD layer is in Python, as here: behave and the Selenium page object share one language.

**When would I choose Playwright?**

- For a new end-to-end suite on a modern web app: less synchronisation code, isolation per test for free, parallel
  runs by default, and the three browser engines from one config.
- When tests are flaky because of timing: auto-waiting and web-first assertions remove most of the cause.
- When failures need to be investigated in CI, where the trace viewer replaces "it works on my machine".

**What did I learn?**

- The page object pays off twice: when the app's markup changes, only the page object changes, and the BDD steps
  could reuse the Selenium page object without writing a single new selector.
- Most of the effort in Selenium went into synchronisation, not into testing. Every wait encodes knowledge of how
  the app reacts ("the input clears after a todo is added"), and getting one wrong produces flaky tests.
- Speed comparisons need the same isolation on both sides: as configured, the suites differ by 2x for reasons that
  have nothing to do with the frameworks.
- End-to-end tests against a public site find real defects. The Escape bug was there before any test was written;
  writing the tests to the TodoMVC specification, instead of to what the app happened to do, is what exposed it.
