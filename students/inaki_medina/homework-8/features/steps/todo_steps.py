# features/steps/todo_steps.py
from behave import given, when, then

@given('I am on the todo page')
def step_impl(context):
    context.todo_page.navigate()

@when('I add a todo "{text}"')
def step_impl(context, text):
    context.todo_page.add_todo(text)

@then('I should see {count:d} todo')
def step_impl(context, count):
    actual_count = len(context.todo_page.get_visible_todos())
    assert actual_count == count, f"Expected {count}, got {actual_count}"

@then('I should see {count:d} todos')
@then('I should see {count:d} todo(s)')
def step_impl(context, count):
    actual_count = len(context.todo_page.get_visible_todos())
    assert actual_count == count, f"Expected {count}, got {actual_count}"

@then('the todo should be "{text}"')
def step_impl(context, text):
    assert text == context.todo_page.get_last_todo()

@given('I have a todo "{text}"')
def step_impl(context, text):
    context.todo_page.add_todo(text)

@when('I mark the todo as complete')
def step_impl(context):
    todo_index = context.todo_page.get_todo_count() - 1
    context.todo_page.toggle_todo(todo_index)

@then('the todo should be marked as done')
def step_impl(context):
    todo_index = context.todo_page.get_todo_count() - 1
    assert context.todo_page.is_todo_completed(todo_index)

@then('the active count should be {count:d}')
def step_impl(context, count):
    actual_count = context.todo_page.get_active_todo_count()
    assert actual_count == count, f"Expected {count} active todos, got {actual_count}"

@when('I delete the todo')
def step_impl(context):
    todo_index = context.todo_page.get_todo_count() - 1
    context.todo_page.delete_todo(todo_index)

@given('I have the following todos:')
def step_impl(context):
    for row in context.table:
        context.todo_page.add_todo(row["text"])
        if row["completed"].lower() == "true":
            todo_index = context.todo_page.get_todo_count() - 1
            context.todo_page.toggle_todo(todo_index)

@when('I filter by "{filter_name}"')
def step_impl(context, filter_name):
    context.todo_page.filter_todos(filter_name)