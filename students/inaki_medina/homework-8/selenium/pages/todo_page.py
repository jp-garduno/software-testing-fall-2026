# pages/todo_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver

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

    def close(self):
        self.driver.quit()

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

    def clear_completed(self):
        """Remove all completed todos."""
        starting_count = self.get_todo_count()
        completed_count = starting_count - self.get_active_todo_count()
        if completed_count == 0:
            return

        clear_button = self.wait.until(
            EC.element_to_be_clickable(self.CLEAR_COMPLETED)
        )
        clear_button.click()
        self.wait.until(
            lambda driver: len(driver.find_elements(*self.TODO_ITEMS))
            == starting_count - completed_count
        )

    def filter_active(self):
        """Show only active todos"""
        filter_link = self.wait.until(
            EC.element_to_be_clickable(self.FILTER_ACTIVE)
        )
        filter_link.click()
        self.wait.until(EC.url_contains("#/active"))


    def filter_completed(self):
        """Show only completed todos"""
        filter_link = self.wait.until(
            EC.element_to_be_clickable(self.FILTER_COMPLETED)
        )
        filter_link.click()
        self.wait.until(EC.url_contains('#/completed'))

    def filter_all(self):
        """Show all todos"""
        filter_link = self.wait.until(
            EC.element_to_be_clickable(self.FILTER_ALL)
        )
        filter_link.click()
        self.wait.until(lambda driver: driver.current_url.endswith("#/"))

    def filter_todos(self, filter_name):
        """Apply one of the supported todo filters."""
        if filter_name == "All":
            self.filter_all()
        elif filter_name == "Active":
            self.filter_active()
        elif filter_name == "Completed":
            self.filter_completed()
        else:
            raise ValueError(f"Unknown todo filter: {filter_name}")

    def get_visible_todos(self):
        """Get list of visible todo texts"""
        todo_items = self.driver.find_elements(*self.TODO_ITEMS)
        return [
            todo_item.find_element(By.CSS_SELECTOR, "label").text.strip()
            for todo_item in todo_items
            if todo_item.is_displayed()
        ]

    def is_todo_completed(self, index):
        """Return whether the todo at the zero-based index is complete."""
        todo_item = self.driver.find_elements(*self.TODO_ITEMS)[index]
        return todo_item.find_element(By.CLASS_NAME, "toggle").is_selected()

    def get_active_todo_count(self):
        """Return the number of todos that are not completed."""
        todo_items = self.driver.find_elements(*self.TODO_ITEMS)
        return sum(
            not todo_item.find_element(By.CLASS_NAME, "toggle").is_selected()
            for todo_item in todo_items
        )

    def _visible_edit_input(self, driver, index):
        todo_items = driver.find_elements(*self.TODO_ITEMS)
        if len(todo_items) <= index:
            return False
        edit_inputs = todo_items[index].find_elements(
            By.CSS_SELECTOR, "input.edit"
        )
        return (
            edit_inputs[0]
            if edit_inputs and edit_inputs[0].is_displayed()
            else False
        )

    def _open_edit_input(self, index):
        todo_to_edit = self.driver.find_elements(*self.TODO_ITEMS)[index]
        name = todo_to_edit.find_element(By.CSS_SELECTOR, "label")
        ActionChains(self.driver).double_click(name).perform()
        return self.wait.until(
            lambda driver: self._visible_edit_input(driver, index)
        )

    def edit_todo(self, index, text):
        name_input = self._open_edit_input(index)
        name_input.send_keys(Keys.CONTROL, "a")
        name_input.send_keys(text)

        def edit_input_has_new_text(driver):
            edit_input = self._visible_edit_input(driver, index)
            return edit_input and edit_input.get_attribute("value") == text

        self.wait.until(
            edit_input_has_new_text
        )
        name_input = self.wait.until(
            lambda driver: self._visible_edit_input(driver, index)
        )
        name_input.send_keys(Keys.ENTER)

        def todo_has_new_text(driver):
            todo_items = driver.find_elements(*self.TODO_ITEMS)
            return (
                len(todo_items) > index
                and todo_items[index]
                .find_element(By.CSS_SELECTOR, "label")
                .text.strip()
                == text
            )

        self.wait.until(
            todo_has_new_text
        )

    def cancel_edit_todo(self, index):
        original_text = self.get_todo_by_index(index)
        name_input = self._open_edit_input(index)
        self.wait.until(
            lambda driver: name_input.get_attribute("value") == original_text
        )
        name_input.click()
        self.wait.until(
            lambda driver: driver.switch_to.active_element == name_input
        )
        self.driver.execute_script(
            "window.__todoKeys = []; "
            "document.addEventListener('keydown', event => "
            "window.__todoKeys.push({key: event.key, target: event.target.outerHTML}), true)"
        )
        ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        try:
            self.wait.until(EC.invisibility_of_element(name_input))
        except TimeoutException:
            print(
                "Cancel debug:",
                self.driver.execute_script(
                    "return {keys: window.__todoKeys, active: document.activeElement.outerHTML, "
                    "items: [...document.querySelectorAll('.todo-list li')].map(item => item.outerHTML)}"
                ),
            )
            raise
        self.wait.until(
            lambda driver: driver.find_elements(*self.TODO_ITEMS)[index]
            .find_element(By.CSS_SELECTOR, "label")
            .text.strip()
            == original_text
        )

    def get_todo_by_index(self, index):
        todo_items = self.wait.until(
            EC.presence_of_all_elements_located(self.TODO_ITEMS)
        )
        return todo_items[index].find_element(
            By.CSS_SELECTOR, "label"
        ).text.strip()

    def get_last_todo(self):
        todo_items = self.wait.until(
            EC.presence_of_all_elements_located(self.TODO_ITEMS)
        )
        return todo_items[-1].find_element(
            By.CSS_SELECTOR, "label"
        ).text.strip()


def create_todo_page():
    return TodoPage(webdriver.Chrome())
