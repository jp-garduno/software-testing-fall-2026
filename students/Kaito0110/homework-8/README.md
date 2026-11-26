# Homework 8: BDD and System-Level Tests

This project automates the TodoMVC React application with Selenium and Playwright,
and defines behavior-driven scenarios with Behave.

## Requirements

- Python 3.9 or newer
- Node.js 18 or newer
- Google Chrome (Selenium) and the Playwright Chromium browser
- Internet access to open TodoMVC at <https://todomvc.com/examples/react/dist/>

## Selenium

From this directory, create and activate a virtual environment, then install and run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r selenium\requirements.txt
python -m pytest selenium\tests -v
```

Selenium Manager resolves the matching ChromeDriver on first run. The tests run
Chrome headlessly and clear TodoMVC local storage before each test.

## Playwright

```powershell
cd playwright
npm install
npx playwright install chromium
npm test
```

Each Playwright test receives a fresh browser context, so its TodoMVC state is isolated.

## BDD with Behave

Run from the homework-8 directory after installing the Selenium requirements:

```powershell
python -m behave features
```

Behave uses the same Selenium Page Object and starts a clean headless Chrome session
for every scenario.

## Coverage

Both browser suites cover creation, completion and uncompletion, deletion (including
completed todos), clearing completed todos, editing, abandoning an unchanged edit,
and all, active, and completed filters. The Behave feature covers creation,
completion, deletion, and the three filter states through a Scenario Outline.

The current official TodoMVC React example keeps an edit open on Escape and commits
on blur. The edit-abandonment check therefore leaves the value unchanged, presses
Escape, and blurs the editor; changing a draft and cancelling it is not supported
by this version of the application.

See [COMPARISON_REPORT.md](COMPARISON_REPORT.md) for the framework comparison and
local execution measurements.
