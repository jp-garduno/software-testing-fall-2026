# The Seven Testing Principles

These seven fundamental principles guide effective software testing (ISTQB).

## 1. Testing Shows Presence of Defects

**Principle**: Testing can show defects are present, but **cannot prove** there are no defects.

**Example**: 100 passing tests ≠ bug-free software

**Takeaway**: Set realistic expectations

## 2. Exhaustive Testing is Impossible

**Principle**: Testing everything is **not feasible** except in trivial cases.

**Example**: Login with 20-char username/password = more combinations than atoms in universe!

**Takeaway**: Prioritize based on risk

## 3. Early Testing

**Principle**: Start testing **as early as possible** in SDLC.

**Cost**: Bug in requirements costs $100, in production costs $1,000,000

**Takeaway**: Test requirements, design, code - not just at the end

## 4. Defect Clustering

**Principle**: Small number of modules contain **most defects** (80/20 rule).

**Example**: Payment module has 45% of all bugs

**Takeaway**: Focus testing on high-risk modules

## 5. Pesticide Paradox

**Principle**: Same tests repeated won't find **new defects**.

**Analogy**: Like pesticides - bugs develop resistance

**Takeaway**: Update and refresh tests regularly

## 6. Testing is Context Dependent

**Principle**: Different software needs **different testing approaches**.

**Examples**:
- Medical software: Safety-critical
- E-commerce: Performance, security
- Mobile game: Usability, fun

**Takeaway**: Adapt testing to context

## 7. Absence of Errors Fallacy

**Principle**: Bug-free software is **useless** if it doesn't meet user needs.

**Example**: Perfect calculator app, but market doesn't need another calculator

**Takeaway**: Build the right thing, not just bug-free thing

---

## Quick Reference

| Principle | Meaning |
|-----------|---------|
| **Presence of Defects** | Testing finds bugs, can't prove absence |
| **Exhaustive Impossible** | Can't test everything |
| **Early Testing** | Test early, fix cheap |
| **Defect Clustering** | 80/20 rule for bugs |
| **Pesticide Paradox** | Update tests regularly |
| **Context Dependent** | Adapt approach to context |
| **Absence of Errors** | Bug-free ≠ Success |

---

Next: [Exercises](../exercises/)
