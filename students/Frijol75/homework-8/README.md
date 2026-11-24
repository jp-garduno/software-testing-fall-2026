# Homework 8: End-to-End Test Automation (Selenium, Playwright & BDD)

**Student**: Frijol75  
**Course**: Software Testing - Fall 2026  
**Application Under Test**: [TodoMVC React](https://todomvc.com/examples/react/dist/)

---

## 📋 Overview

This project provides a complete **System-Level / End-to-End (E2E)** test automation suite for the **TodoMVC React** application using two industry-standard automation frameworks (**Selenium WebDriver** and **Playwright**) alongside **Behavior-Driven Development (BDD)** with **Gherkin / Behave** and the **Page Object Model (POM)** design pattern.

### What Is Included
1. **Part 1 — Selenium E2E Suite (40 pts)**:
   - Page Object Model: [`selenium/pages/todo_page.py`](./selenium/pages/todo_page.py)
   - CRUD Tests (Creation, Completion, Deletion, Editing): [`selenium/tests/test_todo_crud.py`](./selenium/tests/test_todo_crud.py)
   - Filtering Tests (All, Active, Completed): [`selenium/tests/test_todo_filter.py`](./selenium/tests/test_todo_filter.py)
2. **Part 2 — Playwright E2E Suite (40 pts)**:
   - Page Object Model: [`playwright/pages/TodoPage.js`](./playwright/pages/TodoPage.js)
   - CRUD Tests: [`playwright/tests/todo-crud.spec.js`](./playwright/tests/todo-crud.spec.js)
   - Filtering Tests: [`playwright/tests/todo-filter.spec.js`](./playwright/tests/todo-filter.spec.js)
3. **Part 3 — BDD Scenarios with Gherkin & Behave (10 pts)**:
   - Feature Specification: [`features/todo.feature`](./features/todo.feature)
   - Step Definitions: [`features/steps/todo_steps.py`](./features/steps/todo_steps.py)
4. **Part 4 — Framework Comparison Report (10 pts)**:
   - Detailed analysis of Execution Time, Code Complexity (LOC), Developer Experience, and Recommendations in [`COMPARISON_REPORT.md`](./COMPARISON_REPORT.md).
5. **Bonus Features (+10 pts)**:
   - **Bonus A (Visual Regression)**: Automated screenshot capture and pixel-by-pixel visual diff verification using Pillow (`test_bonus_a_visual_regression`).
   - **Bonus B (Cross-Browser Testing)**: Multi-engine Playwright configuration (`chromium`, `firefox`, `webkit`) and compatibility analysis.
   - **Bonus C (Performance Metrics)**: Automated timing benchmarks for page load and CRUD operations (`test_bonus_c_performance_metrics`).

---

## 🗂️ Directory Structure

```
homework-8/
├── selenium/
│   ├── pages/
│   │   ├── __init__.py
│   │   └── todo_page.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_todo_crud.py
│   │   ├── test_todo_filter.py
│   │   └── test_bonus_visual_and_performance.py
│   └── requirements.txt
├── playwright/
│   ├── pages/
│   │   └── TodoPage.js
│   ├── tests/
│   │   ├── todo-crud.spec.js
│   │   └── todo-filter.spec.js
│   ├── playwright.config.js
│   └── package.json
├── features/
│   ├── environment.py
│   ├── todo.feature
│   └── steps/
│       └── todo_steps.py
├── screenshots/
│   ├── selenium_01_single_task.png
│   ├── selenium_02_multiple_tasks.png
│   ├── selenium_03_task_completed.png
│   ├── selenium_04_task_edited.png
│   ├── selenium_05_filter_active.png
│   ├── selenium_06_filter_completed.png
│   ├── visual_baseline_empty.png
│   ├── visual_rerun_empty.png
│   └── visual_populated_state.png
├── COMPARISON_REPORT.md
├── README.md
└── .gitignore
```

---

## 🚀 Setup & Running Instructions

### 1. Run Selenium Tests (Python + Pytest)

Install Python dependencies:
```bash
pip install -r selenium/requirements.txt
```

Run the Selenium E2E test suite (runs headless by default):
```bash
pytest selenium/tests -v
```

To run with a visible browser window:
```bash
HEADLESS=false pytest selenium/tests -v
```

---

### 2. Run Playwright Tests (JavaScript)

Navigate to the `playwright/` folder and install dependencies:
```bash
cd playwright
npm install
```

Run the Playwright E2E test suite:
```bash
npm test
```

Run across all configured browsers (Chromium, Firefox, WebKit):
```bash
npm run test:all-browsers
```

Run in headed (visible) mode:
```bash
npm run test:headed
```

---

### 3. Run BDD Scenarios (Gherkin + Behave)

From the `homework-8/` root directory:
```bash
behave features/todo.feature
```

To run BDD scenarios with a visible browser window:
```bash
HEADLESS=false behave features/todo.feature
```

