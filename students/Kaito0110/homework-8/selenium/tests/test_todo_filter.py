def test_all_filter_shows_active_and_completed_todos(todo_page):
    todo_page.add_todo("Active task")
    todo_page.add_todo("Completed task")
    todo_page.toggle_todo(1)
    todo_page.filter_all()

    assert todo_page.get_visible_todos() == ["Active task", "Completed task"]


def test_active_filter_hides_completed_todos(todo_page):
    todo_page.add_todo("Active task")
    todo_page.add_todo("Completed task")
    todo_page.toggle_todo(1)
    todo_page.filter_active()

    assert todo_page.get_visible_todos() == ["Active task"]


def test_completed_filter_hides_active_todos(todo_page):
    todo_page.add_todo("Active task")
    todo_page.add_todo("Completed task")
    todo_page.toggle_todo(1)
    todo_page.filter_completed()

    assert todo_page.get_visible_todos() == ["Completed task"]
