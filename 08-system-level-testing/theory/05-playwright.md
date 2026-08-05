# Playwright

## Why Playwright?

Playwright is a modern browser automation framework with built-in best practices.

## Key Advantages

1. **Auto-waiting**: No manual waits needed
2. **Fast**: Parallel execution built-in
3. **Reliable**: Fewer flaky tests
4. **Multiple browsers**: Chromium, Firefox, WebKit
5. **API interception**: Mock network requests

## Setup

```bash
# Python
pip install playwright pytest-playwright
playwright install

# JavaScript
npm install @playwright/test
npx playwright install
```

## Basic Usage - Python

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")

    page.fill("#username", "admin")
    page.fill("#password", "password")
    page.click("#login")

    assert "Dashboard" in page.title()
    browser.close()
```

## Basic Usage - JavaScript

```javascript
const { test, expect } = require("@playwright/test");

test("login test", async ({ page }) => {
  await page.goto("https://example.com");

  await page.fill("#username", "admin");
  await page.fill("#password", "password");
  await page.click("#login");

  await expect(page).toHaveTitle(/Dashboard/);
});
```

## Auto-Waiting Example

```javascript
// Playwright waits automatically ✅
await page.click("#submit"); // Waits for element to be ready

// Selenium needs explicit waits ❌
WebDriverWait(driver, 10)
  .until(EC.element_to_be_clickable((By.ID, "submit")))
  .click();
```

## API Mocking

```javascript
test("mock API response", async ({ page }) => {
  await page.route("**/api/users", (route) =>
    route.fulfill({
      status: 200,
      body: JSON.stringify([{ name: "Test User" }]),
    }),
  );

  await page.goto("https://example.com");
  // Page uses mocked data
});
```

## Parallel Testing

```bash
# Run tests in parallel
npx playwright test --workers=4
```

## Comparison: Selenium vs Playwright

| Feature          | Selenium   | Playwright |
| ---------------- | ---------- | ---------- |
| Auto-waiting     | ❌         | ✅         |
| Speed            | Moderate   | Fast       |
| API Interception | Limited    | Built-in   |
| Mobile Emulation | Via Appium | Built-in   |
| Learning Curve   | Moderate   | Easy       |
| Cross-browser    | Excellent  | Good       |

## Best Practices

1. Use `test` fixtures for setup
2. Leverage auto-waiting
3. Use strict locators
4. Run tests in parallel
5. Use API routes for mocking

## Next: Complete [homework-8.md](../homework/homework-8.md)
