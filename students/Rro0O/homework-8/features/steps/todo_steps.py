"""Step definitions. They only talk to the page object, never to Selenium directly."""

# Behave builds these decorators at runtime, so pylint cannot see them.
# pylint: disable=not-callable

from behave import given, then, when
from pages.todo_page import TodoPage


@given("I am on the todo page")
def step_open_page(context):
    context.todo_page = TodoPage(context.driver)
    context.todo_page.navigate()


@given('I have a todo "{text}"')
@when('I add a todo "{text}"')
def step_add_todo(context, text):
    context.todo_page.add_todo(text)


@given("I have the following todos")
@given("I have the following todos:")
def step_add_todo_table(context):
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


@when('I change the todo to "{text}"')
def step_edit_todo(context, text):
    context.todo_page.edit_todo(0, text)


@when("I clear the completed todos")
def step_clear_completed(context):
    context.todo_page.clear_completed()


@when('I filter by "{filter_name}"')
def step_filter(context, filter_name):
    actions = {
        "All": context.todo_page.filter_all,
        "Active": context.todo_page.filter_active,
        "Completed": context.todo_page.filter_completed,
    }
    actions[filter_name]()


@then("I should see {count:d} todo")
@then("I should see {count:d} todos")
@then("I should see {count:d} todo(s)")
def step_check_count(context, count):
    actual = context.todo_page.get_todo_count()
    assert actual == count, f"Expected {count} todos, got {actual}"


@then('the todo should be "{text}"')
def step_check_text(context, text):
    actual = context.todo_page.get_visible_todos()
    assert actual == [text], f"Expected ['{text}'], got {actual}"


@then("the todo should be marked as done")
def step_check_done(context):
    assert context.todo_page.is_completed(0), "The todo is not marked as completed"


@then("the active count should be {count:d}")
def step_check_active_count(context, count):
    actual = context.todo_page.get_active_count()
    assert actual == count, f"Expected {count} active todos, got {actual}"
