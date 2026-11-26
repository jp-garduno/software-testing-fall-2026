"""Part 1: Selenium E2E tests for TodoMVC Task Filtering (All, Active, Completed)."""

import pytest
from todo_driver import create_driver
from todo_page import TodoPage


@pytest.fixture(name="populated_page")
def fixture_populated_page():
    """Provide a TodoPage pre-populated with 2 active tasks and 1 completed task."""
    driver = create_driver()
    page = TodoPage(driver)
    page.navigate()
    page.add_todos(["Active Task 1", "Completed Task 2", "Active Task 3"])
    page.toggle_todo(1)
    yield page
    driver.quit()


# 4. Task Filtering (8 points)
def test_filter_view_all_tasks(populated_page):
    """Verify 'All' filter displays both active and completed tasks."""
    populated_page.filter_active()
    populated_page.filter_all()
    assert populated_page.get_todo_count() == 3
    assert populated_page.get_visible_todos() == [
        "Active Task 1",
        "Completed Task 2",
        "Active Task 3",
    ]


def test_filter_view_active_tasks_only(populated_page):
    """Verify 'Active' filter displays only uncompleted tasks."""
    populated_page.filter_active()
    assert populated_page.get_todo_count() == 2
    assert populated_page.get_visible_todos() == ["Active Task 1", "Active Task 3"]
    assert populated_page.get_active_count() == 2


def test_filter_view_completed_tasks_only(populated_page):
    """Verify 'Completed' filter displays only completed tasks."""
    populated_page.filter_completed()
    assert populated_page.get_todo_count() == 1
    assert populated_page.get_visible_todos() == ["Completed Task 2"]


@pytest.mark.parametrize(
    "filter_name,expected_titles",
    [
        ("All", ["Active Task 1", "Completed Task 2", "Active Task 3"]),
        ("Active", ["Active Task 1", "Active Task 3"]),
        ("Completed", ["Completed Task 2"]),
    ],
    ids=["filter_all", "filter_active", "filter_completed"],
)
def test_filter_by_name_parameterized(populated_page, filter_name, expected_titles):
    """Verify filter_by_name switches views accurately across All, Active, and Completed."""
    populated_page.filter_by_name(filter_name)
    assert populated_page.get_visible_todos() == expected_titles


def test_completing_task_in_active_view_removes_it_from_view(populated_page):
    """Verify completing a task while in Active view hides it immediately."""
    populated_page.filter_active()
    assert populated_page.get_todo_count() == 2
    populated_page.toggle_todo(0)
    assert populated_page.get_todo_count() == 1
    assert populated_page.get_visible_todos() == ["Active Task 3"]
