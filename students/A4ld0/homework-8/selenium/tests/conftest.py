"""Keep browser state isolated and collect evidence from actual executions."""

import json
from pathlib import Path
from time import perf_counter

import pytest

from pages.browser import create_driver
from pages.todo_page import TodoPage

ROOT = Path(__file__).resolve().parents[2]
RECORDS = []


@pytest.fixture
def todo(request):
    start = perf_counter()
    driver = None
    page = None
    setup = None
    startup = None
    try:
        driver = create_driver()
        page = TodoPage(driver)
        page.navigate()
        setup = page.metrics[0]["milliseconds"] / 1000
        startup = perf_counter() - start
        yield page
    finally:
        folder = ROOT / "screenshots"
        folder.mkdir(exist_ok=True)
        RECORDS.append({
            "test": request.node.nodeid,
            "setup_seconds": setup,
            "startup_seconds": startup,
            "operations": page.metrics if page else [],
        })
        if driver is not None:
            try:
                driver.save_screenshot(str(folder / f"selenium-{request.node.name}.png"))
            finally:
                driver.quit()


def pytest_sessionstart(session):
    session.config._homework_started = perf_counter()


def pytest_sessionfinish(session, exitstatus):
    folder = ROOT / "reports"
    folder.mkdir(exist_ok=True)
    reporter = session.config.pluginmanager.get_plugin("terminalreporter")
    stats = reporter.stats if reporter else {}
    report = {
        "total_seconds": perf_counter() - session.config._homework_started,
        "exit_status": int(exitstatus),
        "passed": len(stats.get("passed", [])),
        "failed": len(stats.get("failed", [])),
        "errors": len(stats.get("error", [])),
        "tests": RECORDS,
    }
    (folder / "selenium-metrics.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8")

