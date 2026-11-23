// @ts-check
const { defineConfig, devices } = require("@playwright/test");

// The assignment points at /examples/react/, which now answers 404; the app lives under /dist/.
const rawUrl =
  process.env.TODOMVC_URL || "https://todomvc.com/examples/react/dist/";
const baseURL = rawUrl.endsWith("/") ? rawUrl : `${rawUrl}/`;

module.exports = defineConfig({
  testDir: "./tests",
  fullyParallel: true,
  retries: process.env.CI ? 1 : 0,
  workers: process.env.CI ? 2 : undefined,
  reporter: [
    ["list"],
    ["html", { open: "never" }],
    ["json", { outputFile: "test-results/results.json" }],
  ],
  use: {
    baseURL,
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
  },
  // Visual regression is opt-in (VISUAL=1): baselines are platform-specific screenshots.
  projects: [
    { name: "chromium", use: { ...devices["Desktop Chrome"] } },
    { name: "firefox", use: { ...devices["Desktop Firefox"] } },
    { name: "webkit", use: { ...devices["Desktop Safari"] } },
    ...(process.env.VISUAL
      ? [
          {
            name: "visual",
            testDir: "./visual",
            snapshotPathTemplate:
              "{testDir}/baselines/{arg}-{projectName}-{platform}{ext}",
            use: {
              ...devices["Desktop Chrome"],
              viewport: { width: 1280, height: 800 },
            },
          },
        ]
      : []),
  ],
});
