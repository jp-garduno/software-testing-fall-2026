"""Fresh browser per test, screenshots on failure, measurable fixture setup."""

from pathlib import Path
from time import perf_counter

import pytest

from pages.browser import create_driver
from pages.todo_page import TodoPage

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def todo(request):
    """Always close the browser, including when setup or assertions fail."""
    start = perf_counter()
    driver = create_driver()
    try:
        page = TodoPage(driver)
        page.navigate()
        request.node.user_properties.append(("setup_seconds", perf_counter() - start))
        yield page
        if request.node.name == "test_complete_all":
            folder = ROOT / "screenshots"
            folder.mkdir(exist_ok=True)
            page.screenshot(folder / "selenium-completed.png")
    finally:
        if getattr(request.node, "rep_call", None) and request.node.rep_call.failed:
            folder = ROOT / "reports/live/failures"
            folder.mkdir(parents=True, exist_ok=True)
            driver.save_screenshot(str(folder / f"{request.node.name}.png"))
        driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Expose the test outcome to teardown."""
    del call
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture
def mixed(todo):
    """Two active tasks surrounding one completed task."""
    for text in ["Task 1", "Task 2", "Task 3"]:
        todo.add_todo(text)
    todo.toggle_todo(1)
    return todo
