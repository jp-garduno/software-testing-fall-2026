// Playwright E2E tests: All / Active / Completed filters (TodoMVC React).
const { test, expect } = require('../fixtures/todo-fixtures');

const ALL_TASKS = ['Task 1', 'Task 2', 'Task 3'];

test.describe('Task filtering', () => {
  // Three todos where only "Task 2" is completed.
  test.beforeEach(async ({ todoPage }) => {
    await todoPage.addTodos(...ALL_TASKS);
    await todoPage.toggleTodo(1);
  });

  test('view all tasks', async ({ todoPage, page }) => {
    await todoPage.filterActive();

    await todoPage.filterAll();

    await expect(todoPage.todoLabels).toHaveText(ALL_TASKS);
    await expect(todoPage.selectedFilter).toHaveText('All');
    await expect(page).toHaveURL(/#\/$/);
  });

  test('view active tasks only', async ({ todoPage, page }) => {
    await todoPage.filterActive();

    await expect(todoPage.todoLabels).toHaveText(['Task 1', 'Task 3']);
    await expect(todoPage.selectedFilter).toHaveText('Active');
    await expect(page).toHaveURL(/#\/active$/);
  });

  test('view completed tasks only', async ({ todoPage, page }) => {
    await todoPage.filterCompleted();

    await expect(todoPage.todoLabels).toHaveText(['Task 2']);
    await expect(todoPage.selectedFilter).toHaveText('Completed');
    await expect(page).toHaveURL(/#\/completed$/);
  });

  // Data-driven: one test per filter.
  const FILTER_CASES = [
    { filter: 'All', expected: ALL_TASKS },
    { filter: 'Active', expected: ['Task 1', 'Task 3'] },
    { filter: 'Completed', expected: ['Task 2'] },
  ];
  for (const { filter, expected } of FILTER_CASES) {
    test(`filter "${filter}" shows ${expected.length} todo(s)`, async ({ todoPage }) => {
      await todoPage.applyFilter(filter);

      await expect(todoPage.todoLabels).toHaveText(expected);
      // The counter always reports the active todos, whatever the filter.
      await expect(todoPage.todoCount).toHaveText('2 items left!');
    });
  }

  test('completing task in active view hides it', async ({ todoPage }) => {
    await todoPage.filterActive();

    await todoPage.toggleTodo(0);

    await expect(todoPage.todoLabels).toHaveText(['Task 3']);
    await expect(todoPage.todoCount).toHaveText('1 item left!');
  });

  test('clear completed from completed view', async ({ todoPage }) => {
    await todoPage.filterCompleted();

    await todoPage.clearCompleted();

    await expect(todoPage.todoItems).toHaveCount(0);
    await todoPage.filterAll();
    await expect(todoPage.todoLabels).toHaveText(['Task 1', 'Task 3']);
  });
});
