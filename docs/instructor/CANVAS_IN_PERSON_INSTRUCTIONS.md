# Canvas Instructions - In-Person Weeks 4-16

**Purpose**: Copy these instructions into Canvas for each session during the in-person period.

---

## Week 4: Black Box Testing

### 📅 Session 1: Equivalence Partitioning & Boundary Value Analysis (2 hours)

**Canvas Module Title**: Week 4 - Session 1: Black Box Testing Fundamentals

**Instructions to post in Canvas**:

---

#### Welcome Back! 🎉

This week marks the start of our in-person sessions. We'll dive into **Black Box Testing** - testing from the user's perspective without looking at the code.

#### 📚 Pre-Class Preparation (Complete BEFORE class)

**Required Reading** (1 hour):

1. **[01-introduction.md](../../04-black-box-testing/theory/01-introduction.md)**

   - What is black box testing?
   - When to use it
   - Advantages and limitations

2. **[02-equivalence-partitioning.md](../../04-black-box-testing/theory/02-equivalence-partitioning.md)**

   - EP concepts and examples
   - How to identify partitions

3. **[03-boundary-value-analysis.md](../../04-black-box-testing/theory/03-boundary-value-analysis.md)**
   - BVA technique
   - Finding boundaries
   - Edge cases

**Bring to Class**:

- Your laptop with development environment set up
- Questions about the readings
- Examples of software you've tested as a user

#### 🎯 In-Class Activities

**Part 1: Lecture - Equivalence Partitioning (45 min)**

Topics covered:

- Real-world examples of EP
- How to identify valid/invalid partitions
- Reducing test cases while maintaining coverage
- Common mistakes in EP

**Part 2: Hands-On Exercise - EP (30 min)**

Complete together in class:

- **[01-ep-registration.md](../../04-black-box-testing/exercises/01-ep-registration.md)**

You'll design test cases for a user registration form using EP.

**Part 3: Lecture - Boundary Value Analysis (30 min)**

Topics covered:

- Why boundaries matter (off-by-one errors)
- Identifying boundaries in requirements
- Testing at, above, and below boundaries
- Combining BVA with EP

**Part 4: Hands-On Exercise - BVA (15 min)**

Complete together in class:

- **[02-bva-age-validator.md](../../04-black-box-testing/exercises/02-bva-age-validator.md)**

Design boundary value test cases for an age validation function.

#### 💬 Discussion Questions

1. Can you think of bugs you've encountered that BVA would have caught?
2. How do you decide which technique (EP vs BVA) to use?
3. What's the minimum number of test cases needed for thorough coverage?

#### 📝 Post-Class Work

1. Review today's exercises and solutions
2. Start thinking about Milestone 1 (Project Proposal due this week!)
3. Begin reading theory for Session 2

#### 📚 Resources

