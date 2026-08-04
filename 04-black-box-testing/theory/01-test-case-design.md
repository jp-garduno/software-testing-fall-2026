# Test Case Design

**Module**: 4 - Black Box Testing  
**Topic**: Designing Effective Test Cases  
**Reading Time**: 25 minutes

---

## 🎯 Learning Objectives

After reading this document, you will be able to:

- Understand what makes a good test case
- Write clear, comprehensive test cases
- Structure test cases properly
- Manage test case documentation
- Evaluate test case quality

---

## What is a Test Case?

A **test case** is a set of conditions or variables under which a tester determines whether a system works correctly.

### Components of a Test Case

Every test case should include:

1. **Test Case ID**: Unique identifier (e.g., TC_001)
2. **Test Case Title**: Brief, descriptive name
3. **Description**: What the test case validates
4. **Preconditions**: Setup required before execution
5. **Test Steps**: Detailed instructions to execute
6. **Test Data**: Input values to use
7. **Expected Result**: What should happen
8. **Actual Result**: What actually happened (filled during execution)
9. **Status**: Pass/Fail/Blocked
10. **Priority**: Critical/High/Medium/Low
11. **Created By**: Author name
12. **Execution Date**: When the test was run

---

## Example Test Case

### Test Case Template

```markdown
**Test Case ID**: TC_LOGIN_001
**Title**: Successful login with valid credentials
**Module**: Authentication
**Priority**: Critical
**Created By**: Test Engineer
**Date Created**: 2026-08-04

**Description**:
Verify that a user can successfully log in with valid username and password.

**Preconditions**:

- User account exists in the database
- Username: testuser@example.com
- Password: ValidPass123!
- Application is accessible

**Test Steps**:

1. Navigate to https://app.example.com/login
2. Enter username in the "Email" field
3. Enter password in the "Password" field
4. Click the "Login" button

**Test Data**:

- Username: testuser@example.com
- Password: ValidPass123!

**Expected Result**:

- User is redirected to dashboard page (https://app.example.com/dashboard)
- Welcome message displays: "Welcome back, Test User!"
- User menu shows in top-right corner
- Session cookie is set

**Actual Result**: _(Filled during execution)_

**Status**: _(Pass/Fail)_

**Notes/Comments**: _(Any observations)_
```

---

## What Makes a Good Test Case?

### 1. Clear and Unambiguous

**Bad Example**:

```
Test: Check login
Steps: Login to system
Expected: Works
```

**Good Example**:

```
Test: Verify successful login with valid credentials
Steps:
1. Open login page at /login
2. Enter "user@example.com" in email field
3. Enter "Password123!" in password field
4. Click "Sign In" button
Expected:
- User redirected to /dashboard
- User name displayed in header
- Session token stored in cookies
```

### 2. Repeatable

Anyone should be able to execute the test case and get the same results.

**Include**:

- Exact URLs
- Specific field names
- Precise button labels
- Clear navigation paths

### 3. Self-Contained

Each test case should be independent.

**Bad**: Test case depends on previous test running first  
**Good**: Test case includes all necessary preconditions

### 4. Traceable

Link test cases to requirements.

```
Requirement: REQ-AUTH-001 - Users must log in with email and password
Test Cases:
- TC_AUTH_001: Valid login
- TC_AUTH_002: Invalid email format
- TC_AUTH_003: Wrong password
- TC_AUTH_004: Empty fields
```

### 5. Focused

One test case should verify one specific behavior.

**Bad**: Test login, profile update, and logout in one test  
**Good**: Three separate test cases

---

## Test Case Structure

### Arrange-Act-Assert (AAA) Pattern

```python
def test_login_with_valid_credentials():
    # Arrange - Set up test data and preconditions
    username = "testuser@example.com"
    password = "ValidPass123!"
    user = create_test_user(username, password)

    # Act - Perform the action being tested
    response = login(username, password)

    # Assert - Verify the expected outcome
    assert response.status_code == 200
    assert response.redirect_url == "/dashboard"
    assert "session_token" in response.cookies
```

