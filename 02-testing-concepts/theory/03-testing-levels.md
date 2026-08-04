# Software Testing Levels

## Overview

Testing levels describe **WHERE** in the system you're testing - from individual units to the complete system.

## The Test Pyramid

```
           /\
          /  \        Few, Slow, Expensive
         / UI \       End-to-End Tests
        /------\
       /        \
      / Service \     Some, Medium Speed
     /Integration\    API/Integration Tests
    /-------------\
   /               \
  /   Unit Tests    \ Many, Fast, Cheap
 /___________________\
```

**Key Principle**: More tests at the bottom, fewer at the top.

---

## Level 1: Unit Testing

### What

Test individual components in isolation (functions, methods, classes).

### Who

Developers

### When

During development (ideally before/during coding - TDD)

### Examples

```python
def add(a, b):
    return a + b

# Unit test
def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
```

### Characteristics

- ✅ Fast (milliseconds)
- ✅ Isolated (no dependencies)
- ✅ Many tests (hundreds/thousands)
- ✅ Run frequently
- ✅ Cheap to maintain

### Tools

- Python: pytest, unittest
- JavaScript: Jest, Mocha
- Java: JUnit

---

## Level 2: Integration Testing

### What

Test how components work together.

### Who

Developers, QA

### When

After unit testing

### Examples

```python
# Test database + service layer
def test_save_user():
    user = User("john@example.com")
    user_id = db.save(user)  # DB integration
    loaded = db.get(user_id)  # Verify
    assert loaded.email == "john@example.com"
```

### Types

- **Big Bang**: Integrate all at once
- **Incremental**: Add modules gradually
  - Top-down
  - Bottom-up
  - Sandwich

### Characteristics

- ⚠️ Slower than unit tests
- ⚠️ External dependencies (DB, APIs)
- ⚠️ Fewer tests than unit
- ⚠️ More complex setup

---

## Level 3: System Testing

### What

Test complete, integrated system end-to-end.

### Who

QA team

### When

After integration testing

### Examples

```
User Journey: Purchase Product
1. Browse catalog
2. Search for item
3. Add to cart
4. Enter shipping info
5. Enter payment
6. Confirm order
7. Receive email confirmation

Test: Complete flow works
```

### Includes

- Functional system testing
- Non-functional system testing
  - Performance
  - Security
  - Usability

### Characteristics

- ⏱️ Slow (minutes per test)
- 🌐 Full environment needed
- 📝 Fewer tests (dozens)
- 💰 Expensive to maintain

---

## Level 4: Acceptance Testing

### What

Verify system meets business requirements and user needs.

### Who

End users, Business stakeholders, QA

### When

Before deployment

### Types

**User Acceptance Testing (UAT)**

- Real users test
- In real-world scenarios
- Final validation

**Business Acceptance Testing (BAT)**

- Business validates
- Meets business goals
- Ready for release

**Alpha Testing**

- Internal users
- Developer's site
- Controlled environment

**Beta Testing**

- External users
- User's site
- Real-world conditions

### Example

```
E-commerce UAT:
- 10 beta users
- Complete 5 purchases each
- Provide feedback
- Report bugs
- Rate experience

Acceptance Criteria:
✓ 90%+ successful checkouts
✓ < 5 critical bugs
✓ 4/5 average rating
```

---

## Comparison Matrix

| **Level**   | **Scope** | **Speed** | **Quantity** | **Cost** | **Who** |
| ----------- | --------- | --------- | ------------ | -------- | ------- |
| Unit        | Function  | Fast      | 1000s        | Low      | Devs    |
| Integration | Modules   | Medium    | 100s         | Medium   | Devs/QA |
| System      | Complete  | Slow      | 10s          | High     | QA      |
| Acceptance  | Business  | Slowest   | Few          | Highest  | Users   |

---

## When to Use Each Level

### Unit Tests When:

- Testing business logic
- Testing algorithms
- Testing utilities
- Rapid feedback needed

### Integration Tests When:

- Testing API endpoints
- Testing database interactions
- Testing external services
- Testing module communication

### System Tests When:

- Testing complete workflows
- Testing user journeys
- Testing cross-system features
- Verifying requirements

### Acceptance Tests When:

- Validating user needs
- Getting stakeholder approval
- Pre-release verification
- Business validation

---

## The Testing Pyramid in Practice

### Good Balance

```
Acceptance: 5 tests
System: 20 tests
Integration: 100 tests
Unit: 1000 tests
```

### Anti-Pattern: Ice Cream Cone

```
Manual Testing: Most tests (Bad!)
UI Tests: Many
Integration: Some
Unit: Few
```

### Anti-Pattern: Hourglass

```
UI Tests: Many (Slow!)
Integration: Few (Gap!)
Unit: Many
```

---

## Coverage at Each Level

### Unit Tests Cover

- ✅ Business logic
- ✅ Edge cases
- ✅ Error conditions
- ✅ Algorithms
- ❌ Integration issues
- ❌ UI behavior

### Integration Tests Cover

- ✅ Component communication
- ✅ Data flow
- ✅ API contracts
- ✅ Database operations
- ❌ Complete workflows
- ❌ User experience

### System Tests Cover

- ✅ End-to-end flows
- ✅ User journeys
- ✅ Cross-system features
- ✅ Non-functional requirements
- ❌ Every code path
- ❌ All edge cases

### Acceptance Tests Cover

- ✅ Business requirements
- ✅ User needs
- ✅ Real-world scenarios
- ❌ Technical details

---

## Key Takeaways

1. **Test at all levels** - Each catches different bugs
2. **More at bottom** - Unit tests are foundation
3. **Fewer at top** - System tests are expensive
4. **Balance is key** - Follow the pyramid
5. **Each level has purpose** - Don't skip levels

Next: [Testing Principles](./04-testing-principles.md)
