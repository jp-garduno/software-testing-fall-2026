# Homework 8: End-to-End Test Automation

**Due**: End of Week 15  
**Points**: 110 (100 base + 10 bonus)

## Overview

Automate end-to-end tests for a task management web application using both Selenium and Playwright. Implement Page Object Model, BDD scenarios, and compare both frameworks.

## Application Under Test

**Task Manager App** - Use https://todomvc.com/examples/react/

Features to test:

- Create/edit/delete tasks
- Mark tasks as complete/incomplete
- Filter tasks (all/active/completed)
- Clear completed tasks

## Part 1: Selenium Tests (40 points)

### Test Scenarios

Implement these test cases using Selenium + Page Object Model:

1. **Task Creation** (8 points)

   - Create single task
   - Create multiple tasks
   - Task appears in list

2. **Task Completion** (8 points)

   - Mark task as complete
   - Unmark completed task
   - Complete multiple tasks

3. **Task Deletion** (8 points)

   - Delete single task
   - Delete completed task
   - Clear all completed

4. **Task Filtering** (8 points)

   - View all tasks
   - View active tasks only
   - View completed tasks only

5. **Task Editing** (8 points)
   - Edit task text
   - Cancel edit
   - Save edited task

### Page Object Example

```python
# pages/todo_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TodoPage:
    # Locators
    NEW_TODO_INPUT = (By.CLASS_NAME, "new-todo")
    TODO_LIST = (By.CLASS_NAME, "todo-list")
    TODO_ITEMS = (By.CSS_SELECTOR, ".todo-list li")
    TOGGLE_ALL = (By.CLASS_NAME, "toggle-all")
    CLEAR_COMPLETED = (By.CLASS_NAME, "clear-completed")
    FILTER_ALL = (By.CSS_SELECTOR, "a[href='#/']")
    FILTER_ACTIVE = (By.CSS_SELECTOR, "a[href='#/active']")
    FILTER_COMPLETED = (By.CSS_SELECTOR, "a[href='#/completed']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def navigate(self):
        self.driver.get("https://todomvc.com/examples/react/")

    def add_todo(self, text):
        """Add a new todo item"""
        # TODO: Implement
        pass

    def get_todo_count(self):
        """Return number of todo items"""
        # TODO: Implement
        pass

    def toggle_todo(self, index):
        """Toggle todo completion status"""
        # TODO: Implement
        pass

    def delete_todo(self, index):
        """Delete a todo item"""
        # TODO: Implement
        pass

    def filter_active(self):
        """Show only active todos"""
        # TODO: Implement
        pass

    def filter_completed(self):
        """Show only completed todos"""
        # TODO: Implement
        pass

    def get_visible_todos(self):
        """Get list of visible todo texts"""
        # TODO: Implement
        pass
```

## Part 2: Playwright Tests (40 points)

### Requirements

Implement the same test scenarios using Playwright.

**Example - JavaScript**:

```javascript
// pages/TodoPage.js
class TodoPage {
  constructor(page) {
    this.page = page;
    this.newTodoInput = ".new-todo";
    this.todoList = ".todo-list";
    this.todoItems = ".todo-list li";
  }

  async navigate() {
    await this.page.goto("https://todomvc.com/examples/react/");
  }

  async addTodo(text) {
    await this.page.fill(this.newTodoInput, text);
    await this.page.press(this.newTodoInput, "Enter");
  }

  async getTodoCount() {
    return await this.page.locator(this.todoItems).count();
  }

  async toggleTodo(index) {
    await this.page
      .locator(this.todoItems)
      .nth(index)
      .locator(".toggle")
      .click();
  }

  async deleteTodo(index) {
    const todo = this.page.locator(this.todoItems).nth(index);
    await todo.hover();
    await todo.locator(".destroy").click();
  }

  async filterActive() {
    await this.page.click("text=Active");
  }

  async getVisibleTodos() {
    const todos = await this.page.locator(this.todoItems).allTextContents();
    return todos;
  }
}

module.exports = { TodoPage };
```

**Example Test**:

```javascript
const { test, expect } = require("@playwright/test");
const { TodoPage } = require("../pages/TodoPage");

test.describe("Todo Management", () => {
  let todoPage;

  test.beforeEach(async ({ page }) => {
    todoPage = new TodoPage(page);
    await todoPage.navigate();
  });

  test("add new todo", async () => {
    await todoPage.addTodo("Buy milk");
    expect(await todoPage.getTodoCount()).toBe(1);
    expect(await todoPage.getVisibleTodos()).toContain("Buy milk");
  });

  test("complete todo", async () => {
    await todoPage.addTodo("Test task");
    await todoPage.toggleTodo(0);
    // Verify todo is marked as completed
  });

  test("delete todo", async () => {
    await todoPage.addTodo("Task to delete");
    await todoPage.deleteTodo(0);
    expect(await todoPage.getTodoCount()).toBe(0);
  });

  test("filter active todos", async () => {
    await todoPage.addTodo("Active task");
    await todoPage.addTodo("Completed task");
    await todoPage.toggleTodo(1);
    await todoPage.filterActive();
    const todos = await todoPage.getVisibleTodos();
    expect(todos).toHaveLength(1);
    expect(todos[0]).toContain("Active task");
  });
});
```

