"""Fixtures for the Selenium suite.

One browser is shared by the whole session (starting Chrome is the slowest step), but every
test gets a freshly loaded page. The React example keeps todos in memory only, so reloading
the page is a complete reset and the tests stay independent of each other.
"""

from pathlib import Path

import pytest
from driver_factory import create_driver
from pages.todo_page import TodoPage

SCREENSHOT_DIR = Path(__file__).resolve().parents[2] / "screenshots" / "selenium-failures"


@pytest.fixture(name="driver", scope="session")
def fixture_driver():
    driver = create_driver()
    yield driver
    driver.quit()


@pytest.fixture(name="todo_page")
def fixture_todo_page(driver):
    """The todo app, freshly loaded with an empty list."""
    return TodoPage(driver).navigate()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):  # pylint: disable=unused-argument
    """Save a screenshot of the browser when a test fails, named after the test."""
    outcome = yield
    report = outcome.get_result()
    driver = item.funcargs.get("driver") if hasattr(item, "funcargs") else None
    if report.when == "call" and report.failed and driver is not None:
        SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        driver.save_screenshot(str(SCREENSHOT_DIR / f"{item.name}.png"))
