# Homework 4: Black Box Testing Suite

**Module**: 4 - Black Box Testing  
**Due Date**: End of Week 5  
**Points**: 110 (100 base + 10 bonus)  
**Estimated Time**: 4-5 hours

---

## 🎯 Objectives

This homework will help you:

- Apply all four black box testing techniques systematically
- Design comprehensive test cases using Equivalence Partitioning (EP)
- Identify and test boundary values using Boundary Value Analysis (BVA)
- Create and use decision tables for complex business logic
- Model and test state transitions in a system
- Implement automated tests based on black box design
- Analyze test effectiveness across different techniques

---

## 📋 Assignment Overview

You will design and implement a comprehensive black box test suite for an **Online Banking System**. This assignment requires both test design documentation (planning) and test implementation (coding) using either Python or JavaScript.

The system has complex business rules, multiple states, and various boundary conditions - perfect for applying all black box techniques you've learned.

---

## 🏦 System Under Test: SecureBank Online Banking

### System Description

SecureBank is an online banking platform that allows customers to manage their accounts, transfer money, and pay bills.

### Account Types

- **Savings Account**:

  - Minimum balance: $100
  - Monthly fee: $5 (waived if balance > $1,000)
  - Daily transfer limit: $2,000

- **Checking Account**:

  - Minimum balance: $0
  - Monthly fee: $10 (waived if balance > $5,000)
  - Daily transfer limit: $5,000

- **Premium Account**:
  - Minimum balance: $10,000
  - Monthly fee: $0
  - Daily transfer limit: $50,000

### Account States

- **Active**: Normal operations allowed
- **Frozen**: No transactions allowed (view only)
- **Suspended**: Below minimum balance, warnings shown
- **Closed**: Account terminated

### Core Features

1. **Account Management**

   - Create account
   - View balance
   - Update account information
   - Close account

2. **Money Transfers**

   - Transfer between own accounts
   - Transfer to other bank accounts
   - Validation: sufficient funds, within daily limit, account active

3. **Bill Payment**

   - Pay utilities, credit cards, etc.
   - Validation: valid payee, amount > $0, account has funds
   - Schedule payments (immediate or future date)

4. **Transaction History**
   - View past transactions
   - Filter by date range
   - Export to CSV

### Business Rules

1. **Transfer Rules**:

   - Minimum transfer: $0.01
   - Maximum transfer: Account-type daily limit
   - Cannot transfer if balance < transfer amount
   - Cannot transfer from Frozen or Closed accounts
   - Daily limit resets at midnight

2. **Account State Transitions**:

   - Active → Frozen: By customer request or fraud detection
   - Active → Suspended: Balance drops below minimum
   - Suspended → Active: Balance restored above minimum
   - Any state → Closed: By customer request
   - Closed accounts cannot be reopened

3. **Fee Processing**:
   - Monthly fees charged on 1st of month
   - Fees waived if balance meets threshold (checked at fee time)
   - Insufficient funds for fee → account suspended

---

## 📝 Part 1: Test Design Document (25 points)

Create a comprehensive test design document applying all four black box techniques.

### 1.1 Equivalence Partitioning (6 points)

Identify and document equivalence classes for key inputs.

**Template**:

```markdown
## Equivalence Partitioning

### Input: Transfer Amount

| Partition ID | Description                | Type    | Representative Value | Expected Result                |
| ------------ | -------------------------- | ------- | -------------------- | ------------------------------ |
| EP1          | Valid amount within limits | Valid   | $500                 | Transfer succeeds              |
| EP2          | Zero amount                | Invalid | $0                   | Error: Amount must be positive |
| EP3          | Negative amount            | Invalid | -$100                | Error: Amount must be positive |
| EP4          | Amount exceeds daily limit | Invalid | $100,000             | Error: Exceeds daily limit     |
| EP5          | Amount exceeds balance     | Invalid | Balance + $1         | Error: Insufficient funds      |

### Input: Account Type

| Partition ID | Description | Type | Representative Value | Expected Result |
| ------------ | ----------- | ---- | -------------------- | --------------- |

...
```

**Required Coverage**:

- Transfer amount
- Account type
- Account balance
- Payee information for bill payment
- Date range for transaction history (at least 5 inputs with partitions)

