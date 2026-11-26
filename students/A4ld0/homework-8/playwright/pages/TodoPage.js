const { expect } = require('@playwright/test');
const { performance } = require('node:perf_hooks');

class TodoPage {
  constructor(page) {
    this.page = page;
    this.input = page.locator('.new-todo');
    this.items = page.locator('.todo-list li');
    this.labels = this.items.locator('label');
    this.metrics = [];
  }

  record(operation, start) {
    this.metrics.push({ operation, milliseconds: performance.now() - start });
  }

  async navigate() {
    const start = performance.now();
    await this.page.goto(process.env.TODO_URL || 'https://todomvc.com/examples/react/');
    await expect(this.input).toBeVisible();
    this.record('page_load', start);
  }

  async addTodo(text) {
    const start = performance.now();
    const count = await this.getTodoCount();
    await this.input.fill(text);
    await this.input.press('Enter');
    await expect(this.items).toHaveCount(count + 1);
    this.record('add', start);
  }

  async getTodoCount() {
    return this.items.count();
  }

  async getVisibleTodos() {
    return this.labels.allTextContents();
  }

  async isCompleted(index) {
    return this.items.nth(index).locator('.toggle').isChecked();
  }

  async toggleTodo(index) {
    const start = performance.now();
    const toggle = this.items.nth(index).locator('.toggle');
    const previous = await toggle.isChecked();
    await toggle.click();
    await expect(toggle).toBeChecked({ checked: !previous });
    this.record('toggle', start);
  }

  async deleteTodo(index) {
    const start = performance.now();
    const count = await this.getTodoCount();
    const item = this.items.nth(index);
    await item.hover();
    await item.locator('.destroy').click();
    await expect(this.items).toHaveCount(count - 1);
    this.record('delete', start);
  }

  async clearCompleted() {
    const start = performance.now();
    const remaining = await this.page.locator('.todo-list li:not(.completed)').count();
    await this.page.locator('.clear-completed').click();
    await expect(this.items).toHaveCount(remaining);
    this.record('clear_completed', start);
  }

  async filterBy(name) {
    const start = performance.now();
    const targets = { All: '#/', Active: '#/active', Completed: '#/completed' };
    const filter = this.page.locator(`a[href="${targets[name]}"]`);
    await filter.click();
    await expect(filter).toHaveClass(/selected/);
    this.record('filter', start);
  }

  async activeCount() {
    const text = await this.page.locator('.todo-count').innerText();
    return Number.parseInt(text, 10);
  }

  async editTodo(index, text, save = true) {
    const start = performance.now();
    const item = this.items.nth(index);
    const label = item.locator('label');
    const original = await label.innerText();
    await label.dblclick();
    const editor = item.locator('.edit');
    await editor.fill(text);
    await editor.press(save ? 'Enter' : 'Escape');
    await expect(label).toHaveText(save ? text : original);
    this.record(save ? 'edit' : 'cancel_edit', start);
  }
}

module.exports = { TodoPage };

