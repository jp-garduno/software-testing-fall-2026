"""Fixtures for the Selenium suite."""

from pathlib import Path

import pytest
from firefox_driver import start_firefox
from pages.todo_page import TodoPage

SCREENSHOTS = Path(__file__).resolve().parent.parent / "screenshots" / "selenium"


@pytest.fixture(name="driver", scope="session")
def fixture_driver():
    """One Firefox for the whole run, the same way Playwright shares one browser between tests.

    Sharing it does not couple the tests: the app keeps its todos in memory only, so the
    reload done by the todo_page fixture always starts from an empty list.
    """
    driver = start_firefox()
    yield driver
    driver.quit()


@pytest.fixture(name="todo_page")
def fixture_todo_page(driver, request):
    """The app freshly loaded. After the test, its final state is saved to screenshots/selenium/."""
    todo_page = TodoPage(driver)
    todo_page.navigate()
    yield todo_page
    SCREENSHOTS.mkdir(parents=True, exist_ok=True)
    driver.save_screenshot(str(SCREENSHOTS / f"{request.node.name}.png"))
