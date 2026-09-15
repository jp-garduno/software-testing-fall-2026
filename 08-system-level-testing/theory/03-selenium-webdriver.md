# Selenium WebDriver

## Overview

Selenium WebDriver is a browser automation tool for E2E testing across multiple browsers.

## Setup

### Python

```bash
pip install selenium
# Download ChromeDriver or GeckoDriver
```

### JavaScript

```bash
npm install selenium-webdriver
```

## Basic Usage

### Python

```python
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://example.com")

# Locate elements
element = driver.find_element(By.ID, "username")
element.send_keys("admin")

# Click
driver.find_element(By.ID, "submit").click()

# Assert
assert "Dashboard" in driver.title

driver.quit()
```

### JavaScript

```javascript
const { Builder, By } = require("selenium-webdriver");

(async function () {
  let driver = await new Builder().forBrowser("chrome").build();

  await driver.get("https://example.com");

  await driver.findElement(By.id("username")).sendKeys("admin");
  await driver.findElement(By.id("submit")).click();

  let title = await driver.getTitle();
  console.assert(title.includes("Dashboard"));

  await driver.quit();
})();
```

## Locator Strategies

```python
# By ID (best)
driver.find_element(By.ID, "username")

# By Name
driver.find_element(By.NAME, "email")

# By Class
driver.find_element(By.CLASS_NAME, "btn-primary")

# By CSS Selector
driver.find_element(By.CSS_SELECTOR, ".form-control")

# By XPath (last resort)
driver.find_element(By.XPATH, "//input[@type='submit']")

# By Link Text
driver.find_element(By.LINK_TEXT, "Click Here")
```

## Waits

### Explicit Waits (Recommended)

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
element = wait.until(
    EC.presence_of_element_located((By.ID, "result"))
)
```

### Implicit Waits

```python
driver.implicitly_wait(10)  # seconds
```

## Common Operations

```python
# Click
element.click()

# Type
element.send_keys("text")

# Clear
element.clear()

# Get text
text = element.text

# Get attribute
value = element.get_attribute("value")

# Is displayed
visible = element.is_displayed()

# Screenshots
driver.save_screenshot("screenshot.png")

# Navigate
driver.back()
driver.forward()
driver.refresh()

# Alerts
alert = driver.switch_to.alert
alert.accept()  # or alert.dismiss()
```

## Best Practices

1. Use explicit waits
2. Close browser after tests
3. Use test IDs for locators
4. Implement Page Object Model
5. Run headless in CI

## Next: [04-page-object-model.md](./04-page-object-model.md)
