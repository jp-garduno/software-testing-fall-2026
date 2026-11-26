const { test, expect } = require('./fixtures');

test('create single task', async ({ todo }) => {
  await todo.addTodo('Buy milk');
  expect(await todo.getTodoCount()).toBe(1);
  await expect(todo.labels).toHaveText(['Buy milk']);
});

test('create multiple tasks', async ({ todo }) => {
  for (const text of ['Buy milk', 'Read book', 'Study testing']) {
    await todo.addTodo(text);
  }
  await expect(todo.labels).toHaveText(['Buy milk', 'Read book', 'Study testing']);
});

test('created task appears in list', async ({ todo }) => {
  await todo.addTodo('First task');
  await todo.addTodo('New task');
  expect(await todo.getVisibleTodos()).toContain('New task');
});

test('mark task complete', async ({ todo }) => {
  await todo.addTodo('Read book');
  await todo.toggleTodo(0);
  expect(await todo.isCompleted(0)).toBe(true);
  expect(await todo.activeCount()).toBe(0);
});

test('unmark completed task', async ({ todo }) => {
  await todo.addTodo('Read book');
  await todo.toggleTodo(0);
  await todo.toggleTodo(0);
  expect(await todo.isCompleted(0)).toBe(false);
  expect(await todo.activeCount()).toBe(1);
});

test('complete multiple tasks', async ({ todo }) => {
  await todo.addTodo('First');
  await todo.addTodo('Second');
  await todo.toggleTodo(0);
  await todo.toggleTodo(1);
  expect(await todo.isCompleted(0)).toBe(true);
  expect(await todo.isCompleted(1)).toBe(true);
  expect(await todo.activeCount()).toBe(0);
});

test('delete single task', async ({ todo }) => {
  await todo.addTodo('Keep');
  await todo.addTodo('Delete');
  await todo.deleteTodo(1);
  await expect(todo.labels).toHaveText(['Keep']);
});

test('delete completed task', async ({ todo }) => {
  await todo.addTodo('Completed');
  await todo.addTodo('Active');
  await todo.toggleTodo(0);
  await todo.deleteTodo(0);
  await expect(todo.labels).toHaveText(['Active']);
  expect(await todo.activeCount()).toBe(1);
});

test('clear all completed', async ({ todo }) => {
  for (const text of ['Done 1', 'Keep', 'Done 2']) {
    await todo.addTodo(text);
  }
  await todo.toggleTodo(0);
  await todo.toggleTodo(2);
  await todo.clearCompleted();
  await expect(todo.labels).toHaveText(['Keep']);
  expect(await todo.isCompleted(0)).toBe(false);
});

test('edit task text', async ({ todo }) => {
  await todo.addTodo('Original');
  await todo.editTodo(0, 'Updated');
  await expect(todo.labels).toHaveText(['Updated']);
  expect(await todo.getTodoCount()).toBe(1);
});

test('cancel edit', async ({ todo }) => {
  await todo.addTodo('Original');
  await todo.editTodo(0, 'Discarded', false);
  await expect(todo.labels).toHaveText(['Original']);
});

test('save edited task', async ({ todo }) => {
  await todo.addTodo('Original');
  await todo.addTodo('Other');
  await todo.toggleTodo(0);
  await todo.editTodo(0, 'Saved');
  await expect(todo.labels).toHaveText(['Saved', 'Other']);
  expect(await todo.isCompleted(0)).toBe(true);
});

