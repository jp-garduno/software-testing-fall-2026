"""Page Object Model (POM) for the TodoMVC React application (Selenium)."""

import time
from typing import Any, Dict, List

from todo_driver import By, Keys


class TodoPage:
    """Page Object encapsulating TodoMVC locators and user interactions."""

    URL = "https://todomvc.com/examples/react/dist/"

    # Locators
    NEW_TODO_INPUT = (By.CLASS_NAME, "new-todo")
    TODO_LIST = (By.CLASS_NAME, "todo-list")
    TODO_ITEMS = (By.CSS_SELECTOR, ".todo-list li")
    TOGGLE_ALL = (By.CLASS_NAME, "toggle-all")
    CLEAR_COMPLETED = (By.CLASS_NAME, "clear-completed")
    TODO_COUNT = (By.CLASS_NAME, "todo-count")
    FILTER_ALL = (By.CSS_SELECTOR, "a[href='#/']")
    FILTER_ACTIVE = (By.CSS_SELECTOR, "a[href='#/active']")
    FILTER_COMPLETED = (By.CSS_SELECTOR, "a[href='#/completed']")

    def __init__(self, driver: Any, timeout: int = 10):
        """Initialize the Page Object with a WebDriver instance."""
        self.driver = driver
        self.timeout = timeout
        self.metrics: List[Dict[str, Any]] = []

    def _record_metric(self, action: str, start_time: float) -> None:
        elapsed_ms = round((time.perf_counter() - start_time) * 1000.0, 4)
        self.metrics.append({"action": action, "duration_ms": elapsed_ms})

    def navigate(self) -> None:
        """Navigate to the TodoMVC React application."""
        start = time.perf_counter()
        self.driver.get(self.URL)
        self._record_metric("navigate", start)

    def add_todo(self, text: str) -> None:
        """Add a single todo item by typing text and pressing Enter."""
        start = time.perf_counter()
        input_el = self.driver.find_element(*self.NEW_TODO_INPUT)
        input_el.clear()
        input_el.send_keys(text + Keys.ENTER)
        self._record_metric("add_todo", start)

    def add_todos(self, texts: List[str]) -> None:
        """Add multiple todo items sequentially."""
        for text in texts:
            self.add_todo(text)

    def get_todo_elements(self) -> List[Any]:
        """Return all currently visible todo list item elements."""
        return self.driver.find_elements(*self.TODO_ITEMS)

    def get_todo_count(self) -> int:
        """Return the number of visible todo items."""
        return len(self.get_todo_elements())

    def get_active_count(self) -> int:
        """Parse and return the active items count from the footer counter."""
        elements = self.driver.find_elements(*self.TODO_COUNT)
        if not elements:
            return 0
        text = elements[0].text.strip()
        parts = text.split()
        return int(parts[0]) if parts and parts[0].isdigit() else 0

    def get_visible_todos(self) -> List[str]:
        """Return a list of text labels for all visible todo items."""
        return [el.text for el in self.get_todo_elements()]

    def toggle_todo(self, index: int) -> None:
        """Toggle the completion checkbox of the todo item at `index`."""
        start = time.perf_counter()
        items = self.get_todo_elements()
        if index < 0 or index >= len(items):
            raise IndexError(f"Todo index {index} out of range (0..{len(items) - 1})")
        checkbox = items[index].find_element(By.CSS_SELECTOR, ".toggle")
        checkbox.click()
        self._record_metric("toggle_todo", start)

    def toggle_all(self) -> None:
        """Toggle completion status of all todo items at once."""
        start = time.perf_counter()
        toggle_all_el = self.driver.find_element(*self.TOGGLE_ALL)
        toggle_all_el.click()
        self._record_metric("toggle_all", start)

    def is_todo_completed(self, index: int) -> bool:
        """Return True if the todo item at `index` has the 'completed' CSS class."""
        items = self.get_todo_elements()
        if index < 0 or index >= len(items):
            raise IndexError(f"Todo index {index} out of range")
        classes = items[index].get_attribute("class") or ""
        return "completed" in classes.split()

    def delete_todo(self, index: int) -> None:
        """Delete the todo item at `index` using its destroy button."""
        start = time.perf_counter()
        items = self.get_todo_elements()
        if index < 0 or index >= len(items):
            raise IndexError(f"Todo index {index} out of range")
        destroy_btn = items[index].find_element(By.CSS_SELECTOR, ".destroy")
        destroy_btn.click()
        self._record_metric("delete_todo", start)

    def clear_completed(self) -> None:
        """Click the 'Clear completed' button in the footer."""
        start = time.perf_counter()
        btn = self.driver.find_element(*self.CLEAR_COMPLETED)
        btn.click()
        self._record_metric("clear_completed", start)

    def edit_todo(self, index: int, new_text: str) -> None:
        """Double-click the todo at `index`, replace its text, and press Enter to save."""
        start = time.perf_counter()
        items = self.get_todo_elements()
        if index < 0 or index >= len(items):
            raise IndexError(f"Todo index {index} out of range")
        item = items[index]
        if hasattr(item, "double_click"):
            item.double_click()
        edit_input = item.find_element(By.CSS_SELECTOR, ".edit")
        edit_input.clear()
        edit_input.send_keys(new_text + Keys.ENTER)
        self._record_metric("edit_todo", start)

    def cancel_edit_todo(self, index: int, temporary_text: str) -> None:
        """Double-click the todo at `index`, type temporary text, and press Escape to cancel."""
        start = time.perf_counter()
        items = self.get_todo_elements()
        if index < 0 or index >= len(items):
            raise IndexError(f"Todo index {index} out of range")
        item = items[index]
        if hasattr(item, "double_click"):
            item.double_click()
        edit_input = item.find_element(By.CSS_SELECTOR, ".edit")
        edit_input.clear()
        edit_input.send_keys(temporary_text + Keys.ESCAPE)
        self._record_metric("cancel_edit_todo", start)

    def filter_all(self) -> None:
        """Select the 'All' filter tab."""
        start = time.perf_counter()
        self.driver.find_element(*self.FILTER_ALL).click()
        self._record_metric("filter_all", start)

    def filter_active(self) -> None:
        """Select the 'Active' filter tab."""
        start = time.perf_counter()
        self.driver.find_element(*self.FILTER_ACTIVE).click()
        self._record_metric("filter_active", start)

    def filter_completed(self) -> None:
        """Select the 'Completed' filter tab."""
        start = time.perf_counter()
        self.driver.find_element(*self.FILTER_COMPLETED).click()
        self._record_metric("filter_completed", start)

    def filter_by_name(self, filter_name: str) -> None:
        """Filter todos by display name ('All', 'Active', or 'Completed')."""
        normalized = filter_name.strip().lower()
        if normalized == "all":
            self.filter_all()
        elif normalized == "active":
            self.filter_active()
        elif normalized == "completed":
            self.filter_completed()
        else:
            raise ValueError(f"Unknown filter name: {filter_name}")

    def take_screenshot(self, filepath: str) -> bool:
        """Capture a screenshot of the current page state."""
        return bool(self.driver.save_screenshot(filepath))
