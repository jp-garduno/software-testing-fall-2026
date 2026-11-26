"""Step definitions for features/todo.feature, written on top of the Selenium page object.

Each step has its own function name: the step_impl name repeated for every step works in Behave,
but it redefines the same function again and again, which pylint reports as an error.
"""

# given/when/then are created at runtime by behave.step_registry, so pylint cannot tell they are callable.
# pylint: disable=not-callable

from behave import given, then, when
from pages.todo_page import TodoPage


@given("I am on the todo page")
def step_open_todo_page(context):
    context.todo_page = TodoPage(context.driver)
    context.todo_page.navigate()


@given('I have a todo "{text}"')
def step_have_todo(context, text):
    context.todo_page.add_todo(text)


@given("I have the following todos:")
def step_have_todos(context):
    for index, row in enumerate(context.table):
        context.todo_page.add_todo(row["text"])
        if row["completed"] == "true":
            context.todo_page.toggle_todo(index)


@when('I add a todo "{text}"')
def step_add_todo(context, text):
    context.todo_page.add_todo(text)


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


# The feature writes "1 todo", "0 todos" and "<count> todo(s)", and a parse pattern must match the
# whole step, so the same check is registered under the three spellings.
@then("I should see {count:d} todo")
@then("I should see {count:d} todos")
@then("I should see {count:d} todo(s)")
def step_see_todo_count(context, count):
    actual_count = context.todo_page.get_todo_count()
    assert actual_count == count, f"Expected {count}, got {actual_count}"


@then('the todo should be "{text}"')
def step_todo_text(context, text):
    todos = context.todo_page.get_visible_todos()
    assert todos == [text], f"Expected only {text!r}, got {todos}"


@then("the todo should be marked as done")
def step_todo_done(context):
    assert context.todo_page.is_completed(0), "The todo is not shown as completed"


@then("the active count should be {count:d}")
def step_active_count(context, count):
    actual_count = context.todo_page.get_active_count()
    assert actual_count == count, f"Expected {count} items left, got {actual_count}"
