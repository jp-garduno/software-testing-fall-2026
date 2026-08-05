# Behavior Driven Development (BDD)

## What is BDD?

**Behavior Driven Development** is a collaborative approach that uses natural language to describe application behavior, bridging the gap between technical and non-technical stakeholders.

## Gherkin Syntax

Gherkin uses a simple, readable syntax:

```gherkin
Feature: User Authentication
  As a registered user
  I want to log into the system
  So that I can access my account

  Scenario: Successful login
    Given I am on the login page
    When I enter valid credentials
    And I click the login button
    Then I should see my dashboard
```

### Keywords

- **Feature**: High-level description
- **Scenario**: Specific test case
- **Given**: Initial context (setup)
- **When**: Action/event
- **Then**: Expected outcome
- **And/But**: Additional steps

## Example: E-Commerce

```gherkin
Feature: Shopping Cart

  Scenario: Add item to cart
    Given I am logged in
    And I am on the product page for "Laptop"
    When I click "Add to Cart"
    Then the cart should contain 1 item
    And the cart total should be "$999.99"

  Scenario Outline: Apply discount codes
    Given I have items worth <subtotal> in my cart
    When I apply discount code "<code>"
    Then my total should be <total>

    Examples:
      | subtotal | code    | total  |
      | 100      | SAVE10  | 90     |
      | 100      | SAVE20  | 80     |
      | 50       | SAVE20  | 50     |
```

## Implementation

### Python (Behave)

**features/login.feature**:

```gherkin
Feature: Login
  Scenario: Valid login
    Given I am on the login page
    When I enter username "admin"
    And I enter password "password123"
    And I click login
    Then I see the dashboard
```

**features/steps/login_steps.py**:

```python
from behave import given, when, then

@given('I am on the login page')
def step_impl(context):
    context.browser.get('http://localhost/login')

@when('I enter username "{username}"')
def step_impl(context, username):
    context.browser.find_element(By.ID, 'username').send_keys(username)

@when('I enter password "{password}"')
def step_impl(context, password):
    context.browser.find_element(By.ID, 'password').send_keys(password)

@when('I click login')
def step_impl(context):
    context.browser.find_element(By.ID, 'login-btn').click()

@then('I see the dashboard')
def step_impl(context):
    assert 'Dashboard' in context.browser.title
```

### JavaScript (Cucumber/Jest)

```javascript
// features/login.feature (same as above)

// features/step_definitions/login.steps.js
const { Given, When, Then } = require("@cucumber/cucumber");

Given("I am on the login page", async function () {
  await this.page.goto("http://localhost/login");
});

When("I enter username {string}", async function (username) {
  await this.page.fill("#username", username);
});

When("I enter password {string}", async function (password) {
  await this.page.fill("#password", password);
});

When("I click login", async function () {
  await this.page.click("#login-btn");
});

Then("I see the dashboard", async function () {
  const title = await this.page.title();
  expect(title).toContain("Dashboard");
});
```

## Best Practices

1. **Keep scenarios focused**: One behavior per scenario
2. **Use domain language**: Avoid technical details
3. **Make steps reusable**: Write generic step definitions
4. **Avoid UI details in steps**: Don't mention buttons/fields
5. **Use Background** for common setup

## Benefits

- ✅ Living documentation
- ✅ Non-technical stakeholders understand
- ✅ Collaboration tool
- ✅ Executable specifications

## Next: [03-selenium-webdriver.md](./03-selenium-webdriver.md)