### 1.2 Boundary Value Analysis (7 points)

Identify boundary values for numerical and state boundaries.

**Template**:

```markdown
## Boundary Value Analysis

### Boundary: Transfer Amount (Checking Account - $5,000 limit)

| Test ID | Boundary         | Test Value | Expected Result                |
| ------- | ---------------- | ---------- | ------------------------------ |
| BV1     | Below minimum    | $0.00      | Error: Amount must be positive |
| BV2     | Minimum valid    | $0.01      | Transfer succeeds              |
| BV3     | Just below limit | $4,999.99  | Transfer succeeds              |
| BV4     | At limit         | $5,000.00  | Transfer succeeds              |
| BV5     | Just above limit | $5,000.01  | Error: Exceeds daily limit     |
| BV6     | Far above limit  | $10,000.00 | Error: Exceeds daily limit     |

### Boundary: Account Balance vs Minimum (Savings - $100 minimum)

| Test ID | Boundary | Test Value | Expected Result |
| ------- | -------- | ---------- | --------------- |

...
```

**Required Coverage**:

- Transfer amount boundaries (for at least 2 account types)
- Account balance boundaries (minimum balance threshold)
- Daily limit boundaries
- At least 5 different boundaries with 4-6 test values each

### 1.3 Decision Tables (7 points)

Create decision tables for complex business rules.

**Template**:

```markdown
## Decision Tables

### Decision Table 1: Transfer Validation

| Condition                 | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 | Rule 6 | Rule 7 | Rule 8 |
| ------------------------- | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| Sufficient funds?         | Y      | Y      | Y      | Y      | N      | N      | N      | N      |
| Within daily limit?       | Y      | Y      | N      | N      | Y      | Y      | N      | N      |
| Account is Active?        | Y      | N      | Y      | N      | Y      | N      | Y      | N      |
| **Action**                |
| Transfer succeeds         | X      |        |        |        |        |        |        |        |
| Error: Insufficient funds |        |        |        |        | X      | X      | X      | X      |
| Error: Exceeds limit      |        |        | X      |        |        |        | X      |        |
| Error: Account frozen     |        | X      |        | X      |        | X      |        | X      |

### Decision Table 2: Monthly Fee Processing

| Condition                   | Rule 1  | Rule 2  | Rule 3   | Rule 4  |
| --------------------------- | ------- | ------- | -------- | ------- |
| Account type                | Savings | Savings | Checking | Premium |
| Balance > waiver threshold? | Y       | N       | Y        | -       |
| **Action**                  |

...
```

**Required Coverage**:

- Transfer validation decision table
- Monthly fee processing decision table
- At least 1 additional decision table (e.g., bill payment validation, account creation)

### 1.4 State Transition Testing (5 points)

Create a state transition diagram and table.

**Template**:

```markdown
## State Transition Testing

### State Transition Diagram
```

[Active] ---(Balance < Minimum)---> [Suspended]
| |
|---(Customer/Fraud Request)--> [Frozen]
| |
+---------(Close Request)-------> [Closed]

[Suspended] ---(Deposit restores)---> [Active]
[Suspended] ---(Close Request)-----> [Closed]
[Frozen] ------(Unfreeze)----------> [Active]
[Frozen] ------(Close Request)-----> [Closed]

```

### State Transition Table

| Current State | Event | Next State | Action/Output |
|---------------|-------|------------|---------------|
| Active | Balance drops below minimum | Suspended | Send warning notification |
| Active | Freeze request | Frozen | Block all transactions |
| Active | Close request | Closed | Final statement generated |
| Suspended | Deposit restores balance | Active | Remove restrictions |
| Suspended | Close request | Closed | Final statement generated |
| Frozen | Unfreeze approved | Active | Restore full access |
| Frozen | Close request | Closed | Final statement generated |
| Closed | Any event | Closed | Error: Account closed |

### State Transition Test Cases

| Test ID | Start State | Event | Expected End State | Validation |
|---------|-------------|-------|-------------------|------------|
| ST1 | Active | Transfer causes balance < $100 | Suspended | Warning shown, status = Suspended |
| ST2 | Suspended | Deposit $500 | Active | Status = Active, full access restored |
...
```

**Required**:

- Complete state diagram (ASCII art or description)
- State transition table with all valid transitions
- At least 8 state transition test cases

