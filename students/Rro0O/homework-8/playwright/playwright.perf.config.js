const { defineConfig } = require("@playwright/test");
const functional = require("./playwright.config");

// One worker, so measurements never compete with each other for CPU or network.
module.exports = defineConfig({
  ...functional,
  testDir: "./perf",
  fullyParallel: false,
  workers: 1,
  timeout: 180000,
  reporter: [["list"]],
  use: { baseURL: functional.use.baseURL },
});
