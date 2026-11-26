# Homework 8 – End-to-End Test Automation

**Student:** Aldo Ramón Velázquez Fonseca (A4ld0)

**Application:** [React TodoMVC](https://todomvc.com/examples/react/)

## Coverage

| Feature | Selenium | Playwright |
|---|---:|---:|
| Create tasks | 3 | 3 |
| Complete and reopen tasks | 3 | 3 |
| Delete and clear completed tasks | 3 | 3 |
| Filter tasks | 3 | 3 |
| Edit, save and cancel edits | 3 | 3 |
| Total | 15 | 15 |

The Behave test suite contains six scenarios, including three examples of the filter scenario outline. Each case starts with an isolated browser session or context.

## Requirements

- Python 3.10–3.13 and pip
- Node.js 20+ and npm
- Google Chrome
- Internet access to TodoMVC and the package/browser registries

Run the following PowerShell commands from this homework folder.

### Selenium

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r selenium/requirements.txt
python -m pytest selenium -v
```

Selenium Manager discovers and installs the matching ChromeDriver when required. To use a visible browser, set `$env:HEADED = "1"`.

### Playwright

```powershell
cd playwright
npm install
npx playwright install chrome firefox webkit
npm run test:chrome -- --workers=1
cd ..
```

The single-worker Chrome run is used for the execution comparison. To run the cross-browser suite (45 test cases) and keep its metrics separately:

```powershell
cd playwright
$env:PLAYWRIGHT_METRICS_FILE = "playwright-cross-browser.json"
npm test
Remove-Item Env:PLAYWRIGHT_METRICS_FILE
npm run report
cd ..
```

### BDD

With the Python virtual environment still active:

```powershell
python -m behave features
```

### Generate the measured comparison

```powershell
python generate_report.py
```

The script updates the measured sections in `COMPARISON_REPORT.md` and writes the bonus results to `PERFORMANCE_REPORT.md`. The tests record real page-load and operation durations, status, and screenshots. The Playwright HTML report also includes traces on failure.

The default application URL can be overridden with the `TODO_URL` environment variable.

## Current execution status

All 15 Selenium test cases, 15 Playwright test cases and six BDD scenarios are implemented. Browser execution is pending because the development environment could not install the test dependencies or reach the external service. No timings, screenshots or pass results have been fabricated.

