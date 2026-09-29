# Milestone 3: Black Box Testing

**Due**: End of Week 8  
**Points**: 15 (15% of project grade)  
**Focus**: Test planning and black box test case design  
**Module Applied**: Black Box Testing (Module 4)

---

## 🎯 Objectives

- Create comprehensive test strategy
- Design test cases using black box techniques
- Document test plan with traceability
- Apply EP, BVA, Decision Tables, State Transitions
- Establish quality metrics

---

## 📋 Deliverables

### 1. Test Strategy Document (25 points)

Create `docs/milestones/M3/test-strategy.md`:

#### 1.1 Testing Scope

**In Scope**:

- All functional requirements from M1
- User authentication and authorization
- Core business logic
- API endpoints
- Data validation

**Out of Scope**:

- Performance testing (saved for M7)
- Security penetration testing
- Third-party service integrations (mocked)

#### 1.2 Testing Approach

**Test Levels**:

- Unit Testing (M4)
- Integration Testing (M4)
- System Testing (M6)
- Acceptance Testing (M7)

**Test Types**:

- Functional testing
- Boundary testing
- State transition testing
- Error handling

#### 1.3 Entry and Exit Criteria

**Entry Criteria**:

- Feature code complete
- Development environment stable
- Test data available

**Exit Criteria**:

- All high-priority test cases executed
- 90%+ test cases passing
- All critical bugs fixed
- Test coverage meets target (80%+)

#### 1.4 Test Environment

- Development: Local machines
- Testing: Staging environment
- Test data: Synthetic data, no PII

---

### 2. Test Plan Document (30 points)

Create `docs/milestones/M3/test-plan.md`:

#### 2.1 Features to Test

List all features with priority:

| Feature ID | Feature Name      | Priority | Test Technique       |
| ---------- | ----------------- | -------- | -------------------- |
| F-001      | User Registration | High     | EP, BVA, Decision    |
| F-002      | User Login        | High     | EP, State Transition |
| F-003      | Password Reset    | Medium   | EP, BVA              |
| F-004      | Product Catalog   | High     | EP, BVA              |
| F-005      | Shopping Cart     | High     | Decision, State      |
| F-006      | Checkout          | High     | Decision, BVA        |
| ...        | ...               | ...      | ...                  |

#### 2.2 Test Design Techniques

Document which techniques apply to each feature:

**Equivalence Partitioning (EP)**:

- Email validation (valid/invalid formats)
- Price ranges (negative, zero, positive)
- Quantity inputs (valid/invalid/boundary)

**Boundary Value Analysis (BVA)**:

- Password length (min: 8, max: 128 characters)
- Product stock (0, 1, max inventory)
- Price values (0.00, 0.01, MAX_PRICE)

**Decision Tables**:

- User permissions (role-based access)
- Discount calculations (multiple conditions)
- Order validation (stock, payment, address)

**State Transition**:

- Order status flow (pending → processing → shipped → delivered)
- User account states (active, suspended, deleted)
- Shopping cart lifecycle

---

### 3. Test Cases (40 points)

Create `docs/milestones/M3/test-cases.md` with minimum **20 detailed test cases**.

#### 3.1 Test Case Template

```markdown
### TC-001: User Registration with Valid Data

**Feature**: User Registration (F-001)
**Technique**: Equivalence Partitioning
**Priority**: High
**Preconditions**: User not already registered

**Test Data**:

- Email: valid@example.com
- Password: ValidPass123!
- Confirm Password: ValidPass123!

**Test Steps**:

1. Navigate to registration page
2. Enter email in email field
3. Enter password in password field
4. Enter same password in confirm password field
5. Click "Register" button

**Expected Result**:

- User account created successfully
- Confirmation message displayed
- User redirected to dashboard
- Email verification sent

**Actual Result**: [To be filled during execution]
**Status**: [Pass/Fail/Blocked]
**Tested By**: [Name]
**Date**: [Date]
```

#### 3.2 Required Test Cases

Cover these scenarios (minimum):

**User Authentication (6 test cases)**:

