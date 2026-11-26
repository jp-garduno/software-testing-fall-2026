"""Selenium end-to-end tests: creating, completing, deleting and editing todos."""


class TestTaskCreation:
    def test_create_single_task(self, todo_page):
        todo_page.add_todo("Buy milk")

        assert todo_page.get_todo_count() == 1
        assert todo_page.get_visible_todos() == ["Buy milk"]

    def test_create_multiple_tasks_keeps_order(self, todo_page):
        todo_page.add_todos("Buy milk", "Walk the dog", "Pay rent")

        assert todo_page.get_visible_todos() == ["Buy milk", "Walk the dog", "Pay rent"]
        assert todo_page.get_counter_text() == "3 items left!"

    def test_new_task_appears_in_list_and_clears_input(self, todo_page):
        todo_page.add_todo("Read chapter 8")

        assert "Read chapter 8" in todo_page.get_visible_todos()
        assert todo_page.new_todo_value() == ""
        assert todo_page.is_footer_visible()

    def test_blank_task_is_ignored(self, todo_page):
        todo_page.add_todo("   ")

        assert todo_page.get_todo_count() == 0
        assert not todo_page.is_footer_visible()

    def test_task_text_is_trimmed(self, todo_page):
        todo_page.add_todo("   Call mom   ")

        assert todo_page.get_visible_todos() == ["Call mom"]


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
        assert todo_page.get_counter_text() == "1 item left!"

    def test_complete_multiple_tasks(self, todo_page):
        todo_page.add_todos("Task A", "Task B", "Task C")

        todo_page.toggle_todo(0)
        todo_page.toggle_todo(2)

        assert [todo_page.is_completed(i) for i in range(3)] == [True, False, True]
        assert todo_page.get_active_count() == 1

    def test_toggle_all_completes_every_task(self, todo_page):
        todo_page.add_todos("Task A", "Task B")

        todo_page.toggle_all()

        assert todo_page.get_active_count() == 0
        assert all(todo_page.is_completed(i) for i in range(2))


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
        assert todo_page.get_active_count() == 1

    def test_clear_all_completed(self, todo_page):
        todo_page.add_todos("Done 1", "Pending", "Done 2")
        todo_page.toggle_todo(0)
        todo_page.toggle_todo(2)

        todo_page.clear_completed()

        assert todo_page.get_visible_todos() == ["Pending"]
        assert not todo_page.is_clear_completed_visible()

    def test_deleting_last_task_hides_footer(self, todo_page):
        todo_page.add_todo("Only task")

        todo_page.delete_todo(0)

        assert todo_page.get_todo_count() == 0
        assert not todo_page.is_footer_visible()


class TestTaskEditing:
    def test_edit_task_text(self, todo_page):
        todo_page.add_todo("Buy milk")

        todo_page.edit_todo(0, "Buy oat milk")

        assert todo_page.get_visible_todos() == ["Buy oat milk"]

    def test_double_click_enters_edit_mode(self, todo_page):
        todo_page.add_todo("Buy milk")

        field = todo_page.start_editing(0)

        assert todo_page.is_editing(0)
        assert field.get_property("value") == "Buy milk"

    def test_cancel_edit_without_changes_keeps_text(self, todo_page):
        todo_page.add_todos("Buy milk", "Walk the dog")
        todo_page.start_editing(0)

        todo_page.leave_edit_by_clicking_outside()

        assert todo_page.get_visible_todos() == ["Buy milk", "Walk the dog"]
        assert not todo_page.is_editing(0)

    def test_save_edited_task_on_blur(self, todo_page):
        todo_page.add_todo("Buy milk")
        todo_page.type_in_edit(0, "Buy bread")

        todo_page.leave_edit_by_clicking_outside()

        assert todo_page.get_visible_todos() == ["Buy bread"]

    def test_editing_to_empty_text_deletes_task(self, todo_page):
        todo_page.add_todos("Keep", "Remove by editing")

        todo_page.edit_todo(1, "")

        assert todo_page.get_visible_todos() == ["Keep"]

    def test_edited_text_is_trimmed(self, todo_page):
        todo_page.add_todo("Buy milk")

        todo_page.edit_todo(0, "   Buy eggs   ")

        assert todo_page.get_visible_todos() == ["Buy eggs"]
