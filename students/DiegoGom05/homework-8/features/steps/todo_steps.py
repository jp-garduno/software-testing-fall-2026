import os
import re
import sys

# Permite importar `pages.todo_page` desde selenium/
SELENIUM_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "selenium")
)
if SELENIUM_DIR not in sys.path:
    sys.path.insert(0, SELENIUM_DIR)

from behave import given, when, then
from selenium.webdriver.common.by import By

from pages.todo_page import TodoPage  # noqa: E402
# ----------------------------------------------------------------- helpers
def wait_for_count(context, expected):
    page = context.todo_page
    page.wait.until(lambda d: page.get_todo_count() == expected)


def active_count_text(context):
    return context.driver.find_element(By.CSS_SELECTOR, ".todo-count").text


# ------------------------------------------------------------------- Given
@given("I am on the todo page")
def step_on_todo_page(context):
    context.todo_page = TodoPage(context.driver)
    context.todo_page.navigate()


@given('I have a todo "{text}"')
def step_have_todo(context, text):
    context.todo_page.add_todo(text)
    wait_for_count(context, 1)

@given("I have the following todos:")
def step_have_following_todos(context):
    page = context.todo_page
    for i, row in enumerate(context.table):
        page.add_todo(row["text"])
        wait_for_count(context, i + 1)
        if row["completed"].strip().lower() == "true":
            page.toggle_todo(i)
            page.wait.until(lambda d, i=i: page.is_completed(i))


# -------------------------------------------------------------------- When
@when('I add a todo "{text}"')
def step_add_todo(context, text):
    context.todo_page.add_todo(text)


@when("I mark the todo as complete")
def step_mark_complete(context):
    context.todo_page.toggle_todo(0)


@when("I delete the todo")
def step_delete_todo(context):
    context.todo_page.delete_todo(0)


@when('I filter by "{name}"')
def step_filter_by(context, name):
    # "All" -> filter_all, "Active" -> filter_active, "Completed" -> filter_completed
    getattr(context.todo_page, f"filter_{name.lower()}")()


# -------------------------------------------------------------------- Then
# Behave distingue "todo", "todos" y "todo(s)", así que se apilan los patrones.
@then("I should see {count:d} todo")
@then("I should see {count:d} todos")
@then("I should see {count:d} todo(s)")
def step_see_count(context, count):
    wait_for_count(context, count)
    actual = context.todo_page.get_todo_count()
    assert actual == count, f"Expected {count}, got {actual}"


@then('the todo should be "{text}"')
def step_todo_text(context, text):
    actual = context.todo_page.get_visible_todos()
    assert actual == [text], f"Expected {[text]}, got {actual}"


@then("the todo should be marked as done")
def step_marked_done(context):
    page = context.todo_page
    page.wait.until(lambda d: page.is_completed(0))
    assert page.is_completed(0)


@then("the active count should be {n:d}")
def step_active_count(context, n):
    page = context.todo_page
    page.wait.until(
        lambda d: re.match(r"\d+", active_count_text(context)) is not None
    )
    text = active_count_text(context)
    actual = int(re.match(r"\d+", text).group())
    assert actual == n, f"Expected {n} active, counter says '{text}'"
