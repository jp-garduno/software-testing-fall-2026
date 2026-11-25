const { test, expect } = require('@playwright/test');
const { TodoPage } = require('../pages/TodoPage');

test.describe('Todo CRUD', () => {
  let todoPage;

  test.beforeEach(async ({ page }) => {
    todoPage = new TodoPage(page);
    await todoPage.navigate();
  });

  test.afterEach(async ({}, testInfo) => {
    await todoPage.takeScreenshot(testInfo.title);
  });

  test.describe('Task Creation', () => {
    test('crea una sola tarea', async () => {
      await todoPage.addTodo('Comprar leche');
      expect(await todoPage.getTodoCount()).toBe(1);
    });

    test('crea múltiples tareas', async () => {
      await todoPage.addTodos(['Tarea 1', 'Tarea 2', 'Tarea 3']);
      expect(await todoPage.getTodoCount()).toBe(3);
    });

    test('la tarea aparece en la lista con el texto correcto', async () => {
      await todoPage.addTodo('Lavar el coche');
      const todos = await todoPage.getVisibleTodos();
      expect(todos).toContain('Lavar el coche');
    });
  });

  test.describe('Task Completion', () => {
    test('marca una tarea como completada', async () => {
      await todoPage.addTodo('Tarea a completar');
      await todoPage.toggleTodo(0);
      expect(await todoPage.isTodoCompleted(0)).toBe(true);
    });

    test('desmarca una tarea completada', async () => {
      await todoPage.addTodo('Tarea a alternar');
      await todoPage.toggleTodo(0);
      await todoPage.toggleTodo(0);
      expect(await todoPage.isTodoCompleted(0)).toBe(false);
    });

    test('completa múltiples tareas', async () => {
      await todoPage.addTodos(['A', 'B', 'C']);
      await todoPage.toggleTodo(0);
      await todoPage.toggleTodo(2);
      expect(await todoPage.isTodoCompleted(0)).toBe(true);
      expect(await todoPage.isTodoCompleted(1)).toBe(false);
      expect(await todoPage.isTodoCompleted(2)).toBe(true);
    });
  });

  test.describe('Task Deletion', () => {
    test('elimina una sola tarea', async () => {
      await todoPage.addTodo('Tarea a borrar');
      await todoPage.deleteTodo(0);
      expect(await todoPage.getTodoCount()).toBe(0);
    });

    test('elimina una tarea completada', async () => {
      await todoPage.addTodo('Tarea completada a borrar');
      await todoPage.toggleTodo(0);
      await todoPage.deleteTodo(0);
      expect(await todoPage.getTodoCount()).toBe(0);
    });

    test('limpia todas las tareas completadas', async () => {
      await todoPage.addTodos(['Pendiente', 'Completada 1', 'Completada 2']);
      await todoPage.toggleTodo(1);
      await todoPage.toggleTodo(2);
      await todoPage.clearCompleted();
      const todos = await todoPage.getVisibleTodos();
      expect(todos).toEqual(['Pendiente']);
    });
  });

  test.describe('Task Editing', () => {
    test('edita el texto de una tarea', async () => {
      await todoPage.addTodo('Texto original');
      await todoPage.editTodo(0, 'Texto editado');
      const todos = await todoPage.getVisibleTodos();
      expect(todos).toContain('Texto editado');
    });

    test('cancela la edición de una tarea', async () => {
      await todoPage.addTodo('No debe cambiar');
      await todoPage.cancelEdit(0);
      const todos = await todoPage.getVisibleTodos();
      expect(todos).toContain('No debe cambiar');
    });

    test('guarda la tarea editada tras presionar Enter', async () => {
      await todoPage.addTodo('Antes');
      await todoPage.editTodo(0, 'Después');
      const todos = await todoPage.getVisibleTodos();
      expect(todos).toEqual(['Después']);
    });
  });
});
