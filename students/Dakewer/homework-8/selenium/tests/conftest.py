import os
import re
from pathlib import Path

import pytest

from pages.browser import create_driver
from pages.todo_page import TodoPage

FAILURE_DIR = Path(__file__).resolve().parents[2] / "reports" / "selenium-failures"


def driver_scope(**_kwargs):
    """One browser per test by default; SELENIUM_DRIVER_SCOPE=session reuses it."""
    return os.getenv("SELENIUM_DRIVER_SCOPE", "function")


@pytest.fixture(scope=driver_scope, name="driver")
def fixture_driver():
    browser = create_driver()
    yield browser
    browser.quit()


@pytest.fixture(name="todo_page")
def fixture_todo_page(driver):
    # The app keeps todos in memory only, so loading the page resets all data.
    page = TodoPage(driver)
    page.navigate()
    return page


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """Save a screenshot whenever a test body fails."""
    outcome = yield
    report = outcome.get_result()
    driver = item.funcargs.get("driver")
    if report.when == "call" and report.failed and driver:
        FAILURE_DIR.mkdir(parents=True, exist_ok=True)
        name = re.sub(r"[^\w-]+", "_", item.name)
        driver.save_screenshot(str(FAILURE_DIR / f"{name}.png"))
