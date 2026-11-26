"""Populate the reports using real test-run metrics."""

import json
import re
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parent


def load(filename):
    file = ROOT / "reports" / filename
    return json.loads(file.read_text(encoding="utf-8")) if file.exists() else None


def number(value):
    return f"{value:.3f}" if value is not None else "Pending"


def average(values):
    return mean(values) if values else None


def update(filename, marker, content):
    file = ROOT / filename
    text = file.read_text(encoding="utf-8")
    pattern = f"(<!-- {marker}_START -->).*?(<!-- {marker}_END -->)"
    text = re.sub(pattern, lambda m: f"{m[1]}\n{content}\n{m[2]}",
                  text, flags=re.DOTALL)
    file.write_text(text, encoding="utf-8")


def summary(report, tests, passed):
    if report is None:
        return ["Pending"] * 4
    total = report["total_seconds"]
    setup = average([test["setup_seconds"] for test in tests
                     if test.get("setup_seconds") is not None])
    return [number(total), number(total / len(tests) if tests else None),
            number(setup), f"{passed} / {len(tests)}"]


def rows_for_operation(tests, name):
    return [operation["milliseconds"] for test in tests
            for operation in test.get("operations", [])
            if operation["operation"] == name]


def main():
    selenium = load("selenium-metrics.json")
    playwright = load("playwright-metrics.json")
    cross_browser = load("playwright-cross-browser.json")
    selenium_tests = selenium["tests"] if selenium else []
    chrome_tests = [test for test in (playwright or {}).get("tests", [])
                    if test["browser"] == "chrome"]
    # Only a Chrome-only run has a comparable total duration.
    chrome_only = playwright if playwright and len(chrome_tests) == len(
        playwright["tests"]) else None

    metrics = ["Total execution time (s)", "Average elapsed time per test (s)",
               "Average setup time (s)", "Passed / attempted"]
    se = summary(selenium, selenium_tests, (selenium or {}).get("passed", 0))
    pw = summary(chrome_only, chrome_tests,
                 sum(test["status"] == "passed" for test in chrome_tests))
    lines = ["| Metric | Selenium | Playwright (Chrome) |", "|---|---|---|"]
    lines.extend(f"| {label} | {a} | {b} |"
                 for label, a, b in zip(metrics, se, pw))
    lines.append("\nSetup measures navigation until the task input is ready. "
                 "The comparison requires 15 attempted cases per framework "
                 "and a single-worker Chrome run.")
    update("COMPARISON_REPORT.md", "METRICS", "\n".join(lines))

    lines = ["| Operation | Selenium mean (ms) | Playwright Chrome mean (ms) |",
             "|---|---:|---:|"]
    for operation in ("page_load", "add", "toggle", "delete", "clear_completed",
                      "filter", "edit", "cancel_edit"):
        se_mean = average(rows_for_operation(selenium_tests, operation))
        pw_mean = average(rows_for_operation(chrome_tests, operation))
        lines.append(f"| {operation} | {number(se_mean)} | {number(pw_mean)} |")
    update("PERFORMANCE_REPORT.md", "PERFORMANCE", "\n".join(lines))

    lines = ["| Browser | Cases configured | Passed | Failed | Status |",
             "|---|---:|---:|---:|---|"]
    failure_details = []
    for browser in ("chrome", "firefox", "webkit"):
        tests = [test for test in (cross_browser or {}).get("tests", [])
                 if test["browser"] == browser]
        if not tests:
            lines.append(f"| {browser} | 15 | Pending | Pending | Pending execution |")
            continue
        passed = sum(test["status"] == "passed" for test in tests)
        failed = sum(test["status"] in ("failed", "timedOut", "interrupted")
                     for test in tests)
        status = "Passed" if passed == 15 else "Review results"
        lines.append(f"| {browser} | 15 | {passed} | {failed} | {status} |")
        failures = [test["test"] for test in tests
                    if test["status"] not in ("passed", "skipped")]
        if failures:
            failure_details.append(f"{browser} failures: " + ", ".join(failures))
    update("PERFORMANCE_REPORT.md", "BROWSER",
           "\n".join(lines + [""] + failure_details))


if __name__ == "__main__":
    main()

