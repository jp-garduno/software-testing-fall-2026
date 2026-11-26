const { expect } = require("@playwright/test");

/** Page Object for the TodoMVC React app. Locators auto-wait, so no explicit waits are needed. */
class TodoPage {
  constructor(page) {
    this.page = page;
    this.newTodoInput = page.locator(".new-todo");
    this.todoItems = page.locator(".todo-list li");
    this.toggleAll = page.locator(".toggle-all");
    this.clearCompletedButton = page.locator(".clear-completed");
    this.footer = page.locator(".footer");
    this.itemsLeft = page.locator(".todo-count");
    this.selectedFilter = page.locator(".filters a.selected");
  }

  async navigate(route = "") {
    await this.page.goto(`./${route}`);
    await expect(this.newTodoInput).toBeVisible();
  }

  /** Open the app with empty browser storage. A fresh context already is empty; this is belt and braces. */
  async openClean() {
    await this.navigate();
    await this.page.evaluate(() => {
      window.localStorage.clear();
      window.sessionStorage.clear();
    });
    await this.navigate();
  }

  item(index) {
    return this.todoItems.nth(index);
  }

  async addTodo(text) {
    await this.newTodoInput.fill(text);
    await this.newTodoInput.press("Enter");
  }

  async addTodos(...texts) {
    for (const text of texts) {
      await this.addTodo(text);
    }
  }

  async getTodoCount() {
    return this.todoItems.count();
  }

  async getVisibleTodos() {
    return this.todoItems.locator("label").allTextContents();
  }

  async toggleTodo(index) {
    await this.item(index).locator(".toggle").click();
  }

  async toggleAllTodos() {
    await this.toggleAll.click();
  }

  async deleteTodo(index) {
    const todo = this.item(index);
    await todo.hover();
    await todo.locator(".destroy").click();
  }

  async clearCompleted() {
    await this.clearCompletedButton.click();
  }

  async startEdit(index) {
    await this.item(index).locator("label").dblclick();
  }

  async typeInEdit(index, text) {
    await this.item(index).locator(".edit").fill(text);
  }

  async saveEdit(index) {
    await this.item(index).locator(".edit").press("Enter");
  }

  /** Leave the edit field by clicking elsewhere; the app saves on blur. */
  async blurEdit() {
    await this.newTodoInput.click();
  }

  async editTodo(index, newText) {
    await this.startEdit(index);
    await this.typeInEdit(index, newText);
    await this.saveEdit(index);
  }

  async cancelEdit(index) {
    await this.item(index).locator(".edit").press("Escape");
  }

  async filterAll() {
    await this.page.getByRole("link", { name: "All" }).click();
  }

  async filterActive() {
    await this.page.getByRole("link", { name: "Active" }).click();
  }

  async filterCompleted() {
    await this.page.getByRole("link", { name: "Completed" }).click();
  }
}

module.exports = { TodoPage };
