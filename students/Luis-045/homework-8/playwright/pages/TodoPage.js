const { expect } = require("@playwright/test");

class TodoPage {
  constructor(page) {
    this.page = page;
    this.newTodoInput = page.locator(".new-todo");
    this.todoItems = page.locator(".todo-list li:visible");
    this.editInput = page.locator(".todo-list .edit:visible");
    this.activeCount = page.locator(".todo-count");
  }

  async navigate() {
    await this.page.goto("./");
    await expect(this.newTodoInput).toBeVisible();
  }

  async addTodo(text) {
    await this.newTodoInput.fill(text);
    await this.newTodoInput.press("Enter");
  }

  async getTodoCount() {
    return this.todoItems.count();
  }

  async getVisibleTodos() {
    return this.todoItems.locator("label").allTextContents();
  }

  async expectTodos(texts) {
    await expect(this.todoItems.locator("label")).toHaveText(texts);
  }

  async toggleTodo(index) {
    await this.todoItems.nth(index).locator(".toggle").click();
  }

  async expectCompleted(index, completed = true) {
    await expect(this.todoItems.nth(index).locator(".toggle")).toBeChecked({
      checked: completed,
    });
    if (completed) {
      await expect(this.todoItems.nth(index)).toHaveClass(/completed/);
    } else {
      await expect(this.todoItems.nth(index)).not.toHaveClass(/completed/);
    }
  }

  async expectActiveCount(count) {
    await expect(this.activeCount).toHaveText(
      new RegExp(`^${count} items? left!$`),
    );
  }

  async deleteTodo(index) {
    const item = this.todoItems.nth(index);
    await item.hover();
    await item.locator(".destroy").click();
  }

  async clearCompleted() {
    await this.page
      .getByRole("button", { name: "Clear completed", exact: true })
      .click();
  }

  async filterBy(name) {
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

  async beginEdit(index) {
    await this.todoItems.nth(index).locator("label").dblclick();
    await expect(this.editInput).toBeVisible();
  }

  async replaceEditText(text) {
    await this.editInput.fill(text);
  }

  async expectEditText(text) {
    await expect(this.editInput).toHaveValue(text);
  }

  async finishEdit() {
    await this.editInput.press("Enter");
    await expect(this.editInput).toHaveCount(0);
  }

  async cancelEdit() {
    await this.editInput.press("Escape");
    await expect(this.editInput).toHaveCount(0);
  }

  async blurEdit() {
    await this.newTodoInput.click();
    await expect(this.editInput).toHaveCount(0);
  }
}

module.exports = { TodoPage };
