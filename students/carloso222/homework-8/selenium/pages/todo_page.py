"""Page Object for TodoMVC React (https://todomvc.com/examples/react/dist/).

The page object only knows *how* to drive the page; the tests decide *what* to assert.
Every action waits explicitly for the UI to reflect it, so the tests never need sleep().
"""

import sys
from pathlib import Path

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from support import settings  # pylint: disable=wrong-import-order


class TodoPage:  # pylint: disable=too-many-public-methods
    # Locators
    NEW_TODO_INPUT = (By.CLASS_NAME, "new-todo")
    TODO_LIST = (By.CLASS_NAME, "todo-list")
    TODO_ITEMS = (By.CSS_SELECTOR, ".todo-list li")
    TODO_LABELS = (By.CSS_SELECTOR, ".todo-list li label")
    COMPLETED_ITEMS = (By.CSS_SELECTOR, ".todo-list li.completed")
    # Transparent checkbox laid over the chevron: it is what actually receives the user's click.
    TOGGLE_ALL = (By.CLASS_NAME, "toggle-all")
    CLEAR_COMPLETED = (By.CLASS_NAME, "clear-completed")
    TODO_COUNT = (By.CLASS_NAME, "todo-count")
    FOOTER = (By.CLASS_NAME, "footer")
    FILTER_ALL = (By.CSS_SELECTOR, "a[href='#/']")
    FILTER_ACTIVE = (By.CSS_SELECTOR, "a[href='#/active']")
    FILTER_COMPLETED = (By.CSS_SELECTOR, "a[href='#/completed']")
    SELECTED_FILTER = (By.CSS_SELECTOR, ".filters a.selected")
    # The edit box has class "edit" but shares data-testid="text-input" with the new-todo box,
    # so it is located by class inside the item that is being edited.
    EDIT_INPUT = (By.CSS_SELECTOR, ".todo-list li.editing input.edit")

    # Locators relative to a single <li>
    ITEM_TOGGLE = (By.CLASS_NAME, "toggle")
    ITEM_LABEL = (By.TAG_NAME, "label")
    ITEM_DESTROY = (By.CLASS_NAME, "destroy")

    FILTERS = {
        "All": FILTER_ALL,
        "Active": FILTER_ACTIVE,
        "Completed": FILTER_COMPLETED,
    }

    def __init__(
        self,
        driver: WebDriver,
        base_url: str = settings.BASE_URL,
        timeout: float = settings.TIMEOUT,
    ):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(
            driver, timeout, poll_frequency=settings.POLL_FREQUENCY
        )

    # ------------------------------------------------------------------ navigation
    def navigate(self) -> "TodoPage":
        """Open the app and wait until the new-todo input is ready."""
        self.driver.get(self.base_url)
        self.wait.until(EC.visibility_of_element_located(self.NEW_TODO_INPUT))
        return self

    def reset(self) -> "TodoPage":
        """Start from an empty list: the app keeps its todos in memory only, so a full reload clears them.

        Going through about:blank forces a real page load even when the current URL only differs
        by its #/route fragment (which would otherwise be a same-document navigation).
        """
        self.driver.get("about:blank")
        return self.navigate()

    # ------------------------------------------------------------------ creation
    def add_todo(self, text: str) -> None:
        """Type a todo and press Enter. Blank text is ignored by the app, so nothing is awaited then."""
        field = self.driver.find_element(*self.NEW_TODO_INPUT)
        field.send_keys(text + Keys.ENTER)
        if text.strip():
            # The app clears the input once the todo has been added.
            self.wait.until(
                lambda d: d.find_element(*self.NEW_TODO_INPUT).get_attribute("value")
                == ""
            )

    def add_todos(self, *texts: str) -> None:
        for text in texts:
            self.add_todo(text)

    # ------------------------------------------------------------------ queries
    def get_todo_count(self) -> int:
        """Number of todos visible with the current filter."""
        return len(self.driver.find_elements(*self.TODO_ITEMS))

    def get_visible_todos(self) -> list[str]:
        """Texts of the todos visible with the current filter, in order."""
        return [label.text for label in self.driver.find_elements(*self.TODO_LABELS)]

    def is_completed(self, index: int) -> bool:
        return "completed" in self._item(index).get_attribute("class").split()

    def completion_states(self) -> list[bool]:
        return [
            "completed" in item.get_attribute("class").split() for item in self._items()
        ]

    def get_counter_text(self) -> str:
        """Footer counter, e.g. '2 items left!' (empty when the footer is hidden)."""
        counter = self.driver.find_element(*self.TODO_COUNT)
        return counter.text if counter.is_displayed() else ""

    def get_active_count(self) -> int:
        """Number from the footer counter; 0 when the footer is hidden (no todos)."""
        text = self.get_counter_text()
        return int(text.split()[0]) if text else 0

    def is_footer_visible(self) -> bool:
        return self.driver.find_element(*self.FOOTER).is_displayed()

    def is_clear_completed_visible(self) -> bool:
        return self.driver.find_element(*self.CLEAR_COMPLETED).is_displayed()

    def selected_filter(self) -> str:
        return self.driver.find_element(*self.SELECTED_FILTER).text

    def current_route(self) -> str:
        """Hash route of the current URL, e.g. '#/active'."""
        url = self.driver.current_url
        return url[url.index("#") :] if "#" in url else ""

    def is_editing(self) -> bool:
        return bool(self.driver.find_elements(*self.EDIT_INPUT))

    # ------------------------------------------------------------------ completion
    def toggle_todo(self, index: int) -> None:
        """Click the checkbox of a todo and wait until its state changes (or it leaves the filtered view)."""
        item = self._item(index)
        was_completed = "completed" in item.get_attribute("class").split()
        item.find_element(*self.ITEM_TOGGLE).click()

        def state_changed(_driver):
            try:
                return (
                    "completed" in item.get_attribute("class").split()
                ) != was_completed
            except StaleElementReferenceException:
                return True  # the item was removed from the current filter

        self.wait.until(state_changed)

    def toggle_all(self) -> None:
        before = self._completed_count()
        # opacity:0 makes Selenium report it as "not displayed", so wait for presence, not visibility.
        self.wait.until(EC.presence_of_element_located(self.TOGGLE_ALL)).click()
        # One WebDriver call per poll (reading every item's class would cost one call per todo).
        self.wait.until(lambda _d: self._completed_count() != before)

    # ------------------------------------------------------------------ deletion
    def delete_todo(self, index: int) -> None:
        """Hover over a todo to reveal its (CSS-hidden) delete button, then click it."""
        item = self._item(index)
        count_before = self.get_todo_count()
        ActionChains(self.driver).move_to_element(item).perform()
        destroy = item.find_element(*self.ITEM_DESTROY)
        self.wait.until(EC.visibility_of(destroy))
        destroy.click()
        self.wait.until(lambda _d: self.get_todo_count() == count_before - 1)

    def clear_completed(self) -> None:
        button = self.wait.until(EC.element_to_be_clickable(self.CLEAR_COMPLETED))
        button.click()
        self.wait.until(EC.invisibility_of_element_located(self.CLEAR_COMPLETED))

    # ------------------------------------------------------------------ editing
    def start_editing(self, index: int) -> WebElement:
        """Double-click a todo label and return the edit box."""
        label = self._item(index).find_element(*self.ITEM_LABEL)
        ActionChains(self.driver).double_click(label).perform()
        return self.wait.until(EC.visibility_of_element_located(self.EDIT_INPUT))

    def edit_todo(self, index: int, new_text: str, commit: str = "enter") -> None:
        """Replace a todo's text and commit it with Enter (commit='enter') or by leaving the box ('blur')."""
        field = self.start_editing(index)
        self._replace_text(field, new_text)
        if commit == "enter":
            field.send_keys(Keys.ENTER)
        elif commit == "blur":
            field.send_keys(Keys.TAB)  # moving the focus away triggers the blur handler
        else:
            raise ValueError("commit must be 'enter' or 'blur'")
        self.wait.until(EC.invisibility_of_element_located(self.EDIT_INPUT))

    def cancel_edit(self, index: int, typed_text: str) -> None:
        """Type into the edit box and press Escape (TodoMVC spec: Escape discards the change)."""
        field = self.start_editing(index)
        self._replace_text(field, typed_text)
        field.send_keys(Keys.ESCAPE)

    def wait_until_not_editing(self, timeout: float = 1.0) -> bool:
        """True if the edit box disappears within `timeout` seconds."""
        try:
            WebDriverWait(
                self.driver, timeout, poll_frequency=settings.POLL_FREQUENCY
            ).until(EC.invisibility_of_element_located(self.EDIT_INPUT))
            return True
        except TimeoutException:
            return False

    # ------------------------------------------------------------------ filters
    def filter_all(self) -> None:
        self.apply_filter("All")

    def filter_active(self) -> None:
        self.apply_filter("Active")

    def filter_completed(self) -> None:
        self.apply_filter("Completed")

    def apply_filter(self, name: str) -> None:
        """Click a filter link ('All', 'Active' or 'Completed') and wait until it is selected."""
        link = self.driver.find_element(*self.FILTERS[name])
        link.click()
        self.wait.until(lambda _d: "selected" in link.get_attribute("class").split())

    # ------------------------------------------------------------------ evidence
    def take_screenshot(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.driver.save_screenshot(str(path))
        return path

    # ------------------------------------------------------------------ internals
    @staticmethod
    def _replace_text(field: WebElement, text: str) -> None:
        """Select the current text and type over it.

        WebElement.clear() is not used on purpose: WebDriver blurs the element after clearing it,
        and this app commits an edit on blur, so clear() would save an empty title and delete the todo.
        """
        select_all = Keys.COMMAND if sys.platform == "darwin" else Keys.CONTROL
        field.send_keys(select_all, "a")
        field.send_keys(text if text else Keys.BACKSPACE)

    def _completed_count(self) -> int:
        return len(self.driver.find_elements(*self.COMPLETED_ITEMS))

    def _items(self) -> list[WebElement]:
        return self.driver.find_elements(*self.TODO_ITEMS)

    def _item(self, index: int) -> WebElement:
        self.wait.until(lambda _d: len(self._items()) > index)
        return self._items()[index]
