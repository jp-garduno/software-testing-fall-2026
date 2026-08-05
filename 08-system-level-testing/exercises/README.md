# Module 8: System Level Testing - Exercises

## Overview

System level testing (E2E testing) is best learned through comprehensive, hands-on practice rather than isolated exercises. This module focuses on:

1. **Theory** - Understanding concepts (5 theory files)
2. **Homework** - Comprehensive practical application (homework-8.md)

## Why No Individual Exercises?

E2E testing requires:

- Complete application setup
- Multiple interconnected test scenarios
- Page Object Model implementation
- Framework comparison (Selenium vs Playwright)

These are better addressed in a **single comprehensive homework** that covers all concepts together rather than fragmented exercises.

## Recommended Learning Path

### 1. Study Theory (Week 14)

Read all theory files in order:

- [01-introduction.md](../theory/01-introduction.md) - System testing fundamentals
- [02-bdd-introduction.md](../theory/02-bdd-introduction.md) - Behavior Driven Development
- [03-selenium-webdriver.md](../theory/03-selenium-webdriver.md) - Selenium basics
- [04-page-object-model.md](../theory/04-page-object-model.md) - POM pattern
- [05-playwright.md](../theory/05-playwright.md) - Modern automation

### 2. Hands-On Practice (Week 15)

Complete [Homework 8](../homework/homework-8.md) which covers:

- ✅ Selenium automation with Page Object Model
- ✅ Playwright automation
- ✅ BDD scenarios with Gherkin
- ✅ Framework comparison
- ✅ Real-world application testing (TodoMVC)

### 3. Practice Sites

Use these sites for additional practice:

- **TodoMVC**: https://todomvc.com/examples/react/ (used in homework)
- **The Internet**: https://the-internet.herokuapp.com/ (various test scenarios)
- **UI Testing Playground**: http://uitestingplayground.com/ (challenging scenarios)
- **DemoQA**: https://demoqa.com/ (forms, tables, alerts)

### 4. Quick Experiments

Before starting homework, try quick experiments:

**Selenium Quick Test**:

```python
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://todomvc.com/examples/react/")
# Experiment with finding elements, clicking, typing
driver.quit()
```

**Playwright Quick Test**:

```javascript
const { chromium } = require("playwright");

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto("https://todomvc.com/examples/react/");
  // Experiment with Playwright commands
  await browser.close();
})();
```

## Homework Integration

The homework covers everything you need:

- Part 1: Selenium with Page Object Model (40 pts)
- Part 2: Playwright implementation (40 pts)
- Part 3: BDD Scenarios with Gherkin (10 pts)
- Part 4: Comparison Analysis (10 pts)
- Bonus: Advanced features (10 pts)

## Completion Checklist

- [ ] Read all 5 theory files
- [ ] Experiment with test sites
- [ ] Complete Homework 8
- [ ] Compare Selenium vs Playwright
- [ ] Understand Page Object Model

## Next Steps

1. Start with [Homework 8](../homework/homework-8.md)
2. Apply E2E tests to Team Project (Milestone 6)
3. Prepare for [Module 9: Performance Testing](../../09-performance-testing/README.md)
