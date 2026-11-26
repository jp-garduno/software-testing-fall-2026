// Custom Playwright fixture: every test receives a `todoPage` already opened on an empty list.
// Each test runs in a new browser context, so tests are isolated and can run in parallel.
const path = require('path');
const base = require('@playwright/test');
const { TodoPage } = require('../pages/TodoPage');

const SCREENSHOTS_DIR = path.resolve(__dirname, '..', '..', 'screenshots', 'playwright');

function fileName(testInfo) {
  const title = testInfo.titlePath.slice(1).join(' ');
  return `${title.replace(/[^A-Za-z0-9_.-]+/g, '_')}.png`;
}

const test = base.test.extend({
  todoPage: async ({ page }, use, testInfo) => {
    const todoPage = new TodoPage(page);
    await todoPage.navigate();
    await use(todoPage);
    // Evidence for the report: SAVE_SCREENSHOTS=1 keeps the final state of every test.
    if (process.env.SAVE_SCREENSHOTS === '1') {
      await page.screenshot({ path: path.join(SCREENSHOTS_DIR, testInfo.project.name, fileName(testInfo)) });
    }
  },
});

module.exports = { test, expect: base.expect };
