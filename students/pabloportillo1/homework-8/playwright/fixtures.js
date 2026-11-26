const base = require("@playwright/test");
const { TodoPage } = require("./pages/TodoPage");

const test = base.test.extend({
  todoPage: async ({ page }, use) => {
    const todoPage = new TodoPage(page);
    await todoPage.navigate();
    await use(todoPage);
  },
});

module.exports = { test, expect: base.expect };
