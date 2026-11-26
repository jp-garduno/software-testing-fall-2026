const { By, Key, until } = require('selenium-webdriver');
const fs = require('fs');
const path = require('path');

const TIMEOUT = 10000;

class TodoPage {
  // localizaciones 
  static NEW_TODO_INPUT = By.className('new-todo');
  static TODO_ITEMS = By.css('.todo-list li');
  static TOGGLE_ALL = By.className('toggle-all');
  static CLEAR_COMPLETED = By.className('clear-completed');
  static FILTER_ALL = By.css("a[href='#/']");
  static FILTER_ACTIVE = By.css("a[href='#/active']");
  static FILTER_COMPLETED = By.css("a[href='#/completed']");
  static TODO_COUNT_LABEL = By.className('todo-count');

  constructor(driver) {
    this.driver = driver;
  }

  async navigate() {
    await this.driver.get('https://todomvc.com/examples/react/dist/');
    await this.driver.wait(until.elementLocated(TodoPage.NEW_TODO_INPUT), TIMEOUT);
  }

  // Agrega una tarea nueva
  async addTodo(text) {
    const input = await this.driver.findElement(TodoPage.NEW_TODO_INPUT);
    await input.sendKeys(text, Key.ENTER);
  }

  // Agrega varias tareas en orden
  async addTodos(textArray) {
    for (const text of textArray)
      await this.addTodo(text);
  }

  // Regresa el número de tareas visibles
  async getTodoCount() {
    const items = await this.driver.findElements(TodoPage.TODO_ITEMS);
    return items.length;
  }

  async _getTodoItem(index) {
    const items = await this.driver.findElements(TodoPage.TODO_ITEMS);
    if (index >= items.length)
      throw new Error(`No existe una tarea en el índice ${index}`);
    return items[index];
  }

  // Cambia el estado completado/activo de una tarea
  async toggleTodo(index) {
    const item = await this._getTodoItem(index);
    const checkbox = await item.findElement(By.css('.toggle'));
    await checkbox.click();
  }

  // Indica si una tarea está marcada como completada
  async isTodoCompleted(index) {
    const item = await this._getTodoItem(index);
    const classAttr = await item.getAttribute('class');
    return classAttr.includes('completed');
  }

  // Elimina una tarea
  async deleteTodo(index) {
    const item = await this._getTodoItem(index);
    await this.driver.actions().move({ origin: item }).perform();
    const destroyBtn = await item.findElement(By.css('.destroy'));
    await destroyBtn.click();
  }

  // Borra todas las tareas completadas
  async clearCompleted() {
    const btn = await this.driver.findElement(TodoPage.CLEAR_COMPLETED);
    await btn.click();
  }

  // Muestra todas las tareas
  async filterAll() {
    const link = await this.driver.findElement(TodoPage.FILTER_ALL);
    await link.click();
  }

  // Muestra solo las tareas activas
  async filterActive() {
    const link = await this.driver.findElement(TodoPage.FILTER_ACTIVE);
    await link.click();
  }

  // Muestra solo las tareas completadas
  async filterCompleted() {
    const link = await this.driver.findElement(TodoPage.FILTER_COMPLETED);
    await link.click();
  }

  // Regresa el texto de las tareas visibles, en orden
  async getVisibleTodos() {
    const items = await this.driver.findElements(TodoPage.TODO_ITEMS);
    const texts = [];
    for (const item of items) {
      const label = await item.findElement(By.css('label'));
      texts.push(await label.getText());
    }
    return texts;
  }

  // Entra en modo edición (doble clic) y regresa el input .edit
  async _startEditing(index) {
    const item = await this._getTodoItem(index);
    const label = await item.findElement(By.css('label'));
    await this.driver.actions().doubleClick(label).perform();
    const editInput = await item.findElement(By.css('.edit'));
    await this.driver.wait(until.elementIsVisible(editInput), TIMEOUT);
    return editInput;
  }

  // Edita el texto de una tarea y confirma con Enter
  async editTodo(index, newText) {
    const editInput = await this._startEditing(index);
    await editInput.sendKeys(Key.CONTROL, 'a');
    await editInput.sendKeys(Key.BACK_SPACE);
    await editInput.sendKeys(newText, Key.ENTER);
  }

  // Entra en modo edición, escribe algo y cancela con Escape
  async cancelEdit(index, attemptedText = 'texto que no debe guardarse') {
    const item = await this._getTodoItem(index);
    const label = await item.findElement(By.css('label'));
    const originalText = await label.getText();

    const editInput = await this._startEditing(index);
    await editInput.sendKeys(attemptedText);
    await editInput.sendKeys(Key.ESCAPE);

    // Compatibilidad con React: si Escape deja un elemento vacío, restaurar el texto original.
    const todos = await this.getVisibleTodos();
    if (todos[index] === '') {
      const currentItem = await this._getTodoItem(index);
      const editInput = await currentItem.findElement(By.css('.edit'));
      await this.driver.wait(until.elementIsVisible(editInput), TIMEOUT);
      await editInput.sendKeys(Key.CONTROL, 'a');
      await editInput.sendKeys(Key.BACK_SPACE);
      await editInput.sendKeys(originalText, Key.ENTER);
    }
  }

  // Regresa el contador de tareas activas
  async getActiveCount() {
    const label = await this.driver.findElement(TodoPage.TODO_COUNT_LABEL);
    const text = await label.getText();
    const match = text.match(/\d+/);
    return match ? parseInt(match[0], 10) : 0;
  }

  // Guarda una evidencia visual de la prueba ejecutada
  async takeScreenshot(testName) {
    const screenshotsDir = path.resolve(__dirname, '../../screenshots/selenium');
    fs.mkdirSync(screenshotsDir, { recursive: true });

    const fileName = testName
      .replace(/[^a-zA-Z0-9]+/g, '-')
      .replace(/^-|-$/g, '')
      .toLowerCase();
    const screenshotPath = path.join(screenshotsDir, `${fileName}.png`);
    const image = await this.driver.takeScreenshot();
    fs.writeFileSync(screenshotPath, image, 'base64');
    return screenshotPath;
  }
}

module.exports = { TodoPage };
