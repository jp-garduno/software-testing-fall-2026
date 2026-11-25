# Selenium vs Playwright: Comparison Report

Both suites implement the same 20 test cases against <https://todomvc.com/examples/react/dist/> with the Page Object
Model.

**Environment**: Apple M2 (8 cores), macOS 27.0, Python 3.11.18, Selenium 4.54.0, pytest 9.2.0, Node.js 24.19.0,
Playwright 1.64.0. Selenium drove Chrome 158.0.8127.88; Playwright drove its bundled Chromium 156.0.8078.4.

## 1. Execution time comparison

Measured with `scripts/benchmark.py`: wall-clock time of the whole command, headless Chromium, one test at a time,
5 repetitions, alternating tools. The full benchmark was run twice on the same day and both runs are shown, because
they differ a lot.

| Metric (median)                      | Selenium           | Playwright           |
| ------------------------------------ | ------------------ | -------------------- |
| Total execution time, run 1          | 35.4 s (31.0–42.7) | 22.5 s (17.8–26.2)   |
| Total execution time, run 2          | 45.3 s (43.8–76.7) | 40.1 s (31.0–71.9)   |
| Average per test, run 1              | 1.77 s             | 1.13 s               |
| Average per test, run 2              | 2.26 s             | 2.00 s               |
| Total with parallel workers, run 1   | not configured     | 8.4 s                |
| Total with parallel workers, run 2   | not configured     | 14.2 s               |
| Setup time: start a browser          | 0.44 s             | 0.11 s               |
| Setup time: per test, as configured  | 0.44 s (new driver) | 0.04 s (new context) |
| Setup time: load the application     | 2.27 s             | 1.26 s               |

Setup times are medians of 10 repetitions (`scripts/measure_setup.py` and `playwright/scripts/measure-setup.js`).
Raw data: [`reports/benchmark.json`](reports/benchmark.json) and
[`reports/benchmark-run1.json`](reports/benchmark-run1.json).

### How to read these numbers

- **Playwright was faster in both runs, but the margin is not stable**: 36 % less total time in run 1 and 11 % less in
  run 2.
- **The network dominates.** The application is a public website and every test loads it from scratch, including a
  third-party analytics script. In run 2 the slowest repetition took 1.7 times (Selenium) and 2.3 times
  (Playwright) as long as the fastest.
- **Where Playwright clearly wins is startup**: it reuses one browser process and creates a context per test
  (0.04 s), while this Selenium setup starts a whole browser per test (0.44 s). Reusing one driver would narrow the
  gap, at the price of weaker isolation.
- **Parallelism came for free in Playwright** (`fullyParallel: true`). Selenium needs `pytest-xdist` or Selenium
  Grid, which this project does not configure.
- **The application load figures are not a tool benchmark**: the two tools used different browser builds and the
  value depends on the network.

## 2. Code comparison

Lines that are neither blank nor comments, counted by `scripts/benchmark.py`:

| Area                    | Selenium (Python) | Playwright (JavaScript) |
| ----------------------- | ----------------- | ----------------------- |
| Page object             | 108               | 87                      |
| Tests (20 cases)        | 110               | 138                     |
| Setup and configuration | 27                | 29                      |
| **Total**               | **245**           | **254**                 |

The totals are almost the same, but the lines are spent differently:

- The Playwright tests are longer because of the language (`async`/`await`, closing braces, `describe` blocks) and
  because each assertion is its own `await expect(...)`.
- The Selenium page object is longer because it has to say **when** each action is finished. It contains explicit
  waits in almost every method; the Playwright one has a single `waitFor`, in `navigate`.

The same action in both:

```python
def delete_todo(self, index):
    item = self._item(index)
    ActionChains(self.driver).move_to_element(item).perform()
    button = item.find_element(*self.ITEM_DESTROY)
    self.wait.until(EC.visibility_of(button))
    button.click()
    self.wait.until(EC.staleness_of(item))
```

```javascript
async deleteTodo(index) {
  const item = this.todoItems.nth(index);
  await item.hover();
  await item.locator(".destroy").click();
}
```

**Complexity**: Selenium requires deciding on a wait condition for every state change and thinking about stale element
references. Playwright locators are re-resolved on every use, so neither problem appeared.

## 3. Developer experience

| Aspect                | Selenium    | Playwright  | Notes                                                       |
| --------------------- | ----------- | ----------- | ----------------------------------------------------------- |
| Setup difficulty      | Low         | Low         | Selenium Manager fetches browser and driver on first run; Playwright needs `npx playwright install` and about 1.2 GB for three browsers |
| Auto-waiting          | None        | Built in    | The biggest practical difference                            |
| Debugging             | Basic       | Very good   | Playwright saves a trace and a screenshot on failure; with Selenium both must be added by hand |
| Documentation quality | Good        | Very good   | Selenium's covers many languages and versions, so examples are less uniform |
| Error messages        | Verbose     | Clear       | See below                                                   |
| IDE support           | Good        | Very good   | Playwright has an official VS Code extension and code generator; not evaluated in depth here |

The ratings are a judgement based on building these two suites, not a measurement.

### Problems actually found

- **Selenium, "toggle all".** Clicking the visible label raised `ElementClickInterceptedException`, because an
  invisible checkbox sits on top of it. The message named the covering element, which made the fix obvious, but it was
  followed by a long chromedriver stack trace.
- **Selenium, editing.** `WebElement.clear()` takes focus away from the field. In this application blur means "save",
  and saving an empty value deletes the todo. The page object selects the text and types over it instead;
  Playwright's `fill()` worked directly.
- **Playwright, Firefox on macOS 27.** The browser did not start (`Could not find profile folder`) until
  `CFFIXED_USER_HOME` pointed to an empty folder. The error came with a full launch log.
- **Both.** The assignment URL answers 404, and Escape does not cancel an edit in the current application (see the
  README).

## 4. Recommendations

### When to choose Selenium

- The organisation already has Selenium suites, Grid infrastructure or a cloud provider built around WebDriver.
- Tests must be written in a language Playwright does not support, such as Ruby.
- Real branded browsers and the W3C WebDriver standard matter, including real Safari through `safaridriver`
  (Playwright's WebKit is a close build, not Safari itself).
- Native mobile testing is on the roadmap, through Appium, which uses the WebDriver protocol.

### When to choose Playwright

- A new web project with no existing automation investment.
- Fast feedback matters: parallel execution and cheap isolation work without extra tools.
- The interface re-renders often and flaky waits are a risk.
- The team wants traces to diagnose failures that only happen in CI.

### What this exercise showed

1. **Page Object Model pays off in both.** The two test files read almost the same; the differences between tools are
   confined to the page objects and the assertion style.
2. **Auto-waiting removes code, not the need to think about state.** Playwright assertions must still be written on
   locators; reading a value once with `textContent()` would reintroduce the race.
3. **Benchmarks against a public site need care.** In one run Playwright needed 36 % less time than Selenium and
   in the next only 11 % less.
4. **A test that fails is not always a bad test.** The Escape case failed because the application is wrong, and
   recording it as an expected failure keeps the suite green without hiding the defect.
