"""Playwright: creating, completing, deleting and editing todos (Part 2, same scenarios as Part 1)."""

import pytest
from playwright.sync_api import expect

ESCAPE_DEFECT = (
    "Known defect of this TodoMVC build: Escape is ignored, so the edit field stays open "
    "(the TodoMVC spec says Escape leaves edit mode and discards the change)"
)


class TestTaskCreation:
    """Scenario 1."""

    def test_create_single_task(self, todo_page):
        todo_page.add_todo("Buy milk")

        expect(todo_page.items).to_have_count(1)
        expect(todo_page.counter).to_have_text("1 item left!")

    def test_create_multiple_tasks(self, todo_page):
        todo_page.add_todos("Buy milk", "Pay rent", "Call the dentist")

        expect(todo_page.items).to_have_count(3)
        expect(todo_page.counter).to_have_text("3 items left!")

    def test_task_appears_in_list(self, todo_page):
        todo_page.add_todos("Water the plants", "  Walk the dog  ")

        # Shown in the order they were added, with surrounding spaces trimmed. to_have_text() would
        # normalize the spaces itself, so the exact texts are compared once both items are rendered.
        expect(todo_page.items).to_have_count(2)
        assert todo_page.get_visible_todos() == ["Water the plants", "Walk the dog"]


class TestTaskCompletion:
    """Scenario 2."""

    def test_mark_task_as_complete(self, todo_page):
        todo_page.add_todo("Finish the report")

        todo_page.toggle_todo(0)

        expect(todo_page.item(0)).to_contain_class("completed")
        expect(todo_page.counter).to_have_text("0 items left!")

    def test_unmark_completed_task(self, todo_page):
        todo_page.add_todo("Finish the report")
        todo_page.toggle_todo(0)

        todo_page.toggle_todo(0)

        expect(todo_page.item(0)).not_to_contain_class("completed")
        expect(todo_page.counter).to_have_text("1 item left!")

    def test_complete_multiple_tasks(self, todo_page):
        todo_page.add_todos("Wash the car", "Cook dinner", "Read a book")

        todo_page.toggle_todo(0)
        todo_page.toggle_todo(2)

        expect(todo_page.item(0)).to_contain_class("completed")
        expect(todo_page.item(1)).not_to_contain_class("completed")
        expect(todo_page.item(2)).to_contain_class("completed")
        expect(todo_page.counter).to_have_text("1 item left!")


class TestTaskDeletion:
    """Scenario 3."""

    def test_delete_single_task(self, todo_page):
        todo_page.add_todos("Book flights", "Renew passport")

        todo_page.delete_todo(0)

        expect(todo_page.labels).to_have_text(["Renew passport"])

    def test_delete_completed_task(self, todo_page):
        todo_page.add_todos("Book flights", "Renew passport")
        todo_page.toggle_todo(1)

        todo_page.delete_todo(1)

        expect(todo_page.labels).to_have_text(["Book flights"])
        expect(todo_page.counter).to_have_text("1 item left!")

    def test_clear_all_completed(self, todo_page):
        todo_page.add_todos("Pack bags", "Print tickets", "Water plants")
        todo_page.toggle_todo(0)
        todo_page.toggle_todo(2)

        todo_page.clear_completed()

        expect(todo_page.labels).to_have_text(["Print tickets"])
        expect(todo_page.clear_completed_button).to_be_hidden()


class TestTaskEditing:
    """Scenario 5."""

    def test_edit_task_text(self, todo_page):
        todo_page.add_todo("Buy bread")

        todo_page.start_editing(0)
        todo_page.type_edit("Buy whole wheat bread")
        todo_page.confirm_edit()

        expect(todo_page.labels).to_have_text(["Buy whole wheat bread"])

    @pytest.mark.xfail(strict=True, reason=ESCAPE_DEFECT)
    def test_cancel_edit(self, todo_page):
        todo_page.add_todo("Buy bread")

        todo_page.start_editing(0)
        todo_page.type_edit("Buy cake")
        todo_page.cancel_edit()

        # Expected to fail, so there is no point in retrying for the default 5 seconds.
        expect(todo_page.edit_input).to_be_hidden(timeout=1000)
        expect(todo_page.labels).to_have_text(["Buy bread"])

    def test_save_edited_task(self, todo_page):
        todo_page.add_todos("Call grandma", "Send invoice")

        todo_page.start_editing(1)
        todo_page.type_edit("Send invoice #42")
        todo_page.leave_edit()  # the spec saves an edit on blur as well as on Enter

        expect(todo_page.labels).to_have_text(["Call grandma", "Send invoice #42"])
