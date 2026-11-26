"""Creation, completion, deletion and editing scenarios."""
import pytest


class TestTaskCreation:
    def test_create_single_task(self, todo_page):
        todo_page.add_todo("Buy milk")

        assert todo_page.get_visible_todos() == ["Buy milk"]
        assert todo_page.get_items_left_text() == "1 item left!"

    def test_create_multiple_tasks(self, todo_page):
        todo_page.add_todos("Buy milk", "Walk the dog", "Read a book")

        assert todo_page.get_todo_count() == 3
        assert todo_page.get_items_left_text() == "3 items left!"

    def test_new_tasks_appear_at_end_of_list(self, todo_page):
        todo_page.add_todos("First", "Second")
        todo_page.add_todo("Third")

        assert todo_page.get_visible_todos() == ["First", "Second", "Third"]

    def test_task_text_is_trimmed(self, todo_page):
        todo_page.add_todo("   Water plants   ")

        assert todo_page.get_visible_todos() == ["Water plants"]

    def test_blank_task_is_not_created(self, todo_page):
        todo_page.add_todo("     ")

        assert todo_page.get_todo_count() == 0
        assert not todo_page.is_footer_visible()


class TestTaskCompletion:
    def test_mark_task_as_complete(self, todo_page):
        todo_page.add_todo("Write report")

        todo_page.toggle_todo(0)

        assert todo_page.is_completed(0)
        assert todo_page.get_active_count() == 0

    def test_unmark_completed_task(self, todo_page):
        todo_page.add_todo("Write report")
        todo_page.toggle_todo(0)

        todo_page.toggle_todo(0)

        assert not todo_page.is_completed(0)
        assert todo_page.get_active_count() == 1

    def test_complete_multiple_tasks(self, todo_page):
        todo_page.add_todos("One", "Two", "Three")

        todo_page.toggle_todo(0)
        todo_page.toggle_todo(2)

        assert [todo_page.is_completed(i) for i in range(3)] == [True, False, True]
        assert todo_page.get_active_count() == 1

    def test_toggle_all_completes_every_task(self, todo_page):
        todo_page.add_todos("One", "Two", "Three")

        todo_page.toggle_all()

        assert all(todo_page.is_completed(i) for i in range(3))
        assert todo_page.get_active_count() == 0


class TestTaskDeletion:
    def test_delete_single_task(self, todo_page):
        todo_page.add_todos("Keep me", "Delete me")

        todo_page.delete_todo(1)

        assert todo_page.get_visible_todos() == ["Keep me"]

    def test_delete_completed_task(self, todo_page):
        todo_page.add_todos("Done task", "Pending task")
        todo_page.toggle_todo(0)

        todo_page.delete_todo(0)

        assert todo_page.get_visible_todos() == ["Pending task"]
        assert not todo_page.is_clear_completed_visible()

    def test_clear_all_completed(self, todo_page):
        todo_page.add_todos("Done 1", "Pending", "Done 2")
        todo_page.toggle_todo(0)
        todo_page.toggle_todo(2)

        todo_page.clear_completed()

        assert todo_page.get_visible_todos() == ["Pending"]
        assert todo_page.get_active_count() == 1

    def test_deleting_last_task_hides_footer(self, todo_page):
        todo_page.add_todo("Only task")

        todo_page.delete_todo(0)

        assert todo_page.get_todo_count() == 0
        assert not todo_page.is_footer_visible()


class TestTaskEditing:
    def test_edit_task_text(self, todo_page):
        todo_page.add_todos("Old text", "Untouched")

        todo_page.edit_todo(0, "New text")

        assert todo_page.get_visible_todos() == ["New text", "Untouched"]

    @pytest.mark.known_defect
    @pytest.mark.xfail(
        reason="TodoMVC React has no Escape key handler in the edit field",
        strict=True,
    )
    def test_cancel_edit_with_escape(self, todo_page):
        todo_page.add_todo("Original")
        todo_page.start_edit(0)
        todo_page.type_edit("Discard me")

        todo_page.cancel_edit()

        assert not todo_page.is_editing(), "Escape should close the editor"
        assert todo_page.get_visible_todos() == ["Original"]

    def test_save_edited_task_with_enter(self, todo_page):
        todo_page.add_todo("Draft")
        todo_page.start_edit(0)
        todo_page.type_edit("Final version")

        todo_page.save_edit()

        assert not todo_page.is_editing()
        assert todo_page.get_visible_todos() == ["Final version"]

    def test_save_edited_task_on_blur(self, todo_page):
        todo_page.add_todo("Draft")
        todo_page.start_edit(0)
        todo_page.type_edit("Saved on blur")

        todo_page.save_edit_by_blur()

        assert todo_page.get_visible_todos() == ["Saved on blur"]

    def test_edit_to_empty_text_deletes_task(self, todo_page):
        todo_page.add_todo("Temporary")

        todo_page.edit_todo(0, "")

        assert todo_page.get_todo_count() == 0