- TC-001: Valid registration
- TC-002: Invalid email format
- TC-003: Password too short (BVA)
- TC-004: Duplicate email registration
- TC-005: Valid login
- TC-006: Invalid credentials

**Core Feature Testing (8 test cases)**:

- TC-007-014: Test your main features using EP, BVA, Decision Tables

**State Transitions (3 test cases)**:

- TC-015: Valid state transition
- TC-016: Invalid state transition
- TC-017: State persistence

**Error Handling (3 test cases)**:

- TC-018: Network error handling
- TC-019: Invalid input handling
- TC-020: Server error handling

#### 3.3 Decision Table Example

For **Shopping Cart Checkout**:

| User Logged In | Items in Cart | Valid Payment | Valid Address | **Action**            |
| -------------- | ------------- | ------------- | ------------- | --------------------- |
| Yes            | Yes           | Yes           | Yes           | ✅ Complete checkout  |
| Yes            | Yes           | Yes           | No            | ❌ Show address error |
| Yes            | Yes           | No            | Yes           | ❌ Show payment error |
| Yes            | No            | -             | -             | ❌ Cart empty error   |
| No             | -             | -             | -             | ❌ Redirect to login  |

Create test cases for each row.

#### 3.4 State Transition Diagram

Create diagram for **Order Status**:

```
[New] --place order--> [Pending]
                          |
                     validate payment
                          |
                          v
                     [Processing]
                          |
                      ship order
                          |
                          v
                      [Shipped]
                          |
                     confirm delivery
                          |
                          v
                     [Delivered]
```

Document test cases for each transition and invalid transitions.

---

### 4. Traceability Matrix (15 points)

Create `docs/milestones/M3/traceability-matrix.md`:

Map requirements → test cases:

| Requirement ID | Requirement       | Test Cases             | Coverage |
| -------------- | ----------------- | ---------------------- | -------- |
| FR-001         | User Registration | TC-001, TC-002, TC-003 | 100%     |
| FR-002         | User Login        | TC-005, TC-006         | 100%     |
| FR-003         | Password Reset    | TC-021, TC-022         | 100%     |
| FR-004         | Product Browsing  | TC-007, TC-008, TC-009 | 100%     |
| FR-005         | Add to Cart       | TC-010, TC-011         | 100%     |
| FR-006         | Checkout          | TC-012, TC-013, TC-014 | 100%     |
| ...            | ...               | ...                    | ...      |

**Goal**: 100% of high-priority requirements traced to test cases.

---

### 5. Test Data Management (10 points)

Create `tests/data/test-data.md`:

#### 5.1 Test Users

```json
{
  "valid_user": {
    "email": "testuser@example.com",
    "password": "ValidPass123!",
    "role": "user"
  },
  "admin_user": {
    "email": "admin@example.com",
    "password": "AdminPass123!",
    "role": "admin"
  },
  "invalid_users": [
    { "email": "invalid-email", "password": "short" },
    { "email": "missing@password.com", "password": "" },
    { "email": "", "password": "NoEmail123!" }
  ]
}
```

#### 5.2 Test Data Sets

Create CSV files for data-driven testing (preview for M7):

`tests/data/registration-valid.csv`:

```csv
email,password,expected_result
user1@example.com,ValidPass123!,success
user2@example.com,AnotherPass456!,success
```

`tests/data/registration-invalid.csv`:

```csv
email,password,expected_error
invalid-email,ValidPass123!,invalid_email_format
user@example.com,short,password_too_short
,ValidPass123!,email_required
```

---

## 📤 Submission Instructions

### 1. Create Pull Request

```bash
git checkout -b milestone-3-black-box
# Add all test documentation
git add docs/milestones/M3/ tests/data/
git commit -m "docs(testing): complete M3 black box test plan"
git push -u origin milestone-3-black-box
gh pr create --title "Milestone 3: Black Box Testing"
```

### 2. Required Files

```
docs/milestones/M3/
├── test-strategy.md
├── test-plan.md
├── test-cases.md
├── traceability-matrix.md
└── diagrams/
    ├── state-transition-order.png
    └── decision-table-checkout.png

tests/data/
├── test-data.md
├── registration-valid.csv
└── registration-invalid.csv
```

### 3. Submit on Canvas

