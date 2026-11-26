"""Playwright: the All / Active / Completed filters (Part 2, same scenarios as Part 1)."""

import pytest
from playwright.sync_api import expect


@pytest.fixture(name="mixed_list")
def fixture_mixed_list(todo_page):
    """Three todos with the middle one completed, the same list the BDD scenario outline uses."""
    todo_page.add_todos("Task 1", "Task 2", "Task 3")
    todo_page.toggle_todo(1)
    return todo_page


def test_view_all_tasks(mixed_list):
    mixed_list.filter_completed()

    mixed_list.filter_all()

    expect(mixed_list.labels).to_have_text(["Task 1", "Task 2", "Task 3"])


def test_view_active_tasks_only(mixed_list):
    mixed_list.filter_active()

    expect(mixed_list.labels).to_have_text(["Task 1", "Task 3"])


def test_view_completed_tasks_only(mixed_list):
    mixed_list.filter_completed()

    expect(mixed_list.labels).to_have_text(["Task 2"])
    expect(mixed_list.item(0)).to_contain_class("completed")
