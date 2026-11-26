# Framework Comparison Report: Selenium vs Playwright

## 1. Execution Time Comparison

Results measured running all E2E test suites in headless mode on Windows against the TodoMVC React application (`https://demo.playwright.dev/todomvc/`):

| Metric | Selenium (pytest / Chrome) | Playwright (All 3 Browsers: Chromium, Firefox, WebKit) | Behave (BDD / Selenium Chrome) |
| --- | --- | --- | --- |
| Tests / Scenarios Executed | 14 tests | 36 tests (12 per browser) | 6 scenarios (25 steps) |
| Total Wall-Clock Time | 75.13s (1m 15s) | 1.4m (~84s) | 8.722s (step execution time) |
| Effective Wall-Clock Avg per Test | 5.37s / test | ~2.33s / test | 1.45s / scenario (steps only) |
| Execution Mode | Sequential (1 browser instance per test) | Parallel across workers & BrowserContexts | Sequential (1 browser instance per scenario) |

### Playwright Per-Browser Breakdown (Individual Test Durations)

| Browser Engine | Tests Passed | Avg Duration per Test | Fastest Test | Slowest Test |
| --- | --- | --- | --- | --- |
| Chromium | 12 / 12 | 3.93s (warm tests ~2.4s) | 2.0s (`edit and save task`) | 7.5s (`mark task as complete and unmark it`) |
| Firefox | 12 / 12 | 11.19s | 4.0s (`view active tasks only`) | 22.9s (`complete multiple tasks`) |
| WebKit | 12 / 12 | 6.13s | 4.0s (`delete single task`) | 9.0s (`complete multiple tasks`) |

**Key Timing Insight:** In almost the same wall-clock time that Selenium took to run 14 sequential tests on a single browser (`75.13s`), Playwright executed **36 tests across three completely different browser engines** (`~84s`), achieving more than **2.3x higher throughput** per test thanks to parallel workers and lightweight BrowserContexts.

---

## 2. Code Comparison

| Dimension | Selenium (Python) | Playwright (JavaScript) |
| --- | --- | --- |
| Page Object LOC (`todo_page.py` vs `TodoPage.js`) | ~125 LOC | ~85 LOC |
| CRUD + Filter Tests LOC | ~115 LOC | ~110 LOC |
| Wait management | Requires explicit `WebDriverWait`, `EC`, and custom wait helpers (`_click_filter`) | Built-in auto-waiting on every locator and action |
| Handling React re-renders | Needed explicit `StaleElementReferenceException` retry loop in `get_visible_todos()` | Handled natively by Playwright locators with zero stale-element errors |
| Hover & hidden button clicks | Required `ActionChains.move_to_element()` + JS click fallback for stability | Native `todo.hover()` and `locator.click()` worked reliably across all 3 engines |
| Inline text editing | Needed manual key sequence (`Ctrl+A`, `Backspace`, `send_keys`, `Return`/`Escape`) | Single atomic `.fill(newText)` followed by `.press("Enter" / "Escape")` |

---

## 3. Developer Experience

| Aspect | Selenium | Playwright | Notes |
| --- | --- | --- | --- |
| Setup difficulty | Medium | Easy | Selenium 4 Manager auto-downloaded Chrome for Testing even without local Chrome installed; Playwright cleanly installs Chromium, Firefox, and WebKit via `npx playwright install`. |
| Auto-waiting | Manual | Built-in | Selenium required explicit waits and stale-element handling for React filter transitions. |
| Debugging | Basic | Excellent | Playwright provides per-test timings, HTML reports, traces, and automatic failure screenshots out of the box. |
| Documentation quality | Good | Excellent | Playwright documentation offers concise, modern async POM examples. |
| Error messages | Verbose stacktraces | Clear and actionable | Selenium printed long chromedriver stacktraces on `StaleElementReferenceException`; Playwright pinpoints exact locators and DOM state. |
| IDE support | Good | Excellent | Strong IntelliSense and integrated test runner support in VS Code. |

---

## 4. Issues Encountered & Lessons Learned During Initial Runs

Running automated E2E tests surfaced three concrete real-world issues that directly illustrated the differences between Selenium and Playwright:

1. **Outdated Application URL (`TimeoutException` across all 14 tests — 208.78s):**
   The original URL referenced in the specification (`https://todomvc.com/examples/react/`) now returns a 404 page because TodoMVC relocated its compiled React build to `/examples/react/dist/`. As a result, all 14 Selenium tests timed out waiting 10 seconds for `.new-todo`.
2. **Real Defect Detected in TodoMVC React (`tastejs/todomvc#2309`):**
   After updating to `https://todomvc.com/examples/react/dist/`, 13 of 14 Selenium tests passed, but `test_cancel_edit_preserves_original_text` failed (`AssertionError: assert ['Discarded text'] == ['Original task']`). Investigation confirmed an open upstream bug in that build where pressing `Escape` fails to cancel editing and blurring saves the discarded text. Both suites were migrated to the official Playwright-maintained TodoMVC mirror (`https://demo.playwright.dev/todomvc/`), which adheres strictly to the TodoMVC specification.
3. **DOM Race Condition in Selenium (`StaleElementReferenceException`):**
   When running `test_view_active_tasks_only` on the React app, clicking the **Active** filter triggered a DOM re-render at the exact millisecond Selenium iterated over `.todo-list li` elements, throwing `StaleElementReferenceException`. Fixing this required adding `_click_filter()` (waiting for the `selected` class on the filter anchor) and a retry loop in `get_visible_todos()`. By contrast, Playwright executed the exact same scenario 3 times (Chromium, Firefox, WebKit) with zero flakiness and no manual retry code.

---

## 5. Cross-Browser Compatibility Matrix (Bonus B)

All 12 Playwright tests (CRUD, editing, filtering, and performance) passed across all three engines (`36 passed` in `1.4m`):

| Feature Area | Chromium | Firefox | WebKit | Notes |
| --- | --- | --- | --- | --- |
| Task Creation (Single & Multiple) | Pass | Pass | Pass | Consistent Enter key submission |
| Task Completion & Unmarking | Pass | Pass | Pass | Identical `.completed` class & active counter updates |
| Task Deletion & Clear Completed | Pass | Pass | Pass | Hover reveals `.destroy` consistently across engines |
| Task Filtering (All / Active / Completed) | Pass | Pass | Pass | Hash routing (`#/`, `#/active`, `#/completed`) behaves uniformly |
| Task Editing & Cancel (`Escape`) | Pass | Pass | Pass | Double-click inline editing and Escape revert work identically |
| Performance Thresholds | Pass | Pass | Pass | Chromium was fastest; WebKit had highest DOM mutation latency |

---

## 6. Recommendations

- **When to choose Selenium:** Choose Selenium when integrating with legacy browser environments, existing enterprise Selenium Grids, or established Python/Java BDD toolchains like Behave/Cucumber.
- **When to choose Playwright:** Choose Playwright for modern SPA frameworks (React, Vue, Angular) where parallel execution, native auto-waiting, multi-engine coverage (including WebKit/Safari), and lower test maintenance overhead are priorities.
- **What I learned:** Applying the Page Object Model in both frameworks isolated every fix (changing the URL, fixing `edit_todo`, and hardening filter waits) to a single class file without touching test assertions. Moreover, real E2E tests do not just validate code—they uncover genuine upstream defects and DOM timing pitfalls.