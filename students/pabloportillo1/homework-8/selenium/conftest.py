from pathlib import Path

import pytest
from browser import create_driver
from pages.todo_page import TodoPage

FAILURE_SCREENSHOTS = Path(__file__).resolve().parent.parent / "artifacts" / "selenium"


@pytest.fixture(scope="session", name="driver")
def fixture_driver():
    browser = create_driver()
    yield browser
    browser.quit()


@pytest.fixture(name="todo_page")
def fixture_todo_page(driver):
    page = TodoPage(driver)
    page.navigate()
    return page


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed and "todo_page" in item.funcargs:
        FAILURE_SCREENSHOTS.mkdir(parents=True, exist_ok=True)
        item.funcargs["todo_page"].driver.save_screenshot(str(FAILURE_SCREENSHOTS / f"{item.name}.png"))
