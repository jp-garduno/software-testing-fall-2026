"""Part 3: Behave-compatible BDD step definitions for features/todo.feature."""

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from bdd_runner import StepRegistry  # noqa: E402  # pylint: disable=wrong-import-position
from todo_page import TodoPage  # noqa: E402  # pylint: disable=wrong-import-position

REGISTRY = StepRegistry()

try:
    from behave import given as behave_given, when as behave_when, then as behave_then
except ImportError:  # pragma: no cover
    behave_given = behave_when = behave_then = None


def given(pattern: str):
    """Register a Given step definition with both Behave (if installed) and our StepRegistry."""
    def decorator(func):
        registered = REGISTRY.register("given", pattern)(func)
        if behave_given is not None:  # pragma: no cover
            behave_given(pattern)(func)
        return registered
    return decorator


def when(pattern: str):
    """Register a When step definition."""
    def decorator(func):
        registered = REGISTRY.register("when", pattern)(func)
        if behave_when is not None:  # pragma: no cover
            behave_when(pattern)(func)
        return registered
    return decorator


def then(pattern: str):
    """Register a Then step definition."""
    def decorator(func):
        registered = REGISTRY.register("then", pattern)(func)
        if behave_then is not None:  # pragma: no cover
            behave_then(pattern)(func)
        return registered
    return decorator


@given("I am on the todo page")
def step_on_todo_page(context):
    """Navigate to TodoMVC page."""
    context.todo_page = TodoPage(context.driver)
    context.todo_page.navigate()


@given('I have a todo "{text}"')
def step_have_single_todo(context, text):
    """Pre-populate a single todo item."""
    context.todo_page.add_todo(text)


@given("I have the following todos:")
def step_have_table_todos(context):
    """Pre-populate multiple todos from a Gherkin data table."""
    for idx, row in enumerate(context.table or []):
        context.todo_page.add_todo(row["text"])
        if row.get("completed", "").strip().lower() == "true":
            context.todo_page.toggle_todo(idx)


@when('I add a todo "{text}"')
def step_when_add_todo(context, text):
    """Add a new todo item."""
    context.todo_page.add_todo(text)


@when("I mark the todo as complete")
def step_when_mark_complete(context):
    """Mark the first todo item as complete."""
    context.todo_page.toggle_todo(0)


@when("I unmark the completed todo")
def step_when_unmark_complete(context):
    """Toggle the first completed todo item back to active."""
    context.todo_page.toggle_todo(0)


@when('I edit the todo to "{new_text}"')
def step_when_edit_todo(context, new_text):
    """Edit the first todo item's text."""
    context.todo_page.edit_todo(0, new_text)


@when("I delete the todo")
def step_when_delete_todo(context):
    """Delete the first todo item."""
    context.todo_page.delete_todo(0)


@when("I clear completed todos")
def step_when_clear_completed(context):
    """Clear all completed todo items."""
    context.todo_page.clear_completed()


@when('I filter by "{filter_name}"')
def step_when_filter_by(context, filter_name):
    """Filter todos by All, Active, or Completed."""
    context.todo_page.filter_by_name(filter_name)


@then("I should see {count:d} todo")
def step_then_see_singular(context, count):
    """Verify exact count of visible todos (singular grammar)."""
    actual = context.todo_page.get_todo_count()
    assert actual == count, f"Expected {count}, got {actual}"


@then("I should see {count:d} todos")
def step_then_see_plural(context, count):
    """Verify exact count of visible todos (plural grammar)."""
    actual = context.todo_page.get_todo_count()
    assert actual == count, f"Expected {count}, got {actual}"


@then("I should see {count:d} todo(s)")
def step_then_see_optional_plural(context, count):
    """Verify exact count of visible todos (Scenario Outline grammar)."""
    actual = context.todo_page.get_todo_count()
    assert actual == count, f"Expected {count}, got {actual}"


@then('the todo should be "{expected_text}"')
def step_then_todo_text(context, expected_text):
    """Verify the first visible todo has expected text."""
    visible = context.todo_page.get_visible_todos()
    assert visible and visible[0] == expected_text


@then("the todo should be marked as done")
def step_then_todo_done(context):
    """Verify the first todo item is marked completed."""
    assert context.todo_page.is_todo_completed(0) is True


@then("the todo should be active")
def step_then_todo_active(context):
    """Verify the first todo item is active (not completed)."""
    assert context.todo_page.is_todo_completed(0) is False


@then("the active count should be {count:d}")
def step_then_active_count(context, count):
    """Verify the footer active items counter matches expected count."""
    actual = context.todo_page.get_active_count()
    assert actual == count, f"Expected active count {count}, got {actual}"
