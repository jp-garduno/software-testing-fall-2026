"""Pytest fixtures for the Selenium suite: one shared Chrome, a clean TodoMVC page per test."""

import os
from pathlib import Path

import pytest
from selenium import webdriver

from pages.todo_page import TodoPage

ARTIFACTS = Path(__file__).resolve().parent / "artifacts"


def _chrome_options():
    options = webdriver.ChromeOptions()
    if os.environ.get("HEADLESS", "1") != "0":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,900")
    if os.environ.get("CI"):
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    return options


@pytest.fixture(scope="session")
def driver():
    """A single Chrome for the whole run; tests isolate themselves by clearing browser storage."""
    browser = webdriver.Chrome(options=_chrome_options())
    yield browser
    browser.quit()


@pytest.fixture
def todo_page(driver, request):  # pylint: disable=redefined-outer-name
    """A TodoPage opened on an empty list. A failing test leaves a screenshot in artifacts/."""
    page = TodoPage(driver)
    page.open_clean()
    yield page
    report = getattr(request.node, "rep_call", None)
    if report is not None and report.failed:
        ARTIFACTS.mkdir(exist_ok=True)
        driver.save_screenshot(str(ARTIFACTS / f"{request.node.name}.png"))


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Expose each phase's report on the test item so fixtures can see whether the test failed."""
    outcome = yield
    setattr(item, f"rep_{call.when}", outcome.get_result())
