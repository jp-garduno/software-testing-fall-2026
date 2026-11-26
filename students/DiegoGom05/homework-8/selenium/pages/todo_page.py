from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TodoPage:
    # Locators
    NEW_TODO_INPUT = (By.CLASS_NAME, "new-todo")
    TODO_LIST = (By.CLASS_NAME, "todo-list")
    TODO_ITEMS = (By.CSS_SELECTOR, ".todo-list li")
    TODO_COUNT = (By.CSS_SELECTOR, ".todo-count")
    TOGGLE_ALL = (By.CLASS_NAME, "toggle-all")
    CLEAR_COMPLETED = (By.CLASS_NAME, "clear-completed")
    FILTER_ALL = (By.CSS_SELECTOR, "a[href='#/']")
    FILTER_ACTIVE = (By.CSS_SELECTOR, "a[href='#/active']")
    FILTER_COMPLETED = (By.CSS_SELECTOR, "a[href='#/completed']")

    URL = "https://todomvc.com/examples/react/dist/"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def navigate(self):
        self.driver.get(self.URL)
        self.wait.until(EC.presence_of_element_located(self.NEW_TODO_INPUT))

    # ------------------------------------------------------------ helpers
    def _items(self):
        return self.driver.find_elements(*self.TODO_ITEMS)

    # ------------------------------------------------------------ actions
    def add_todo(self, text):
        """Add a new todo item"""
        inp = self.wait.until(EC.element_to_be_clickable(self.NEW_TODO_INPUT))
        inp.send_keys(text, Keys.ENTER)

    def toggle_todo(self, index):
        """Toggle todo completion status"""
        self._items()[index].find_element(By.CSS_SELECTOR, ".toggle").click()

    def delete_todo(self, index):
        """Delete a todo item (the button only appears on hover)"""
        item = self._items()[index]
        ActionChains(self.driver).move_to_element(item).perform()
        item.find_element(By.CSS_SELECTOR, ".destroy").click()

    def edit_todo(self, index, new_text, commit=True):
        """Double-click to edit; Enter saves, Escape cancels"""
        item = self._items()[index]
        label = item.find_element(By.TAG_NAME, "label")
        ActionChains(self.driver).double_click(label).perform()
        edit = self.wait.until(
            lambda d: item.find_element(By.CSS_SELECTOR, ".edit")
        )
        edit.send_keys(Keys.CONTROL + "a")  # on Mac use Keys.COMMAND
        if new_text:
            edit.send_keys(new_text)
        else:
            edit.send_keys(Keys.BACKSPACE)
        edit.send_keys(Keys.ENTER if commit else Keys.ESCAPE)

    def clear_completed(self):
        self.wait.until(EC.element_to_be_clickable(self.CLEAR_COMPLETED)).click()

    def filter_all(self):
        """Show all todos"""
        self.driver.find_element(*self.FILTER_ALL).click()

    def filter_active(self):
        """Show only active todos"""
        self.driver.find_element(*self.FILTER_ACTIVE).click()

    def filter_completed(self):
        """Show only completed todos"""
        self.driver.find_element(*self.FILTER_COMPLETED).click()

    # ------------------------------------------------------------ queries
    def get_todo_count(self):
        """Return number of todo items"""
        return len(self._items())

    def get_visible_todos(self):
        """Get list of visible todo texts"""
        return [i.text for i in self._items()]

    def is_completed(self, index):
        items = self._items()
        return "completed" in items[index].get_attribute("class")
