@echo off
REM Bonus B - runs the Playwright suite on Chromium, Firefox and WebKit (4 workers) and refreshes
REM reports\playwright-cross-browser.json, screenshots\playwright\ and reports\timing-summary.md.
setlocal
cd /d "%~dp0.."
set "VENV_PY=%~dp0..\..\..\..\venv\Scripts\python.exe"
if exist "%VENV_PY%" (set "PYTHON=%VENV_PY%") else (set "PYTHON=python")
if exist reports\CROSS_DONE.txt del reports\CROSS_DONE.txt
if exist screenshots\playwright rmdir /s /q screenshots\playwright
set FORCE_COLOR=0
set SAVE_SCREENSHOTS=1
set PW_OUTPUT_DIR=test-results/cross-browser
set "PW_JSON_REPORT=%CD%\reports\playwright-cross-browser.json"
pushd playwright
call npx playwright test --project=chromium --project=firefox --project=webkit --workers=4 > ..\reports\cross-browser-output.txt 2>&1
popd
"%PYTHON%" scripts\summarize_timings.py
echo finished > reports\CROSS_DONE.txt
echo Done. You can close this window.
pause
