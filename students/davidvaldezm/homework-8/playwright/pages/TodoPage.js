/** TodoMVC interactions shared by all acceptance tests. */
class TodoPage {
  constructor(page) {
    this.page = page;
    this.newTodoInput = page.locator('.new-todo');
    this.todoItems = page.locator('.todo-list li');
    this.labels = this.todoItems.locator('label');
    this.counter = page.locator('.todo-count');
  }

  async navigate() {
    await this.page.goto(process.env.TODO_URL || 'https://todomvc.com/examples/react/dist/');
    await this.newTodoInput.waitFor({ state: 'visible' });
  }

  async addTodo(text) {
    await this.newTodoInput.fill(text);
    await this.newTodoInput.press('Enter');
  }

  checkbox(index) {
    return this.todoItems.nth(index).locator('.toggle');
  }

  async toggleTodo(index) {
    await this.checkbox(index).click();
  }

  async completeAll() {
    await this.page.locator('.toggle-all').check();
  }

  async deleteTodo(index) {
    const item = this.todoItems.nth(index);
    await item.hover();
    await item.locator('.destroy').click();
  }

  async clearCompleted() {
    await this.page.locator('.clear-completed').click();
  }

  async filterBy(name) {
    await this.page.getByRole('link', { name, exact: true }).click();
  }

  async editTodo(index, text, save = 'enter') {
    await this.todoItems.nth(index).locator('label').dblclick();
    const editor = this.page.locator('li.editing .edit');
    await editor.fill(text);
    if (save === 'blur') {
      await this.newTodoInput.click();
    } else {
      await editor.press(save === 'cancel' ? 'Escape' : 'Enter');
    }
    await editor.waitFor({ state: 'hidden', timeout: 10000 });
  }

  async reload() {
    await this.page.reload();
    await this.newTodoInput.waitFor({ state: 'visible' });
  }
}

module.exports = { TodoPage };
