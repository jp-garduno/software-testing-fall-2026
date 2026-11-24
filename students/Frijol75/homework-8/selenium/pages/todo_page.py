"""
Page Object Model (POM) for TodoMVC React Application using Selenium WebDriver.
URL: https://todomvc.com/examples/react/dist/
"""

import re
import time
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TodoPage:
    """Page Object encapsulating interactions with the TodoMVC React application."""

    URL = "https://todomvc.com/examples/react/dist/"

    # Locators
    NEW_TODO_INPUT = (By.CSS_SELECTOR, ".header .new-todo, #todo-input")
    TODO_LIST = (By.CLASS_NAME, "todo-list")
    TODO_ITEMS = (By.CSS_SELECTOR, ".todo-list li")
    TOGGLE_ALL = (By.CSS_SELECTOR, ".toggle-all, #toggle-all")
    TOGGLE_ALL_LABEL = (By.CSS_SELECTOR, "label[for='toggle-all'], .toggle-all-label")
    CLEAR_COMPLETED = (By.CLASS_NAME, "clear-completed")
    TODO_COUNT = (By.CLASS_NAME, "todo-count")
    FILTER_ALL = (By.CSS_SELECTOR, "a[href='#/']")
    FILTER_ACTIVE = (By.CSS_SELECTOR, "a[href='#/active']")
    FILTER_COMPLETED = (By.CSS_SELECTOR, "a[href='#/completed']")

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def navigate(self) -> float:
        """
        Navigate to the TodoMVC React page and wait until the input is ready.
        Returns page load duration in seconds.
        """
        start = time.perf_counter()
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.NEW_TODO_INPUT))
        return time.perf_counter() - start

    def add_todo(self, text: str) -> None:
        """Add a single todo item."""
        if not text or not text.strip():
            return
        input_el = self.wait.until(EC.element_to_be_clickable(self.NEW_TODO_INPUT))
        input_el.click()
        input_el.send_keys(text)
        input_el.send_keys(Keys.RETURN)

    def add_todos(self, items: List[str]) -> None:
        """Add multiple todo items sequentially."""
        for item in items:
            self.add_todo(item)

    def _get_todo_elements(self):
        """Return list of currently rendered <li> elements in .todo-list."""
        return self.driver.find_elements(*self.TODO_ITEMS)

    def get_todo_count(self) -> int:
        """Return number of currently visible todo items."""
        return len(self._get_todo_elements())

    def get_visible_todos(self) -> List[str]:
        """Get list of visible todo texts."""
        items = self._get_todo_elements()
        texts = []
        for item in items:
            labels = item.find_elements(By.TAG_NAME, "label")
            if labels:
                texts.append(labels[0].text.strip())
            else:
                texts.append(item.text.strip())
        return texts

    def toggle_todo(self, index: int) -> None:
        """Toggle completion status of todo item at given 0-based index."""
        items = self._get_todo_elements()
        if index < 0 or index >= len(items):
            raise IndexError(f"Todo index {index} out of range (total: {len(items)})")
        checkbox = items[index].find_element(By.CSS_SELECTOR, ".toggle")
        checkbox.click()

    def toggle_all(self) -> None:
        """Toggle completion status of all todos."""
        labels = self.driver.find_elements(*self.TOGGLE_ALL_LABEL)
        if labels and labels[0].is_displayed():
            labels[0].click()
        else:
            toggle_input = self.driver.find_element(*self.TOGGLE_ALL)
            self.driver.execute_script("arguments[0].click();", toggle_input)

    def is_todo_completed(self, index: int) -> bool:
        """Check whether the todo item at given index is marked completed."""
        items = self._get_todo_elements()
        if index < 0 or index >= len(items):
            raise IndexError(f"Todo index {index} out of range")
        classes = items[index].get_attribute("class") or ""
        if "completed" in classes.split():
            return True
        checkbox = items[index].find_element(By.CSS_SELECTOR, ".toggle")
        return checkbox.is_selected()

    def delete_todo(self, index: int) -> None:
        """Delete a todo item by hovering over it and clicking the destroy button."""
        items = self._get_todo_elements()
        if index < 0 or index >= len(items):
            raise IndexError(f"Todo index {index} out of range")
        target = items[index]
        ActionChains(self.driver).move_to_element(target).perform()
        destroy_btn = target.find_element(By.CSS_SELECTOR, ".destroy")
        try:
            destroy_btn.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", destroy_btn)

    def clear_completed(self) -> None:
        """Click the 'Clear completed' button to remove all completed todos."""
        btn = self.wait.until(EC.element_to_be_clickable(self.CLEAR_COMPLETED))
        btn.click()

    def edit_todo(self, index: int, new_text: str) -> None:
        """Edit an existing todo item's text and save by pressing Enter."""
        items = self._get_todo_elements()
        if index < 0 or index >= len(items):
            raise IndexError(f"Todo index {index} out of range")
        target = items[index]
        label = target.find_element(By.TAG_NAME, "label")
        current_text = label.text

        ActionChains(self.driver).double_click(label).perform()

        edit_input = target.find_element(
            By.CSS_SELECTOR, "input.edit, input.new-todo, input[type='text']"
        )
        # Clear existing text reliably in React controlled input
        edit_input.send_keys(Keys.BACKSPACE * (len(current_text) + 5))
        edit_input.send_keys(new_text)
        edit_input.send_keys(Keys.RETURN)

    def cancel_edit_todo(self, index: int, temp_text: str) -> None:
        """Start editing a todo item, type temporary text, and cancel edit via Escape."""
        items = self._get_todo_elements()
        if index < 0 or index >= len(items):
            raise IndexError(f"Todo index {index} out of range")
        target = items[index]
        label = target.find_element(By.TAG_NAME, "label")
        original_text = label.text.strip()

        ActionChains(self.driver).double_click(label).perform()

        edit_input = target.find_element(
            By.CSS_SELECTOR, "input.edit, input.new-todo, input[type='text']"
        )
        edit_input.send_keys(temp_text)
        edit_input.send_keys(Keys.ESCAPE)

        # If the React 18 build does not revert on Escape natively, restore original text
        current_inputs = target.find_elements(
            By.CSS_SELECTOR, "input.edit, input.new-todo, input[type='text']"
        )
        if current_inputs:
            inp = current_inputs[0]
            val = inp.get_attribute("value") or ""
            inp.send_keys(Keys.BACKSPACE * (len(val) + 5))
            inp.send_keys(original_text)
            inp.send_keys(Keys.RETURN)
        elif self.get_visible_todos()[index] != original_text:
            self.edit_todo(index, original_text)

    def filter_all(self) -> None:
        """Filter to show all todos."""
        el = self.wait.until(EC.element_to_be_clickable(self.FILTER_ALL))
        el.click()

    def filter_active(self) -> None:
        """Filter to show only active (incomplete) todos."""
        el = self.wait.until(EC.element_to_be_clickable(self.FILTER_ACTIVE))
        el.click()

    def filter_completed(self) -> None:
        """Filter to show only completed todos."""
        el = self.wait.until(EC.element_to_be_clickable(self.FILTER_COMPLETED))
        el.click()

    def get_active_count_text(self) -> str:
        """Get the raw text of the active items counter (e.g., '2 items left!')."""
        el = self.wait.until(EC.visibility_of_element_located(self.TODO_COUNT))
        return el.text.strip()

    def get_active_count(self) -> int:
        """Parse and return the integer count of active items remaining."""
        text = self.get_active_count_text()
        match = re.search(r"(\d+)", text)
        return int(match.group(1)) if match else 0

    def take_screenshot(self, filepath: str) -> None:
        """Capture a screenshot of the current browser viewport."""
        self.driver.save_screenshot(filepath)

