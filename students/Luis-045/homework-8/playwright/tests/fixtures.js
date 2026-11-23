const path = require("node:path");
const { test: base, expect } = require("@playwright/test");
const { TodoPage } = require("../pages/TodoPage");

const test = base.extend({
  todoPage: async ({ page, browser }, use, testInfo) => {
    const todoPage = new TodoPage(page);
    await todoPage.navigate();
    testInfo.annotations.push({
      type: "browser_version",
      description: browser.version(),
    });
    await use(todoPage);
    const name = testInfo.title.replace(/[^a-z0-9]+/gi, "-").toLowerCase();
    await page.screenshot({
      path: path.join(__dirname, "../../screenshots", `playwright-${name}.png`),
    });
  },
});

module.exports = { test, expect };
