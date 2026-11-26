// Tiny Playwright reporter: dump setup and test durations to $BENCH_OUT.
const fs = require('fs');

class TimingReporter {
  totals = { tests: 0, setup: 0, total: 0, failed: 0 };

  onStepEnd(test, result, step) {
    // "Before Hooks" covers fixtures (browser, context, page) and beforeEach.
    if (!step.parent && step.title === 'Before Hooks') this.totals.setup += step.duration / 1000;
  }

  onTestEnd(test, result) {
    this.totals.tests += 1;
    this.totals.total += result.duration / 1000;
    if (test.outcome() === 'unexpected') this.totals.failed += 1;
  }

  onEnd() {
    fs.writeFileSync(process.env.BENCH_OUT, JSON.stringify(this.totals));
  }
}

module.exports = TimingReporter;
