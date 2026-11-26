"""Isolated browser fixtures, evidence capture and measured suite results."""

import json
import os
from time import perf_counter

import pytest
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from playwright.sync_api import sync_playwright

from support import (
    ROOT,
    BASE_URL,
    STATS,
    SESSION_STARTED,
    page_type,
    chrome_launch_options,
)


@pytest.fixture(scope="session")
def selenium_driver():
    """Launch a disposable headless Chrome profile using Selenium Manager."""
    started = perf_counter()
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")
    if os.environ.get("CHROME_BINARY"):
        options.binary_location = os.environ["CHROME_BINARY"]
    driver = WebDriver(options=options)
    driver.set_page_load_timeout(30)
    STATS["setup"]["selenium"] = {
        "seconds": perf_counter() - started,
        "version": driver.capabilities["browserVersion"],
    }
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def playwright_browser():
    """Launch the same installed Chrome used by Selenium for a fair comparison."""
    started = perf_counter()
    with sync_playwright() as runtime:
        browser = runtime.chromium.launch(**chrome_launch_options(), headless=True)
        STATS["setup"]["playwright"] = {
            "seconds": perf_counter() - started,
            "version": browser.version,
        }
        yield browser
        browser.close()


@pytest.fixture
def todo(request):
    """Give every case clean storage and persist screenshots for key states."""
    engine = "selenium" if "selenium/tests" in request.node.nodeid else "playwright"
    context = None
    if engine == "selenium":
        adapter = page_type(engine)(request.getfixturevalue("selenium_driver"))
    else:
        browser = request.getfixturevalue("playwright_browser")
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        adapter = page_type(engine)(context.new_page())
    try:
        adapter.navigate()
        STATS["operations"].append(
            {
                "engine": engine,
                "operation": "page_load",
                "seconds": adapter.page_load_seconds(),
                "success": True,
            }
        )
        yield adapter
    finally:
        if request.node.name in {
            "test_create_single",
            "test_complete_single",
            "test_filter_completed",
            "test_cancel_edit",
        }:
            destination = ROOT / "screenshots" / f"{engine}-{request.node.name}.png"
            destination.parent.mkdir(exist_ok=True)
            adapter.screenshot(destination)
        if context:
            context.close()


def pytest_runtest_logreport(report):
    """Save pytest's real setup/call/teardown timing and outcomes."""
    engine = "selenium" if "selenium/tests" in report.nodeid else "playwright"
    STATS["tests"].append(
        {
            "engine": engine,
            "test": report.nodeid,
            "phase": report.when,
            "seconds": report.duration,
            "outcome": report.outcome,
        }
    )


def pytest_sessionfinish(session, exitstatus):
    """Write separate per-framework results without fabricating timings."""
    del session
    destination = ROOT / "reports"
    destination.mkdir(exist_ok=True)
    for engine, setup in STATS["setup"].items():
        result = {
            "url": BASE_URL,
            "exit_status": exitstatus,
            "browser_setup": setup,
            "suite_seconds": perf_counter() - SESSION_STARTED,
            "tests": [row for row in STATS["tests"] if row["engine"] == engine],
            "operations": [
                row for row in STATS["operations"] if row["engine"] == engine
            ],
        }
        (destination / f"{engine}_metrics.json").write_text(
            json.dumps(result, indent=2) + "\n", encoding="utf-8"
        )