---

## 📝 Part 2: Test Implementation (30 points)

Implement automated tests based on your test design using **Python with pytest** OR **JavaScript with Jest**.

### 2.1 Setup Requirements

**Python Option**:

```bash
pip install pytest pytest-cov
```

**JavaScript Option**:

```bash
npm install --save-dev jest
```

### 2.2 Implementation Requirements

Create the following test files:

```
tests/
├── test_equivalence_partitioning.py (or .test.js)
├── test_boundary_values.py (or .test.js)
├── test_decision_tables.py (or .test.js)
├── test_state_transitions.py (or .test.js)
└── conftest.py (or jest.setup.js)
```

### 2.3 Minimum Test Cases

You must implement **at least 20 test cases** total:

- At least 5 EP tests
- At least 6 BVA tests
- At least 5 decision table tests
- At least 4 state transition tests

### 2.4 Code Structure

**Python Example**:

```python
# banking_system.py

class BankAccount:
    def __init__(self, account_type, initial_balance):
        self.account_type = account_type
        self.balance = initial_balance
        self.state = "Active"
        self.daily_transfer_total = 0

    def transfer(self, amount):
        """Transfer money from this account."""
        # Implement transfer logic with validation
        pass

    def get_daily_limit(self):
        """Return daily transfer limit based on account type."""
        limits = {
            "Savings": 2000,
            "Checking": 5000,
            "Premium": 50000
        }
        return limits.get(self.account_type, 0)

    # Add more methods...

# test_boundary_values.py

import pytest
from banking_system import BankAccount

class TestBoundaryValues:

    def test_transfer_at_minimum_valid_amount(self):
        """BV2: Transfer exactly $0.01 should succeed"""
        account = BankAccount("Checking", 1000)
        result = account.transfer(0.01)
        assert result["success"] == True
        assert account.balance == 999.99

    def test_transfer_below_minimum(self):
        """BV1: Transfer $0.00 should fail"""
        account = BankAccount("Checking", 1000)
        result = account.transfer(0.00)
        assert result["success"] == False
        assert "must be positive" in result["error"]

    def test_transfer_at_daily_limit_checking(self):
        """BV4: Transfer exactly at $5,000 limit should succeed"""
        account = BankAccount("Checking", 10000)
        result = account.transfer(5000)
        assert result["success"] == True
        assert account.daily_transfer_total == 5000

    # Add more tests...
```

**JavaScript Example**:

```javascript
// bankingSystem.js

class BankAccount {
  constructor(accountType, initialBalance) {
    this.accountType = accountType;
    this.balance = initialBalance;
    this.state = "Active";
    this.dailyTransferTotal = 0;
  }

  transfer(amount) {
    // Implement transfer logic with validation
  }

  getDailyLimit() {
    const limits = {
      Savings: 2000,
      Checking: 5000,
      Premium: 50000,
    };
    return limits[this.accountType] || 0;
  }

  // Add more methods...
}

module.exports = BankAccount;

// boundaryValues.test.js

const BankAccount = require("./bankingSystem");

describe("Boundary Value Analysis", () => {
  test("BV2: Transfer exactly $0.01 should succeed", () => {
    const account = new BankAccount("Checking", 1000);
    const result = account.transfer(0.01);
    expect(result.success).toBe(true);
    expect(account.balance).toBeCloseTo(999.99, 2);
  });

  test("BV1: Transfer $0.00 should fail", () => {
    const account = new BankAccount("Checking", 1000);
    const result = account.transfer(0.0);
    expect(result.success).toBe(false);
    expect(result.error).toContain("must be positive");
  });

  test("BV4: Transfer exactly at $5,000 limit should succeed", () => {
    const account = new BankAccount("Checking", 10000);
    const result = account.transfer(5000);
    expect(result.success).toBe(true);
    expect(account.dailyTransferTotal).toBe(5000);
  });

  // Add more tests...
});
```

### 2.5 Test Requirements

Each test must:

- Have a clear, descriptive name
- Include a docstring/comment referencing the test design (e.g., "BV2:", "EP1:", "ST3:")
- Use proper assertions
- Be independent (can run in any order)
- Actually pass (all tests must pass)

---

## 📝 Part 3: Test Execution Report (25 points)

