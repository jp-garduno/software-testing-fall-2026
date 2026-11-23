"""Behave step definitions for features/todo.feature, built on the Selenium TodoPage."""

from behave import given, then, when


@given("I am on the todo page")
def step_on_todo_page(context):
    context.todo_page.open_clean()


@when('I add a todo "{text}"')
@given('I have a todo "{text}"')
def step_add_todo(context, text):
    context.todo_page.add_todo(text)


@given("I have the following todos:")
def step_add_todos_from_table(context):
    for row in context.table:
        context.todo_page.add_todo(row["text"])
        if row["completed"] == "true":
            context.todo_page.toggle_todo(context.todo_page.get_todo_count() - 1)


@when("I mark the todo as complete")
def step_complete_todo(context):
    context.todo_page.toggle_todo(0)


@when("I delete the todo")
def step_delete_todo(context):
    context.todo_page.delete_todo(0)


@when('I change the todo to "{text}"')
def step_change_todo(context, text):
    context.todo_page.edit_todo(0, text)


@when('I start editing the todo and type "{text}"')
def step_start_editing(context, text):
    context.todo_page.start_edit(0)
    context.todo_page.type_in_edit(0, text)


@when("I press Escape")
def step_press_escape(context):
    context.todo_page.cancel_edit(0)
    context.todo_page.wait_until_not_editing(0)


@then("the todo should no longer be in edit mode")
def step_not_editing(context):
    assert context.todo_page.wait_until_not_editing(0), "The todo is still being edited"


@when("I clear the completed todos")
def step_clear_completed(context):
    context.todo_page.clear_completed()


@when('I filter by "{name}"')
def step_filter(context, name):
    getattr(context.todo_page, f"filter_{name.lower()}")()


@then("I should see {count:d} todo")
@then("I should see {count:d} todos")
@then("I should see {count:d} todo(s)")
def step_see_count(context, count):
    actual = context.todo_page.get_todo_count()
    assert actual == count, f"Expected {count} todo(s), got {actual}"


@then('the todo should be "{text}"')
@then('the todos should be "{texts}"')
def step_see_texts(context, text=None, texts=None):
    expected = [item.strip() for item in (texts if texts is not None else text).split(",")]
    actual = context.todo_page.get_visible_todos()
    assert actual == expected, f"Expected {expected}, got {actual}"


@then("the todo should be marked as done")
def step_marked_done(context):
    assert context.todo_page.is_completed(0), "The todo is not marked as completed"


@then("the active count should be {count:d}")
def step_active_count(context, count):
    actual = context.todo_page.get_items_left()
    assert actual == count, f"Expected {count} active item(s), got {actual}"
