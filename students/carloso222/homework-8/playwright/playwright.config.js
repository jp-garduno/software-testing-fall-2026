// Playwright configuration for Homework 8.
//   npm test                    -> Chromium only (used for the Selenium vs Playwright comparison)
//   npm run test:cross-browser  -> Chromium, Firefox and WebKit, 4 workers (bonus B)
//   npm run test:perf           -> performance metrics (bonus C)
// Environment variables: BASE_URL, HEADLESS=0, SAVE_SCREENSHOTS=1, PW_WORKERS, PW_TIMEOUT (ms),
// PW_CHANNEL=chrome|msedge (use an installed browser instead of the bundled Chromium).
const path = require('path');
const { defineConfig, devices } = require('@playwright/test');
const { DEFAULT_BASE_URL } = require('./pages/TodoPage');

const channel = process.env.PW_CHANNEL ? { channel: process.env.PW_CHANNEL } : {};
const jsonReport = process.env.PW_JSON_REPORT || path.join(__dirname, '..', 'reports', 'playwright-results.json');

module.exports = defineConfig({
  testDir: './tests',
  outputDir: process.env.PW_OUTPUT_DIR || 'test-results',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  workers: process.env.PW_WORKERS ? Number(process.env.PW_WORKERS) : undefined,
  timeout: Number(process.env.PW_TIMEOUT || 30000),
  expect: { timeout: 5000 },
  reporter: [
    ['list'],
    ['html', { open: 'never', outputFolder: 'playwright-report' }],
    ['json', { outputFile: jsonReport }],
  ],
  use: {
    baseURL: process.env.BASE_URL || DEFAULT_BASE_URL,
    headless: process.env.HEADLESS !== '0',
    actionTimeout: 10000,
    navigationTimeout: 15000,
    screenshot: 'only-on-failure',
    trace: 'retain-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'], ...channel } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    { name: 'perf', testDir: './perf', fullyParallel: false, use: { ...devices['Desktop Chrome'], ...channel } },
  ],
});