### 3.1 Run All Tests

**Python**:

```bash
pytest -v --cov=banking_system --cov-report=html --cov-report=term
```

**JavaScript**:

```bash
npm test -- --coverage --verbose
```

### 3.2 Report Contents

Create a document (`test-execution-report.md`) with:

**1. Test Summary** (5 points)

```markdown
## Test Execution Summary

- **Date**: 2026-08-XX
- **Test Framework**: pytest / Jest
- **Total Tests**: 23
- **Passed**: 23
- **Failed**: 0
- **Skipped**: 0
- **Duration**: 0.45s

## Coverage Summary

- **Line Coverage**: 87%
- **Branch Coverage**: 82%
- **Function Coverage**: 100%
```

**2. Test Results by Technique** (10 points)

```markdown
## Results by Technique

### Equivalence Partitioning (5 tests)

- ✅ test_transfer_valid_amount
- ✅ test_transfer_zero_amount
- ✅ test_transfer_negative_amount
- ✅ test_transfer_exceeds_limit
- ✅ test_account_type_savings

**Defects Found**: None (or describe any issues)

### Boundary Value Analysis (7 tests)

- ✅ test_transfer_at_minimum_valid_amount
- ✅ test_transfer_below_minimum
  ...

**Defects Found**: Found edge case where $0.001 rounds incorrectly

### Decision Tables (6 tests)

...

### State Transitions (5 tests)

...
```

**3. Screenshots** (5 points)

- Terminal output showing test results
- Coverage report (HTML or terminal)
- Any test failures and fixes

**4. Coverage Analysis** (5 points)

- Which code paths are covered?
- Which are not covered and why?
- How does coverage differ by technique?

---

## 📝 Part 4: Analysis Report (15 points)

Write a report (500-700 words) analyzing your experience. Save as `analysis-report.md`.

### Required Sections

**1. Technique Effectiveness** (5 points)

- Which black box technique found the most potential issues?
- Which was easiest/hardest to apply?
- Which gave you the most confidence in quality?

**2. Coverage Comparison** (4 points)

- How much of the system did each technique cover?
- Were there overlaps between techniques?
- Were there gaps that no technique caught?

**3. Real-World Application** (3 points)

- How would you apply these techniques in a real project?
- Which technique would you prioritize and why?
- What combinations of techniques work best together?

**4. Recommendations** (3 points)

- What would you do differently next time?
- How could the test design be improved?
- What additional testing would you recommend?

### Example Structure

```markdown
# Black Box Testing Analysis Report

## Executive Summary

Brief overview of your findings (2-3 sentences)

## Technique Effectiveness

### Equivalence Partitioning

EP was particularly effective at... I found that... The main challenge was...

### Boundary Value Analysis

BVA revealed edge cases in... The most valuable boundary was...

### Decision Tables

Decision tables helped visualize... The complexity of... I discovered that...

### State Transition Testing

State testing was crucial for... Without this technique, I would have missed...

## Coverage Comparison

[Create a table or chart comparing techniques]

## Real-World Application

In a professional setting, I would... The banking domain particularly benefits from...

## Recommendations

For future testing of similar systems...

## Lessons Learned

The most important insight was...
```

---

## 📝 Part 5: Documentation & Organization (5 points)

### Repository Structure

```
homework-4/
├── README.md (setup instructions, how to run)
├── design/
│   └── test-design-document.md (Part 1)
├── src/
│   ├── banking_system.py (or .js)
│   └── __init__.py (if Python)
├── tests/
│   ├── test_equivalence_partitioning.py
│   ├── test_boundary_values.py
│   ├── test_decision_tables.py
│   ├── test_state_transitions.py
│   └── conftest.py (or jest.config.js)
├── reports/
│   ├── test-execution-report.md (Part 3)
│   ├── analysis-report.md (Part 4)
│   └── screenshots/
│       ├── test-results.png
│       └── coverage-report.png
├── requirements.txt (or package.json)
└── .gitignore
```

### README Requirements

Your README must include:

1. Project description
2. Prerequisites (Python 3.11+ or Node 22+)
3. Installation instructions
4. How to run tests
5. How to view coverage report
6. Brief description of what was tested

### Example README:

````markdown
# Homework 4: Black Box Testing - SecureBank System

## Description

