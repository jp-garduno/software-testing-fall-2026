from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TodoPage:
    """Page Object Model for TodoMVC React application."""

    URL = "https://todomvc.com/examples/react/"

    NEW_TODO_INPUT = (By.CSS_SELECTOR, ".new-todo")
    TODO_LIST = (By.CSS_SELECTOR, ".todo-list")
    TODO_ITEMS = (By.CSS_SELECTOR, ".todo-list li")
    TODO_COUNT = (By.CSS_SELECTOR, ".todo-count")
    CLEAR_COMPLETED = (By.CSS_SELECTOR, ".clear-completed")
    FILTER_ALL = (By.CSS_SELECTOR, "a[href='#/']")
    FILTER_ACTIVE = (By.CSS_SELECTOR, "a[href='#/active']")
    FILTER_COMPLETED = (By.CSS_SELECTOR, "a[href='#/completed']")
    HEADER = (By.TAG_NAME, "h1")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def navigate(self):
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.NEW_TODO_INPUT))

    def add_todo(self, text):
        """Add a new todo item."""
        input_box = self.wait.until(EC.element_to_be_clickable(self.NEW_TODO_INPUT))
        input_box.send_keys(text)
        input_box.send_keys(Keys.RETURN)

    def get_todo_items(self):
        return self.driver.find_elements(*self.TODO_ITEMS)

    def get_todo_count(self):
        """Return number of visible todo items."""
        return len(self.get_todo_items())

    def get_visible_todos(self):
        """Get list of visible todo texts."""
        return [
            item.find_element(By.TAG_NAME, "label").text
            for item in self.get_todo_items()
        ]

    def is_todo_completed(self, index):
        """Return True if the todo at index is marked completed."""
        items = self.get_todo_items()
        classes = items[index].get_attribute("class") or ""
        return "completed" in classes.split()

    def toggle_todo(self, index):
        """Toggle todo completion status."""
        items = self.get_todo_items()
        checkbox = items[index].find_element(By.CSS_SELECTOR, ".toggle")
        checkbox.click()

    def delete_todo(self, index):
        """Delete a todo item by hovering and clicking destroy."""
        items = self.get_todo_items()
        item = items[index]
        ActionChains(self.driver).move_to_element(item).perform()
        destroy_btn = item.find_element(By.CSS_SELECTOR, ".destroy")
        self.driver.execute_script("arguments[0].click();", destroy_btn)

    def edit_todo(self, index, new_text, save=True):
        """Edit todo text; press Enter to save or cancel if save=False."""
        items = self.get_todo_items()
        item = items[index]
        label = item.find_element(By.TAG_NAME, "label")
        ActionChains(self.driver).double_click(label).perform()

        edit_input = self.wait.until(
            lambda d: item.find_element(
                By.CSS_SELECTOR, "input.edit, input.new-todo, input[type='text']"
            )
        )
        edit_input.send_keys(Keys.CONTROL, "a")
        edit_input.send_keys(Keys.BACKSPACE)
        edit_input.send_keys(new_text)

        if save:
            edit_input.send_keys(Keys.RETURN)
        else:
            edit_input.send_keys(Keys.ESCAPE)
            # En la versión moderna de TodoMVC React, blur cancela sin guardar
            remaining_inputs = item.find_elements(
                By.CSS_SELECTOR, "input.edit, input.new-todo, input[type='text']"
            )
            if remaining_inputs:
                self.driver.find_element(*self.HEADER).click()

    def clear_completed(self):
        """Click the Clear Completed button."""
        btn = self.wait.until(EC.element_to_be_clickable(self.CLEAR_COMPLETED))
        btn.click()

    def filter_all(self):
        """Show all todos."""
        self.wait.until(EC.element_to_be_clickable(self.FILTER_ALL)).click()

    def filter_active(self):
        """Show only active todos."""
        self.wait.until(EC.element_to_be_clickable(self.FILTER_ACTIVE)).click()

    def filter_completed(self):
        """Show only completed todos."""
        self.wait.until(EC.element_to_be_clickable(self.FILTER_COMPLETED)).click()

    def get_active_count(self):
        """Parse remaining active items count from footer."""
        elements = self.driver.find_elements(*self.TODO_COUNT)
        if not elements:
            return 0
        text = elements[0].text.strip()
        return int(text.split()[0])