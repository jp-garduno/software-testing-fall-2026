# Milestone 6: System Testing

**Due**: End of Week 14  
**Points**: 15 (15% of project grade)  
**Focus**: End-to-end test automation with BDD and Selenium/Playwright  
**Module Applied**: System Level Testing (Module 8)

---

## 🎯 Objectives

- Write BDD scenarios in Gherkin
- Implement E2E tests with Selenium or Playwright
- Use Page Object Model pattern
- Automate 5+ complete user workflows
- Generate E2E test reports

---

## 📋 Deliverables

### 1. BDD Feature Files (25 points)

#### 1.1 Feature File Structure

Create at least **5 feature files** in Gherkin:

**File**: `tests/e2e/features/user-authentication.feature`

```gherkin
Feature: User Authentication
  As a user
  I want to register and login to the application
  So that I can access my personalized content

  Background:
    Given the application is running
    And I am on the homepage

  Scenario: Successful user registration
    Given I am on the registration page
    When I enter "newuser@example.com" in the email field
    And I enter "ValidPass123!" in the password field
    And I enter "ValidPass123!" in the confirm password field
    And I click the "Register" button
    Then I should see a success message "Registration successful"
    And I should be redirected to the dashboard
    And I should see "Welcome, newuser@example.com"

  Scenario: Registration with existing email
    Given a user exists with email "existing@example.com"
    And I am on the registration page
    When I enter "existing@example.com" in the email field
    And I enter "ValidPass123!" in the password field
    And I enter "ValidPass123!" in the confirm password field
    And I click the "Register" button
    Then I should see an error "Email already registered"
    And I should remain on the registration page

  Scenario Outline: Registration with invalid data
    Given I am on the registration page
    When I enter "<email>" in the email field
    And I enter "<password>" in the password field
    And I enter "<confirm_password>" in the confirm password field
    And I click the "Register" button
    Then I should see an error "<error_message>"

    Examples:
      | email               | password       | confirm_password | error_message              |
      | invalid-email       | ValidPass123!  | ValidPass123!    | Invalid email format       |
      | user@example.com    | short          | short            | Password too short         |
      | user@example.com    | ValidPass123!  | DifferentPass1!  | Passwords do not match     |
      |                     | ValidPass123!  | ValidPass123!    | Email is required          |

  Scenario: Successful login
    Given a user exists with email "user@example.com" and password "ValidPass123!"
    And I am on the login page
    When I enter "user@example.com" in the email field
    And I enter "ValidPass123!" in the password field
    And I click the "Login" button
    Then I should be redirected to the dashboard
    And I should see "Welcome back"

  Scenario: Login with incorrect password
    Given a user exists with email "user@example.com"
    And I am on the login page
    When I enter "user@example.com" in the email field
    And I enter "WrongPassword123!" in the password field
    And I click the "Login" button
    Then I should see an error "Invalid credentials"
    And I should remain on the login page
```

#### 1.2 Required Feature Files

Create feature files for these user workflows:

1. **user-authentication.feature** (registration, login, logout)
2. **<core-feature-1>.feature** (e.g., product-browsing.feature)
3. **<core-feature-2>.feature** (e.g., shopping-cart.feature)
4. **<core-feature-3>.feature** (e.g., checkout-process.feature)
5. **<core-feature-4>.feature** (e.g., order-management.feature)

**Minimum**: 5 feature files with 15+ scenarios total

---

### 2. Page Object Model Implementation (30 points)

#### 2.1 Page Object Structure

Create page objects for all pages:

**Python (Selenium)**: `tests/e2e/pages/login_page.py`

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """Page Object for Login Page"""

    # Locators
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def navigate(self):
        """Navigate to login page"""
        self.driver.get("http://localhost:3000/login")
        return self

    def enter_email(self, email):
        """Enter email in email field"""
        email_input = self.wait.until(
            EC.visibility_of_element_located(self.EMAIL_INPUT)
        )
        email_input.clear()
        email_input.send_keys(email)
        return self

    def enter_password(self, password):
        """Enter password in password field"""
        password_input = self.driver.find_element(*self.PASSWORD_INPUT)
        password_input.clear()
        password_input.send_keys(password)
        return self

    def click_login(self):
        """Click login button"""
        login_btn = self.driver.find_element(*self.LOGIN_BUTTON)
        login_btn.click()
        return self

    def get_error_message(self):
        """Get error message text"""
        error = self.wait.until(
            EC.visibility_of_element_located(self.ERROR_MESSAGE)
        )
        return error.text

    def login(self, email, password):
        """Complete login flow"""
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
        return self
