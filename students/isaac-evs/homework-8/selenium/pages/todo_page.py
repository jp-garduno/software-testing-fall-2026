"""Page Object for the TodoMVC React app, driven with Selenium and explicit waits."""

import os
import re

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# The assignment points at /examples/react/, which now answers 404; the app lives under /dist/.
BASE_URL = os.environ.get("TODOMVC_URL", "https://todomvc.com/examples/react/dist/")
DEFAULT_TIMEOUT = 10


class TodoPage:  # pylint: disable=too-many-public-methods  # a page object exposes every user action
    """Everything a test may do with, or ask of, the TodoMVC page."""

    NEW_TODO_INPUT = (By.CSS_SELECTOR, ".new-todo")
    TODO_ITEMS = (By.CSS_SELECTOR, ".todo-list li")
    COMPLETED_ITEMS = (By.CSS_SELECTOR, ".todo-list li.completed")
    TOGGLE_ALL = (By.CSS_SELECTOR, ".toggle-all")
    CLEAR_COMPLETED = (By.CSS_SELECTOR, ".clear-completed")
    FOOTER = (By.CSS_SELECTOR, ".footer")
    ITEMS_LEFT = (By.CSS_SELECTOR, ".todo-count")
    SELECTED_FILTER = (By.CSS_SELECTOR, ".filters a.selected")
    FILTER_ALL = (By.CSS_SELECTOR, ".filters a[href='#/']")
    FILTER_ACTIVE = (By.CSS_SELECTOR, ".filters a[href='#/active']")
    FILTER_COMPLETED = (By.CSS_SELECTOR, ".filters a[href='#/completed']")

    def __init__(self, driver, timeout=DEFAULT_TIMEOUT):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    # ---- navigation -------------------------------------------------------------------------

    def navigate(self, route=""):
        """Open the app (optionally at a route such as '#/active') and wait for the input."""
        self.driver.get(BASE_URL + route)
        self.wait.until(EC.visibility_of_element_located(self.NEW_TODO_INPUT))

    def open_clean(self):
        """Open the app with empty browser storage so no test sees another test's tasks."""
        self.navigate()
        self.driver.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")
        self.navigate()

    # ---- helpers ----------------------------------------------------------------------------

    def _items(self):
        return self.driver.find_elements(*self.TODO_ITEMS)

    def _item(self, index):
        items = self._items()
        if not -len(items) <= index < len(items):
            raise IndexError(f"No todo at index {index}; the list has {len(items)} item(s)")
        return items[index]

    def _until(self, condition, message, timeout=None):
        return WebDriverWait(self.driver, timeout or self.timeout).until(lambda _: condition(), message)

    # ---- creating ---------------------------------------------------------------------------

    def add_todo(self, text):
        """Type a task and press Enter. Waits for the new row only when one is expected."""
        before = self.get_todo_count()
        field = self.driver.find_element(*self.NEW_TODO_INPUT)
        field.send_keys(text, Keys.ENTER)
        if text.strip():
            self._until(lambda: self.get_todo_count() == before + 1, f"'{text}' never appeared in the list")

    def add_todos(self, *texts):
        """Add several tasks in order."""
        for text in texts:
            self.add_todo(text)

    # ---- reading ----------------------------------------------------------------------------

    def get_todo_count(self):
        """Number of rows currently shown (respects the active filter)."""
        return len(self._items())

    def get_visible_todos(self):
        """Task texts in the order shown."""
        return [item.find_element(By.CSS_SELECTOR, "label").get_attribute("textContent") for item in self._items()]

    def is_completed(self, index):
        """True when the row carries the 'completed' class."""
        return "completed" in self._item(index).get_attribute("class").split()

    def is_editing(self, index):
        """True while the row is in edit mode."""
        return "editing" in self._item(index).get_attribute("class").split()

    def get_edit_value(self, index):
        """Current contents of the row's edit field."""
        return self._item(index).find_element(By.CSS_SELECTOR, ".edit").get_attribute("value")

    def get_items_left(self):
        """The number in the 'N items left!' counter."""
        text = self.driver.find_element(*self.ITEMS_LEFT).get_attribute("textContent")
        return int(re.search(r"\d+", text).group())

    def is_footer_visible(self):
        """True when the footer (counter and filters) is displayed."""
        return self.driver.find_element(*self.FOOTER).is_displayed()

    def is_clear_completed_visible(self):
        """True when the 'Clear completed' button is displayed."""
        return self.driver.find_element(*self.CLEAR_COMPLETED).is_displayed()

    def get_selected_filter(self):
        """Label of the highlighted filter link: All, Active or Completed."""
        return self.driver.find_element(*self.SELECTED_FILTER).get_attribute("textContent")

    def get_route(self):
        """The URL hash, e.g. '#/active'."""
        return self.driver.execute_script("return window.location.hash;")

    # ---- completing -------------------------------------------------------------------------

    def toggle_todo(self, index):
        """Click a row's checkbox and wait until its state flips (or the row leaves the view)."""
        item = self._item(index)
        was_completed = self.is_completed(index)
        count = self.get_todo_count()
        item.find_element(By.CSS_SELECTOR, ".toggle").click()
        self._until(
            lambda: self.get_todo_count() != count or self.is_completed(index) != was_completed,
            f"Todo {index} did not change state",
        )

    def toggle_all(self):
        """Click the 'toggle all' checkbox (the visible chevron is a label the input sits over)."""
        self.driver.find_element(*self.TOGGLE_ALL).click()

    # ---- deleting ---------------------------------------------------------------------------

    def delete_todo(self, index):
        """Hover a row to reveal its delete button, click it, wait for the row to go."""
        item = self._item(index)
        count = self.get_todo_count()
        ActionChains(self.driver).move_to_element(item).perform()
        self.wait.until(EC.element_to_be_clickable(item.find_element(By.CSS_SELECTOR, ".destroy"))).click()
        self._until(lambda: self.get_todo_count() == count - 1, f"Todo {index} was not removed")

    def clear_completed(self):
        """Press 'Clear completed' and wait until no completed row is left."""
        self.wait.until(EC.element_to_be_clickable(self.CLEAR_COMPLETED)).click()
        self._until(lambda: not self.driver.find_elements(*self.COMPLETED_ITEMS), "Completed tasks were not cleared")

    # ---- editing ----------------------------------------------------------------------------

    def start_edit(self, index):
        """Double-click a task's label to enter edit mode."""
        label = self._item(index).find_element(By.CSS_SELECTOR, "label")
        ActionChains(self.driver).double_click(label).perform()
        self._until(lambda: self.is_editing(index), f"Todo {index} did not enter edit mode")

    def type_in_edit(self, index, text):
        """Replace the contents of the row's edit field."""
        field = self._item(index).find_element(By.CSS_SELECTOR, ".edit")
        # Not field.clear(): Selenium blurs the field afterwards and the app saves on blur,
        # so the emptied value would be committed (and the task deleted) before the new text is typed.
        field.send_keys(Keys.END, Keys.BACKSPACE * len(field.get_attribute("value")), text)

    def save_edit(self, index):
        """Confirm the edit with Enter and wait for edit mode to end."""
        self._item(index).find_element(By.CSS_SELECTOR, ".edit").send_keys(Keys.ENTER)
        self._until(lambda: self._edit_ended(index), "Edit mode did not end after Enter")

    def blur_edit(self, index):
        """Leave the edit field by clicking elsewhere (the app saves on blur)."""
        self.driver.find_element(*self.NEW_TODO_INPUT).click()
        self._until(lambda: self._edit_ended(index), "Edit mode did not end after blur")

    def edit_todo(self, index, new_text):
        """Edit a task's text and save it with Enter."""
        self.start_edit(index)
        self.type_in_edit(index, new_text)
        self.save_edit(index)

    def cancel_edit(self, index):
        """Press Escape in the row's edit field. Returns without waiting; callers assert the outcome."""
        self._item(index).find_element(By.CSS_SELECTOR, ".edit").send_keys(Keys.ESCAPE)

    def wait_until_not_editing(self, index, timeout=2):
        """Wait for the row to leave edit mode; True if it did, False on timeout."""
        try:
            self._until(lambda: self._edit_ended(index), "still editing", timeout=timeout)
            return True
        except TimeoutException:
            return False

    def _edit_ended(self, index):
        items = self._items()
        return index >= len(items) or "editing" not in items[index].get_attribute("class").split()

    # ---- filtering --------------------------------------------------------------------------

    def _filter(self, locator, name):
        self.driver.find_element(*locator).click()
        self._until(lambda: self.get_selected_filter() == name, f"Filter {name} was not selected")

    def filter_all(self):
        """Show all tasks."""
        self._filter(self.FILTER_ALL, "All")

    def filter_active(self):
        """Show only tasks that are not completed."""
        self._filter(self.FILTER_ACTIVE, "Active")

    def filter_completed(self):
        """Show only completed tasks."""
        self._filter(self.FILTER_COMPLETED, "Completed")
