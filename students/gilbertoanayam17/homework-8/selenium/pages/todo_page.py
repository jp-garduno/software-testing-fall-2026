"""Page Object for TodoMVC React, driven with Selenium WebDriver.

Every action ends with an explicit wait for its visible effect, so the tests never sleep and never
read the page before React has re-rendered it.
"""

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# The URL in the assignment (/examples/react/) now answers 404. The React build is served from dist/.
APP_URL = "https://todomvc.com/examples/react/dist/"

SETTLE_FOR_SCREENSHOT = """
document.activeElement.blur();
const style = document.createElement("style");
style.textContent = "*, *::before, *::after { transition: none !important; animation: none !important; }";
document.head.appendChild(style);
"""


class TodoPage:
    """What a user can do and see on the todo list. Tests never touch a locator directly."""

    # Locators
    NEW_TODO_INPUT = (By.CLASS_NAME, "new-todo")
    TODO_LIST = (By.CLASS_NAME, "todo-list")
    TODO_ITEMS = (By.CSS_SELECTOR, ".todo-list li")
    TOGGLE_ALL = (By.CLASS_NAME, "toggle-all")
    CLEAR_COMPLETED = (By.CLASS_NAME, "clear-completed")
    FILTER_ALL = (By.CSS_SELECTOR, "a[href='#/']")
    FILTER_ACTIVE = (By.CSS_SELECTOR, "a[href='#/active']")
    FILTER_COMPLETED = (By.CSS_SELECTOR, "a[href='#/completed']")
    APP = (By.CLASS_NAME, "todoapp")
    HEADING = (By.CSS_SELECTOR, ".header h1")
    ITEM_COUNTER = (By.CLASS_NAME, "todo-count")
    ITEM_LABELS = (By.CSS_SELECTOR, ".todo-list li label")
    EDIT_INPUT = (By.CSS_SELECTOR, ".todo-list li input.edit")
    HOVERED = (By.CSS_SELECTOR, ".todo-list li:hover, .filters a:hover")
    # Searched inside one todo item
    TOGGLE = (By.CLASS_NAME, "toggle")
    LABEL = (By.TAG_NAME, "label")
    DESTROY = (By.CLASS_NAME, "destroy")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def navigate(self):
        """Load a fresh copy of the app. Todos only live in memory, so every load starts empty."""
        self.driver.get(APP_URL)
        self.wait.until(EC.element_to_be_clickable(self.NEW_TODO_INPUT))

    # ------------------------------------------------------------------ creating

    def add_todo(self, text):
        """Add a new todo item"""
        before = self.get_todo_count()
        self.driver.find_element(*self.NEW_TODO_INPUT).send_keys(text, Keys.ENTER)
        self.wait.until(lambda driver: len(driver.find_elements(*self.TODO_ITEMS)) == before + 1)

    def add_todos(self, *texts):
        """Add several todos in the given order."""
        for text in texts:
            self.add_todo(text)

    # ---------------------------------------------------------------- completing

    def toggle_todo(self, index):
        """Toggle todo completion status (meant for the All view, where the item stays in the list)."""
        item = self._item(index)
        was_completed = self._has_class(item, "completed")
        item.find_element(*self.TOGGLE).click()
        self.wait.until(lambda _: self._has_class(item, "completed") != was_completed)

    def is_completed(self, index):
        """True when the todo is shown as done (struck through)."""
        return self._has_class(self._item(index), "completed")

    # ------------------------------------------------------------------ deleting

    def delete_todo(self, index):
        """Delete a todo item"""
        item = self._item(index)
        # The destroy button is display:none until the pointer is over the item.
        ActionChains(self.driver).move_to_element(item).perform()
        self.wait.until(EC.visibility_of(item.find_element(*self.DESTROY))).click()
        self.wait.until(EC.staleness_of(item))

    def clear_completed(self):
        """Press "Clear completed" and wait for the button to hide again."""
        self.driver.find_element(*self.CLEAR_COMPLETED).click()
        self.wait.until(EC.invisibility_of_element_located(self.CLEAR_COMPLETED))

    # ------------------------------------------------------------------- editing

    def start_editing(self, index):
        """Double-click the todo text to open its edit field."""
        label = self._item(index).find_element(*self.LABEL)
        ActionChains(self.driver).double_click(label).perform()
        self.wait.until(EC.visibility_of_element_located(self.EDIT_INPUT))

    def type_edit(self, text):
        """Replace the text in the open edit field without saving it yet."""
        field = self.driver.find_element(*self.EDIT_INPUT)
        # Select and overwrite: WebElement.clear() blurs the field, and a blur saves the edit.
        field.send_keys(Keys.CONTROL, "a")
        field.send_keys(text)

    def confirm_edit(self):
        """Save the edit with Enter."""
        self.driver.find_element(*self.EDIT_INPUT).send_keys(Keys.ENTER)
        self.wait.until(EC.invisibility_of_element_located(self.EDIT_INPUT))

    def cancel_edit(self):
        """Press Escape, which the TodoMVC spec says discards the edit."""
        self.driver.find_element(*self.EDIT_INPUT).send_keys(Keys.ESCAPE)

    def leave_edit(self):
        """Click outside the edit field (on the heading) so it loses focus."""
        self.driver.find_element(*self.HEADING).click()
        self.wait.until(EC.invisibility_of_element_located(self.EDIT_INPUT))

    def is_editing(self, index):
        """True while the todo shows its edit field."""
        return self._has_class(self._item(index), "editing")

    # ----------------------------------------------------------------- filtering

    def filter_all(self):
        """Show all todos"""
        self._choose_filter(self.FILTER_ALL)

    def filter_active(self):
        """Show only active todos"""
        self._choose_filter(self.FILTER_ACTIVE)

    def filter_completed(self):
        """Show only completed todos"""
        self._choose_filter(self.FILTER_COMPLETED)

    # ------------------------------------------------------------------- reading

    def get_todo_count(self):
        """Return number of todo items"""
        return len(self.driver.find_elements(*self.TODO_ITEMS))

    def get_visible_todos(self):
        """Get list of visible todo texts"""
        return [label.text for label in self.driver.find_elements(*self.ITEM_LABELS)]

    def get_active_count(self):
        """The number in the "N items left!" counter."""
        # textContent instead of .text, which is empty while the footer is hidden.
        counter = self.driver.find_element(*self.ITEM_COUNTER).get_attribute("textContent")
        return int(counter.split()[0])

    def save_app_screenshot(self, path):
        """Save an image of the app alone, in a state that does not depend on timing or on the mouse.

        Before the capture, the focus is removed (no blinking caret), CSS transitions jump to their end
        (a completed todo fades to gray over 0.4 s), and the pointer rests on the heading, which is drawn
        above the captured box, so no hover effect is left (the delete button, a filter link border).
        """
        self.driver.execute_script(SETTLE_FOR_SCREENSHOT)
        # Two moves on purpose. ActionChains does not see where element.click() left the pointer, so a
        # single move to a spot it believes the pointer is already on sends no event and the hover stays.
        heading = self.driver.find_element(*self.HEADING)
        ActionChains(self.driver).move_to_element(heading).move_by_offset(1, 0).perform()
        self.wait.until(lambda driver: not driver.find_elements(*self.HOVERED))
        self.driver.find_element(*self.APP).screenshot(str(path))

    # ------------------------------------------------------------------- helpers

    def _item(self, index):
        locator = (By.CSS_SELECTOR, f".todo-list li:nth-child({index + 1})")
        return self.wait.until(EC.presence_of_element_located(locator))

    def _choose_filter(self, locator):
        link = self.wait.until(EC.element_to_be_clickable(locator))
        link.click()
        self.wait.until(lambda _: self._has_class(link, "selected"))

    @staticmethod
    def _has_class(element, name):
        return name in element.get_attribute("class").split()
