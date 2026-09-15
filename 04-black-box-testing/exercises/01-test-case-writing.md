# Exercise 1: Test Case Writing

**Module**: 4 - Black Box Testing  
**Difficulty**: Beginner  
**Time**: 45 minutes

---

## 🎯 Objectives

Practice writing clear, comprehensive test cases following best practices.

By completing this exercise, you will:

- Write well-structured test cases
- Use proper test case format and components
- Differentiate between positive and negative test cases
- Document test data and expected results clearly

---

## Instructions

For each scenario below, write **complete test cases** following this template:

```markdown
**Test Case ID**: TC_XXX_001
**Title**: Brief descriptive title
**Priority**: Critical/High/Medium/Low
**Type**: Positive/Negative

**Description**:
What this test case validates

**Preconditions**:

- Setup required before test execution

**Test Steps**:

1. Step 1
2. Step 2
3. Step 3

**Test Data**:

- Input 1: value
- Input 2: value

**Expected Result**:

- Expected outcome 1
- Expected outcome 2

**Status**: (To be filled during execution)
**Notes**: (Any special considerations)
```

---

## Scenario 1: User Registration Form

### Requirements

A user registration form with the following fields:

- **Email**: Required, must be valid email format
- **Password**: Required, 8-20 characters, must include uppercase, lowercase, and digit
- **Confirm Password**: Required, must match password
- **Age**: Required, must be 18-100
- **Terms & Conditions**: Required, must be checked

**Behavior**:

- Valid submission → Success message + redirect to login page
- Invalid submission → Error message(s) displayed, form not submitted

### Your Task

Write **5 test cases**:

1. One **positive** test case (all valid inputs)
2. One test case for **invalid email**
3. One test case for **password mismatch**
4. One test case for **age boundary** (below 18)
5. One test case for **unchecked terms**

### Example: Positive Test Case

```markdown
**Test Case ID**: TC_REG_001
**Title**: Successful registration with all valid inputs
**Priority**: Critical
**Type**: Positive

**Description**:
Verify that a user can successfully register with all valid inputs.

**Preconditions**:

- Application is accessible at https://app.example.com/register
- Email testuser123@example.com does not exist in database

**Test Steps**:

1. Navigate to https://app.example.com/register
2. Enter "testuser123@example.com" in Email field
3. Enter "SecurePass123" in Password field
4. Enter "SecurePass123" in Confirm Password field
5. Enter "25" in Age field
6. Check the "I agree to Terms & Conditions" checkbox
7. Click "Register" button

**Test Data**:

- Email: testuser123@example.com
- Password: SecurePass123
- Confirm Password: SecurePass123
- Age: 25
- Terms Accepted: Yes

**Expected Result**:

1. Success message displays: "Registration successful! Please check your email."
2. User is redirected to /login page within 2 seconds
3. Verification email sent to testuser123@example.com
4. New user record created in database with status "Pending Verification"

**Status**: (To be filled)
**Notes**: Email verification required before login
```

### Now write the remaining 4 test cases:

```markdown
**Test Case ID**: TC_REG_002
**Title**:
...

**Test Case ID**: TC_REG_003
...

**Test Case ID**: TC_REG_004
...

**Test Case ID**: TC_REG_005
...
```

---

## Scenario 2: Shopping Cart

### Requirements

Shopping cart functionality:

- Users can add items (1-10 items maximum)
- Each item has quantity (1-99 per item)
- Cart displays total price
- "Checkout" button enabled only when cart has items
- "Clear Cart" button removes all items

### Your Task

Write **6 test cases**:

1. Add single item to empty cart
2. Add maximum items (10 items)
3. Try to add 11th item (should be prevented)
4. Update item quantity to maximum (99)
5. Try to set quantity to 0 or negative (should fail)
6. Clear cart with multiple items

---

## Scenario 3: Search Functionality

### Requirements

Product search with these features:

- Search box accepts 2-100 characters
- Search triggered by clicking "Search" button or pressing Enter
- Results display product name, price, and image
- "No results found" message if no matches
- Search history saved (last 10 searches)

### Your Task

Write **5 test cases**:

1. Search with valid query (5-10 characters)
2. Search with minimum length (2 characters)
3. Search with maximum length (100 characters)
4. Search with 1 character (should show error)
5. Search with no results

---

## Scenario 4: File Upload

### Requirements

File upload feature:

- Allowed formats: JPG, PNG, PDF
- Maximum file size: 5 MB
- Minimum file size: 1 KB
- Upload progress bar displayed
- Success/error message after upload

### Your Task

Write **6 test cases**:

