# Performance Report (Bonus C)

Measured by [`playwright/perf/performance.spec.js`](playwright/perf/performance.spec.js) with `npm run test:perf`.

- 5 iterations per browser, each in a new context (empty cache), one worker.
- Operation times include the assertion that confirms the screen was updated, and the automation overhead. They are
  useful to compare runs and browsers, not as the exact time a user perceives.
- The measurement was run twice on the same day (Apple M2, macOS 27.0). All values are medians in milliseconds,
  written as **run A / run B**.

## Page load

| Metric                           | Chromium 156 | Firefox 157 | WebKit 27.2 |
| -------------------------------- | ------------ | ----------- | ----------- |
| First contentful paint           | 304 / 692    | 946 / 830   | 547 / 1290  |
| DOMContentLoaded                 | 403 / 860    | 949 / 1176  | 637 / 1385  |
| Load event                       | 462 / 1323   | 1924 / 1243 | 940 / 1754  |
| Navigation until input is usable | 475 / 1343   | 1954 / 1263 | 961 / 1775  |

## Operations with 50 tasks

| Operation                   | Chromium 156 | Firefox 157 | WebKit 27.2 |
| --------------------------- | ------------ | ----------- | ----------- |
| Add 50 tasks (one by one)   | 197 / 193    | 300 / 302   | 267 / 298   |
| Toggle all                  | 27 / 35      | 53 / 48     | 29 / 38     |
| Switch to the Active filter | 43 / 42      | 50 / 49     | 34 / 35     |
| Clear completed             | 33 / 33      | 57 / 54     | 34 / 34     |

JSON of run B, with minimum and maximum: `reports/performance-<browser>.json`.

## Analysis

- **Page load is dominated by the network.** The same browser differs by up to almost three times between runs, so
  these figures cannot rank the browsers.
- **Operations are stable and local.** The application keeps its state in memory and makes no requests after loading;
  most medians differ by less than 15 % between runs.
- **Adding a task costs about 4 to 6 ms** including the round trip from the test runner.
- **Bulk operations stay under 60 ms** with 50 tasks in all three engines.

## Budgets

The test fails if a median exceeds these limits. They are deliberately generous so that network noise does not cause
false alarms:

| Metric                      | Budget |
| --------------------------- | ------ |
| Navigation                  | 10 s   |
| Add 50 tasks                | 15 s   |
| Toggle all, filter, clear   | 2 s    |
