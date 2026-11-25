class TestTaskCreation:
    def test_create_single_task(self, todo_page):
        todo_page.add_todo("Buy milk")
        assert todo_page.get_todo_count() == 1
        assert "Buy milk" in todo_page.get_visible_todos()

    def test_create_multiple_tasks(self, todo_page):
        tasks = ["Task 1", "Task 2", "Task 3"]
        for task in tasks:
            todo_page.add_todo(task)
        assert todo_page.get_todo_count() == 3
        assert todo_page.get_visible_todos() == tasks

    def test_created_task_appears_in_list(self, todo_page):
        todo_page.add_todo("Prepare presentation")
        visible = todo_page.get_visible_todos()
        assert len(visible) == 1
        assert visible[0] == "Prepare presentation"


class TestTaskCompletion:
    def test_mark_task_as_complete(self, todo_page):
        todo_page.add_todo("Finish homework")
        todo_page.toggle_todo(0)
        assert todo_page.is_todo_completed(0) is True
        assert todo_page.get_active_count() == 0

    def test_unmark_completed_task(self, todo_page):
        todo_page.add_todo("Review PR")
        todo_page.toggle_todo(0)
        assert todo_page.is_todo_completed(0) is True
        todo_page.toggle_todo(0)
        assert todo_page.is_todo_completed(0) is False
        assert todo_page.get_active_count() == 1

    def test_complete_multiple_tasks(self, todo_page):
        todo_page.add_todo("Task A")
        todo_page.add_todo("Task B")
        todo_page.add_todo("Task C")
        todo_page.toggle_todo(0)
        todo_page.toggle_todo(2)
        assert todo_page.is_todo_completed(0) is True
        assert todo_page.is_todo_completed(1) is False
        assert todo_page.is_todo_completed(2) is True
        assert todo_page.get_active_count() == 1


class TestTaskDeletion:
    def test_delete_single_task(self, todo_page):
        todo_page.add_todo("Temporary task")
        todo_page.delete_todo(0)
        assert todo_page.get_todo_count() == 0

    def test_delete_completed_task(self, todo_page):
        todo_page.add_todo("Keep me")
        todo_page.add_todo("Remove me")
        todo_page.toggle_todo(1)
        todo_page.delete_todo(1)
        assert todo_page.get_visible_todos() == ["Keep me"]

    def test_clear_all_completed(self, todo_page):
        todo_page.add_todo("Active task")
        todo_page.add_todo("Done 1")
        todo_page.add_todo("Done 2")
        todo_page.toggle_todo(1)
        todo_page.toggle_todo(2)
        todo_page.clear_completed()
        assert todo_page.get_visible_todos() == ["Active task"]


class TestTaskEditing:
    def test_edit_and_save_task(self, todo_page):
        todo_page.add_todo("Initial text")
        todo_page.edit_todo(0, "Updated text", save=True)
        assert todo_page.get_visible_todos() == ["Updated text"]

    def test_cancel_edit_preserves_original_text(self, todo_page):
        todo_page.add_todo("Original task")
        todo_page.edit_todo(0, "Discarded text", save=False)
        assert todo_page.get_visible_todos() == ["Original task"]