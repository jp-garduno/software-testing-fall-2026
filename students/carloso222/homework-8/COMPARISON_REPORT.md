# Comparison Report: Selenium vs Playwright

Both suites test the same application (TodoMVC React, live site `https://todomvc.com/examples/react/dist/`)
with the same 28 test cases, the same Page Object Model design and headless browsers.

**Environment:** Windows 11 (build 26200), 16 logical CPUs · Python 3.11.9 + Selenium 4.54.0 + pytest 9.2 +
Behave 1.3.3 · Node 22.19.0 + Playwright 1.65.1 · Google Chrome 158.0.8127.37 · measured on 25 Nov 2026.
Raw data: [`reports/`](reports/) · generated summary: [`reports/timing-summary.md`](reports/timing-summary.md).

## 1. Execution Time Comparison

| Metric                        | Selenium                                              | Playwright                                                                                          |
| ----------------------------- | ----------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Total execution time          | **43.61 s** (45.49 s wall clock)                      | **20.12 s** with 8 parallel workers (23.27 s wall clock) · 31.98 s with 1 worker on the same Chrome |
| Average per test              | **1.52 s**                                            | **1.01 s** (1 worker, same Chrome) · 0.96 s (1 worker, bundled Chromium)                            |
| Setup time (browser start-up) | **1.74 s** (average of 5 `webdriver.Chrome()` starts) | **0.87 s** (average of 5 `launch()` + `newContext()` + `newPage()`)                                 |

Measuring fairly took four Playwright configurations, because Playwright's defaults differ from Selenium's
in two ways: it runs tests **in parallel**, and it uses its **own bundled Chromium** (a lightweight
_headless shell_) instead of the installed Chrome.

| Metric               | Selenium + Chrome (serial)         | Playwright + Chrome, 1 worker      | Playwright + bundled Chromium, 1 worker | Playwright + bundled Chromium, 8 workers |
| -------------------- | ---------------------------------- | ---------------------------------- | --------------------------------------- | ---------------------------------------- |
| Tests                | 28 (27 passed, 1 expected failure) | 28 (27 passed, 1 expected failure) | 28 (27 passed, 1 expected failure)      | 28 (27 passed, 1 expected failure)       |
| Total (runner)       | 43.61 s                            | 31.98 s                            | 29.59 s                                 | 20.12 s                                  |
| Wall clock           | 45.49 s                            | 35.05 s                            | 32.73 s                                 | 23.27 s                                  |
| Average per test     | 1.52 s                             | 1.01 s                             | 0.96 s                                  | 3.81 s\*                                 |
| Speed-up vs Selenium | 1.00×                              | **1.36×**                          | 1.47×                                   | **2.17×**                                |

\* With 8 workers, each test reports a longer duration because 8 browsers share the CPU. In parallel runs
the total time matters; per-test durations are not comparable to serial runs.

**Same browser, one test at a time, Playwright is 1.36× faster. With its defaults (parallel workers), it is
2.17× faster.** The BDD suite (Behave, reusing the Selenium page object) ran its 8 active scenarios in 8.98 s.

### Where the time goes (from bonus C, same Chrome for both tools)

Detailed numbers: [`bonus/performance/PERFORMANCE_REPORT.md`](bonus/performance/PERFORMANCE_REPORT.md).

| Operation (average of 5 runs)            | Selenium | Playwright | Ratio |
| ---------------------------------------- | -------- | ---------- | ----- |
| Add 1 todo                               | 230 ms   | 124 ms     | 1.9×  |
| Complete 1 todo                          | 258 ms   | 79 ms      | 3.3×  |
| Edit 1 todo                              | 632 ms   | 137 ms     | 4.6×  |
| Delete 1 todo                            | 574 ms   | 113 ms     | 5.1×  |
| Whole workflow (10 operations, 21 todos) | 5,221 ms | 2,104 ms   | 2.5×  |

The browser and the app are the same, so the gap is the tool's protocol:

- **Selenium sends one HTTP request to `chromedriver` for every command:** every `find_element`,
  `click`, `send_keys`, `get_attribute` and `is_displayed`, plus every check inside an explicit wait.
  "Add 1 todo" takes about 4 commands and costs 230 ms, so each command costs roughly 50 ms on this machine.
  "Edit" (double-click, select-all, type, Enter, two waits) and "Delete" (hover, reveal, click, wait) need
  the most commands, and they show the biggest gaps.
