// Playwright configuration for the TodoMVC suite.
// BASE_URL overrides the target (for example a local copy of the app); the default is the
// live example. The assignment's /examples/react/ link answers 404, the app lives in /dist/.
const { defineConfig, devices } = require("@playwright/test");

const baseURL = process.env.BASE_URL || "https://todomvc.com/examples/react/dist/";

module.exports = defineConfig({
  testDir: "./tests",
  fullyParallel: true,
  workers: process.env.CI ? 2 : undefined,
  retries: 0,
  timeout: 30000,
  expect: {
    timeout: 5000,
    toHaveScreenshot: { maxDiffPixelRatio: 0.01 },
  },
  // One baseline per screenshot name, without the browser/OS suffix Playwright adds by default.
  snapshotPathTemplate: "{testDir}/__screenshots__/{testFileName}/{arg}{ext}",
  reporter: [["list"], ["html", { open: "never", outputFolder: "playwright-report" }]],
  use: {
    baseURL,
    viewport: { width: 1280, height: 900 },
    screenshot: "only-on-failure",
    trace: "retain-on-failure",
  },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"], viewport: { width: 1280, height: 900 } } }],
});
