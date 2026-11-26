from selenium.webdriver.common.by import By


def test_create_single_todo_and_display_text(todo_page):
    todo_page.add_todo("Buy milk")

    assert todo_page.get_todo_count() == 1
    assert todo_page.get_visible_todos() == ["Buy milk"]


def test_create_multiple_todos(todo_page):
    todo_page.add_todo("Buy milk")
    todo_page.add_todo("Read a book")

    assert todo_page.get_todo_count() == 2
    assert todo_page.get_visible_todos() == ["Buy milk", "Read a book"]


def test_complete_and_uncomplete_todo(todo_page):
    todo_page.add_todo("Test completion")

    todo_page.toggle_todo(0)
    assert todo_page.is_completed(0)
    assert todo_page.get_active_count() == 0

    todo_page.toggle_todo(0)
    assert not todo_page.is_completed(0)
    assert todo_page.get_active_count() == 1


def test_complete_multiple_todos(todo_page):
    todo_page.add_todo("First task")
    todo_page.add_todo("Second task")

    todo_page.toggle_todo(0)
    todo_page.toggle_todo(1)

    assert todo_page.get_active_count() == 0
    assert todo_page.is_completed(0)
    assert todo_page.is_completed(1)


def test_delete_single_todo(todo_page):
    todo_page.add_todo("Remove me")
    todo_page.delete_todo(0)

    assert todo_page.get_todo_count() == 0


def test_delete_completed_todo(todo_page):
    todo_page.add_todo("Completed task")
    todo_page.toggle_todo(0)
    todo_page.delete_todo(0)

    assert todo_page.get_todo_count() == 0


def test_clear_all_completed_todos(todo_page):
    todo_page.add_todo("Completed task")
    todo_page.add_todo("Active task")
    todo_page.toggle_todo(0)
    todo_page.clear_completed()

    assert todo_page.get_visible_todos() == ["Active task"]


def test_edit_todo_text(todo_page):
    todo_page.add_todo("Original task")
    todo_page.edit_todo(0, "Updated task")

    assert todo_page.get_visible_todos() == ["Updated task"]


def test_abandon_unchanged_todo_edit(todo_page):
    todo_page.add_todo("Original task")
    todo_page.edit_todo(0, "Original task", save=False)

    assert todo_page.get_visible_todos() == ["Original task"]
    assert "editing" not in todo_page._todo(0).get_attribute("class").split()


def test_save_edited_todo(todo_page):
    todo_page.add_todo("Draft")
    todo_page.edit_todo(0, "Saved task")

    assert todo_page.get_visible_todos() == ["Saved task"]


def test_save_empty_edit_deletes_todo(todo_page):
    todo_page.add_todo("Remove by empty edit")
    todo_page.edit_todo(0, "")
    todo_page.wait.until(
        lambda driver: len(driver.find_elements(By.CSS_SELECTOR, ".todo-list li")) == 0
    )

    assert todo_page.get_todo_count() == 0
