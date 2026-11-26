const URL = process.env.TODO_URL || "https://todomvc.com/examples/react/dist/";

class TodoPage {
  constructor(page) {
    this.page = page;
    this.newTodoInput = page.locator(".new-todo");
    this.items = page.locator(".todo-list li");
    this.labels = page.locator(".todo-list li label");
    this.clearCompletedBtn = page.locator(".clear-completed");
    this.filterAllLink = page.locator("a[href='#/']");
    this.filterActiveLink = page.locator("a[href='#/active']");
    this.filterCompletedLink = page.locator("a[href='#/completed']");
  }

  async navigate() {
    await this.page.goto(URL);
    await this.newTodoInput.waitFor();
  }

  async addTodo(text) {
    await this.newTodoInput.fill(text);
    await this.newTodoInput.press("Enter");
  }

  item(index) {
    return this.items.nth(index);
  }

  async getTodoCount() {
    return await this.items.count();
  }

  async getVisibleTodos() {
    return await this.labels.allTextContents();
  }

  async toggleTodo(index) {
    await this.item(index).locator(".toggle").click();
  }

  async deleteTodo(index) {
    const todo = this.item(index);
    await todo.hover(); // el botón .destroy solo aparece con hover
    await todo.locator(".destroy").click();
  }

  async editTodo(index, newText, commit = true) {
    const todo = this.item(index);
    await todo.locator("label").dblclick();
    const edit = todo.locator(".edit");
    await edit.fill(newText);
    await edit.press(commit ? "Enter" : "Escape");
  }

  async clearCompleted() {
    await this.clearCompletedBtn.click();
  }

  async filterAll() {
    await this.filterAllLink.click();
  }

  async filterActive() {
    await this.filterActiveLink.click();
  }

  async filterCompleted() {
    await this.filterCompletedLink.click();
  }
}

module.exports = { TodoPage };
