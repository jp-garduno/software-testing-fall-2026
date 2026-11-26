# pylint: disable=not-callable
from behave import given, then, when
from pages.todo_page import TodoPage


@given("I am on the todo page")
def open_todo_page(context):
    context.todo_page = TodoPage(context.driver)
    context.todo_page.navigate()


@given('I have a todo "{text}"')
@when('I add a todo "{text}"')
def add_todo(context, text):
    context.todo_page.add_todo(text)


@given("I have the following todos:")
def add_todo_table(context):
    for index, row in enumerate(context.table):
        context.todo_page.add_todo(row["text"])
        if row["completed"] == "true":
            context.todo_page.toggle_todo(index)


@when("I mark the todo as complete")
def complete_todo(context):
    context.todo_page.toggle_todo(0)


@when("I delete the todo")
def delete_todo(context):
    context.todo_page.delete_todo(0)


@when('I edit the todo to "{text}"')
def edit_todo(context, text):
    context.todo_page.edit_todo(0, text)


@when('I change the todo to "{text}" and press Escape')
def cancel_edit(context, text):
    context.todo_page.start_editing(0, text)
    context.todo_page.cancel_editing()


@when("I clear the completed todos")
def clear_completed(context):
    context.todo_page.clear_completed()


@when('I filter by "{name}"')
def filter_todos(context, name):
    context.todo_page.filter_by(name)


@then("I should see {count:d} todo")
@then("I should see {count:d} todos")
@then("I should see {count:d} todo(s)")
def check_todo_count(context, count):
    actual = context.todo_page.get_todo_count()
    assert actual == count, f"Expected {count} todos, got {actual}"


@then('the todo should be "{text}"')
def check_todo_text(context, text):
    todos = context.todo_page.get_visible_todos()
    assert todos == [text], f"Expected only {text!r}, got {todos}"


@then("the todo should be marked as done")
def check_todo_done(context):
    assert context.todo_page.is_todo_completed(0), "The todo is not marked as completed"


@then("the todo should not be in edit mode")
def check_not_editing(context):
    assert not context.todo_page.is_editing(), "The todo is still in edit mode"


@then("the active count should be {count:d}")
def check_active_count(context, count):
    actual = int(context.todo_page.items_left_text().split()[0])
    assert actual == count, f"Expected {count} active todos, got {actual}"
