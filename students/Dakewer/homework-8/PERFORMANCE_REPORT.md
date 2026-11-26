# Performance report

- URL: http://127.0.0.1:7002/
- Browser: chromium 153.0.8010.12 (linux x64)
- Iterations: 10
- Date: 2026-11-26T00:59:39.182Z

All values in milliseconds. Operation times are measured from the test
process, so they include Playwright protocol overhead.

## Page load

| Metric | Min | Median | p95 | Max |
| --- | ---: | ---: | ---: | ---: |
| DOMContentLoaded | 46.3 | 56.1 | 67.2 | 67.2 |
| Load event | 46.6 | 56.3 | 67.5 | 67.5 |
| First contentful paint | 44.0 | 48.0 | 76.0 | 76.0 |

## Operations

| Metric | Min | Median | p95 | Max |
| --- | ---: | ---: | ---: | ---: |
| Add 1 todo | 28.6 | 35.4 | 58.3 | 58.3 |
| Add 50 todos | 625.4 | 770.2 | 856.1 | 856.1 |
| Toggle 1 todo (51 items) | 36.3 | 42.8 | 60.7 | 60.7 |
| Filter active (51 items) | 52.3 | 56.7 | 60.7 | 60.7 |
| Edit 1 todo | 59.8 | 66.2 | 74.2 | 74.2 |
| Delete 1 todo | 84.2 | 92.9 | 102.0 | 102.0 |
| Toggle all | 31.5 | 44.4 | 54.9 | 54.9 |
| Clear completed (50 items) | 31.9 | 38.9 | 50.4 | 50.4 |

## Notes

- Measured against the local copy of the app (`scripts/serve_app.py`), so page
  load figures do **not** include internet latency. Do not compare them with
  runs against todomvc.com.
- With 10 samples the p95 equals the maximum (nearest-rank method).
- Budgets enforced by the test: median page load < 3000 ms, median single
  operation < 1000 ms, median bulk insert < 10000 ms.
- Regenerate with `npm run test:perf`; output goes to `reports/performance/`.
