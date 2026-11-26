"""TodoMVC page object: selectors, actions and explicit synchronization."""

import os

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TodoPage:
    """Expose the user vocabulary without leaking selectors into tests."""

    NEW_TODO_INPUT = (By.CSS_SELECTOR, ".new-todo")
    TODO_ITEMS = (By.CSS_SELECTOR, ".todo-list li")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(
            driver, 10, ignored_exceptions=(StaleElementReferenceException,)
        )

    def navigate(self):
        """Load the real React app in a clean browser profile."""
        self.driver.get(
            os.getenv("TODO_URL", "https://todomvc.com/examples/react/dist/")
        )
        self.wait.until(EC.visibility_of_element_located(self.NEW_TODO_INPUT))

    def get_visible_todos(self):
        """Read only visible labels, excluding editor and button text."""
        return [item.find_element(By.TAG_NAME, "label").text for item in self._items()]

    def _items(self):
        return [
            item
            for item in self.driver.find_elements(*self.TODO_ITEMS)
            if item.is_displayed()
        ]

    def get_todo_count(self):
        """Count visible tasks in the current filter."""
        return len(self._items())

    def wait_for_todos(self, texts):
        """Wait for exact content and order, including empty results."""
        self.wait.until(lambda _: self.get_visible_todos() == texts)

    def add_todo(self, text):
        """Submit text and wait for the resulting list."""
        before = self.get_visible_todos()
        self.driver.find_element(*self.NEW_TODO_INPUT).send_keys(text, Keys.ENTER)
        self.wait_for_todos(before + [text.strip()] if text.strip() else before)

    def is_completed(self, index):
        """Read the task checkbox state."""
        return (
            self._items()[index].find_element(By.CSS_SELECTOR, ".toggle").is_selected()
        )

    def toggle_todo(self, index):
        """Toggle a task and synchronize with the updated checkbox."""
        expected = not self.is_completed(index)
        self._items()[index].find_element(By.CSS_SELECTOR, ".toggle").click()
        self.wait.until(lambda _: self.is_completed(index) == expected)

    def complete_all(self):
        """Click the visible toggle-all input."""
        self.driver.find_element(By.CSS_SELECTOR, ".toggle-all").click()
        self.wait.until(
            lambda _: all(self.is_completed(i) for i in range(self.get_todo_count()))
        )

    def active_count(self):
        """Read the count displayed by the application."""
        return int(
            self.driver.find_element(By.CSS_SELECTOR, ".todo-count").text.split()[0]
        )

    def delete_todo(self, index):
        """Hover to reveal delete, then wait for that row to disappear."""
        before = self.get_visible_todos()
        item = self._items()[index]
        ActionChains(self.driver).move_to_element(item).perform()
        item.find_element(By.CSS_SELECTOR, ".destroy").click()
        self.wait_for_todos(before[:index] + before[index + 1 :])

    def clear_completed(self):
        """Remove completed tasks while preserving active tasks."""
        active = [
            text
            for i, text in enumerate(self.get_visible_todos())
            if not self.is_completed(i)
        ]
        self.driver.find_element(By.CSS_SELECTOR, ".clear-completed").click()
        self.wait_for_todos(active)

    def filter_by(self, name):
        """Select a named filter and wait for its selected state."""
        link = self.driver.find_element(By.LINK_TEXT, name)
        link.click()
        self.wait.until(lambda _: "selected" in link.get_attribute("class"))

    def edit_todo(self, index, text, save="enter"):
        """Edit a task; Enter/blur saves and Escape cancels."""
        before = self.get_visible_todos()
        ActionChains(self.driver).double_click(
            self._items()[index].find_element(By.TAG_NAME, "label")
        ).perform()
        editor = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "li.editing .edit"))
        )
        editor.send_keys(Keys.CONTROL, "a")
        editor.send_keys(Keys.BACKSPACE)
        editor.send_keys(text)
        if save == "blur":
            self.driver.find_element(*self.NEW_TODO_INPUT).click()
        else:
            editor.send_keys(Keys.ESCAPE if save == "cancel" else Keys.ENTER)
        self.wait.until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "li.editing .edit"))
        )
        if save != "cancel":
            before[index : index + 1] = [text.strip()] if text.strip() else []
        self.wait_for_todos(before)

    def reload(self):
        """Reload to verify localStorage persistence through the UI."""
        self.driver.refresh()
        self.wait.until(EC.visibility_of_element_located(self.NEW_TODO_INPUT))

    def screenshot(self, path):
        """Capture browser evidence."""
        self.driver.save_screenshot(str(path))
