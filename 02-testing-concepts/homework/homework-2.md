# Homework 2: Testing Concepts Analysis

**Module**: 2 - Software Testing Concepts  
**Due Date**: End of Week 3  
**Points**: 100  
**Estimated Time**: 4-5 hours

---

## 🎯 Objectives

This homework will help you:

- Apply testing concepts to real-world applications
- Design comprehensive test strategies
- Understand the relationship between testing types and levels
- Make informed decisions about testing priorities
- Think critically about quality assurance

---

## 📋 Assignment Overview

You will select a real application (web, mobile, or desktop), analyze its testing needs, and design a comprehensive test strategy. This is a theoretical exercise focused on planning, not implementation.

---

## 📝 Part 1: Application Selection & Analysis (20 points)

**File**: `part1-application-analysis.md` (minimum 300 words)

### 1.1 Choose an Application

Select **ONE** of the following:

- **Option A**: Choose an existing application you use regularly (e.g., Instagram, Netflix, Spotify, Gmail)
- **Option B**: Choose a hypothetical application:
  - Online food delivery platform
  - Student management system
  - Fitness tracking mobile app
  - Personal finance manager

### 1.2 Application Description

Write a detailed description (300-500 words) including:

- **Purpose**: What does the application do?
- **Target Users**: Who uses it?
- **Key Features**: List the main features (at least 5)
- **Technology Stack** (if known): Web/Mobile/Desktop, Frontend/Backend technologies
- **Critical Functions**: Which features are mission-critical?

### Example:

```markdown
## Application: FoodHub - Online Food Delivery Platform

**Purpose**: FoodHub connects customers with local restaurants, allowing
users to browse menus, place orders, track delivery, and pay online.

**Target Users**:

- Customers (ordering food)
- Restaurants (managing menus and orders)
- Delivery drivers (fulfilling orders)

**Key Features**:

1. User registration and authentication
2. Restaurant search and filtering
3. Menu browsing and cart management
4. Order placement and payment processing
5. Real-time order tracking
6. User reviews and ratings
7. Delivery driver assignment and navigation

...
```

---

## 📝 Part 2: Testing Types Classification (25 points)

**File**: `part2-testing-types.md` (minimum 8 test types)

For your selected application, identify and describe **at least 8 different test types** needed.

### Template for Each Test Type:

**Important**: Use `## Test Type:` heading (not `###`) for each test type in your file.

```markdown
## Test Type: [Functional/Non-Functional/Regression/etc.]

**Category**: [Functional or Non-Functional]

**Purpose**: Why is this testing type needed for this application?

**Examples** (at least 3):

1. [Specific test scenario]
2. [Specific test scenario]
3. [Specific test scenario]

**Priority**: [Critical/High/Medium/Low]

**Justification**: Why this priority level?
```

### Example:

```markdown
## Test Type: Functional Testing

**Category**: Functional

**Purpose**: Verify that all features work according to requirements.
In a food delivery app, users must be able to complete orders successfully.

**Examples**:

1. User can search for restaurants by cuisine type
2. Adding items to cart correctly updates total price
3. Payment processing completes and order is confirmed

**Priority**: Critical

**Justification**: These are core features - if they don't work, the
application has no value to users.

---

## Test Type: Performance Testing

**Category**: Non-Functional

**Purpose**: Ensure the app handles load during peak ordering times
(lunch/dinner rush) and provides good response times.

**Examples**:

1. Homepage loads in under 2 seconds
2. Search results display in under 1 second
3. System handles 10,000 concurrent users during peak hours

**Priority**: High

**Justification**: Slow performance leads to abandoned orders and lost revenue.
```

**Required Test Types** (must include these, plus others):

- Functional Testing
- Performance Testing
- Security Testing
- Usability Testing
- Regression Testing
- At least 3 more relevant types

---

## 📝 Part 3: Testing Levels Strategy (25 points)

**File**: `part3-testing-levels.md` (all 4 levels required)

Design a testing strategy for **each testing level**. Explain what will be tested at each level.

**Important**: Use `## [Level Name] Testing` heading for each level (e.g., `## Unit Testing`).

### Template:

