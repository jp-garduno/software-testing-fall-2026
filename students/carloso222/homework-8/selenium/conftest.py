"""Pytest fixtures for the Selenium suite.

One browser is started per test session; every test gets a freshly loaded page, which is
enough for isolation because TodoMVC React keeps its todos in memory only.
"""

import json
import re
import time

import pytest
from pages.todo_page import TodoPage
from support import settings
from support.driver_factory import create_driver


@pytest.fixture(scope="session", name="driver")
def fixture_driver():
    start = time.perf_counter()
    drv = create_driver()
    setup_seconds = time.perf_counter() - start
    _write_setup_time(setup_seconds)
    yield drv
    drv.quit()


@pytest.fixture(name="todo_page")
def fixture_todo_page(driver, request):
    page = TodoPage(driver).reset()
    yield page
    failed = (
        getattr(request.node, "rep_call", None) is not None
        and request.node.rep_call.failed
    )
    if settings.SAVE_SCREENSHOTS or failed:
        name = re.sub(r"[^A-Za-z0-9_.-]+", "_", request.node.name)
        page.take_screenshot(settings.SCREENSHOTS_DIR / "selenium" / f"{name}.png")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):  # pylint: disable=unused-argument
    """Expose each phase's report on the test item so fixtures can see whether the test failed."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


def _write_setup_time(seconds: float) -> None:
    settings.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    data = {
        "browser": settings.BROWSER,
        "headless": settings.HEADLESS,
        "driver_start_seconds": round(seconds, 3),
    }
    (settings.REPORTS_DIR / "selenium-setup.json").write_text(
        json.dumps(data, indent=2), encoding="utf-8"
    )
