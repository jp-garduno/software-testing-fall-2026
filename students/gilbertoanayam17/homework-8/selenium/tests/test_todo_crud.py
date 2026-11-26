"""Selenium: creating, completing, deleting and editing todos (Part 1, scenarios 1, 2, 3 and 5)."""

import pytest

ESCAPE_DEFECT = (
    "Known defect of this TodoMVC build: Escape is ignored, so the edit field stays open "
    "(the TodoMVC spec says Escape leaves edit mode and discards the change)"
)


class TestTaskCreation:
    """Scenario 1."""

    def test_create_single_task(self, todo_page):
        todo_page.add_todo("Buy milk")

        assert todo_page.get_todo_count() == 1
        assert todo_page.get_active_count() == 1

    def test_create_multiple_tasks(self, todo_page):
        todo_page.add_todos("Buy milk", "Pay rent", "Call the dentist")

        assert todo_page.get_todo_count() == 3
        assert todo_page.get_active_count() == 3

    def test_task_appears_in_list(self, todo_page):
        todo_page.add_todos("Water the plants", "  Walk the dog  ")

        # Shown in the order they were added, with surrounding spaces trimmed.
        assert todo_page.get_visible_todos() == ["Water the plants", "Walk the dog"]


class TestTaskCompletion:
    """Scenario 2."""

    def test_mark_task_as_complete(self, todo_page):
        todo_page.add_todo("Finish the report")

        todo_page.toggle_todo(0)

        assert todo_page.is_completed(0)
        assert todo_page.get_active_count() == 0

    def test_unmark_completed_task(self, todo_page):
        todo_page.add_todo("Finish the report")
        todo_page.toggle_todo(0)

        todo_page.toggle_todo(0)

        assert not todo_page.is_completed(0)
        assert todo_page.get_active_count() == 1

    def test_complete_multiple_tasks(self, todo_page):
        todo_page.add_todos("Wash the car", "Cook dinner", "Read a book")

        todo_page.toggle_todo(0)
        todo_page.toggle_todo(2)

        assert [todo_page.is_completed(i) for i in range(3)] == [True, False, True]
        assert todo_page.get_active_count() == 1


class TestTaskDeletion:
    """Scenario 3."""

    def test_delete_single_task(self, todo_page):
        todo_page.add_todos("Book flights", "Renew passport")

        todo_page.delete_todo(0)

        assert todo_page.get_visible_todos() == ["Renew passport"]

    def test_delete_completed_task(self, todo_page):
        todo_page.add_todos("Book flights", "Renew passport")
        todo_page.toggle_todo(1)

        todo_page.delete_todo(1)

        assert todo_page.get_visible_todos() == ["Book flights"]
        assert todo_page.get_active_count() == 1

    def test_clear_all_completed(self, todo_page):
        todo_page.add_todos("Pack bags", "Print tickets", "Water plants")
        todo_page.toggle_todo(0)
        todo_page.toggle_todo(2)

        todo_page.clear_completed()

        assert todo_page.get_visible_todos() == ["Print tickets"]


class TestTaskEditing:
    """Scenario 5."""

    def test_edit_task_text(self, todo_page):
        todo_page.add_todo("Buy bread")

        todo_page.start_editing(0)
        todo_page.type_edit("Buy whole wheat bread")
        todo_page.confirm_edit()

        assert todo_page.get_visible_todos() == ["Buy whole wheat bread"]

    @pytest.mark.xfail(strict=True, reason=ESCAPE_DEFECT)
    def test_cancel_edit(self, todo_page):
        todo_page.add_todo("Buy bread")

        todo_page.start_editing(0)
        todo_page.type_edit("Buy cake")
        todo_page.cancel_edit()

        assert not todo_page.is_editing(0)
        assert todo_page.get_visible_todos() == ["Buy bread"]

    def test_save_edited_task(self, todo_page):
        todo_page.add_todos("Call grandma", "Send invoice")

        todo_page.start_editing(1)
        todo_page.type_edit("Send invoice #42")
        todo_page.leave_edit()  # the spec saves an edit on blur as well as on Enter

        assert todo_page.get_visible_todos() == ["Call grandma", "Send invoice #42"]
        assert todo_page.get_todo_count() == 2
