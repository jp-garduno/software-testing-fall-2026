"""Creation, completion, deletion and editing scenarios."""


def test_create_single_task(todo):
    todo.add_todo("Buy milk")
    assert todo.get_todo_count() == 1
    assert todo.get_visible_todos() == ["Buy milk"]


def test_create_multiple_tasks(todo):
    for text in ("Buy milk", "Read book", "Study testing"):
        todo.add_todo(text)
    assert todo.get_visible_todos() == ["Buy milk", "Read book", "Study testing"]


def test_created_task_appears_in_list(todo):
    todo.add_todo("First task")
    todo.add_todo("New task")
    assert "New task" in todo.get_visible_todos()


def test_mark_task_complete(todo):
    todo.add_todo("Read book")
    todo.toggle_todo(0)
    assert todo.is_completed(0)
    assert todo.active_count() == 0


def test_unmark_completed_task(todo):
    todo.add_todo("Read book")
    todo.toggle_todo(0)
    todo.toggle_todo(0)
    assert not todo.is_completed(0)
    assert todo.active_count() == 1


def test_complete_multiple_tasks(todo):
    todo.add_todo("First")
    todo.add_todo("Second")
    todo.toggle_todo(0)
    todo.toggle_todo(1)
    assert all(todo.is_completed(i) for i in range(2))
    assert todo.active_count() == 0


def test_delete_single_task(todo):
    todo.add_todo("Keep")
    todo.add_todo("Delete")
    todo.delete_todo(1)
    assert todo.get_visible_todos() == ["Keep"]


def test_delete_completed_task(todo):
    todo.add_todo("Completed")
    todo.add_todo("Active")
    todo.toggle_todo(0)
    todo.delete_todo(0)
    assert todo.get_visible_todos() == ["Active"]
    assert todo.active_count() == 1


def test_clear_all_completed(todo):
    for text in ("Done 1", "Keep", "Done 2"):
        todo.add_todo(text)
    todo.toggle_todo(0)
    todo.toggle_todo(2)
    todo.clear_completed()
    assert todo.get_visible_todos() == ["Keep"]
    assert not todo.is_completed(0)


def test_edit_task_text(todo):
    todo.add_todo("Original")
    todo.edit_todo(0, "Updated")
    assert todo.get_visible_todos() == ["Updated"]
    assert todo.get_todo_count() == 1


def test_cancel_edit(todo):
    todo.add_todo("Original")
    todo.edit_todo(0, "Discarded", save=False)
    assert todo.get_visible_todos() == ["Original"]


def test_save_edited_task(todo):
    todo.add_todo("Original")
    todo.add_todo("Other")
    todo.toggle_todo(0)
    todo.edit_todo(0, "Saved")
    assert todo.get_visible_todos() == ["Saved", "Other"]
    assert todo.is_completed(0)

