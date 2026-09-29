# Test Case Template

Use this template for writing detailed test cases (Milestone 3).

---

## TC-XXX: [Test Case Title]

**Feature**: [Feature Name] (F-XXX)  
**Test Technique**: [EP / BVA / Decision Table / State Transition]  
**Priority**: [High / Medium / Low]  
**Module**: [Module name]

### Preconditions

List any conditions that must be true before executing this test:

- [ ] Precondition 1 (e.g., User is logged in)
- [ ] Precondition 2 (e.g., Database has test data)
- [ ] Precondition 3 (e.g., Feature flag enabled)

### Test Data

| Field           | Value   | Notes                |
| --------------- | ------- | -------------------- |
| Input 1         | [value] | [why this value]     |
| Input 2         | [value] | [why this value]     |
| Expected Output | [value] | [what should happen] |

### Test Steps

| Step | Action                         | Expected Result             |
| ---- | ------------------------------ | --------------------------- |
| 1    | Navigate to [page/endpoint]    | [Page loads / API responds] |
| 2    | Enter [data] in [field]        | [Field accepts input]       |
| 3    | Click [button] / Submit [form] | [Action triggers]           |
| 4    | Observe [result]               | [Expected behavior occurs]  |
| 5    | Verify [condition]             | [Condition is true]         |

### Expected Result

**Primary Outcome**:

- [Main expected result]

**Secondary Outcomes**:

- [Side effect 1]
- [Side effect 2]
- [Data persisted correctly]
- [UI updated properly]

### Actual Result

**Status**: [Not Executed / Pass / Fail / Blocked]  
**Executed By**: [Name]  
**Date**: [YYYY-MM-DD]  
**Environment**: [Dev / Test / Staging]

**Result Description**:

- [What actually happened when test was executed]
- [Any deviations from expected results]

### Pass/Fail Criteria

**Pass if**:

- All expected results are observed
- No errors or unexpected behavior
- Data validated correctly

**Fail if**:

- Any expected result is missing
- Error occurs
- Unexpected behavior

### Notes / Comments

- [Any additional observations]
- [Related test cases: TC-XXX, TC-XXY]
- [Known issues: BUG-XXX]
- [Environment-specific notes]

### Test Evidence

- [ ] Screenshot attached: [filename.png]
- [ ] Log file saved: [logfile.log]
- [ ] Database state verified
- [ ] API response captured

---

## Example: Real Test Case

### TC-001: User Registration with Valid Data

**Feature**: User Registration (F-001)  
**Test Technique**: Equivalence Partitioning  
**Priority**: High  
**Module**: Authentication

#### Preconditions

- [ ] Application is running
- [ ] Database is accessible
- [ ] Email server is configured (for verification)

#### Test Data

| Field            | Value               | Notes                                  |
| ---------------- | ------------------- | -------------------------------------- |
| Email            | newuser@example.com | Valid email format, not yet registered |
| Password         | ValidPass123!       | Meets password requirements            |
| Confirm Password | ValidPass123!       | Matches password field                 |
| Expected Status  | 201 Created         | Successful registration                |

#### Test Steps

| Step | Action                                     | Expected Result                         |
| ---- | ------------------------------------------ | --------------------------------------- |
| 1    | Navigate to `/register`                    | Registration form displayed             |
| 2    | Enter `newuser@example.com` in email field | Email field accepts input               |
| 3    | Enter `ValidPass123!` in password field    | Password field accepts input (masked)   |
| 4    | Enter `ValidPass123!` in confirm field     | Confirm field accepts input (masked)    |
| 5    | Click "Register" button                    | Form submits, loading indicator shows   |
| 6    | Wait for response                          | Success message appears                 |
| 7    | Verify redirect to dashboard               | User redirected to `/dashboard`         |
| 8    | Check database for new user                | User record exists with hashed password |

#### Expected Result

**Primary Outcome**:

- User account created successfully
- HTTP status 201 Created
- User redirected to dashboard
- Welcome message displayed

**Secondary Outcomes**:

- Verification email sent to user
- Password is hashed (not stored as plain text)
- User ID assigned
- Created timestamp recorded

#### Actual Result

**Status**: Pass ✅  
**Executed By**: Jane Doe  
**Date**: 2026-10-15  
**Environment**: Test

**Result Description**:

- User registration completed successfully
- All expected results were observed
- Verification email received within 30 seconds
- Database shows hashed password (bcrypt)

#### Pass/Fail Criteria

**Pass if**:

- User account created in database
- Status code is 201
- Redirect to dashboard occurs
- No error messages
- Email sent

**Fail if**:

- Account not created
- Error message displayed
- Password stored in plain text
- No redirect

#### Notes / Comments

- Test executed on Chrome 118.0
- Email verification tested separately (TC-002)
- Related to TC-002 (email verification), TC-005 (login)
- Performance: Registration took 0.8 seconds

#### Test Evidence

- [x] Screenshot attached: tc-001-success-message.png
- [x] Database query result saved
- [x] Email inbox screenshot: verification-email.png

---

## Tips for Writing Good Test Cases

1. **Be specific**: Don't say "enter data", say "enter 'test@example.com'"
2. **One test case = one scenario**: Don't combine multiple behaviors
3. **Make it reproducible**: Anyone should be able to execute from your steps
4. **Include all data**: Test data, expected results, preconditions
5. **Think negative**: Include invalid inputs and error scenarios
6. **Update status**: Keep actual results current

## Common Mistakes

- ❌ Vague steps: "Test login" → ✅ "Enter 'user@example.com' in email field"
- ❌ Multiple tests in one case → ✅ Split into separate test cases
- ❌ Missing preconditions → ✅ List all required setup
- ❌ No expected result → ✅ Clearly state what should happen
- ❌ Not updating status → ✅ Mark as Pass/Fail after execution

---

**Use this template for Milestone 3: Black Box Testing**
