# Performance Report (bonus C)

Measured with `playwright/perf/measure.js` in Chromium (Playwright 1.65.1, headless), 10 runs, each in a fresh
browser context. Raw data: `playwright/perf/results-live.json` and `results-local.json`; the table below is generated
by `playwright/perf/report.js`.

- **Live**: `https://todomvc.com/examples/react/dist/`
- **Local**: an unmodified copy of the same four files (`index.html`, `app.bundle.js`, `app.css`, `base.js`) served from
  `127.0.0.1`. It isolates what the network costs from what the app costs. The copy is not committed.

## Results

| Metric (ms) | Live median | Live p90 | Local median | Local p90 |
| --- | ---: | ---: | ---: | ---: |
| page ready (goto + input visible) | 1008.6 | 1174.8 | 37.5 | 47.4 |
| DOMContentLoaded | 648.5 | 1018.1 | 24.4 | 29.0 |
| load event | 993.4 | 1160.5 | 24.4 | 29.0 |
| first contentful paint | 460.0 | 808.0 | 16.0 | 20.0 |
| add 1 task | 29.6 | 32.1 | 27.4 | 29.8 |
| add 99 more tasks (total) | 286.8 | 333.1 | 283.4 | 307.4 |
| toggle all (100 tasks) | 29.0 | 39.9 | 30.9 | 37.2 |
| filter Active (100 completed, none shown) | 36.2 | 38.4 | 36.7 | 38.7 |
| filter Completed (100 shown) | 30.3 | 31.1 | 29.6 | 31.1 |
| clear completed (100 tasks) | 31.9 | 32.1 | 31.9 | 32.9 |
| delete 1 task | 79.0 | 79.9 | 79.1 | 79.7 |

"Add 99 more tasks" is the total for 99 additions (about 2.9 ms each is not meaningful, see the caveat below).

## What the numbers say

- **Page load is network-bound.** Against the live site the page is usable after about 1.0 s (median); from localhost
  it takes about 38 ms. The app itself (a 237 KB bundle) is not what makes loading slow.
- **Operations cost the same everywhere** (about 30 ms for add, toggle, filter and clear, even with 100 tasks on the
  list), because they run in the browser and touch no network. Nothing grows noticeably with 100 tasks.
- **Deleting is the slowest operation (about 79 ms)**, but that includes hovering the row to reveal the delete
  button, then clicking it; it is the only operation with two actions.
- Live-site load times vary more between runs (p90 up to 1.0 s for DOMContentLoaded against a 0.65 s median).

## Caveats

- **The operation timings have a floor of about 30 ms that is not the app.** They are measured from Node and include the
  Playwright round trips and the polling of `waitForFunction`, so differences of a few milliseconds between rows
  (29 vs 36 ms) are noise, not evidence that one operation is faster. They are good for spotting something that
  becomes 10x slower, not for tuning.
- 10 runs per site on one laptop, on one day, from one network. The live figures depend on the connection.
- Only Chromium was measured (Firefox does not start in this environment, see `README.md`).
