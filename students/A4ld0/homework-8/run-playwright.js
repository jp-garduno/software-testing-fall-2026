const path = require('node:path');
const { spawnSync } = require('node:child_process');

// Execute the real Playwright suite, with optional Node coverage and JSON totals.
const args = process.argv.slice(2);
const coverage = args.includes('--coverage');
const outputIndex = args.findIndex(arg => arg === '--outputFile' || arg.startsWith('--outputFile='));
let outputFile;
if (outputIndex !== -1) {
  const option = args[outputIndex];
  outputFile = option.includes('=') ? option.split('=').slice(1).join('=') : args[outputIndex + 1];
}
const playwrightArgs = [
  require.resolve('@playwright/test/cli'),
  'test', '--config=playwright/playwright.config.js', '--project=chrome', '--workers=1',
];
const command = coverage
  ? [
    require.resolve('c8/bin/c8.js'), '--all', '--include=playwright/pages/**/*.js',
    '--reporter=json-summary', '--reporter=text', process.execPath, ...playwrightArgs,
  ]
  : playwrightArgs;
const env = { ...process.env };
if (args.includes('--json')) {
  env.PLAYWRIGHT_RESULTS_FILE = path.resolve(outputFile || 'js-results.json');
}
const result = spawnSync(process.execPath, command, { stdio: 'inherit', env, cwd: __dirname });
if (result.error) {
  console.error(result.error);
}
process.exitCode = result.status ?? 1;
