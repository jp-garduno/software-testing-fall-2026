import pytest


def test_add_todo_single_task_appears_in_list(todo_page):
    todo_page.add_todo("Buy milk")

    assert todo_page.get_visible_todos() == ["Buy milk"]


def test_add_todo_several_tasks_keep_entry_order(todo_page):
    todo_page.add_todo("Buy milk", "Walk the dog", "Pay rent")

    assert todo_page.get_visible_todos() == ["Buy milk", "Walk the dog", "Pay rent"]


def test_add_todo_several_tasks_counted_as_items_left(todo_page):
    todo_page.add_todo("Buy milk", "Walk the dog")

    assert todo_page.items_left_text() == "2 items left!"


def test_add_todo_surrounding_spaces_are_trimmed(todo_page):
    todo_page.add_todo("   Call mom   ")

    assert todo_page.get_visible_todos() == ["Call mom"]


def test_add_todo_blank_text_is_ignored(todo_page):
    todo_page.add_todo("     ")

    assert todo_page.get_todo_count() == 0


def test_add_todo_markup_is_shown_as_plain_text(todo_page):
    todo_page.add_todo("<b>Bold</b> plan")

    assert todo_page.get_visible_todos() == ["<b>Bold</b> plan"]


def test_toggle_todo_marks_task_completed(todo_page):
    todo_page.add_todo("Read book")

    todo_page.toggle_todo(0)

    assert (todo_page.is_todo_completed(0), todo_page.items_left_text()) == (True, "0 items left!")


def test_toggle_todo_twice_unmarks_task(todo_page):
    todo_page.add_todo("Read book")
    todo_page.toggle_todo(0)

    todo_page.toggle_todo(0)

    assert (todo_page.is_todo_completed(0), todo_page.items_left_text()) == (False, "1 item left!")


def test_toggle_todo_several_tasks_leaves_others_active(todo_page):
    todo_page.add_todo("Task 1", "Task 2", "Task 3")

    todo_page.toggle_todo(0)
    todo_page.toggle_todo(2)

    assert [todo_page.is_todo_completed(index) for index in range(3)] == [True, False, True]


def test_toggle_todo_single_remaining_task_uses_singular_counter(todo_page):
    todo_page.add_todo("Task 1", "Task 2")

    todo_page.toggle_todo(0)

    assert todo_page.items_left_text() == "1 item left!"


def test_toggle_all_marks_every_task_completed(todo_page):
    todo_page.add_todo("Task 1", "Task 2", "Task 3")

    todo_page.toggle_all()

    assert todo_page.items_left_text() == "0 items left!"


def test_toggle_all_twice_reactivates_every_task(todo_page):
    todo_page.add_todo("Task 1", "Task 2")
    todo_page.toggle_all()

    todo_page.toggle_all()

    assert [todo_page.is_todo_completed(index) for index in range(2)] == [False, False]


def test_delete_todo_removes_only_that_task(todo_page):
    todo_page.add_todo("Keep me", "Delete me", "Keep me too")

    todo_page.delete_todo(1)

    assert todo_page.get_visible_todos() == ["Keep me", "Keep me too"]


def test_delete_todo_completed_task_is_removed(todo_page):
    todo_page.add_todo("Done task", "Open task")
    todo_page.toggle_todo(0)

    todo_page.delete_todo(0)

    assert (todo_page.get_visible_todos(), todo_page.items_left_text()) == (["Open task"], "1 item left!")


def test_clear_completed_removes_every_completed_task(todo_page):
    todo_page.add_todo("Task 1", "Task 2", "Task 3")
    todo_page.toggle_todo(0)
    todo_page.toggle_todo(2)

    todo_page.clear_completed()

    assert todo_page.get_visible_todos() == ["Task 2"]


def test_clear_completed_hidden_without_completed_tasks(todo_page):
    todo_page.add_todo("Task 1")

    assert todo_page.is_clear_completed_visible() is False


def test_open_editor_shows_current_text(todo_page):
    todo_page.add_todo("Original text")

    editor = todo_page.open_editor(0)

    assert (editor.get_attribute("value"), todo_page.is_editing()) == ("Original text", True)


def test_edit_todo_new_text_is_saved(todo_page):
    todo_page.add_todo("Buy milk", "Walk the dog")

    todo_page.edit_todo(0, "Buy oat milk")

    assert todo_page.get_visible_todos() == ["Buy oat milk", "Walk the dog"]


def test_edit_todo_surrounding_spaces_are_trimmed(todo_page):
    todo_page.add_todo("Buy milk")

    todo_page.edit_todo(0, "  Buy bread  ")

    assert todo_page.get_visible_todos() == ["Buy bread"]


def test_edit_todo_empty_text_deletes_task(todo_page):
    todo_page.add_todo("Buy milk", "Walk the dog")

    todo_page.edit_todo(0, "")

    assert todo_page.get_visible_todos() == ["Walk the dog"]


def test_edit_todo_keeps_completed_state(todo_page):
    todo_page.add_todo("Buy milk")
    todo_page.toggle_todo(0)

    todo_page.edit_todo(0, "Buy oat milk")

    assert (todo_page.get_visible_todos(), todo_page.is_todo_completed(0)) == (["Buy oat milk"], True)


@pytest.mark.xfail(
    strict=True,
    reason="Known defect: the TodoMVC spec says Escape discards the edit, but this React build ignores Escape "
    "and keeps the editor open with the changed text",
)
def test_cancel_editing_escape_discards_changes(todo_page):
    todo_page.add_todo("Buy milk")
    todo_page.start_editing(0, "Something else")

    todo_page.cancel_editing()

    assert (todo_page.get_visible_todos(), todo_page.is_editing()) == (["Buy milk"], False)
