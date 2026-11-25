// Page Object for TodoMVC React (https://todomvc.com/examples/react/dist/).
// It exposes locators and user actions; the tests make the assertions with Playwright's
// web-first `expect`, which retries until the UI reaches the expected state.

// The URL in the homework statement (https://todomvc.com/examples/react/) returns 404;
// the React example is served from /dist/.
const DEFAULT_BASE_URL = 'https://todomvc.com/examples/react/dist/';

class TodoPage {
  /**
   * @param {import('@playwright/test').Page} page
   * @param {string} [baseUrl]
   */
  constructor(page, baseUrl = process.env.BASE_URL || DEFAULT_BASE_URL) {
    this.page = page;
    this.baseUrl = baseUrl;

    this.newTodoInput = page.locator('.new-todo');
    this.todoList = page.locator('.todo-list');
    this.todoItems = page.locator('.todo-list li');
    this.todoLabels = page.locator('.todo-list li label');
    // Transparent checkbox laid over the chevron: it is what receives the user's click.
    this.toggleAllInput = page.locator('.toggle-all');
    this.clearCompletedButton = page.locator('.clear-completed');
    this.todoCount = page.locator('.todo-count');
    this.footer = page.locator('.footer');
    this.selectedFilter = page.locator('.filters a.selected');
    // The edit box shares data-testid="text-input" with the new-todo box, so getByTestId()
    // would match two elements while editing; it is located by class instead.
    this.editInput = page.locator('.todo-list li.editing .edit');
    this.filters = {
      All: page.locator('a[href="#/"]'),
      Active: page.locator('a[href="#/active"]'),
      Completed: page.locator('a[href="#/completed"]'),
    };
  }

  async navigate() {
    // todomvc.com also loads Google Analytics and learn.json; waiting for the full "load" event
    // made Firefox hang for up to 30 s, so wait for the DOM and then for the app's input.
    await this.page.goto(this.baseUrl, { waitUntil: 'domcontentloaded' });
    await this.newTodoInput.waitFor();
  }

  /** @param {string} text */
  async addTodo(text) {
    await this.newTodoInput.fill(text);
    await this.newTodoInput.press('Enter');
  }

  /** @param {...string} texts */
  async addTodos(...texts) {
    for (const text of texts) {
      await this.addTodo(text);
    }
  }

  /** @param {number} index */
  item(index) {
    return this.todoItems.nth(index);
  }

  async getTodoCount() {
    return this.todoItems.count();
  }

  async getVisibleTodos() {
    return this.todoLabels.allTextContents();
  }

  /** Number shown in the footer counter ("2 items left!"); 0 when the footer is hidden. */
  async getActiveCount() {
    if (!(await this.todoCount.isVisible())) {
      return 0;
    }
    const text = await this.todoCount.textContent();
    return Number.parseInt(text, 10);
  }

  /** @param {number} index */
  async toggleTodo(index) {
    await this.item(index).locator('.toggle').click();
  }

  async toggleAll() {
    await this.toggleAllInput.click();
  }

  /** Hover to reveal the (CSS-hidden) delete button, then click it. */
  async deleteTodo(index) {
    const todo = this.item(index);
    await todo.hover();
    await todo.locator('.destroy').click();
  }

  async clearCompleted() {
    await this.clearCompletedButton.click();
  }

  /** Double-click a label to open its edit box. */
  async startEditing(index) {
    await this.item(index).locator('label').dblclick();
    await this.editInput.waitFor();
    return this.editInput;
  }

  /**
   * Replace a todo's text and commit it with Enter or by leaving the box (blur).
   * @param {number} index
   * @param {string} newText
   * @param {{ commit?: 'enter' | 'blur' }} [options]
   */
  async editTodo(index, newText, { commit = 'enter' } = {}) {
    const field = await this.startEditing(index);
    await field.fill(newText);
    await field.press(commit === 'blur' ? 'Tab' : 'Enter');
  }

  /** Type into the edit box and press Escape (TodoMVC spec: Escape discards the change). */
  async cancelEdit(index, typedText) {
    const field = await this.startEditing(index);
    await field.fill(typedText);
    await field.press('Escape');
  }

  async filterAll() {
    await this.applyFilter('All');
  }

  async filterActive() {
    await this.applyFilter('Active');
  }

  async filterCompleted() {
    await this.applyFilter('Completed');
  }

  /** @param {'All' | 'Active' | 'Completed'} name */
  async applyFilter(name) {
    await this.filters[name].click();
  }
}

module.exports = { TodoPage, DEFAULT_BASE_URL };
