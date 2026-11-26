const { defineConfig } = require("@playwright/test");

module.exports = defineConfig({
  testDir: "./tests",
  fullyParallel: true,
  workers: 4,
  reporter: "list",
  use: {
    baseURL: "https://todomvc.com/examples/react/dist/",
    browserName: "chromium",
    headless: true,
    actionTimeout: 10000,
    navigationTimeout: 20000,
  },
});
