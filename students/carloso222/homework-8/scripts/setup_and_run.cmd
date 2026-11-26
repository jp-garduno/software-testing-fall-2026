@echo off
REM Homework 8 - installs the dependencies and runs every suite (double-click or run from cmd).
REM Python: uses the repo's venv (..\..\..\..\venv) when it exists, otherwise "python" from PATH.
setlocal
cd /d "%~dp0.."
if not exist reports mkdir reports
set "LOG=%CD%\reports\setup-log.txt"
set "VENV_PY=%~dp0..\..\..\..\venv\Scripts\python.exe"
if exist "%VENV_PY%" (set "PYTHON=%VENV_PY%") else (set "PYTHON=python")
if exist reports\RUN_DONE.txt del reports\RUN_DONE.txt
echo Python: %PYTHON%
echo Python: %PYTHON% > "%LOG%"

echo [1/4] Installing Python packages (selenium, behave, pytest)...
"%PYTHON%" -m pip install -r requirements.txt >> "%LOG%" 2>&1 || goto :failed

echo [2/4] Installing @playwright/test...
pushd playwright
call npm install --no-audit --no-fund >> "%LOG%" 2>&1 || goto :failed

echo [3/4] Downloading Playwright browsers (Chromium, Firefox, WebKit)...
call npx playwright install chromium firefox webkit >> "%LOG%" 2>&1 || goto :failed
popd

echo [4/4] Running Selenium, Behave, Playwright, cross-browser and performance suites...
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_all.ps1
echo finished > reports\RUN_DONE.txt
echo.
echo Done. Results in reports\ and bonus\performance\. You can close this window.
pause
exit /b 0

:failed
echo FAILED - see reports\setup-log.txt
echo failed > reports\RUN_DONE.txt
pause
exit /b 1
