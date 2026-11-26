import sys
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "selenium"))


def before_scenario(context, scenario):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    context.driver = webdriver.Chrome(options=options)

    from pages.todo_page import TodoPage

    context.todo_page = TodoPage(context.driver)
    context.todo_page.navigate()
    context.driver.execute_script("window.localStorage.clear()")
    context.driver.refresh()
    context.todo_page.wait.until(
        lambda driver: driver.find_element(*TodoPage.NEW_TODO_INPUT)
    )


def after_scenario(context, scenario):
    driver = getattr(context, "driver", None)
    if driver is not None:
        driver.quit()
