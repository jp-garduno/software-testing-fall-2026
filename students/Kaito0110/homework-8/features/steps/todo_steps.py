from behave import given, then, when


@given("I am on the todo page")
def step_on_todo_page(context):
    assert context.todo_page.get_todo_count() == 0


@when('I add a todo "{text}"')
@given('I have a todo "{text}"')
def step_add_todo(context, text):
    context.todo_page.add_todo(text)


@then("I should see {count:d} todo")
@then("I should see {count:d} todos")
def step_check_todo_count(context, count):
    actual = context.todo_page.get_todo_count()
    assert actual == count, f"Expected {count} visible todos, got {actual}"


@then('the todo should be "{text}"')
def step_check_todo_text(context, text):
    assert context.todo_page.get_visible_todos() == [text]


@when("I mark the todo as complete")
def step_complete_todo(context):
    context.todo_page.toggle_todo(0)


@then("the todo should be marked as done")
def step_check_completed(context):
    assert context.todo_page.is_completed(0)


@then("the active count should be {count:d}")
def step_check_active_count(context, count):
    assert context.todo_page.get_active_count() == count


@when("I delete the todo")
def step_delete_todo(context):
    context.todo_page.delete_todo(0)


@given("I have these todos:")
def step_add_table_todos(context):
    for row in context.table:
        context.todo_page.add_todo(row["text"])
        if row["completed"].lower() == "true":
            context.todo_page.toggle_todo(context.todo_page.get_todo_count() - 1)


@when('I filter by "{filter_name}"')
def step_filter_todos(context, filter_name):
    filters = {
        "all": context.todo_page.filter_all,
        "active": context.todo_page.filter_active,
        "completed": context.todo_page.filter_completed,
    }
    try:
        filters[filter_name.lower()]()
    except KeyError as error:
        raise AssertionError(f"Unsupported todo filter: {filter_name}") from error
