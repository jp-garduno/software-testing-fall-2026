# Selenium and Playwright Comparison

## Execution Time Comparison

The measurements below are recorded from the local test runs in this project. They
include browser startup and navigation time and therefore vary with network and
machine load.

| Metric                      |                        Selenium |                      Playwright |
| --------------------------- | ------------------------------: | ------------------------------: |
| Total execution time        |                         88.47 s |                          8.70 s |
| Average per test (14 tests) |                          6.32 s |                          0.62 s |
| Setup time                  | Included in total; not isolated | Included in total; not isolated |

Both frameworks target the current official React example at
<https://todomvc.com/examples/react/dist/>. The totals are the runner-reported
elapsed time for each complete suite. Setup is included in each total and was not
isolated; averages are total suite time divided by 14 tests. Timings vary with
network and machine load. Re-run the commands in [README.md](README.md) to compare
on another machine.

## Code Comparison

| Area                     | Selenium                           | Playwright                                     |
| ------------------------ | ---------------------------------- | ---------------------------------------------- |
| Page Object              | `selenium/pages/todo_page.py`      | `playwright/pages/TodoPage.js`                 |
| Test files               | 2                                  | 2                                              |
| Test cases               | 14                                 | 14                                             |
| Page Object LOC          | 91                                 | 66                                             |
| CRUD and filter test LOC | 79                                 | 111                                            |
| Total functional LOC     | 170                                | 177                                            |
| Main interaction style   | WebDriver calls and explicit waits | Locator API with automatic actionability waits |
| Test runner              | pytest                             | Playwright Test                                |

LOC counts exclude blank and comment-only lines, as well as configs and dependency
manifests. Selenium's Page Object is longer because it includes explicit waits and
WebDriver-specific setup; Playwright's test code is longer because its assertions
are more declarative. Overall size is similar, with Playwright using 7 more
functional lines in this implementation.

The suites implement the same user flows. Selenium requires an explicit wait for
the page and uses WebDriver element lookups; Playwright locators wait automatically
for common actions and assertions. Both Page Objects keep selectors and interactions
out of the test cases. The current TodoMVC React example does not cancel a modified
draft on Escape; both suites verify an unchanged edit can be abandoned without
changing the task instead.

## Developer Experience

| Aspect                | Selenium                               | Playwright                                     | Notes                                                                              |
| --------------------- | -------------------------------------- | ---------------------------------------------- | ---------------------------------------------------------------------------------- |
| Setup difficulty      | Moderate                               | Moderate                                       | Selenium Manager handles ChromeDriver; Playwright requires installing its browser. |
| Auto-waiting          | Explicit waits for page state          | Built in for locator actions and assertions    | The Playwright tests use `expect` assertions and polling for state changes.        |
| Debugging             | Browser logs and pytest failures       | Trace, inspector, and headed execution options | Playwright has integrated debugging utilities.                                     |
| Documentation quality | Strong                                 | Strong                                         | Both projects provide maintained documentation and examples.                       |
| Error messages        | WebDriver exceptions and wait timeouts | Locator-aware timeout messages                 | Playwright errors usually identify the failing locator/action.                     |
| IDE support           | Broad ecosystem support                | Strong editor integrations                     | Both work with common Python and JavaScript tooling.                               |

## Recommendations

- Choose Selenium when an existing project already uses WebDriver, when its
  language/browser ecosystem is required, or when broad WebDriver compatibility
  is important.
- Choose Playwright for new browser automation where integrated auto-waiting,
  browser contexts, and built-in test tooling simplify test maintenance.
- This exercise demonstrates how Page Objects make equivalent tests easier to
  compare, while the frameworks differ most in waiting behavior and setup.
