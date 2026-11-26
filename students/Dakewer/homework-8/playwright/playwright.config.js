// @ts-check
const { defineConfig, devices } = require('@playwright/test');
const { BASE_URL } = require('./config/target');

module.exports = defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  reporter: [['list'], ['html', { open: 'never' }]],
  use: {
    baseURL: BASE_URL,
    screenshot: 'only-on-failure',
    trace: 'retain-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      testMatch: 'todo-*.spec.js',
      use: {
        ...devices['Desktop Chrome'],
        // PW_CHANNEL=chromium runs the full browser instead of the headless shell.
        channel: process.env.PW_CHANNEL,
      },
    },
    {
      name: 'visual',
      testMatch: 'visual/*.spec.js',
      use: { ...devices['Desktop Chrome'], channel: 'chromium' },
      // A retry would hide a real visual difference behind a second run.
      retries: 0,
    },
    {
      name: 'performance',
      testMatch: 'performance/*.spec.js',
      use: { ...devices['Desktop Chrome'], channel: 'chromium', trace: 'off' },
      retries: 0,
    },
  ],
});
