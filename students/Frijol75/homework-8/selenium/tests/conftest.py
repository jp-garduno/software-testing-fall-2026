"""
Pytest fixtures for Selenium TodoMVC E2E test suite.
"""

import os
import sys
import pytest
from selenium import webdriver

# Ensure selenium directory is on sys.path so `from pages.todo_page import TodoPage` works
SELENIUM_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SELENIUM_DIR not in sys.path:
    sys.path.insert(0, SELENIUM_DIR)

from pages.todo_page import TodoPage  # noqa: E402


@pytest.fixture
def driver():
    """Initialize and yield a configured Chrome WebDriver instance."""
    options = webdriver.ChromeOptions()
    if os.environ.get("HEADLESS", "true").lower() != "false":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,800")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(options=options)
    yield browser
    browser.quit()


@pytest.fixture
def todo_page(driver):
    """Navigate to TodoMVC and return an initialized TodoPage instance."""
    page = TodoPage(driver)
    page.navigate()
    return page

