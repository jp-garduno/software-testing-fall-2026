const { defineConfig, devices } = require("@playwright/test");

/**
 * Playwright configuration supporting Cross-Browser Testing (Bonus Option B:
 * Chromium, Firefox, and WebKit) plus screenshot capture on failure.
 */
module.exports = defineConfig({
  testDir: "./tests",
  timeout: 30000,
  fullyParallel: true,
  retries: 0,
  reporter: [["list"], ["html", { open: "never" }]],
  use: {
    baseURL: "https://todomvc.com/examples/react/dist/",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
    {
      name: "firefox",
      use: { ...devices["Desktop Firefox"] },
    },
    {
      name: "webkit",
      use: { ...devices["Desktop Safari"] },
    },
  ],
});
