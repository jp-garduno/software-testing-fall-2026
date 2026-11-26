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
| Lines of code | 239 | 129 |
| Complexity | alot | medium |

## 3. Speed
the latest rerun took 85.54s for Selenium and 30.01s for Playwright.


## 4. Recommendations

- When would you choose Selenium?
	if I know selenium alot and need to tests alot
- When would you choose Playwright?
	i'm a begginer and don't mind the time it takes to run tests + i might purposelly slow it down to view if it is correct with my own eyes
- What did you learn?
	i learned to code selenium a bit but i just transalted selenium int playwright with copilot and didn't learn much playwright. I also learned to test with tdd and it's uses
