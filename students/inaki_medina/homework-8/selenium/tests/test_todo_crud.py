from uuid import uuid4

from selenium import webdriver
from selenium.webdriver.common.by import By

from pages.todo_page import TodoPage


def test_add_todo_increases_count():
    driver = webdriver.Chrome()
    try:
        page = TodoPage(driver)
        page.navigate()

        starting_count = page.get_todo_count()
        page.add_todo(f"Learn Selenium {uuid4().hex[:8]}")

        assert page.get_todo_count() == starting_count + 1
    finally:
        driver.quit()


def test_toggle_todo_completion():
    driver = webdriver.Chrome()
    try:
        page = TodoPage(driver)
        page.navigate()

        todo_index = page.get_todo_count()
        page.add_todo(f"Toggle todo {uuid4().hex[:8]}")
        todo_item = driver.find_elements(*TodoPage.TODO_ITEMS)[todo_index]
        checkbox = todo_item.find_element(By.CLASS_NAME, "toggle")
        assert not checkbox.is_selected()

        page.toggle_todo(todo_index)
        todo_item = driver.find_elements(*TodoPage.TODO_ITEMS)[todo_index]
        checkbox = todo_item.find_element(By.CLASS_NAME, "toggle")
        assert checkbox.is_selected()

        page.toggle_todo(todo_index)
        todo_item = driver.find_elements(*TodoPage.TODO_ITEMS)[todo_index]
        checkbox = todo_item.find_element(By.CLASS_NAME, "toggle")
        assert not checkbox.is_selected()
    finally:
        driver.quit()


def test_delete_todo():
    driver = webdriver.Chrome()
    try:
        page = TodoPage(driver)
        page.navigate()

        starting_count = page.get_todo_count()
        todo_index = starting_count
        page.add_todo(f"Delete todo {uuid4().hex[:8]}")

        page.delete_todo(todo_index)

        assert page.get_todo_count() == starting_count
    finally:
        driver.quit()