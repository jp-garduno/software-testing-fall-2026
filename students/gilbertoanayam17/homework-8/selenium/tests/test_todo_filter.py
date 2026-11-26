"""Selenium: the All / Active / Completed filters (Part 1, scenario 4)."""

import pytest


@pytest.fixture(name="mixed_list")
def fixture_mixed_list(todo_page):
    """Three todos with the middle one completed, the same list the BDD scenario outline uses."""
    todo_page.add_todos("Task 1", "Task 2", "Task 3")
    todo_page.toggle_todo(1)
    return todo_page


def test_view_all_tasks(mixed_list):
    mixed_list.filter_completed()

    mixed_list.filter_all()

    assert mixed_list.get_visible_todos() == ["Task 1", "Task 2", "Task 3"]


def test_view_active_tasks_only(mixed_list):
    mixed_list.filter_active()

    assert mixed_list.get_visible_todos() == ["Task 1", "Task 3"]


def test_view_completed_tasks_only(mixed_list):
    mixed_list.filter_completed()

    assert mixed_list.get_visible_todos() == ["Task 2"]
    assert mixed_list.is_completed(0)
