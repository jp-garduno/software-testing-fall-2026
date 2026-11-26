# Selenium vs Playwright: Comparison Report

Both suites automate the **same 41 scenarios** against TodoMVC (create, complete, delete, edit, filter), each with a
Page Object. Selenium 4.36 drives Chrome 158 from pytest; Playwright 1.65.1 drives its own Chromium build from
`@playwright/test`. Everything below was measured on one laptop (8 cores, 8 GB) that also had other applications
running (load average about 3.5 during the runs), so treat the numbers as indicative, not as a benchmark of the tools.

## 1. Execution time

`tools/benchmark.py` runs each suite, headless, several times and records the wall-clock time of the whole command
and the time the runner itself reports. Raw data: `benchmark/results-local.json` and `results-live.json`.

Selenium runs its tests serially. Playwright is shown with 1 worker (the same work, for a like-for-like comparison)
and with 4 workers, which is how it is normally used.

### Against a local copy of the app (5 runs, medians) - the like-for-like comparison

| Metric                                    | Selenium | Playwright, 1 worker | Playwright, 4 workers |
| ----------------------------------------- | -------: | -------------------: | --------------------: |
| Total execution time (whole command)      |   11.1 s |               12.2 s |                 6.1 s |
| Runner-reported time                      |   10.8 s |               11.7 s |                 5.4 s |
| Average per test (runner time / 41 tests) |   0.26 s |               0.29 s |                0.13 s |
| Failures in the 5 runs                    |        0 |                    0 |                     0 |

Run to run the spread was small (Selenium 10.9-12.5 s, Playwright serial 12.1-12.8 s, parallel 5.5-6.6 s).
Serially the two are within about 10% of each other (Selenium slightly faster); Playwright's advantage here is that it
can run tests in parallel at no extra effort, which almost halved the time.

### Against the live site (3 runs, medians) - what a user of the course would actually see

| Metric                               | Selenium | Playwright, 1 worker | Playwright, 4 workers |
| ------------------------------------ | -------: | -------------------: | --------------------: |
| Total execution time (whole command) |   13.0 s |               43.7 s |                18.4 s |
| Failures in the 3 runs               |        0 |                    0 |                     0 |

**This difference is not about the frameworks.** During these runs downloading the 237 KB app bundle took between
1.1 and 6.0 s. The suites differ in how they isolate tests: my Selenium suite shares one browser, so the app is
downloaded once and then served from the browser cache, while Playwright gives every test a brand-new browser context
with an empty cache, so every test downloads it again (I measured the first load of a fresh context at 0.7-2.4 s, and
a second load in the same context at about 25 ms). That is a trade-off in how I set up each suite, not a limit of
either tool: Selenium could start a fresh browser per test (cleaner, slower; I did not measure that) and Playwright
could share a context (faster, less isolated). The local-copy table removes the network and is the fairer
comparison; the live table shows that on a slow connection per-test isolation has a visible price.

An earlier live pass (not kept, superseded by the one above) had one parallel run with 6 failures while the network was
very slow. The Playwright assertion timeout was 5 s then; it is now 10 s, the same as the Selenium waits, so a slow
day does not penalise one tool.

### Setup time

| Step (median and range of 8 samples)          | Selenium                                                                    | Playwright           |
| --------------------------------------------- | --------------------------------------------------------------------------- | -------------------- |
| Start the browser (Selenium: driver + Chrome) | 0.9 s (0.55-1.39 s)                                                         | 0.09 s (0.08-0.15 s) |
| Create an isolated context and page           | not applicable (shared browser; storage cleared and page reloaded per test) | 0.06 s (0.04-0.28 s) |

Selenium pays its start-up once per run; Playwright pays a small context cost per test (about 41 x 0.06 s, roughly
2-3 s over the run, my arithmetic, not a separate measurement). Selenium also needs a matching chromedriver; Selenium
Manager resolved it automatically. Playwright needed `npx playwright install` to download its
browsers.

## 2. Code comparison

Counted with `tools/count_loc.py` (non-blank lines that are not comments or docstrings; Python docstrings and
JavaScript JSDoc are both excluded). Python is formatted with black at 120 columns; JavaScript is shown at prettier's
default width of 80 and at 120 columns, because the narrower width wraps more lines.

| Part                             | Selenium (Python) | Playwright (JS, 80 col) | Playwright (JS, 120 col) |
| -------------------------------- | ----------------: | ----------------------: | -----------------------: |
| Page Object                      |               128 |                      87 |                       87 |
| Tests (CRUD + filter, 41 tests)  |               182 |                     255 |                      249 |
| Shared setup (conftest / config) |                33 |                      40 |                       34 |
| **Total**                        |           **343** |                 **382** |                  **370** |

