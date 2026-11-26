// Bonus C - performance metrics.
// Measures page load (Navigation Timing API) and how long the main operations take, then
// writes reports/performance.json and reports/performance.md. The budgets are deliberately
// generous: the goal is to catch a big regression, not to benchmark the machine.
const fs = require("fs");
const path = require("path");
const { performance } = require("perf_hooks");
const { test, expect } = require("@playwright/test");
const { TodoPage } = require("../pages/TodoPage");

const BULK = 50;
const REPORT_DIR = path.join(__dirname, "..", "reports");
const results = [];

test.describe.configure({ mode: "serial" });

async function timed(name, budgetMs, action) {
  const start = performance.now();
  await action();
  const ms = Math.round(performance.now() - start);
  results.push({ metric: name, ms, budgetMs });
  expect(ms, `${name} took ${ms} ms (budget ${budgetMs} ms)`).toBeLessThan(budgetMs);
}

test("page load timing", async ({ page }) => {
  const todoPage = new TodoPage(page);
  await todoPage.navigate();

  const timing = await page.evaluate(() => {
    const [nav] = performance.getEntriesByType("navigation");
    return {
      ttfb: nav.responseStart - nav.requestStart,
      domContentLoaded: nav.domContentLoadedEventEnd - nav.startTime,
      load: nav.loadEventEnd - nav.startTime,
    };
  });
  for (const [metric, value] of Object.entries(timing)) {
    results.push({ metric: `page ${metric}`, ms: Math.round(value), budgetMs: 5000 });
    expect(value).toBeLessThan(5000);
  }
});

test(`bulk operations with ${BULK} tasks`, async ({ page }) => {
  const todoPage = new TodoPage(page);
  await todoPage.navigate();
  const texts = Array.from({ length: BULK }, (_, i) => `Task ${i + 1}`);

  await timed(`add ${BULK} tasks`, 15000, async () => {
    await todoPage.addTodos(...texts);
    await expect(todoPage.todoItems).toHaveCount(BULK);
  });
  await timed(`toggle all ${BULK} tasks`, 3000, async () => {
    await todoPage.toggleAll();
    await expect(todoPage.todoCount).toHaveText("0 items left!");
  });
  await timed("switch to Active filter", 3000, async () => {
    await todoPage.filterActive();
    await expect(todoPage.todoItems).toHaveCount(0);
  });
  await timed("switch to All filter", 3000, async () => {
    await todoPage.filterAll();
    await expect(todoPage.todoItems).toHaveCount(BULK);
  });
  await timed(`clear ${BULK} completed tasks`, 3000, async () => {
    await todoPage.clearCompleted();
    await expect(todoPage.todoItems).toHaveCount(0);
  });
});

test.afterAll(() => {
  fs.mkdirSync(REPORT_DIR, { recursive: true });
  fs.writeFileSync(path.join(REPORT_DIR, "performance.json"), `${JSON.stringify(results, null, 2)}\n`);
  const rows = results.map((r) => `| ${r.metric} | ${r.ms} | ${r.budgetMs} | ${r.ms < r.budgetMs ? "✅" : "❌"} |`);
  const markdown = [
    "# Performance report",
    "",
    `Generated ${new Date().toISOString()} against ${process.env.BASE_URL || "the live TodoMVC site"}.`,
    "",
    "| Metric | Time (ms) | Budget (ms) | OK |",
    "| ------ | --------- | ----------- | -- |",
    ...rows,
    "",
  ].join("\n");
  fs.writeFileSync(path.join(REPORT_DIR, "performance.md"), markdown);
});