- Pull Request URL
- Test Strategy document link
- Test Cases document link (20+ test cases)
- Traceability Matrix link

---

## 🎯 Grading Rubric

| Category                | Points | Criteria                                           |
| ----------------------- | ------ | -------------------------------------------------- |
| **Test Strategy**       | 25     | Comprehensive, clear scope, entry/exit criteria    |
| **Test Plan**           | 30     | Features identified, techniques mapped, priorities |
| **Test Cases**          | 40     | 20+ detailed cases, covers EP/BVA/DT/ST            |
| **Traceability Matrix** | 15     | Complete mapping, 100% high-priority coverage      |
| **Test Data**           | 10     | Well-organized, sufficient test data sets          |
| **Quality & Clarity**   | 10     | Professional documentation, clear diagrams         |

**Total**: 130 points (30% bonus available)

**Bonus Points**:

- +5: Decision tables for multiple features
- +5: State transition diagrams for multiple flows
- +10: 30+ test cases (50% more than required)
- +10: Automated test case management tool integration

**Deductions**:

- < 20 test cases: -5 points per missing case
- Missing technique (EP/BVA/DT/ST): -10 points each
- No traceability matrix: -15 points
- Poor documentation quality: -10 points

---

## ✅ Checklist

- [ ] Test strategy document complete
- [ ] Test plan identifies all features
- [ ] 20+ detailed test cases written
- [ ] EP technique applied (at least 5 cases)
- [ ] BVA technique applied (at least 5 cases)
- [ ] Decision Table created (at least 1 feature)
- [ ] State Transition diagram created (at least 1 flow)
- [ ] Traceability matrix links all requirements to test cases
- [ ] Test data organized and documented
- [ ] All diagrams clear and professional
- [ ] Documents reviewed by team members
- [ ] PR created and submitted

---

## 💡 Tips for Success

### Test Case Writing

1. **Be specific**: "User logs in" → "User enters valid email and password, clicks login button"
2. **Include expected results**: What should happen vs what did happen
3. **Make reproducible**: Anyone should be able to execute from your steps
4. **Cover happy and unhappy paths**: Don't just test valid inputs

### Equivalence Partitioning

- Identify input domains
- Divide into valid and invalid partitions
- Test one value from each partition
- Example: Age input → [-∞, 0], [1, 17], [18, 120], [121, +∞]

### Boundary Value Analysis

- Find boundaries between partitions
- Test: boundary-1, boundary, boundary+1
- Example: Max 100 items → Test with 99, 100, 101

### Decision Tables

- Identify all conditions
- List all possible combinations
- Reduce using rules (eliminate impossible combinations)
- Create test case for each column

### State Transitions

- Draw diagram first
- Test all valid transitions
- Test invalid transitions (should be rejected)
- Test state persistence (after restart)

### Common Mistakes

- ❌ Test cases too vague
- ❌ Only testing happy paths
- ❌ Not using BVA (testing only middle values)
- ❌ Missing expected results
- ❌ No traceability to requirements
- ❌ Incomplete decision tables

---

## 📚 Resources

- [Module 4: Black Box Testing Theory](../../04-black-box-testing/theory/)
- [Module 4: Exercises](../../04-black-box-testing/exercises/)
- [Test Case Template](../templates/test-case-template.md)

---

## ❓ FAQ

**Q: Do we execute these test cases now?**  
A: Not yet! M3 is design only. Execution happens in M4-M6 with automated tests.

**Q: Can we use test management tools?**  
A: Yes! Tools like TestRail, Zephyr, or even GitHub Issues are great. Bonus points!

**Q: How detailed should test cases be?**  
A: Detailed enough that another team member can execute them without asking questions.

**Q: Should we write test cases for incomplete features?**  
A: Yes! Design tests based on requirements. Implementation continues through M4.

**Q: What if we find issues while designing tests?**  
A: Great! Document them as bugs/issues. This is value of test planning.

**Q: Can we modify requirements from M1?**  
A: Minor refinements yes, major changes need instructor approval. Update traceability matrix.

---

**Good test planning prevents bugs and saves time later. Invest effort here!** 📋✅
