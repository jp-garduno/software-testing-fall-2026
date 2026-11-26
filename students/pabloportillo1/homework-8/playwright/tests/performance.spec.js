const { performance } = require("node:perf_hooks");
const { test, expect } = require("@playwright/test");
const { TodoPage } = require("../pages/TodoPage");

const RUNS = 5;
const BULK_SIZE = 50;
const BUDGET_MS = { pageLoad: 5000, addBulk: 15000 };

async function timed(action) {
  const start = performance.now();
  await action();
  return performance.now() - start;
}

function median(values) {
  const sorted = [...values].sort((a, b) => a - b);
  const middle = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[middle] : (sorted[middle - 1] + sorted[middle]) / 2;
}

async function measureRun(page) {
  const todoPage = new TodoPage(page);
  const pageLoad = await timed(async () => {
    await todoPage.navigate();
    await expect(todoPage.newTodoInput).toBeVisible();
  });
  const navigation = await page.evaluate(() => performance.getEntriesByType("navigation")[0].toJSON());
  const titles = Array.from({ length: BULK_SIZE }, (_, index) => `Task ${index + 1}`);
  return {
    pageLoad,
    domContentLoaded: navigation.domContentLoadedEventEnd,
    loadEvent: navigation.loadEventEnd,
    addOne: await timed(async () => {
      await todoPage.addTodo("First task");
      await expect(todoPage.items).toHaveCount(1);
    }),
    addBulk: await timed(async () => {
      await todoPage.addTodo(...titles);
      await expect(todoPage.items).toHaveCount(BULK_SIZE + 1);
    }),
    toggleAll: await timed(async () => {
      await todoPage.toggleAll();
      await expect(todoPage.counter).toHaveText("0 items left!");
    }),
    filterSwitch: await timed(async () => {
      await todoPage.filterActive();
      await expect(todoPage.items).toHaveCount(0);
    }),
    clearCompleted: await timed(async () => {
      await todoPage.filterBy("All");
      await todoPage.clearCompleted();
      await expect(todoPage.items).toHaveCount(0);
    }),
  };
}

test("performance: page load and operation times", { tag: "@performance" }, async ({ browser }, testInfo) => {
  test.setTimeout(120000);
  const runs = [];
  for (let run = 0; run < RUNS; run += 1) {
    const context = await browser.newContext({ baseURL: testInfo.project.use.baseURL });
    runs.push(await measureRun(await context.newPage()));
    await context.close();
  }
  const medians = Object.fromEntries(
    Object.keys(runs[0]).map((metric) => [metric, median(runs.map((r) => r[metric]))]),
  );

  await testInfo.attach("performance", {
    body: JSON.stringify({ browser: testInfo.project.name, runs: RUNS, bulkSize: BULK_SIZE, medians }),
    contentType: "application/json",
  });

  expect(medians.pageLoad).toBeLessThan(BUDGET_MS.pageLoad);
  expect(medians.addBulk).toBeLessThan(BUDGET_MS.addBulk);
});