### Given-When-Then (BDD Style)

```gherkin
Scenario: User logs in with valid credentials
  Given a registered user with email "testuser@example.com"
  And the user is on the login page
  When the user enters valid credentials
  And clicks the "Login" button
  Then the user should be redirected to the dashboard
  And a welcome message should be displayed
  And a session should be created
```

---

## Types of Test Cases

### 1. Positive Test Cases

Test that the system works correctly with valid inputs.

**Example**: Login with correct username and password

### 2. Negative Test Cases

Test that the system handles invalid inputs gracefully.

**Example**: Login with wrong password

### 3. Edge/Boundary Test Cases

Test behavior at the limits of acceptable inputs.

**Example**: Login with maximum allowed password length (50 characters)

### 4. Error Test Cases

Test error handling and recovery.

**Example**: Login when database is unavailable

---

## Test Case Organization

### By Feature

```
Authentication/
├── TC_AUTH_001_valid_login.md
├── TC_AUTH_002_invalid_password.md
├── TC_AUTH_003_account_locked.md
└── TC_AUTH_004_password_reset.md
```

### By Priority

- **P0 (Critical)**: Smoke tests, core functionality
- **P1 (High)**: Major features
- **P2 (Medium)**: Secondary features
- **P3 (Low)**: Nice-to-have features

### By Test Type

- **Functional**: Feature behavior
- **Regression**: Previously working features
- **Smoke**: Basic functionality check
- **Sanity**: Quick verification after changes

---

## Writing Effective Test Steps

### Be Specific

**Vague**: "Enter user information"  
**Specific**: "Enter 'John Doe' in the 'Full Name' field"

### Use Action Verbs

- Click
- Enter
- Select
- Verify
- Navigate
- Scroll
- Hover
- Wait for

### Number Steps

```
1. Open the application
2. Click "New User" button
3. Enter "john@example.com" in the Email field
4. Click "Save" button
5. Verify success message appears
```

### Include Verification Points

Don't just perform actions—verify results at each critical step.

```
1. Navigate to /products page
   ✓ Verify page title is "Products"
2. Search for "laptop"
   ✓ Verify search results contain "laptop" in title or description
3. Sort by "Price: Low to High"
   ✓ Verify first item has lower price than second item
```

---

## Test Data Management

### Use Realistic Data

**Bad**: Name = "aaaa", Email = "test@test.com"  
**Good**: Name = "Sarah Johnson", Email = "sarah.johnson@example.com"

### Document Test Accounts

```markdown
## Test Accounts

| Username             | Password    | Role  | Status |
| -------------------- | ----------- | ----- | ------ |
| admin@example.com    | Admin123!   | Admin | Active |
| testuser@example.com | Test123!    | User  | Active |
| locked@example.com   | Locked123!  | User  | Locked |
| expired@example.com  | Expired123! | User  | Trial  |
```

### Separate Test Data from Test Logic

**Python Example**:

```python
# test_data.py
LOGIN_CREDENTIALS = {
    "valid_user": {
        "email": "testuser@example.com",
        "password": "ValidPass123!"
    },
    "invalid_password": {
        "email": "testuser@example.com",
        "password": "WrongPassword"
    },
    "invalid_email": {
        "email": "notauser@example.com",
        "password": "ValidPass123!"
    }
}

# test_login.py
from test_data import LOGIN_CREDENTIALS

def test_valid_login():
    credentials = LOGIN_CREDENTIALS["valid_user"]
    response = login(credentials["email"], credentials["password"])
    assert response.success == True
```

---

## Expected vs Actual Results

### Writing Expected Results

Be specific and measurable:

**Vague**: "User should be logged in"

**Specific**:

```
Expected Results:
1. HTTP Status: 200 OK
2. Page URL: https://app.example.com/dashboard
3. Page Title: "Dashboard - MyApp"
4. User Menu: Displays "Test User" with dropdown
5. Session Cookie: "session_id" cookie is set with expiry in 24 hours
6. Database: "last_login" timestamp updated to current time
7. Response Time: Less than 2 seconds
```