```

**JavaScript (Playwright)**: `tests/e2e/pages/LoginPage.js`

```javascript
class LoginPage {
  constructor(page) {
    this.page = page;

    // Locators
    this.emailInput = page.locator("#email");
    this.passwordInput = page.locator("#password");
    this.loginButton = page.locator('button[type="submit"]');
    this.errorMessage = page.locator(".error-message");
  }

  async navigate() {
    await this.page.goto("http://localhost:3000/login");
  }

  async enterEmail(email) {
    await this.emailInput.clear();
    await this.emailInput.fill(email);
  }

  async enterPassword(password) {
    await this.passwordInput.clear();
    await this.passwordInput.fill(password);
  }

  async clickLogin() {
    await this.loginButton.click();
  }

  async getErrorMessage() {
    return await this.errorMessage.textContent();
  }

  async login(email, password) {
    await this.enterEmail(email);
    await this.enterPassword(password);
    await this.clickLogin();
  }
}

module.exports = LoginPage;
```

#### 2.2 Required Page Objects

Create page objects for all pages:

- `LoginPage` - Login functionality
- `RegisterPage` - Registration functionality
- `DashboardPage` - Main dashboard
- `<Feature>Page` - For each major feature (e.g., ProductPage, CartPage, CheckoutPage)
- `BasePage` - Common functionality

**Minimum**: 5 page objects

---

### 3. Step Definitions (25 points)

#### 3.1 Implement Step Definitions

**Python (Behave)**: `tests/e2e/steps/auth_steps.py`

```python
from behave import given, when, then
from tests.e2e.pages.login_page import LoginPage
from tests.e2e.pages.register_page import RegisterPage
from tests.e2e.pages.dashboard_page import DashboardPage

@given('I am on the login page')
def step_navigate_to_login(context):
    context.login_page = LoginPage(context.driver)
    context.login_page.navigate()

@when('I enter "{text}" in the email field')
def step_enter_email(context, text):
    context.login_page.enter_email(text)

@when('I enter "{text}" in the password field')
def step_enter_password(context, text):
    context.login_page.enter_password(text)

@when('I click the "Login" button')
def step_click_login(context):
    context.login_page.click_login()

@then('I should be redirected to the dashboard')
def step_verify_dashboard_redirect(context):
    context.dashboard_page = DashboardPage(context.driver)
    assert context.driver.current_url.endswith('/dashboard')

@then('I should see an error "{error_text}"')
def step_verify_error_message(context, error_text):
    actual_error = context.login_page.get_error_message()
    assert error_text in actual_error, \
        f"Expected '{error_text}' in error message, got '{actual_error}'"

@given('a user exists with email "{email}" and password "{password}"')
def step_create_test_user(context, email, password):
    # Create test user in database or via API
    from tests.utils.test_data import create_user
    context.test_user = create_user(email, password)
```

**JavaScript (Cucumber)**: `tests/e2e/steps/auth.steps.js`

```javascript
const { Given, When, Then } = require("@cucumber/cucumber");
const { expect } = require("@playwright/test");
const LoginPage = require("../pages/LoginPage");
const DashboardPage = require("../pages/DashboardPage");

Given("I am on the login page", async function () {
  this.loginPage = new LoginPage(this.page);
  await this.loginPage.navigate();
});

When("I enter {string} in the email field", async function (email) {
  await this.loginPage.enterEmail(email);
});

When("I enter {string} in the password field", async function (password) {
  await this.loginPage.enterPassword(password);
});

When("I click the {string} button", async function (buttonText) {
  if (buttonText === "Login") {
    await this.loginPage.clickLogin();
  }
});

Then("I should be redirected to the dashboard", async function () {
  this.dashboardPage = new DashboardPage(this.page);
  expect(this.page.url()).toContain("/dashboard");
});

Then("I should see an error {string}", async function (errorText) {
  const actualError = await this.loginPage.getErrorMessage();
  expect(actualError).toContain(errorText);
});

Given(
  "a user exists with email {string} and password {string}",
  async function (email, password) {
    // Create test user via API
    const { createUser } = require("../utils/testData");
    this.testUser = await createUser(email, password);
  },
);
```

---

### 4. E2E Test Execution (15 points)

#### 4.1 Test Configuration

**Python (Behave)**: `tests/e2e/environment.py`

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def before_all(context):
    """Set up before all tests"""
    context.base_url = "http://localhost:3000"

def before_scenario(context, scenario):
    """Set up before each scenario"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    context.driver = webdriver.Chrome(options=options)
    context.driver.implicitly_wait(10)
    context.driver.maximize_window()

def after_scenario(context, scenario):
    """Clean up after each scenario"""
    if scenario.status == 'failed':
        # Take screenshot on failure
        screenshot_path = f"screenshots/{scenario.name}.png"
        context.driver.save_screenshot(screenshot_path)

    context.driver.quit()
```

