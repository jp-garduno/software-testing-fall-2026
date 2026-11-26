# Selenium and Playwright Comparison

## 1. Execution Time Comparison

Measured by running `python run_tests.py`, which runs the Selenium and
Playwright suites concurrently. Each backend runs 11 pytest cases and 6 Behave
scenarios. Average time is the backend's suite total divided by 17 test cases
and scenarios.

| Metric | Selenium | Playwright |
|---|---:|---:|
| Total execution time | 78.00 s | 26.97 s |
| Average per test | 4.59 s | 1.59 s |
| Setup time (browser launch + navigation) | 1.52 s | 1.31 s |
| TodoPage line coverage | 98% | 98% |

Coverage is for each browser's `TodoPage` implementation, including pytest and
Behave runs. The remaining uncovered lines are defensive or invalid-input
branches.

## 2. Code Comparison

| Metric | Selenium | Playwright |
|---|---|---|
| Lines of code |  |  |
| Complexity |  |  |

## 3. Developer Experience

| Aspect | Selenium | Playwright | Notes |
|---|---|---|---|
| Setup difficulty |  |  |  |
| Auto-waiting |  |  |  |
| Debugging |  |  |  |
| Documentation quality |  |  |  |
| Error messages |  |  |  |
| IDE support |  |  |  |

## 4. Recommendations

- When would you choose Selenium?
- When would you choose Playwright?
- What did you learn?
