"""Step definitions for features/todo.feature.

Every step delegates to the Selenium Page Object (selenium/pages/todo_page.py), so the
Gherkin layer contains no locators and no waits.
"""

from behave import given, then, when  # pylint: disable=no-name-in-module
from pages.todo_page import TodoPage


@given("I am on the todo page")
def open_todo_page(context):
    context.todo_page = TodoPage(context.driver).navigate()


@given('I have a todo "{text}"')
@when('I add a todo "{text}"')
def add_todo(context, text):
    context.todo_page.add_todo(text)


@given("I have the following todos:")
def add_todo_table(context):
    for row in context.table:
        context.todo_page.add_todo(row["text"])
        if row["completed"].strip().lower() == "true":
            context.todo_page.toggle_todo(context.todo_page.get_todo_count() - 1)


@when("I mark the todo as complete")
def complete_todo(context):
    context.todo_page.toggle_todo(0)


@when("I delete the todo")
def delete_todo(context):
    context.todo_page.delete_todo(0)


@when('I change the todo to "{text}"')
def edit_todo(context, text):
    context.todo_page.edit_todo(0, text)


@when("I start editing the todo and click outside")
def start_and_leave_edit(context):
    context.todo_page.start_editing(0)
    context.todo_page.leave_edit_by_clicking_outside()


@when("I clear the completed todos")
def clear_completed(context):
    context.todo_page.clear_completed()


@when('I filter by "{name}"')
def filter_todos(context, name):
    context.todo_page.filter_by(name)


@then("I should see {count:d} todo")
@then("I should see {count:d} todos")
@then("I should see {count:d} todo(s)")
def check_count(context, count):
    actual = context.todo_page.get_todo_count()
    assert actual == count, f"Expected {count} todo(s), got {actual}"


@then('the todo should be "{text}"')
def check_text(context, text):
    todos = context.todo_page.get_visible_todos()
    assert todos == [text], f"Expected only {text!r}, got {todos}"


@then("the todo should be marked as done")
def check_done(context):
    assert context.todo_page.is_completed(0), "The todo is not marked as completed"


@then("the active count should be {count:d}")
def check_active_count(context, count):
    actual = context.todo_page.get_active_count()
    assert actual == count, f"Expected {count} active, got {actual}"
