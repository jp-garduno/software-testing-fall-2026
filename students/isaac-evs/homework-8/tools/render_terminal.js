// Renders captured console output (a text file) to a PNG, for the screenshots/ folder.
// Usage (from homework-8/): node tools/render_terminal.js screenshots/output/x.txt screenshots/x.png "title"
const fs = require("fs");
const { chromium } = require("../playwright/node_modules/@playwright/test");

const escapeHtml = (text) =>
  text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

(async () => {
  const [input, output, title = ""] = process.argv.slice(2);
  const text = escapeHtml(fs.readFileSync(input, "utf8"));
  const html = `<body style="margin:0;background:#1e1e1e;color:#d4d4d4">
    <div style="padding:8px 14px;background:#333;font:13px -apple-system,sans-serif;color:#aaa">${escapeHtml(title)}</div>
    <pre style="margin:0;padding:14px;font:13px/1.4 Menlo,Consolas,monospace;white-space:pre-wrap">${text}</pre></body>`;
  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: 1280, height: 400 },
  });
  await page.setContent(html);
  await page.screenshot({ path: output, fullPage: true });
  await browser.close();
})();
