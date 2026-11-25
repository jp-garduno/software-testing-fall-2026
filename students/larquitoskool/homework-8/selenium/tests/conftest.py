import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.todo_page import TodoPage


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,800")

    web_driver = webdriver.Chrome(options=options)
    yield web_driver
    web_driver.quit()


@pytest.fixture
def todo_page(driver):
    page = TodoPage(driver)
    page.navigate()
    return page