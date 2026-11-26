"""Step definitions for features/todo.feature (Behave + Selenium Page Object)."""

# Behave builds given/when/then at import time, which pylint cannot see (false "not-callable").
# pylint: disable=not-callable

from behave import given, then, when


def _add(context, text):
    context.todo_page.add_todo(text)
    context.current_index = context.todo_page.get_todo_count() - 1


@given("I am on the todo page")
def step_open_todo_page(context):
    context.todo_page.reset()


@given('I have a todo "{text}"')
def step_have_todo(context, text):
    _add(context, text)


@given("I have the following todos:")
def step_have_todos_table(context):
    for row in context.table:
        _add(context, row["text"])
        if row["completed"].strip().lower() == "true":
            context.todo_page.toggle_todo(context.current_index)


@when('I add a todo "{text}"')
def step_add_todo(context, text):
    _add(context, text)


@when("I mark the todo as complete")
def step_mark_complete(context):
    context.todo_page.toggle_todo(context.current_index)


@when("I delete the todo")
def step_delete_todo(context):
    context.todo_page.delete_todo(context.current_index)


@when('I filter by "{filter_name}"')
def step_filter_by(context, filter_name):
    context.todo_page.apply_filter(filter_name)


@when('I edit the todo to "{text}"')
def step_edit_todo(context, text):
    context.todo_page.edit_todo(context.current_index, text)


@when('I change the todo to "{text}" and press Escape')
def step_change_and_escape(context, text):
    context.todo_page.cancel_edit(context.current_index, text)


@when("I clear the completed todos")
def step_clear_completed(context):
    context.todo_page.clear_completed()


# The feature file says "1 todo", "0 todos" and "3 todo(s)": one step handles all three.
@then("I should see {count:d} todo")
@then("I should see {count:d} todos")
@then("I should see {count:d} todo(s)")
def step_should_see_count(context, count):
    actual = context.todo_page.get_todo_count()
    assert actual == count, f"Expected {count} todo(s), got {actual}"


@then('the todo should be "{text}"')
def step_todo_text(context, text):
    todos = context.todo_page.get_visible_todos()
    assert todos[context.current_index] == text, f"Expected '{text}', got {todos}"


@then("I should see the todos:")
def step_should_see_todos(context):
    expected = [row["text"] for row in context.table]
    actual = context.todo_page.get_visible_todos()
    assert actual == expected, f"Expected {expected}, got {actual}"


@then("the todo should be marked as done")
def step_marked_done(context):
    assert context.todo_page.is_completed(
        context.current_index
    ), "The todo is not marked as completed"


@then("the active count should be {count:d}")
def step_active_count(context, count):
    actual = context.todo_page.get_active_count()
    assert (
        actual == count
    ), f"Expected {count} active todo(s), got {actual} ({context.todo_page.get_counter_text()!r})"


@then("the todo should not be in edit mode")
def step_not_editing(context):
    assert context.todo_page.wait_until_not_editing(
        timeout=1.0
    ), "The edit box is still open"
