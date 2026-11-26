const path = require('node:path');
const { test, expect } = require('./fixtures');

test('create single', async ({ todo }) => {
  await todo.addTodo('Buy milk');
  await expect(todo.labels).toHaveText(['Buy milk']);
  await expect(todo.todoItems).toHaveCount(1);
});

test('create multiple', async ({ todo }) => {
  for (const text of ['Read', 'Write', 'Review']) await todo.addTodo(text);
  await expect(todo.labels).toHaveText(['Read', 'Write', 'Review']);
  await expect(todo.counter).toHaveText(/^3 items? left!$/);
});

test('complete task', async ({ todo }) => {
  await todo.addTodo('Read');
  await todo.toggleTodo(0);
  await expect(todo.checkbox(0)).toBeChecked();
  await expect(todo.counter).toHaveText(/^0 items? left!$/);
});

test('uncomplete task', async ({ todo }) => {
  await todo.addTodo('Read');
  await todo.toggleTodo(0);
  await todo.toggleTodo(0);
  await expect(todo.checkbox(0)).not.toBeChecked();
  await expect(todo.counter).toHaveText(/^1 items? left!$/);
});

test('complete all', async ({ todo }) => {
  for (const text of ['Read', 'Write', 'Review']) await todo.addTodo(text);
  await todo.completeAll();
  for (let i = 0; i < 3; i += 1) await expect(todo.checkbox(i)).toBeChecked();
  await expect(todo.counter).toHaveText(/^0 items? left!$/);
  await todo.page.screenshot({ path: path.join(__dirname, '../../screenshots/playwright-completed.png') });
});

test('delete single', async ({ todo }) => {
  await todo.addTodo('Delete me');
  await todo.deleteTodo(0);
  await expect(todo.todoItems).toHaveCount(0);
});

test('delete completed', async ({ todo }) => {
  await todo.addTodo('Delete me');
  await todo.toggleTodo(0);
  await todo.deleteTodo(0);
  await expect(todo.todoItems).toHaveCount(0);
});

test('clear completed', async ({ mixed }) => {
  await mixed.clearCompleted();
  await expect(mixed.labels).toHaveText(['Task 1', 'Task 3']);
  await expect(mixed.counter).toHaveText(/^2 items? left!$/);
});

for (const [name, text, save, expected] of [
  ['edit enter', 'Final', 'enter', ['Final']],
  ['edit cancel', 'Discard', 'cancel', ['Draft']],
  ['edit blur', 'Saved on blur', 'blur', ['Saved on blur']],
  ['blank edit deletes', '   ', 'enter', []],
]) {
  test(name, async ({ todo }) => {
    test.fail(save === 'cancel', 'React demo defect: Escape leaves the editor open and does not cancel');
    await todo.addTodo('Draft');
    await todo.editTodo(0, text, save);
    await expect(todo.labels).toHaveText(expected);
  });
}

test('blank creation', async ({ todo }) => {
  await todo.addTodo('   ');
  await expect(todo.todoItems).toHaveCount(0);
});

test('trim creation', async ({ todo }) => {
  await todo.addTodo('  Trim me  ');
  await expect(todo.labels).toHaveText(['Trim me']);
});

test('duplicate tasks', async ({ todo }) => {
  await todo.addTodo('Repeated');
  await todo.addTodo('Repeated');
  await todo.deleteTodo(0);
  await expect(todo.labels).toHaveText(['Repeated']);
});
