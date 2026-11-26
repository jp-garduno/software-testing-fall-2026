const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");
const { version } = require("@playwright/test/package.json");

class MetricsReporter {
  constructor() {
    this.tests = [];
  }

  onBegin(config) {
    this.workers = config.workers;
    this.url = config.projects[0].use.baseURL;
  }

  onTestEnd(test, result) {
    const setup = result.steps.find((step) => step.title === "Before Hooks");
    const teardown = result.steps.find((step) => step.title === "After Hooks");
    this.tests.push({
      name: test.title,
      outcome:
        test.expectedStatus === "failed" && result.status === "failed"
          ? "xfailed"
          : result.status === test.expectedStatus
            ? "passed"
            : "failed",
      actual_status: result.status,
      expected_status: test.expectedStatus,
      error: result.error?.message,
      total_seconds: result.duration / 1000,
      setup_seconds: (setup?.duration || 0) / 1000,
      teardown_seconds: (teardown?.duration || 0) / 1000,
      browser: test.annotations.find((item) => item.type === "browser_version")
        ?.description,
    });
  }

  onEnd(result) {
    const count = this.tests.length;
    const report = {
      framework: "playwright",
      status: result.status,
      total_seconds: result.duration / 1000,
      average_per_test_seconds: count ? result.duration / 1000 / count : 0,
      average_setup_seconds: count
        ? this.tests.reduce((sum, test) => sum + test.setup_seconds, 0) / count
        : 0,
      versions: {
        node: process.version,
        playwright: version,
        browser: this.tests[0]?.browser,
      },
      platform: `${os.platform()} ${os.release()} ${os.arch()}`,
      url: this.url,
      workers: this.workers,
      tests: this.tests,
      passed: this.tests.filter((test) => test.outcome === "passed").length,
      failed: this.tests.filter((test) => test.outcome === "failed").length,
      expected_failures: this.tests.filter((test) => test.outcome === "xfailed")
        .length,
    };
    const directory = path.join(__dirname, "../reports");
    fs.mkdirSync(directory, { recursive: true });
    const filename = process.env.PW_REPORT_NAME || "playwright-results.json";
    fs.writeFileSync(
      path.join(directory, filename),
      JSON.stringify(report, null, 2) + "\n",
    );
  }
}

module.exports = MetricsReporter;
