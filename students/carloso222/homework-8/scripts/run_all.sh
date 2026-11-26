#!/usr/bin/env bash
# Runs every suite of Homework 8 and writes the reports used by COMPARISON_REPORT.md.
# Usage (from the homework-8 folder):  ./scripts/run_all.sh [--skip-cross-browser] [--skip-perf]
# Uses $PYTHON if set, otherwise python3.
# Timed runs take no screenshots (they would add time); evidence runs take them.
set -u
cd "$(dirname "$0")/.."
ROOT="$PWD"
PYTHON="${PYTHON:-python3}"
SKIP_CROSS=0; SKIP_PERF=0
for arg in "$@"; do
  case "$arg" in
    --skip-cross-browser) SKIP_CROSS=1 ;;
    --skip-perf) SKIP_PERF=1 ;;
  esac
done
mkdir -p reports
export FORCE_COLOR=0 PY_COLORS=0
WALL="{"

step() {  # step <name> <command...>
  local name="$1"; shift
  echo; echo "=== $name ==="
  local start end took
  start=$(date +%s.%N)
  "$@"
  end=$(date +%s.%N)
  took=$(awk "BEGIN {printf \"%.2f\", $end - $start}")
  echo "$name took ${took} s"
  WALL="$WALL\"$name\": $took, "
}

# --- Selenium + BDD
export SAVE_SCREENSHOTS=0
step selenium bash -c "$PYTHON -m pytest --junitxml=reports/selenium-junit.xml 2>&1 | tee reports/selenium-output.txt"
export SAVE_SCREENSHOTS=1
step selenium_screenshots bash -c "$PYTHON -m pytest -q > /dev/null 2>&1"
step behave bash -c "$PYTHON -m behave --junit --junit-directory reports/behave-junit 2>&1 | tee reports/behave-output.txt"

# --- Playwright
cd playwright
[ -d node_modules ] || npm install --no-audit --no-fund
export SAVE_SCREENSHOTS=0 PW_OUTPUT_DIR=test-results/chromium
export PW_JSON_REPORT="$ROOT/reports/playwright-results.json"
step playwright bash -c "npx playwright test --project=chromium 2>&1 | tee ../reports/playwright-output.txt"
export PW_JSON_REPORT="$ROOT/reports/playwright-results-1worker.json" PW_WORKERS=1
step playwright_1worker bash -c "npx playwright test --project=chromium 2>&1 | tee ../reports/playwright-1worker-output.txt"
# Same browser binary as Selenium (the installed Google Chrome) for an apples-to-apples comparison.
export PW_JSON_REPORT="$ROOT/reports/playwright-results-chrome-1worker.json" PW_CHANNEL=chrome
step playwright_chrome_1worker bash -c "npx playwright test --project=chromium 2>&1 | tee ../reports/playwright-chrome-1worker-output.txt"
unset PW_WORKERS PW_CHANNEL
if [ "$SKIP_CROSS" -eq 0 ]; then
  export SAVE_SCREENSHOTS=1 PW_OUTPUT_DIR=test-results/cross-browser
  export PW_JSON_REPORT="$ROOT/reports/playwright-cross-browser.json"
  # 4 workers: with 8, three browsers starting at once overloaded the machine and Firefox timed out.
  step cross_browser bash -c "npx playwright test --project=chromium --project=firefox --project=webkit --workers=4 2>&1 | tee ../reports/cross-browser-output.txt"
  export SAVE_SCREENSHOTS=0
fi
if [ "$SKIP_PERF" -eq 0 ]; then
  export PW_CHANNEL=chrome PW_OUTPUT_DIR=test-results/perf  # Selenium also drives the installed Chrome
  export PW_JSON_REPORT="$ROOT/reports/playwright-perf.json"
  step perf_playwright bash -c "npx playwright test --project=perf 2>&1 | tee ../reports/perf-playwright-output.txt"
  unset PW_CHANNEL
fi
unset PW_JSON_REPORT PW_OUTPUT_DIR
cd "$ROOT"

# --- Bonus C: performance
if [ "$SKIP_PERF" -eq 0 ]; then
  step perf_selenium bash -c "$PYTHON bonus/performance/selenium_perf.py 2>&1 | tee reports/perf-selenium-output.txt"
  "$PYTHON" bonus/performance/generate_report.py
fi

echo "${WALL%, }}" > reports/wall-clock.json
"$PYTHON" scripts/summarize_timings.py
echo; echo "Done. See reports/timing-summary.md and bonus/performance/PERFORMANCE_REPORT.md"
