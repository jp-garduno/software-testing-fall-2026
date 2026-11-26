"""Filtering tasks by status."""

import pytest


@pytest.fixture(name="mixed_todos")
def fixture_mixed_todos(todo_page):
    """Three todos where only the second one is completed."""
    todo_page.add_todos("Task 1", "Task 2", "Task 3")
    todo_page.toggle_todo(1)
    return todo_page


def test_view_all_tasks(mixed_todos):
    mixed_todos.filter_active()

    mixed_todos.filter_all()

    assert mixed_todos.get_visible_todos() == ["Task 1", "Task 2", "Task 3"]
    assert mixed_todos.get_selected_filter() == "All"


def test_view_active_tasks_only(mixed_todos):
    mixed_todos.filter_active()

    assert mixed_todos.get_visible_todos() == ["Task 1", "Task 3"]
    assert mixed_todos.get_selected_filter() == "Active"


def test_view_completed_tasks_only(mixed_todos):
    mixed_todos.filter_completed()

    assert mixed_todos.get_visible_todos() == ["Task 2"]
    assert mixed_todos.get_selected_filter() == "Completed"


def test_completing_task_under_active_filter_hides_it(mixed_todos):
    mixed_todos.filter_active()

    mixed_todos.toggle_todo(0)

    assert mixed_todos.get_visible_todos() == ["Task 3"]
    assert mixed_todos.get_active_count() == 1
