"""Page Object for the TodoMVC React app, driven with Selenium WebDriver.

The tests talk to this class instead of the DOM: if a selector changes, it changes here only.
Every action waits explicitly for the page to reach the state the action produces (one more
item, one fewer item, the new filter selected...), so the tests never need ``time.sleep``.
"""

from __future__ import annotations

import os
import re
from typing import List

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# The assignment links to /examples/react/, which now answers 404; the app lives in /dist/.
DEFAULT_URL = "https://todomvc.com/examples/react/dist/"


class TodoPage:  # pylint: disable=too-many-public-methods
    """Actions and queries a user can perform on the todo list."""

    # Locators
    NEW_TODO_INPUT = (By.CSS_SELECTOR, "input.new-todo")
    TODO_ITEMS = (By.CSS_SELECTOR, ".todo-list li")
    ITEM_LABEL = (By.CSS_SELECTOR, "label")
    ITEM_TOGGLE = (By.CSS_SELECTOR, "input.toggle")
    ITEM_DESTROY = (By.CSS_SELECTOR, "button.destroy")
    ITEM_EDIT_INPUT = (By.CSS_SELECTOR, "input.edit")
    TOGGLE_ALL = (By.CSS_SELECTOR, "input.toggle-all")
    TODO_COUNT = (By.CSS_SELECTOR, ".todo-count")
    CLEAR_COMPLETED = (By.CSS_SELECTOR, "button.clear-completed")
    FOOTER = (By.CSS_SELECTOR, "footer.footer")
    TITLE = (By.CSS_SELECTOR, ".todoapp h1")
    FILTERS = {
        "All": (By.CSS_SELECTOR, "a[href='#/']"),
        "Active": (By.CSS_SELECTOR, "a[href='#/active']"),
        "Completed": (By.CSS_SELECTOR, "a[href='#/completed']"),
    }

    def __init__(self, driver, base_url: str | None = None, timeout: float = 10) -> None:
        self.driver = driver
        self.base_url = base_url or os.environ.get("BASE_URL", DEFAULT_URL)
        self.wait = WebDriverWait(driver, timeout)

    # ------------------------------------------------------------------ #
    # Navigation
    # ------------------------------------------------------------------ #
    def navigate(self) -> "TodoPage":
        """Open the app with an empty list (the React example keeps todos in memory only)."""
        self.driver.get(self.base_url)
        self.wait.until(EC.presence_of_element_located(self.NEW_TODO_INPUT))
        return self

    # ------------------------------------------------------------------ #
    # Creating
    # ------------------------------------------------------------------ #
    def add_todo(self, text: str) -> None:
        """Type a todo and press Enter, then wait for the app to process it.

        The app ignores blank text. A new todo is active, so it shows up in the All and Active
        views but not in the Completed view.
        """
        accepted = bool(text.strip())
        shown = accepted and self.current_route() != "#/completed"
        expected = self.get_todo_count() + (1 if shown else 0)
        field = self.driver.find_element(*self.NEW_TODO_INPUT)
        field.send_keys(text, Keys.ENTER)
        if accepted:
            self.wait.until(lambda _: self.new_todo_value() == "")
        self.wait.until(lambda _: self.get_todo_count() == expected)

    def add_todos(self, *texts: str) -> None:
        for text in texts:
            self.add_todo(text)

    def new_todo_value(self) -> str:
        """Current text of the "What needs to be done?" field."""
        return self.driver.find_element(*self.NEW_TODO_INPUT).get_property("value")

    # ------------------------------------------------------------------ #
    # Reading
    # ------------------------------------------------------------------ #
    def _items(self):
        return self.driver.find_elements(*self.TODO_ITEMS)

    def _item(self, index: int):
        items = self._items()
        if not 0 <= index < len(items):
            raise IndexError(f"There is no todo #{index}; the list shows {len(items)}")
        return items[index]

    def get_todo_count(self) -> int:
        """Number of todos currently shown (after the active filter)."""
        return len(self._items())

    def get_visible_todos(self) -> List[str]:
        """Texts of the todos currently shown, top to bottom."""
        return [item.find_element(*self.ITEM_LABEL).text for item in self._items()]

    def is_completed(self, index: int) -> bool:
        item = self._item(index)
        return "completed" in (item.get_dom_attribute("class") or "").split()

    def get_active_count(self) -> int:
        """The number in the "N items left!" counter."""
        text = self.driver.find_element(*self.TODO_COUNT).text
        match = re.match(r"(\d+)", text)
        return int(match.group(1)) if match else 0

    def get_counter_text(self) -> str:
        return self.driver.find_element(*self.TODO_COUNT).text

    def is_footer_visible(self) -> bool:
        """The footer (counter, filters) is hidden while the list is empty."""
        footers = self.driver.find_elements(*self.FOOTER)
        return bool(footers) and footers[0].get_dom_attribute("hidden") is None

    def is_clear_completed_visible(self) -> bool:
        buttons = self.driver.find_elements(*self.CLEAR_COMPLETED)
        return bool(buttons) and buttons[0].get_dom_attribute("hidden") is None

    # ------------------------------------------------------------------ #
    # Completing
    # ------------------------------------------------------------------ #
    def toggle_todo(self, index: int) -> None:
        """Click the round checkbox of a todo and wait for its completed state to flip."""
        was_completed = self.is_completed(index)
        count = self.get_todo_count()
        self._item(index).find_element(*self.ITEM_TOGGLE).click()
        # In the Active/Completed views the item disappears instead of changing class.
        self.wait.until(lambda _: self.get_todo_count() != count or self.is_completed(index) != was_completed)

    def toggle_all(self) -> None:
        """Click the chevron left of the input: completes every todo (or reopens them all)."""
        target = not self.driver.find_element(*self.TOGGLE_ALL).is_selected()
        self.driver.find_element(*self.TOGGLE_ALL).click()
        self.wait.until(lambda _: all(self.is_completed(i) == target for i in range(self.get_todo_count())))

    # ------------------------------------------------------------------ #
    # Deleting
    # ------------------------------------------------------------------ #
    def delete_todo(self, index: int) -> None:
        """Hover the todo so its × button appears, click it and wait for the item to go."""
        item = self._item(index)
        count = self.get_todo_count()
        ActionChains(self.driver).move_to_element(item).perform()
        destroy = item.find_element(*self.ITEM_DESTROY)
        self.wait.until(lambda _: destroy.is_enabled())
        ActionChains(self.driver).move_to_element(destroy).click().perform()
        self.wait.until(lambda _: self.get_todo_count() == count - 1)

    def clear_completed(self) -> None:
        self.driver.find_element(*self.CLEAR_COMPLETED).click()
        self.wait.until(lambda _: not self.is_clear_completed_visible())

    # ------------------------------------------------------------------ #
    # Editing
    # ------------------------------------------------------------------ #
    def start_editing(self, index: int):
        """Double-click a todo's label; returns the edit field that replaces it."""
        label = self._item(index).find_element(*self.ITEM_LABEL)
        ActionChains(self.driver).double_click(label).perform()
        return self.wait.until(EC.presence_of_element_located(self.ITEM_EDIT_INPUT))

    def is_editing(self, index: int) -> bool:
        return "editing" in (self._item(index).get_dom_attribute("class") or "").split()

    def edit_todo(self, index: int, new_text: str) -> None:
        """Replace a todo's text and save it with Enter."""
        field = self.start_editing(index)
        field.send_keys(Keys.CONTROL, "a")
        field.send_keys(Keys.BACKSPACE, new_text, Keys.ENTER)
        self._wait_until_not_editing()

    def _wait_until_not_editing(self) -> None:
        self.wait.until(lambda _: not self.driver.find_elements(*self.ITEM_EDIT_INPUT))

    def type_in_edit(self, index: int, new_text: str):
        """Replace the text in edit mode without saving yet (to test blur and Escape)."""
        field = self.start_editing(index)
        field.send_keys(Keys.CONTROL, "a")
        field.send_keys(Keys.BACKSPACE, new_text)
        return field

    def leave_edit_by_clicking_outside(self) -> None:
        """Blur the edit field by clicking the page title; the app saves on blur."""
        self.driver.find_element(*self.TITLE).click()
        self._wait_until_not_editing()

    # ------------------------------------------------------------------ #
    # Filtering
    # ------------------------------------------------------------------ #
    def _filter(self, name: str) -> None:
        self.driver.find_element(*self.FILTERS[name]).click()
        self.wait.until(lambda _: self.selected_filter() == name)

    def filter_all(self) -> None:
        self._filter("All")

    def filter_active(self) -> None:
        self._filter("Active")

    def filter_completed(self) -> None:
        self._filter("Completed")

    def filter_by(self, name: str) -> None:
        """Filter by link text: All, Active or Completed."""
        if name not in self.FILTERS:
            raise ValueError(f"Unknown filter {name!r}; use All, Active or Completed")
        self._filter(name)

    def selected_filter(self) -> str:
        """Name of the filter link currently highlighted."""
        for name, locator in self.FILTERS.items():
            if "selected" in (self.driver.find_element(*locator).get_dom_attribute("class") or "").split():
                return name
        return ""

    def current_route(self) -> str:
        """The hash route of the URL, e.g. '#/active'."""
        return self.driver.execute_script("return window.location.hash") or "#/"
