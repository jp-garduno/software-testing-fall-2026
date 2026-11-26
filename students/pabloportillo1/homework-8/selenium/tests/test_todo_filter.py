import pytest


@pytest.fixture(name="mixed_todos")
def fixture_mixed_todos(todo_page):
    todo_page.add_todo("Task 1", "Task 2", "Task 3")
    todo_page.toggle_todo(1)
    return todo_page


@pytest.mark.parametrize(
    "filter_name, expected_todos",
    [
        ("All", ["Task 1", "Task 2", "Task 3"]),
        ("Active", ["Task 1", "Task 3"]),
        ("Completed", ["Task 2"]),
    ],
)
def test_filter_by_shows_matching_tasks(mixed_todos, filter_name, expected_todos):
    mixed_todos.filter_by(filter_name)

    assert mixed_todos.get_visible_todos() == expected_todos


@pytest.mark.parametrize("filter_name", ["All", "Active", "Completed"])
def test_filter_by_highlights_chosen_filter(mixed_todos, filter_name):
    mixed_todos.filter_by(filter_name)

    assert mixed_todos.selected_filter() == filter_name


def test_filter_active_completing_task_hides_it(mixed_todos):
    mixed_todos.filter_active()

    mixed_todos.toggle_todo(0)

    assert mixed_todos.get_visible_todos() == ["Task 3"]


def test_filter_completed_new_task_is_not_listed(mixed_todos):
    mixed_todos.filter_completed()

    mixed_todos.add_todo("Task 4")

    assert (mixed_todos.get_visible_todos(), mixed_todos.items_left_text()) == (["Task 2"], "3 items left!")


def test_filter_all_after_other_filter_lists_every_task_again(mixed_todos):
    mixed_todos.filter_completed()

    mixed_todos.filter_by("All")

    assert mixed_todos.get_todo_count() == 3


def test_filter_active_counter_ignores_filter(mixed_todos):
    mixed_todos.filter_completed()

    assert mixed_todos.items_left_text() == "2 items left!"
