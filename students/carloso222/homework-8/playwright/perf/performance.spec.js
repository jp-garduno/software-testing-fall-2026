// Bonus C - performance metrics with Playwright (run: npm run test:perf).
// Measures browser start-up, page load and the time of each user operation, and writes
// ../bonus/performance/results/playwright.json. bonus/performance/selenium_perf.py measures the
// same things with Selenium, and bonus/performance/generate_report.py compares both.
const fs = require('fs');
const os = require('os');
const path = require('path');
const { test, expect } = require('@playwright/test');
const { TodoPage } = require('../pages/TodoPage');

const RUNS = Number(process.env.PERF_RUNS || 5);
const BULK = 20;
const OUTPUT = path.resolve(__dirname, '..', '..', 'bonus', 'performance', 'results', 'playwright.json');

const results = { tool: 'Playwright', runs: RUNS, setup: [], pageLoad: [], operations: {} };

async function timed(action) {
  const start = performance.now();
  await action();
  return performance.now() - start;
}

function record(name, ms) {
  (results.operations[name] = results.operations[name] || []).push(Number(ms.toFixed(1)));
}

test.describe.configure({ mode: 'serial' });

test.describe('Performance metrics', () => {
  test('browser start-up (setup time)', async ({ playwright, browserName, channel, headless }) => {
    test.setTimeout(120000);
    for (let i = 0; i < RUNS; i += 1) {
      let browser;
      const ms = await timed(async () => {
        browser = await playwright[browserName].launch({ channel, headless });
        const context = await browser.newContext();
        await context.newPage();
      });
      results.setup.push(Number(ms.toFixed(1)));
      await browser.close();
    }
  });

  test('page load', async ({ page, browser, channel }) => {
    test.setTimeout(120000);
    const via = channel ? ` (channel: ${channel})` : ' (bundled)';
    results.browser = `${browser.browserType().name()} ${browser.version()}${via}`;
    const todoPage = new TodoPage(page);
    for (let i = 0; i < RUNS; i += 1) {
      await page.goto('about:blank');
      const wall = await timed(() => page.goto(todoPage.baseUrl, { waitUntil: 'load' }));
      const timing = await page.evaluate(() => {
        const nav = performance.getEntriesByType('navigation')[0];
        const fcp = performance.getEntriesByName('first-contentful-paint')[0];
        return {
          ttfb: nav.responseStart,
          domContentLoaded: nav.domContentLoadedEventEnd,
          load: nav.loadEventEnd,
          fcp: fcp ? fcp.startTime : null,
        };
      });
      results.pageLoad.push({ wall: Number(wall.toFixed(1)), ...timing });
    }
  });

  test('user operations', async ({ page }) => {
    test.setTimeout(180000);
    const todoPage = new TodoPage(page);
    const bulk = Array.from({ length: BULK }, (_, i) => `Bulk task ${i + 1}`);

    for (let i = 0; i < RUNS; i += 1) {
      await page.goto('about:blank');
      await todoPage.navigate();

      record('add_1_todo', await timed(async () => {
        await todoPage.addTodo('First task');
        await expect(todoPage.todoItems).toHaveCount(1);
      }));
      record(`add_${BULK}_todos`, await timed(async () => {
        await todoPage.addTodos(...bulk);
        await expect(todoPage.todoItems).toHaveCount(BULK + 1);
      }));
      record('toggle_1_todo', await timed(async () => {
        await todoPage.toggleTodo(0);
        await expect(todoPage.item(0)).toHaveClass(/completed/);
      }));
      record('toggle_all', await timed(async () => {
        await todoPage.toggleAll();
        await expect(todoPage.todoCount).toHaveText('0 items left!');
      }));
      record('filter_active', await timed(async () => {
        await todoPage.filterActive();
        await expect(todoPage.filters.Active).toHaveClass(/selected/);
      }));
      record('filter_completed', await timed(async () => {
        await todoPage.filterCompleted();
        await expect(todoPage.filters.Completed).toHaveClass(/selected/);
      }));
      record('filter_all', await timed(async () => {
        await todoPage.filterAll();
        await expect(todoPage.filters.All).toHaveClass(/selected/);
      }));
      record('edit_1_todo', await timed(async () => {
        await todoPage.editTodo(0, 'Edited task');
        await expect(todoPage.todoLabels.first()).toHaveText('Edited task');
      }));
      record('delete_1_todo', await timed(async () => {
        await todoPage.deleteTodo(0);
        await expect(todoPage.todoItems).toHaveCount(BULK);
      }));
      record('clear_completed', await timed(async () => {
        await todoPage.clearCompleted();
        await expect(todoPage.footer).toBeHidden();
      }));
    }
  });

  test.afterAll(() => {
    results.environment = {
      os: `${os.type()} ${os.release()}`,
      node: process.version,
      baseUrl: process.env.BASE_URL || require('../pages/TodoPage').DEFAULT_BASE_URL,
      measuredAt: new Date().toISOString(),
    };
    fs.mkdirSync(path.dirname(OUTPUT), { recursive: true });
    fs.writeFileSync(OUTPUT, `${JSON.stringify(results, null, 2)}\n`);
  });
});
