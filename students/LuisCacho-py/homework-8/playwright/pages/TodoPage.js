/**
 * Part 2: Playwright Page Object Model for the TodoMVC React application.
 */
class TodoPage {
  constructor(page) {
    this.page = page;
    this.url = "https://todomvc.com/examples/react/dist/";
    this.newTodoInput = ".new-todo";
    this.todoList = ".todo-list";
    this.todoItems = ".todo-list li";
    this.toggleAllCheckbox = ".toggle-all";
    this.clearCompletedButton = ".clear-completed";
    this.todoCountLabel = ".todo-count";
  }

  async navigate() {
    await this.page.goto(this.url);
  }

  async addTodo(text) {
    await this.page.fill(this.newTodoInput, text);
    await this.page.press(this.newTodoInput, "Enter");
  }

  async addTodos(texts) {
    for (const text of texts) {
      await this.addTodo(text);
    }
  }

  async getTodoCount() {
    return await this.page.locator(this.todoItems).count();
  }

  async getActiveCount() {
    const countLocator = this.page.locator(this.todoCountLabel);
    if ((await countLocator.count()) === 0) {
      return 0;
    }
    const text = await countLocator.textContent();
    const match = (text || "").trim().match(/^(\d+)/);
    return match ? parseInt(match[1], 10) : 0;
  }

  async toggleTodo(index) {
    await this.page
      .locator(this.todoItems)
      .nth(index)
      .locator(".toggle")
      .click();
  }

  async toggleAll() {
    await this.page.locator(this.toggleAllCheckbox).click();
  }

  async isTodoCompleted(index) {
    const classAttr = await this.page
      .locator(this.todoItems)
      .nth(index)
      .getAttribute("class");
    return Boolean(classAttr && classAttr.split(/\s+/).includes("completed"));
  }

  async deleteTodo(index) {
    const todo = this.page.locator(this.todoItems).nth(index);
    await todo.hover();
    await todo.locator(".destroy").click();
  }

  async clearCompleted() {
    await this.page.locator(this.clearCompletedButton).click();
  }

  async editTodo(index, newText) {
    const todo = this.page.locator(this.todoItems).nth(index);
    await todo.dblclick();
    const editInput = todo.locator(".edit");
    await editInput.fill(newText);
    await editInput.press("Enter");
  }

  async cancelEditTodo(index, tempText) {
    const todo = this.page.locator(this.todoItems).nth(index);
    await todo.dblclick();
    const editInput = todo.locator(".edit");
    await editInput.fill(tempText);
    await editInput.press("Escape");
  }

  async filterAll() {
    await this.page.click("a[href='#/']");
  }

  async filterActive() {
    await this.page.click("a[href='#/active']");
  }

  async filterCompleted() {
    await this.page.click("a[href='#/completed']");
  }

  async getVisibleTodos() {
    const rawTexts = await this.page
      .locator(`${this.todoItems} label`)
      .allTextContents();
    return rawTexts.map((item) => item.trim());
  }
}

module.exports = { TodoPage };
