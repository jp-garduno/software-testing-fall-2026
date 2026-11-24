"""Equivalent Selenium and Playwright acceptance scenarios."""

import pytest


def test_create_single(todo):
    todo.add_todo("Buy milk")
    assert todo.get_visible_todos() == ["Buy milk"]
    assert todo.get_todo_count() == 1


def test_create_multiple(todo):
    for text in ["Read", "Write", "Review"]:
        todo.add_todo(text)
    assert todo.get_visible_todos() == ["Read", "Write", "Review"]
    assert todo.active_count() == 3


def test_complete_task(todo):
    todo.add_todo("Read")
    todo.toggle_todo(0)
    assert todo.is_completed(0)
    assert todo.active_count() == 0


def test_uncomplete_task(todo):
    todo.add_todo("Read")
    todo.toggle_todo(0)
    todo.toggle_todo(0)
    assert not todo.is_completed(0)
    assert todo.active_count() == 1


def test_complete_all(todo):
    for text in ["Read", "Write", "Review"]:
        todo.add_todo(text)
    todo.complete_all()
    assert all(todo.is_completed(i) for i in range(3))
    assert todo.active_count() == 0


def test_delete_single(todo):
    todo.add_todo("Delete me")
    todo.delete_todo(0)
    assert todo.get_visible_todos() == []


def test_delete_completed(todo):
    todo.add_todo("Delete me")
    todo.toggle_todo(0)
    todo.delete_todo(0)
    assert todo.get_todo_count() == 0


def test_clear_completed(mixed):
    mixed.clear_completed()
    assert mixed.get_visible_todos() == ["Task 1", "Task 3"]
    assert mixed.active_count() == 2


def test_edit_enter(todo):
    todo.add_todo("Draft")
    todo.edit_todo(0, "Final")
    assert todo.get_visible_todos() == ["Final"]


@pytest.mark.xfail(
    strict=True,
    reason="React demo defect: Escape leaves the editor open and does not cancel",
)
def test_edit_cancel(todo):
    todo.add_todo("Original")
    todo.edit_todo(0, "Discard", save="cancel")
    assert todo.get_visible_todos() == ["Original"]


def test_edit_blur(todo):
    todo.add_todo("Draft")
    todo.edit_todo(0, "Saved on blur", save="blur")
    assert todo.get_visible_todos() == ["Saved on blur"]


def test_blank_creation(todo):
    todo.add_todo("   ")
    assert todo.get_todo_count() == 0


def test_trim_creation(todo):
    todo.add_todo("  Trim me  ")
    assert todo.get_visible_todos() == ["Trim me"]


def test_blank_edit_deletes(todo):
    todo.add_todo("Remove")
    todo.edit_todo(0, "   ")
    assert todo.get_todo_count() == 0


def test_duplicate_tasks(todo):
    todo.add_todo("Repeated")
    todo.add_todo("Repeated")
    todo.delete_todo(0)
    assert todo.get_visible_todos() == ["Repeated"]
