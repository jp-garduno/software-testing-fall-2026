import pytest
from selenium import webdriver
from pages.todo_page import TodoPage

@pytest.fixture
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument("--headless=new")
    d = webdriver.Chrome(options=opts)
    yield d
    d.quit()

@pytest.fixture
def todo_page(driver):
    page = TodoPage(driver)
    page.navigate()
    return page
