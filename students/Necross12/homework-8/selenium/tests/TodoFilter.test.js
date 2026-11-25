const { Builder } = require('selenium-webdriver');
const { TodoPage } = require('../pages/TodoPage');

jest.setTimeout(30000);

describe('Task Filtering', () => {
  let driver;
  let todoPage;

  beforeAll(async () => {
    driver = await new Builder().forBrowser('chrome').build();
  });

  afterAll(async () => {
    await driver.quit();
  });

  beforeEach(async () => {
    todoPage = new TodoPage(driver);
    await todoPage.navigate();
    await todoPage.addTodos(['Tarea 1', 'Tarea 2', 'Tarea 3']);
    await todoPage.toggleTodo(1); // "Tarea 2" queda completada
  });

  afterEach(async () => {
    await todoPage.takeScreenshot(expect.getState().currentTestName);
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
