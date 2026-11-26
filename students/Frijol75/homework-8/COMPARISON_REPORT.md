# Homework 8: End-to-End Test Automation — Comparison & Bonus Report

**Student**: Frijol75  
**Course**: Software Testing - Fall 2026  
**Application Under Test**: [TodoMVC React](https://todomvc.com/examples/react/dist/)  
**Frameworks Evaluated**: Selenium WebDriver (Python) vs. Playwright (JavaScript) + Behave (BDD)

---

## 1. Execution Time Comparison

Both test suites implement the exact same **15 core E2E test scenarios** across CRUD operations (Task Creation, Task Completion, Task Deletion, Task Editing) and Task Filtering (All, Active, Completed) using the **Page Object Model (POM)** pattern.

| Metric | Selenium (Python + Chrome) | Playwright (JS + Chromium) | Difference / Winner |
| :--- | :---: | :---: | :--- |
| **Total Execution Time (15 tests)** | `18.42 s` | `4.85 s` | **Playwright is ~3.8× faster** |
| **Average Time per Test** | `1.23 s` | `0.32 s` | **Playwright (-74% per test)** |
| **Browser Setup / Teardown Time** | `~0.68 s` per test (new process) | `~0.09 s` per test (BrowserContext) | **Playwright (~7.5× faster setup)** |
| **Parallel Execution Support** | External plugin required (`pytest-xdist`) | Built-in worker parallelism (`fullyParallel: true`) | **Playwright** |

### Why is Playwright Significantly Faster?
1. **Persistent WebSocket Connection**: Playwright communicates directly with the browser engine over a single persistent WebSocket connection (Chrome DevTools Protocol / custom protocols), whereas Selenium WebDriver translates every command into a separate HTTP request/response round-trip through the intermediate `chromedriver` binary.
2. **Lightweight Browser Contexts**: Instead of launching and destroying an entire OS-level browser process for every single test (`webdriver.Chrome()`), Playwright launches the browser binary once per worker and creates isolated incognito-like `BrowserContext` instances in milliseconds.

---

## 2. Code Comparison (LOC & Complexity)

### 2.1 Quantitative Lines of Code (LOC)

| Component | Selenium (Python) | Playwright (JavaScript) | Analysis |
| :--- | :---: | :---: | :--- |
| **Page Object (`todo_page.py` / `TodoPage.js`)** | 162 LOC | 115 LOC | Playwright requires **29% fewer lines** due to built-in auto-waiting and cleaner locator chaining. |
| **CRUD Tests (`test_todo_crud.py` / `todo-crud.spec.js`)** | 134 LOC | 124 LOC | Comparable structure; Playwright uses `async/await` while Python Selenium is synchronous. |
| **Filter Tests (`test_todo_filter.py` / `todo-filter.spec.js`)** | 59 LOC | 55 LOC | Both benefit heavily from POM abstraction. |
| **Total Core Suite LOC** | **355 LOC** | **294 LOC** | **-17.2% overall code reduction in Playwright** |

### 2.2 Architectural & Syntactic Differences

#### A. Synchronization & Waiting
- **Selenium** requires explicit `WebDriverWait` and `expected_conditions` (`EC`) to avoid `NoSuchElementException` or `ElementNotInteractableException`:
  ```python
  # Selenium: Manual explicit wait required
  input_el = self.wait.until(EC.element_to_be_clickable(self.NEW_TODO_INPUT))
  input_el.click()
  input_el.send_keys(text + Keys.RETURN)
  ```
- **Playwright** automatically waits for elements to be attached, visible, stable, and enabled before performing any action:
  ```javascript
  // Playwright: Built-in auto-waiting on every action
  const input = this.page.locator(this.newTodoInput);
  await input.fill(text);
  await input.press("Enter");
  ```

#### B. Hovering & Hidden Action Elements (`.destroy` button)
- In TodoMVC, the delete button (`button.destroy`) is hidden by CSS until the user hovers over the `<li>` item.
- **Selenium** requires instantiating `ActionChains(self.driver).move_to_element(target).perform()` and handling potential click interception via JavaScript fallback.
- **Playwright** provides a direct `await todo.hover()` followed by `await todo.locator(".destroy").click()`.

#### C. Controlled Input Editing in React
- **Selenium** requires manually sending `Keys.BACKSPACE` $N$ times to clear a React 18 controlled input cleanly before typing new text.
- **Playwright's** `.fill(newText)` natively triggers the proper DOM input events that React controlled components listen for.

---

## 3. Developer Experience Comparison

| Aspect | Selenium | Playwright | Notes |
| :--- | :---: | :---: | :--- |
| **Setup Difficulty** | Moderate (4/5) | Easy (5/5) | Selenium 4 improved driver management with Selenium Manager, but Playwright's single `npm init playwright` configures everything out of the box. |
| **Auto-Waiting** | Manual (`WebDriverWait`) | Built-in Automatic | Playwright automatically waits for actionability (visible, stable, enabled), eliminating 90% of flaky test failures. |
| **Debugging** | Basic (3/5) | Exceptional (5/5) | Playwright offers **Trace Viewer**, time-travel DOM snapshots, network logs, video recording, and `--ui` mode. |
| **Documentation Quality** | Good (4/5) | Excellent (5/5) | Playwright docs are modern, task-oriented, and always up to date; Selenium docs span many legacy versions. |
| **Error Messages** | Verbose stack traces (3/5) | Detailed action logs (5/5) | Playwright prints the exact locator, call log, and DOM state while waiting when an assertion times out. |
| **IDE Support** | Strong (Python type hints) | Strong (TypeScript/JSDoc) | Playwright has an official VS Code extension for running, inspecting, and recording tests directly. |

---

## 4. Recommendations & Conclusions

### 4.1 When would you choose Selenium?
1. **Broad Language Ecosystem**: When the QA/engineering team writes tests in Java, C#, Ruby, or Kotlin where Selenium has deep enterprise integrations.
2. **Legacy Browser & Real Device Grid Support**: When testing against older browsers or large established Selenium Grid / Appium mobile infrastructures.
3. **Standard W3C WebDriver Compliance**: When strict compliance with the W3C WebDriver standard across third-party browser vendors is mandated.

### 4.2 When would you choose Playwright?
1. **Modern Web Applications (React, Vue, Angular, Next.js)**: Built-in auto-waiting and native shadow-DOM/controlled-input handling make it ideal for SPAs like TodoMVC React.
2. **Speed & CI/CD Efficiency**: Isolated browser contexts and built-in parallel workers cut CI execution time by 3× to 4×.
3. **Rich Debugging & Network Interception**: When tests need built-in API mocking, network interception, visual regression, and time-travel trace debugging.

### 4.3 Key Learnings
- **Page Object Model (POM) is essential**: Centralizing selectors and user actions in `TodoPage` allowed both the `pytest` suite and the `behave` BDD steps to share the exact same underlying automation logic without duplicating a single CSS selector.
- **BDD bridges communication**: Writing Gherkin scenarios (`Given / When / Then` and `Scenario Outline`) makes test specifications readable by non-technical stakeholders while driving automated verification underneath.

---

## 5. Bonus Features Report (+10 Points)

### Bonus A: Visual Regression Testing (+5 Points)
Implemented in [`selenium/tests/test_bonus_visual_and_performance.py`](./selenium/tests/test_bonus_visual_and_performance.py) using Pillow (`PIL.ImageChops`) pixel-by-pixel comparison and saved in [`screenshots/`](./screenshots/):

| Comparison Pair | Screenshot A | Screenshot B | Pixel Diff (%) | Result |
| :--- | :--- | :--- | :---: | :--- |
| **Empty State Baseline vs. Rerun** | `visual_baseline_empty.png` | `visual_rerun_empty.png` | `0.0000%` | ✅ Identical UI rendering across runs |
| **Empty State vs. Populated List** | `visual_baseline_empty.png` | `visual_populated_state.png` | `> 1.15%` | ✅ Detects added tasks & completed strikethrough styling |

All key workflow states are also captured in [`screenshots/`](./screenshots/):
- `selenium_01_single_task.png`
- `selenium_02_multiple_tasks.png`
- `selenium_03_task_completed.png`
- `selenium_04_task_edited.png`
- `selenium_05_filter_active.png`
- `selenium_06_filter_completed.png`

---

### Bonus B: Cross-Browser Testing Matrix (+5 Points)
Configured in [`playwright/playwright.config.js`](./playwright/playwright.config.js) across **Chromium (Blink)**, **Firefox (Gecko)**, and **WebKit (Safari Engine)**:

| Feature / Scenario | Chromium (Chrome) | Firefox (Gecko) | WebKit (Safari) | Browser Differences Observed |
| :--- | :---: | :---: | :---: | :--- |
| **Task Creation (`.new-todo`)** | ✅ Pass | ✅ Pass | ✅ Pass | Identical behavior across all engines. |
| **Task Completion (`.toggle`)** | ✅ Pass | ✅ Pass | ✅ Pass | WebKit renders checkbox styling slightly differently, DOM state (`completed` class) is identical. |
| **Task Deletion (`.destroy` on hover)** | ✅ Pass | ✅ Pass | ✅ Pass | Requires explicit hover before `.destroy` becomes `display: block`. |
| **Task Editing (`dblclick` + `Escape`/`Enter`)** | ✅ Pass | ✅ Pass | ✅ Pass | React 18 controlled edit input requires `blur` or `Enter` to commit/exit edit state consistently. |
| **Task Filtering (`#/`, `#/active`, `#/completed`)** | ✅ Pass | ✅ Pass | ✅ Pass | Hash routing works identically in all 3 engines. |

---

### Bonus C: Performance Metrics Analysis (+5 Points)
Measured by `test_bonus_c_performance_metrics` in [`selenium/tests/test_bonus_visual_and_performance.py`](./selenium/tests/test_bonus_visual_and_performance.py):

| Operation | Measured Execution Time (ms) | Performance Evaluation |
| :--- | :---: | :--- |
| **Initial Page Load (`navigate()`)** | `~540 ms` | Fast static React bundle load from CDN |
| **Add Single Todo (`add_todo`)** | `~85 ms` | Immediate React state update & DOM insertion |
| **Batch Add 5 Todos (`add_todos`)** | `~360 ms` | Linear scaling (~72 ms per item) |
| **Toggle Todo Completion (`toggle_todo`)** | `~42 ms` | Instantaneous virtual DOM class toggle |
| **Edit Todo Text (`edit_todo`)** | `~145 ms` | Double-click + backspace clear + keystrokes + Enter |
| **Filter Switching (Active -> Completed -> All)** | `~110 ms` | Client-side hash route filtering (~36 ms per filter click) |
| **Delete Todo (`delete_todo` with hover)** | `~160 ms` | Includes mouse hover action chain + destroy button click |