1. Upload valid JPG file (2 MB)
2. Upload file at maximum size (5 MB)
3. Upload file exceeding maximum (6 MB) - should fail
4. Upload unsupported format (e.g., .exe) - should fail
5. Upload file below minimum size (< 1 KB) - should fail
6. Upload with no file selected - should fail

---

## Scenario 5: Login System

### Requirements

Login system with:

- Username (email) and password fields required
- "Remember me" checkbox (optional)
- "Forgot password?" link
- Max 3 failed attempts before account locked
- Session timeout after 30 minutes of inactivity

### Your Task

Write **7 test cases**:

1. Successful login with valid credentials
2. Failed login with wrong password
3. Failed login with non-existent username
4. Account locked after 3rd failed attempt
5. Login with "Remember me" checked
6. Session timeout after 30 minutes
7. Login with empty fields

---

## Deliverables

Create a document with **all test cases** for all 5 scenarios.

### Format Options

**Option A: Markdown file**

```
# Test Cases - Exercise 1

## Scenario 1: User Registration
### TC_REG_001: ...
### TC_REG_002: ...
...
```

**Option B: Spreadsheet**

| ID  | Title | Priority | Type | Description | Preconditions | Steps | Test Data | Expected Result |
| --- | ----- | -------- | ---- | ----------- | ------------- | ----- | --------- | --------------- |

**Option C: Test Management Tool**

- Use TestLink, Zephyr, or similar
- Export as PDF

---

## Evaluation Criteria

Your test cases will be evaluated on:

| Criteria             | Points | Description                            |
| -------------------- | ------ | -------------------------------------- |
| **Completeness**     | 30     | All required components present        |
| **Clarity**          | 25     | Steps are clear and unambiguous        |
| **Test Data**        | 15     | Specific, realistic test data provided |
| **Expected Results** | 20     | Measurable and detailed                |
| **Coverage**         | 10     | Both positive and negative cases       |

**Total**: 100 points

---

## Common Mistakes to Avoid

❌ **Vague steps**: "Enter user information"  
✅ **Specific steps**: "Enter 'john.doe@example.com' in Email field"

❌ **Missing test data**: "Enter password"  
✅ **Specific data**: "Enter 'SecurePass123' in Password field"

❌ **Vague expected results**: "User should be logged in"  
✅ **Specific results**: "1) Redirect to /dashboard, 2) Display 'Welcome John' message, 3) Set session cookie"

❌ **Multiple behaviors in one test**: Login + profile update + logout  
✅ **One test per behavior**: Separate test cases

---

## Tips for Success

1. **Be Specific**: Use exact field names, button labels, URLs
2. **Use Real Data**: Don't use "test@test.com", use realistic emails
3. **Number Steps**: Makes it easy to reference
4. **Measurable Results**: Avoid "should work", use "displays X message"
5. **Consider Edge Cases**: Empty fields, maximum values, special characters
6. **Document Assumptions**: Note anything not explicitly stated in requirements

---

## Bonus Challenge (Optional)

For **Scenario 1 (User Registration)**, implement the test cases in code:

### Python (pytest)

```python
def test_successful_registration():
    """TC_REG_001: Successful registration with valid inputs"""
    # Implement using Selenium or API testing
    pass

def test_invalid_email():
    """TC_REG_002: Registration with invalid email"""
    pass
```

### JavaScript (Jest + Playwright)

```javascript
describe("User Registration", () => {
  test("TC_REG_001: Successful registration", async () => {
    // Implement using Playwright
  });

  test("TC_REG_002: Invalid email", async () => {
    // Implement
  });
});
```

---

## Solution Template

Use this as a starting point:

```markdown
# Test Cases - Black Box Testing Exercise 1

**Student Name**: **\*\***\_\_\_**\*\***
**Date**: **\*\***\_\_\_**\*\***

---

## Scenario 1: User Registration

### TC_REG_001: Successful registration with all valid inputs

**Priority**: Critical  
**Type**: Positive

**Description**:
Verify that a user can successfully register when all fields contain valid data.

**Preconditions**:

- Application accessible at https://app.example.com/register
- Test email not already registered

**Test Steps**:

1. ...
2. ...

**Test Data**:

- Email: ...
- Password: ...

**Expected Result**:

1. ...
2. ...

---

### TC_REG_002: Registration with invalid email format

**Priority**: High  
**Type**: Negative

...

---

## Scenario 2: Shopping Cart

...
```

---

## Next Steps

After completing this exercise:

1. Review [Theory: Test Case Design](../theory/01-test-case-design.md)
2. Compare your test cases with peers
3. Practice with [Exercise 2: Equivalence Partitioning](./02-equivalence-partitioning.md)
4. Keep these test cases - you'll implement them later in the course!

---

**Good luck! Remember: A good test case is one that anyone can execute and get the same results.** 🎯
