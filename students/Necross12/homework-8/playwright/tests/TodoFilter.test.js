const { test, expect } = require('@playwright/test');
const { TodoPage } = require('../pages/TodoPage');

test.describe('Task Filtering', () => {
  let todoPage;

  test.beforeEach(async ({ page }) => {
    todoPage = new TodoPage(page);
    await todoPage.navigate();
    await todoPage.addTodos(['Tarea 1', 'Tarea 2', 'Tarea 3']);
    await todoPage.toggleTodo(1); // "Tarea 2" queda completada
  });

  test.afterEach(async ({}, testInfo) => {
    await todoPage.takeScreenshot(testInfo.title);
  });

  test('muestra todas las tareas', async () => {
    await todoPage.filterAll();
    const todos = await todoPage.getVisibleTodos();
    expect(todos).toHaveLength(3);
  });

  test('muestra solo las tareas activas', async () => {
    await todoPage.filterActive();
    const todos = await todoPage.getVisibleTodos();
    expect(todos).toHaveLength(2);
    expect(todos).not.toContain('Tarea 2');
  });

  test('muestra solo las tareas completadas', async () => {
    await todoPage.filterCompleted();
    const todos = await todoPage.getVisibleTodos();
    expect(todos).toEqual(['Tarea 2']);
  });
});
