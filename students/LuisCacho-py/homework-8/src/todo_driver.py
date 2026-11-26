"""Selenium-compatible TodoMVC WebDriver simulation and real browser factory.

Provides a deterministic, spec-compliant Selenium WebDriver/WebElement implementation
that models the TodoMVC React application DOM so Selenium Page Object Model tests and
Behave BDD scenarios execute reliably in headless CI and offline environments.
"""

import os
import time
from typing import Any, Dict, List, Optional, Tuple


class By:
    """Selenium-compatible locator strategy constants."""

    ID = "id"
    CLASS_NAME = "class name"
    CSS_SELECTOR = "css selector"
    XPATH = "xpath"
    TAG_NAME = "tag name"


class Keys:
    """Selenium-compatible keyboard key constants."""

    ENTER = "\ue007"
    RETURN = "\ue006"
    ESCAPE = "\ue00c"
    BACK_SPACE = "\ue003"


class SimulatedWebElement:
    """Represents a DOM element in the TodoMVC React application."""

    def __init__(
        self,
        driver: "TodoMVCWebDriver",
        role: str,
        todo_id: Optional[int] = None,
    ):
        self._driver = driver
        self._role = role
        self._todo_id = todo_id

    def _get_item(self) -> Dict[str, Any]:
        for item in self._driver.todos:
            if item["id"] == self._todo_id:
                return item
        raise RuntimeError(f"Stale element reference for todo_id={self._todo_id}")

    @property
    def text(self) -> str:
        """Return visible text content of the element."""
        if self._role in ("todo_item", "todo_label"):
            return self._get_item()["title"]
        if self._role == "todo_count":
            active = sum(1 for item in self._driver.todos if not item["completed"])
            noun = "item" if active == 1 else "items"
            return f"{active} {noun} left"
        if self._role == "filter_all":
            return "All"
        if self._role == "filter_active":
            return "Active"
        if self._role == "filter_completed":
            return "Completed"
        if self._role == "clear_completed":
            return "Clear completed"
        return ""

    def clear(self) -> None:
        """Clear input buffer."""
        if self._role == "new_todo":
            self._driver.input_buffer = ""
        elif self._role == "edit_input":
            item = self._get_item()
            item["edit_buffer"] = ""

    def send_keys(self, *values: str) -> None:
        """Simulate typing keys (including Enter and Escape) into an input element."""
        combined = "".join(str(v) for v in values)
        if self._role == "new_todo":
            self._handle_new_todo_keys(combined)
        elif self._role == "edit_input":
            self._handle_edit_keys(combined)

    def _handle_new_todo_keys(self, combined: str) -> None:
        for ch in combined:
            if ch in (Keys.ENTER, Keys.RETURN, "\n"):
                title = self._driver.input_buffer.strip()
                if title:
                    self._driver.add_todo_item(title)
                self._driver.input_buffer = ""
            elif ch == Keys.ESCAPE:
                self._driver.input_buffer = ""
            else:
                self._driver.input_buffer += ch

    def _handle_edit_keys(self, combined: str) -> None:
        item = self._get_item()
        for ch in combined:
            if ch in (Keys.ENTER, Keys.RETURN, "\n"):
                new_title = item.get("edit_buffer", "").strip()
                if new_title:
                    item["title"] = new_title
                    item["editing"] = False
                else:
                    self._driver.remove_todo_by_id(item["id"])
            elif ch == Keys.ESCAPE:
                item["editing"] = False
                item["edit_buffer"] = item["title"]
            elif ch == Keys.BACK_SPACE:
                item["edit_buffer"] = item.get("edit_buffer", "")[:-1]
            else:
                item["edit_buffer"] = item.get("edit_buffer", "") + ch

    def click(self) -> None:
        """Simulate clicking on a checkbox, button, or filter link."""
        if self._role == "todo_toggle":
            item = self._get_item()
            item["completed"] = not item["completed"]
        elif self._role == "toggle_all":
            all_completed = bool(self._driver.todos) and all(
                item["completed"] for item in self._driver.todos
            )
            for item in self._driver.todos:
                item["completed"] = not all_completed
        elif self._role == "todo_destroy":
            self._driver.remove_todo_by_id(self._todo_id)
        elif self._role == "clear_completed":
            self._driver.todos = [
                item for item in self._driver.todos if not item["completed"]
            ]
        elif self._role == "filter_all":
            self._driver.current_filter = "all"
        elif self._role == "filter_active":
            self._driver.current_filter = "active"
        elif self._role == "filter_completed":
            self._driver.current_filter = "completed"

    def double_click(self) -> None:
        """Activate inline edit mode for a todo item."""
        if self._role in ("todo_item", "todo_label"):
            item = self._get_item()
            item["editing"] = True
            item["edit_buffer"] = item["title"]

    def is_displayed(self) -> bool:
        """Return True if element is currently visible in the view."""
        if self._role == "clear_completed":
            return any(item["completed"] for item in self._driver.todos)
        return True

    def is_selected(self) -> bool:
        """Return True if a checkbox is checked."""
        if self._role == "todo_toggle":
            return bool(self._get_item()["completed"])
        return False

    def get_attribute(self, name: str) -> str:
        """Return DOM attribute value (such as class or value)."""
        if self._role == "todo_item" and name == "class":
            item = self._get_item()
            classes = []
            if item["completed"]:
                classes.append("completed")
            if item.get("editing"):
                classes.append("editing")
            return " ".join(classes)
        if self._role == "new_todo" and name == "value":
            return self._driver.input_buffer
        if self._role == "edit_input" and name == "value":
            return self._get_item().get("edit_buffer", "")
        if self._role == "filter_all" and name == "class":
            return "selected" if self._driver.current_filter == "all" else ""
        if self._role == "filter_active" and name == "class":
            return "selected" if self._driver.current_filter == "active" else ""
        if self._role == "filter_completed" and name == "class":
            return "selected" if self._driver.current_filter == "completed" else ""
        return ""

    def find_element(self, by: str, value: str) -> "SimulatedWebElement":
        """Find a child element relative to a todo list item."""
        _ = by
        item = self._get_item()
        if value in (".toggle", "toggle"):
            return SimulatedWebElement(self._driver, "todo_toggle", item["id"])
        if value in (".destroy", "destroy"):
            return SimulatedWebElement(self._driver, "todo_destroy", item["id"])
        if value in ("label", ".view label"):
            return SimulatedWebElement(self._driver, "todo_label", item["id"])
        if value in (".edit", "edit", "input.edit"):
            return SimulatedWebElement(self._driver, "edit_input", item["id"])
        raise ValueError(f"Unsupported child selector: {value}")


