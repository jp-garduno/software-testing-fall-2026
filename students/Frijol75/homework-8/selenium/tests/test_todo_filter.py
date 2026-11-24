"""
Selenium E2E Tests for TodoMVC Filtering Operations (Part 1 - Section 4):
4. Task Filtering (8 points):
   - View all tasks
   - View active tasks only
   - View completed tasks only
"""

import os

SCREENSHOTS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "screenshots",
)


class TestTaskFiltering:
    """4. Task Filtering scenarios (8 points)."""

    def test_view_all_tasks(self, todo_page):
        """Verify 'All' filter displays both active and completed tasks."""
        todo_page.add_todos(["Active Task 1", "Completed Task 2", "Active Task 3"])
        todo_page.toggle_todo(1)

        todo_page.filter_active()
        assert todo_page.get_todo_count() == 2

        todo_page.filter_all()
        assert todo_page.get_todo_count() == 3
        assert todo_page.get_visible_todos() == [
            "Active Task 1",
            "Completed Task 2",
            "Active Task 3",
        ]

    def test_view_active_tasks_only(self, todo_page):
        """Verify 'Active' filter hides completed tasks and shows only active ones."""
        todo_page.add_todos(["Write documentation", "Fix bug #42", "Deploy release"])
        todo_page.toggle_todo(1)  # Mark 'Fix bug #42' as completed

        todo_page.filter_active()
        assert todo_page.get_todo_count() == 2
        assert todo_page.get_visible_todos() == ["Write documentation", "Deploy release"]
        assert todo_page.get_active_count() == 2

        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
        todo_page.take_screenshot(os.path.join(SCREENSHOTS_DIR, "selenium_05_filter_active.png"))

    def test_view_completed_tasks_only(self, todo_page):
        """Verify 'Completed' filter displays only completed tasks."""
        todo_page.add_todos(["Morning standup", "Code review", "Update dependencies"])
        todo_page.toggle_todo(0)
        todo_page.toggle_todo(2)

        todo_page.filter_completed()
        assert todo_page.get_todo_count() == 2
        assert todo_page.get_visible_todos() == ["Morning standup", "Update dependencies"]
        assert todo_page.get_active_count() == 1

        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
        todo_page.take_screenshot(os.path.join(SCREENSHOTS_DIR, "selenium_06_filter_completed.png"))
