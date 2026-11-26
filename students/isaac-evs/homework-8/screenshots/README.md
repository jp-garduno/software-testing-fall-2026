# Screenshots

All captured on 2026-11-23 from real runs against `https://todomvc.com/examples/react/dist/`.

| File                            | What it shows                                                                          | How it was made                                                                               |
| ------------------------------- | -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `selenium-test-execution.png`   | `pytest -v` of the Selenium suite: 40 passed, 1 expected failure, page-object coverage | The console output (`output/selenium-pytest.txt`) rendered to an image                        |
| `playwright-test-execution.png` | `playwright test --project=chromium`: 41 passed                                        | Console output (`output/playwright-list.txt`) rendered to an image                            |
| `behave-test-execution.png`     | `behave`: 9 scenarios passed, 1 excluded                                               | Console output (`output/behave.txt`) rendered to an image                                     |
| `visual-test-execution.png`     | The 5 visual regression tests passing                                                  | Console output (`output/playwright-visual.txt`) rendered to an image                          |
| `playwright-html-report.png`    | Playwright's own HTML report: 41 passed, 0 failed, 0 flaky                             | A real browser screenshot of `playwright-report/index.html`                                   |
| `visual-diff-example.png`       | How a visual difference is reported (red/yellow = changed pixels)                      | Playwright's diff image from a run with a style change injected on purpose (`VISUAL_BREAK=1`) |

**The `*-test-execution.png` files are not screenshots of a terminal window.** The runs were made from a command-line
session without a screen to capture, so the console text was saved to `output/` and rendered to PNG with
`tools/render_terminal.js` (`node tools/render_terminal.js <text> <png> <title>`). The text files are the source of truth.
The report and diff images are genuine browser output.
