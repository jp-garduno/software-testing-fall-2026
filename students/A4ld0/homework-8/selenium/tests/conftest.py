"""Keep browser state isolated and collect evidence from actual executions."""

import json
from pathlib import Path
from time import perf_counter

import pytest

from pages.browser import create_driver
from pages.todo_page import TodoPage

ROOT = Path(__file__).resolve().parents[2]
RECORDS = []
SESSION_START = pytest.StashKey[float]()


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
    session.config.stash[SESSION_START] = perf_counter()


def pytest_sessionfinish(session, exitstatus):
    folder = ROOT / "reports"
    folder.mkdir(exist_ok=True)
    reporter = session.config.pluginmanager.get_plugin("terminalreporter")
    stats = reporter.stats if reporter else {}
    selenium_ids = {record["test"] for record in RECORDS}
    report = {
        "total_seconds": perf_counter() - session.config.stash.get(SESSION_START, perf_counter()),
        "exit_status": int(exitstatus),
        "passed": sum(item.nodeid in selenium_ids for item in stats.get("passed", [])),
        "failed": sum(item.nodeid in selenium_ids for item in stats.get("failed", [])),
        "errors": sum(item.nodeid in selenium_ids for item in stats.get("error", [])),
        "tests": RECORDS,
    }
    (folder / "selenium-metrics.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8")
