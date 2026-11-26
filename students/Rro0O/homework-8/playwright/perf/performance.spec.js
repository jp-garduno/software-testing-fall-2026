/**
 * Bonus C: page load and operation timings, one JSON file per browser.
 * Run with `npm run test:perf`; PERFORMANCE_REPORT.md summarises the JSON written to reports/.
 */

const fs = require("fs");
const path = require("path");
const { test, expect } = require("@playwright/test");
const { TodoPage } = require("../pages/TodoPage");

const ITERATIONS = 5;
const TODO_COUNT = 50;
const REPORTS_DIR = path.resolve(__dirname, "..", "..", "reports");

// Generous ceilings: they catch a broken or badly degraded page, not normal network noise.
const BUDGET_MS = { load: 10000, addTodos: 15000, toggleAll: 2000, filter: 2000, clearCompleted: 2000 };

/** Milliseconds taken by an async action, including the assertion that proves it finished. */
async function timeIt(action) {
  const start = process.hrtime.bigint();
  await action();
  return Number(process.hrtime.bigint() - start) / 1e6;
}

function median(values) {
  const sorted = [...values].sort((a, b) => a - b);
  return sorted[Math.floor(sorted.length / 2)];
}

function summarize(samples) {
  return {
    median: median(samples),
    min: Math.min(...samples),
    max: Math.max(...samples),
  };
}

async function measureOnce(context) {
  const page = await context.newPage();
  const todoPage = new TodoPage(page);
  const result = {};

  result.load = await timeIt(() => todoPage.navigate());
  const navigation = await page.evaluate(() => {
    const [entry] = performance.getEntriesByType("navigation");
    const paint = performance.getEntriesByName("first-contentful-paint")[0];
    return {
      domContentLoaded: entry.domContentLoadedEventEnd,
      loadEvent: entry.loadEventEnd,
      firstContentfulPaint: paint ? paint.startTime : null,
    };
  });
  Object.assign(result, navigation);

  result.addTodos = await timeIt(async () => {
    for (let i = 1; i <= TODO_COUNT; i += 1) {
      await todoPage.addTodo(`Task ${i}`);
    }
    await expect(todoPage.todoItems).toHaveCount(TODO_COUNT);
  });
  result.toggleAll = await timeIt(async () => {
    await todoPage.toggleAll();
    await expect(todoPage.completedItems).toHaveCount(TODO_COUNT);
  });
  result.filter = await timeIt(async () => {
    await todoPage.filterActive();
    await expect(todoPage.todoItems).toHaveCount(0);
  });
  await todoPage.filterAll();
  result.clearCompleted = await timeIt(async () => {
    await todoPage.clearCompleted();
    await expect(todoPage.todoItems).toHaveCount(0);
  });

  await page.close();
  return result;
}

test("page load and operation timings stay within budget", async ({ browser, browserName, baseURL }) => {
  const runs = [];
  for (let i = 0; i < ITERATIONS; i += 1) {
    const context = await browser.newContext({ baseURL });
    runs.push(await measureOnce(context));
    await context.close();
  }

  const metrics = {};
  for (const name of Object.keys(runs[0])) {
    const samples = runs.map((run) => run[name]).filter((value) => value !== null);
    if (samples.length > 0) {
      metrics[name] = summarize(samples);
    }
  }

  fs.mkdirSync(REPORTS_DIR, { recursive: true });
  const report = {
    browser: browserName,
    version: browser.version(),
    iterations: ITERATIONS,
    todoCount: TODO_COUNT,
    metrics,
  };
  fs.writeFileSync(path.join(REPORTS_DIR, `performance-${browserName}.json`), `${JSON.stringify(report, null, 2)}\n`);

  for (const [name, budget] of Object.entries(BUDGET_MS)) {
    expect(metrics[name].median, `median ${name}`).toBeLessThan(budget);
  }
});
