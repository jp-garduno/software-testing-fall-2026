const { defineConfig, devices } = require("@playwright/test");

module.exports = defineConfig({
  testDir: "./tests",
  fullyParallel: true,
  forbidOnly: Boolean(process.env.CI),
  retries: 0,
  workers: 2,
  timeout: 30000,
  expect: { timeout: 10000 },
  reporter: [["list"], ["html", { open: "never" }], ["./metrics-reporter.js"]],
  use: {
    baseURL:
      process.env.TODO_BASE_URL || "https://todomvc.com/examples/react/dist/",
    viewport: { width: 1280, height: 900 },
    locale: "en-US",
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
  },
  projects: [
    {
      name: "chrome",
      use: { ...devices["Desktop Chrome"], channel: "chrome" },
    },
  ],
});
