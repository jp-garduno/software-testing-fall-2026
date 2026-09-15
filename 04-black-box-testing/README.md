# Module 4: Black Box Testing

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Design effective test cases using systematic techniques
- Apply equivalence partitioning to reduce test cases
- Use boundary value analysis to find edge case bugs
- Create decision tables for complex business logic
- Design state transition tests for stateful systems
- Choose the appropriate black box technique for different scenarios

## 📚 Theory Materials

### [1. How to Design Test Cases](./theory/01-test-case-design.md)

- What makes a good test case
- Test case structure and components
- Writing clear test steps
- Expected vs actual results
- Test case management

### [2. Equivalence Partitioning](./theory/02-equivalence-partitioning.md)

- Understanding equivalence classes
- Valid and invalid partitions
- Reducing test cases systematically
- Examples and practice problems

### [3. Boundary Value Analysis](./theory/03-boundary-value-analysis.md)

- Why boundaries matter
- Identifying boundaries in requirements
- Testing at, below, and above boundaries
- Combining with equivalence partitioning

### [4. Decision Tables](./theory/04-decision-tables.md)

- When to use decision tables
- Creating complete decision tables
- Reducing redundant rules
- Testing complex business rules

### [5. State Transition Testing](./theory/05-state-transition.md)

- Understanding state machines
- State transition diagrams
- Valid and invalid transitions
- Coverage criteria for state testing

## 🎥 Video Resources

- **Black Box Testing Overview** (15 min): Introduction to specification-based testing
- **Equivalence Partitioning in Action** (20 min): Step-by-step examples
- **Boundary Value Analysis** (25 min): Finding bugs at the edges
- **Decision Tables Deep Dive** (30 min): Complex business logic testing
- **State Transition Testing** (25 min): Testing stateful systems

**Note**: Video links will be provided in the LMS.

## 💻 Practical Exercises

All exercises include scenarios for both Python and JavaScript/TypeScript implementation.

### [Exercise 1: Test Case Writing](./exercises/01-test-case-writing.md)

Practice writing clear, comprehensive test cases for given requirements.

### [Exercise 2: Equivalence Partitioning](./exercises/02-equivalence-partitioning.md)

**Scenarios**:

1. Credit card validation function
2. Date validation function
3. Flight booking eligibility checker
4. URL validation function

### [Exercise 3: Boundary Value Analysis](./exercises/03-boundary-value-analysis.md)

**Scenarios**:

1. Loan eligibility calculator (income and credit score)
2. E-commerce product categorization (price ranges)
3. Shipping cost calculator (weight and dimensions)

### [Exercise 4: Decision Tables](./exercises/04-decision-tables.md)

**Scenarios**:

1. Weather advisory system (temperature and humidity)
2. User authentication system (username and password rules)
3. Insurance premium calculator (age, coverage, and history)

### [Exercise 5: State Transition](./exercises/05-state-transition.md)

**Scenarios**:

1. Order processing system (New → Confirmed → Shipped → Delivered)
2. User account states (Active, Suspended, Locked, Deleted)
3. Traffic light controller

### [Exercise 6: Comprehensive Challenge](./exercises/06-comprehensive.md)

Apply multiple techniques to a complex system (Shopping cart with discounts, shipping, and payment processing).

## 📝 In-Class Exercises

For instructor-led sessions, enhanced and expanded:

### [In-Class Exercise Set](./exercises/in-class-exercises.md)

**Session 1: Equivalence Partitioning & BVA**

1. Number classifier (positive/negative/zero)
2. Password validator with multiple rules
3. Purchase discount calculator
4. E-commerce order processor

**Session 2: Decision Tables & State Transition** 5. Shipping cost calculator (weight and method) 6. ATM state machine 7. Elevator control system

## 📝 Homework Assignment

**[Homework 4: Black Box Test Design](./homework/homework-4.md)**

**Due**: End of Week 5

**Objectives**:

- Design comprehensive test cases using all black box techniques
- Implement test cases in Python and JavaScript
- Document your testing approach
- Achieve thorough specification coverage

**Deliverables**:

- Test design document with equivalence classes, boundaries, decision tables, and state diagrams
- Implemented test cases in both Python (pytest) and JavaScript (Jest)
- Test execution report
- GitHub repository with all code and documentation

**Grading Rubric**: See homework file for details.

## 🛠️ Tools & Frameworks

### Python

- **Testing Framework**: pytest
- **Installation**:
  ```bash
  pip install pytest pytest-cov
  ```
- **Running Tests**:
  ```bash
  pytest test_*.py -v
  ```

### JavaScript/TypeScript

- **Testing Framework**: Jest
- **Installation**:
  ```bash
  npm install --save-dev jest @types/jest
  ```
- **Running Tests**:
  ```bash
  npm test
  ```

