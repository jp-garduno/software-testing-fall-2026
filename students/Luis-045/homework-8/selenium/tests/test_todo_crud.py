"""Creation, completion, deletion, editing and input boundaries."""

import os

import pytest

from selenium.common.exceptions import TimeoutException


def test_create_single_task(todo_page):
    todo_page.add_todo("Buy milk")
    assert todo_page.get_visible_todos() == ["Buy milk"]
    assert todo_page.get_active_count() == 1


def test_create_multiple_tasks(todo_page):
    tasks = ["Buy milk", "Read book", "Study testing"]
    for task in tasks:
        todo_page.add_todo(task)
    assert todo_page.get_visible_todos() == tasks
    assert todo_page.get_active_count() == 3


def test_task_appears_in_list(todo_page):
    text = "Revisar tarea 8: café & pruebas"
    todo_page.add_todo(text)
    assert todo_page.get_visible_todos() == [text]
    assert not todo_page.is_completed(0)


def test_mark_task_complete(todo_page):
    todo_page.add_todo("Read book")
    todo_page.toggle_todo(0)
    assert todo_page.is_completed(0)
    assert todo_page.get_active_count() == 0


def test_unmark_completed_task(todo_page):
    todo_page.add_todo("Read book")
    todo_page.toggle_todo(0)
    todo_page.toggle_todo(0)
    assert not todo_page.is_completed(0)
    assert todo_page.get_active_count() == 1


def test_complete_multiple_tasks(todo_page):
    todo_page.add_todo("First")
    todo_page.add_todo("Second")
    todo_page.toggle_todo(0)
    todo_page.toggle_todo(1)
    assert all(todo_page.is_completed(index) for index in range(2))
    assert todo_page.get_active_count() == 0


def test_delete_single_task(todo_page):
    todo_page.add_todo("Keep")
    todo_page.add_todo("Remove")
    todo_page.delete_todo(1)
    assert todo_page.get_visible_todos() == ["Keep"]
    assert todo_page.get_active_count() == 1


def test_delete_completed_task(todo_page):
    todo_page.add_todo("Keep")
    todo_page.add_todo("Done")
    todo_page.toggle_todo(1)
    todo_page.delete_todo(1)
    assert todo_page.get_visible_todos() == ["Keep"]
    assert todo_page.get_active_count() == 1


def test_clear_all_completed(todo_page):
    for task in ["Done one", "Keep", "Done two"]:
        todo_page.add_todo(task)
    todo_page.toggle_todo(0)
    todo_page.toggle_todo(2)
    todo_page.clear_completed()
    assert todo_page.get_visible_todos() == ["Keep"]
    assert todo_page.get_active_count() == 1


def test_edit_task_text_and_save_on_blur(todo_page):
    todo_page.add_todo("Old title")
    todo_page.begin_edit(0)
    todo_page.replace_edit_text("Updated title")
    assert todo_page.get_edit_text() == "Updated title"
    todo_page.blur_edit()
    assert todo_page.get_visible_todos() == ["Updated title"]


@pytest.mark.xfail(
    condition=os.getenv("VERIFY_KNOWN_DEFECTS") != "1",
    raises=TimeoutException,
    strict=True,
    reason="TODO-001: deployed TodoMVC ignores Escape in the inline editor",
)
def test_cancel_edit(todo_page):
    todo_page.add_todo("Original title")
    todo_page.begin_edit(0)
    todo_page.replace_edit_text("Discard this draft")
    todo_page.cancel_edit()
    assert todo_page.get_visible_todos() == ["Original title"]


def test_save_edited_task(todo_page):
    todo_page.add_todo("Old title")
    todo_page.begin_edit(0)
    todo_page.replace_edit_text("Saved title")
    todo_page.finish_edit()
    todo_page.wait_for_todos(["Saved title"])
    assert todo_page.get_visible_todos() == ["Saved title"]


def test_ignore_whitespace_only_task(todo_page):
    todo_page.add_todo("   ")
    assert todo_page.get_todo_count() == 0


def test_trim_new_task_text(todo_page):
    todo_page.add_todo("  Trim this title  ")
    assert todo_page.get_visible_todos() == ["Trim this title"]


def test_empty_edit_deletes_task(todo_page):
    todo_page.add_todo("Remove by editing")
    todo_page.begin_edit(0)
    todo_page.replace_edit_text("")
    todo_page.finish_edit()
    todo_page.wait_for_todos([])
    assert todo_page.get_todo_count() == 0