- [Black Box Testing Theory](../../04-black-box-testing/theory/)
- [Testing Guidelines](../../team-project/guidelines/testing-guidelines.md)
- [ISTQB Foundation Level Syllabus](https://www.istqb.org/)

---

### 📅 Session 2: Decision Tables & State Transition Testing (2 hours)

**Canvas Module Title**: Week 4 - Session 2: Advanced Black Box Techniques

**Instructions to post in Canvas**:

---

#### Session 2 Focus 🎯

Building on EP and BVA, today we'll learn two powerful techniques for complex logic and stateful systems.

#### 📚 Pre-Class Preparation (Complete BEFORE class)

**Required Reading** (1 hour):

1. **[04-decision-tables.md](../../04-black-box-testing/theory/04-decision-tables.md)**

   - When to use decision tables
   - Building decision tables
   - Reducing redundant test cases

2. **[05-state-transition.md](../../04-black-box-testing/theory/05-state-transition.md)**
   - State machines in testing
   - Creating state diagrams
   - Testing all transitions

**Review**:

- Your project ideas for Milestone 1

#### 🎯 In-Class Activities

**Part 1: Lecture - Decision Tables (45 min)**

Topics covered:

- Business rules and complex logic
- Building decision tables step-by-step
- Identifying redundant rules
- Real-world examples (loan approval, discount calculation)

**Part 2: Hands-On Exercise - Decision Tables (30 min)**

Complete together in class:

- **[03-decision-table-discount.md](../../04-black-box-testing/exercises/03-decision-table-discount.md)**

Design test cases for a complex discount system using decision tables.

**Part 3: Lecture - State Transition Testing (30 min)**

Topics covered:

- Systems with states (user sessions, workflows)
- Drawing state diagrams
- Testing valid and invalid transitions
- Coverage criteria for state-based testing

**Part 4: Hands-On Exercise - State Transitions (15 min)**

Complete together in class:

- **[04-state-transition-atm.md](../../04-black-box-testing/exercises/04-state-transition-atm.md)**

Model an ATM withdrawal flow and design transition tests.

#### 💬 Discussion Questions

1. When would you choose decision tables over other techniques?
2. How do you handle systems with many states?
3. Can you identify state machines in your team project?

#### 📝 Post-Class Work

1. **DUE THIS WEEK**: Milestone 1 - Project Proposal

   - Team formation
   - Project selection
   - Requirements specification
   - Submit on Canvas

2. Start Homework 4 (due Week 9)
   - Black box test case design for online banking system
   - Use all 4 techniques learned this week

#### 🎯 Milestone 1 Reminder

**Due**: End of this week  
**Deliverables**:

- Team roster and roles
- Project description
- Requirements specification
- Architecture diagram
- Technology stack
- Timeline

See: [milestone-1-proposal.md](../../team-project/milestones/milestone-1-proposal.md)

---

## Week 5: Black Box Testing Deep Dive

### 📅 Session 1: Test Case Design Workshop (2 hours)

**Canvas Module Title**: Week 5 - Session 1: Black Box Test Design Practice

**Instructions to post in Canvas**:

---

#### Workshop Focus 🛠️

Today is all about practice! We'll apply all four black box techniques to real-world scenarios.

#### 📚 Pre-Class Preparation

**Optional Review**:

- Revisit Week 4 theory documents
- Look at your Milestone 1 project requirements
- Think about test scenarios for your project

#### 🎯 In-Class Activities

**Part 1: Case Study - E-Commerce Checkout (60 min)**

Working in teams of 2-3:

**Scenario**: Design comprehensive test cases for an e-commerce checkout flow.

Requirements provided:

- Shopping cart with multiple items
- Discount codes (percentage and fixed amount)
- Shipping options (standard, express, overnight)
- Payment methods (credit card, PayPal, gift card)
- Tax calculation based on location

**Your task**:

1. Identify equivalence partitions (15 min)
2. Determine boundary values (15 min)
3. Create decision table for discount rules (15 min)
4. Draw state diagram for checkout flow (15 min)

**Part 2: Team Presentations (30 min)**

- 3-4 teams present their test designs
- Class feedback and discussion
- Instructor highlights best practices

**Part 3: Homework 4 Introduction (30 min)**

Review Homework 4 requirements:

- Online Banking System test case design
- Minimum 20 test cases required
- Use all 4 techniques
- Due Week 9
- Worth 110 points

Walk through the requirements together and answer questions.

#### 💬 Discussion Questions

1. Which technique was most useful for the checkout scenario?
2. How many test cases did you create? Could you reduce that number?
3. What edge cases did you identify?

#### 📝 Post-Class Work

1. Continue working on Homework 4
2. Apply black box techniques to your team project
3. Prepare for Exam 1 review (next week!)

---

### 📅 Session 2: Black Box Testing Best Practices (2 hours)

**Canvas Module Title**: Week 5 - Session 2: Test Case Quality & Documentation

**Instructions to post in Canvas**:

---

#### Session Focus 📝

Learn how to write high-quality test cases that others can understand and execute.

#### 📚 Pre-Class Preparation

**Bring to Class**:

- Your draft test cases from Homework 4
- Questions about test case documentation

#### 🎯 In-Class Activities

**Part 1: Lecture - Test Case Quality (45 min)**

Topics covered:

- Characteristics of good test cases (clear, concise, repeatable)
- Test case templates and standards
- Writing test steps vs expected results
- Traceability to requirements
- Test case reviews

**Part 2: Peer Review Exercise (45 min)**

**Activity**: Test Case Review Workshop

1. Pair up with another student (15 min)
2. Exchange your draft Homework 4 test cases
3. Review each other's work using checklist:
   - Are test cases clear and unambiguous?
   - Can you execute them without asking questions?
   - Are expected results specific?
   - Is coverage adequate?
4. Provide written feedback

**Part 3: Exam 1 Review (30 min)**

**Next Week: Exam 1** (Modules 1-3: Git, Testing Concepts, Static Testing)

Review topics:

- Git commands and workflows
- Branching and merging
- Testing types and levels
- Static testing techniques
- Pre-commit hooks
- Conventional commits

**Exam Format**:

- Practical hands-on exam (not multiple choice)
- 2 hours in class
- You'll use your laptop
- Open resources (course materials, documentation)
- No collaboration

#### 💬 Discussion Questions

1. What makes a test case "good"?
2. How do you balance detail vs brevity in test cases?
3. Should test cases include actual test data or just examples?

#### 📝 Post-Class Work

1. **Study for Exam 1** - Focus on:

   - Git operations (branching, merging, conflicts)
   - Setting up pre-commit hooks
   - Linting configuration
   - Conventional commit format

2. **Homework 2 Due This Week**

   - Testing analysis report
   - Submit on Canvas

3. Continue Homework 4 (due Week 9)

#### 📚 Exam 1 Study Resources

- [Module 1: Git Theory](../../01-git/theory/)
- [Module 2: Testing Concepts](../../02-testing-concepts/theory/)
- [Module 3: Static Testing](../../03-static-testing/theory/)
- Review all exercises from Modules 1-3
- Practice setting up pre-commit hooks
- Review your Homework 1, 2, 3 solutions

---

## Week 6: Exam 1 Week

### 📅 Session 1: Exam 1 Review Session (2 hours)

**Canvas Module Title**: Week 6 - Session 1: Exam 1 Review

**Instructions to post in Canvas**:

---

#### Review Session 📚

Today's session is dedicated to reviewing for Exam 1. Come with questions!

#### 🎯 Session Structure

**Part 1: Q&A Session (60 min)**

Open floor for any questions about Modules 1-3:

- Git workflows and commands
- Testing concepts and principles
- Static testing setup
- Pre-commit hooks
- Linting tools

**Part 2: Hands-On Practice (60 min)**

Work through practice problems:

1. **Git Exercise** (20 min)

   - Create repository
   - Make commits with conventional commits
   - Create branches
   - Resolve a mock merge conflict

2. **Pre-commit Setup** (20 min)

   - Install pre-commit framework
   - Configure hooks for Python project
   - Test hook execution
   - Fix linting issues

3. **Testing Concepts** (20 min)
   - Identify testing type for scenarios
   - Apply testing principles
   - Design a test strategy

#### 💬 Study Tips

**Git (Module 1)**:

- Practice creating branches and merging
- Know how to resolve conflicts
- Understand pull request workflow
- Be familiar with git log, git diff, git status

**Testing Concepts (Module 2)**:

- Know testing types (functional vs non-functional)
- Understand testing levels (unit, integration, system, acceptance)
- Remember the 7 testing principles
- Understand the testing pyramid

**Static Testing (Module 3)**:

- Conventional commit format (type, scope, description)
- Pre-commit hook configuration
- Linting tools (Black, isort, Pylint, ESLint, Prettier)
- Benefits of static testing

#### 📝 Exam 1 Details

**When**: Session 2 (next class)  
**Duration**: 2 hours  
**Coverage**: Modules 1-3  
**Format**: Practical hands-on tasks  
**Weight**: 15% of final grade

**What to Bring**:

- Your laptop (fully charged!)
- Development environment set up
- Git installed and configured
- Python and Node.js installed

**Allowed**:

- Course materials (GitHub repository)
- Official documentation websites
- Your own notes

**Not Allowed**:

- Collaboration with other students
- Copying code from others
- Asking for help during exam

#### 🎯 Last-Minute Prep

**Tonight**:

1. Review all Module 1-3 theory documents
2. Practice git commands in terminal
3. Set up a test repository with pre-commit hooks
4. Review your homework solutions
5. Get good sleep!

**Before Exam**:

- Verify your laptop works
- Test your development environment
- Have backup plan (power adapter, internet access)

#### 📝 Post-Session Work

**Study tonight!** Exam tomorrow in Session 2.

---

### 📅 Session 2: **EXAM 1** 🎯 (2 hours)

**Canvas Module Title**: Week 6 - Session 2: Exam 1 (Modules 1-3)

**Instructions to post in Canvas**:

---

#### Exam 1: Practical Assessment

**Duration**: 2 hours  
**Coverage**: Modules 1-3 (Git, Testing Concepts, Static Testing)  
**Weight**: 15% of final grade

#### 📋 Exam Format

You will receive a separate exam document at the start of class with detailed instructions.

**Typical exam structure** (example):

**Part 1: Git Operations** (30%)

- Create repository with specific structure
- Make commits following conventional commit standard
- Create feature branch
- Resolve merge conflict
- Create pull request

**Part 2: Static Testing Setup** (40%)

- Configure pre-commit hooks for provided project
- Set up linting tools (Black, Pylint for Python OR ESLint, Prettier for JavaScript)
- Fix linting issues in provided code
- Verify hooks work correctly

**Part 3: Testing Concepts** (30%)

- Analyze requirements and identify test types needed
- Design test strategy for given scenario
- Apply testing principles
- Answer scenario-based questions

#### ✅ Before You Begin

- [ ] Laptop fully charged
- [ ] Git configured with your name/email
- [ ] Python 3.11+ OR Node.js 22+ installed
- [ ] Text editor ready (VS Code recommended)
- [ ] Stable internet connection
- [ ] Exam document downloaded from Canvas

#### 📤 Submission Instructions

1. Create repository as instructed in exam
2. Push all work to GitHub
3. Submit repository URL on Canvas
4. Submit before end of class time
5. No late submissions accepted

#### 🚫 Academic Integrity

- This is an individual exam
- No collaboration with other students
- You may use course materials and documentation
- Do not share your work or exam details
- Violations will result in a zero

#### ⏱️ Time Management

- Read all instructions first (5 min)
- Allocate time per section (Part 1: 35 min, Part 2: 50 min, Part 3: 30 min)
- Save time for testing and submission (10 min)
- Don't get stuck - move on and come back

#### 📝 After Exam

**Relax! You've earned it.** 🎉

Next week we start White Box Testing (Module 5).

**Don't forget**:

- **Milestone 2 due this week** - Foundation & Git Setup
- Start preparing for Module 5

---

## Week 7: White Box Testing Introduction

### 📅 Session 1: Code Coverage & Unit Testing (2 hours)

**Canvas Module Title**: Week 7 - Session 1: White Box Testing Fundamentals

**Instructions to post in Canvas**:

---

#### Welcome to White Box Testing! 🔍

Unlike black box testing, we now look **inside** the code to design tests. This week focuses on unit testing and code coverage.

#### 📚 Pre-Class Preparation (Complete BEFORE class)

**Required Reading** (1.5 hours):

1. **[01-introduction.md](../../05-white-box-testing/theory/01-introduction.md)**

   - White box vs black box
   - Structural testing
   - When to use white box techniques

2. **[02-statement-coverage.md](../../05-white-box-testing/theory/02-statement-coverage.md)**

   - Statement coverage metrics
   - How to achieve 100% statement coverage
   - Limitations

3. **[03-branch-coverage.md](../../05-white-box-testing/theory/03-branch-coverage.md)**
   - Branch coverage vs statement coverage
   - Testing all decision paths
   - Coverage tools

**Setup**:

- Ensure pytest (Python) OR Jest (JavaScript) is installed
- Have a code editor ready

#### 🎯 In-Class Activities

**Part 1: Lecture - Code Coverage (45 min)**

Topics covered:

- Statement coverage
- Branch coverage
- Path coverage
- Condition coverage
- Coverage tools (pytest-cov, Jest coverage)
- Interpreting coverage reports
- Coverage goals (when is 100% necessary?)

**Part 2: Hands-On - Coverage Exercise (30 min)**

Choose your language:

**Python Track**:

- **[01-calculator-coverage.md](../../05-white-box-testing/exercises/python/01-calculator-coverage.md)**

**JavaScript Track**:

- **[01-calculator-coverage.md](../../05-white-box-testing/exercises/javascript/01-calculator-coverage.md)**

**Activity**:

1. Analyze provided calculator code
2. Run initial tests and check coverage
3. Add tests to increase coverage to 100%
4. Generate HTML coverage report

**Part 3: Lecture - Unit Testing Best Practices (30 min)**

Topics covered:

- AAA pattern (Arrange-Act-Assert)
- Test naming conventions
- Test independence
- Test fixtures and setup
- Parametrized tests
- What to unit test vs what to skip

**Part 4: Live Coding - Unit Tests (15 min)**

Instructor demonstrates:

- Writing unit tests from scratch
- Using fixtures
- Parametrized testing
- Checking coverage as you go

#### 💬 Discussion Questions

1. Is 100% code coverage always necessary?
2. Can you have 100% coverage but still have bugs?
3. How do you decide what to unit test?

#### 📝 Post-Class Work

1. **Homework 3 Due This Week**

   - Static testing setup
   - Submit on Canvas

2. Complete the coverage exercise for your chosen language

3. Start thinking about Milestone 3 (due Week 8)

#### 📚 Resources

- [pytest documentation](https://docs.pytest.org/)
- [Jest documentation](https://jestjs.io/)
- [Testing Guidelines](../../team-project/guidelines/testing-guidelines.md)

---

### 📅 Session 2: Integration Testing & Mocking (2 hours)

**Canvas Module Title**: Week 7 - Session 2: Integration Testing & Mocking

**Instructions to post in Canvas**:

---

#### Beyond Unit Tests 🔗

Today we move from testing isolated units to testing how components work together, and learn when to use mocks.

#### 📚 Pre-Class Preparation (Complete BEFORE class)

**Required Reading** (1 hour):

1. **[04-integration-testing.md](../../05-white-box-testing/theory/04-integration-testing.md)**

   - Unit vs integration tests
   - Integration test strategies
   - Test doubles

2. **[05-mocking.md](../../05-white-box-testing/theory/05-mocking.md)**
   - When to mock
   - Mock vs stub vs spy vs fake
   - unittest.mock (Python) or Jest mocks (JavaScript)

#### 🎯 In-Class Activities

**Part 1: Lecture - Integration Testing (40 min)**

Topics covered:

- What is integration testing?
- API testing with real databases
- Test database setup and teardown
- Integration test patterns
- How much to integration test

**Part 2: Hands-On - Integration Testing (30 min)**

Choose your language:

**Python Track**:

- **[02-api-integration-test.md](../../05-white-box-testing/exercises/python/02-api-integration-test.md)**

**JavaScript Track**:

- **[02-api-integration-test.md](../../05-white-box-testing/exercises/javascript/02-api-integration-test.md)**

**Activity**:
Write integration tests for a REST API with database operations.

**Part 3: Lecture - Mocking Strategies (30 min)**

Topics covered:

- Why mock external dependencies?
- When NOT to mock
- Mocking databases, APIs, file systems
- pytest fixtures vs unittest.mock
- Jest mock functions
- Common mocking pitfalls

**Part 4: Hands-On - Mocking Exercise (20 min)**

**Activity**:
Refactor tests from Part 2 to use mocks for external API calls.

Compare:

- Test speed with vs without mocks
- Test reliability
- Test clarity

#### 💬 Discussion Questions

1. When should you use real dependencies vs mocks?
2. Can you over-mock? What are the risks?
3. How do you test that your mocks are accurate?

#### 📝 Post-Class Work

1. Start Homework 5 (due Week 10)

   - White box testing for TaskFlow Management system
   - 50+ unit tests
   - 20+ integration tests
   - 80%+ coverage required

2. **Milestone 3 Due Next Week** (Black Box Test Planning)

#### 🎯 Homework 5 Preview

Review the assignment:

- [homework-5.md](../../05-white-box-testing/homework/homework-5.md)

Requirements:

- Comprehensive unit test suite (50+ tests)
- Integration tests for API endpoints (20+ tests)
- Mock external dependencies appropriately
- Achieve 80%+ code coverage
- Generate coverage reports
- Document bugs found through testing

**Worth 110 points (100 base + 10 bonus)**

---

## Week 8: White Box Testing Deep Dive

### 📅 Session 1: Advanced Coverage Techniques (2 hours)

**Canvas Module Title**: Week 8 - Session 1: Path Coverage & Cyclomatic Complexity

**Instructions to post in Canvas**:

---

#### Advanced Coverage Metrics 📊

Moving beyond statement and branch coverage to more sophisticated metrics.

#### 📚 Pre-Class Preparation (Complete BEFORE class)

**Required Reading** (1 hour):

1. **[06-path-coverage.md](../../05-white-box-testing/theory/06-path-coverage.md)**
   - Independent paths
   - Cyclomatic complexity
   - Path coverage tools

**Optional Advanced Reading**:

- Martin Fowler on Test Coverage
- ISTQB Advanced Level - Test Analyst

**Bring to Class**:

- Progress on Homework 5
- Questions about coverage

#### 🎯 In-Class Activities

**Part 1: Lecture - Path Coverage & Cyclomatic Complexity (45 min)**

Topics covered:

- What is path coverage?
- Calculating cyclomatic complexity
- Independent paths through code
- When path coverage matters
- Practical limits of path coverage
- Using coverage to identify complex code

**Part 2: Workshop - Coverage Analysis (45 min)**

**Activity**: Analyze Real Code

Working in pairs:

1. Choose a function from your team project or Homework 5
2. Draw control flow graph
3. Calculate cyclomatic complexity
4. Identify all independent paths
5. Design tests for each path
6. Measure actual coverage achieved

**Part 3: Coverage Report Analysis (30 min)**

**Activity**: Deep dive into coverage reports

1. Generate coverage reports for Homework 5
2. Identify uncovered lines
3. Determine if uncovered code is:
   - Error handling (hard to test)
   - Dead code (should be removed)
   - Missing test scenarios
4. Prioritize what to test next

#### 💬 Discussion Questions

1. When is high cyclomatic complexity a problem?
2. Should you always aim for 100% path coverage?
3. How do you balance coverage metrics with test quality?

#### 📝 Post-Class Work

1. **Milestone 3 Due This Week**

   - Black box test planning
   - Minimum 20 test cases
   - Use all 4 black box techniques
   - Submit on Canvas

2. Continue Homework 5 (due Week 10)
   - Focus on increasing coverage
   - Add integration tests

---

### 📅 Session 2: White Box Testing Best Practices (2 hours)

**Canvas Module Title**: Week 8 - Session 2: Test Quality & Maintenance

**Instructions to post in Canvas**:

---

#### Writing Maintainable Tests 🛠️

Learn how to write tests that don't become a burden as your codebase grows.

#### 📚 Pre-Class Preparation

**Review**:

- Your Homework 5 tests
- Identify any "code smells" in your tests

**Think About**:

- Have you found any bugs through your tests?
- Are your tests easy to understand?
- How long do your tests take to run?

#### 🎯 In-Class Activities

**Part 1: Lecture - Test Quality (45 min)**

Topics covered:

- Test code is real code - treat it well
- DRY principle in tests (fixtures, helpers)
- Test readability vs test performance
- Flaky tests and how to prevent them
- Test execution speed
- Test pyramid revisited

**Part 2: Code Review Workshop (45 min)**

**Activity**: Peer Test Code Review

1. Form groups of 3 students
2. Each person shares their Homework 5 test code
3. Review each other's tests for:
   - Clarity and readability
   - Proper use of fixtures
   - AAA pattern adherence
   - Test independence
   - Coverage quality
4. Provide constructive feedback

**Part 3: Refactoring Exercise (30 min)**

**Activity**: Improve Test Code

Take feedback from peer review and refactor your tests:

- Extract common setup to fixtures
- Improve test names
- Remove duplication
- Make assertions more specific

#### 💬 Discussion Questions

1. What makes a test "maintainable"?
2. How do you handle slow-running tests?
3. When should you delete tests?

#### 📝 Post-Class Work

1. Apply refactoring to Homework 5
2. Prepare for Module 6 (TDD) next week
3. Review Milestone 4 requirements (due Week 10)

#### 📚 Next Week Preview: Test-Driven Development

Next week we learn **TDD** - writing tests BEFORE code. This flips everything we've done so far!

**Prep for Week 9**:

- Read about TDD philosophy
- Be ready to try something different
- Bring an open mind!

---

## Week 9: Test-Driven Development

### 📅 Session 1: TDD Introduction & Red-Green-Refactor (2 hours)

**Canvas Module Title**: Week 9 - Session 1: Test-Driven Development Fundamentals

**Instructions to post in Canvas**:

---

#### Welcome to TDD! 🔴🟢🔧

Test-Driven Development flips the script: write tests FIRST, then code. It's challenging but powerful.

#### 📚 Pre-Class Preparation (Complete BEFORE class)

**Required Reading** (1.5 hours):

1. **[01-introduction.md](../../06-test-driven-development/theory/01-introduction.md)**

   - What is TDD?
   - The TDD cycle
   - Benefits and challenges

2. **[02-red-green-refactor.md](../../06-test-driven-development/theory/02-red-green-refactor.md)**
   - RED: Write failing test
   - GREEN: Make it pass
   - REFACTOR: Improve code
   - Discipline and rhythm

**Watch** (optional but recommended):

- Kent Beck on TDD
- Uncle Bob Martin - The Three Laws of TDD

#### 🎯 In-Class Activities

**Part 1: Lecture - TDD Philosophy (30 min)**

Topics covered:

- Why TDD works
- The three laws of TDD
- TDD vs test-after
- When TDD helps most
- When TDD is challenging

**Three Laws of TDD**:

1. Don't write production code until you have a failing test
2. Don't write more of a test than is sufficient to fail
3. Don't write more production code than is sufficient to pass the test

**Part 2: Live Coding Demo - FizzBuzz (30 min)**

Instructor demonstrates TDD with classic FizzBuzz problem:

- Write first failing test
- Minimal code to pass
- Refactor
- Repeat
- Show the rhythm and discipline

**Part 3: Hands-On - Your First TDD (60 min)**

Choose a kata to practice TDD:

**Options**:

- **[fizzbuzz.md](../../06-test-driven-development/exercises/fizzbuzz.md)** (beginner)
- **[string-calculator.md](../../06-test-driven-development/exercises/string-calculator.md)** (intermediate)

**Rules**:

1. Write test FIRST (watch it fail)
2. Write minimal code to pass
3. Refactor if needed
4. Commit after each RED-GREEN-REFACTOR cycle
5. NO CODE WITHOUT A FAILING TEST FIRST

Work in pairs (driver/navigator) and switch every 5 minutes.

#### 💬 Discussion Questions

1. How did TDD feel? Comfortable? Frustrating?
2. Did you catch yourself writing code before tests?
3. How did the design emerge from the tests?

#### 📝 Post-Class Work

1. Complete one TDD kata at home:

   - Choose from exercises in Module 6
   - Follow strict TDD
   - Commit after each cycle
   - Reflect on the experience

2. **Homework 4 Due This Week**

   - Black box test design
   - Submit on Canvas

3. Read theory for Session 2

---

### 📅 Session 2: TDD Best Practices & Anti-patterns (2 hours)

**Canvas Module Title**: Week 9 - Session 2: Advanced TDD

**Instructions to post in Canvas**:

---

#### TDD Mastery 🎯

Now that you've tried TDD, let's learn how to do it well and avoid common pitfalls.

#### 📚 Pre-Class Preparation (Complete BEFORE class)

**Required Reading** (1 hour):

1. **[03-best-practices.md](../../06-test-driven-development/theory/03-best-practices.md)**

   - Baby steps
   - Triangulation
   - Fake it till you make it
   - Test list technique

2. **[04-anti-patterns.md](../../06-test-driven-development/theory/04-anti-patterns.md)**
   - Testing implementation details
   - Over-mocking in TDD
   - Skipping refactoring
   - Writing tests after

**Reflect on**:

- Your TDD kata experience
- Challenges you faced

#### 🎯 In-Class Activities

**Part 1: Lecture - TDD Techniques (40 min)**

Topics covered:

- Baby steps (smallest possible increment)
- Triangulation (forcing generalization)
- Fake it till you make it (hardcode first)
- Test list (tracking what to test)
- TDD with legacy code
- TDD at different scales (unit, integration, system)

**Part 2: Hands-On - Intermediate Kata (50 min)**

Choose a more complex kata:

**Options**:

- **[bowling-game.md](../../06-test-driven-development/exercises/bowling-game.md)** (intermediate)
- **[roman-numerals.md](../../06-test-driven-development/exercises/roman-numerals.md)** (intermediate)

**Focus on**:

- Taking baby steps
- Using a test list
- Triangulation when needed
- Clean refactoring

**Part 3: TDD Reflection Discussion (30 min)**

Class discussion:

- What's hard about TDD?
- What benefits did you observe?
- When would you use TDD in real projects?
- When might you not use TDD?

#### 💬 Discussion Questions

1. Is TDD always worth the extra time?
2. How do you convince a team to try TDD?
3. Can you do TDD with UI code? Databases?

#### 📝 Post-Class Work

1. Start Homework 6 (due Week 12)

   - Library Management System
   - MUST use strict TDD
   - Git history will be checked!
   - 15-20 commits showing RED-GREEN-REFACTOR

2. Review Milestone 4 requirements (due next week)
   - Unit and integration testing
   - 80%+ coverage
   - White box testing focus

#### 🎯 Milestone 4 Reminder

**Due**: End of Week 10  
**Focus**: White Box Testing

Deliverables:

- 50+ unit tests
- 20+ integration tests
- 80%+ code coverage
- Coverage report analysis
- Document bugs found

See: [milestone-4-white-box.md](../../team-project/milestones/milestone-4-white-box.md)

---

## Week 10: TDD Deep Dive

### 📅 Session 1: TDD in Real Projects (2 hours)

**Canvas Module Title**: Week 10 - Session 1: Applying TDD to Your Project

**Instructions to post in Canvas**:

---

#### TDD in the Real World 🌍

Applying TDD to actual project features, not just katas.

#### 📚 Pre-Class Preparation

**Bring to Class**:

- Your team project codebase
- A new feature you need to implement
- Questions about applying TDD

**Think About**:

- What feature could you build with TDD this week?
- What makes it harder than katas?

#### 🎯 In-Class Activities

**Part 1: Lecture - TDD at Scale (40 min)**

Topics covered:

- TDD with databases (test database strategies)
- TDD with web APIs (mocking vs real services)
- TDD with frontend code
- TDD in teams (pair programming)
- TDD and continuous integration
- Dealing with legacy code

**Part 2: Workshop - Plan Your TDD Feature (40 min)**

**Activity**: Work with your team

1. Choose a feature for Milestone 5 (due Week 12)
2. Write out test list (what needs to be tested?)
3. Identify dependencies (what needs mocking?)
4. Plan your TDD approach
5. Start first test together

**Part 3: Live Coding - Real Feature TDD (40 min)**

Instructor demonstrates TDD with real project feature:

- Start with acceptance criteria
- Break into small testable pieces
- TDD each piece
- Show commit history
- Refactor at the end

#### 💬 Discussion Questions

1. How do you break a big feature into TDD-able pieces?
2. When do you write integration tests vs unit tests in TDD?
3. How do you handle external dependencies?

#### 📝 Post-Class Work

1. **Homework 5 Due This Week**

   - White box testing
   - Submit on Canvas

2. Work on Milestone 5 preparation
   - Choose your TDD feature
   - Create test list
   - Start planning approach

---

### 📅 Session 2: TDD Workshop & Code Review (2 hours)

**Canvas Module Title**: Week 10 - Session 2: TDD Practice Session

**Instructions to post in Canvas**:

---

#### TDD Practice Time 💻

Dedicated time for TDD practice with instructor support.

#### 🎯 In-Class Activities

**Part 1: Advanced Kata Session (90 min)**

Choose a challenging kata:

**Options**:

- **[bank-account.md](../../06-test-driven-development/exercises/bank-account.md)** (advanced)
- Continue with Bowling Game or Roman Numerals
- Work on your Milestone 5 feature with TDD

**Guidelines**:

- Strict TDD discipline
- Pair programming encouraged
- Instructor available for questions
- Commit every RED-GREEN-REFACTOR cycle

**Part 2: Code Review & Discussion (30 min)**

**Activity**: Show your TDD work

- 2-3 volunteers show their git history
- Walk through RED-GREEN-REFACTOR cycles
- Class discusses design that emerged
- Instructor provides feedback

#### 💬 Discussion Questions

1. How has your TDD improved since Week 9?
2. What's still challenging?
3. Will you use TDD in your projects?

#### 📝 Post-Class Work

1. **Milestone 4 Due This Week**

   - White box testing deliverables
   - Submit on Canvas

2. Start Milestone 5 work (due Week 12)

   - Implement feature using strict TDD
   - Remember: tests first, always!

3. Continue Homework 6 (due Week 12)

#### 🎯 Week 11 Preview: Exam 2

**Next week is Exam 2** (Modules 4-6: Black Box, White Box, TDD)

Topics to review:

- All black box techniques (EP, BVA, Decision Tables, State Transition)
- Code coverage metrics
- Unit vs integration testing
- Mocking strategies
- TDD cycle (RED-GREEN-REFACTOR)

**Start studying!**

---

## Week 11: Exam 2 Week

### 📅 Session 1: Exam 2 Review Session (2 hours)

**Canvas Module Title**: Week 11 - Session 1: Exam 2 Review

**Instructions to post in Canvas**:

---

#### Exam 2 Review 📚

Comprehensive review of Modules 4-6. Bring all your questions!

#### 🎯 Session Structure

**Part 1: Concept Review (60 min)**

Quick review of key concepts:

**Module 4 - Black Box Testing** (20 min):

- Equivalence Partitioning
- Boundary Value Analysis
- Decision Tables
- State Transition Testing

**Module 5 - White Box Testing** (20 min):

- Code coverage types
- Unit testing best practices
- Integration testing
- Mocking strategies

**Module 6 - TDD** (20 min):

- RED-GREEN-REFACTOR cycle
- Three laws of TDD
- TDD techniques (baby steps, triangulation)
- TDD best practices and anti-patterns

**Part 2: Q&A Session (30 min)**

Open floor for questions about any of the three modules.

**Part 3: Practice Problems (30 min)**

Work through sample problems:

1. **Black Box Exercise** (10 min)

   - Given requirements, design test cases using all 4 techniques

2. **White Box Exercise** (10 min)

   - Analyze code coverage report
   - Write unit tests for uncovered code
   - Identify what to mock

3. **TDD Exercise** (10 min)
   - Start a feature with TDD
   - Show first 3 RED-GREEN-REFACTOR cycles

#### 💬 Exam 2 Details

**When**: Session 2 (next class)  
**Duration**: 2 hours  
**Coverage**: Modules 4-6  
**Format**: Practical hands-on tasks  
**Weight**: 20% of final grade

**Likely exam structure**:

**Part 1: Black Box Test Design** (30%)

- Design test cases for given requirements
- Use all 4 techniques (EP, BVA, Decision Table, State Transition)
- Document test cases clearly

**Part 2: White Box Testing** (40%)

- Write unit tests for provided code
- Achieve specified coverage target
- Mock external dependencies
- Fix bugs discovered by tests

**Part 3: TDD** (30%)

- Implement feature using strict TDD
- Commit after each cycle
- Git history will be verified
- Show RED-GREEN-REFACTOR pattern

**What to Bring**:

- Laptop with development environment
- Testing frameworks installed (pytest/Jest)
- Code editor ready
- Coverage tools installed

#### 📝 Study Checklist

**Black Box Testing**:

- [ ] Can you design EP test cases?
- [ ] Can you identify boundaries and write BVA tests?
- [ ] Can you create decision tables?
- [ ] Can you model state transitions?

**White Box Testing**:

- [ ] Can you write unit tests with AAA pattern?
- [ ] Do you know how to mock dependencies?
- [ ] Can you interpret coverage reports?
- [ ] Can you write integration tests?

**TDD**:

- [ ] Can you follow strict TDD (test-first)?
- [ ] Do you understand RED-GREEN-REFACTOR?
- [ ] Can you take baby steps?
- [ ] Can you refactor safely with green tests?

#### 🎯 Final Exam Prep Tips

**Tonight**:

1. Review all homework solutions (HW 4, 5, 6)
2. Revisit key theory documents
3. Practice TDD with a kata
4. Ensure development environment works
5. Get good sleep!

---

### 📅 Session 2: **EXAM 2** 🎯 (2 hours)

**Canvas Module Title**: Week 11 - Session 2: Exam 2 (Modules 4-6)

**Instructions to post in Canvas**:

---

#### Exam 2: Practical Assessment

**Duration**: 2 hours  
**Coverage**: Modules 4-6 (Black Box, White Box, TDD)  
**Weight**: 20% of final grade

#### 📋 Exam Format

You will receive a separate exam document at the start of class with detailed instructions.

**Expected format**:

**Part 1: Black Box Test Design** (30%)

- Requirements for an application feature
- Design comprehensive test cases using:
  - Equivalence Partitioning
  - Boundary Value Analysis
  - Decision Tables
  - State Transition Testing
- Document test cases in provided template

**Part 2: White Box Testing** (40%)

- Provided codebase with existing code
- Tasks:
  - Write unit tests for specified modules
  - Achieve 85%+ code coverage
  - Write integration tests for API endpoints
  - Mock external dependencies appropriately
  - Document any bugs found

**Part 3: TDD Implementation** (30%)

- Implement a feature using strict TDD
- Requirements will be provided
- Must show RED-GREEN-REFACTOR in git history
- Minimum 10 commits demonstrating TDD cycles
- Tests must be written BEFORE code

#### ✅ Before You Begin

- [ ] Laptop fully charged
- [ ] Development environment verified
- [ ] pytest OR Jest installed
- [ ] Coverage tools ready (pytest-cov / Jest --coverage)
- [ ] Git configured
- [ ] Text editor ready
- [ ] Exam document downloaded

#### 📤 Submission Instructions

1. Create repository as instructed
2. Complete all three parts
3. Push all commits to GitHub
4. Verify git history shows TDD cycles
5. Submit repository URL on Canvas
6. Submit before end of class time

#### ⏱️ Time Management

- Read all instructions carefully (5 min)
- Part 1: Black Box (~35 min)
- Part 2: White Box (~50 min)
- Part 3: TDD (~25 min)
- Testing and submission (10 min)

#### 🚫 Academic Integrity

- Individual work only
- No collaboration during exam
- You may use course materials and documentation
- Do not share your work
- Violations = zero grade

#### 📝 After Exam

**Well done!** 🎉

Next modules:

- Module 7: Data-Driven Testing
- Module 8: System-Level Testing
- Module 9: Performance Testing

**Don't forget**:

- **Milestone 5 due next week** (TDD Feature)
- **Homework 6 due next week** (TDD Implementation)

---

## Week 12: Data-Driven Testing

### 📅 Session 1: Parameterized Tests & Test Data Management (2 hours)

**Canvas Module Title**: Week 12 - Session 1: Data-Driven Testing Fundamentals

**Instructions to post in Canvas**:

---

#### Welcome to Data-Driven Testing! 📊

Learn how to run the same test with multiple sets of data - reducing code duplication and increasing coverage.

#### 📚 Pre-Class Preparation (Complete BEFORE class)

**Required Reading** (1.5 hours):

1. **[01-introduction.md](../../07-data-driven-testing/theory/01-introduction.md)**

   - What is data-driven testing?
   - Benefits and use cases
   - DDT vs regular testing

2. **[02-parameterized-tests.md](../../07-data-driven-testing/theory/02-parameterized-tests.md)**

   - pytest.mark.parametrize
   - Jest test.each()
   - Parameterization best practices

3. **[03-test-data-management.md](../../07-data-driven-testing/theory/03-test-data-management.md)**
   - External data sources (CSV, JSON, Excel)
   - Test data organization
   - Data-driven frameworks

#### 🎯 In-Class Activities

**Part 1: Lecture - Parameterized Testing (45 min)**

Topics covered:

- Why duplicate test code is bad
- Parameterization syntax (Python and JavaScript)
- Multiple parameters
- Test naming with parameters
- When to parameterize vs separate tests

**Part 2: Hands-On - Parameterized Tests (30 min)**

Choose your language:

**Python Track**:

- **[01-basic-parametrization.md](../../07-data-driven-testing/exercises/python/01-basic-parametrization.md)**

**JavaScript Track**:

- **[01-basic-parametrization.md](../../07-data-driven-testing/exercises/javascript/01-basic-parametrization.md)**

**Activity**:
Refactor regular tests into parameterized tests.

**Part 3: Lecture - External Test Data (30 min)**

Topics covered:

- CSV files for test data
- JSON test data files
- Excel spreadsheets
- Database-driven tests
- Pros/cons of external data

**Part 4: Hands-On - CSV Test Data (15 min)**

**Activity**:
Load test data from CSV file and run parameterized tests.

#### 💬 Discussion Questions

1. When should test data be in code vs external files?
2. How do you handle large test data sets?
3. How do you maintain test data over time?

#### 📝 Post-Class Work

1. **Homework 6 Due This Week**

   - TDD implementation
   - Submit on Canvas

2. **Milestone 5 Due This Week**

   - TDD feature implementation
   - Submit on Canvas

3. Start Homework 7 (due Week 13)
   - E-Commerce Order Processing
   - Data-driven testing focus

---

### 📅 Session 2: Advanced Data-Driven Testing (2 hours)

**Canvas Module Title**: Week 12 - Session 2: DDT Best Practices

**Instructions to post in Canvas**:

---

#### Data-Driven Testing Mastery 🎯

Advanced techniques for managing test data and scaling DDT.

#### 📚 Pre-Class Preparation (Complete BEFORE class)

**Required Reading** (1 hour):

1. **[04-best-practices.md](../../07-data-driven-testing/theory/04-best-practices.md)**
   - Separating test logic from test data
   - Data-driven assertions
   - Handling test data versions
   - DDT in CI/CD

**Review**:

- Your Homework 7 requirements

#### 🎯 In-Class Activities

**Part 1: Lecture - DDT Best Practices (40 min)**

Topics covered:

- Separating what from data
- Test data factories
- Combinatorial testing (pairwise)
- Negative testing with DDT
- Performance considerations
- DDT maintenance challenges

**Part 2: Workshop - Real Project DDT (50 min)**

**Activity**: Apply DDT to your team project

Working in teams:

1. Identify test cases that could be data-driven
2. Extract test data to external file
3. Implement parameterized tests
4. Show before/after comparison (lines of code saved)

**Part 3: Advanced Exercise (30 min)**

Choose advanced exercise:

**Python Track**:

- **[04-api-testing-json.md](../../07-data-driven-testing/exercises/python/04-api-testing-json.md)**

**JavaScript Track**:

- **[04-api-testing-json.md](../../07-data-driven-testing/exercises/javascript/04-api-testing-json.md)**

**Activity**:
Test REST API with JSON test data file containing multiple scenarios.

#### 💬 Discussion Questions

1. Can you have too much data-driven testing?
2. How do you balance readability vs DRY in tests?
3. When should you NOT use DDT?

#### 📝 Post-Class Work

1. Complete Homework 7 (due next week)

   - E-Commerce order processing
   - CSV, JSON, Excel data sources
   - Comprehensive DDT implementation

2. Start reading Module 8 (System-Level Testing)

3. Review Milestone 6 requirements (due Week 14)

---

## Week 13: System-Level Testing

### 📅 Session 1: BDD & Gherkin Syntax (2 hours)

**Canvas Module Title**: Week 13 - Session 1: Behavior-Driven Development

**Instructions to post in Canvas**:

---

#### System-Level Testing Begins! 🌐

Moving from unit/integration to testing the entire system as a user would.

#### 📚 Pre-Class Preparation (Complete BEFORE class)

**Required Reading** (1.5 hours):

1. **[01-introduction.md](../../08-system-level-testing/theory/01-introduction.md)**

   - What is system-level testing?
   - E2E testing
   - User acceptance testing

2. **[02-bdd-gherkin.md](../../08-system-level-testing/theory/02-bdd-gherkin.md)**
   - BDD philosophy
   - Gherkin syntax (Given-When-Then)
   - Feature files
   - Step definitions

**Install**:

- Selenium WebDriver
- Behave (Python) OR Cucumber.js (JavaScript)
- ChromeDriver or GeckoDriver

#### 🎯 In-Class Activities

**Part 1: Lecture - BDD & Gherkin (45 min)**

Topics covered:

- BDD vs TDD vs ATDD
- Writing user stories
- Gherkin syntax (Feature, Scenario, Given-When-Then)
- Best practices for scenarios
- Avoiding anti-patterns

**Part 2: Hands-On - Write Gherkin (30 min)**

**Activity**: Write feature files

Given a user story for your team project:

1. Write Feature description
2. Write 3-5 Scenarios in Gherkin
3. Use Given-When-Then format
4. Keep scenarios focused and clear

**Part 3: Lecture - Step Definitions (30 min)**

Topics covered:

- Connecting Gherkin to code
- Step definition patterns
- Reusing steps
- Context sharing between steps

**Part 4: Hands-On - Step Definitions (15 min)**

**Activity**:
Implement step definitions for the feature file you wrote.

#### 💬 Discussion Questions

1. Who should write Gherkin scenarios? Developers? QA? Product?
2. How detailed should scenarios be?
3. How do you avoid duplication in step definitions?

#### 📝 Post-Class Work

1. **Homework 7 Due This Week**

   - Data-driven testing
   - Submit on Canvas

2. Start Homework 8 (due Week 15)

   - E2E testing with Selenium and Playwright
   - BDD scenarios with Gherkin

3. Write feature files for your team project

---

### 📅 Session 2: Selenium & Web Automation (2 hours)

**Canvas Module Title**: Week 13 - Session 2: Selenium WebDriver

**Instructions to post in Canvas**:

---

#### Web Test Automation 🤖

Learn to automate browser testing with Selenium.

#### 📚 Pre-Class Preparation (Complete BEFORE class)

**Required Reading** (1 hour):

1. **[03-selenium-webdriver.md](../../08-system-level-testing/theory/03-selenium-webdriver.md)**
   - Selenium architecture
   - Locator strategies
   - WebDriver commands
   - Waits (implicit, explicit)

**Setup Verification**:

- Selenium installed
- ChromeDriver or GeckoDriver downloaded
- Test browser opens with WebDriver

#### 🎯 In-Class Activities

**Part 1: Lecture - Selenium Fundamentals (40 min)**

Topics covered:

- Selenium architecture
- Locator strategies (ID, class, CSS, XPath)
- Finding elements
- Interacting with elements (click, sendKeys, clear)
- Waits and timing issues
- Handling alerts, frames, windows

**Part 2: Live Coding - Selenium Demo (30 min)**

Instructor demonstrates:

- Open browser with WebDriver
- Navigate to website
- Find elements
- Interact with form
- Assert expected results
- Close browser

**Part 3: Hands-On - First Selenium Test (50 min)**

**Activity**: Write your first Selenium test

Test a simple web application (TodoMVC):

1. Open TodoMVC app
2. Add a todo item
3. Mark it complete
4. Verify it appears with line-through
5. Delete the todo
6. Verify it's removed

Choose your language:

- Python: Selenium + pytest
- JavaScript: WebDriverIO or Selenium with Jest

#### 💬 Discussion Questions

1. What's challenging about web test automation?
2. How do you handle dynamic content?
3. What makes Selenium tests flaky?

#### 📝 Post-Class Work

1. Complete basic Selenium exercises
2. Start implementing E2E tests for team project
3. Practice locating elements on your project's web pages

---

## Week 14: System-Level Testing Advanced

### 📅 Session 1: Playwright & Modern E2E Testing (2 hours)

**Canvas Module Title**: Week 14 - Session 1: Playwright

**Instructions to post in Canvas**:

---

#### Modern E2E Testing with Playwright 🎭

Playwright is a newer, faster alternative to Selenium. Learn the differences.

#### 📚 Pre-Class Preparation (Complete BEFORE class)

**Required Reading** (1 hour):

1. **[05-playwright.md](../../08-system-level-testing/theory/05-playwright.md)**
   - Playwright vs Selenium
   - Playwright features
   - Auto-wait mechanism
   - Multi-browser testing

**Install**:

- Playwright: `npm install playwright` or `pip install playwright`
- Install browsers: `playwright install`

#### 🎯 In-Class Activities

**Part 1: Lecture - Playwright Features (40 min)**

Topics covered:

- What makes Playwright different
- Auto-waiting (no more explicit waits!)
- Network interception
- Multi-tab/context support
- Parallel execution
- Test recording and codegen

**Part 2: Live Coding - Playwright Demo (30 min)**

Instructor demonstrates:

- Same test as Selenium session, but in Playwright
- Compare code simplicity
- Show auto-wait in action
- Demonstrate codegen tool
- Show test recording

**Part 3: Hands-On - Playwright Test (50 min)**

**Activity**: Convert Selenium test to Playwright

Take your TodoMVC test from last session:

1. Rewrite using Playwright
2. Compare lines of code
3. Notice simpler syntax
4. Run both and compare speed
5. Discuss pros/cons of each

#### 💬 Discussion Questions

1. When would you choose Playwright over Selenium?
2. Is Playwright's auto-wait always better?
3. How do you decide which E2E tool to use?

#### 📝 Post-Class Work

1. Complete Playwright exercises
2. Choose Selenium OR Playwright for Homework 8
3. Work on Milestone 6 (due this week)

---

### 📅 Session 2: Page Object Model & E2E Best Practices (2 hours)

**Canvas Module Title**: Week 14 - Session 2: Page Object Model

**Instructions to post in Canvas**:

---

#### Maintainable E2E Tests 🏗️

Learn the Page Object Model pattern to make E2E tests maintainable.

#### 📚 Pre-Class Preparation (Complete BEFORE class)

**Required Reading** (1 hour):

1. **[04-page-object-model.md](../../08-system-level-testing/theory/04-page-object-model.md)**
   - POM pattern
   - Benefits of POM
   - Implementing page objects
   - POM best practices

**Review**:

- Your E2E tests (how can they be improved?)

#### 🎯 In-Class Activities

**Part 1: Lecture - Page Object Model (45 min)**

Topics covered:

- Why E2E tests become unmaintainable
- POM pattern explained
- Separating test logic from page interactions
- Page object design
- Component objects
- POM anti-patterns

**Part 2: Refactoring Workshop (45 min)**

**Activity**: Refactor to Page Objects

Take your existing E2E tests:

1. Identify pages in your application
2. Create page object classes
3. Move locators to page objects
4. Move actions to page objects
5. Refactor tests to use page objects
6. Compare before/after maintainability

**Part 3: E2E Best Practices (30 min)**

Topics covered:

- Test data management in E2E
- Test independence
- Running E2E in CI/CD
- Parallel execution
- Dealing with flaky tests
- When to E2E vs API test vs unit test

#### 💬 Discussion Questions

1. How do you keep page objects up to date?
2. Can POM be over-engineered?
3. How many E2E tests is enough?

#### 📝 Post-Class Work

1. **Milestone 6 Due This Week**

   - E2E test automation
   - 5+ feature files in Gherkin
   - Selenium OR Playwright tests
   - Page Object Model
   - Submit on Canvas

2. Continue Homework 8 (due next week)

3. Start reading Module 9 (Performance Testing)

---

## Week 15: Performance Testing

### 📅 Session 1: Performance Testing Fundamentals (2 hours)

**Canvas Module Title**: Week 15 - Session 1: Introduction to Performance Testing

**Instructions to post in Canvas**:

---

#### Performance Testing Begins! ⚡

Learn to test not just IF your application works, but HOW WELL it works under load.

#### 📚 Pre-Class Preparation (Complete BEFORE class)

**Required Reading** (1.5 hours):

1. **[01-introduction.md](../../09-performance-testing/theory/01-introduction.md)**

   - What is performance testing?
   - Types: load, stress, spike, endurance
   - Performance metrics
   - When to performance test

2. **[02-test-design.md](../../09-performance-testing/theory/02-test-design.md)**
   - Defining performance requirements
   - Designing load profiles
   - Test scenarios
   - Success criteria

**Install**:

- Apache JMeter (download from apache.org/jmeter)
- Verify it launches successfully

#### 🎯 In-Class Activities

**Part 1: Lecture - Performance Testing Types (45 min)**

Topics covered:

- Load testing (expected load)
- Stress testing (breaking point)
- Spike testing (sudden load increase)
- Endurance/soak testing (long duration)
- Performance metrics (response time, throughput, errors)
- SLAs and SLOs

**Part 2: Lecture - Performance Test Design (30 min)**

Topics covered:

- Identifying critical user journeys
- Determining load profiles
- Ramp-up strategies
- Think time and pacing
- Test data needs
- Success/failure criteria

**Part 3: Workshop - Design Performance Tests (45 min)**

**Activity**: Design performance tests for your project

Working in teams:

1. Identify 3 critical user scenarios
2. Define expected load (users, requests/sec)
3. Design load profile (ramp-up, duration)
4. Define success criteria (response time < X, error rate < Y%)
5. Document test plan

#### 💬 Discussion Questions

1. How do you determine "realistic" load?
2. When should you performance test?
3. How do you test when you don't have production-level infrastructure?

#### 📝 Post-Class Work

1. **Homework 8 Due This Week**

   - E2E testing with Selenium/Playwright
   - Submit on Canvas

2. Install and familiarize yourself with JMeter

3. Start Homework 9 (due Week 16)
   - Performance testing with JMeter
   - Load, stress, and spike tests

---

### 📅 Session 2: JMeter & Load Testing (2 hours)

**Canvas Module Title**: Week 15 - Session 2: Apache JMeter

**Instructions to post in Canvas**:

---

#### Hands-On with JMeter 🧪

Learn to use the most popular performance testing tool.

#### 📚 Pre-Class Preparation (Complete BEFORE class)

**Required Reading** (1.5 hours):

1. **[03-jmeter-fundamentals.md](../../09-performance-testing/theory/03-jmeter-fundamentals.md)**

   - JMeter components (Thread Group, Samplers, Listeners)
   - Creating test plans
   - Variables and properties
   - Assertions

2. **[04-jmeter-advanced.md](../../09-performance-testing/theory/04-jmeter-advanced.md)**
   - Correlation and extraction
   - Parameterization
   - Distributed testing
   - CLI mode

**Verify**:

- JMeter launches successfully
- You can create a basic test plan

#### 🎯 In-Class Activities

**Part 1: Lecture - JMeter Architecture (30 min)**

Topics covered:

- JMeter components overview
- Thread Groups (users, ramp-up, duration)
- Samplers (HTTP, JDBC, etc.)
- Listeners (graphs, tables, reports)
- Timers (think time)
- Assertions (validations)

**Part 2: Live Demo - First JMeter Test (40 min)**

Instructor demonstrates:

- Create new test plan
- Add Thread Group
- Add HTTP Request sampler
- Add View Results Tree listener
- Run simple test
- Analyze results
- Add assertions
- Add timers

**Part 3: Hands-On - Your First Load Test (50 min)**

**Activity**: Create JMeter test for an API

Test a public API or your team project:

1. Create test plan
2. Configure thread group (10 users, 5 sec ramp-up, 30 sec duration)
3. Add HTTP requests for key endpoints
4. Add response assertions
5. Add listeners (View Results Tree, Summary Report, Response Time Graph)
6. Run test
7. Analyze results

#### 💬 Discussion Questions

1. What's a "good" response time?
2. How do you handle dynamic data (session IDs, tokens)?
3. When are performance issues actually backend vs frontend?

#### 📝 Post-Class Work

1. Complete JMeter tutorial exercises

2. Work on Homework 9 (due next week)

   - Create comprehensive JMeter test plan
   - Load test
   - Stress test
   - Spike test
   - Performance analysis report

3. **Prepare for Exam 3** (next week!)

---

## Week 16: Final Week

### 📅 Session 1: Course Review & Exam 3 Prep (2 hours)

**Canvas Module Title**: Week 16 - Session 1: Final Exam Review

**Instructions to post in Canvas**:

---

#### Final Exam Review 📚

Comprehensive review of Modules 7-9 plus course wrap-up.

#### 🎯 Session Structure

**Part 1: Module Review (60 min)**

**Module 7 - Data-Driven Testing** (20 min):

- Parameterized tests
- Test data sources (CSV, JSON, Excel)
- DDT best practices

**Module 8 - System-Level Testing** (20 min):

- BDD and Gherkin
- Selenium WebDriver
- Playwright
- Page Object Model

**Module 9 - Performance Testing** (20 min):

- Performance test types
- JMeter fundamentals
- Load profiles and test design
- Analyzing performance results

**Part 2: Q&A Session (30 min)**

Open questions about Modules 7-9.

**Part 3: Practice Problems (30 min)**

Work through sample problems for each module.

#### 💬 Exam 3 Details

**When**: Session 2 (next class)  
**Duration**: 2 hours  
**Coverage**: Modules 7-9  
**Format**: Practical hands-on  
**Weight**: 20% of final grade

**Expected sections**:

**Part 1: Data-Driven Testing** (25%)

- Write parameterized tests
- Load test data from CSV/JSON
- Refactor tests to be data-driven

**Part 2: System-Level Testing** (50%)

- Write Gherkin feature file
- Implement E2E test with Selenium/Playwright
- Use Page Object Model pattern
- Test a web application

**Part 3: Performance Testing** (25%)

- Create JMeter test plan
- Configure load test
- Execute and analyze results
- Identify performance bottlenecks

**What to Bring**:

- Laptop with development environment
- Testing frameworks installed
- JMeter installed
- Selenium/Playwright ready

#### 📝 Study Checklist

**Data-Driven Testing**:

- [ ] Can you write parameterized tests?
- [ ] Can you load data from CSV/JSON?
- [ ] Do you know when to use DDT?

**System-Level Testing**:

- [ ] Can you write Gherkin scenarios?
- [ ] Can you automate browser tests?
- [ ] Do you understand Page Object Model?

**Performance Testing**:

- [ ] Can you create JMeter test plan?
- [ ] Do you know different test types (load, stress, spike)?
- [ ] Can you analyze performance results?

#### 🎯 Final Study Tips

**Tonight**:

1. Review Homework 7, 8, 9 solutions
2. Practice writing Gherkin scenarios
3. Run through JMeter tutorial
4. Review Selenium/Playwright basics
5. Get good sleep!

---

### 📅 Session 2: **EXAM 3** 🎯 + Final Presentations (4 hours)

**Canvas Module Title**: Week 16 - Session 2: Exam 3 & Final Presentations

**Instructions to post in Canvas**:

---

#### Final Exam & Presentations 🎓

**Session Plan**:

- **First 2 hours**: Exam 3
- **Break**: 15 minutes
- **Next 1.5 hours**: Team Project Final Presentations
- **Last 30 min**: Course wrap-up & feedback

---

### Part 1: Exam 3 (2 hours)

#### Exam 3: Practical Assessment

**Duration**: 2 hours  
**Coverage**: Modules 7-9 (Data-Driven, System-Level, Performance)  
**Weight**: 20% of final grade

#### 📋 Exam Format

You will receive a separate exam document with detailed instructions.

**Expected structure**:

**Part 1: Data-Driven Testing** (25%)

- Refactor provided tests to use parameterization
- Load test data from CSV file
- Add assertions for each data set

**Part 2: System-Level Testing** (50%)

- Write feature file in Gherkin for given user story
- Implement step definitions
- Write E2E test using Selenium OR Playwright
- Implement Page Object Model
- Test provided web application

**Part 3: Performance Testing** (25%)

- Create JMeter test plan for API
- Configure load test (specified users/duration)
- Execute test
- Generate reports
- Identify performance issues from results

#### ✅ Before You Begin

- [ ] Laptop charged
- [ ] Development environment ready
- [ ] JMeter installed
- [ ] Selenium/Playwright configured
- [ ] Exam document downloaded

#### 📤 Submission Instructions

1. Complete all three parts
2. Push code to GitHub repository
3. Include JMeter test plan (.jmx file)
4. Include performance test results
5. Submit repository URL on Canvas
6. Submit before 2-hour mark

---

### Part 2: Final Presentations (1.5 hours)

#### Team Project Presentations

**Milestone 7: Final Presentation**

Each team presents their semester-long project.

#### 📋 Presentation Format

**Time**: 10-15 minutes per team  
**Audience**: Class + instructor

**Required Content**:

1. **Project Overview** (2 min)

   - What did you build?
   - Technology stack
   - Team members and roles

2. **Demo** (3 min)

   - Live demonstration of key features
   - Show the application working

3. **Testing Approach** (5 min)

   - Black box test cases designed
   - White box testing (unit + integration)
   - TDD feature implementation
   - E2E tests with Selenium/Playwright
   - Performance testing results

4. **Lessons Learned** (3 min)

   - What worked well?
   - Challenges faced
   - If you could start over, what would you do differently?

5. **Q&A** (2 min)
   - Answer questions from class/instructor

#### ✅ Presentation Checklist

- [ ] Slides prepared (optional but recommended)
- [ ] Demo environment ready and tested
- [ ] All team members participate
- [ ] Time presentation (stay within 15 min)
- [ ] Test demo beforehand!

#### 📝 Deliverables

**Due Today**:

- Live presentation
- Project report document
- Performance test results
- Individual reflection (submitted separately)

See: [milestone-7-final.md](../../team-project/milestones/milestone-7-final.md)

---

### Part 3: Course Wrap-Up (30 minutes)

#### Congratulations! 🎉

You've completed the Software Testing course!

#### 📊 What You've Learned

**Module 1: Git** - Version control fundamentals  
**Module 2: Testing Concepts** - Testing types, levels, principles  
**Module 3: Static Testing** - Pre-commit hooks, linting  
**Module 4: Black Box Testing** - EP, BVA, Decision Tables, State Transition  
**Module 5: White Box Testing** - Coverage, unit tests, mocking  
**Module 6: TDD** - Test-first development  
**Module 7: Data-Driven Testing** - Parameterization, test data  
**Module 8: System-Level Testing** - BDD, Selenium, Playwright, POM  
**Module 9: Performance Testing** - JMeter, load testing

#### 🎯 Skills Acquired

- ✅ Design comprehensive test cases
- ✅ Write unit, integration, and E2E tests
- ✅ Achieve high code coverage
- ✅ Practice test-driven development
- ✅ Automate browser testing
- ✅ Performance test applications
- ✅ Work in teams with Git workflows
- ✅ Use CI/CD for automated testing

#### 📝 Final Reminders

**Due Today**:

- **Homework 9**: Performance Testing (submit on Canvas)
- **Milestone 7**: Final Presentation (completed in class)
- **Individual Reflection**: Submit separately by end of day

**Grades**:

- Final grades will be posted within 1 week
- Check Canvas for your final score
- Reach out if you have questions about grading

#### 💬 Course Feedback

Please complete the course evaluation survey (link on Canvas).

Your feedback helps improve the course for future students!

#### 🙏 Thank You!

Thank you for your hard work, engagement, and dedication this semester.

**You are now equipped to be effective software testers and quality advocates!**

**Best of luck in your future careers!** 🚀

---

**Course Complete!** 🎓✨
