"""Selenium Page Object for the official TodoMVC React application."""

import sys
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as conditions
from selenium.webdriver.support.ui import WebDriverWait

from support import BASE_URL, measured


class TodoPage:
    """Hide CSS selectors, synchronization and browser details from tests."""

    engine = "selenium"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def rows(self):
        """Return freshly located rows to avoid stale element caching."""
        return self.driver.find_elements(By.CSS_SELECTOR, ".todo-list li")

    @measured
    def navigate(self):
        """Clear this disposable profile's storage and open a clean application."""
        self.driver.get(BASE_URL)
        self.wait.until(
            conditions.visibility_of_element_located((By.CSS_SELECTOR, ".new-todo"))
        )
        self.driver.execute_script("window.localStorage.clear()")
        self.driver.refresh()
        self.wait.until(
            conditions.visibility_of_element_located((By.CSS_SELECTOR, ".new-todo"))
        )
        self.wait.until(lambda _: self.get_todo_count() == 0)

    @measured
    def add_todo(self, text):
        """Create a task and wait for its row to appear."""
        count = self.get_todo_count()
        self.driver.find_element(By.CSS_SELECTOR, ".new-todo").send_keys(
            text, Keys.ENTER
        )
        self.wait.until(lambda _: self.get_todo_count() == count + 1)

    def get_todo_count(self):
        """Count visible rows, respecting the selected filter."""
        return len(self.rows())

    def get_visible_todos(self):
        """Return task labels without unrelated controls or counter text."""
        return [row.find_element(By.CSS_SELECTOR, "label").text for row in self.rows()]

    def completed_states(self):
        """Expose the checked state of each visible task."""
        return [
            row.find_element(By.CSS_SELECTOR, ".toggle").is_selected()
            for row in self.rows()
        ]

    def active_count(self):
        """Read the application's active item counter."""
        return int(
            self.driver.find_element(By.CSS_SELECTOR, ".todo-count").text.split()[0]
        )

    @measured
    def toggle_todo(self, index):
        """Toggle a task and wait for the checkbox state to change."""
        before = self.completed_states()[index]
        self.rows()[index].find_element(By.CSS_SELECTOR, ".toggle").click()
        self.wait.until(lambda _: self.completed_states()[index] != before)

    @measured
    def delete_todo(self, index):
        """Reveal the hover-only delete control and remove the selected row."""
        count = self.get_todo_count()
        row = self.rows()[index]
        ActionChains(self.driver).move_to_element(row).perform()
        row.find_element(By.CSS_SELECTOR, ".destroy").click()
        self.wait.until(lambda _: self.get_todo_count() == count - 1)

    @measured
    def clear_completed(self):
        """Remove all completed tasks while retaining active tasks."""
        expected = self.completed_states().count(False)
        self.driver.find_element(By.CSS_SELECTOR, ".clear-completed").click()
        self.wait.until(lambda _: self.get_todo_count() == expected)

    @measured
    def filter_by(self, name):
        """Choose an application filter and wait for its selected indicator."""
        self.driver.find_element(By.LINK_TEXT, name).click()
        self.wait.until(
            lambda _: self.driver.find_element(
                By.CSS_SELECTOR, ".filters .selected"
            ).text
            == name
        )

    @measured
    def edit_todo(self, index, text, finish="enter"):
        """Edit through the UI and commit with Enter/blur or cancel with Escape."""
        row = self.rows()[index]
        ActionChains(self.driver).double_click(
            row.find_element(By.CSS_SELECTOR, "label")
        ).perform()
        editor = self.wait.until(
            conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, ".todo-list li.editing .edit")
            )
        )
        modifier = Keys.COMMAND if sys.platform == "darwin" else Keys.CONTROL
        editor.send_keys(modifier, "a", Keys.NULL, text)
        if finish == "blur":
            self.driver.find_element(By.CSS_SELECTOR, ".new-todo").click()
        else:
            editor.send_keys(Keys.ESCAPE if finish == "escape" else Keys.ENTER)
            if finish == "escape":
                self.driver.find_element(By.CSS_SELECTOR, ".new-todo").click()
        self.wait.until(
            conditions.invisibility_of_element_located(
                (By.CSS_SELECTOR, ".todo-list li.editing .edit")
            )
        )

    def assert_todos(self, expected):
        """Assert exact visible task order, using an explicit retry wait."""
        self.wait.until(lambda _: self.get_visible_todos() == expected)
        assert self.get_visible_todos() == expected

    @measured
    def reload(self):
        """Reload without clearing persistent data."""
        self.driver.refresh()
        self.wait.until(
            conditions.visibility_of_element_located((By.CSS_SELECTOR, ".new-todo"))
        )

    def screenshot(self, path):
        """Capture the real browser for execution evidence."""
        self.driver.save_screenshot(str(path))

    def page_load_seconds(self):
        """Read the browser's Navigation Timing duration for the latest load."""
        return self.driver.execute_script(
            "return performance.getEntriesByType('navigation')[0].loadEventEnd / 1000"
        )
