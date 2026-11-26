/** Page Object for the TodoMVC React application (Playwright). */

class TodoPage {
  constructor(page) {
    this.page = page;
    this.newTodoInput = page.locator(".new-todo");
    this.todoItems = page.locator(".todo-list li");
    this.itemLabels = page.locator(".todo-list li label");
    this.completedItems = page.locator(".todo-list li.completed");
    this.editInputs = page.locator(".todo-list li input.edit");
    this.toggleAllCheckbox = page.locator(".toggle-all");
    this.counter = page.locator(".todo-count");
    this.clearCompletedButton = page.locator(".clear-completed");
    this.heading = page.locator("h1");
    this.sidebar = page.locator("aside.learn");
    this.selectedFilter = page.locator(".filters a.selected");
  }

  // Navigation

  /** Opens the application. The base URL comes from playwright.config.js. */
  async navigate() {
    await this.page.goto("./");
    await this.newTodoInput.waitFor();
    // The sidebar is fetched after the page loads and pushes the list sideways;
    // a click in progress at that moment is lost.
    await this.sidebar.waitFor();
  }

  // Actions

  /** Types a todo and presses Enter. Blank text is ignored by the application. */
  async addTodo(text) {
    await this.newTodoInput.fill(text);
    await this.newTodoInput.press("Enter");
  }

  async addTodos(...texts) {
    for (const text of texts) {
      await this.addTodo(text);
    }
  }

  /** Flips the completion checkbox of the visible todo at `index`. */
  async toggleTodo(index) {
    await this.todoItems.nth(index).locator(".toggle").click();
  }

  async toggleAll() {
    await this.toggleAllCheckbox.click();
  }

  /** Hovers the todo to reveal its destroy button, then clicks it. */
  async deleteTodo(index) {
    const item = this.todoItems.nth(index);
    await item.hover();
    await item.locator(".destroy").click();
  }

  async startEdit(index) {
    await this.todoItems.nth(index).locator("label").dblclick();
  }

  /** Replaces the content of an open edit field without submitting it. */
  async typeInEdit(index, text) {
    await this.editInput(index).fill(text);
  }

  async pressEnterInEdit(index) {
    await this.editInput(index).press("Enter");
  }

  async pressEscapeInEdit(index) {
    await this.editInput(index).press("Escape");
  }

  /** Moves focus away from the edit field by clicking the page heading. */
  async blurEdit() {
    await this.heading.click();
  }

  /** Edits a todo and saves it with Enter. */
  async editTodo(index, newText) {
    await this.startEdit(index);
    await this.typeInEdit(index, newText);
    await this.pressEnterInEdit(index);
  }

  async filterAll() {
    await this.filterLink("All").click();
  }

  async filterActive() {
    await this.filterLink("Active").click();
  }

  async filterCompleted() {
    await this.filterLink("Completed").click();
  }

  async clearCompleted() {
    await this.clearCompletedButton.click();
  }

  // Locators and queries. Tests assert on locators so Playwright can retry them.

  item(index) {
    return this.todoItems.nth(index);
  }

  editInput(index) {
    return this.todoItems.nth(index).locator("input.edit");
  }

  filterLink(name) {
    return this.page.getByRole("link", { name, exact: true });
  }

  async getTodoCount() {
    return this.todoItems.count();
  }

  async getVisibleTodos() {
    return this.itemLabels.allTextContents();
  }
}

module.exports = { TodoPage };
