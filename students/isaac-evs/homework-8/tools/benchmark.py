"""Benchmark the Selenium and Playwright suites (same 41 scenarios, Chromium, headless, live site).

Usage (from homework-8/):  [BENCH_LABEL=local TODOMVC_URL=...] python tools/benchmark.py [runs]
-> benchmark/results-<label>.json (label defaults to 'live')

Per run it records the wall-clock time of the whole command (interpreter/Node start-up included) and the
time the test runner itself reports. Browser start-up is timed separately in its own fresh process.
"""

import json
import os
import statistics
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUNS = int(sys.argv[1]) if len(sys.argv) > 1 else 5
PYTHON = sys.executable

SELENIUM_STARTUP = """
import sys, time
sys.path.insert(0, "selenium")
t = time.perf_counter()
from conftest import _chrome_options
from selenium import webdriver
d = webdriver.Chrome(options=_chrome_options())
print(time.perf_counter() - t)
d.quit()
"""

PLAYWRIGHT_STARTUP = """
const { chromium } = require("@playwright/test");
(async () => {
  const t0 = performance.now();
  const browser = await chromium.launch();
  const t1 = performance.now();
  const context = await browser.newContext();
  const page = await context.newPage();
  const t2 = performance.now();
  console.log(JSON.stringify({ launch: (t1 - t0) / 1000, context_and_page: (t2 - t1) / 1000 }));
  await browser.close();
})();
"""


def timed(command, cwd):
    """Run a command, returning (wall seconds, completed process)."""
    start = time.perf_counter()
    process = subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=False)
    return time.perf_counter() - start, process


def selenium_run():
    junit = ROOT / "benchmark" / "selenium-junit.xml"
    wall, process = timed([PYTHON, "-m", "pytest", "-q", "-p", "no:cacheprovider", f"--junitxml={junit}"], ROOT)
    suite = ET.parse(junit).getroot().find("testsuite")
    cases = suite.findall("testcase")
    return {
        "wall": wall,
        "runner": float(suite.get("time")),
        "tests": len(cases),
        "failures": int(suite.get("failures")) + int(suite.get("errors")),
        "returncode": process.returncode,
        "durations": [float(case.get("time")) for case in cases],
    }


def playwright_run(workers):
    out = ROOT / "benchmark" / "playwright-report.json"
    command = ["npx", "playwright", "test", "--project=chromium", f"--workers={workers}", "--reporter=json"]
    wall, process = timed(command, ROOT / "playwright")
    out.write_text(process.stdout, encoding="utf-8")
    report = json.loads(process.stdout)
    durations = []

    def walk(suite):
        for spec in suite.get("specs", []):
            for test in spec["tests"]:
                durations.append(sum(result["duration"] for result in test["results"]) / 1000)
        for child in suite.get("suites", []):
            walk(child)

    for top in report["suites"]:
        walk(top)
    stats = report["stats"]
    return {
        "wall": wall,
        "runner": stats["duration"] / 1000,
        "tests": len(durations),
        "failures": stats["unexpected"] + stats["flaky"],
        "returncode": process.returncode,
        "durations": durations,
    }


def startup_times():
    selenium = []
    playwright = []
    for _ in range(RUNS):
        _, process = timed([PYTHON, "-c", SELENIUM_STARTUP], ROOT)
        selenium.append(float(process.stdout.strip().splitlines()[-1]))
        _, process = timed(["node", "-e", PLAYWRIGHT_STARTUP], ROOT / "playwright")
        playwright.append(json.loads(process.stdout.strip().splitlines()[-1]))
    return {"selenium_driver_and_browser": selenium, "playwright": playwright}


def summarize(runs):
    return {
        "median_wall": statistics.median(run["wall"] for run in runs),
        "median_runner": statistics.median(run["runner"] for run in runs),
        "tests": runs[0]["tests"],
        "failures_per_run": [run["failures"] for run in runs],
        "mean_per_test": statistics.mean(d for run in runs for d in run["durations"]),
        "median_per_test": statistics.median(d for run in runs for d in run["durations"]),
    }


def main():
    (ROOT / "benchmark").mkdir(exist_ok=True)
    runs = {"selenium": [], "playwright_parallel": [], "playwright_serial": []}
    for index in range(RUNS):
        print(f"run {index + 1}/{RUNS}", flush=True)
        runs["selenium"].append(selenium_run())
        runs["playwright_parallel"].append(playwright_run(workers=4))
        runs["playwright_serial"].append(playwright_run(workers=1))
    result = {
        "runs": RUNS,
        "summary": {name: summarize(value) for name, value in runs.items()},
        "raw_wall": {name: [run["wall"] for run in value] for name, value in runs.items()},
        "startup": startup_times(),
    }
    label = os.environ.get("BENCH_LABEL", "live")
    result["label"] = label
    result["url"] = os.environ.get("TODOMVC_URL", "https://todomvc.com/examples/react/dist/")
    (ROOT / "benchmark" / f"results-{label}.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], indent=2))


if __name__ == "__main__":
    main()
