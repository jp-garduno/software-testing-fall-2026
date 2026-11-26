from playwright.sync_api import Browser, Page, Playwright, expect, sync_playwright


class TodoPage:
    NEW_TODO_INPUT = ".new-todo"
    TODO_ITEMS = ".todo-list li"
    FILTER_ALL = "a[href='#/']"
    FILTER_ACTIVE = "a[href='#/active']"
    FILTER_COMPLETED = "a[href='#/completed']"

    def __init__(self, page: Page, browser: Browser, playwright: Playwright):
        self.page = page
        self.browser = browser
        self.playwright = playwright
        self.todo_items = page.locator(self.TODO_ITEMS)

    def close(self):
        self.browser.close()
        self.playwright.stop()

    def navigate(self):
        self.page.goto("https://todomvc.com/examples/react/dist/")

    def add_todo(self, text):
        todo_input = self.page.locator(self.NEW_TODO_INPUT)
        todo_input.wait_for(state="visible")
        todo_input.fill(text)
        todo_input.press("Enter")
        expect(todo_input).to_have_value("")

    def get_todo_count(self):
        return self.todo_items.count()

    def toggle_todo(self, index):
        toggle = self.todo_items.nth(index).locator(".toggle")
        was_checked = toggle.is_checked()
        toggle.click()
        if was_checked:
            expect(toggle).not_to_be_checked()
        else:
            expect(toggle).to_be_checked()

    def delete_todo(self, index):
        starting_count = self.todo_items.count()
        todo_item = self.todo_items.nth(index)
        todo_item.hover()
        todo_item.locator(".destroy").click()
        expect(self.todo_items).to_have_count(starting_count - 1)

    def clear_completed(self):
        starting_count = self.todo_items.count()
        completed_count = starting_count - self.get_active_todo_count()
        if completed_count == 0:
            return

        self.page.locator(".clear-completed").click()
        expect(self.todo_items).to_have_count(starting_count - completed_count)

    def filter_active(self):
        self.page.locator(self.FILTER_ACTIVE).click()
        self.page.wait_for_function("() => location.hash === '#/active'")

    def filter_completed(self):
        self.page.locator(self.FILTER_COMPLETED).click()
        self.page.wait_for_function("() => location.hash === '#/completed'")

    def filter_all(self):
        self.page.locator(self.FILTER_ALL).click()
        self.page.wait_for_function("() => location.hash === '#/'")

    def filter_todos(self, filter_name):
        if filter_name == "All":
            self.filter_all()
        elif filter_name == "Active":
            self.filter_active()
        elif filter_name == "Completed":
            self.filter_completed()
        else:
            raise ValueError(f"Unknown todo filter: {filter_name}")

    def get_visible_todos(self):
        visible_items = self.page.locator(f"{self.TODO_ITEMS}:visible")
        return [
            visible_items.nth(index).locator("label").inner_text().strip()
            for index in range(visible_items.count())
        ]

    def is_todo_completed(self, index):
        return self.todo_items.nth(index).locator(".toggle").is_checked()

    def get_active_todo_count(self):
        return sum(
            not self.todo_items.nth(index).locator(".toggle").is_checked()
            for index in range(self.todo_items.count())
        )

    def edit_todo(self, index, text):
        edit_input = self._open_edit_input(index)
        edit_input.fill(text)
        edit_input.press("Enter")
        expect(self.todo_items.nth(index).locator("label")).to_have_text(text)

    def cancel_edit_todo(self, index):
        original_text = self.get_todo_by_index(index)
        self._open_edit_input(index).press("Escape")
        expect(self.todo_items.nth(index).locator("label")).to_have_text(
            original_text
        )

    def _open_edit_input(self, index):
        todo_item = self.todo_items.nth(index)
        todo_item.locator("label").dblclick()
        edit_input = todo_item.locator("input.edit")
        expect(edit_input).to_be_visible()
        return edit_input

    def get_todo_by_index(self, index):
        return self.todo_items.nth(index).locator("label").inner_text().strip()

    def get_last_todo(self):
        expect(self.todo_items).not_to_have_count(0)
        return self.todo_items.last.locator("label").inner_text().strip()


def create_todo_page():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch()
    page = browser.new_page()
    return TodoPage(page, browser, playwright)
