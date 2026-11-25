import pytest
from pages.todo_page import TodoPage

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(name="driver")
def chrome_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,800")

    web_driver = webdriver.Chrome(options=options)  # pylint: disable=not-callable
    yield web_driver
    web_driver.quit()


@pytest.fixture
def todo_page(driver):
    page = TodoPage(driver)
    page.navigate()
    return page