**JavaScript (Playwright)**: `tests/e2e/support/hooks.js`

```javascript
const { Before, After, BeforeAll, AfterAll } = require("@cucumber/cucumber");
const { chromium } = require("@playwright/test");

BeforeAll(async function () {
  global.browser = await chromium.launch({
    headless: true,
  });
});

Before(async function () {
  this.context = await global.browser.newContext();
  this.page = await this.context.newPage();
});

After(async function (scenario) {
  if (scenario.result.status === "FAILED") {
    const screenshot = await this.page.screenshot();
    this.attach(screenshot, "image/png");
  }

  await this.page.close();
  await this.context.close();
});

AfterAll(async function () {
  await global.browser.close();
});
```

#### 4.2 Run Tests

```bash
# Python
behave tests/e2e/features/ --format pretty --format html --outfile reports/e2e-report.html

# JavaScript
npm run test:e2e -- --format html:reports/e2e-report.html
```

---

### 5. Test Report (5 points)

Create `docs/milestones/M6/e2e-test-report.md`:

```markdown
# E2E Test Report

## Test Execution Summary

**Date**: 2026-XX-XX
**Environment**: Chrome (headless)
**Application URL**: http://localhost:3000

## Results

| Feature             | Scenarios | Passed | Failed | Skipped | Duration |
| ------------------- | --------- | ------ | ------ | ------- | -------- |
| User Authentication | 5         | 5      | 0      | 0       | 45s      |
| Product Browsing    | 3         | 3      | 0      | 0       | 30s      |
| Shopping Cart       | 4         | 4      | 0      | 0       | 50s      |
| Checkout Process    | 3         | 2      | 1      | 0       | 40s      |
| Order Management    | 2         | 2      | 0      | 0       | 25s      |
| **TOTAL**           | **17**    | **16** | **1**  | **0**   | **190s** |

## Failed Scenarios

### Checkout Process - Payment with invalid card

**Error**: Timeout waiting for payment confirmation
**Screenshot**: [checkout-payment-fail.png]
**Status**: Bug reported (#45)

## Coverage

- 5 complete user workflows tested
- 17 scenarios covering happy and unhappy paths
- All critical user journeys automated

## Issues Found

1. **BUG-10**: Payment confirmation timeout (HIGH)
2. **BUG-11**: Cart total not updating after discount (MEDIUM)
3. **BUG-12**: Order history pagination issue (LOW)

## Next Steps

1. Fix payment confirmation bug
2. Re-run failed scenarios
3. Add more edge case scenarios
4. Integrate E2E tests into CI/CD
```

Include screenshots from test execution.

---

## 📤 Submission Instructions

### Required Files

```
tests/e2e/
├── features/
│   ├── user-authentication.feature
│   ├── product-browsing.feature
│   ├── shopping-cart.feature
│   ├── checkout.feature
│   └── order-management.feature
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   ├── register_page.py
│   ├── dashboard_page.py
│   └── ...
├── steps/
│   ├── auth_steps.py
│   ├── product_steps.py
│   └── ...
├── utils/
│   └── test_data.py
├── environment.py (Python) or hooks.js (JS)
└── behave.ini / cucumber.js

docs/milestones/M6/
├── e2e-test-report.md
├── bdd-scenarios.md
└── screenshots/
```

### Submit on Canvas

- Pull Request URL
- E2E test report link
- HTML test report (attach or link)

---

## 🎯 Grading Rubric

| Category               | Points | Criteria                                  |
| ---------------------- | ------ | ----------------------------------------- |
| **BDD Feature Files**  | 25     | 5+ features, 15+ scenarios, clear Gherkin |
| **Page Object Model**  | 30     | 5+ page objects, good abstraction         |
| **Step Definitions**   | 25     | All steps implemented, reusable           |
| **E2E Test Execution** | 15     | Tests run successfully, reports generated |
| **Test Report**        | 5      | Clear documentation, screenshots          |
| **Quality**            | 10     | Clean code, good practices                |

**Total**: 110 points (10% bonus available)

**Requirements**:

- 5 feature files (REQUIRED)
- 15+ scenarios (REQUIRED)
- 5 page objects (REQUIRED)
- All tests must run in CI (REQUIRED)

---

## ✅ Checklist

- [ ] 5 feature files written in Gherkin
- [ ] 15+ scenarios covering user workflows
- [ ] Page Object Model implemented
- [ ] 5+ page objects created
- [ ] All step definitions implemented
- [ ] Tests run successfully locally
- [ ] Test report generated
- [ ] Screenshots of test execution
- [ ] E2E tests integrated into CI/CD
- [ ] All scenarios documented
- [ ] PR created and submitted

---

**E2E tests validate the entire system from a user's perspective. Make them count!** 🌐✅