## Part 3: BDD Scenarios (10 points)

### Feature File

**features/todo.feature**:

```gherkin
Feature: Todo Management
  As a user
  I want to manage my todo list
  So that I can track my tasks

  Background:
    Given I am on the todo page

  Scenario: Add a new todo
    When I add a todo "Buy groceries"
    Then I should see 1 todo
    And the todo should be "Buy groceries"

  Scenario: Complete a todo
    Given I have a todo "Read book"
    When I mark the todo as complete
    Then the todo should be marked as done
    And the active count should be 0

  Scenario: Delete a todo
    Given I have a todo "Old task"
    When I delete the todo
    Then I should see 0 todos

  Scenario Outline: Filter todos
    Given I have the following todos:
      | text      | completed |
      | Task 1    | false     |
      | Task 2    | true      |
      | Task 3    | false     |
    When I filter by "<filter>"
    Then I should see <count> todo(s)

    Examples:
      | filter     | count |
      | All        | 3     |
      | Active     | 2     |
      | Completed  | 1     |
```

### Step Definitions (Python - Behave)

```python
# features/steps/todo_steps.py
from behave import given, when, then
from pages.todo_page import TodoPage

@given('I am on the todo page')
def step_impl(context):
    context.todo_page = TodoPage(context.driver)
    context.todo_page.navigate()

@when('I add a todo "{text}"')
def step_impl(context, text):
    context.todo_page.add_todo(text)

@then('I should see {count:d} todo')
def step_impl(context, count):
    actual_count = context.todo_page.get_todo_count()
    assert actual_count == count, f"Expected {count}, got {actual_count}"

@given('I have a todo "{text}"')
def step_impl(context, text):
    context.todo_page.add_todo(text)
```

## Part 4: Comparison Report (10 points)

Create **COMPARISON_REPORT.md** with:

### 1. Execution Time Comparison

Run both test suites and compare:

| Metric               | Selenium | Playwright |
| -------------------- | -------- | ---------- |
| Total execution time |          |            |
| Average per test     |          |            |
| Setup time           |          |            |

### 2. Code Comparison

Compare LOC and complexity for equivalent functionality.

### 3. Developer Experience

| Aspect                | Selenium | Playwright | Notes |
| --------------------- | -------- | ---------- | ----- |
| Setup difficulty      |          |            |       |
| Auto-waiting          |          |            |       |
| Debugging             |          |            |       |
| Documentation quality |          |            |       |
| Error messages        |          |            |       |
| IDE support           |          |            |       |

### 4. Recommendations

- When would you choose Selenium?
- When would you choose Playwright?
- What did you learn?

## Bonus Options (+10 points total)

Choose ANY TWO:

### A. Visual Regression (+5 points)

- Take screenshots at key points
- Compare screenshots across runs
- Report visual differences

### B. Cross-Browser Testing (+5 points)

- Run Playwright tests on Chrome, Firefox, WebKit
- Document browser differences
- Create compatibility matrix

### C. Performance Metrics (+5 points)

- Measure page load times
- Track operation execution times
- Generate performance report

### D. CI/CD Pipeline (+5 points)

- GitHub Actions workflow
- Run tests on push
- Publish test reports as artifacts

## Deliverables

```
homework-8/
├── selenium/
│   ├── pages/
│   │   └── todo_page.py
│   ├── tests/
│   │   ├── test_todo_crud.py
│   │   └── test_todo_filter.py
│   └── requirements.txt
├── playwright/
│   ├── pages/
│   │   └── TodoPage.js
│   ├── tests/
│   │   ├── todo-crud.spec.js
│   │   └── todo-filter.spec.js
│   └── package.json
├── features/
│   ├── todo.feature
│   └── steps/
│       └── todo_steps.py
├── COMPARISON_REPORT.md
├── README.md
└── screenshots/
    └── (test execution screenshots)
```

## Grading Rubric

- **Selenium Tests** (40%): Implementation, POM, coverage
- **Playwright Tests** (40%): Implementation, POM, coverage
- **BDD Scenarios** (10%): Feature file + step definitions
- **Comparison Report** (10%): Analysis and insights
- **Bonus** (10%): Advanced features

## Tips

1. Use explicit waits in Selenium
2. Leverage Playwright's auto-waiting
3. Make tests independent
4. Use descriptive test names
5. Handle edge cases
6. Clean up test data
7. Run tests in parallel (Playwright)

## Resources

- [TodoMVC React](https://todomvc.com/examples/react/)
- [Selenium Docs](https://www.selenium.dev/documentation/)
- [Playwright Docs](https://playwright.dev/)
- [Behave Docs](https://behave.readthedocs.io/)

## Submission

1. Create branch: `homework-8-solution`
2. Commit frequently with conventional commits
3. Create PR with test results
4. Include README with run instructions

Good luck! 🚀