- The Page Object is about 32% smaller in Playwright, mainly because it contains **no synchronisation code**: the
  Selenium page object has 12 explicit-wait calls (`_until` / `wait.until`, plus the helper that defines them) that make
  each action wait for the DOM to reflect it, against 0 in Playwright, where locators and assertions wait by themselves.
- The Playwright tests are about 37% longer: every call is `await`ed, and each spec declares its `describe` blocks and
  its `beforeEach`. Selenium's tests are short because the page object's waits do the synchronising.
- Overall the two suites end up within about 8-11% of each other. Playwright moves the complexity out of the page
  object; it does not remove code.
- Neither suite contains a `sleep` or fixed timeout (checked with `grep`). Both avoid fixed delays, but Selenium
  needs the author to build the synchronisation (about a third of the page object's methods wait on something).
- Complexity of the logic itself is the same: both page objects expose the same user actions (add, toggle, delete,
  edit, filter, counters).

## 3. Developer experience

Judged only from building and running these two suites. Where I did not evaluate something, the table says so.

| Aspect                | Selenium                                                                | Playwright                                                                     | Notes                                                                                                                                                                                             |
| --------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Setup difficulty      | `pip install` and Chrome; the driver was fetched automatically          | `npm install` plus `npx playwright install` (downloads browsers)               | Both easy. Firefox would not start in this environment (browser exits with "Could not find profile folder"), so I could not use it with Playwright; an environment issue, not a tool issue.       |
| Auto-waiting          | None built in; explicit waits written by hand                           | Built in for actions and assertions                                            | In Selenium my `StaleElementReferenceException` came from `clear()`, which blurs the field, and this app saves on blur. Selenium reported only "stale element"; working out the cause was manual. |
| Debugging             | Stack traces from chromedriver; I wrote a screenshot-on-failure hook    | HTML report, traces and failure screenshots are built in; call log on timeouts | The Playwright call log ("waiting for element to be visible, enabled and stable") pointed straight at why the toggle-all label could not be clicked.                                              |
| Documentation quality | Not evaluated                                                           | Not evaluated                                                                  | I worked mostly from error messages and the app's own source, not by reading either project's docs in depth.                                                                                      |
| Error messages        | Short message followed by many lines of native stack                    | Message plus a call log of what it was waiting for                             | See the two examples above.                                                                                                                                                                       |
| IDE support           | Not evaluated                                                           | Not evaluated                                                                  |                                                                                                                                                                                                   |
| Parallel runs         | Needs an extra plugin (pytest-xdist) and a driver per worker; not tried | Built in (`workers`); 4 workers halved the time                                |                                                                                                                                                                                                   |
| Cross-browser         | Only Chrome used                                                        | Chromium and WebKit passed (41/41 each); Firefox could not run here            |                                                                                                                                                                                                   |

A surprise on the Playwright side: `toHaveText` ignores leading and trailing whitespace by default, so my first
"whitespace is trimmed" tests could not detect a missing trim. A mutation check showed this (see the README), and they
now compare the exact text.

## 4. Recommendations

**When I would choose Selenium**

- The team already has Selenium suites, a Selenium Grid, or tooling around WebDriver.
- Tests must be written in Java, C# or Ruby, or run on real browsers through a vendor grid.
- Serial, single-browser runs where a shared, cache-warm browser keeps things fast (11.1 s here against 12.2 s).

**When I would choose Playwright**

- A new project: no waiting code to write, and failures come with a report, trace and screenshot.
- The suite is big enough that parallel runs matter (6.1 s against 11.1 s here).
- Several browser engines are needed (Chromium and WebKit worked here).

**What I learned**

1. **Passing tests prove little until you break the app.** Running both suites against a local copy with five
   one-line mutations (the active filter shows everything, no trimming of new tasks, an off-by-one counter, "clear
   completed" keeping completed tasks, delete keeping only the deleted task) caught every mutation, and also exposed a
   weak assertion in my own Playwright tests.
2. **The live app has a real defect.** Escape does not cancel an edit, contrary to the TodoMVC specification
   (confirmed in the app's source). That scenario is an expected failure in all three suites rather than a skipped or
   deleted test. My first behave version of it passed by mistake, because the label kept the old text while the task was
   still in edit mode; a missing "no longer editing" check hid the defect.
3. **Timing comparisons are easy to get wrong.** The same suites took 12 s or 44 s depending on the network and on
   per-test isolation. I only trusted the comparison after repeating it against a local copy.
4. **The assignment's URL was out of date** (`/examples/react/` returns 404; the app is under `/dist/`), so the first
   thing to do with any given target is to open it.

## Limitations of this comparison

- One machine under unrelated load; 5 runs (local) and 3 runs (live), medians reported.
- Selenium used Chrome 158 and Playwright its own Chromium build, so the browsers themselves differ.
- Test counts are equal (41 each) but the suites were written by one person in sequence; the second was influenced by
  the first.
- Selenium and Playwright use different isolation strategies, as explained above.
