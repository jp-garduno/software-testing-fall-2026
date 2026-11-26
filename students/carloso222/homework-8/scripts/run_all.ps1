# Runs every suite of Homework 8 and writes the reports used by COMPARISON_REPORT.md.
# Usage (PowerShell, from the homework-8 folder):
#   .\scripts\run_all.ps1                         # everything
#   .\scripts\run_all.ps1 -SkipCrossBrowser -SkipPerf
# Uses $env:PYTHON if set (e.g. the repo's venv), otherwise "python".
# Timed runs take no screenshots (they would add time); evidence runs take them.
param(
    [switch]$SkipCrossBrowser,
    [switch]$SkipPerf
)

$ErrorActionPreference = "Continue"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8   # read npx/python output as UTF-8
$env:FORCE_COLOR = "0"                                     # no ANSI colour codes in the logs (Node)
$env:PY_COLORS = "0"                                       # ... and none from pytest
$env:PYTHONIOENCODING = "utf-8"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$python = if ($env:PYTHON) { $env:PYTHON } else { "python" }
New-Item -ItemType Directory -Force -Path reports | Out-Null
$wall = [ordered]@{}
$utf8 = New-Object System.Text.UTF8Encoding $false

function Measure-Step([string]$name, [scriptblock]$block) {
    Write-Host "`n=== $name ===" -ForegroundColor Cyan
    $watch = [System.Diagnostics.Stopwatch]::StartNew()
    & $block
    $watch.Stop()
    $script:wall[$name] = [math]::Round($watch.Elapsed.TotalSeconds, 2)
    Write-Host ("{0} took {1:N2} s" -f $name, $watch.Elapsed.TotalSeconds) -ForegroundColor Cyan
}

function Save-Log([string]$file) {
    # Collects the pipeline output and writes it as UTF-8 without BOM (Tee-Object would write UTF-16).
    begin { $lines = New-Object System.Collections.Generic.List[string] }
    process { $text = "$_"; Write-Host $text; $lines.Add($text) }
    end { [System.IO.File]::WriteAllLines((Join-Path $root $file), $lines, $utf8) }
}

# --- Selenium + BDD -----------------------------------------------------------------
$env:SAVE_SCREENSHOTS = "0"
Measure-Step "selenium" { & $python -m pytest --junitxml=reports/selenium-junit.xml 2>&1 | Save-Log "reports/selenium-output.txt" }
$env:SAVE_SCREENSHOTS = "1"
Measure-Step "selenium_screenshots" { & $python -m pytest -q 2>&1 | Out-Null }
Measure-Step "behave" { & $python -m behave --junit --junit-directory reports/behave-junit 2>&1 | Save-Log "reports/behave-output.txt" }

# --- Playwright ---------------------------------------------------------------------
Push-Location playwright
if (-not (Test-Path node_modules)) { npm install --no-audit --no-fund }
$env:SAVE_SCREENSHOTS = "0"
$env:PW_OUTPUT_DIR = "test-results/chromium"
$env:PW_JSON_REPORT = Join-Path $root "reports/playwright-results.json"
Measure-Step "playwright" { npx playwright test --project=chromium 2>&1 | Save-Log "reports/playwright-output.txt" }
$env:PW_WORKERS = "1"
$env:PW_JSON_REPORT = Join-Path $root "reports/playwright-results-1worker.json"
Measure-Step "playwright_1worker" { npx playwright test --project=chromium 2>&1 | Save-Log "reports/playwright-1worker-output.txt" }
# Same browser binary as Selenium (the installed Google Chrome) for an apples-to-apples comparison.
$env:PW_CHANNEL = "chrome"
$env:PW_JSON_REPORT = Join-Path $root "reports/playwright-results-chrome-1worker.json"
Measure-Step "playwright_chrome_1worker" { npx playwright test --project=chromium 2>&1 | Save-Log "reports/playwright-chrome-1worker-output.txt" }
Remove-Item Env:PW_CHANNEL
Remove-Item Env:PW_WORKERS
if (-not $SkipCrossBrowser) {
    $env:SAVE_SCREENSHOTS = "1"
    $env:PW_OUTPUT_DIR = "test-results/cross-browser"
    $env:PW_JSON_REPORT = Join-Path $root "reports/playwright-cross-browser.json"
    # 4 workers: with 8, three browsers starting at once overloaded the machine and Firefox timed out.
    Measure-Step "cross_browser" { npx playwright test --project=chromium --project=firefox --project=webkit --workers=4 2>&1 | Save-Log "reports/cross-browser-output.txt" }
    $env:SAVE_SCREENSHOTS = "0"
}
if (-not $SkipPerf) {
    $env:PW_CHANNEL = "chrome"   # Selenium also drives the installed Chrome
    $env:PW_OUTPUT_DIR = "test-results/perf"
    $env:PW_JSON_REPORT = Join-Path $root "reports/playwright-perf.json"
    Measure-Step "perf_playwright" { npx playwright test --project=perf 2>&1 | Save-Log "reports/perf-playwright-output.txt" }
    Remove-Item Env:PW_CHANNEL
}
Remove-Item Env:PW_JSON_REPORT
Remove-Item Env:PW_OUTPUT_DIR
Pop-Location

# --- Bonus C: performance -------------------------------------------------------------
if (-not $SkipPerf) {
    Measure-Step "perf_selenium" { & $python bonus/performance/selenium_perf.py 2>&1 | Save-Log "reports/perf-selenium-output.txt" }
    & $python bonus/performance/generate_report.py
}

[System.IO.File]::WriteAllText((Join-Path $root "reports/wall-clock.json"), ($wall | ConvertTo-Json), $utf8)
& $python scripts/summarize_timings.py
Write-Host "`nDone. See reports/timing-summary.md and bonus/performance/PERFORMANCE_REPORT.md" -ForegroundColor Green
