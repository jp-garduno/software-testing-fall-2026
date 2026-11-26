// Page Object for the TodoMVC React application.
// Actions rely on Playwright auto-waiting. Locators are public so tests can use
// web-first assertions, which retry until the expected state is reached.
class TodoPage {
  /** @param {import('@playwright/test').Page} page */
  constructor(page) {
    this.page = page;
    this.newTodoInput = page.locator('.new-todo');
    this.todoItems = page.locator('.todo-list li');
    this.todoLabels = page.locator('.todo-list li label');
    this.editInput = page.locator('.todo-list li .edit');
    this.title = page.locator('.header h1');
    this.todoCount = page.locator('.todo-count');
    this.toggleAllCheckbox = page.locator('.toggle-all');
    this.clearCompletedButton = page.locator('.clear-completed');
    this.selectedFilter = page.locator('.filters a.selected');
    this.filterAllLink = page.locator('a[href="#/"]');
    this.filterActiveLink = page.locator('a[href="#/active"]');
    this.filterCompletedLink = page.locator('a[href="#/completed"]');
  }

  // Navigation

  async navigate() {
    // An empty path resolves against `baseURL` from playwright.config.js.
    await this.page.goto('');
    await this.newTodoInput.waitFor();
  }

  // Creation

  async addTodo(text) {
    await this.newTodoInput.fill(text);
    await this.newTodoInput.press('Enter');
  }

  async addTodos(...texts) {
    for (const text of texts) {
      await this.addTodo(text);
    }
  }

  // Queries (immediate snapshots; prefer expect(locator) in assertions)

  async getTodoCount() {
    return this.todoItems.count();
  }

  async getVisibleTodos() {
    return this.todoLabels.allTextContents();
  }

  item(index) {
    return this.todoItems.nth(index);
  }

  toggle(index) {
    return this.item(index).locator('.toggle');
  }

  // Completion

  async toggleTodo(index) {
    // click() rather than check(): in a filtered view the item disappears.
    await this.toggle(index).click();
  }

  async toggleAll() {
    await this.toggleAllCheckbox.click();
  }

  // Deletion

  async deleteTodo(index) {
    const todo = this.item(index);
    await todo.hover();
    await todo.locator('.destroy').click();
  }

  async clearCompleted() {
    await this.clearCompletedButton.click();
  }

  // Editing

  async startEdit(index) {
    await this.item(index).locator('label').dblclick();
    await this.editInput.waitFor();
  }

  async typeEdit(text) {
    await this.editInput.fill(text);
  }

  async saveEdit() {
    await this.editInput.press('Enter');
    await this.editInput.waitFor({ state: 'hidden' });
  }

  async saveEditByBlur() {
    await this.title.click();
    await this.editInput.waitFor({ state: 'hidden' });
  }

  async cancelEdit() {
    await this.editInput.press('Escape');
  }

  async editTodo(index, text) {
    await this.startEdit(index);
    await this.typeEdit(text);
    await this.saveEdit();
  }

  // Filtering

  async filterAll() {
    await this.filterAllLink.click();
  }

  async filterActive() {
    // A text selector such as "text=Active" could also match a todo's title.
    await this.filterActiveLink.click();
  }

  async filterCompleted() {
    await this.filterCompletedLink.click();
  }
}

module.exports = { TodoPage };
