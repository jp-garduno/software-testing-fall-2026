"""Page Object for the TodoMVC React application (Selenium)."""

import os

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# The URL in the assignment (/examples/react/) answers 404; the app is served from dist/.
DEFAULT_URL = "https://todomvc.com/examples/react/dist/"


class TodoPage:
    """Actions and queries available on the todo list screen."""

    NEW_TODO_INPUT = (By.CLASS_NAME, "new-todo")
    TODO_ITEMS = (By.CSS_SELECTOR, ".todo-list li")
    ITEM_LABELS = (By.CSS_SELECTOR, ".todo-list li label")
    COMPLETED_ITEMS = (By.CSS_SELECTOR, ".todo-list li.completed")
    ITEM_TOGGLE = (By.CSS_SELECTOR, ".toggle")
    ITEM_LABEL = (By.TAG_NAME, "label")
    ITEM_DESTROY = (By.CSS_SELECTOR, ".destroy")
    ITEM_EDIT_INPUT = (By.CSS_SELECTOR, "input.edit")
    TOGGLE_ALL = (By.CLASS_NAME, "toggle-all")
    TODO_COUNTER = (By.CLASS_NAME, "todo-count")
    CLEAR_COMPLETED = (By.CLASS_NAME, "clear-completed")
    HEADING = (By.TAG_NAME, "h1")
    SELECTED_FILTER = (By.CSS_SELECTOR, ".filters a.selected")
    FILTER_ALL = (By.CSS_SELECTOR, "a[href='#/']")
    FILTER_ACTIVE = (By.CSS_SELECTOR, "a[href='#/active']")
    FILTER_COMPLETED = (By.CSS_SELECTOR, "a[href='#/completed']")

    def __init__(self, driver, url=None, timeout=10):
        self.driver = driver
        self.url = url or os.environ.get("TODO_URL", DEFAULT_URL)
        self.wait = WebDriverWait(driver, timeout)

    # Navigation

    def navigate(self):
        """Open the application and wait until it accepts input."""
        self.driver.get(self.url)
        self.wait.until(EC.element_to_be_clickable(self.NEW_TODO_INPUT))

    # Actions

    def add_todo(self, text):
        """Type a todo and press Enter. Blank text is ignored by the application."""
        field = self.driver.find_element(*self.NEW_TODO_INPUT)
        field.send_keys(text, Keys.ENTER)
        if text.strip():
            self.wait.until(lambda _: field.get_attribute("value") == "")

    def add_todos(self, *texts):
        for text in texts:
            self.add_todo(text)

    def toggle_todo(self, index):
        """Flip the completion checkbox of the visible todo at ``index``."""
        item = self._item(index)
        checkbox = item.find_element(*self.ITEM_TOGGLE)
        was_checked = checkbox.is_selected()
        checkbox.click()
        # Under a filter the item leaves the list, which also means the click landed.
        self.wait.until(EC.any_of(EC.staleness_of(item), lambda _: checkbox.is_selected() != was_checked))

    def toggle_all(self):
        self.driver.find_element(*self.TOGGLE_ALL).click()

    def delete_todo(self, index):
        """Hover the todo to reveal its destroy button, then click it."""
        item = self._item(index)
        ActionChains(self.driver).move_to_element(item).perform()
        button = item.find_element(*self.ITEM_DESTROY)
        self.wait.until(EC.visibility_of(button))
        button.click()
        self.wait.until(EC.staleness_of(item))

    def start_edit(self, index):
        """Double click a todo label and return its edit field."""
        item = self._item(index)
        ActionChains(self.driver).double_click(item.find_element(*self.ITEM_LABEL)).perform()
        return self.wait.until(lambda _: item.find_element(*self.ITEM_EDIT_INPUT))

    def type_in_edit(self, index, text):
        """Replace the content of an open edit field without submitting it."""
        field = self._item(index).find_element(*self.ITEM_EDIT_INPUT)
        # WebElement.clear() blurs the field, which would save (and delete) the todo.
        self.driver.execute_script("arguments[0].select()", field)
        field.send_keys(text if text else Keys.BACKSPACE)

    def press_enter_in_edit(self, index):
        self._item(index).find_element(*self.ITEM_EDIT_INPUT).send_keys(Keys.ENTER)

    def press_escape_in_edit(self, index):
        self._item(index).find_element(*self.ITEM_EDIT_INPUT).send_keys(Keys.ESCAPE)

    def blur_edit(self):
        """Move focus away from the edit field by clicking the page heading."""
        self.driver.find_element(*self.HEADING).click()
        self.wait.until(lambda d: not d.find_elements(*self.ITEM_EDIT_INPUT))

    def edit_todo(self, index, new_text):
        """Edit a todo and save it with Enter."""
        self.start_edit(index)
        self.type_in_edit(index, new_text)
        self.press_enter_in_edit(index)
        self.wait.until(lambda d: not d.find_elements(*self.ITEM_EDIT_INPUT))

    def filter_all(self):
        self._apply_filter(self.FILTER_ALL, "All")

    def filter_active(self):
        self._apply_filter(self.FILTER_ACTIVE, "Active")

    def filter_completed(self):
        self._apply_filter(self.FILTER_COMPLETED, "Completed")

    def clear_completed(self):
        self.wait.until(EC.element_to_be_clickable(self.CLEAR_COMPLETED)).click()
        self.wait.until(lambda d: not d.find_elements(*self.COMPLETED_ITEMS))

    # Queries

    def get_todo_count(self):
        """Number of todos currently rendered (depends on the active filter)."""
        return len(self.driver.find_elements(*self.TODO_ITEMS))

    def get_visible_todos(self):
        return [label.text for label in self.driver.find_elements(*self.ITEM_LABELS)]

    def is_completed(self, index):
        return "completed" in self._item(index).get_attribute("class").split()

    def is_editing(self, index):
        return bool(self._item(index).find_elements(*self.ITEM_EDIT_INPUT))

    def get_active_count(self):
        """Number shown by the "N items left!" counter (0 while the footer is hidden)."""
        text = self.driver.find_element(*self.TODO_COUNTER).get_attribute("textContent")
        return int(text.split()[0])

    def get_counter_text(self):
        return self.driver.find_element(*self.TODO_COUNTER).text

    def get_selected_filter(self):
        return self.driver.find_element(*self.SELECTED_FILTER).text

    def is_footer_visible(self):
        return self.driver.find_element(*self.TODO_COUNTER).is_displayed()

    def is_clear_completed_visible(self):
        return self.driver.find_element(*self.CLEAR_COMPLETED).is_displayed()

    # Helpers

    def _item(self, index):
        self.wait.until(lambda d: len(d.find_elements(*self.TODO_ITEMS)) > index)
        return self.driver.find_elements(*self.TODO_ITEMS)[index]

    def _apply_filter(self, locator, name):
        self.wait.until(EC.element_to_be_clickable(locator)).click()
        self.wait.until(lambda _: self.get_selected_filter() == name)
