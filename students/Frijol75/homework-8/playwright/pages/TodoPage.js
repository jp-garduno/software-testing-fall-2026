/**
 * Page Object Model (POM) for TodoMVC React Application using Playwright.
 * URL: https://todomvc.com/examples/react/dist/
 */

class TodoPage {
  constructor(page) {
    this.page = page;
    this.url = "https://todomvc.com/examples/react/dist/";
    this.newTodoInput = ".header .new-todo, #todo-input";
    this.todoList = ".todo-list";
    this.todoItems = ".todo-list li";
    this.toggleAllCheckbox = ".toggle-all, #toggle-all";
    this.clearCompletedButton = ".clear-completed";
    this.todoCountSpan = ".todo-count";
    this.filterAllLink = "a[href='#/']";
    this.filterActiveLink = "a[href='#/active']";
    this.filterCompletedLink = "a[href='#/completed']";
  }

  async navigate() {
    await this.page.goto(this.url);
    await this.page.locator(this.newTodoInput).waitFor({ state: "visible" });
  }

  async addTodo(text) {
    const input = this.page.locator(this.newTodoInput);
    await input.fill(text);
    await input.press("Enter");
  }

  async addTodos(items) {
    for (const item of items) {
      await this.addTodo(item);
    }
  }

  async getTodoCount() {
    return await this.page.locator(this.todoItems).count();
  }

  async getVisibleTodos() {
    const labels = this.page.locator(`${this.todoItems} label`);
    const count = await labels.count();
    const results = [];
    for (let i = 0; i < count; i++) {
      const text = await labels.nth(i).textContent();
      results.push((text || "").trim());
    }
    return results;
  }

  async toggleTodo(index) {
    await this.page
      .locator(this.todoItems)
      .nth(index)
      .locator(".toggle")
      .click();
  }

  async isTodoCompleted(index) {
    const item = this.page.locator(this.todoItems).nth(index);
    const classAttr = (await item.getAttribute("class")) || "";
    if (classAttr.split(/\s+/).includes("completed")) {
      return true;
    }
    return await item.locator(".toggle").isChecked();
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
    await todo.locator("label").dblclick();
    const editInput = todo.locator("input.edit, input.new-todo, input[type='text']");
    await editInput.fill(newText);
    await editInput.press("Enter");
  }

  async cancelEditTodo(index, tempText) {
    const todo = this.page.locator(this.todoItems).nth(index);
    const originalText = ((await todo.locator("label").textContent()) || "").trim();
    await todo.locator("label").dblclick();
    const editInput = todo.locator("input.edit, input.new-todo, input[type='text']");
    await editInput.fill(tempText);
    await editInput.press("Escape");
    if (await editInput.isVisible()) {
      await editInput.fill(originalText);
      await editInput.press("Enter");
    } else {
      const visible = await this.getVisibleTodos();
      if (visible[index] !== originalText) {
        await this.editTodo(index, originalText);
      }
    }
  }

  async filterAll() {
    await this.page.locator(this.filterAllLink).click();
  }

  async filterActive() {
    await this.page.locator(this.filterActiveLink).click();
  }

  async filterCompleted() {
    await this.page.locator(this.filterCompletedLink).click();
  }

  async getActiveCount() {
    const text = (await this.page.locator(this.todoCountSpan).textContent()) || "0";
    const match = text.match(/(\d+)/);
    return match ? parseInt(match[1], 10) : 0;
  }

  async takeScreenshot(filepath) {
    await this.page.screenshot({ path: filepath });
  }
}

module.exports = { TodoPage };

