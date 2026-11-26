// Filtering scenarios: All / Active / Completed.
const { test, expect } = require('@playwright/test');
const { TodoPage } = require('../pages/TodoPage');

let todoPage;

test.beforeEach(async ({ page }) => {
  todoPage = new TodoPage(page);
  await todoPage.navigate();
});

test.describe('Task Filtering', () => {
  // Three todos where only the middle one is completed.
  test.beforeEach(async () => {
    await todoPage.addTodos('Task 1', 'Task 2', 'Task 3');
    await todoPage.toggleTodo(1);
  });

  test('view all tasks', async () => {
    await todoPage.filterActive();

    await todoPage.filterAll();

    await expect(todoPage.todoLabels).toHaveText(['Task 1', 'Task 2', 'Task 3']);
  });

  test('view active tasks only', async () => {
    await todoPage.filterActive();

    await expect(todoPage.todoLabels).toHaveText(['Task 1', 'Task 3']);
  });

  test('view completed tasks only', async () => {
    await todoPage.filterCompleted();

    await expect(todoPage.todoLabels).toHaveText(['Task 2']);
  });

  for (const name of ['All', 'Active', 'Completed']) {
    test(`selected filter is highlighted: ${name}`, async () => {
      await todoPage[`filter${name}`]();

      await expect(todoPage.selectedFilter).toHaveText(name);
    });
  }

  test('completing task removes it from active view', async () => {
    await todoPage.filterActive();

    await todoPage.toggleTodo(0);

    await expect(todoPage.todoLabels).toHaveText(['Task 3']);
  });
});

test.describe('Task Filtering with no completed tasks', () => {
  test('empty completed view keeps footer', async () => {
    await todoPage.addTodo('Not done yet');

    await todoPage.filterCompleted();

    await expect(todoPage.todoItems).toHaveCount(0);
    await expect(todoPage.todoCount).toBeVisible();
  });
});
