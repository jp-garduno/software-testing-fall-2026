const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests',
  fullyParallel: true,
  workers: 1,
  retries: 0,
  timeout: 30000,
  expect: { timeout: 10000 },
  reporter: [
    ['list'],
    ['html', { open: 'never' }],
    ['json', { outputFile: '../reports/live/playwright-results.json' }],
    ['junit', { outputFile: '../reports/live/playwright-results.xml' }],
  ],
  use: {
    channel: 'chrome',
    headless: process.env.HEADED !== '1',
    viewport: { width: 1280, height: 900 },
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    launchOptions: process.env.CHROME_BINARY ? { executablePath: process.env.CHROME_BINARY } : {},
  },
});
