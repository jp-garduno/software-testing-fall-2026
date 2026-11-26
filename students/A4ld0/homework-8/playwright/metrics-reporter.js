const fs = require('node:fs');
const path = require('node:path');

class MetricsReporter {
  constructor() {
    this.tests = [];
  }

  onTestEnd(test, result) {
    const attachment = result.attachments.find(item => item.name === 'metrics');
    const metrics = attachment?.body ? JSON.parse(attachment.body.toString()) : {};
    this.tests.push({
      test: test.title,
      browser: test.parent.project().name,
      status: result.status,
      duration_seconds: result.duration / 1000,
      ...metrics,
    });
  }

  onEnd(result) {
    const folder = path.resolve(__dirname, '../reports');
    fs.mkdirSync(folder, { recursive: true });
    const filename = process.env.PLAYWRIGHT_METRICS_FILE || 'playwright-metrics.json';
    fs.writeFileSync(path.join(folder, filename), JSON.stringify({
      total_seconds: result.duration / 1000,
      status: result.status,
      tests: this.tests,
    }, null, 2));
  }
}

module.exports = MetricsReporter;

