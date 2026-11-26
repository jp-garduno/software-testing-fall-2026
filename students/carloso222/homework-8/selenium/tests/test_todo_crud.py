"""Selenium E2E tests: create, complete, delete and edit todos (TodoMVC React)."""

import pytest

ESCAPE_DEFECT = (
    "DEFECT in TodoMVC React: Escape does not cancel editing. The edit box stays open and the "
    "typed text is saved on blur, although the TodoMVC spec says Escape must discard the change."
)


class TestTaskCreation:
    def test_create_single_task(self, todo_page):
        todo_page.add_todo("Buy milk")

        assert todo_page.get_todo_count() == 1
        assert todo_page.get_visible_todos() == ["Buy milk"]

    def test_create_multiple_tasks(self, todo_page):
        tasks = ["Buy milk", "Walk the dog", "Write the report"]

        todo_page.add_todos(*tasks)

        assert todo_page.get_todo_count() == 3
        assert todo_page.get_visible_todos() == tasks  # same order as typed

    def test_task_appears_in_list_as_active(self, todo_page):
        todo_page.add_todo("Read chapter 8")

        assert "Read chapter 8" in todo_page.get_visible_todos()
        assert not todo_page.is_completed(0)
        assert todo_page.is_footer_visible()
        assert todo_page.get_counter_text() == "1 item left!"

    def test_task_text_is_trimmed(self, todo_page):
        todo_page.add_todo("   Pay rent   ")

        assert todo_page.get_visible_todos() == ["Pay rent"]

    @pytest.mark.parametrize("blank_text", ["", "   "], ids=["empty", "spaces"])
    def test_blank_task_is_not_created(self, todo_page, blank_text):
        todo_page.add_todo(blank_text)

        assert todo_page.get_todo_count() == 0
        assert not todo_page.is_footer_visible()


class TestTaskCompletion:
    def test_mark_task_as_complete(self, todo_page):
        todo_page.add_todo("Finish homework 8")

        todo_page.toggle_todo(0)

        assert todo_page.is_completed(0)
        assert todo_page.get_counter_text() == "0 items left!"
        assert todo_page.is_clear_completed_visible()

    def test_unmark_completed_task(self, todo_page):
        todo_page.add_todo("Finish homework 8")
        todo_page.toggle_todo(0)

        todo_page.toggle_todo(0)

        assert not todo_page.is_completed(0)
        assert todo_page.get_active_count() == 1
        assert not todo_page.is_clear_completed_visible()

    def test_complete_multiple_tasks(self, todo_page):
        todo_page.add_todos("Task A", "Task B", "Task C")

        todo_page.toggle_todo(0)
        todo_page.toggle_todo(2)

        assert todo_page.completion_states() == [True, False, True]
        assert todo_page.get_counter_text() == "1 item left!"

    def test_toggle_all_completes_and_reopens_every_task(self, todo_page):
        todo_page.add_todos("Task A", "Task B", "Task C")

        todo_page.toggle_all()
        assert todo_page.completion_states() == [True, True, True]
        assert todo_page.get_active_count() == 0

        todo_page.toggle_all()
        assert todo_page.completion_states() == [False, False, False]
        assert todo_page.get_active_count() == 3


class TestTaskDeletion:
    def test_delete_single_task(self, todo_page):
        todo_page.add_todo("Task to delete")

        todo_page.delete_todo(0)

        assert todo_page.get_todo_count() == 0
        assert not todo_page.is_footer_visible()

    def test_delete_one_task_keeps_the_others(self, todo_page):
        todo_page.add_todos("Task A", "Task B", "Task C")

        todo_page.delete_todo(1)

        assert todo_page.get_visible_todos() == ["Task A", "Task C"]
        assert todo_page.get_active_count() == 2

    def test_delete_completed_task(self, todo_page):
        todo_page.add_todos("Done task", "Pending task")
        todo_page.toggle_todo(0)

        todo_page.delete_todo(0)

        assert todo_page.get_visible_todos() == ["Pending task"]
        assert todo_page.get_active_count() == 1
        assert not todo_page.is_clear_completed_visible()

    def test_clear_all_completed(self, todo_page):
        todo_page.add_todos("Task A", "Task B", "Task C", "Task D")
        todo_page.toggle_todo(0)
        todo_page.toggle_todo(2)

        todo_page.clear_completed()

        assert todo_page.get_visible_todos() == ["Task B", "Task D"]
        assert todo_page.completion_states() == [False, False]
        assert not todo_page.is_clear_completed_visible()


class TestTaskEditing:
    def test_edit_task_text(self, todo_page):
        todo_page.add_todo("Buy mlk")

        todo_page.edit_todo(0, "Buy milk", commit="enter")

        assert todo_page.get_visible_todos() == ["Buy milk"]
        assert not todo_page.is_editing()

    def test_save_edited_task_on_blur(self, todo_page):
        todo_page.add_todos("Call mom", "Book flights")

        todo_page.edit_todo(1, "  Book flights to Guadalajara  ", commit="blur")

        assert todo_page.get_visible_todos() == [
            "Call mom",
            "Book flights to Guadalajara",
        ]
        assert not todo_page.is_editing()

    def test_edit_keeps_completed_state(self, todo_page):
        todo_page.add_todo("Old title")
        todo_page.toggle_todo(0)

        todo_page.edit_todo(0, "New title")

        assert todo_page.get_visible_todos() == ["New title"]
        assert todo_page.is_completed(0)

    def test_edit_without_changes_keeps_text(self, todo_page):
        todo_page.add_todo("Original text")

        todo_page.edit_todo(0, "Original text")

        assert todo_page.get_visible_todos() == ["Original text"]

    @pytest.mark.known_defect
    @pytest.mark.xfail(reason=ESCAPE_DEFECT, strict=True)
    def test_cancel_edit_with_escape_discards_changes(self, todo_page):
        todo_page.add_todo("Original text")

        todo_page.cancel_edit(0, "Changed text")

        assert todo_page.wait_until_not_editing(
            timeout=1.0
        ), "Escape should close the edit box"
        assert todo_page.get_visible_todos() == ["Original text"]

    def test_clearing_text_while_editing_deletes_task(self, todo_page):
        todo_page.add_todos("Keep me", "Delete me")

        todo_page.edit_todo(1, "")

        assert todo_page.get_visible_todos() == ["Keep me"]
