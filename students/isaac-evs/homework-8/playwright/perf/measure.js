// Performance metrics for TodoMVC (bonus C): page-load timings and the duration of user operations.
// Usage: node perf/measure.js [runs] [outputFile]   (TODOMVC_URL selects the app)
const fs = require("fs");
const path = require("path");
const { chromium } = require("@playwright/test");

const RUNS = Number(process.argv[2]) || 10;
const OUTPUT = process.argv[3] || path.join(__dirname, "results.json");
const URL =
  process.env.TODOMVC_URL || "https://todomvc.com/examples/react/dist/";
const BULK = 100;

const now = () => performance.now();

async function timed(fn) {
  const start = now();
  await fn();
  return now() - start;
}

async function oneRun(browser) {
  const context = await browser.newContext();
  const page = await context.newPage();
  const input = page.locator(".new-todo");
  const items = page.locator(".todo-list li");
  const metrics = {};

  metrics["page ready (goto + input visible)"] = await timed(async () => {
    await page.goto(URL);
    await input.waitFor({ state: "visible" });
  });
  const nav = await page.evaluate(() => {
    const entry = performance.getEntriesByType("navigation")[0];
    const paint = performance.getEntriesByName("first-contentful-paint")[0];
    return {
      dom: entry.domContentLoadedEventEnd,
      load: entry.loadEventEnd,
      fcp: paint ? paint.startTime : null,
      transfer: entry.transferSize,
    };
  });
  metrics["DOMContentLoaded"] = nav.dom;
  metrics["load event"] = nav.load;
  if (nav.fcp !== null) metrics["first contentful paint"] = nav.fcp;

  metrics["add 1 task"] = await timed(async () => {
    await input.fill("First task");
    await input.press("Enter");
    await items.first().waitFor();
  });
  metrics[`add ${BULK - 1} more tasks (total)`] = await timed(async () => {
    for (let i = 2; i <= BULK; i += 1) {
      await input.fill(`Task ${i}`);
      await input.press("Enter");
    }
    await page.waitForFunction(
      (n) => document.querySelectorAll(".todo-list li").length === n,
      BULK,
    );
  });
  metrics[`toggle all (${BULK} tasks)`] = await timed(async () => {
    await page.locator(".toggle-all").check();
    await page.waitForFunction(
      (n) => document.querySelectorAll(".todo-list li.completed").length === n,
      BULK,
    );
  });
  metrics[`filter Active (${BULK} completed, none shown)`] = await timed(
    async () => {
      await page.getByRole("link", { name: "Active" }).click();
      await page.waitForFunction(
        () => document.querySelectorAll(".todo-list li").length === 0,
      );
    },
  );
  metrics[`filter Completed (${BULK} shown)`] = await timed(async () => {
    await page.getByRole("link", { name: "Completed" }).click();
    await page.waitForFunction(
      (n) => document.querySelectorAll(".todo-list li").length === n,
      BULK,
    );
  });
  metrics[`clear completed (${BULK} tasks)`] = await timed(async () => {
    await page.locator(".clear-completed").click();
    await page.waitForFunction(
      () => document.querySelectorAll(".todo-list li").length === 0,
    );
  });
  await page.evaluate(() => {
    window.location.hash = "#/"; // the footer, and its All link, is hidden while the list is empty
  });
  await input.fill("Delete me");
  await input.press("Enter");
  metrics["delete 1 task"] = await timed(async () => {
    await items.first().hover();
    await items.first().locator(".destroy").click();
    await page.waitForFunction(
      () => document.querySelectorAll(".todo-list li").length === 0,
    );
  });

  await context.close();
  return metrics;
}

function summarize(samples) {
  const sorted = [...samples].sort((a, b) => a - b);
  const pick = (q) =>
    sorted[Math.min(sorted.length - 1, Math.floor(q * sorted.length))];
  return {
    median: pick(0.5),
    p90: pick(0.9),
    min: sorted[0],
    max: sorted[sorted.length - 1],
  };
}

(async () => {
  const browser = await chromium.launch();
  const runs = [];
  for (let i = 0; i < RUNS; i += 1) runs.push(await oneRun(browser));
  await browser.close();

  const summary = {};
  for (const name of Object.keys(runs[0])) {
    summary[name] = summarize(
      runs.map((run) => run[name]).filter((value) => typeof value === "number"),
    );
  }
  const result = {
    url: URL,
    runs: RUNS,
    browser: "chromium",
    date: new Date().toISOString(),
    summary,
  };
  fs.writeFileSync(OUTPUT, `${JSON.stringify(result, null, 2)}\n`);

  console.log(`${URL}  (${RUNS} runs, times in ms)`);
  for (const [name, s] of Object.entries(summary)) {
    console.log(
      `${name.padEnd(44)} median ${s.median.toFixed(1).padStart(8)}  p90 ${s.p90.toFixed(1).padStart(8)}`,
    );
  }
})();