Comprehensive black box test suite for an online banking system using EP, BVA,
decision tables, and state transition testing.

## Prerequisites

- Python 3.11+ (or Node.js 22+)
- pytest and pytest-cov (or Jest)

## Installation

```bash
# Python
pip install -r requirements.txt

# JavaScript
npm install
```
````

## Running Tests

```bash
# Python - All tests
pytest -v

# Python - With coverage
pytest --cov=src --cov-report=html

# JavaScript
npm test

# JavaScript - With coverage
npm test -- --coverage
```

## Project Structure

- `design/` - Test design documentation
- `src/` - Banking system implementation
- `tests/` - Automated test suite
- `reports/` - Test execution and analysis reports

## Test Coverage

- Equivalence Partitioning: 5 tests
- Boundary Value Analysis: 7 tests
- Decision Tables: 6 tests
- State Transitions: 5 tests
- **Total**: 23 tests

## Author

[Your Name]

````

---

## 📤 Submission Requirements

### GitHub Repository

1. Create a new public repository named `banking-black-box-tests` or similar
2. Include all files listed in Part 5 structure
3. Ensure all tests pass before submitting
4. Tag your final submission: `git tag -a hw4-final -m "Homework 4 submission"`

### Canvas Submission

Submit:
1. **GitHub Repository URL** (including tag)
2. **Test Design Document** (PDF export of the markdown)
3. **Analysis Report** (PDF)
4. **Brief Reflection** (200-300 words):
   - What was most challenging?
   - What did you learn about black box testing?
   - How confident are you in the quality of the banking system?

---

## 🎯 Grading Rubric

| **Category** | **Points** | **Criteria** |
|--------------|------------|--------------|
| **Test Design - EP** | 6 | At least 5 inputs with complete partition tables, valid/invalid classes |
| **Test Design - BVA** | 7 | At least 5 boundaries with 4-6 test values each, systematic coverage |
| **Test Design - Decision Tables** | 7 | At least 3 decision tables, all rules covered, clear actions |
| **Test Design - State Transitions** | 5 | Complete diagram, transition table, 8+ test cases |
| **Test Implementation** | 30 | 20+ tests, all pass, proper structure, good assertions, follows design |
| **Test Execution Report** | 25 | Complete results, coverage analysis, screenshots, clear documentation |
| **Analysis Report** | 15 | 500-700 words, addresses all sections, thoughtful insights |
| **Documentation** | 5 | Well-organized repo, complete README, clear setup instructions |
| **Quality & Professionalism** | 5 | Code quality, commit messages, presentation |
| **Total** | **110** | (10 bonus points included) |

### Detailed Grading Criteria

**Excellent (90-100%)**:
- Comprehensive test design covering all edge cases
- All tests implemented and passing
- Deep analysis with professional insights
- Production-ready documentation
- Goes beyond minimum requirements

**Good (80-89%)**:
- Complete coverage of requirements
- Most tests implemented correctly
- Clear analysis with good insights
- Good documentation
- Minor gaps or improvements possible

**Satisfactory (70-79%)**:
- Meets minimum requirements
- Tests pass but coverage could be better
- Basic analysis
- Adequate documentation
- Several areas need improvement

**Needs Improvement (<70%)**:
- Incomplete test design
- Tests fail or insufficient coverage
- Superficial analysis
- Poor documentation
- Missing key components

---

## 🎁 Bonus Opportunities (+10 points)

### Bonus Option 1: Dual Implementation (+5 points)

Implement the test suite in **BOTH Python AND JavaScript**:
- Both must have equivalent tests
- Both must achieve >80% coverage
- Document differences in implementation

### Bonus Option 2: CI/CD Integration (+3 points)

Set up GitHub Actions to run tests automatically:
- Create `.github/workflows/test.yml`
- Run tests on push and pull request
- Generate and upload coverage report
- Add status badge to README

