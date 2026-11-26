"""Equivalent CRUD contracts executed through the Playwright Page Object."""

import pytest


def test_create_single(todo):
    """Create one task and verify its exact text and active count."""
    todo.add_todo("Buy milk")
    todo.assert_todos(["Buy milk"])
    assert todo.active_count() == 1


def test_create_multiple(todo):
    """Create three independent tasks in insertion order."""
    for text in ("Read", "Write", "Review"):
        todo.add_todo(text)
    todo.assert_todos(["Read", "Write", "Review"])
    assert todo.get_todo_count() == 3


def test_created_task_appears(todo):
    """Task creation trims surrounding whitespace without changing content."""
    todo.add_todo("  Prepare report  ")
    todo.assert_todos(["Prepare report"])
    assert todo.completed_states() == [False]


def test_complete_single(todo):
    """Mark a task complete and verify the remaining counter."""
    todo.add_todo("Read book")
    todo.toggle_todo(0)
    assert todo.completed_states() == [True]
    assert todo.active_count() == 0


def test_uncomplete(todo):
    """A second toggle restores a task to active."""
    todo.add_todo("Read book")
    todo.toggle_todo(0)
    todo.toggle_todo(0)
    assert todo.completed_states() == [False]
    assert todo.active_count() == 1


def test_complete_multiple(todo):
    """Completing two tasks leaves the third active."""
    for text in ("Read", "Write", "Review"):
        todo.add_todo(text)
    todo.toggle_todo(0)
    todo.toggle_todo(1)
    assert todo.completed_states() == [True, True, False]
    assert todo.active_count() == 1


def test_delete_single(todo):
    """Delete an active task and verify the list is empty."""
    todo.add_todo("Remove me")
    todo.delete_todo(0)
    todo.assert_todos([])


def test_delete_completed(todo):
    """Deleting a completed task keeps the other task active."""
    todo.add_todo("Keep")
    todo.add_todo("Remove")
    todo.toggle_todo(1)
    todo.delete_todo(1)
    todo.assert_todos(["Keep"])
    assert todo.completed_states() == [False]


def test_clear_completed(todo):
    """Clear completed removes only completed tasks."""
    for text in ("First", "Keep", "Last"):
        todo.add_todo(text)
    todo.toggle_todo(0)
    todo.toggle_todo(2)
    todo.clear_completed()
    todo.assert_todos(["Keep"])
    assert todo.active_count() == 1


def test_edit_text(todo):
    """Enter commits a new task title."""
    todo.add_todo("Old title")
    todo.edit_todo(0, "New title")
    todo.assert_todos(["New title"])


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="TodoMVC React: Escape then blur saves discarded text; see DEFECTS.md",
)
def test_cancel_edit(todo):
    """Escape discards unsaved edits."""
    todo.add_todo("Original")
    todo.edit_todo(0, "Discarded", finish="escape")
    assert todo.get_visible_todos() == ["Original"]


def test_save_edit(todo):
    """Blur commits the edited title in the visible task list."""
    todo.add_todo("Original")
    todo.edit_todo(0, "Saved", finish="blur")
    todo.assert_todos(["Saved"])
