# Cross-Browser Compatibility Matrix (Bonus B)

The 20 Playwright tests run on the three browser engines with `npm run test:cross-browser`.

**Environment**: macOS 27.0 (Apple M2), Playwright 1.64.0, headless. Full output:
[`reports/playwright-cross-browser.txt`](reports/playwright-cross-browser.txt) (60 passed).

| Feature                          | Chromium 156 | Firefox 157 | WebKit 27.2 |
| -------------------------------- | ------------ | ----------- | ----------- |
| Create one and several tasks     | Pass         | Pass        | Pass        |
| Trim input, ignore blank tasks   | Pass         | Pass        | Pass        |
| Complete and unmark tasks        | Pass         | Pass        | Pass        |
| Toggle all                       | Pass         | Pass        | Pass        |
| Delete (hover button)            | Pass         | Pass        | Pass        |
| Clear completed                  | Pass         | Pass        | Pass        |
| Filter all / active / completed  | Pass         | Pass        | Pass        |
| Edit and save with Enter or blur | Pass         | Pass        | Pass        |
| Save empty text deletes the task | Pass         | Pass        | Pass        |
| Escape cancels an edit           | **Defect**   | **Defect**  | **Defect**  |

"Defect" means the application does not follow the specification. The test is marked with `test.fail`, so Playwright
counts it as passed while the defect is present (shown with `✘` in the console output).

## Browser differences observed

- **Functional behaviour**: none. The same page object and the same assertions worked in the three engines without
  browser-specific code.
- **Speed of operations**: Chromium was the fastest at adding tasks; Firefox was the slowest at adding, toggling all
  and clearing (see [PERFORMANCE_REPORT.md](PERFORMANCE_REPORT.md)).
- **Tooling**: only Firefox needed a workaround to start on macOS 27 (`CFFIXED_USER_HOME`, see the README). This is a
  problem of the test environment, not of the application.

## Scope

- Selenium and the BDD scenarios were run on Chrome only.
- WebKit is the engine behind Safari, but it is not the Safari application.
- Desktop viewports only; no mobile emulation.