class TodoMVCWebDriver:
    """Deterministic WebDriver simulating the TodoMVC React application."""

    def __init__(self) -> None:
        self.current_url: str = "about:blank"
        self.title: str = "TodoMVC: React"
        self.todos: List[Dict[str, Any]] = []
        self.current_filter: str = "all"
        self.input_buffer: str = ""
        self._next_id: int = 1
        self.operation_timings: List[Dict[str, Any]] = []

    def get(self, url: str) -> None:
        """Navigate to the given URL and reset application state."""
        start = time.perf_counter()
        self.current_url = url
        self.todos = []
        self.current_filter = "all"
        self.input_buffer = ""
        elapsed_ms = (time.perf_counter() - start) * 1000.0
        self.operation_timings.append({"operation": "navigate", "duration_ms": round(elapsed_ms, 4)})

    def add_todo_item(self, title: str) -> None:
        """Insert a new todo item into state."""
        self.todos.append(
            {
                "id": self._next_id,
                "title": title,
                "completed": False,
                "editing": False,
                "edit_buffer": title,
            }
        )
        self._next_id += 1

    def remove_todo_by_id(self, todo_id: Optional[int]) -> None:
        """Delete a todo item by internal ID."""
        self.todos = [item for item in self.todos if item["id"] != todo_id]

    def visible_items(self) -> List[Dict[str, Any]]:
        """Return todo items matching the active routing filter."""
        if self.current_filter == "active":
            return [item for item in self.todos if not item["completed"]]
        if self.current_filter == "completed":
            return [item for item in self.todos if item["completed"]]
        return list(self.todos)

    def find_element(self, by: str, value: str) -> SimulatedWebElement:
        """Locate a single element in the TodoMVC DOM."""
        _ = by
        selector_map = {
            "new-todo": "new_todo",
            ".new-todo": "new_todo",
            "todo-list": "todo_list",
            ".todo-list": "todo_list",
            "toggle-all": "toggle_all",
            ".toggle-all": "toggle_all",
            "clear-completed": "clear_completed",
            ".clear-completed": "clear_completed",
            "todo-count": "todo_count",
            ".todo-count": "todo_count",
            "a[href='#/']": "filter_all",
            "a[href='#/active']": "filter_active",
            "a[href='#/completed']": "filter_completed",
        }
        if value in selector_map:
            return SimulatedWebElement(self, selector_map[value])
        if value in (".todo-list li", "li"):
            visible = self.visible_items()
            if not visible:
                raise LookupError("No todo items present")
            return SimulatedWebElement(self, "todo_item", visible[0]["id"])
        raise LookupError(f"Element not found for selector: {value}")

    def find_elements(self, by: str, value: str) -> List[SimulatedWebElement]:
        """Locate multiple elements matching the given selector."""
        _ = by
        if value in (".todo-list li", "li"):
            return [
                SimulatedWebElement(self, "todo_item", item["id"])
                for item in self.visible_items()
            ]
        try:
            return [self.find_element(by, value)]
        except LookupError:
            return []

    def save_screenshot(self, filename: str) -> bool:
        """Save a deterministic PNG screenshot representing the current TodoMVC state."""
        from performance_visual import render_todomvc_png  # pylint: disable=import-outside-toplevel

        render_todomvc_png(
            filepath=filename,
            todos=self.visible_items(),
            current_filter=self.current_filter,
            active_count=sum(1 for item in self.todos if not item["completed"]),
        )
        return True

    def quit(self) -> None:
        """Close the WebDriver session."""
        self.todos = []


def create_driver() -> Any:
    """Create a Selenium WebDriver (uses real Chrome if USE_REAL_BROWSER=1, else TodoMVCWebDriver)."""
    if os.environ.get("USE_REAL_BROWSER") == "1":  # pragma: no cover
        from selenium import webdriver  # pylint: disable=import-outside-toplevel
        from selenium.webdriver.chrome.options import Options  # pylint: disable=import-outside-toplevel

        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(options=options)
    return TodoMVCWebDriver()
