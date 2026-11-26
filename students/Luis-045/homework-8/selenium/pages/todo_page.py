"""TodoMVC interactions and explicit waits; assertions belong in the tests."""

import os

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_URL = "https://todomvc.com/examples/react/dist/"


class TodoPage:
    """Model the task list, filters, completion controls and inline editor."""

    NEW_TODO_INPUT = (By.CSS_SELECTOR, ".new-todo")
    TODO_ITEMS = (By.CSS_SELECTOR, ".todo-list li")
    EDIT_INPUT = (By.CSS_SELECTOR, ".todo-list .edit")
    CLEAR_COMPLETED = (By.CSS_SELECTOR, ".clear-completed")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(
            driver, 10, ignored_exceptions=(StaleElementReferenceException,)
        )

    def navigate(self):
        """Open the configured app and wait until it accepts input."""
        self.driver.get(os.getenv("TODO_BASE_URL", DEFAULT_URL))
        self.wait.until(EC.visibility_of_element_located(self.NEW_TODO_INPUT))

    def _visible_items(self):
        return [
            item
            for item in self.driver.find_elements(*self.TODO_ITEMS)
            if item.is_displayed()
        ]

    def _item(self, index):
        def find_item(_driver):
            items = self._visible_items()
            return items[index] if len(items) > index else False

        return self.wait.until(find_item)

    def get_visible_todos(self):
        """Return visible labels in their displayed order."""
        return [
            item.find_element(By.CSS_SELECTOR, "label").text
            for item in self._visible_items()
        ]

    def get_todo_count(self):
        """Count only tasks displayed by the current filter."""
        return len(self._visible_items())

    def wait_for_todos(self, expected):
        """Wait for a complete expected list, including an empty result."""
        self.wait.until(lambda _driver: self.get_visible_todos() == expected)

    def add_todo(self, text):
        """Submit an input; whitespace-only entries must not create a task."""
        previous = self.get_visible_todos()
        self.wait.until(EC.element_to_be_clickable(self.NEW_TODO_INPUT)).send_keys(
            text, Keys.ENTER
        )
        expected = previous + [text.strip()] if text.strip() else previous
        self.wait_for_todos(expected)

    def is_completed(self, index):
        """Read the checkbox state for a visible task."""
        return self._item(index).find_element(By.CSS_SELECTOR, ".toggle").is_selected()

    def toggle_todo(self, index):
        """Toggle a task while the All filter preserves its index."""
        was_completed = self.is_completed(index)
        self._item(index).find_element(By.CSS_SELECTOR, ".toggle").click()
        self.wait.until(lambda _driver: self.is_completed(index) != was_completed)

    def get_active_count(self):
        """Read the footer's remaining-task count."""
        return int(
            self.driver.find_element(By.CSS_SELECTOR, ".todo-count").text.split()[0]
        )

    def delete_todo(self, index):
        """Reveal a task's delete button and wait for the row to disappear."""
        before = self.get_todo_count()
        item = self._item(index)
        ActionChains(self.driver).move_to_element(item).perform()
        self.wait.until(
            EC.element_to_be_clickable(item.find_element(By.CSS_SELECTOR, ".destroy"))
        ).click()
        self.wait.until(lambda _driver: self.get_todo_count() == before - 1)

    def clear_completed(self):
        """Remove completed tasks without removing active tasks."""
        expected = [
            item.find_element(By.CSS_SELECTOR, "label").text
            for item in self._visible_items()
            if not item.find_element(By.CSS_SELECTOR, ".toggle").is_selected()
        ]
        self.wait.until(EC.element_to_be_clickable(self.CLEAR_COMPLETED)).click()
        self.wait_for_todos(expected)

    def filter_by(self, name):
        """Select All, Active or Completed and wait for the selected link."""
        link = self.driver.find_element(By.LINK_TEXT, name)
        link.click()
        self.wait.until(lambda _driver: "selected" in link.get_attribute("class"))

    def filter_all(self):
        """Display all tasks."""
        self.filter_by("All")

    def filter_active(self):
        """Display active tasks."""
        self.filter_by("Active")

    def filter_completed(self):
        """Display completed tasks."""
        self.filter_by("Completed")

    def begin_edit(self, index):
        """Open the inline editor by double-clicking a task label."""
        label = self._item(index).find_element(By.CSS_SELECTOR, "label")
        ActionChains(self.driver).double_click(label).perform()
        self.wait.until(EC.visibility_of_element_located(self.EDIT_INPUT))

    def replace_edit_text(self, text):
        """Replace the draft without saving it."""
        editor = self.wait.until(EC.visibility_of_element_located(self.EDIT_INPUT))
        editor.send_keys(Keys.CONTROL, "a")
        editor.send_keys(Keys.BACKSPACE)
        editor.send_keys(text)

    def get_edit_text(self):
        """Read the current unsaved draft."""
        return self.wait.until(
            EC.visibility_of_element_located(self.EDIT_INPUT)
        ).get_attribute("value")

    def finish_edit(self, key=Keys.ENTER):
        """Save with Enter or cancel with Escape, then wait for the editor to close."""
        self.wait.until(EC.visibility_of_element_located(self.EDIT_INPUT)).send_keys(
            key
        )
        self.wait.until(EC.invisibility_of_element_located(self.EDIT_INPUT))

    def cancel_edit(self):
        """Discard the current draft."""
        self.finish_edit(Keys.ESCAPE)

    def blur_edit(self):
        """Save the draft by moving focus to the new-task input."""
        self.driver.find_element(*self.NEW_TODO_INPUT).click()
        self.wait.until(EC.invisibility_of_element_located(self.EDIT_INPUT))
