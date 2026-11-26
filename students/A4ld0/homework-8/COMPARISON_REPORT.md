# Selenium vs. Playwright

**Student:** Aldo Ramón Velázquez Fonseca

## 1. Execution time comparison

<!-- METRICS_START -->
| Metric | Selenium | Playwright (Chrome) |
|---|---|---|
| Total execution time (s) | Pending | Pending |
| Average elapsed time per test (s) | Pending | Pending |
| Average setup time (s) | Pending | Pending |
| Passed / attempted | Pending | Pending |

Setup measures navigation until the task input is ready. The comparison requires 15 attempted cases per framework and a single-worker Chrome run.
<!-- METRICS_END -->

## 2. Code comparison

The two page objects implement the same operations. Counting non-empty lines of the page object and two test files:

| Code | Selenium (Python) | Playwright (JavaScript) |
|---|---:|---:|
| Page object | 99 | 86 |
| CRUD tests | 67 | 82 |
| Filter tests | 20 | 22 |
| Total | 186 | 190 |

Selenium's explicit waits and element lookup account for more page-object code. Playwright has shorter methods with locator actions and retryable assertions. The JavaScript tests contain more lines due to repeated async operations and braces. Both approaches keep selectors and interaction details inside reusable page objects.

## 3. Developer experience

| Aspect | Selenium | Playwright | Notes |
|---|---|---|---|
| Setup difficulty | Moderate | Low | Selenium requires a driver, managed automatically by Selenium Manager. Playwright installs compatible browsers through its CLI. |
| Auto-waiting | Explicit WebDriverWait | Built-in actionability and retrying assertions | Both still require correct expected states. |
| Debugging | Screenshots and pytest output | Screenshots, trace viewer and HTML reports | Trace viewer captures actions and DOM snapshots. |
| Documentation quality | Detailed WebDriver guides | Detailed runnable browser-testing guides | Both document page objects and locators. |
| Error messages | WebDriver exceptions and timeout stack traces | Locator/action logs and assertion details | Browser traces add context for failed interactions. |
| IDE support | Python pytest integration | JavaScript/TypeScript test runner integration | Both can be debugged from modern IDEs. |

## 4. Recommendations and learning

I would choose Selenium for projects that already use WebDriver, need integration with Selenium Grid, or use Python for their automated tests. I would choose Playwright for new web projects that require browser isolation, cross-browser testing, and easy debugging of asynchronous interfaces.

Implementing the same cases with both frameworks demonstrates the value of Page Object Model: changes to the UI selectors can be handled in one place. Independent test setup keeps one case from affecting another. Gherkin allows the expected behavior to be described in a format that can be understood without reading the test implementation.

The execution-time comparison is pending an actual browser run. The qualitative comparison is based on the implementations and their configured features.

