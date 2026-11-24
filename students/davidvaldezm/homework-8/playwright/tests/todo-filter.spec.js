const { test, expect } = require('./fixtures');

for (const [name, texts] of [
  ['All', ['Task 1', 'Task 2', 'Task 3']],
  ['Active', ['Task 1', 'Task 3']],
  ['Completed', ['Task 2']],
]) {
  test(`filter ${name}`, async ({ mixed }) => {
    await mixed.filterBy(name);
    await expect(mixed.labels).toHaveText(texts);
    await mixed.filterBy('All');
    await expect(mixed.labels).toHaveText(['Task 1', 'Task 2', 'Task 3']);
    await expect(mixed.counter).toHaveText(/^2 items? left!$/);
  });
}

test('empty filter', async ({ todo }) => {
  await todo.addTodo('Active task');
  await todo.filterBy('Completed');
  await expect(todo.todoItems).toHaveCount(0);
  await todo.filterBy('All');
  await expect(todo.labels).toHaveText(['Active task']);
});
