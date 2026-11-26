"""Page object for the React TodoMVC application."""

import os
from time import perf_counter

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TodoPage:
    URL = os.getenv("TODO_URL", "https://todomvc.com/examples/react/")
    NEW_TODO = (By.CSS_SELECTOR, ".new-todo")
    ITEMS = (By.CSS_SELECTOR, ".todo-list li")
    CLEAR = (By.CSS_SELECTOR, ".clear-completed")
    COUNT = (By.CSS_SELECTOR, ".todo-count")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.metrics = []

    def navigate(self):
        start = perf_counter()
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.NEW_TODO))
        self._record("page_load", start)

    def _record(self, operation, start):
        self.metrics.append({
            "operation": operation,
            "milliseconds": (perf_counter() - start) * 1000,
        })

    def _items(self):
        return self.driver.find_elements(*self.ITEMS)

    def _item(self, index):
        return self.wait.until(lambda _: self._items()[index]
                               if len(self._items()) > index else False)

    def get_todo_count(self):
        return len(self._items())

    def get_visible_todos(self):
        return [item.find_element(By.CSS_SELECTOR, "label").text
                for item in self._items() if item.is_displayed()]

    def add_todo(self, text):
        start = perf_counter()
        count = self.get_todo_count()
        field = self.wait.until(EC.element_to_be_clickable(self.NEW_TODO))
        field.send_keys(text, Keys.ENTER)
        self.wait.until(lambda _: self.get_todo_count() == count + 1)
        self._record("add", start)

    def is_completed(self, index):
        return "completed" in (self._item(index).get_attribute("class") or "").split()

    def toggle_todo(self, index):
        start = perf_counter()
        previous = self.is_completed(index)
        toggle = self._item(index).find_element(By.CSS_SELECTOR, ".toggle")
        toggle.click()
        self.wait.until(lambda _: self.is_completed(index) != previous)
        self._record("toggle", start)

    def delete_todo(self, index):
        start = perf_counter()
        count = self.get_todo_count()
        item = self._item(index)
        ActionChains(self.driver).move_to_element(item).perform()
        self.wait.until(lambda _: item.find_element(
            By.CSS_SELECTOR, ".destroy").is_displayed())
        item.find_element(By.CSS_SELECTOR, ".destroy").click()
        self.wait.until(lambda _: self.get_todo_count() == count - 1)
        self._record("delete", start)

    def clear_completed(self):
        start = perf_counter()
        remaining = sum(not self.is_completed(i) for i in range(self.get_todo_count()))
        self.wait.until(EC.element_to_be_clickable(self.CLEAR)).click()
        self.wait.until(lambda _: self.get_todo_count() == remaining)
        self._record("clear_completed", start)

    def filter_by(self, name):
        start = perf_counter()
        target = {"All": "#/", "Active": "#/active", "Completed": "#/completed"}[name]
        locator = (By.CSS_SELECTOR, f'a[href="{target}"]')
        self.wait.until(EC.element_to_be_clickable(locator)).click()
        self.wait.until(lambda _: "selected" in (
            self.driver.find_element(*locator).get_attribute("class") or "").split())
        self._record("filter", start)

    def filter_active(self):
        self.filter_by("Active")

    def filter_completed(self):
        self.filter_by("Completed")

    def active_count(self):
        counter = self.wait.until(EC.visibility_of_element_located(self.COUNT))
        return int(counter.text.split()[0])

    def edit_todo(self, index, text, *, save=True):
        start = perf_counter()
        item = self._item(index)
        original = item.find_element(By.CSS_SELECTOR, "label").text
        ActionChains(self.driver).double_click(
            item.find_element(By.CSS_SELECTOR, "label")).perform()
        editor = self.wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, ".todo-list li .edit")))
        editor.send_keys(Keys.CONTROL, "a")
        editor.send_keys(text, Keys.ENTER if save else Keys.ESCAPE)
        expected = text if save else original
        self.wait.until(lambda _: self._item(index).find_element(
            By.CSS_SELECTOR, "label").text == expected)
        self._record("edit" if save else "cancel_edit", start)

