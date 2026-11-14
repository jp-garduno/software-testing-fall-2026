# pages/todo_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TodoPage:
    # Locators
    NEW_TODO_INPUT = (By.CLASS_NAME, "new-todo")
    TODO_LIST = (By.CLASS_NAME, "todo-list")
    TODO_ITEMS = (By.CSS_SELECTOR, ".todo-list li")
    TOGGLE_ALL = (By.CLASS_NAME, "toggle-all")
    CLEAR_COMPLETED = (By.CLASS_NAME, "clear-completed")
    FILTER_ALL = (By.CSS_SELECTOR, "a[href='#/']")
    FILTER_ACTIVE = (By.CSS_SELECTOR, "a[href='#/active']")
    FILTER_COMPLETED = (By.CSS_SELECTOR, "a[href='#/completed']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def navigate(self):
        self.driver.get("https://todomvc.com/examples/react/dist/")

    def add_todo(self, text):
        """Add a new todo item"""
        print(f"Waiting for the todo input to add: {text}")
        todo_input = self.wait.until(
            EC.visibility_of_element_located(self.NEW_TODO_INPUT)
        )
        print("Todo input is ready; typing the todo.")
        todo_input.send_keys(text)
        print("Submitting the todo.")
        todo_input.send_keys(Keys.ENTER)
        print("Waiting for the todo input to clear.")
        self.wait.until(
            lambda driver: driver.find_element(
                *self.NEW_TODO_INPUT
            ).get_attribute("value") == ""
        )
        print(f"Todo added: {text}")

    def get_todo_count(self):
        """Return number of todo items"""
        return len(self.driver.find_elements(*self.TODO_ITEMS))

    def toggle_todo(self, index):
        """Toggle completion for the todo at the zero-based index."""
        todo_item = self.driver.find_elements(*self.TODO_ITEMS)[index]
        toggle = todo_item.find_element(By.CLASS_NAME, "toggle")
        was_selected = toggle.is_selected()
        toggle.click()
        self.wait.until(
            lambda driver: driver.find_elements(*self.TODO_ITEMS)[
                index
            ].find_element(By.CLASS_NAME, "toggle").is_selected()
            != was_selected
        )

    def delete_todo(self, index):
        """Delete a todo item"""
        todo_item = self.driver.find_elements(*self.TODO_ITEMS)[index]
        ActionChains(self.driver).move_to_element(todo_item).perform()
        delete_button = todo_item.find_element(By.CLASS_NAME, "destroy")
        delete_button = self.wait.until(
            EC.element_to_be_clickable(delete_button)
        )
        delete_button.click()
        self.wait.until(EC.staleness_of(todo_item))

    def filter_active(self):
        """Show only active todos"""
        # TODO: Implement
        pass

    def filter_completed(self):
        """Show only completed todos"""
        # TODO: Implement
        pass

    def get_visible_todos(self):
        """Get list of visible todo texts"""
        # TODO: Implement
        pass