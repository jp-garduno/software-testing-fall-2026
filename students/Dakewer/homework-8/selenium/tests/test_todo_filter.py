"""Filtering scenarios: All / Active / Completed."""
import pytest


@pytest.fixture(name="mixed_todos")
def fixture_mixed_todos(todo_page):
    """Three todos where only the middle one is completed."""
    todo_page.add_todos("Task 1", "Task 2", "Task 3")
    todo_page.toggle_todo(1)
    return todo_page


class TestTaskFiltering:
    def test_view_all_tasks(self, mixed_todos):
        mixed_todos.filter_active()

        mixed_todos.filter_all()

        assert mixed_todos.get_visible_todos() == ["Task 1", "Task 2", "Task 3"]

    def test_view_active_tasks_only(self, mixed_todos):
        mixed_todos.filter_active()

        assert mixed_todos.get_visible_todos() == ["Task 1", "Task 3"]

    def test_view_completed_tasks_only(self, mixed_todos):
        mixed_todos.filter_completed()

        assert mixed_todos.get_visible_todos() == ["Task 2"]

    @pytest.mark.parametrize("name", ["All", "Active", "Completed"])
    def test_selected_filter_is_highlighted(self, mixed_todos, name):
        getattr(mixed_todos, f"filter_{name.lower()}")()

        assert mixed_todos.get_selected_filter() == name

    def test_completing_task_removes_it_from_active_view(self, mixed_todos):
        mixed_todos.filter_active()

        mixed_todos.toggle_todo(0)

        assert mixed_todos.get_visible_todos() == ["Task 3"]

    def test_empty_completed_view_keeps_footer(self, todo_page):
        todo_page.add_todo("Not done yet")

        todo_page.filter_completed()

        assert todo_page.get_todo_count() == 0
        assert todo_page.is_footer_visible()
