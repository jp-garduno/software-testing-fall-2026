/**
 * Setup cost of one Playwright test, split like scripts/measure_setup.py:
 * "browser_start" (launch + context + page), "new_context" (what each test pays when the
 * browser is reused) and "navigation" (loading the application, mostly network).
 */

const { chromium } = require("@playwright/test");
const { TodoPage } = require("../pages/TodoPage");
const config = require("../playwright.config");

const ITERATIONS = 10;

function median(values) {
  const sorted = [...values].sort((a, b) => a - b);
  const middle = sorted.length / 2;
  return (sorted[Math.floor(middle - 0.5)] + sorted[Math.floor(middle)]) / 2;
}

/** Seconds taken by an async action, plus whatever it returns. */
async function timeIt(action) {
  const start = performance.now();
  const value = await action();
  return [(performance.now() - start) / 1000, value];
}

async function newPage(browser) {
  const context = await browser.newContext({ baseURL: config.use.baseURL });
  return context.newPage();
}

async function main() {
  const browserStart = [];
  const newContext = [];
  const navigation = [];
  let version = "";

  for (let i = 0; i < ITERATIONS; i += 1) {
    const [startSeconds, [browser, page]] = await timeIt(async () => {
      const launched = await chromium.launch();
      return [launched, await newPage(launched)];
    });
    browserStart.push(startSeconds);
    const [navigationSeconds] = await timeIt(() => new TodoPage(page).navigate());
    navigation.push(navigationSeconds);
    const [contextSeconds] = await timeIt(() => newPage(browser));
    newContext.push(contextSeconds);
    version = browser.version();
    await browser.close();
  }

  const result = {
    browser_start: median(browserStart),
    new_context: median(newContext),
    navigation: median(navigation),
    version,
    iterations: ITERATIONS,
  };
  process.stdout.write(`${JSON.stringify(result)}\n`);
}

main();
