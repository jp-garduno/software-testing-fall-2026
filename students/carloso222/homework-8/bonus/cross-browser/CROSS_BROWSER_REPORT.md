# Cross-Browser Report (Bonus B)

The 28 Playwright tests were run unchanged on the three browser engines Playwright ships:

| Project    | Engine          | Build used                             | Device profile               |
| ---------- | --------------- | -------------------------------------- | ---------------------------- |
| `chromium` | Blink (Chrome)  | Chrome Headless Shell 159.0.8154.6     | Desktop Chrome, 1280×720     |
| `firefox`  | Gecko           | Firefox 159.0 (Playwright build v1572) | Desktop Firefox, 1280×720    |
| `webkit`   | WebKit (Safari) | WebKit 27.2 (Playwright build v2388)   | Desktop Safari, 1280×720 @2x |

Machine: Windows 11 (build 26200), 16 logical CPUs, Node 22.19.0, Playwright 1.65.1, live site
`https://todomvc.com/examples/react/dist/`, 25 Nov 2026.

Command: `npm run test:cross-browser` (`--project=chromium --project=firefox --project=webkit --workers=4`),
or `scripts\run_cross_browser.cmd` on Windows.

## Result

**84 / 84 tests behaved as expected** in 128.8 s (4 workers): 81 passed, and the known-defect test
(marked as an expected failure) failed as expected in each of the three browsers.

## Compatibility matrix

| Feature                                            | Chromium  | Firefox   | WebKit    | Notes                                                             |
| -------------------------------------------------- | --------- | --------- | --------- | ----------------------------------------------------------------- |
| Create todos (Enter, trimming, blank ignored)      | ✅        | ✅        | ✅        |                                                                   |
| Complete / reopen a todo                           | ✅        | ✅        | ✅        |                                                                   |
| Toggle all (transparent checkbox over the chevron) | ✅        | ✅        | ✅        | `opacity: 0` input is clickable in every engine                   |
| Delete (button revealed on hover)                  | ✅        | ✅        | ✅        | `:hover` CSS works with Playwright's `hover()` in all three       |
| Edit (double-click, Enter, blur, empty = delete)   | ✅        | ✅        | ✅        |                                                                   |
| Cancel edit with Escape                            | ❌ defect | ❌ defect | ❌ defect | same defect everywhere: it is in the app's code, not in a browser |
| Filters All / Active / Completed (hash routes)     | ✅        | ✅        | ✅        |                                                                   |
| Clear completed                                    | ✅        | ✅        | ✅        |                                                                   |
| Counter text (`"1 item left!"`)                    | ✅        | ✅        | ✅        |                                                                   |

No functional differences were found between the browsers: the DOM, the selectors and the behaviour
were identical, so the same page object works everywhere without browser-specific branches.

## Timing per browser (4 workers in parallel)

| Browser  | Tests | Total test time | Average per test | Fastest | Slowest |
| -------- | ----- | --------------- | ---------------- | ------- | ------- |
| Chromium | 28    | 68.8 s          | 2.46 s           | 0.98 s  | 4.84 s  |
| Firefox  | 28    | 262.0 s         | 9.36 s           | 6.27 s  | 25.00 s |
| WebKit   | 28    | 94.1 s          | 3.36 s           | 1.21 s  | 4.93 s  |

The three browsers ran at the same time on the same machine, so the absolute times include
contention; the ranking is the useful part: **Chromium < WebKit < Firefox**. Firefox is about 3.8× slower
than Chromium per test on this machine, mostly in browser start-up and page creation (see below).

## Difference found: Firefox times out under heavy parallel load

The first cross-browser run used Playwright's default of 8 workers (half of the 16 logical CPUs), so up
to 8 browsers of three different engines started at once. **4 Firefox tests failed** with
`Test timeout of 30000ms exceeded`. Raw output: `reports/cross-browser-8workers-output.txt`, `reports/playwright-cross-browser-8workers.json`.

The Playwright trace of one failure (`create single task`, Firefox) showed where the 30 s went:

| Step               | Time   |
| ------------------ | ------ |
| Launch browser     | 14.5 s |
| Create context     | 1.9 s  |
| Create page        | 17.1 s |
| Navigate           | 7.6 s  |
| `fill("Buy milk")` | 3.7 s  |

A `fill()` normally takes a few milliseconds, so the machine was simply saturated. This was not a
defect in the app or in the test. It is the kind of environmental flakiness that makes E2E suites
unreliable. Two changes fixed it:

1. **4 workers for the cross-browser run** (`--workers=4`). With them, all 84 tests passed.
2. **Navigation waits for `DOMContentLoaded`, then for the app's input**, instead of the full `load`
   event. On todomvc.com, `base.js` also loads Google Analytics and `learn.json`. In an earlier run,
   waiting for `load` made one Firefox test hang for 30 s. These third-party requests never happen
   against a local copy of the app, which is why the problem only showed up against the real site.

The test timeout is configurable (`PW_TIMEOUT`), but it was not raised: hiding slowness behind a longer
timeout would also hide real regressions.

## Evidence

- Screenshots of the same test (_complete multiple tasks_) in each browser: `screenshots/playwright/{chromium,firefox,webkit}/`.
  Run with `SAVE_SCREENSHOTS=1` to capture the final state of every test.
  WebKit images are 2560×1440 because the _Desktop Safari_ profile uses `deviceScaleFactor: 2`.
- Per-test matrix with durations: [`reports/timing-summary.md`](../../reports/timing-summary.md#cross-browser-matrix-playwright-bonus-b).
- Raw results: `reports/playwright-cross-browser.json`, console output: `reports/cross-browser-output.txt`.
