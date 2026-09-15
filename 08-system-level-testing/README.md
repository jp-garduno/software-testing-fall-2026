# Module 8: System Level Testing

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Understand system-level and end-to-end testing
- Write BDD scenarios using Gherkin syntax
- Automate web testing with Selenium WebDriver
- Use Playwright for modern E2E testing
- Implement Page Object Model pattern
- Integrate E2E tests into CI/CD pipelines

## 📚 Module Contents

This module is divided into three key areas:

### 8.1 Behavior Driven Development (BDD)

- Gherkin syntax (Given-When-Then)
- Feature files and step definitions
- Behave (Python) and Cucumber/Jest (JavaScript)
- Collaboration between technical and non-technical stakeholders

### 8.2 Selenium WebDriver

- Browser automation fundamentals
- Locator strategies (ID, class, XPath, CSS)
- Interacting with web elements
- Handling waits and synchronization
- Page Object Model design pattern

### 8.3 Playwright

- Modern browser automation
- Cross-browser testing (Chromium, Firefox, WebKit)
- Auto-waiting and reliability
- Network interception and mocking
- Visual comparisons and screenshots

## 📚 Theory Materials

### [1. Introduction to System Testing](./theory/01-introduction.md)

- System testing vs integration testing
- End-to-end testing importance
- Types of system tests
- The test automation pyramid

### [2. Behavior Driven Development](./theory/02-bdd-introduction.md)

- BDD philosophy and benefits
- Gherkin syntax guide
- Writing effective scenarios
- Living documentation

### [3. Selenium WebDriver](./theory/03-selenium-webdriver.md)

- WebDriver architecture
- Setting up Selenium
- Locator strategies
- WebDriver commands
- Best practices

### [4. Page Object Model](./theory/04-page-object-model.md)

- Design pattern for test maintenance
- Separation of concerns
- Implementing POM
- Examples in Python and JavaScript

### [5. Playwright](./theory/05-playwright.md)

- Why Playwright
- Key features and advantages
- Setting up Playwright
- Playwright vs Selenium
- Modern testing patterns

## 🛠️ Setup Instructions

### Python - Selenium

```bash
pip install selenium behave
```

Download WebDriver:

- ChromeDriver: https://chromedriver.chromium.org/
- GeckoDriver (Firefox): https://github.com/mozilla/geckodriver/

### Python - Playwright

```bash
pip install playwright pytest-playwright
playwright install
```

### JavaScript - Selenium

```bash
npm install --save-dev selenium-webdriver
```

### JavaScript - Playwright

```bash
npm install --save-dev @playwright/test
npx playwright install
```

## 💻 Practical Exercises

**Note**: This module uses an integrated approach. Instead of separate exercises, all concepts are covered in the comprehensive homework assignment.

See [exercises/README.md](./exercises/README.md) for:

- Theory study guide
- Practice sites for experimentation
- Quick code examples for Selenium and Playwright
- Integrated homework approach explanation

**Why no separate exercises?** E2E testing requires complete application setup and interconnected scenarios. The homework provides hands-on practice with:

- Selenium automation with Page Object Model
- Playwright automation
- BDD scenarios with Gherkin
- Framework comparison
- Real-world application (TodoMVC)

## 📝 Homework Assignment

**[Homework 8: End-to-End Test Automation](./homework/homework-8.md)**

**Due**: End of Week 15

**Objectives**:

- Automate test scenarios for a web application
- Implement Page Object Model
- Use both Selenium and Playwright
- Write BDD feature files
- Compare both tools

## 🎥 Video Resources

- **BDD Introduction** (20 min)
- **Selenium Basics** (30 min)
- **Page Object Model Pattern** (25 min)
- **Playwright Deep Dive** (35 min)
- **E2E Best Practices** (20 min)

## 📖 Gherkin Syntax Quick Reference

```gherkin
Feature: User Login
  As a registered user
  I want to log into the application
  So that I can access my dashboard

  Background:
    Given I am on the login page

  Scenario: Successful login
    Given I have valid credentials
    When I enter my username "user@example.com"
    And I enter my password "SecurePass123"
    And I click the login button
    Then I should see the dashboard
    And I should see a welcome message "Welcome back!"

  Scenario Outline: Failed login attempts
    When I enter username "<username>"
    And I enter password "<password>"
    And I click the login button
    Then I should see error "<error_message>"

    Examples:
      | username          | password      | error_message           |
      | invalid@email.com | wrong123      | Invalid credentials     |
      | user@example.com  | wrongpass     | Invalid credentials     |
      |                   | password123   | Username required       |
      | user@example.com  |               | Password required       |
```

## 🔄 Selenium vs Playwright Comparison

| **Feature**          | **Selenium**                      | **Playwright**                 |
| -------------------- | --------------------------------- | ------------------------------ |
| **Browsers**         | Chrome, Firefox, Safari, Edge     | Chromium, Firefox, WebKit      |
| **Language Support** | Many (Python, Java, C#, JS, etc.) | Python, JavaScript, .NET, Java |
| **Auto-waiting**     | Manual waits needed               | Built-in auto-waiting          |
| **Speed**            | Moderate                          | Faster                         |
| **API Interception** | Limited                           | Built-in support               |
| **Maturity**         | Very mature                       | Newer but rapidly evolving     |
| **Learning Curve**   | Moderate                          | Easier for modern patterns     |
| **Mobile Testing**   | Appium integration                | Mobile web supported           |
| **Community**        | Large, established                | Growing rapidly                |

## 📖 Page Object Model Example

### Python (Selenium):

```python
class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.ID, "username")
        self.password_input = (By.ID, "password")
        self.login_button = (By.ID, "login-btn")

    def login(self, username, password):
        self.driver.find_element(*self.username_input).send_keys(username)
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.login_button).click()
```

### JavaScript (Playwright):

```javascript
class LoginPage {
  constructor(page) {
    this.page = page;
    this.usernameInput = page.locator("#username");
    this.passwordInput = page.locator("#password");
    this.loginButton = page.locator("#login-btn");
  }

  async login(username, password) {
    await this.usernameInput.fill(username);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }
}
```

## 🎯 Self-Assessment Checklist

- [ ] Write Gherkin feature files
- [ ] Implement step definitions for BDD
- [ ] Set up Selenium WebDriver
- [ ] Locate elements using various strategies
- [ ] Implement Page Object Model
- [ ] Set up Playwright
- [ ] Write Playwright tests
- [ ] Compare Selenium and Playwright
- [ ] Integrate E2E tests in CI/CD

## 🚀 Next Steps

- Complete all exercises for both Selenium and Playwright
- Complete [Homework 8](./homework/homework-8.md)
- Work on Team Project Milestone 6 (E2E Tests)
- Preview [Module 9: Performance Testing](../09-performance-testing/README.md)
- Prepare for **Exam 3** (Week 16)

---

**Remember**: System tests are slow and brittle. Follow the testing pyramid - fewer E2E tests, more unit tests! 🎯
