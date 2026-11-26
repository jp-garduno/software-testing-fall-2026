"""Executable Gherkin steps using the same Selenium Page Object as pytest."""

# Behave creates its decorators dynamically; Pylint sees their initial None values.
# pylint: disable=not-callable
from behave import given, then, when
from pages.todo_page import TodoPage


@given("I am on the todo page")
def open_todo_page(context):
    """Navigate after the scenario hook has created an isolated driver."""
    context.todo_page = TodoPage(context.driver)
    context.todo_page.navigate()


@given('I have a todo "{text}"')
@when('I add a todo "{text}"')
def add_todo(context, text):
    context.todo_page.add_todo(text)


@then("I should see {count:d} todo")
@then("I should see {count:d} todos")
@then("I should see {count:d} todo(s)")
def check_todo_count(context, count):
    actual = context.todo_page.get_todo_count()
    assert actual == count, f"Expected {count} visible todos, got {actual}"


@then('the todo should be "{text}"')
def check_todo_text(context, text):
    assert context.todo_page.get_visible_todos() == [text]


@when("I mark the todo as complete")
def complete_todo(context):
    context.todo_page.toggle_todo(0)


@then("the todo should be marked as done")
def check_completion(context):
    assert context.todo_page.is_completed(0)


@then("the active count should be {count:d}")
def check_active_count(context, count):
    assert context.todo_page.get_active_count() == count


@when("I delete the todo")
def delete_todo(context):
    context.todo_page.delete_todo(0)


@given("I have the following todos:")
def create_todos_from_table(context):
    for index, row in enumerate(context.table):
        context.todo_page.add_todo(row["text"])
        if row["completed"].lower() == "true":
            context.todo_page.toggle_todo(index)


@when('I filter by "{name}"')
def filter_todos(context, name):
    context.todo_page.filter_by(name)


@then('the visible todos should be "{texts}"')
def check_visible_todos(context, texts):
    expected = texts.split(", ")
    context.todo_page.wait_for_todos(expected)
    assert context.todo_page.get_visible_todos() == expected


@when('I edit the todo to "{text}"')
def edit_todo(context, text):
    context.todo_page.begin_edit(0)
    context.todo_page.replace_edit_text(text)


@when("I save the edit")
def save_edit(context):
    context.todo_page.finish_edit()