```markdown
## Unit Testing

**Scope**: Individual functions/methods/components

**What to Test**:

- [Component 1 and what aspects]
- [Component 2 and what aspects]
- [Component 3 and what aspects]

**Tools**: [e.g., pytest, Jest, JUnit]

**Coverage Goal**: [e.g., 80% code coverage]

**Example Test Cases**:

1. [Specific unit test]
2. [Specific unit test]
3. [Specific unit test]

**Estimated Number of Tests**: [e.g., ~150 unit tests]

---

## Integration Testing

...
```

**Required Coverage**:

- Unit Testing
- Integration Testing
- System Testing
- Acceptance Testing

For each level, provide:

- Clear scope definition
- At least 3 example test cases
- Recommended tools
- Estimated coverage/number of tests

---

## 📝 Part 4: Testing Principles Application (20 points)

**File**: `part4-testing-principles.md` (all 7 principles required)

Apply **each of the seven testing principles** to your application. Explain how each principle influences your testing strategy.

**Important**: Use numbered headings for each principle (e.g., `## 1. Testing Shows Presence of Defects`).

### Template:

```markdown
## 1. Testing Shows Presence of Defects (Not Absence)

**Application to FoodHub**:
Even if all our tests pass, we cannot guarantee the app is bug-free.
Our testing will focus on finding defects in critical areas like
payment processing and order tracking, but we acknowledge that
issues may still exist in less-tested areas.

**Impact on Strategy**:

- Prioritize testing high-risk areas
- Continuous monitoring in production
- Encourage user feedback channels

---

## 2. Exhaustive Testing is Impossible

**Application to FoodHub**:
...
```

Address **all seven principles**:

1. Testing shows presence of defects
2. Exhaustive testing is impossible
3. Early testing
4. Defect clustering
5. Pesticide paradox
6. Testing is context dependent
7. Absence-of-errors fallacy

---

## 📝 Part 5: Risk Analysis & Test Prioritization (10 points)

**File**: `part5-risk-analysis.md` (minimum 6 risks)

Create a risk matrix and prioritize testing efforts.

### 5.1 Risk Matrix

Identify at least 6 risks and classify them using a markdown table:

| **Risk**                   | **Likelihood** | **Impact** | **Priority** | **Mitigation Strategy**                            |
| -------------------------- | -------------- | ---------- | ------------ | -------------------------------------------------- |
| Payment processing failure | Low            | Critical   | P0           | Extensive integration testing with payment gateway |
| Incorrect order totals     | Medium         | High       | P1           | Unit tests for all calculation logic               |
| App crashes under load     | Medium         | High       | P1           | Performance testing with load simulation           |
| ...                        | ...            | ...        | ...          | ...                                                |

**Likelihood**: Low / Medium / High  
**Impact**: Low / Medium / High / Critical  
**Priority**: P0 (Critical) / P1 (High) / P2 (Medium) / P3 (Low)

### 5.2 Testing Priority Order

Based on your risk analysis, list testing activities in priority order:

1. [Highest priority testing activity]
2. [Second priority testing activity]
3. ...

---

## 📤 Submission Requirements

**To receive automated grading and credit**, you must submit your work in this course repository.

### Submission Structure

Create your submission directory in the course repository:

```bash
students/<your-github-username>/homework-2/
```

### Required Files

Submit **5 markdown files** (one for each part) plus a README:

1. **README.md** - Brief overview of your submission

   ```markdown
   # Homework 2: Testing Concepts Analysis

   **Student**: [Your Name]
   **Application**: [Application Name]
   **Date**: [Submission Date]

   ## Summary

   Brief 2-3 sentence summary of your testing strategy for the chosen application.
   ```

2. **part1-application-analysis.md** - Application Selection & Analysis

   - Minimum 300 words
   - Include all sections from Part 1

3. **part2-testing-types.md** - Testing Types Classification

   - At least 8 test types
   - Each type should have a heading: `## Test Type: [Name]`

4. **part3-testing-levels.md** - Testing Levels Strategy

   - All 4 testing levels (Unit, Integration, System, Acceptance)
   - Each level should have a heading: `## Unit Testing`, `## Integration Testing`, etc.

5. **part4-testing-principles.md** - Testing Principles Application

   - All 7 testing principles
   - Each principle should have a numbered heading: `## 1. Testing Shows Presence of Defects`, etc.

6. **part5-risk-analysis.md** - Risk Analysis & Test Prioritization
   - Risk matrix table with at least 6 risks
   - Testing priority order

### Submission Process