- **Playwright keeps one WebSocket connection open** and runs its actionability checks and assertion retries
  inside the browser.

Two results show how much this matters. The first version of Selenium's `toggle_all()` waited until
_every item's_ `class` attribute changed, which is one command per todo on every poll: **815 ms**. Waiting on
a single `find_elements(".todo-list li.completed")` dropped it to **188 ms**, measured on the same machine.
Also, `WebDriverWait` polls every **0.5 s** by default, so any condition that is not already true at the
first check costs at least half a second. The page object uses 0.1 s.

## 2. Code Comparison

Lines of code without blank lines, comments or docstrings (Python counted with `pygount`, JavaScript with a
comment-aware line counter), after formatting with Black and Prettier:

| Component          | Selenium (Python)                    | Playwright (JavaScript)                                        |
| ------------------ | ------------------------------------ | -------------------------------------------------------------- |
| Page Object        | 165 (`pages/todo_page.py`)           | 93 (`pages/TodoPage.js`)                                       |
| Setup and fixtures | 92 (`conftest.py` 38, `support/` 54) | 53 (`fixtures/todo-fixtures.js` 19, `playwright.config.js` 34) |
| CRUD tests         | 118                                  | 141                                                            |
| Filter tests       | 41                                   | 52                                                             |
| **Total**          | **416**                              | **339**                                                        |

| Complexity indicator                             | Selenium                                                             | Playwright                                                                  |
| ------------------------------------------------ | -------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| Public methods in the page object                | 28                                                                   | 18                                                                          |
| Explicit waits in the page object                | 15 (`WebDriverWait.until`)                                           | 2 (`waitFor`), the rest is auto-waiting                                     |
| Mouse helpers                                    | 3 `ActionChains` (hover, double-click)                               | built-in `hover()`, `dblclick()`                                            |
| Stale-element handling                           | needed (`toggle_todo` in a filtered view)                            | not needed (locators re-query the DOM)                                      |
| Query methods that exist only to feed assertions | 12 (`get_counter_text`, `completion_states`, `selected_filter`, ...) | 3, kept from the template and unused by the tests, which assert on locators |

The Playwright _page object_ is 44% smaller. Its _test files_ are a little longer because every check is an
`await expect(locator)...` web-first assertion, which Prettier often wraps over several lines. Those assertions
also wait and retry, which a plain Python `assert` cannot do. The same action shows the difference:

```python
# Selenium (pages/todo_page.py)
def delete_todo(self, index):
    item = self._item(index)
    count_before = self.get_todo_count()
    ActionChains(self.driver).move_to_element(item).perform()
    destroy = item.find_element(*self.ITEM_DESTROY)
    self.wait.until(EC.visibility_of(destroy))
    destroy.click()
    self.wait.until(lambda _d: self.get_todo_count() == count_before - 1)
```

```javascript
// Playwright (pages/TodoPage.js)
async deleteTodo(index) {
  const todo = this.item(index);
  await todo.hover();
  await todo.locator('.destroy').click();
}
```

## 3. Developer Experience

Scores from 1 (poor) to 5 (excellent), from implementing and debugging this homework:

| Aspect                | Selenium | Playwright | Notes                                                                                                                                                                                                                                                                                                                                               |
| --------------------- | -------- | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Setup difficulty      | 4        | 4          | Selenium: `pip install selenium`, and Selenium Manager downloaded `chromedriver` for the installed Chrome automatically. Playwright: `npm install` plus `npx playwright install`, one command but about 400 MB of browsers. Where that download is blocked, `PW_CHANNEL=chrome` uses the installed Chrome instead.                                  |
| Auto-waiting          | 2        | 5          | Every Selenium action needed an explicit wait, and a toggled item that leaves a filtered view raises `StaleElementReferenceException`. Playwright waited for actionability and retried assertions on its own. No suite has a single `sleep()`.                                                                                                      |
| Debugging             | 3        | 5          | The Playwright **trace viewer** diagnosed the Firefox timeouts (launch 14.5 s, page creation 17.1 s: an overloaded machine, not a bug). Its HTML report and failure screenshots come built in. Selenium's screenshots on failure needed a custom pytest hook.                                                                                       |
| Documentation quality | 4        | 5          | Both are well documented. Playwright's docs cover the runner, fixtures, assertions and config in one place. Selenium's cover the WebDriver API, but waits and test structure depend on pytest's docs.                                                                                                                                               |
| Error messages        | 3        | 5          | Selenium's best message was precise: `element click intercepted ... Other element would receive the click: <input class="toggle-all">` led straight to the toggle-all fix. But a failed `WebDriverWait` raises `TimeoutException` with an **empty message**. Playwright prints the locator, expected vs received value, the timeout and a call log. |
| IDE support           | 4        | 5          | Type hints and docstrings in the Python page object give good completion in VS Code. Playwright adds an official VS Code extension (run/debug a test, pick locators) and `codegen`.                                                                                                                                                                 |

### Pitfalls that cost the most time

1. **The assignment's URL returns 404.** The app is at `/examples/react/dist/`, and every suite reads `BASE_URL`.
2. **Selenium's `clear()` deleted todos.** WebDriver blurs the field after clearing it, and the app saves an
   edit on blur, so `clear()` saved an empty title, which deletes the todo. The fix is to select all and type over.
3. **The toggle-all checkbox is invisible** (`opacity: 0`) and lies on top of its label. Clicking the label is
   intercepted, and Selenium's visibility wait never succeeds. The fix is to click the checkbox, waiting for presence.
4. **Third-party scripts on the real site** (Google Analytics, `learn.json`) can delay the `load` event.
   Both tools now wait for `DOMContentLoaded` and then for the app's input (`page_load_strategy="eager"` / `waitUntil: 'domcontentloaded'`).
5. **Too much parallelism is flaky too.** With 8 workers × 3 browsers, 4 Firefox tests timed out; with 4 workers, all 84 passed
   (see [`bonus/cross-browser/CROSS_BROWSER_REPORT.md`](bonus/cross-browser/CROSS_BROWSER_REPORT.md)).

## 4. Recommendations

### When would you choose Selenium?

- The team writes tests in **Java, C#, Ruby or Python** and wants one tool for every language. Playwright supports fewer languages.
- An existing **Selenium Grid**, cloud provider or **Appium** mobile setup must be reused.
- Testing the **real branded browsers** that users run (Chrome, Edge, Firefox, Safari through `safaridriver`) through the
  **W3C WebDriver standard** matters more than speed.
- There is a large existing Selenium suite: rewriting working tests rarely pays off.

### When would you choose Playwright?

- New end-to-end suites for **modern single-page apps** (React, Vue, Angular), where auto-waiting removes most flakiness.
- **CI time matters:** parallel workers and isolated browser contexts out of the box. Here it was 2.17× faster with defaults.
- You need **cross-browser coverage including WebKit on Windows/Linux**, network mocking (`page.route`), traces,
  videos or screenshots without extra libraries.

**For this project I would choose Playwright:** less code, faster runs, and far better diagnostics. Selenium stays
the better choice when the constraint is language, existing infrastructure or real-browser fidelity.

### What did I learn?

- **E2E tests find real defects.** The suites found that Escape does not cancel editing, which the TodoMVC spec
  requires. The test documents it (`xfail(strict=True)` / `test.fail()` / `@known_defect`) instead of being
  deleted, and it will fail loudly once the app is fixed.
- **The tool and the app interact.** `clear()` triggering a blur, or an invisible checkbox covering its label,
  are not bugs of either one alone. Only a system-level test shows them.
- **Most flakiness came from the environment, not from the test logic:** third-party scripts, an overloaded
  machine, a wrong URL. Waiting for an app-specific "ready" signal and limiting parallelism worked better
  than raising timeouts.
- **A fair benchmark needs the same conditions.** Comparing Selenium + Chrome against Playwright's bundled
  headless shell in parallel would have exaggerated the difference (2.17× vs 1.36× on the same browser).
- **The testing pyramid is real.** 28 E2E tests take 20 to 45 s, while hundreds of unit tests run in under a
  second. E2E tests should cover the critical user journeys, and the edge cases belong at lower levels.