## 📊 Black Box Testing Techniques Comparison

| **Technique**                | **Best For**           | **Strengths**             | **Limitations**          |
| ---------------------------- | ---------------------- | ------------------------- | ------------------------ |
| **Equivalence Partitioning** | Input validation       | Reduces test cases        | May miss edge cases      |
| **Boundary Value Analysis**  | Numeric ranges         | Finds edge case bugs      | Only for ordered data    |
| **Decision Tables**          | Complex business rules | Ensures complete coverage | Can become large         |
| **State Transition**         | Stateful systems       | Tests all state changes   | Requires state knowledge |

## 🎯 When to Use Each Technique

```
┌─────────────────────────────────────────────────┐
│          Your Testing Scenario                  │
└─────────────────────────────────────────────────┘
                      ↓
       ┌──────────────┴──────────────┐
       │  What are you testing?      │
       └──────────────┬──────────────┘
                      ↓
    ┌─────────────────┼─────────────────┐
    ↓                 ↓                  ↓
Input values?    Business logic?    State changes?
    ↓                 ↓                  ↓
    │                 │                  │
    ├─ Numbers? → BVA │                  │
    ├─ Categories? → EP                  │
    └─ Ranges? → EP+BVA                  │
                      ↓                  ↓
            Multiple conditions?    State machine?
                      ↓                  ↓
              Decision Tables      State Transition
```

## 📖 Real-World Applications

### Example 1: E-Commerce Checkout

- **EP**: Discount codes (valid/invalid/expired)
- **BVA**: Quantity limits (min/max items)
- **Decision Table**: Shipping cost (location, weight, speed)
- **State Transition**: Order status workflow

### Example 2: Banking Application

- **EP**: Account types (savings/checking/credit)
- **BVA**: Transfer amounts (min/max limits)
- **Decision Table**: Transaction approval rules
- **State Transition**: Account states (active/frozen/closed)

### Example 3: Form Validation

- **EP**: Email format validation
- **BVA**: Password length requirements
- **Decision Table**: Field combination validation
- **State Transition**: Form submission states

## ❓ Common Questions

**Q: Should I always use all techniques?**
A: No. Choose based on what you're testing. Simple input validation might only need EP/BVA.

**Q: How many test cases is enough?**
A: Enough to cover all equivalence classes, critical boundaries, all decision table rules, and major state transitions. Quality over quantity.

**Q: Can I combine techniques?**
A: Yes! EP and BVA work great together. Use multiple techniques for comprehensive coverage.

**Q: What if requirements are unclear?**
A: Document assumptions, ask questions, and design tests based on expected behavior. Black box testing can reveal requirement gaps.

**Q: How is this different from white box testing?**
A: Black box tests specifications/requirements without knowing internal code. White box tests internal structure/logic.

## 🎯 Self-Assessment Checklist

Before moving to Module 5, make sure you can:

- [ ] Identify equivalence classes from requirements
- [ ] Apply boundary value analysis to numeric inputs
- [ ] Create complete decision tables
- [ ] Design state transition diagrams
- [ ] Write clear, testable test cases
- [ ] Choose appropriate techniques for different scenarios
- [ ] Implement black box tests in Python and JavaScript
- [ ] Calculate specification coverage

## 🔗 Connections to Other Modules

- **Module 2 (Testing Concepts)**: Black box is functional testing at various levels
- **Module 3 (Static Testing)**: Can find issues before dynamic testing
- **Module 5 (White Box)**: Complementary approach focusing on code structure
- **Module 6 (TDD)**: Black box thinking helps write tests first
- **Module 8 (System Testing)**: Black box techniques apply to E2E scenarios

## 📚 Additional Resources

### Required Reading

- ISTQB Foundation Syllabus - Section 4 (Test Techniques)
- "Black Box Testing" by Boris Beizer (selected chapters)

### Recommended Resources

- [Test Design Techniques](https://www.guru99.com/test-case-design-techniques.html)
- [Equivalence Partitioning Examples](https://www.softwaretestinghelp.com/equivalence-partitioning-testing/)
- [BVA Tutorial](https://www.softwaretestinghelp.com/boundary-value-analysis-testing/)

### Practice Problems

- [TryQA Practice Problems](https://tryqa.com/what-is-boundary-value-analysis-and-equivalence-partitioning/)
- Additional exercises in the [exercises](./exercises/) folder

## 🚀 Next Steps

Once you complete this module:

1. Complete all [exercises](./exercises/) - practice makes perfect!
2. Complete [Homework 4](./homework/homework-4.md)
3. Review for **Exam 1** (Week 6) covering Modules 1-3
4. Preview [Module 5: White Box Testing](../05-white-box-testing/README.md)

---

**Remember**: Black box testing is about testing WHAT the software does, not HOW it does it. Think like a user, not a developer! 🎯
