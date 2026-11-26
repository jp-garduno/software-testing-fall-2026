"""Selenium E2E tests: All / Active / Completed filters (TodoMVC React)."""

import pytest

ALL_TASKS = ["Task 1", "Task 2", "Task 3"]


@pytest.fixture(name="seeded_page")
def fixture_seeded_page(todo_page):
    """Three todos where only 'Task 2' is completed."""
    todo_page.add_todos(*ALL_TASKS)
    todo_page.toggle_todo(1)
    return todo_page


def test_view_all_tasks(seeded_page):
    seeded_page.filter_active()

    seeded_page.filter_all()

    assert seeded_page.get_visible_todos() == ALL_TASKS
    assert seeded_page.selected_filter() == "All"
    assert seeded_page.current_route() == "#/"


def test_view_active_tasks_only(seeded_page):
    seeded_page.filter_active()

    assert seeded_page.get_visible_todos() == ["Task 1", "Task 3"]
    assert seeded_page.selected_filter() == "Active"
    assert seeded_page.current_route() == "#/active"


def test_view_completed_tasks_only(seeded_page):
    seeded_page.filter_completed()

    assert seeded_page.get_visible_todos() == ["Task 2"]
    assert seeded_page.selected_filter() == "Completed"
    assert seeded_page.current_route() == "#/completed"


@pytest.mark.parametrize(
    "filter_name, expected_todos",
    [("All", ALL_TASKS), ("Active", ["Task 1", "Task 3"]), ("Completed", ["Task 2"])],
)
def test_each_filter_shows_expected_todos(seeded_page, filter_name, expected_todos):
    seeded_page.apply_filter(filter_name)

    assert seeded_page.get_visible_todos() == expected_todos
    # The counter always reports the active todos, whatever the filter.
    assert seeded_page.get_counter_text() == "2 items left!"


def test_completing_task_in_active_view_hides_it(seeded_page):
    seeded_page.filter_active()

    seeded_page.toggle_todo(0)

    assert seeded_page.get_visible_todos() == ["Task 3"]
    assert seeded_page.get_active_count() == 1


def test_clear_completed_from_completed_view(seeded_page):
    seeded_page.filter_completed()

    seeded_page.clear_completed()

    assert seeded_page.get_todo_count() == 0
    seeded_page.filter_all()
    assert seeded_page.get_visible_todos() == ["Task 1", "Task 3"]
