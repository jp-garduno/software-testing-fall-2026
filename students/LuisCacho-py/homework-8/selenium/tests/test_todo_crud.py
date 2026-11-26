"""Part 1: Selenium E2E tests for TodoMVC CRUD operations (Creation, Completion, Deletion, Editing)."""

import pytest
from todo_driver import create_driver
from todo_page import TodoPage


@pytest.fixture(name="todo_page")
def fixture_todo_page():
    """Provide an initialized TodoPage navigated to TodoMVC and quit driver after test."""
    driver = create_driver()
    page = TodoPage(driver)
    page.navigate()
    yield page
    driver.quit()


# 1. Task Creation (8 points)
def test_create_single_task(todo_page):
    """Verify creating a single task displays it in the list and increments count."""
    todo_page.add_todo("Buy milk")
    assert todo_page.get_todo_count() == 1
    assert todo_page.get_visible_todos() == ["Buy milk"]
    assert todo_page.get_active_count() == 1


def test_create_multiple_tasks(todo_page):
    """Verify creating multiple tasks preserves insertion order and counts."""
    tasks = ["Write Selenium tests", "Write Playwright tests", "Document BDD scenarios"]
    todo_page.add_todos(tasks)
    assert todo_page.get_todo_count() == 3
    assert todo_page.get_visible_todos() == tasks
    assert todo_page.get_active_count() == 3


def test_ignore_empty_or_whitespace_task(todo_page):
    """Verify submitting empty or whitespace-only text does not add a task."""
    todo_page.add_todo("   ")
    assert todo_page.get_todo_count() == 0
    assert todo_page.get_active_count() == 0


# 2. Task Completion (8 points)
def test_mark_task_as_complete(todo_page):
    """Verify marking a single task as complete updates its status and active counter."""
    todo_page.add_todo("Pay electricity bill")
    assert todo_page.is_todo_completed(0) is False
    todo_page.toggle_todo(0)
    assert todo_page.is_todo_completed(0) is True
    assert todo_page.get_active_count() == 0


def test_unmark_completed_task(todo_page):
    """Verify unmarking a completed task returns it to active state."""
    todo_page.add_todo("Review pull request")
    todo_page.toggle_todo(0)
    assert todo_page.is_todo_completed(0) is True
    todo_page.toggle_todo(0)
    assert todo_page.is_todo_completed(0) is False
    assert todo_page.get_active_count() == 1


def test_complete_multiple_tasks_and_toggle_all(todo_page):
    """Verify completing multiple tasks individually and via toggle_all."""
    todo_page.add_todos(["Task A", "Task B", "Task C"])
    todo_page.toggle_todo(0)
    todo_page.toggle_todo(2)
    assert todo_page.is_todo_completed(0) is True
    assert todo_page.is_todo_completed(1) is False
    assert todo_page.is_todo_completed(2) is True
    assert todo_page.get_active_count() == 1

    # Toggle all marks remaining active as completed, then second toggle unmarks all
    todo_page.toggle_all()
    assert all(todo_page.is_todo_completed(i) for i in range(3))
    assert todo_page.get_active_count() == 0

    todo_page.toggle_all()
    assert not any(todo_page.is_todo_completed(i) for i in range(3))
    assert todo_page.get_active_count() == 3


# 3. Task Deletion (8 points)
def test_delete_single_active_task(todo_page):
    """Verify deleting a single active task removes it from the list."""
    todo_page.add_todos(["Keep me", "Delete me"])
    todo_page.delete_todo(1)
    assert todo_page.get_todo_count() == 1
    assert todo_page.get_visible_todos() == ["Keep me"]


def test_delete_completed_task(todo_page):
    """Verify deleting a completed task removes it and preserves active tasks."""
    todo_page.add_todos(["Done task", "Pending task"])
    todo_page.toggle_todo(0)
    todo_page.delete_todo(0)
    assert todo_page.get_todo_count() == 1
    assert todo_page.get_visible_todos() == ["Pending task"]
    assert todo_page.get_active_count() == 1


def test_clear_all_completed_tasks(todo_page):
    """Verify 'Clear completed' removes all completed tasks while keeping active ones."""
    todo_page.add_todos(["Task 1", "Task 2", "Task 3"])
    todo_page.toggle_todo(0)
    todo_page.toggle_todo(2)
    todo_page.clear_completed()
    assert todo_page.get_todo_count() == 1
    assert todo_page.get_visible_todos() == ["Task 2"]


# 5. Task Editing (8 points)
def test_edit_and_save_task_text(todo_page):
    """Verify double-clicking a task, editing text, and pressing Enter updates the task."""
    todo_page.add_todo("Initial draft")
    todo_page.edit_todo(0, "Final published report")
    assert todo_page.get_visible_todos() == ["Final published report"]


def test_cancel_edit_preserves_original_text(todo_page):
    """Verify pressing Escape while editing restores the original task text."""
    todo_page.add_todo("Original title")
    todo_page.cancel_edit_todo(0, "Discarded edit")
    assert todo_page.get_visible_todos() == ["Original title"]


def test_edit_task_to_empty_deletes_item(todo_page):
    """Verify saving an empty string during edit removes the task item."""
    todo_page.add_todos(["First item", "To be cleared"])
    todo_page.edit_todo(1, "   ")
    assert todo_page.get_todo_count() == 1
    assert todo_page.get_visible_todos() == ["First item"]
