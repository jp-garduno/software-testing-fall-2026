// Playwright E2E tests: create, complete, delete and edit todos (TodoMVC React).
const { test, expect } = require('../fixtures/todo-fixtures');

const ESCAPE_DEFECT =
  'DEFECT in TodoMVC React: Escape does not cancel editing. The edit box stays open and the typed ' +
  'text is saved on blur, although the TodoMVC spec says Escape must discard the change.';

test.describe('Task creation', () => {
  test('create single task', async ({ todoPage }) => {
    await todoPage.addTodo('Buy milk');

    await expect(todoPage.todoItems).toHaveCount(1);
    await expect(todoPage.todoLabels).toHaveText(['Buy milk']);
  });

  test('create multiple tasks', async ({ todoPage }) => {
    const tasks = ['Buy milk', 'Walk the dog', 'Write the report'];

    await todoPage.addTodos(...tasks);

    await expect(todoPage.todoItems).toHaveCount(3);
    await expect(todoPage.todoLabels).toHaveText(tasks); // same order as typed
  });

  test('task appears in list as active', async ({ todoPage }) => {
    await todoPage.addTodo('Read chapter 8');

    await expect(todoPage.todoLabels).toContainText(['Read chapter 8']);
    await expect(todoPage.item(0)).not.toHaveClass(/completed/);
    await expect(todoPage.footer).toBeVisible();
    await expect(todoPage.todoCount).toHaveText('1 item left!');
  });

  test('task text is trimmed', async ({ todoPage }) => {
    await todoPage.addTodo('   Pay rent   ');

    await expect(todoPage.todoLabels).toHaveText(['Pay rent']);
  });

  for (const [name, blankText] of [
    ['empty', ''],
    ['spaces', '   '],
  ]) {
    test(`blank task is not created (${name})`, async ({ todoPage }) => {
      await todoPage.addTodo(blankText);

      await expect(todoPage.todoItems).toHaveCount(0);
      await expect(todoPage.footer).toBeHidden();
    });
  }
});

test.describe('Task completion', () => {
  test('mark task as complete', async ({ todoPage }) => {
    await todoPage.addTodo('Finish homework 8');

    await todoPage.toggleTodo(0);

    await expect(todoPage.item(0)).toHaveClass(/completed/);
    await expect(todoPage.item(0).locator('.toggle')).toBeChecked();
    await expect(todoPage.todoCount).toHaveText('0 items left!');
    await expect(todoPage.clearCompletedButton).toBeVisible();
  });

  test('unmark completed task', async ({ todoPage }) => {
    await todoPage.addTodo('Finish homework 8');
    await todoPage.toggleTodo(0);

    await todoPage.toggleTodo(0);

    await expect(todoPage.item(0)).not.toHaveClass(/completed/);
    await expect(todoPage.todoCount).toHaveText('1 item left!');
    await expect(todoPage.clearCompletedButton).toBeHidden();
  });

  test('complete multiple tasks', async ({ todoPage }) => {
    await todoPage.addTodos('Task A', 'Task B', 'Task C');

    await todoPage.toggleTodo(0);
    await todoPage.toggleTodo(2);

    await expect(todoPage.todoItems).toHaveClass([/completed/, /^(?!.*completed)/, /completed/]);
    await expect(todoPage.todoCount).toHaveText('1 item left!');
  });

  test('toggle all completes and reopens every task', async ({ todoPage }) => {
    await todoPage.addTodos('Task A', 'Task B', 'Task C');

    await todoPage.toggleAll();
    await expect(todoPage.todoItems).toHaveClass([/completed/, /completed/, /completed/]);
    await expect(todoPage.todoCount).toHaveText('0 items left!');

    await todoPage.toggleAll();
    await expect(todoPage.page.locator('.todo-list li.completed')).toHaveCount(0);
    await expect(todoPage.todoCount).toHaveText('3 items left!');
  });
});

test.describe('Task deletion', () => {
  test('delete single task', async ({ todoPage }) => {
    await todoPage.addTodo('Task to delete');

    await todoPage.deleteTodo(0);

    await expect(todoPage.todoItems).toHaveCount(0);
    await expect(todoPage.footer).toBeHidden();
  });

  test('delete one task keeps the others', async ({ todoPage }) => {
    await todoPage.addTodos('Task A', 'Task B', 'Task C');

    await todoPage.deleteTodo(1);

    await expect(todoPage.todoLabels).toHaveText(['Task A', 'Task C']);
    await expect(todoPage.todoCount).toHaveText('2 items left!');
  });

  test('delete completed task', async ({ todoPage }) => {
    await todoPage.addTodos('Done task', 'Pending task');
    await todoPage.toggleTodo(0);

    await todoPage.deleteTodo(0);

    await expect(todoPage.todoLabels).toHaveText(['Pending task']);
    await expect(todoPage.todoCount).toHaveText('1 item left!');
    await expect(todoPage.clearCompletedButton).toBeHidden();
  });

  test('clear all completed', async ({ todoPage }) => {
    await todoPage.addTodos('Task A', 'Task B', 'Task C', 'Task D');
    await todoPage.toggleTodo(0);
    await todoPage.toggleTodo(2);

    await todoPage.clearCompleted();

    await expect(todoPage.todoLabels).toHaveText(['Task B', 'Task D']);
    await expect(todoPage.page.locator('.todo-list li.completed')).toHaveCount(0);
    await expect(todoPage.clearCompletedButton).toBeHidden();
  });
});

test.describe('Task editing', () => {
  test('edit task text', async ({ todoPage }) => {
    await todoPage.addTodo('Buy mlk');

    await todoPage.editTodo(0, 'Buy milk', { commit: 'enter' });

    await expect(todoPage.todoLabels).toHaveText(['Buy milk']);
    await expect(todoPage.editInput).toHaveCount(0);
  });

  test('save edited task on blur', async ({ todoPage }) => {
    await todoPage.addTodos('Call mom', 'Book flights');

    await todoPage.editTodo(1, '  Book flights to Guadalajara  ', { commit: 'blur' });

    await expect(todoPage.todoLabels).toHaveText(['Call mom', 'Book flights to Guadalajara']);
    await expect(todoPage.editInput).toHaveCount(0);
  });

  test('edit keeps completed state', async ({ todoPage }) => {
    await todoPage.addTodo('Old title');
    await todoPage.toggleTodo(0);

    await todoPage.editTodo(0, 'New title');

    await expect(todoPage.todoLabels).toHaveText(['New title']);
    await expect(todoPage.item(0)).toHaveClass(/completed/);
  });

  test('edit without changes keeps text', async ({ todoPage }) => {
    await todoPage.addTodo('Original text');

    await todoPage.editTodo(0, 'Original text');

    await expect(todoPage.todoLabels).toHaveText(['Original text']);
  });

  test('cancel edit with Escape discards changes @known-defect', async ({ todoPage }) => {
    test.fail(true, ESCAPE_DEFECT);
    await todoPage.addTodo('Original text');

    await todoPage.cancelEdit(0, 'Changed text');

    await expect(todoPage.editInput, 'Escape should close the edit box').toHaveCount(0, { timeout: 1000 });
    await expect(todoPage.todoLabels).toHaveText(['Original text']);
  });

  test('clearing text while editing deletes task', async ({ todoPage }) => {
    await todoPage.addTodos('Keep me', 'Delete me');

    await todoPage.editTodo(1, '');

    await expect(todoPage.todoLabels).toHaveText(['Keep me']);
  });
});
