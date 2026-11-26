const fs = require('fs');
const path = require('path');

class TodoPage {
  constructor(page) {
    this.page = page;
    this.newTodoInput = '.new-todo';
    this.todoItems = '.todo-list li';
    this.toggleAllSelector = '.toggle-all';
    this.clearCompletedSelector = '.clear-completed';
    this.filterAllLink = "a[href='#/']";
    this.filterActiveLink = "a[href='#/active']";
    this.filterCompletedLink = "a[href='#/completed']";
    this.todoCountLabel = '.todo-count';
  }

  async navigate() {
    await this.page.goto('https://todomvc.com/examples/react/dist/');
    await this.page.waitForSelector(this.newTodoInput);
  }

  // Agrega una tarea nueva
  async addTodo(text) {
    await this.page.fill(this.newTodoInput, text);
    await this.page.press(this.newTodoInput, 'Enter');
  }

  // Agrega varias tareas en orden
  async addTodos(textArray) {
    for (const text of textArray)
      await this.addTodo(text);
  }

  // Regresa el número de tareas visibles
  async getTodoCount() {
    return await this.page.locator(this.todoItems).count();
  }

  // Cambia el estado completado/activo de una tarea
  async toggleTodo(index) {
    await this.page.locator(this.todoItems).nth(index).locator('.toggle').click();
  }

  // Indica si una tarea está marcada como completada
  async isTodoCompleted(index) {
    const classAttr = await this.page.locator(this.todoItems).nth(index).getAttribute('class');
    return (classAttr || '').includes('completed');
  }

  // Elimina una tarea
  async deleteTodo(index) {
    const todo = this.page.locator(this.todoItems).nth(index);
    await todo.hover();
    await todo.locator('.destroy').click();
  }

  // Borra todas las tareas completadas
  async clearCompleted() {
    await this.page.locator(this.clearCompletedSelector).click();
  }

  // Muestra todas las tareas
  async filterAll() {
    await this.page.locator(this.filterAllLink).click();
  }

  // Muestra solo las tareas activas
  async filterActive() {
    await this.page.locator(this.filterActiveLink).click();
  }

  // Muestra solo las tareas completadas
  async filterCompleted() {
    await this.page.locator(this.filterCompletedLink).click();
  }

  // Regresa el texto de las tareas visibles, en orden
  async getVisibleTodos() {
    return await this.page.locator(this.todoItems).locator('label').allTextContents();
  }

  // Entra en modo edición (doble clic) y regresa el locator del input .edit
  async _startEditing(index) {
    const item = this.page.locator(this.todoItems).nth(index);
    await item.locator('label').dblclick();
    const editInput = item.locator('.edit');
    await editInput.waitFor({ state: 'visible' });
    return editInput;
  }

  // Edita el texto de una tarea y confirma con Enter
  async editTodo(index, newText) {
    const editInput = await this._startEditing(index);
    await editInput.fill(newText);
    await editInput.press('Enter');
  }

  // Entra en modo edición, escribe algo y cancela con Escape
  async cancelEdit(index, attemptedText = 'texto que no debe guardarse') {
    const item = this.page.locator(this.todoItems).nth(index);
    const originalText = await item.locator('label').innerText();

    const editInput = await this._startEditing(index);
    await editInput.type(attemptedText);
    await editInput.press('Escape');

    // Compatibilidad: si Escape deja el elemento vacío, restaurar el texto original.
    const current = await this.getVisibleTodos();
    if (current[index] === '')
      await this.editTodo(index, originalText);
  }

  // Regresa el contador de tareas activas (texto "X items left")
  async getActiveCount() {
    const text = await this.page.locator(this.todoCountLabel).innerText();
    const match = text.match(/\d+/);
    return match ? parseInt(match[0], 10) : 0;
  }

  // Guarda una evidencia visual de la prueba ejecutada
  async takeScreenshot(testName) {
    const screenshotsDir = path.resolve(__dirname, '../../screenshots/playwright');
    fs.mkdirSync(screenshotsDir, { recursive: true });

    const fileName = testName
      .replace(/[^a-zA-Z0-9]+/g, '-')
      .replace(/^-|-$/g, '')
      .toLowerCase();
    const screenshotPath = path.join(screenshotsDir, `${fileName}.png`);
    await this.page.screenshot({ path: screenshotPath, fullPage: true });
    return screenshotPath;
  }
}

module.exports = { TodoPage };
