# pylint: disable=not-callable
import os
import sys

from behave import given, then, when

SELENIUM_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "selenium")
)
if SELENIUM_DIR not in sys.path:
    sys.path.insert(0, SELENIUM_DIR)

from pages.todo_page import TodoPage  # pylint: disable=wrong-import-position


@given("I am on the todo page")
def step_open_todo_page(context):
    context.todo_page = TodoPage(context.driver)
    context.todo_page.navigate()


@given('I have a todo "{text}"')
@when('I add a todo "{text}"')
def step_add_todo(context, text):
    context.todo_page.add_todo(text)


@given("I have the following todos:")
def step_add_multiple_todos(context):
    for index, row in enumerate(context.table):
        context.todo_page.add_todo(row["text"])
        if row["completed"].strip().lower() == "true":
            context.todo_page.toggle_todo(index)


@when("I mark the todo as complete")
def step_complete_first_todo(context):
    context.todo_page.toggle_todo(0)


@when("I delete the todo")
def step_delete_first_todo(context):
    context.todo_page.delete_todo(0)


@when('I filter by "{filter_name}"')
def step_filter_todos(context, filter_name):
    name = filter_name.strip().lower()
    if name == "all":
        context.todo_page.filter_all()
    elif name == "active":
        context.todo_page.filter_active()
    elif name == "completed":
        context.todo_page.filter_completed()
    else:
        raise ValueError(f"Unknown filter: {filter_name}")


@then("I should see {count:d} todo")
@then("I should see {count:d} todos")
@then("I should see {count:d} todo(s)")
def step_verify_todo_count(context, count):
    actual_count = context.todo_page.get_todo_count()
    assert actual_count == count, f"Expected {count}, got {actual_count}"


@then('the todo should be "{text}"')
def step_verify_todo_text(context, text):
    visible = context.todo_page.get_visible_todos()
    assert text in visible, f"Expected '{text}' in {visible}"


@then("the todo should be marked as done")
def step_verify_todo_done(context):
    assert context.todo_page.is_todo_completed(0) is True


@then("the active count should be {count:d}")
def step_verify_active_count(context, count):
    actual = context.todo_page.get_active_count()
    assert actual == count, f"Expected active count {count}, got {actual}"
