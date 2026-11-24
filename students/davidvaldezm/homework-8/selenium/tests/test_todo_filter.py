"""Verify exact filter contents, navigation and empty results."""

import pytest


@pytest.mark.parametrize(
    "name,texts",
    [
        ("All", ["Task 1", "Task 2", "Task 3"]),
        ("Active", ["Task 1", "Task 3"]),
        ("Completed", ["Task 2"]),
    ],
)
def test_filter(mixed, name, texts):
    mixed.filter_by(name)
    mixed.wait_for_todos(texts)
    assert mixed.get_visible_todos() == texts
    mixed.filter_by("All")
    mixed.wait_for_todos(["Task 1", "Task 2", "Task 3"])
    assert mixed.active_count() == 2


def test_empty_filter(todo):
    todo.add_todo("Active task")
    todo.filter_by("Completed")
    todo.wait_for_todos([])
    assert todo.get_todo_count() == 0
    todo.filter_by("All")
    todo.wait_for_todos(["Active task"])
