class TodoPage {
  constructor(page) {
    this.page = page;
    this.url = "https://demo.playwright.dev/todomvc/";
    this.newTodoInput = ".new-todo";
    this.todoItems = ".todo-list li";
    this.todoLabels = ".todo-list li label";
    this.clearCompletedBtn = ".clear-completed";
    this.todoCount = ".todo-count";
  }

  async navigate() {
    await this.page.goto(this.url);
    await this.page.waitForSelector(this.newTodoInput);
  }

  async addTodo(text) {
    await this.page.fill(this.newTodoInput, text);
    await this.page.press(this.newTodoInput, "Enter");
  }

  async getTodoCount() {
    return await this.page.locator(this.todoItems).count();
  }

  async getVisibleTodos() {
    return await this.page.locator(this.todoLabels).allTextContents();
  }

  async isTodoCompleted(index) {
    const className =
      (await this.page.locator(this.todoItems).nth(index).getAttribute("class")) || "";
    return className.split(" ").includes("completed");
  }

  async toggleTodo(index) {
    await this.page.locator(this.todoItems).nth(index).locator(".toggle").click();
  }

  async deleteTodo(index) {
    const todo = this.page.locator(this.todoItems).nth(index);
    await todo.hover();
    await todo.locator(".destroy").click();
  }

  async editTodo(index, newText, save = true) {
    const todo = this.page.locator(this.todoItems).nth(index);
    await todo.locator("label").dblclick();

    const editInput = todo.locator("input.edit");
    await editInput.fill(newText);

    if (save) {
      await editInput.press("Enter");
    } else {
      await editInput.press("Escape");
    }
  }

  async clearCompleted() {
    await this.page.click(this.clearCompletedBtn);
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

  async getActiveCount() {
    const locator = this.page.locator(this.todoCount);
    if ((await locator.count()) === 0) return 0;
    const text = (await locator.textContent()).trim();
    return parseInt(text.split(" ")[0], 10);
  }
}

module.exports = { TodoPage };