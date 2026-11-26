"""Fixtures for the bonus tests (visual regression and performance), which reuse the Selenium page object."""

import pytest
from firefox_driver import start_firefox
from pages.todo_page import TodoPage


@pytest.fixture(name="driver", scope="session")
def fixture_driver():
    driver = start_firefox()
    yield driver
    driver.quit()


@pytest.fixture(name="todo_page")
def fixture_todo_page(driver):
    todo_page = TodoPage(driver)
    todo_page.navigate()
    return todo_page
