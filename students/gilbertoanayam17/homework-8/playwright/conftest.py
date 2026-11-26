"""Fixtures for the Playwright suite.

pytest-playwright already gives every test a `page` in its own browser context, opened from one
browser that the whole session shares.
"""

import os
import sys
from pathlib import Path

import pytest
from pages.todo_page import TodoPage

SCREENSHOTS = Path(__file__).resolve().parent.parent / "screenshots" / "playwright"


def window_visible():
    """Same rule as selenium/firefox_driver.py: a window unless HEADLESS=1, CI or no Linux display."""
    if os.environ.get("HEADLESS") == "1" or os.environ.get("CI"):
        return False
    if sys.platform.startswith("linux"):
        return bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))
    return True


@pytest.fixture(name="browser_type_launch_args", scope="session")
def fixture_browser_type_launch_args(browser_type_launch_args):
    """pytest-playwright runs headless unless --headed is passed. Here the window shows by default."""
    headless = browser_type_launch_args.get("headless", not window_visible())
    return {**browser_type_launch_args, "headless": headless}


@pytest.fixture(name="browser_context_args", scope="session")
def fixture_browser_context_args(browser_context_args):
    """Same window size as the Selenium suite (below the breakpoint where the sidebar moves the app)."""
    return {**browser_context_args, "viewport": {"width": 800, "height": 900}}


@pytest.fixture(name="todo_page")
def fixture_todo_page(page, request):
    """The app freshly loaded. After the test, its final state is saved to screenshots/playwright/."""
    todo_page = TodoPage(page)
    todo_page.navigate()
    yield todo_page
    page.screenshot(path=SCREENSHOTS / f"{request.node.originalname}.png")
