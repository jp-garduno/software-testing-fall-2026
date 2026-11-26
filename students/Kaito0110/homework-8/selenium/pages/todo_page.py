from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class TodoPage:
    URL = "https://todomvc.com/examples/react/dist/"
    NEW_TODO_INPUT = (By.CSS_SELECTOR, ".new-todo")
    TODO_ITEMS = (By.CSS_SELECTOR, ".todo-list li")
    TODO_COUNT = (By.CSS_SELECTOR, ".todo-count")
    FILTER_ALL = (By.CSS_SELECTOR, "a[href='#/']")
    FILTER_ACTIVE = (By.CSS_SELECTOR, "a[href='#/active']")
    FILTER_COMPLETED = (By.CSS_SELECTOR, "a[href='#/completed']")
    CLEAR_COMPLETED = (By.CSS_SELECTOR, ".clear-completed")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def navigate(self):
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.NEW_TODO_INPUT))

    def add_todo(self, text):
        input_box = self.wait.until(
            EC.visibility_of_element_located(self.NEW_TODO_INPUT)
        )
        input_box.send_keys(text, Keys.ENTER)
        self.wait.until(lambda driver: len(driver.find_elements(*self.TODO_ITEMS)) > 0)

    def get_todo_count(self):
        return len(self.driver.find_elements(*self.TODO_ITEMS))

    def get_visible_todos(self):
        return [
            item.find_element(By.CSS_SELECTOR, "label").text
            for item in self.driver.find_elements(*self.TODO_ITEMS)
        ]

    def _todo(self, index):
        return self.wait.until(
            lambda driver: driver.find_elements(*self.TODO_ITEMS)[index]
        )

    def toggle_todo(self, index):
        self._todo(index).find_element(By.CSS_SELECTOR, ".toggle").click()

    def is_completed(self, index):
        return "completed" in self._todo(index).get_attribute("class").split()

    def delete_todo(self, index):
        item = self._todo(index)
        previous_count = self.get_todo_count()
        ActionChains(self.driver).move_to_element(item).perform()
        item.find_element(By.CSS_SELECTOR, ".destroy").click()
        self.wait.until(
            lambda driver: len(driver.find_elements(*self.TODO_ITEMS))
            == previous_count - 1
        )

    def filter_all(self):
        self.wait.until(EC.element_to_be_clickable(self.FILTER_ALL)).click()

    def filter_active(self):
        self.wait.until(EC.element_to_be_clickable(self.FILTER_ACTIVE)).click()

    def filter_completed(self):
        self.wait.until(EC.element_to_be_clickable(self.FILTER_COMPLETED)).click()

    def get_active_count(self):
        count_text = self.wait.until(
            EC.visibility_of_element_located(self.TODO_COUNT)
        ).text
        return int(count_text.split()[0])

    def clear_completed(self):
        self.wait.until(EC.element_to_be_clickable(self.CLEAR_COMPLETED)).click()

    def edit_todo(self, index, text, save=True):
        item = self._todo(index)
        label = item.find_element(By.CSS_SELECTOR, "label")
        ActionChains(self.driver).double_click(label).perform()
        editor = self.wait.until(
            lambda driver: driver.find_elements(*self.TODO_ITEMS)[index].find_element(
                By.CSS_SELECTOR, "input.edit"
            )
        )
        if not save:
            editor.send_keys(Keys.ESCAPE)
            self.driver.find_element(*self.NEW_TODO_INPUT).click()
            self.wait.until(
                lambda driver: "editing"
                not in driver.find_elements(*self.TODO_ITEMS)[index]
                .get_attribute("class")
                .split()
            )
            return

        editor.send_keys(Keys.CONTROL, "a")
        if text:
            editor.send_keys(text)
        else:
            editor.send_keys(Keys.BACKSPACE)
        editor = self.wait.until(
            lambda driver: driver.find_elements(*self.TODO_ITEMS)[index].find_element(
                By.CSS_SELECTOR, "input.edit"
            )
        )
        editor.send_keys(Keys.ENTER)