Example workflow:
```yaml
name: Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest --cov=src --cov-report=xml
      - uses: codecov/codecov-action@v2
````

### Bonus Option 3: Visual Diagrams (+2 points)

Create professional visual diagrams (not ASCII art):

- State transition diagram using Mermaid, PlantUML, or draw.io
- Decision tree visualization
- Test coverage visualization
- Include in documentation

---

## 💡 Tips for Success

1. **Start with design first** - Don't code until design is complete
2. **Be systematic** - Work through one technique at a time
3. **Think about edge cases** - Banking has many rules to test
4. **Keep tests independent** - Each test should run standalone
5. **Document as you go** - Don't save documentation for the end
6. **Test your tests** - Make sure they actually catch bugs
7. **Use fixtures/setup** - Reduce code duplication in tests
8. **Reference your design** - Link test code back to design docs
9. **Run tests frequently** - Don't wait until all tests are written
10. **Review coverage** - Ensure tests actually execute your code

---

## ⚠️ Common Mistakes to Avoid

- ❌ **Skipping test design** - Going straight to coding without planning
- ❌ **Incomplete partitions** - Missing invalid classes in EP
- ❌ **Ignoring boundaries** - Only testing valid values
- ❌ **Incomplete decision tables** - Not covering all rule combinations
- ❌ **Invalid state transitions** - Including impossible state changes
- ❌ **Tests that don't match design** - Implementation doesn't follow plan
- ❌ **Tests that always pass** - Not actually validating behavior
- ❌ **Poor test names** - Can't tell what test does from name
- ❌ **No assertions** - Tests run but don't verify anything
- ❌ **Hardcoded test data** - Not using fixtures or setup methods
- ❌ **Missing documentation** - No README or unclear instructions
- ❌ **Submitting failing tests** - All tests must pass

---

## 🆘 Getting Help

If you're stuck:

1. Review the [Module 4 theory materials](../theory/)
2. Check the [black box exercises](../exercises/) for examples
3. Look at testing framework documentation:
   - [pytest documentation](https://docs.pytest.org/)
   - [Jest documentation](https://jestjs.io/)
4. Ask questions in the course discussion forum
5. Attend office hours
6. Review the example test structures provided above

---

## 📚 Resources

### Black Box Testing

- [Module 4 Theory - Equivalence Partitioning](../theory/01-equivalence-partitioning.md)
- [Module 4 Theory - Boundary Value Analysis](../theory/02-boundary-value-analysis.md)
- [Module 4 Theory - Decision Tables](../theory/03-decision-tables.md)
- [Module 4 Theory - State Transition Testing](../theory/04-state-transition-testing.md)

### Testing Frameworks

- [pytest Documentation](https://docs.pytest.org/)
- [pytest Coverage Plugin](https://pytest-cov.readthedocs.io/)
- [Jest Documentation](https://jestjs.io/)
- [Jest Coverage](https://jestjs.io/docs/configuration#collectcoverage-boolean)

### Test Design

- [ISTQB Glossary](https://glossary.istqb.org/)
- [Test Design Techniques](https://www.guru99.com/test-design-techniques.html)
- [Black Box Testing Guide](https://www.softwaretestinghelp.com/black-box-testing/)

---

## ✅ Submission Checklist

Before submitting, verify:

### Design (Part 1)

- [ ] EP tables for at least 5 inputs with valid/invalid partitions
- [ ] BVA tables for at least 5 boundaries with 4-6 test values each
- [ ] At least 3 decision tables with all rules covered
- [ ] Complete state transition diagram and table
- [ ] At least 8 state transition test cases

### Implementation (Part 2)

- [ ] All test files created and organized properly
- [ ] At least 20 test cases implemented
- [ ] All tests pass (run pytest or npm test)
- [ ] Tests reference design document (e.g., "BV2:", "EP1:")
- [ ] Code is clean and well-structured

### Reports (Parts 3 & 4)

- [ ] Test execution report with summary and coverage
- [ ] Screenshots of test results and coverage
- [ ] Analysis report 500-700 words
- [ ] All required sections completed

### Repository (Part 5)

- [ ] Complete README with setup instructions
- [ ] All files organized in correct structure
- [ ] requirements.txt or package.json included
- [ ] .gitignore configured properly
- [ ] Repository is public and accessible

### Submission

- [ ] Repository URL submitted to Canvas
- [ ] Final commit tagged (hw4-final)
- [ ] PDF exports of reports uploaded
- [ ] Reflection document written (200-300 words)
- [ ] All tests pass one final time before submission

---

**Good luck!** This homework brings together all the black box testing techniques you've learned. Take your time with the design phase - good test design leads to effective test implementation! 🎯
