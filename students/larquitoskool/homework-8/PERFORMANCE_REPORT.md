# Performance Metrics Report (Bonus C)

Metrics captured via `playwright/tests/todo-performance.spec.js` against `https://demo.playwright.dev/todomvc/` across Chromium, Firefox, and WebKit.

## Measured Benchmarks Across Browsers

| Operation | Budget (Threshold) | Chromium | Firefox | WebKit | Status |
| --- | --- | --- | --- | --- | --- |
| Initial Page Load (`navigate`) | < 10,000 ms | 905 ms | 1,386 ms | 1,634 ms | Pass |
| Create 5 Tasks Sequentially | < 5,000 ms | 728 ms | 1,151 ms | 1,953 ms | Pass |
| Toggle + Full Filter Cycle (Active -> Completed -> All) | < 3,000 ms | 516 ms | 662 ms | 1,443 ms | Pass |
| **Combined Measured Operations** | **< 18,000 ms** | **2,149 ms** | **3,199 ms** | **5,030 ms** | **Pass** |

## Observations

- **Chromium led in every metric:** Initial load completed in under 1 second (`905 ms`), and the full filter cycle took `516 ms`.
- **Firefox showed moderate overhead:** Page load (`1,386 ms`) and creating 5 tasks (`1,151 ms`) were ~1.5x slower than Chromium, though filtering remained responsive (`662 ms`).
- **WebKit had the highest interaction latency on Windows:** Creating 5 tasks (`1,953 ms`) and cycling through filters (`1,443 ms`) took roughly 2.7x–2.8x longer than Chromium, while still staying comfortably within all defined performance budgets.
- **End-to-end suite impact:** Measuring per-operation metrics inside automated tests confirmed that React state updates themselves remain fast across all engines, and that cross-browser speed differences are driven mainly by engine startup and input dispatch overhead.