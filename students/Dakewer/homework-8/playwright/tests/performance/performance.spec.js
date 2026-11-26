// Bonus C: page load and operation timings, with a generated report.
const fs = require('fs');
const path = require('path');
const { test, expect } = require('@playwright/test');
const { TodoPage } = require('../../pages/TodoPage');
const { BASE_URL } = require('../../config/target');

const ITERATIONS = Number(process.env.PERF_ITERATIONS || 10);
const OUTPUT_DIR = path.resolve(__dirname, '../../../reports/performance');
// Generous budgets (ms) on the median: they catch regressions, not noise.
const LOAD_BUDGET_MS = 3000;
const OPERATION_BUDGET_MS = 1000;

function summarize(samples) {
  const sorted = [...samples].sort((a, b) => a - b);
  const middle = Math.floor(sorted.length / 2);
  const median = sorted.length % 2 ? sorted[middle] : (sorted[middle - 1] + sorted[middle]) / 2;
  // Nearest-rank percentile.
  const p95 = sorted[Math.ceil(sorted.length * 0.95) - 1];
  return { samples: sorted.length, min: sorted[0], median, p95, max: sorted.at(-1) };
}

async function timed(operation) {
  const start = performance.now();
  await operation();
  return performance.now() - start;
}

function table(title, rows) {
  const lines = Object.entries(rows).map(([name, s]) =>
    `| ${name} | ${[s.min, s.median, s.p95, s.max].map((v) => v.toFixed(1)).join(' | ')} |`);
  const header = ['| Metric | Min | Median | p95 | Max |', '| --- | ---: | ---: | ---: | ---: |'];
  return [`## ${title}`, '', ...header, ...lines, ''].join('\n');
}

test('measure page load and todo operations', async ({ browser }) => {
  test.setTimeout(120_000);
  const load = { 'DOMContentLoaded': [], 'Load event': [], 'First contentful paint': [] };
  const operations = {};
  const record = async (name, operation) => (operations[name] ??= []).push(await timed(operation));

  for (let i = 0; i < ITERATIONS; i++) {
    // A new context per iteration means a cold HTTP cache.
    const context = await browser.newContext({ baseURL: BASE_URL });
    const page = await context.newPage();
    const todo = new TodoPage(page);
    await todo.navigate();
    await page.waitForFunction(() =>
      performance.getEntriesByType('navigation')[0].loadEventEnd > 0 &&
      performance.getEntriesByName('first-contentful-paint').length > 0);

    const timing = await page.evaluate(() => {
      const nav = performance.getEntriesByType('navigation')[0];
      const paint = performance.getEntriesByName('first-contentful-paint')[0];
      return { dcl: nav.domContentLoadedEventEnd, load: nav.loadEventEnd, fcp: paint.startTime };
    });
    load['DOMContentLoaded'].push(timing.dcl);
    load['Load event'].push(timing.load);
    load['First contentful paint'].push(timing.fcp);

    await record('Add 1 todo', async () => {
      await todo.addTodo('Single');
      await expect(todo.todoItems).toHaveCount(1);
    });
    await record('Add 50 todos', async () => {
      for (let n = 1; n <= 50; n++) await todo.addTodo(`Bulk ${n}`);
      await expect(todo.todoItems).toHaveCount(51);
    });
    await record('Toggle 1 todo (51 items)', async () => {
      await todo.toggleTodo(0);
      await expect(todo.toggle(0)).toBeChecked();
    });
    await record('Filter active (51 items)', async () => {
      await todo.filterActive();
      await expect(todo.todoItems).toHaveCount(50);
    });
    await record('Edit 1 todo', async () => {
      await todo.editTodo(0, 'Edited');
      await expect(todo.todoLabels.first()).toHaveText('Edited');
    });
    await record('Delete 1 todo', async () => {
      await todo.deleteTodo(0);
      await expect(todo.todoItems).toHaveCount(49);
    });
    await record('Toggle all', async () => {
      await todo.toggleAll();
      await expect(todo.todoCount).toHaveText('0 items left!');
    });
    await record('Clear completed (50 items)', async () => {
      await todo.clearCompleted();
      await expect(todo.todoCount).toBeHidden();
    });
    await context.close();
  }

  const summary = (group) => Object.fromEntries(Object.entries(group).map(([k, v]) => [k, summarize(v)]));
  const results = {
    url: BASE_URL,
    browser: `${browser.browserType().name()} ${browser.version()}`,
    platform: `${process.platform} ${process.arch}`,
    iterations: ITERATIONS,
    date: new Date().toISOString(),
    pageLoad: summary(load),
    operations: summary(operations),
  };

  const report = [
    '# Performance report', '',
    `- URL: ${results.url}`,
    `- Browser: ${results.browser} (${results.platform})`,
    `- Iterations: ${results.iterations}`,
    `- Date: ${results.date}`, '',
    'All values in milliseconds. Operation times are measured from the test',
    'process, so they include Playwright protocol overhead.', '',
    table('Page load', results.pageLoad),
    table('Operations', results.operations),
  ].join('\n');

  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  fs.writeFileSync(path.join(OUTPUT_DIR, 'performance-report.json'), JSON.stringify(results, null, 2));
  fs.writeFileSync(path.join(OUTPUT_DIR, 'performance-report.md'), report);
  await test.info().attach('performance-report', { body: report, contentType: 'text/markdown' });

  for (const [name, s] of Object.entries(results.pageLoad)) {
    expect.soft(s.median, `${name} median`).toBeLessThan(LOAD_BUDGET_MS);
  }
  for (const [name, s] of Object.entries(results.operations)) {
    // The bulk insert is 50 operations, so it gets a proportionally larger budget.
    const budget = name === 'Add 50 todos' ? OPERATION_BUDGET_MS * 10 : OPERATION_BUDGET_MS;
    expect.soft(s.median, `${name} median`).toBeLessThan(budget);
  }
});