1. **Create your branch**:

   ```bash
   git checkout -b feat/<your-username>/homework-2
   ```

2. **Create your directory**:

   ```bash
   mkdir -p students/<your-username>/homework-2
   cd students/<your-username>/homework-2
   ```

3. **Create all required files** in this directory

4. **Commit your work**:

   ```bash
   git add .
   git commit -m "feat: complete homework 2 - testing concepts analysis"
   git push -u origin feat/<your-username>/homework-2
   ```

5. **Create a Pull Request**:
   - Title: `Homework 2: Testing Concepts Analysis - <Your Name>`
   - Base branch: `main`
   - **Add the `homework` label** to your PR
   - Fill out the PR description using the template

**Formatting Guidelines**:

- Use markdown headers (`##`, `###`) for structure
- Include tables where appropriate (use markdown table syntax)
- Use bullet points for lists
- Code blocks for examples (use \`\`\` fences)
- Clear, readable formatting

---

## 🎯 Grading Rubric

| **Category**               | **Points** | **Criteria**                                                                  |
| -------------------------- | ---------- | ----------------------------------------------------------------------------- |
| **Application Analysis**   | 20         | Clear, detailed description; identifies key features and critical functions   |
| **Testing Types**          | 25         | At least 8 types; well-explained with relevant examples; justified priorities |
| **Testing Levels**         | 25         | All four levels covered; specific test cases; appropriate tools identified    |
| **Principles Application** | 20         | All seven principles applied; clear explanations; impacts strategy            |
| **Risk Analysis**          | 10         | Comprehensive risk matrix; logical prioritization; practical mitigation       |
| **Quality & Presentation** | 10         | Well-organized, clear writing, proper formatting, no major errors             |
| **Total**                  | **110**    | (10 points are bonus)                                                         |

### Detailed Criteria:

**Excellent (90-100%)**:

- Thorough analysis with deep understanding
- Creative application of concepts
- Professional presentation
- Goes beyond minimum requirements

**Good (80-89%)**:

- Complete coverage of all requirements
- Clear understanding demonstrated
- Minor gaps or areas for improvement

**Satisfactory (70-79%)**:

- Meets most requirements
- Basic understanding shown
- Some sections need more depth

**Needs Improvement (<70%)**:

- Missing key components
- Superficial analysis
- Significant gaps in understanding

---

## 💡 Tips for Success

1. **Choose wisely**: Pick an application you understand well or research thoroughly
2. **Be specific**: Generic statements get lower scores than specific examples
3. **Think like a tester**: What could go wrong? What's most important?
4. **Use course materials**: Reference concepts from theory documents
5. **Proofread**: Check for clarity, grammar, and formatting
6. **Start early**: This requires thoughtful analysis, not just quick answers

---

## ⚠️ Common Mistakes to Avoid

- ❌ Too generic - "Test that it works" is not a good test description
- ❌ Confusing types and levels - "Unit testing" is a level, not a type
- ❌ Listing without explanation - Always justify your decisions
- ❌ Ignoring non-functional testing - It's as important as functional
- ❌ No prioritization - Not all tests are equally important
- ❌ Poor formatting - Makes it hard to read and grade

---

## 📚 Resources

- [Module 2 Theory Materials](../theory/)
- [ISTQB Glossary](https://glossary.istqb.org/)
- [Testing Types Reference](../theory/02-testing-types.md)
- [Testing Levels Reference](../theory/03-testing-levels.md)
- [Testing Principles Reference](../theory/04-testing-principles.md)

---

## ✅ Submission Checklist

Before submitting, verify:

- [ ] All required files are in `students/<your-username>/homework-2/`
- [ ] README.md is present with basic information
- [ ] part1-application-analysis.md has 300+ words
- [ ] part2-testing-types.md has at least 8 test types with proper headings
- [ ] part3-testing-levels.md covers all 4 testing levels with proper headings
- [ ] part4-testing-principles.md covers all 7 principles with numbered headings
- [ ] part5-risk-analysis.md has risk matrix with at least 6 risks
- [ ] All files are well-formatted markdown and proofread
- [ ] Created a pull request in the course repository
- [ ] Added the `homework` label to your PR
- [ ] All files are committed and pushed to your branch

---

**Good luck!** This assignment will help you think like a professional QA engineer. Take your time and be thorough! 🎯
