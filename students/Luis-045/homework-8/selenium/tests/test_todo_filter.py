"""The same mixed data must produce exact results for every filter."""

import pytest


@pytest.fixture(name="mixed_todos")
def mixed_todos_page(todo_page):
    """Keep two active tasks around one completed task."""
    for text in ["Task 1", "Task 2", "Task 3"]:
        todo_page.add_todo(text)
    todo_page.toggle_todo(1)
    return todo_page


def test_view_all_tasks(mixed_todos):
    mixed_todos.filter_active()
    mixed_todos.wait_for_todos(["Task 1", "Task 3"])
    mixed_todos.filter_all()
    mixed_todos.wait_for_todos(["Task 1", "Task 2", "Task 3"])
    assert mixed_todos.get_visible_todos() == ["Task 1", "Task 2", "Task 3"]


def test_view_active_tasks_only(mixed_todos):
    mixed_todos.filter_active()
    mixed_todos.wait_for_todos(["Task 1", "Task 3"])
    assert mixed_todos.get_visible_todos() == ["Task 1", "Task 3"]
    assert mixed_todos.get_active_count() == 2


def test_view_completed_tasks_only(mixed_todos):
    mixed_todos.filter_completed()
    mixed_todos.wait_for_todos(["Task 2"])
    assert mixed_todos.get_visible_todos() == ["Task 2"]
    assert mixed_todos.is_completed(0)