### Recording Actual Results

During execution:

```
Actual Results:
1. HTTP Status: 200 OK ✓
2. Page URL: https://app.example.com/dashboard ✓
3. Page Title: "Dashboard - MyApp" ✓
4. User Menu: Displays "Test User" with dropdown ✓
5. Session Cookie: Cookie set, expires in 24 hours ✓
6. Database: "last_login" timestamp updated ✓
7. Response Time: 1.8 seconds ✓

Status: PASS
Executed By: Jane Smith
Date: 2026-08-04 10:30 AM
Environment: QA Environment
Build: v2.3.1
```

---

## Test Case Maintenance

### Keep Test Cases Up to Date

- Review test cases when requirements change
- Update test cases when UI/API changes
- Archive obsolete test cases
- Version control test documentation

### Review and Refactor

Periodically review test cases for:

- **Clarity**: Are steps clear?
- **Relevance**: Still testing important functionality?
- **Redundancy**: Duplicate tests?
- **Coverage**: Missing scenarios?

---

## Test Case Quality Checklist

Before finalizing a test case, verify:

- [ ] Unique and clear test case ID
- [ ] Descriptive title that explains what is being tested
- [ ] Complete preconditions listed
- [ ] Numbered, specific test steps
- [ ] Exact test data provided
- [ ] Measurable expected results
- [ ] Priority assigned
- [ ] Linked to requirement or user story
- [ ] Independent and repeatable
- [ ] Peer reviewed

---

## Common Mistakes to Avoid

### 1. Too Vague

❌ "Test that login works"  
✅ "Verify successful login with valid email and password redirects to dashboard"

### 2. Too Many Actions

❌ One test case with 50 steps testing multiple features  
✅ Multiple focused test cases, each with 5-10 steps

### 3. Missing Preconditions

❌ "Click Submit button"  
✅ "Given user is on registration form with all required fields filled, When user clicks Submit button..."

### 4. No Test Data

❌ "Enter username"  
✅ "Enter 'testuser@example.com' in Username field"

### 5. Ambiguous Expected Results

❌ "User should see error message"  
✅ "Error message 'Invalid password. Please try again.' displays below password field in red text"

---

## Tools for Test Case Management

### Open Source

- **TestLink**: Web-based test management
- **Zephyr**: Jira plugin for test cases
- **TestRail**: Comprehensive test management

### Lightweight Options

- **Markdown Files**: In version control (like this course!)
- **Spreadsheets**: Google Sheets, Excel
- **Notion/Confluence**: Wiki-based documentation

### Example in Markdown

```markdown
# Login Test Cases

## TC_LOGIN_001: Valid Login

**Priority**: P0  
**Status**: Active

**Steps**:

1. Navigate to /login
2. Enter valid email
3. Enter valid password
4. Click Login

**Expected**: Redirect to /dashboard

---

## TC_LOGIN_002: Invalid Password

**Priority**: P1  
**Status**: Active

**Steps**:

1. Navigate to /login
2. Enter valid email
3. Enter invalid password
4. Click Login

**Expected**: Error message "Invalid password"
```

---

## Summary

Good test cases are:

- **Clear**: Anyone can understand and execute
- **Complete**: All necessary information included
- **Consistent**: Follow standard format
- **Correct**: Validate actual requirements
- **Maintainable**: Easy to update when needed

Writing quality test cases is a skill that improves with practice. Start with the template, follow the guidelines, and refine based on feedback.

---

## Practice Exercise

Write a complete test case for one of these scenarios:

1. User registration with email verification
2. Password reset flow
3. Adding items to shopping cart
4. Searching for products with filters
5. Submitting a contact form

Include all components: ID, title, description, preconditions, steps, test data, and expected results.

---

## Next Steps

- Read [02-equivalence-partitioning.md](./02-equivalence-partitioning.md)
- Practice with [Exercise 1: Test Case Writing](../exercises/01-test-case-writing.md)
- Review the [class exercises](../exercises/class-exercises.md)
