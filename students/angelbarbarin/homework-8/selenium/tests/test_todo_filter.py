"""Selenium end-to-end tests: All / Active / Completed filters."""

import pytest


@pytest.fixture(name="mixed_list")
def fixture_mixed_list(todo_page):
    """Three todos, the middle one completed."""
    todo_page.add_todos("Task 1", "Task 2", "Task 3")
    todo_page.toggle_todo(1)
    return todo_page


def test_view_all_tasks(mixed_list):
    mixed_list.filter_all()

    assert mixed_list.get_visible_todos() == ["Task 1", "Task 2", "Task 3"]
    assert mixed_list.selected_filter() == "All"


def test_view_active_tasks_only(mixed_list):
    mixed_list.filter_active()

    assert mixed_list.get_visible_todos() == ["Task 1", "Task 3"]
    assert mixed_list.current_route() == "#/active"


def test_view_completed_tasks_only(mixed_list):
    mixed_list.filter_completed()

    assert mixed_list.get_visible_todos() == ["Task 2"]
    assert mixed_list.current_route() == "#/completed"


def test_all_is_selected_by_default(todo_page):
    todo_page.add_todo("Anything")

    assert todo_page.selected_filter() == "All"


def test_completing_task_in_active_view_removes_it(mixed_list):
    mixed_list.filter_active()

    mixed_list.toggle_todo(0)

    assert mixed_list.get_visible_todos() == ["Task 3"]


def test_new_task_in_completed_view_is_not_shown(mixed_list):
    mixed_list.filter_completed()

    mixed_list.add_todo("Task 4")  # it is active, so the Completed view must not show it

    assert mixed_list.get_visible_todos() == ["Task 2"]
    mixed_list.filter_all()
    assert mixed_list.get_todo_count() == 4


def test_clear_completed_from_completed_view_empties_it(mixed_list):
    mixed_list.filter_completed()

    mixed_list.clear_completed()

    assert mixed_list.get_todo_count() == 0
    mixed_list.filter_all()
    assert mixed_list.get_visible_todos() == ["Task 1", "Task 3"]


@pytest.mark.parametrize(
    "filter_name,expected",
    [("All", ["Task 1", "Task 2", "Task 3"]), ("Active", ["Task 1", "Task 3"]), ("Completed", ["Task 2"])],
)
def test_filter_by_name(mixed_list, filter_name, expected):
    mixed_list.filter_by(filter_name)

    assert mixed_list.get_visible_todos() == expected


def test_unknown_filter_name_is_rejected(todo_page):
    with pytest.raises(ValueError, match="Unknown filter"):
        todo_page.filter_by("Archived")
