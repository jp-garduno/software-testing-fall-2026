"""Task creation, completion, deletion and editing."""

import pytest

# Task creation


def test_create_single_task(todo_page):
    todo_page.add_todo("Buy milk")

    assert todo_page.get_visible_todos() == ["Buy milk"]
    assert todo_page.get_counter_text() == "1 item left!"


def test_create_multiple_tasks(todo_page):
    todo_page.add_todos("Buy milk", "Walk the dog", "Read book")

    assert todo_page.get_todo_count() == 3
    assert todo_page.get_counter_text() == "3 items left!"


def test_new_task_appears_at_end_of_list_and_input_is_trimmed(todo_page):
    todo_page.add_todos("First", "   Second with spaces   ")

    assert todo_page.get_visible_todos() == ["First", "Second with spaces"]


def test_blank_task_is_not_created(todo_page):
    todo_page.add_todo("     ")

    assert todo_page.get_todo_count() == 0
    assert not todo_page.is_footer_visible()


# Task completion


def test_mark_task_as_complete(todo_page):
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
    todo_page.add_todos("One", "Two", "Three")

    todo_page.toggle_todo(0)
    todo_page.toggle_todo(2)

    assert [todo_page.is_completed(i) for i in range(3)] == [True, False, True]
    assert todo_page.get_active_count() == 1


def test_toggle_all_completes_every_task(todo_page):
    todo_page.add_todos("One", "Two", "Three")

    todo_page.toggle_all()

    assert all(todo_page.is_completed(i) for i in range(3))
    assert todo_page.get_active_count() == 0


# Task deletion


def test_delete_single_task(todo_page):
    todo_page.add_todos("Keep me", "Delete me")

    todo_page.delete_todo(1)

    assert todo_page.get_visible_todos() == ["Keep me"]


def test_delete_completed_task(todo_page):
    todo_page.add_todo("Done task")
    todo_page.toggle_todo(0)

    todo_page.delete_todo(0)

    assert todo_page.get_todo_count() == 0
    assert not todo_page.is_footer_visible()


def test_clear_all_completed_tasks(todo_page):
    todo_page.add_todos("One", "Two", "Three")
    todo_page.toggle_todo(0)
    todo_page.toggle_todo(2)

    todo_page.clear_completed()

    assert todo_page.get_visible_todos() == ["Two"]
    assert not todo_page.is_clear_completed_visible()


# Task editing


def test_edit_task_text(todo_page):
    todo_page.add_todo("Original text")

    todo_page.edit_todo(0, "Updated text")

    assert todo_page.get_visible_todos() == ["Updated text"]


def test_cancel_edit_without_changes_keeps_original(todo_page):
    todo_page.add_todo("Original text")
    todo_page.start_edit(0)

    todo_page.blur_edit()

    assert todo_page.get_visible_todos() == ["Original text"]


@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason="Application defect: the edit field ignores Escape, although the TodoMVC spec says it discards the edit",
)
def test_escape_cancels_edit(todo_page):
    todo_page.add_todo("Original text")
    todo_page.start_edit(0)
    todo_page.type_in_edit(0, "Discard me")

    todo_page.press_escape_in_edit(0)

    assert not todo_page.is_editing(0), "Escape should leave edit mode"
    assert todo_page.get_visible_todos() == ["Original text"]


def test_save_edited_task_on_blur(todo_page):
    todo_page.add_todo("Original text")
    todo_page.start_edit(0)
    todo_page.type_in_edit(0, "Saved by blur")

    todo_page.blur_edit()

    assert todo_page.get_visible_todos() == ["Saved by blur"]


def test_saving_empty_text_deletes_task(todo_page):
    todo_page.add_todo("Soon gone")

    todo_page.edit_todo(0, "")

    assert todo_page.get_todo_count() == 0
