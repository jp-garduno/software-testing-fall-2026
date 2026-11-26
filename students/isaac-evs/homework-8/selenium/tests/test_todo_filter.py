"""Filtering tasks by All / Active / Completed (Selenium + Page Object Model)."""

import pytest


@pytest.fixture(name="mixed_todos")
def make_mixed_todos(todo_page):
    """Three tasks of which only 'Task 2' is completed."""
    todo_page.add_todos("Task 1", "Task 2", "Task 3")
    todo_page.toggle_todo(1)
    return todo_page


class TestFilterViews:
    def test_view_all_tasks(self, mixed_todos):
        mixed_todos.filter_all()
        assert mixed_todos.get_visible_todos() == ["Task 1", "Task 2", "Task 3"]

    def test_view_active_tasks_only(self, mixed_todos):
        mixed_todos.filter_active()
        assert mixed_todos.get_visible_todos() == ["Task 1", "Task 3"]

    def test_view_completed_tasks_only(self, mixed_todos):
        mixed_todos.filter_completed()
        assert mixed_todos.get_visible_todos() == ["Task 2"]

    @pytest.mark.parametrize(
        "choose_filter, expected_count",
        [("filter_all", 3), ("filter_active", 2), ("filter_completed", 1)],
    )
    def test_each_filter_shows_the_expected_number_of_tasks(self, mixed_todos, choose_filter, expected_count):
        getattr(mixed_todos, choose_filter)()
        assert mixed_todos.get_todo_count() == expected_count

    def test_returning_to_all_restores_every_task(self, mixed_todos):
        mixed_todos.filter_completed()
        mixed_todos.filter_all()
        assert mixed_todos.get_todo_count() == 3

    def test_items_left_counter_ignores_the_filter(self, mixed_todos):
        mixed_todos.filter_completed()
        assert mixed_todos.get_items_left() == 2


class TestFilterBehaviour:
    def test_all_is_selected_by_default(self, todo_page):
        assert todo_page.get_selected_filter() == "All"

    def test_selecting_a_filter_updates_the_route(self, mixed_todos):
        mixed_todos.filter_active()
        assert mixed_todos.get_route() == "#/active"

    def test_opening_a_filter_route_directly_applies_it(self, mixed_todos):
        mixed_todos.navigate("#/completed")
        assert mixed_todos.get_selected_filter() == "Completed"

    def test_completing_a_task_in_the_active_view_removes_it_from_the_view(self, mixed_todos):
        mixed_todos.filter_active()
        mixed_todos.toggle_todo(0)
        assert mixed_todos.get_visible_todos() == ["Task 3"]

    def test_reopening_a_task_in_the_completed_view_removes_it_from_the_view(self, mixed_todos):
        mixed_todos.filter_completed()
        mixed_todos.toggle_todo(0)
        assert mixed_todos.get_todo_count() == 0

    def test_clear_completed_in_the_all_view_leaves_only_active_tasks(self, mixed_todos):
        mixed_todos.clear_completed()
        mixed_todos.filter_completed()
        assert mixed_todos.get_todo_count() == 0
