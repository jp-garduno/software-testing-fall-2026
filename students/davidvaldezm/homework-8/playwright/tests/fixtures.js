const { test: base, expect } = require('@playwright/test');
const { performance } = require('node:perf_hooks');
const { TodoPage } = require('../pages/TodoPage');

const test = base.extend({
  todo: async ({ page }, use, testInfo) => {
    const start = performance.now();
    const todo = new TodoPage(page);
    await todo.navigate();
    testInfo.annotations.push({ type: 'setup_ms', description: String(performance.now() - start) });
    await use(todo);
  },
  mixed: async ({ todo }, use) => {
    for (const text of ['Task 1', 'Task 2', 'Task 3']) await todo.addTodo(text);
    await todo.toggleTodo(1);
    await use(todo);
  },
});

module.exports = { test, expect };
