"""Playwright Page Object for the same TodoMVC React UI contract."""

from playwright.sync_api import expect

from support import BASE_URL, measured


class TodoPage:
    """Use locators and web-first assertions instead of manual sleeps."""

    engine = "playwright"

    def __init__(self, page):
        self.page = page
        self.rows = page.locator(".todo-list li")

    @measured
    def navigate(self):
        """Reset the disposable context and synchronize on the task input."""
        self.page.goto(BASE_URL)
        expect(self.page.locator(".new-todo")).to_be_visible()
        self.page.evaluate("window.localStorage.clear()")
        self.page.reload()
        expect(self.page.locator(".new-todo")).to_be_visible()
        expect(self.rows).to_have_count(0)

    @measured
    def add_todo(self, text):
        """Create one task through the input and Enter key."""
        count = self.get_todo_count()
        self.page.locator(".new-todo").fill(text)
        self.page.locator(".new-todo").press("Enter")
        expect(self.rows).to_have_count(count + 1)

    def get_todo_count(self):
        """Count currently rendered task rows."""
        return self.rows.count()

    def get_visible_todos(self):
        """Read only task labels."""
        return self.rows.locator("label").all_text_contents()

    def completed_states(self):
        """Read the checked state for every rendered task."""
        return [
            self.rows.nth(index).locator(".toggle").is_checked()
            for index in range(self.rows.count())
        ]

    def active_count(self):
        """Read the rendered active item count."""
        return int(self.page.locator(".todo-count").inner_text().split()[0])

    @measured
    def toggle_todo(self, index):
        """Toggle through a real click, then assert the updated checked state."""
        checkbox = self.rows.nth(index).locator(".toggle")
        previous = checkbox.is_checked()
        checkbox.click()
        expect(checkbox).to_be_checked(checked=not previous)

    @measured
    def delete_todo(self, index):
        """Reveal and click the row's delete control."""
        count = self.get_todo_count()
        row = self.rows.nth(index)
        row.hover()
        row.locator(".destroy").click()
        expect(self.rows).to_have_count(count - 1)

    @measured
    def clear_completed(self):
        """Remove completed tasks via the application's footer control."""
        expected = self.completed_states().count(False)
        self.page.locator(".clear-completed").click()
        expect(self.rows).to_have_count(expected)

    @measured
    def filter_by(self, name):
        """Choose an exact filter label and verify its selected state."""
        self.page.get_by_role("link", name=name, exact=True).click()
        expect(self.page.locator(".filters .selected")).to_have_text(name)

    @measured
    def edit_todo(self, index, text, finish="enter"):
        """Commit with Enter/blur or restore the previous text with Escape."""
        self.rows.nth(index).locator("label").dblclick()
        editor = self.page.locator(".todo-list li.editing .edit")
        editor.fill(text)
        if finish == "blur":
            self.page.locator(".new-todo").click()
        else:
            editor.press("Escape" if finish == "escape" else "Enter")
            if finish == "escape":
                self.page.locator(".new-todo").click()
        expect(editor).not_to_be_visible()

    def assert_todos(self, expected):
        """Retry the complete ordered list assertion until the UI settles."""
        expect(self.rows.locator("label")).to_have_text(expected)

    @measured
    def reload(self):
        """Reload while preserving task persistence."""
        self.page.reload()
        expect(self.page.locator(".new-todo")).to_be_visible()

    def screenshot(self, path):
        """Save a real browser capture."""
        self.page.screenshot(path=str(path), full_page=True)

    def page_load_seconds(self):
        """Read the same Navigation Timing metric used in the Selenium adapter."""
        return self.page.evaluate(
            "performance.getEntriesByType('navigation')[0].loadEventEnd / 1000"
        )
