# Homework 8 – End-to-End Test Automation

**Student:** Aldo Ramón Velázquez Fonseca (A4ld0)

**Application:** [TodoMVC (TypeScript + React)](https://todomvc.com/examples/typescript-react/)

The assignment's `/examples/react/` URL returns HTTP 404. Its `/examples/react/dist/` replacement leaves the editor open when Escape is pressed. The official TypeScript + React example supports all required scenarios, including cancelling an edit.

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
python -m pip install -r requirements.txt
pytest -v --cov=. --cov-report=json --cov-report=term
```

Selenium Manager discovers and installs the matching ChromeDriver when required. To use a visible browser, set `$env:HEADED = "1"`.

For comparison timings, run `pytest selenium/tests -v` separately to exclude the report-generation unit tests from the measured duration.

### Playwright

```powershell
npm install
npx playwright install chrome firefox webkit
npm test -- --coverage --json --outputFile=js-results.json
```

The single-worker Chrome run is used for the execution comparison. To run the cross-browser suite (45 test cases) and keep its metrics separately:

```powershell
$env:PLAYWRIGHT_METRICS_FILE = "playwright-cross-browser.json"
npm run test:cross-browser
Remove-Item Env:PLAYWRIGHT_METRICS_FILE
npm run report
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

Set `TODO_URL` to test a different deployment of the application. Set `CHROME_BIN` to use a specific Chrome binary in both suites.

## Local verification

On Windows with Chrome for Testing, all 15 Selenium cases, 15 Playwright cases, and six Behave scenarios passed. The grading commands also passed five Python report tests and measured 99.42% Python and 100% JavaScript statement coverage.

