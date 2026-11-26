"""Page Object for TodoMVC React, driven with Playwright (sync API).

Playwright waits for every element to be visible, enabled and stable before acting on it, so the
methods below contain no waits. Assertions belong to the tests, which use expect() on the locators
this class exposes and are retried until they pass or time out.
"""

from playwright.sync_api import Page

# The URL in the assignment (/examples/react/) now answers 404. The React build is served from dist/.
APP_URL = "https://todomvc.com/examples/react/dist/"


class TodoPage:
    """What a user can do and see on the todo list."""

    def __init__(self, page: Page):
        self.page = page
        self.new_todo_input = page.locator(".new-todo")
        self.items = page.locator(".todo-list li")
        self.labels = page.locator(".todo-list li label")
        self.edit_input = page.locator(".todo-list li .edit")
        self.counter = page.locator(".todo-count")
        self.clear_completed_button = page.locator(".clear-completed")

    def navigate(self):
        """Load a fresh copy of the app. Todos only live in memory, so every load starts empty."""
        self.page.goto(APP_URL)

    def item(self, index):
        """Locator of the todo at the given position, for expect() assertions."""
        return self.items.nth(index)

    # ------------------------------------------------------------------ creating

    def add_todo(self, text):
        """Type a todo and press Enter."""
        self.new_todo_input.fill(text)
        self.new_todo_input.press("Enter")

    def add_todos(self, *texts):
        """Add several todos in the given order."""
        for text in texts:
            self.add_todo(text)

    # ---------------------------------------------------- completing and deleting

    def toggle_todo(self, index):
        """Click the round checkbox of a todo."""
        self.item(index).locator(".toggle").click()

    def delete_todo(self, index):
        """Hover a todo to reveal its destroy button, then click it."""
        todo = self.item(index)
        todo.hover()
        todo.locator(".destroy").click()

    def clear_completed(self):
        """Press "Clear completed"."""
        self.clear_completed_button.click()

    # ------------------------------------------------------------------- editing

    def start_editing(self, index):
        """Double-click the todo text to open its edit field."""
        self.item(index).locator("label").dblclick()

    def type_edit(self, text):
        """Replace the text in the open edit field without saving it yet."""
        self.edit_input.fill(text)

    def confirm_edit(self):
        """Save the edit with Enter."""
        self.edit_input.press("Enter")

    def cancel_edit(self):
        """Press Escape, which the TodoMVC spec says discards the edit."""
        self.edit_input.press("Escape")

    def leave_edit(self):
        """Click outside the edit field (on the heading) so it loses focus."""
        self.page.locator(".header h1").click()

    # ----------------------------------------------------------------- filtering

    def filter_all(self):
        """Show all todos."""
        self._filter_link("All").click()

    def filter_active(self):
        """Show only active todos."""
        self._filter_link("Active").click()

    def filter_completed(self):
        """Show only completed todos."""
        self._filter_link("Completed").click()

    def _filter_link(self, name):
        return self.page.locator(".filters").get_by_role("link", name=name, exact=True)

    # ------------------------------------------------------------------- reading

    def get_todo_count(self):
        """Number of todos rendered right now (no retry; tests prefer expect().to_have_count)."""
        return self.items.count()

    def get_visible_todos(self):
        """Texts of the todos rendered right now (no retry; tests prefer expect().to_have_text)."""
        return self.labels.all_text_contents()
