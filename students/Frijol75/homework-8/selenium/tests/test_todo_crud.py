"""
Selenium E2E Tests for TodoMVC CRUD Operations (Part 1):
1. Task Creation (single, multiple, list verification)
2. Task Completion (mark complete, unmark completed, complete multiple)
3. Task Deletion (delete single, delete completed, clear all completed)
5. Task Editing (edit task text, cancel edit, save edited task)
"""

import os

SCREENSHOTS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "screenshots",
)


class TestTaskCreation:
    """1. Task Creation scenarios (8 points)."""

    def test_create_single_task(self, todo_page):
        """Create a single task and verify count is 1."""
        todo_page.add_todo("Buy groceries")
        assert todo_page.get_todo_count() == 1
        assert todo_page.get_visible_todos() == ["Buy groceries"]
        assert todo_page.get_active_count() == 1

        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
        todo_page.take_screenshot(os.path.join(SCREENSHOTS_DIR, "selenium_01_single_task.png"))

    def test_create_multiple_tasks(self, todo_page):
        """Create multiple tasks and verify order and count."""
        tasks = ["Write Selenium tests", "Implement Page Object Model", "Run E2E suite"]
        todo_page.add_todos(tasks)

        assert todo_page.get_todo_count() == 3
        assert todo_page.get_visible_todos() == tasks
        assert todo_page.get_active_count() == 3

        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
        todo_page.take_screenshot(os.path.join(SCREENSHOTS_DIR, "selenium_02_multiple_tasks.png"))

    def test_task_appears_in_list(self, todo_page):
        """Verify newly added task appears in the visible todo list immediately."""
        todo_page.add_todo("Review pull request")
        visible = todo_page.get_visible_todos()
        assert "Review pull request" in visible
        assert not todo_page.is_todo_completed(0)


class TestTaskCompletion:
    """2. Task Completion scenarios (8 points)."""

    def test_mark_task_as_complete(self, todo_page):
        """Mark an active task as complete and verify completed status."""
        todo_page.add_todo("Finish homework 8")
        assert not todo_page.is_todo_completed(0)

        todo_page.toggle_todo(0)
        assert todo_page.is_todo_completed(0)
        assert todo_page.get_active_count() == 0

        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
        todo_page.take_screenshot(os.path.join(SCREENSHOTS_DIR, "selenium_03_task_completed.png"))

    def test_unmark_completed_task(self, todo_page):
        """Unmark a completed task and verify it returns to active status."""
        todo_page.add_todo("Pay electricity bill")
        todo_page.toggle_todo(0)
        assert todo_page.is_todo_completed(0)

        todo_page.toggle_todo(0)
        assert not todo_page.is_todo_completed(0)
        assert todo_page.get_active_count() == 1

    def test_complete_multiple_tasks(self, todo_page):
        """Complete multiple tasks selectively."""
        todo_page.add_todos(["Task A", "Task B", "Task C"])
        todo_page.toggle_todo(0)
        todo_page.toggle_todo(2)

        assert todo_page.is_todo_completed(0)
        assert not todo_page.is_todo_completed(1)
        assert todo_page.is_todo_completed(2)
        assert todo_page.get_active_count() == 1


class TestTaskDeletion:
    """3. Task Deletion scenarios (8 points)."""

    def test_delete_single_task(self, todo_page):
        """Delete a single active task and verify list becomes empty."""
        todo_page.add_todo("Temporary task")
        assert todo_page.get_todo_count() == 1

        todo_page.delete_todo(0)
        assert todo_page.get_todo_count() == 0

    def test_delete_completed_task(self, todo_page):
        """Delete a specific completed task while keeping active tasks."""
        todo_page.add_todos(["Keep me", "Delete me when done"])
        todo_page.toggle_todo(1)
        assert todo_page.is_todo_completed(1)

        todo_page.delete_todo(1)
        assert todo_page.get_todo_count() == 1
        assert todo_page.get_visible_todos() == ["Keep me"]

    def test_clear_all_completed(self, todo_page):
        """Clear all completed tasks at once using the 'Clear completed' button."""
        todo_page.add_todos(["Task 1", "Task 2", "Task 3"])
        todo_page.toggle_todo(0)
        todo_page.toggle_todo(1)

        todo_page.clear_completed()
        assert todo_page.get_todo_count() == 1
        assert todo_page.get_visible_todos() == ["Task 3"]


class TestTaskEditing:
    """5. Task Editing scenarios (8 points)."""

    def test_edit_task_text(self, todo_page):
        """Double-click a task to edit its text."""
        todo_page.add_todo("Initial draft")
        todo_page.edit_todo(0, "Updated final version")

        assert todo_page.get_todo_count() == 1
        assert todo_page.get_visible_todos() == ["Updated final version"]

        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
        todo_page.take_screenshot(os.path.join(SCREENSHOTS_DIR, "selenium_04_task_edited.png"))

    def test_cancel_edit(self, todo_page):
        """Cancel an in-progress edit and verify the original text is preserved."""
        todo_page.add_todo("Original task title")
        todo_page.cancel_edit_todo(0, "Discarded change")

        assert todo_page.get_todo_count() == 1
        assert todo_page.get_visible_todos() == ["Original task title"]

    def test_save_edited_task(self, todo_page):
        """Edit and save a specific task in a multi-item list without affecting others."""
        todo_page.add_todos(["First item", "Second item", "Third item"])
        todo_page.edit_todo(1, "Second item (Edited)")

        assert todo_page.get_visible_todos() == [
            "First item",
            "Second item (Edited)",
            "Third item",
        ]

