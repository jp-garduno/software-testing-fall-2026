// Creation, completion, deletion and editing scenarios.
const { test, expect } = require('@playwright/test');
const { TodoPage } = require('../pages/TodoPage');

let todoPage;

test.beforeEach(async ({ page }) => {
  todoPage = new TodoPage(page);
  await todoPage.navigate();
});

test.describe('Task Creation', () => {
  test('create single task', async () => {
    await todoPage.addTodo('Buy milk');

    await expect(todoPage.todoLabels).toHaveText(['Buy milk']);
    await expect(todoPage.todoCount).toHaveText('1 item left!');
  });

  test('create multiple tasks', async () => {
    await todoPage.addTodos('Buy milk', 'Walk the dog', 'Read a book');

    await expect(todoPage.todoItems).toHaveCount(3);
    await expect(todoPage.todoCount).toHaveText('3 items left!');
  });

  test('new tasks appear at end of list', async () => {
    await todoPage.addTodos('First', 'Second');
    await todoPage.addTodo('Third');

    await expect(todoPage.todoLabels).toHaveText(['First', 'Second', 'Third']);
  });

  test('task text is trimmed', async () => {
    await todoPage.addTodo('   Water plants   ');

    // toHaveText() normalises whitespace, so compare the raw text instead.
    await expect.poll(() => todoPage.getVisibleTodos()).toEqual(['Water plants']);
  });

  test('blank task is not created', async () => {
    await todoPage.addTodo('     ');

    await expect(todoPage.todoItems).toHaveCount(0);
    await expect(todoPage.todoCount).toBeHidden();
  });
});

test.describe('Task Completion', () => {
  test('mark task as complete', async () => {
    await todoPage.addTodo('Write report');

    await todoPage.toggleTodo(0);

    await expect(todoPage.toggle(0)).toBeChecked();
    await expect(todoPage.item(0)).toHaveClass(/completed/);
    await expect(todoPage.todoCount).toHaveText('0 items left!');
  });

  test('unmark completed task', async () => {
    await todoPage.addTodo('Write report');
    await todoPage.toggleTodo(0);

    await todoPage.toggleTodo(0);

    await expect(todoPage.toggle(0)).not.toBeChecked();
    await expect(todoPage.item(0)).not.toHaveClass(/completed/);
    await expect(todoPage.todoCount).toHaveText('1 item left!');
  });

  test('complete multiple tasks', async () => {
    await todoPage.addTodos('One', 'Two', 'Three');

    await todoPage.toggleTodo(0);
    await todoPage.toggleTodo(2);

    await expect(todoPage.toggle(0)).toBeChecked();
    await expect(todoPage.toggle(1)).not.toBeChecked();
    await expect(todoPage.toggle(2)).toBeChecked();
    await expect(todoPage.todoCount).toHaveText('1 item left!');
  });

  test('toggle all completes every task', async () => {
    await todoPage.addTodos('One', 'Two', 'Three');

    await todoPage.toggleAll();

    for (const index of [0, 1, 2]) {
      await expect(todoPage.toggle(index)).toBeChecked();
    }
    await expect(todoPage.todoCount).toHaveText('0 items left!');
  });
});

test.describe('Task Deletion', () => {
  test('delete single task', async () => {
    await todoPage.addTodos('Keep me', 'Delete me');

    await todoPage.deleteTodo(1);

    await expect(todoPage.todoLabels).toHaveText(['Keep me']);
  });

  test('delete completed task', async () => {
    await todoPage.addTodos('Done task', 'Pending task');
    await todoPage.toggleTodo(0);

    await todoPage.deleteTodo(0);

    await expect(todoPage.todoLabels).toHaveText(['Pending task']);
    await expect(todoPage.clearCompletedButton).toBeHidden();
  });

  test('clear all completed', async () => {
    await todoPage.addTodos('Done 1', 'Pending', 'Done 2');
    await todoPage.toggleTodo(0);
    await todoPage.toggleTodo(2);

    await todoPage.clearCompleted();

    await expect(todoPage.todoLabels).toHaveText(['Pending']);
    await expect(todoPage.todoCount).toHaveText('1 item left!');
  });

  test('deleting last task hides footer', async () => {
    await todoPage.addTodo('Only task');

    await todoPage.deleteTodo(0);

    await expect(todoPage.todoItems).toHaveCount(0);
    await expect(todoPage.todoCount).toBeHidden();
  });
});

test.describe('Task Editing', () => {
  test('edit task text', async () => {
    await todoPage.addTodos('Old text', 'Untouched');

    await todoPage.editTodo(0, 'New text');

    await expect(todoPage.todoLabels).toHaveText(['New text', 'Untouched']);
  });

  test('cancel edit with escape', { tag: '@known-defect' }, async () => {
    test.fail(true, 'TodoMVC React has no Escape key handler');
    await todoPage.addTodo('Original');
    await todoPage.startEdit(0);
    await todoPage.typeEdit('Discard me');

    await todoPage.cancelEdit();

    // Immediate check: React updates synchronously on key events.
    expect(await todoPage.editInput.isVisible(), 'Escape should close the editor').toBe(false);
    await expect(todoPage.todoLabels).toHaveText(['Original']);
  });

  test('save edited task with enter', async () => {
    await todoPage.addTodo('Draft');
    await todoPage.startEdit(0);
    await todoPage.typeEdit('Final version');

    await todoPage.saveEdit();

    await expect(todoPage.editInput).toBeHidden();
    await expect(todoPage.todoLabels).toHaveText(['Final version']);
  });

  test('save edited task on blur', async () => {
    await todoPage.addTodo('Draft');
    await todoPage.startEdit(0);
    await todoPage.typeEdit('Saved on blur');

    await todoPage.saveEditByBlur();

    await expect(todoPage.todoLabels).toHaveText(['Saved on blur']);
  });

  test('edit to empty text deletes task', async () => {
    await todoPage.addTodo('Temporary');

    await todoPage.editTodo(0, '');

    await expect(todoPage.todoItems).toHaveCount(0);
  });
});
