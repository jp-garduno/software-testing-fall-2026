import sys

from browser import APP_URL

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

SELECT_ALL_MODIFIER = Keys.COMMAND if sys.platform == "darwin" else Keys.CONTROL


class TodoPage:
    """Page object for the TodoMVC React app; every action waits for the change it causes."""

    NEW_TODO_INPUT = (By.CSS_SELECTOR, "input.new-todo")
    TODO_ITEMS = (By.CSS_SELECTOR, ".todo-list li")
    TODO_LABEL = (By.CSS_SELECTOR, "label")
    TOGGLE = (By.CSS_SELECTOR, "input.toggle")
    DESTROY = (By.CSS_SELECTOR, "button.destroy")
    EDIT_INPUT = (By.CSS_SELECTOR, ".todo-list li.editing input.edit")
    EDITING_ITEMS = (By.CSS_SELECTOR, ".todo-list li.editing")
    COMPLETED_ITEMS = (By.CSS_SELECTOR, ".todo-list li.completed")
    TOGGLE_ALL = (By.CSS_SELECTOR, "input.toggle-all")
    TODO_COUNT = (By.CSS_SELECTOR, ".todo-count")
    CLEAR_COMPLETED = (By.CSS_SELECTOR, "button.clear-completed")
    SELECTED_FILTER = (By.CSS_SELECTOR, ".filters a.selected")
    FILTERS = {
        "All": (By.CSS_SELECTOR, ".filters a[href='#/']"),
        "Active": (By.CSS_SELECTOR, ".filters a[href='#/active']"),
        "Completed": (By.CSS_SELECTOR, ".filters a[href='#/completed']"),
    }

    def __init__(self, driver, url=APP_URL):
        self.driver = driver
        self.url = url
        self.wait = WebDriverWait(driver, 10)

    def navigate(self):
        """Load a fresh copy of the app; the blank page first forces a reload even if only the #/ route differs."""
        self.driver.get("about:blank")
        self.driver.get(self.url)
        self.wait.until(EC.visibility_of_element_located(self.NEW_TODO_INPUT))

    def add_todo(self, *texts):
        field = self.driver.find_element(*self.NEW_TODO_INPUT)
        for text in texts:
            field.send_keys(text, Keys.ENTER)
            if text.strip():
                self.wait.until(lambda _: field.get_attribute("value") == "")

    def toggle_todo(self, index):
        item = self._item(index)
        was_completed = self._is_completed(item)
        item.find_element(*self.TOGGLE).click()
        self.wait.until(lambda _: self._toggled_or_hidden(item, was_completed))

    def toggle_all(self):
        self.driver.find_element(*self.TOGGLE_ALL).click()

    def delete_todo(self, index):
        item = self._item(index)
        ActionChains(self.driver).move_to_element(item).perform()
        self.wait.until(EC.element_to_be_clickable(item.find_element(*self.DESTROY))).click()
        self.wait.until(EC.staleness_of(item))

    def clear_completed(self):
        self.driver.find_element(*self.CLEAR_COMPLETED).click()
        self.wait.until(lambda driver: not driver.find_elements(*self.COMPLETED_ITEMS))

    def open_editor(self, index):
        label = self._item(index).find_element(*self.TODO_LABEL)
        ActionChains(self.driver).double_click(label).perform()
        return self.wait.until(EC.visibility_of_element_located(self.EDIT_INPUT))

    def start_editing(self, index, text):
        """Replace the todo's text in its editor without confirming it.

        Select-all plus typing, not WebElement.clear(): WebDriver blurs the field after clearing, and this app
        saves on blur, so clear() would save an empty title and delete the todo.
        """
        editor = self.open_editor(index)
        ActionChains(self.driver).key_down(SELECT_ALL_MODIFIER).send_keys("a").key_up(SELECT_ALL_MODIFIER).perform()
        editor.send_keys(Keys.BACKSPACE, text)
        return editor

    def edit_todo(self, index, text):
        self.start_editing(index, text).send_keys(Keys.ENTER)
        self.wait.until(lambda driver: not driver.find_elements(*self.EDITING_ITEMS))

    def cancel_editing(self):
        self.driver.find_element(*self.EDIT_INPUT).send_keys(Keys.ESCAPE)

    def is_editing(self):
        return bool(self.driver.find_elements(*self.EDITING_ITEMS))

    def filter_by(self, name):
        link = self.driver.find_element(*self.FILTERS[name])
        link.click()
        self.wait.until(lambda _: "selected" in link.get_attribute("class"))

    def filter_active(self):
        self.filter_by("Active")

    def filter_completed(self):
        self.filter_by("Completed")

    def selected_filter(self):
        return self.driver.find_element(*self.SELECTED_FILTER).text

    def get_todo_count(self):
        return len(self.driver.find_elements(*self.TODO_ITEMS))

    def get_visible_todos(self):
        return [item.find_element(*self.TODO_LABEL).text for item in self.driver.find_elements(*self.TODO_ITEMS)]

    def is_todo_completed(self, index):
        return self._is_completed(self._item(index))

    def items_left_text(self):
        return self.driver.find_element(*self.TODO_COUNT).text

    def is_clear_completed_visible(self):
        return self.driver.find_element(*self.CLEAR_COMPLETED).is_displayed()

    def _item(self, index):
        return self.driver.find_elements(*self.TODO_ITEMS)[index]

    def _toggled_or_hidden(self, item, was_completed):
        try:
            return self._is_completed(item) != was_completed
        except StaleElementReferenceException:
            return True

    @staticmethod
    def _is_completed(item):
        return "completed" in item.get_attribute("class").split()
