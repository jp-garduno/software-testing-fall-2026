const { test: base, expect } = require('@playwright/test');
const path = require('node:path');
const fs = require('node:fs');
const { TodoPage } = require('../pages/TodoPage');

const test = base.extend({
  todo: async ({ page }, use, testInfo) => {
    const todo = new TodoPage(page);
    await todo.navigate();
    const setupSeconds = todo.metrics[0].milliseconds / 1000;
    try {
      await use(todo);
    } finally {
      await testInfo.attach('metrics', {
        body: JSON.stringify({ setup_seconds: setupSeconds, operations: todo.metrics }),
        contentType: 'application/json',
      });
      const folder = path.resolve(__dirname, '../../screenshots');
      fs.mkdirSync(folder, { recursive: true });
      const name = testInfo.title.replace(/[^a-zA-Z0-9]+/g, '-');
      await page.screenshot({ path: path.join(folder, `playwright-${testInfo.project.name}-${name}.png`) });
    }
  },
});

module.exports = { test, expect };

