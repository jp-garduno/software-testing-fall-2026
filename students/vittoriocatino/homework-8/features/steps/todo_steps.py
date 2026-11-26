"""Executable Gherkin bindings reusing the Playwright Page Object."""

import behave

# Behave replaces these public decorators dynamically when initializing its runner.
given = vars(behave)["given"]
when = vars(behave)["when"]
then = vars(behave)["then"]


@given("I am on the todo page")
def open_page(context):
    """Open a clean TodoMVC page."""
    context.todo_page.navigate()


@when('I add a todo "{text}"')
@given('I have a todo "{text}"')
def add_task(context, text):
    """Add a task through the UI."""
    context.todo_page.add_todo(text)


@given("I have the following todos:")
def add_table(context):
    """Translate each table row into real task creation and completion actions."""
    for index, row in enumerate(context.table):
        context.todo_page.add_todo(row["text"])
        if row["completed"] == "true":
            context.todo_page.toggle_todo(index)


@when("I mark the todo as complete")
def complete_task(context):
    """Complete the first task."""
    context.todo_page.toggle_todo(0)


@then("the todo should be marked as done")
def assert_done(context):
    """Verify the task checkbox is checked."""
    assert context.todo_page.completed_states() == [True]


@then("the active count should be {count:d}")
def assert_count(context, count):
    """Check the application's remaining-task counter."""
    assert context.todo_page.active_count() == count


@when("I delete the todo")
def delete_task(context):
    """Delete the first task via its hover control."""
    context.todo_page.delete_todo(0)


@when('I filter by "{name}"')
def filter_tasks(context, name):
    """Select All, Active or Completed."""
    context.todo_page.filter_by(name)


@then("I should see {count:d} todo")
def assert_visible_count(context, count):
    """Check the number of tasks rendered by the active filter."""
    assert context.todo_page.get_todo_count() == count


@then('the visible tasks should be "{texts}"')
def assert_tasks(context, texts):
    """Check complete ordered task labels, not only the count."""
    context.todo_page.assert_todos(texts.split(", ") if texts else [])


@when('I rename the todo to "{text}" and {action}')
def rename_task(context, text, action):
    """Save with Enter or cancel with Escape."""
    assert action in ("save", "cancel")
    context.todo_page.edit_todo(
        0, text, finish="escape" if action == "cancel" else "enter"
    )


@when("I clear completed tasks")
def clear_tasks(context):
    """Remove only tasks previously marked complete."""
    context.todo_page.clear_completed()
