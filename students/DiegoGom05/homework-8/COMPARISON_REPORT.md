# Comparison Report: Selenium vs Playwright

**Application under test:** TodoMVC React (`https://todomvc.com/examples/react/dist/`)
**Suites:** 19 equivalent tests per framework (14 CRUD + 5 filters), plus 6 BDD scenarios (Behave + Selenium).
**Environment:** Windows 11, Python 3.10.8, pytest 9.1.1, Playwright (Chromium 151), headless Chrome for Selenium.

> **Note on the URL.** The URL in the assignment (`/examples/react/`) no longer serves the app: it returned a client error and Selenium timed out waiting for `.new-todo`. The working URL is `/examples/react/dist/`. Both Page Objects read it from `TODO_URL` and default to the `dist` URL.

## 1. Execution Time Comparison

| Metric               | Selenium                                              | Playwright                                       |
| -------------------- | ----------------------------------------------------- | ------------------------------------------------ |
| Tests                | 19 (18 passed, 1 xfailed)                             | 19 (19 passed)                                   |
| Total execution time | 88.32 s                                               | 15.7 s                                           |
| Average per test     | ~4.65 s                                               | ~0.83 s                                          |
| Workers              | 1 (sequential)                                        | 2 (parallel)                                     |
| Setup time           | _(fill in, see below)_                                | _(fill in, see below)_                           |
| First-time install   | `pip install` (fast, driver downloaded automatically) | `npm install` ~2 min + ~190 MB Chromium download |

**Reading these numbers fairly**

- The Selenium total includes ~10 s of waiting in the `xfail` test (`test_cancel_edit`), which times out on purpose. Without it: ~78 s, or ~4.3 s per test.
- Playwright ran with 2 workers, so its wall-clock time benefits from parallelism. Looking at individual tests, most took 0.6 to 0.8 s each (the first one took ~3.7 s because of browser start-up). Selenium can also run in parallel with `pytest-xdist`, which I did not try.
- Overall, Playwright finished about **5.6x faster** in this run. This is a single run; the numbers should be averaged over several runs for a stronger claim.
- **Setup time:** run `pytest --durations=5 -v` in `selenium/` and read the `setup` lines (browser launch per test). For Playwright, the first test in each worker shows the start-up cost.
- **BDD (Behave + Selenium):** 6 scenarios ran in about 4.4 s, ~0.55 s of which is page load per scenario.

## 2. Code Comparison

Lines of code measured with `wc -l`:

| File group   | Selenium (Python) | Playwright (JavaScript) |
| ------------ | ----------------- | ----------------------- |
| Page Object  | 90                | 71                      |
| CRUD tests   | 170               | 140                     |
| Filter tests | 70                | 57                      |
| **Total**    | **330**           | **268**                 |

Playwright needed about **19% fewer lines** (268 vs 330) for the same 19 tests. Where the difference comes from:

- **No explicit waits.** In Selenium I wrote `wait_for_count` and `wait_for_completed` helpers and called them throughout the tests. In Playwright, assertions such as `toHaveCount` and `toHaveText` retry automatically, so none were needed.
- **Locators as objects.** The Playwright Page Object exposes locators (`items`, `labels`) that tests use directly with `expect(...)`. In Selenium, each query re-finds elements with `find_elements`, and the Page Object wraps every access in a method.
- **Simpler editing.** Playwright's `fill()` replaces the text directly, while in Selenium I had to select all (`CTRL+A`) and type, with a different shortcut needed on Mac.
- **Complexity is similar in structure** (same Page Object pattern, same test names), but Selenium's tests carry extra synchronization code.

## 3. Developer Experience

| Aspect                | Selenium          | Playwright        | Notes                                                                                                                                                                                                                                                |
| --------------------- | ----------------- | ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Setup difficulty      | Easy              | Easy, but heavier | Selenium 4.6+ downloads the driver automatically. Playwright downloads its own browsers (~190 MB), and `npm install` took ~2 min.                                                                                                                    |
| Auto-waiting          | Manual            | Built in          | Selenium needed `WebDriverWait` and custom helpers. Playwright's locators and `expect` retry on their own.                                                                                                                                           |
| Debugging             | Manual            | Better tooling    | In Selenium I debugged by adding `print` statements and a forced `assert False` to inspect state. Playwright is configured with screenshots and traces on failure (`trace: "retain-on-failure"`), though I did not need them since all tests passed. |
| Documentation quality | Good, broad       | Good, focused     | _(add your own impression)_                                                                                                                                                                                                                          |
| Error messages        | Poor in this case | _(verify)_        | Selenium's timeout produced an empty `TimeoutException: Message:` with an unresolved native stack trace, which did not say what element or condition failed. I had no failing Playwright test, so I cannot compare its messages from experience.     |
| IDE support           | Good              | Good              | _(add your own impression)_                                                                                                                                                                                                                          |

### Differences found while testing

- **Cancel edit (Escape).** `test_cancel_edit` failed in Selenium: after pressing Escape (via `send_keys` and via `ActionChains`) the item stayed in `editing` state. The same scenario **passed in Playwright**. I did not determine the cause, so it is recorded as an observed difference. The Selenium test is marked `xfail` with the reason documented.
- **Hover-only buttons.** The delete button (`.destroy`) only appears on hover, so both frameworks needed an explicit hover before clicking.
- **Behave step matching.** A step defined without the trailing colon (`I have the following todos`) did not match the feature line `I have the following todos:`, leaving three scenarios `undefined`. Behave also treats `todo`, `todos` and `todo(s)` as different step texts.

## 4. Recommendations

**When would I choose Selenium?**

- The team already has a Selenium suite, a Grid, or infrastructure built around it.
- The test language is Java, C# or Ruby and the team does not want to adopt Node.
- The project must cover older or less common browsers, or integrate with existing tools and cloud providers built on the WebDriver standard.

**When would I choose Playwright?**

- New projects and modern JavaScript-heavy apps, where auto-waiting removes most flakiness.
- When speed and parallel execution matter: it was ~5.6x faster in this run, with less code.
- When debugging tools (traces, screenshots on failure, HTML report) and multi-browser support (Chromium, Firefox, WebKit) come built in.

**What did I learn?**

- Check the application first. The assignment URL was no longer valid, and the symptom (a timeout) looked like a bug in my own code.
- Explicit waits are where Selenium costs the most effort. Most of the extra code and the slower runs came from synchronization.
- The same scenario can behave differently across tools (Escape while editing), so one tool passing does not prove the app is correct and one failing does not prove the app is wrong.
- Tests need to be independent. Using a fresh browser per test made every test order-independent.
- Marking a known failure as `xfail` with a reason keeps the suite green while still documenting the problem.
