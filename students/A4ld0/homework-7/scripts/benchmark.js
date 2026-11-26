const { spawnSync } = require("node:child_process");
const { mkdtempSync, writeFileSync, rmSync, rmdirSync } = require("node:fs");
const { tmpdir } = require("node:os");
const { join, resolve } = require("node:path");
const { performance } = require("node:perf_hooks");
const { loadOrders } = require("../tests/testData");

const root = resolve(__dirname, "..");
const directory = mkdtempSync(join(tmpdir(), "homework7-benchmark-"));
const template = `
const { test } = require("node:test");
const Order = require(${JSON.stringify(resolve(root, "src/orderCalculator.js"))});
const { assertTotals } = require(${JSON.stringify(resolve(root, "tests/assertTotals.js"))});

function check(row) {
  const order = new Order(row.items, row.customer_type);
  if (row.discount_code !== "NONE") order.applyDiscount(row.discount_code);
  order.setShipping(row.distance_km, row.is_express);
  assertTotals(order.calculateTotal(), row.expected);
}
`;

function run(file, count) {
  const start = performance.now();
  const result = spawnSync(process.execPath, ["--test", "--test-reporter=spec", file], { encoding: "utf8" });
  if (result.error) throw result.error;
  if (result.status !== 0 || !new RegExp(`ℹ pass ${count}\\b`).test(result.stdout)) {
    throw new Error(result.stdout + result.stderr);
  }
  return performance.now() - start;
}

function median(samples) {
  return [...samples].sort((a, b) => a - b)[Math.floor(samples.length / 2)];
}

try {
  const seeds = loadOrders().slice(0, 10);
  const results = [];
  for (const count of [10, 50, 100, 500]) {
    const rows = Array.from({ length: count }, (_, index) => ({
      ...seeds[index % seeds.length], name: `case_${index + 1}`
    }));
    const traditional = join(directory, "traditional.test.cjs");
    const driven = join(directory, "data-driven.test.cjs");
    writeFileSync(join(directory, "cases.json"), JSON.stringify(rows));
    writeFileSync(traditional, template + rows.map(row =>
      `test("${row.name}", () => check(${JSON.stringify(row)}));`).join("\n"));
    writeFileSync(driven, template + `
const rows = require("./cases.json");
for (const row of rows) test(row.name, () => check(row));
`);
    const samples = { traditional: [], driven: [] };
    for (let repeat = 0; repeat < 5; repeat++) {
      const variants = repeat % 2 === 0 ? [["traditional", traditional], ["driven", driven]] :
        [["driven", driven], ["traditional", traditional]];
      for (const [name, file] of variants) samples[name].push(run(file, count));
    }
    results.push({ count, traditional: median(samples.traditional), driven: median(samples.driven) });
  }

  const max = Math.max(...results.flatMap(({ traditional, driven }) => [traditional, driven]));
  const rows = results.map(({ count, traditional, driven }) => `
<tr><th scope="row">${count}</th>
<td><meter min="0" max="${max}" value="${traditional}"></meter> ${traditional.toFixed(1)} ms</td>
<td><meter min="0" max="${max}" value="${driven}"></meter> ${driven.toFixed(1)} ms</td></tr>`);
  writeFileSync(join(root, "benchmark_results.html"), `<!doctype html>
<html lang="en">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Order suite benchmark</title>
<style>
body { font: 16px system-ui, sans-serif; max-width: 54rem; margin: 3rem auto; padding: 0 1rem; color: #182537; }
table { border-collapse: collapse; width: 100%; }
th, td { text-align: left; padding: .8rem .5rem; border-bottom: 1px solid #d6e0ec; }
meter { width: min(15vw, 9rem); vertical-align: middle; }
</style>
<h1>Order suite execution time</h1>
<p>Median wall time over five runs per variant on Node.js ${process.version}. Every bar uses the same scale.</p>
<table>
<thead><tr><th scope="col">Cases</th><th scope="col">Traditional</th><th scope="col">Data-driven</th></tr></thead>
<tbody>${rows.join("\n")}</tbody>
</table>
</html>
`);
  console.table(results);
} finally {
  for (const file of ["traditional.test.cjs", "data-driven.test.cjs", "cases.json"]) {
    rmSync(join(directory, file), { force: true });
  }
  rmdirSync(directory);
}
