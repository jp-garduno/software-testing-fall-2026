// Page Object for the TodoMVC React app, driven with Playwright.
// Playwright locators wait automatically (until the element exists, is visible and enabled),
// so unlike the Selenium version there are no explicit waits in the actions.

const FILTER_NAMES = ["All", "Active", "Completed"];

class TodoPage {
  /**
   * @param {import('@playwright/test').Page} page
   */
  constructor(page) {
    this.page = page;
    this.title = page.locator(".todoapp h1");
    this.newTodoInput = page.locator("input.new-todo");
    this.todoItems = page.locator(".todo-list li");
    this.toggleAllCheckbox = page.locator("input.toggle-all");
    this.todoCount = page.locator(".todo-count");
    this.clearCompletedButton = page.locator("button.clear-completed");
    this.footer = page.locator("footer.footer");
    this.filterLinks = page.locator(".filters a");
  }

  /** Open the app with an empty list (the React example keeps todos in memory only). */
  async navigate() {
    await this.page.goto("./");
    await this.newTodoInput.waitFor();
  }

  /** Type a todo and press Enter. */
  async addTodo(text) {
    await this.newTodoInput.fill(text);
    await this.newTodoInput.press("Enter");
  }

  async addTodos(...texts) {
    for (const text of texts) {
      await this.addTodo(text);
    }
  }

  item(index) {
    return this.todoItems.nth(index);
  }

  async getTodoCount() {
    return this.todoItems.count();
  }

  /** Texts of the todos currently shown, top to bottom. */
  async getVisibleTodos() {
    return this.todoItems.locator("label").allTextContents();
  }

  async toggleTodo(index) {
    await this.item(index).locator("input.toggle").click();
  }

  async toggleAll() {
    await this.toggleAllCheckbox.click();
  }

  /** Hover the todo so its × button appears, then click it. */
  async deleteTodo(index) {
    const todo = this.item(index);
    await todo.hover();
    await todo.locator("button.destroy").click();
  }

  async clearCompleted() {
    await this.clearCompletedButton.click();
  }

  /** Double-click the label; returns the edit field that replaces it. */
  async startEditing(index) {
    await this.item(index).locator("label").dblclick();
    return this.item(index).locator("input.edit");
  }

  /** Replace a todo's text and save it with Enter. */
  async editTodo(index, newText) {
    const field = await this.startEditing(index);
    await field.fill(newText);
    await field.press("Enter");
  }

  /** Replace the text in edit mode without saving yet (to test blur and Escape). */
  async typeInEdit(index, newText) {
    const field = await this.startEditing(index);
    await field.fill(newText);
    return field;
  }

  /** Blur the edit field by clicking the page title; the app saves on blur. */
  async leaveEditByClickingOutside() {
    await this.title.click();
  }

  async filterBy(name) {
    if (!FILTER_NAMES.includes(name)) {
      throw new Error(`Unknown filter "${name}"; use All, Active or Completed`);
    }
    await this.page.getByRole("link", { name, exact: true }).click();
  }

  async filterAll() {
    await this.filterBy("All");
  }

  async filterActive() {
    await this.filterBy("Active");
  }

  async filterCompleted() {
    await this.filterBy("Completed");
  }

  filterLink(name) {
    return this.page.getByRole("link", { name, exact: true });
  }
}

module.exports = { TodoPage, FILTER_NAMES };
