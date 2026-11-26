from uuid import uuid4


def test_add_todo_increases_count(todo_page):
    starting_count = todo_page.get_todo_count()
    title = f"Learn todo automation {uuid4().hex[:8]}"

    todo_page.add_todo(title)

    assert todo_page.get_todo_count() == starting_count + 1
    assert title in todo_page.get_visible_todos()


def test_add_multiple_todos(todo_page):
    titles = [
        f"First todo {uuid4().hex[:8]}",
        f"Second todo {uuid4().hex[:8]}",
        f"Third todo {uuid4().hex[:8]}",
    ]
    starting_count = todo_page.get_todo_count()

    for title in titles:
        todo_page.add_todo(title)

    assert todo_page.get_todo_count() == starting_count + len(titles)
    assert all(title in todo_page.get_visible_todos() for title in titles)


def test_toggle_todo_completion(todo_page):
    todo_index = todo_page.get_todo_count()
    todo_page.add_todo(f"Toggle todo {uuid4().hex[:8]}")
    assert not todo_page.is_todo_completed(todo_index)

    todo_page.toggle_todo(todo_index)
    assert todo_page.is_todo_completed(todo_index)

    todo_page.toggle_todo(todo_index)
    assert not todo_page.is_todo_completed(todo_index)


def test_complete_multiple_todos(todo_page):
    starting_index = todo_page.get_todo_count()
    initial_active_count = todo_page.get_active_todo_count()
    for title in ("First", "Second", "Third"):
        todo_page.add_todo(f"{title} {uuid4().hex[:8]}")

    todo_page.toggle_todo(starting_index)
    todo_page.toggle_todo(starting_index + 1)

    assert todo_page.is_todo_completed(starting_index)
    assert todo_page.is_todo_completed(starting_index + 1)
    assert not todo_page.is_todo_completed(starting_index + 2)
    assert todo_page.get_active_todo_count() == initial_active_count + 1


def test_delete_todo(todo_page):
    starting_count = todo_page.get_todo_count()
    todo_page.add_todo(f"Delete todo {uuid4().hex[:8]}")

    todo_page.delete_todo(starting_count)

    assert todo_page.get_todo_count() == starting_count


def test_delete_completed_todo(todo_page):
    starting_index = todo_page.get_todo_count()
    active_todo = f"Keep active {uuid4().hex[:8]}"
    completed_todo = f"Delete completed {uuid4().hex[:8]}"
    todo_page.add_todo(active_todo)
    todo_page.add_todo(completed_todo)
    todo_page.toggle_todo(starting_index + 1)

    todo_page.delete_todo(starting_index + 1)

    assert todo_page.get_todo_count() == starting_index + 1
    assert active_todo in todo_page.get_visible_todos()
    assert completed_todo not in todo_page.get_visible_todos()


def test_clear_completed_todos(todo_page):
    starting_index = todo_page.get_todo_count()
    initial_active_count = todo_page.get_active_todo_count()
    active_todo = f"Keep active {uuid4().hex[:8]}"
    completed_todos = [f"Clear completed {uuid4().hex[:8]}" for _ in range(2)]
    todo_page.add_todo(active_todo)
    for title in completed_todos:
        todo_page.add_todo(title)
        todo_page.toggle_todo(todo_page.get_todo_count() - 1)

    todo_page.clear_completed()

    assert todo_page.get_todo_count() == starting_index + 1
    assert todo_page.get_visible_todos()[-1] == active_todo
    assert todo_page.get_active_todo_count() == initial_active_count + 1

def test_active_and_completed_todo(todo_page):
    starting_count = todo_page.get_todo_count()
    active_todo = f"Active todo {uuid4().hex[:8]}"
    completed_todo = f"Completed todo {uuid4().hex[:8]}"
    todo_page.add_todo(active_todo)
    todo_page.add_todo(completed_todo)
    todo_page.toggle_todo(starting_count + 1)

    todo_page.filter_active()
    visible_todos = todo_page.get_visible_todos()
    assert active_todo in visible_todos
    assert completed_todo not in visible_todos

    todo_page.filter_completed()
    visible_todos = todo_page.get_visible_todos()
    assert active_todo not in visible_todos
    assert completed_todo in visible_todos


def test_edit_todo(todo_page):
    todo_index = todo_page.get_todo_count()
    todo_number = uuid4().hex[:8]
    new_text = f"Edited todo {todo_number}"
    todo_page.add_todo(f"Todo to edit {todo_number}")

    todo_page.edit_todo(todo_index, new_text)

    assert new_text in todo_page.get_visible_todos()


def test_cancel_edit_todo(todo_page):
    todo_index = todo_page.get_todo_count()
    original_text = f"Keep original {uuid4().hex[:8]}"
    todo_page.add_todo(original_text)

    todo_page.cancel_edit_todo(todo_index)

    assert todo_page.get_todo_by_index(todo_index) == original_text


def test_filter_all_shows_both_todo_states(todo_page):
    active_todo = f"Active todo {uuid4().hex[:8]}"
    completed_todo = f"Completed todo {uuid4().hex[:8]}"
    todo_page.add_todo(active_todo)
    todo_page.add_todo(completed_todo)
    todo_page.toggle_todo(todo_page.get_todo_count() - 1)

    todo_page.filter_completed()
    todo_page.filter_all()

    visible_todos = todo_page.get_visible_todos()
    assert active_todo in visible_todos
    assert completed_todo in visible_todos

