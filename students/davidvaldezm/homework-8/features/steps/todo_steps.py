"""Executable BDD steps delegating all browser interactions to the POM."""

# Behave creates these decorators dynamically; astroid infers them as None.
# pylint: disable=not-callable

from behave import given, then, when


@given("I am on the todo page")
def open_page(context):
    context.todo.navigate()


@given('I have a todo "{text}"')
@when('I add a todo "{text}"')
def add_todo(context, text):
    context.todo.add_todo(text)


@given("I have the following todos:")
def add_table(context):
    for index, row in enumerate(context.table):
        context.todo.add_todo(row["text"])
        if row["completed"] == "true":
            context.todo.toggle_todo(index)


@when("I mark the todo as complete")
def complete(context):
    context.todo.toggle_todo(0)


@then("the todo should be marked as done")
def check_done(context):
    assert context.todo.is_completed(0)


@then("the active count should be {count:d}")
def check_active(context, count):
    assert context.todo.active_count() == count


@when("I delete the todo")
def delete(context):
    context.todo.delete_todo(0)


@when('I filter by "{name}"')
def filter_tasks(context, name):
    context.todo.filter_by(name)


@then("I should see {count:d} todos")
def check_count(context, count):
    context.todo.wait.until(lambda _: context.todo.get_todo_count() == count)
    assert context.todo.get_todo_count() == count


@then('the visible tasks should be "{texts}"')
def check_text(context, texts):
    expected = texts.split(", ")
    context.todo.wait_for_todos(expected)
    assert context.todo.get_visible_todos() == expected


@when('I edit the todo to "{text}"')
def edit(context, text):
    context.todo.edit_todo(0, text)


@when('I cancel editing the todo to "{text}"')
def cancel_edit(context, text):
    context.todo.edit_todo(0, text, save="cancel")


@when("I clear completed tasks")
def clear(context):
    context.todo.clear_completed()
