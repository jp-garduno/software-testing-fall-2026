# TodoPage Learning Plan

## Working rules

- I want to learn Selenium; I can't code everything at once.
- I want you to do the `add_todo` method, using [homework-8.md](../../../08-system-level-testing/homework/homework-8.md) as the reference for the first part.
- Work through the page object one method at a time. Explain the Selenium concepts used and leave the other methods for a later step.
- Use explicit waits and verify each step before moving on.
- Any implementation I request must also be recorded in this plan.
- Keep Selenium checks in test files rather than a separate runner for each method.

## Done

- Implemented `add_todo`: wait for the input to be visible, enter the task, submit with Enter, and wait for the input to clear.
- Added console prints to `add_todo` so each step is visible while the script runs.
- Implemented `get_todo_count`: use `find_elements` with the todo-item locator and return the number of matching items.
- Implemented `toggle_todo(index)`: click the completion checkbox for the zero-based todo index and wait for its selected state to change. Toggling a todo marks it complete; toggling it again marks it active.
- Added a toggle completion/uncompletion test to `selenium/tests/test_todo_crud.py`; the add test uses a unique title to avoid conflicts with saved todos.
- Implemented `delete_todo(index)`: hover over the zero-based todo row to reveal its X/destroy button, click the button, and wait for the row to be removed from the DOM.
- Added a delete test to `selenium/tests/test_todo_crud.py`; it creates a uniquely named todo, deletes it, and verifies the count returns to its starting value.
- Updated `navigate()` to use the current TodoMVC React example URL (`https://todomvc.com/examples/react/dist/`), since the homework URL returns 404.
- Removed the standalone `selenium/run_add_todo.py` script. Run the CRUD tests from the Selenium folder with `python -m pytest tests\test_todo_crud.py -q`.

## To do

- Implement and understand the active and completed filters.
- Implement and understand `get_visible_todos`.
- Add and run Selenium tests for filtering.
