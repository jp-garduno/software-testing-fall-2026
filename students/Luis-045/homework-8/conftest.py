"""Selenium fixtures, screenshots and timings for the comparison report."""

import importlib.metadata
import json
import os
import platform
import time
from pathlib import Path

import pytest
from browser import create_driver
from pages.todo_page import DEFAULT_URL, TodoPage

ROOT = Path(__file__).resolve().parent
RUN = {"tests": {}, "browser_start_seconds": []}


def pytest_sessionstart(session):
    """Measure the full pytest session, including browser setup and cleanup."""
    RUN["started"] = time.perf_counter()
    RUN["tests"].clear()
    RUN["browser_start_seconds"].clear()
    RUN["python"] = platform.python_version()
    RUN["selenium"] = importlib.metadata.version("selenium")
    RUN["pytest"] = pytest.__version__
    RUN["root"] = str(session.config.rootpath)


@pytest.fixture
def todo_page(request):
    """Give every test a new Chrome profile and save its final visible state."""
    started = time.perf_counter()
    driver = create_driver()
    RUN["browser_start_seconds"].append(time.perf_counter() - started)
    RUN["browser"] = driver.capabilities["browserVersion"]
    page = TodoPage(driver)
    try:
        page.navigate()
        RUN["url"] = driver.current_url
        yield page
    finally:
        try:
            screenshot = ROOT / "screenshots" / f"selenium-{request.node.name}.png"
            screenshot.parent.mkdir(exist_ok=True)
            driver.save_screenshot(str(screenshot))
        finally:
            driver.quit()


def pytest_runtest_logreport(report):
    """Collect setup, body and teardown outcomes without changing pytest's result."""
    test = RUN["tests"].setdefault(report.nodeid, {"name": report.nodeid})
    test[report.when] = {
        "seconds": report.duration,
        "outcome": report.outcome,
    }
    if hasattr(report, "wasxfail"):
        test[report.when]["expected_failure"] = report.wasxfail
    if report.failed:
        test[report.when]["error"] = report.longreprtext


def pytest_sessionfinish(session, exitstatus):
    """Persist actual results even when the suite fails."""
    tests = list(RUN["tests"].values())
    for test in tests:
        outcomes = [
            stage["outcome"] for stage in test.values() if isinstance(stage, dict)
        ]
        expected_failure = any(
            stage.get("expected_failure")
            for stage in test.values()
            if isinstance(stage, dict)
        )
        if "failed" in outcomes:
            test["outcome"] = "failed"
        elif expected_failure and "skipped" in outcomes:
            test["outcome"] = "xfailed"
        else:
            test["outcome"] = "skipped" if "skipped" in outcomes else "passed"
    duration = time.perf_counter() - RUN["started"]
    setup = sum(test.get("setup", {}).get("seconds", 0) for test in tests)
    result = {
        "framework": "selenium",
        "exit_code": int(exitstatus),
        "total_seconds": duration,
        "average_per_test_seconds": duration / len(tests) if tests else 0,
        "average_setup_seconds": setup / len(tests) if tests else 0,
        "versions": {
            name: RUN.get(name) for name in ("python", "selenium", "pytest", "browser")
        },
        "platform": platform.platform(),
        "url": RUN.get("url", DEFAULT_URL),
        "workers": 1,
        "collected": session.testscollected,
        "tests": tests,
        "passed": sum(test["outcome"] == "passed" for test in tests),
        "failed": sum(test["outcome"] == "failed" for test in tests),
        "expected_failures": sum(test["outcome"] == "xfailed" for test in tests),
    }
    report_dir = ROOT / "reports"
    report_dir.mkdir(exist_ok=True)
    filename = os.getenv("SELENIUM_REPORT_NAME", "selenium-results.json")
    (report_dir / filename).write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
