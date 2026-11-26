// Builds the markdown comparison table for PERFORMANCE_REPORT.md from the two result files.
const fs = require("fs");
const path = require("path");

const read = (name) =>
  JSON.parse(fs.readFileSync(path.join(__dirname, name), "utf8"));
const live = read("results-live.json");
const local = read("results-local.json");
const ms = (value) => value.toFixed(1);

const rows = Object.keys(live.summary).map((name) => {
  const a = live.summary[name];
  const b = local.summary[name];
  return `| ${name} | ${ms(a.median)} | ${ms(a.p90)} | ${ms(b.median)} | ${ms(b.p90)} |`;
});
console.log(
  "| Metric (ms) | Live median | Live p90 | Local median | Local p90 |",
);
console.log("| --- | ---: | ---: | ---: | ---: |");
console.log(rows.join("\n"));
