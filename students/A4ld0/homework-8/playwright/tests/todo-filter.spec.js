const { test, expect } = require('./fixtures');

test.beforeEach(async ({ todo }) => {
  for (const text of ['Active 1', 'Completed', 'Active 2']) {
    await todo.addTodo(text);
  }
  await todo.toggleTodo(1);
});

test('view all tasks', async ({ todo }) => {
  await todo.filterBy('Active');
  await todo.filterBy('All');
  await expect(todo.labels).toHaveText(['Active 1', 'Completed', 'Active 2']);
});

test('view active tasks', async ({ todo }) => {
  await todo.filterBy('Active');
  await expect(todo.labels).toHaveText(['Active 1', 'Active 2']);
  expect(await todo.activeCount()).toBe(2);
});

test('view completed tasks', async ({ todo }) => {
  await todo.filterBy('Completed');
  await expect(todo.labels).toHaveText(['Completed']);
  expect(await todo.isCompleted(0)).toBe(true);
});

