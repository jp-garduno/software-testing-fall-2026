const { spawnSync } = require("node:child_process");
const { writeFileSync } = require("node:fs");
const { resolve } = require("node:path");
const { loadOrders, loadCustomers, loadWorkflows } = require("../tests/testData");

const orders = loadOrders();
const customers = loadCustomers();
const workflows = loadWorkflows();
if (orders.length < 25 || customers.length < 30 || workflows.length < 3) {
  throw new Error("Expected at least 25 orders, 30 customers, and 3 workflows");
}
if (process.argv.includes("--validate-only")) return;

const root = resolve(__dirname, "..");
const run = spawnSync(process.execPath, [
  "--test", "--test-reporter=spec", "--experimental-test-coverage",
  "--test-coverage-include=src/*.js", "--test-coverage-lines=81", "tests/*.test.js"
], { cwd: root, encoding: "utf8" });

if (run.error) throw run.error;
const output = run.stdout + run.stderr;
writeFileSync(resolve(root, "test_results.txt"), output);
const coverage = output.match(/start of coverage report[\s\S]*?end of coverage report/);
if (coverage) {
  const report = coverage[0].split(/\r?\n/).map(line => line.replace(/^ℹ\s?/, "")).join("\n");
  const escaped = report.replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;");
  writeFileSync(resolve(root, "coverage_report.html"), `<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Homework 7 · Coverage</title>
<style>
body { font: 17px system-ui, sans-serif; background: #f4f7fa; color: #182537; margin: 3rem auto; padding: 0 1rem; max-width: 65rem; }
pre { background: white; border: 1px solid #d6e0ec; border-radius: .5rem; padding: 1rem; overflow: auto; }
</style>
<h1>Homework 7 test coverage</h1>
<p>Node.js ${process.version} · Production modules in <code>src/</code></p>
<pre>${escaped}</pre>
</html>
`);
}
process.stdout.write(output);
process.exitCode = run.status ?? 1;
