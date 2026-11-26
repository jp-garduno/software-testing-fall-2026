"""Filtering scenarios with independent mixed task lists."""

import pytest


@pytest.fixture
def mixed(todo):
    for text in ("Active 1", "Completed", "Active 2"):
        todo.add_todo(text)
    todo.toggle_todo(1)
    return todo


def test_view_all_tasks(mixed):
    mixed.filter_active()
    mixed.filter_by("All")
    assert mixed.get_visible_todos() == ["Active 1", "Completed", "Active 2"]


def test_view_active_tasks(mixed):
    mixed.filter_active()
    assert mixed.get_visible_todos() == ["Active 1", "Active 2"]
    assert mixed.active_count() == 2


def test_view_completed_tasks(mixed):
    mixed.filter_completed()
    assert mixed.get_visible_todos() == ["Completed"]
    assert mixed.is_completed(0)

