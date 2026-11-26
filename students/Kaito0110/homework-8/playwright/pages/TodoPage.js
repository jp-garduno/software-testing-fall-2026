class TodoPage {
  constructor(page) {
    this.page = page;
    this.newTodoInput = page.locator(".new-todo");
    this.todoItems = page.locator(".todo-list li");
    this.todoCount = page.locator(".todo-count");
  }

  async navigate() {
    await this.page.goto("./");
    await this.newTodoInput.waitFor({ state: "visible" });
  }

  async addTodo(text) {
    await this.newTodoInput.fill(text);
    await this.newTodoInput.press("Enter");
    await this.todoItems.first().waitFor({ state: "visible" });
  }

  async getTodoCount() {
    return this.todoItems.count();
  }

  async getVisibleTodos() {
    return this.todoItems.locator("label").allTextContents();
  }

  async toggleTodo(index) {
    await this.todoItems.nth(index).locator(".toggle").click();
  }

  async isCompleted(index) {
    return this.todoItems.nth(index).evaluate((item) =>
      item.classList.contains("completed"),
    );
  }

  async deleteTodo(index) {
    const item = this.todoItems.nth(index);
    await item.hover();
    await item.locator(".destroy").click();
    await item.waitFor({ state: "detached" });
  }

  async filterAll() {
    await this.page.locator("a[href='#/']").click();
  }

  async filterActive() {
    await this.page.locator("a[href='#/active']").click();
  }

  async filterCompleted() {
    await this.page.locator("a[href='#/completed']").click();
  }

  async getActiveCount() {
    const text = await this.todoCount.innerText();
    return Number.parseInt(text.trim().split(/\s+/)[0], 10);
  }

  async clearCompleted() {
    await this.page.locator(".clear-completed").click();
  }

  async editTodo(index, text, save = true) {
    const item = this.todoItems.nth(index);
    await item.locator("label").dblclick();
    const editor = item.locator("input.edit");
    if (save) {
      await editor.fill(text);
      await editor.press("Enter");
      return;
    }

    await editor.press("Escape");
    await this.newTodoInput.click();
  }
}

module.exports = { TodoPage };
