"""Equivalent filtering contracts, with mixed active/completed tasks."""


def mixed_tasks(todo):
    """Create the same deterministic dataset for each independent filter case."""
    for text in ("First", "Second", "Third"):
        todo.add_todo(text)
    todo.toggle_todo(1)


def test_filter_all(todo):
    """All restores all tasks after visiting another filter."""
    mixed_tasks(todo)
    todo.filter_by("Completed")
    todo.filter_by("All")
    todo.assert_todos(["First", "Second", "Third"])


def test_filter_active(todo):
    """Active shows only the two unfinished tasks."""
    mixed_tasks(todo)
    todo.filter_by("Active")
    todo.assert_todos(["First", "Third"])
    assert todo.completed_states() == [False, False]


def test_filter_completed(todo):
    """Completed shows only the finished task."""
    mixed_tasks(todo)
    todo.filter_by("Completed")
    todo.assert_todos(["Second"])
    assert todo.completed_states() == [True]
