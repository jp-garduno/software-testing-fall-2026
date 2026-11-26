"""Page Object for the TodoMVC React application.

Tests never touch locators or waits directly. Every action method returns only
after its effect is visible in the DOM, so callers can assert immediately.
"""
import os

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_URL = "https://todomvc.com/examples/react/dist/"


class TodoPage:
    # Locators
    NEW_TODO_INPUT = (By.CLASS_NAME, "new-todo")
    TODO_ITEMS = (By.CSS_SELECTOR, ".todo-list li")
    ITEM_LABEL = (By.CSS_SELECTOR, "label")
    ITEM_TOGGLE = (By.CSS_SELECTOR, ".toggle")
    ITEM_DESTROY = (By.CSS_SELECTOR, ".destroy")
    EDIT_INPUT = (By.CSS_SELECTOR, ".todo-list li .edit")
    TITLE = (By.CSS_SELECTOR, ".header h1")
    TODO_COUNT = (By.CLASS_NAME, "todo-count")
    TOGGLE_ALL = (By.CLASS_NAME, "toggle-all")
    CLEAR_COMPLETED = (By.CLASS_NAME, "clear-completed")
    SELECTED_FILTER = (By.CSS_SELECTOR, ".filters a.selected")
    FILTER_ALL = (By.CSS_SELECTOR, "a[href='#/']")
    FILTER_ACTIVE = (By.CSS_SELECTOR, "a[href='#/active']")
    FILTER_COMPLETED = (By.CSS_SELECTOR, "a[href='#/completed']")

    def __init__(self, driver, base_url=None, timeout=10):
        self.driver = driver
        self.base_url = base_url or os.getenv("TODO_URL", DEFAULT_URL)
        self.wait = WebDriverWait(
            driver, timeout, poll_frequency=0.05,
            ignored_exceptions=[StaleElementReferenceException],
        )

    # Navigation

    def navigate(self):
        self.driver.get(self.base_url)
        self.wait.until(EC.visibility_of_element_located(self.NEW_TODO_INPUT))

    # Creation

    def add_todo(self, text):
        """Type a todo and press Enter. Blank text is ignored by the app."""
        field = self.wait.until(EC.element_to_be_clickable(self.NEW_TODO_INPUT))
        field.send_keys(text, Keys.ENTER)
        if text.strip():
            self.wait.until(lambda _: field.get_attribute("value") == "")

    def add_todos(self, *texts):
        for text in texts:
            self.add_todo(text)

    # Queries

    def get_todo_count(self):
        """Return the number of todo items currently displayed."""
        return len(self.get_visible_todos())

    def get_visible_todos(self):
        """Return the texts of the displayed todos, in order."""
        def read_labels(driver):
            texts = [
                item.find_element(*self.ITEM_LABEL).get_attribute("textContent")
                for item in driver.find_elements(*self.TODO_ITEMS)
                if item.is_displayed()
            ]
            # Wrapped in a tuple so that an empty list does not count as "keep waiting".
            return (texts,)

        return self.wait.until(read_labels)[0]

    def is_completed(self, index):
        """True when the item is both checked and styled as completed."""
        item = self._item(index)
        checked = item.find_element(*self.ITEM_TOGGLE).is_selected()
        styled = "completed" in item.get_attribute("class").split()
        return checked and styled

    def get_items_left_text(self):
        return self.wait.until(EC.visibility_of_element_located(self.TODO_COUNT)).text

    def get_active_count(self):
        """Number shown in the footer, e.g. 2 for '2 items left!'."""
        return int(self.get_items_left_text().split()[0])

    def is_footer_visible(self):
        return self._is_displayed(self.TODO_COUNT)

    def is_clear_completed_visible(self):
        return self._is_displayed(self.CLEAR_COMPLETED)

    def get_selected_filter(self):
        return self.wait.until(EC.visibility_of_element_located(self.SELECTED_FILTER)).text

    # Completion

    def toggle_todo(self, index):
        """Toggle completion of the item at `index` among the displayed items."""
        checkbox = self._item(index).find_element(*self.ITEM_TOGGLE)
        was_checked = checkbox.is_selected()
        checkbox.click()

        def state_changed(_):
            try:
                return checkbox.is_selected() != was_checked
            except StaleElementReferenceException:
                return True  # a filtered view removed the item

        self.wait.until(state_changed)

    def toggle_all(self):
        checkbox = self.wait.until(EC.presence_of_element_located(self.TOGGLE_ALL))
        was_checked = checkbox.is_selected()
        checkbox.click()
        self.wait.until(lambda driver: driver.find_element(*self.TOGGLE_ALL).is_selected() != was_checked)

    # Deletion

    def delete_todo(self, index):
        """Hover the item so the delete button appears, then click it."""
        item = self._item(index)
        ActionChains(self.driver).move_to_element(item).perform()
        button = item.find_element(*self.ITEM_DESTROY)
        self.wait.until(EC.element_to_be_clickable(button)).click()
        self.wait.until(EC.staleness_of(item))

    def clear_completed(self):
        self.wait.until(EC.element_to_be_clickable(self.CLEAR_COMPLETED)).click()
        self.wait.until(EC.invisibility_of_element_located(self.CLEAR_COMPLETED))

    # Editing

    def start_edit(self, index):
        label = self._item(index).find_element(*self.ITEM_LABEL)
        ActionChains(self.driver).double_click(label).perform()
        self.wait.until(EC.visibility_of_element_located(self.EDIT_INPUT))

    def type_edit(self, text):
        """Replace the content of the open edit field without committing it.

        WebElement.clear() is deliberately avoided: it removes focus, which this
        app treats as "save", and saving an empty value deletes the todo.
        """
        field = self.wait.until(EC.visibility_of_element_located(self.EDIT_INPUT))
        self.driver.execute_script("arguments[0].select()", field)
        field.send_keys(text or Keys.BACKSPACE)

    def save_edit(self):
        """Commit the open edit with Enter."""
        self.driver.find_element(*self.EDIT_INPUT).send_keys(Keys.ENTER)
        self._wait_until_not_editing()

    def save_edit_by_blur(self):
        """Commit the open edit by clicking outside the field."""
        self.driver.find_element(*self.TITLE).click()
        self._wait_until_not_editing()

    def cancel_edit(self):
        """Press Escape. Does not wait: tests check whether the editor closed."""
        self.driver.find_element(*self.EDIT_INPUT).send_keys(Keys.ESCAPE)

    def edit_todo(self, index, text):
        self.start_edit(index)
        self.type_edit(text)
        self.save_edit()

    def is_editing(self):
        return self._is_displayed(self.EDIT_INPUT)

    # Filtering

    def filter_all(self):
        self._apply_filter(self.FILTER_ALL)

    def filter_active(self):
        """Show only active todos."""
        self._apply_filter(self.FILTER_ACTIVE)

    def filter_completed(self):
        """Show only completed todos."""
        self._apply_filter(self.FILTER_COMPLETED)

    # Helpers

    def _apply_filter(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()
        self.wait.until(lambda driver: "selected" in driver.find_element(*locator).get_attribute("class"))

    def _item(self, index):
        def nth_item(driver):
            items = driver.find_elements(*self.TODO_ITEMS)
            return items[index] if len(items) > index else False

        return self.wait.until(nth_item, message=f"no todo at index {index}")

    def _is_displayed(self, locator):
        elements = self.driver.find_elements(*locator)
        return bool(elements) and elements[0].is_displayed()

    def _wait_until_not_editing(self):
        self.wait.until(EC.invisibility_of_element_located(self.EDIT_INPUT))
