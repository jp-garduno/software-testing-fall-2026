"""
Behave BDD Step Definitions for Todo Management feature (Part 3).
"""

import os
import sys
from behave import given, when, then

HOMEWORK_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SELENIUM_DIR = os.path.join(HOMEWORK_DIR, "selenium")
if SELENIUM_DIR not in sys.path:
    sys.path.insert(0, SELENIUM_DIR)

from pages.todo_page import TodoPage  # noqa: E402


@given("I am on the todo page")
def step_on_todo_page(context):
    context.todo_page = TodoPage(context.driver)
    context.todo_page.navigate()


@given('I have a todo "{text}"')
def step_have_single_todo(context, text):
    context.todo_page.add_todo(text)


@given("I have the following todos")
@given("I have the following todos:")
def step_have_multiple_todos(context):
    for index, row in enumerate(context.table):
        context.todo_page.add_todo(row["text"])
        if row["completed"].strip().lower() == "true":
            context.todo_page.toggle_todo(index)


@when('I add a todo "{text}"')
def step_add_todo(context, text):
    context.todo_page.add_todo(text)


@when("I mark the todo as complete")
def step_mark_todo_complete(context):
    context.todo_page.toggle_todo(0)


@when("I delete the todo")
def step_delete_todo(context):
    context.todo_page.delete_todo(0)


@when('I edit the todo to "{new_text}"')
def step_edit_todo(context, new_text):
    context.todo_page.edit_todo(0, new_text)


@when('I filter by "{filter_name}"')
def step_filter_todos(context, filter_name):
    normalized = filter_name.strip().lower()
    if normalized == "all":
        context.todo_page.filter_all()
    elif normalized == "active":
        context.todo_page.filter_active()
    elif normalized == "completed":
        context.todo_page.filter_completed()
    else:
        raise ValueError(f"Unsupported filter: {filter_name}")


@then("I should see {count:d} todo")
@then("I should see {count:d} todos")
@then("I should see {count:d} todo(s)")
def step_verify_todo_count(context, count):
    actual_count = context.todo_page.get_todo_count()
    assert actual_count == count, f"Expected {count} todo(s), got {actual_count}"


@then('the todo should be "{text}"')
def step_verify_todo_text(context, text):
    todos = context.todo_page.get_visible_todos()
    assert text in todos, f"Expected '{text}' in visible todos {todos}"


@then("the todo should be marked as done")
def step_verify_todo_completed(context):
    assert context.todo_page.is_todo_completed(0), "Expected todo item 0 to be completed"


@then("the active count should be {count:d}")
def step_verify_active_count(context, count):
    actual = context.todo_page.get_active_count()
    assert actual == count, f"Expected active count {count}, got {actual}"

