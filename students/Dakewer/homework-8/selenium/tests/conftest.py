import os
import re
from pathlib import Path
from urllib.parse import urlparse

import pytest

from pages.browser import create_driver
from pages.todo_page import DEFAULT_URL, TodoPage

FAILURE_DIR = Path(__file__).resolve().parents[2] / "reports" / "selenium-failures"


def driver_scope(fixture_name, config):
    """One browser per test by default; SELENIUM_DRIVER_SCOPE=session reuses it."""
    return os.getenv("SELENIUM_DRIVER_SCOPE", "function")


@pytest.fixture(scope=driver_scope)
def driver():
    browser = create_driver()
    yield browser
    browser.quit()


@pytest.fixture
def todo_page(driver):
    # The app keeps todos in memory only, so loading the page resets all data.
    page = TodoPage(driver)
    page.navigate()
    return page


def is_local_build():
    host = urlparse(os.getenv("TODO_URL", DEFAULT_URL)).hostname
    return host in ("localhost", "127.0.0.1")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Save a screenshot whenever a test body fails."""
    outcome = yield
    report = outcome.get_result()
    driver = item.funcargs.get("driver")
    if report.when == "call" and report.failed and driver:
        FAILURE_DIR.mkdir(parents=True, exist_ok=True)
        name = re.sub(r"[^\w-]+", "_", item.name)
        driver.save_screenshot(str(FAILURE_DIR / f"{name}.png"))
