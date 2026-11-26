const { spawnSync } = require("node:child_process");
const { readFileSync, writeFileSync } = require("node:fs");
const { basename, resolve } = require("node:path");
const { loadOrders, loadCustomers, loadWorkflows } = require("../tests/testData");

function writeReports() {
  const root = resolve(__dirname, "..");
  const run = spawnSync(process.execPath, [require.resolve("jest/bin/jest"), "--coverage", "--runInBand"], {
    cwd: root, encoding: "utf8", env: { ...process.env, FORCE_COLOR: "0" }
  });

  if (run.error) throw run.error;
  const output = (run.stdout + run.stderr).replace(/[ \t]+$/gm, "");
  writeFileSync(resolve(root, "test_results.txt"), output);
  if (run.status === 0) {
    const summary = JSON.parse(readFileSync(resolve(root, "coverage/coverage-summary.json"), "utf8"));
    const rows = Object.entries(summary).map(([file, metrics]) => {
      const label = file === "total" ? "All production files" : basename(file);
      const cells = ["statements", "branches", "functions", "lines"]
        .map(metric => `<td>${metrics[metric].pct}%</td>`).join("");
      return `<tr><th scope="row">${label}</th>${cells}</tr>`;
    });
    writeFileSync(resolve(root, "coverage_report.html"), `<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Homework 7 coverage</title>
<style>
body { font: 17px system-ui, sans-serif; color: #182537; margin: 3rem auto; padding: 0 1rem; max-width: 52rem; }
table { border-collapse: collapse; width: 100%; }
th, td { padding: .75rem; border-bottom: 1px solid #d6e0ec; text-align: left; }
</style>
<h1>Homework 7 test coverage</h1>
<p>Jest coverage for production modules in <code>src/</code></p>
<table>
<thead><tr><th>File</th><th>Statements</th><th>Branches</th><th>Functions</th><th>Lines</th></tr></thead>
<tbody>${rows.join("\n")}</tbody>
</table>
</html>
`);
  }
  process.stdout.write(output);
  process.exitCode = run.status ?? 1;
}

const orders = loadOrders();
const customers = loadCustomers();
const workflows = loadWorkflows();
if (orders.length < 25 || customers.length < 30 || workflows.length < 3) {
  throw new Error("Expected at least 25 orders, 30 customers, and 3 workflows");
}
if (!process.argv.includes("--validate-only")) writeReports();
