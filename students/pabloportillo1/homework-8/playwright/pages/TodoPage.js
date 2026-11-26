/**
 * Page object for the TodoMVC React app. Actions return once Playwright has performed them; tests assert with
 * web-first expect() calls on the exposed locators, which retry until the page catches up.
 */
class TodoPage {
  constructor(page) {
    this.page = page;
    this.newTodoInput = page.locator("input.new-todo");
    this.items = page.locator(".todo-list li");
    this.labels = page.locator(".todo-list li label");
    this.editor = page.locator(".todo-list li.editing input.edit");
    this.toggleAllCheckbox = page.locator("input.toggle-all");
    this.counter = page.locator(".todo-count");
    this.clearCompletedButton = page.locator("button.clear-completed");
    this.selectedFilter = page.locator(".filters a.selected");
  }

  async navigate(route = "") {
    await this.page.goto(`./${route}`);
  }

  item(index) {
    return this.items.nth(index);
  }

  async addTodo(...texts) {
    for (const text of texts) {
      await this.newTodoInput.fill(text);
      await this.newTodoInput.press("Enter");
    }
  }

  async toggleTodo(index) {
    await this.item(index).locator("input.toggle").click();
  }

  async toggleAll() {
    await this.toggleAllCheckbox.click();
  }

  async deleteTodo(index) {
    const item = this.item(index);
    await item.hover();
    await item.locator("button.destroy").click();
  }

  async clearCompleted() {
    await this.clearCompletedButton.click();
  }

  async openEditor(index) {
    await this.item(index).locator("label").dblclick();
    return this.editor;
  }

  async startEditing(index, text) {
    const editor = await this.openEditor(index);
    await editor.fill(text);
    return editor;
  }

  async editTodo(index, text) {
    const editor = await this.startEditing(index, text);
    await editor.press("Enter");
  }

  async cancelEditing() {
    await this.editor.press("Escape");
  }

  async filterBy(name) {
    await this.page.locator(".filters").getByRole("link", { name, exact: true }).click();
  }

  async filterActive() {
    await this.filterBy("Active");
  }

  async filterCompleted() {
    await this.filterBy("Completed");
  }

  async getTodoCount() {
    return this.items.count();
  }

  async getVisibleTodos() {
    return this.labels.allTextContents();
  }
}

module.exports = { TodoPage };
