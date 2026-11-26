"""Executable Gherkin steps using the Selenium page object."""

from behave import given, when, then


@given("I am on the todo page")
def navigate(context):
    context.todo_page.navigate()


@when('I add a todo "{text}"')
@given('I have a todo "{text}"')
def add(context, text):
    context.todo_page.add_todo(text)


@then("I should see {count:d} todo")
@then("I should see {count:d} todos")
@then("I should see {count:d} todo(s)")
def check_count(context, count):
    assert context.todo_page.get_todo_count() == count


@then('the todo should be "{text}"')
def check_text(context, text):
    assert context.todo_page.get_visible_todos() == [text]


@when("I mark the todo as complete")
def complete(context):
    context.todo_page.toggle_todo(0)


@then("the todo should be marked as done")
def check_completed(context):
    assert context.todo_page.is_completed(0)


@then("the active count should be {count:d}")
def check_active(context, count):
    assert context.todo_page.active_count() == count


@when("I delete the todo")
def delete(context):
    context.todo_page.delete_todo(0)


@given("I have the following todos:")
def add_table(context):
    for index, row in enumerate(context.table):
        context.todo_page.add_todo(row["text"])
        if row["completed"] == "true":
            context.todo_page.toggle_todo(index)


@when('I filter by "{filter_name}"')
def filter_todos(context, filter_name):
    context.todo_page.filter_by(filter_name)

