import pytest
from driver_factory import create_driver
from pages.todo_page import TodoPage


@pytest.fixture
def driver():
    """A fresh browser per test, so no test can see another test's todos."""
    web_driver = create_driver()
    yield web_driver
    web_driver.quit()


@pytest.fixture
def todo_page(driver):
    page = TodoPage(driver)
    page.navigate()
    return page
