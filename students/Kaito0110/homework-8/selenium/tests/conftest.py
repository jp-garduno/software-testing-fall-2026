import sys
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pages.todo_page import TodoPage


@pytest.fixture
def todo_page():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    page = TodoPage(driver)
    try:
        page.navigate()
        driver.execute_script("window.localStorage.clear()")
        driver.refresh()
        page.wait.until(
            lambda current_driver: current_driver.find_element(*TodoPage.NEW_TODO_INPUT)
        )
        yield page
    finally:
        driver.quit()
