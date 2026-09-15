# Page Object Model (POM)

## What is POM?

Page Object Model is a design pattern that creates an object repository for web elements, separating test logic from page structure.

## Without POM (Bad)

```python
def test_login():
    driver.find_element(By.ID, "username").send_keys("admin")
    driver.find_element(By.ID, "password").send_keys("pass")
    driver.find_element(By.ID, "submit").click()
    assert "Dashboard" in driver.title

# If UI changes, update ALL tests
```

## With POM (Good)

```python
class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def login(self, username, password):
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "submit").click()

def test_login():
    login_page = LoginPage(driver)
    login_page.login("admin", "pass")
    assert "Dashboard" in driver.title

# If UI changes, update only LoginPage
```

## Full Example - Python

```python
from selenium.webdriver.common.by import By

class LoginPage:
    # Locators
    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-btn")
    ERROR_MSG = (By.CLASS_NAME, "error")

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get("https://example.com/login")

    def login(self, username, password):
        self.driver.find_element(*self.USERNAME).send_keys(username)
        self.driver.find_element(*self.PASSWORD).send_keys(password)
        self.driver.find_element(*self.LOGIN_BTN).click()

    def get_error_message(self):
        return self.driver.find_element(*self.ERROR_MSG).text

# Test
def test_invalid_login():
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login("wrong", "credentials")
    assert "Invalid" in login_page.get_error_message()
```

## Full Example - JavaScript

```javascript
class LoginPage {
  constructor(page) {
    this.page = page;
    this.usernameInput = "#username";
    this.passwordInput = "#password";
    this.loginButton = "#login-btn";
    this.errorMessage = ".error";
  }

  async open() {
    await this.page.goto("https://example.com/login");
  }

  async login(username, password) {
    await this.page.fill(this.usernameInput, username);
    await this.page.fill(this.passwordInput, password);
    await this.page.click(this.loginButton);
  }

  async getErrorMessage() {
    return await this.page.textContent(this.errorMessage);
  }
}

// Test
test("invalid login shows error", async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.open();
  await loginPage.login("wrong", "credentials");
  expect(await loginPage.getErrorMessage()).toContain("Invalid");
});
```

## Benefits

- ✅ DRY: Write locators once
- ✅ Maintainability: Change in one place
- ✅ Readability: Tests read like user actions
- ✅ Reusability: Share pages across tests

## Best Practices

1. One class per page
2. Store locators as constants
3. Methods return other page objects (page chaining)
4. Keep assertions in tests, not pages
5. Use descriptive method names

## Next: [05-playwright.md](./05-playwright.md)
