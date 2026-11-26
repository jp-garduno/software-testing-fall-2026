# Behave creates the step decorators at runtime, so pylint cannot see that they are callable.
# pylint: disable=not-callable
from behave import given, then, use_step_matcher, when

from pages.todo_page import TodoPage


@given("I am on the todo page")
def step_open_todo_page(context):
    context.todo_page = TodoPage(context.driver)
    context.todo_page.navigate()


@given('I have a todo "{text}"')
@when('I add a todo "{text}"')
def step_add_todo(context, text):
    context.todo_page.add_todo(text)


@given("I have the following todos:")
def step_add_todos_from_table(context):
    for index, row in enumerate(context.table):
        context.todo_page.add_todo(row["text"])
        if row["completed"].strip().lower() == "true":
            context.todo_page.toggle_todo(index)


@when("I mark the todo as complete")
def step_complete_todo(context):
    context.todo_page.toggle_todo(0)


@when("I delete the todo")
def step_delete_todo(context):
    context.todo_page.delete_todo(0)


@when('I filter by "{name}"')
def step_filter_by(context, name):
    filters = {
        "All": context.todo_page.filter_all,
        "Active": context.todo_page.filter_active,
        "Completed": context.todo_page.filter_completed,
    }
    filters[name]()


# One regex step covers "1 todo", "0 todos" and "2 todo(s)".
use_step_matcher("re")


@then(r"I should see (?P<count>\d+) todo(?:s|\(s\))?")
def step_check_todo_count(context, count):
    actual = context.todo_page.get_todo_count()
    assert actual == int(count), f"Expected {count} todos, got {actual}"


use_step_matcher("parse")


@then('the todo should be "{text}"')
def step_check_todo_text(context, text):
    todos = context.todo_page.get_visible_todos()
    assert todos == [text], f"Expected only '{text}', got {todos}"


@then("the todo should be marked as done")
def step_check_todo_done(context):
    assert context.todo_page.is_completed(0), "The todo is not marked as completed"


@then("the active count should be {count:d}")
def step_check_active_count(context, count):
    actual = context.todo_page.get_active_count()
    assert actual == count, f"Expected {count} active todos, got {actual}"
