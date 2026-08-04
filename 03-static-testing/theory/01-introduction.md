# Introduction to Static Testing

## What is Static Testing?

**Static Testing** examines code **without executing it**. It finds defects by reviewing code, documentation, and design.

### Static vs Dynamic Testing

```
Static Testing (No Execution)
- Code reviews
- Inspections
- Linting
- Static analysis
- Walkthroughs

Dynamic Testing (Execution Required)
- Unit tests
- Integration tests
- System tests
- Performance tests
```

## Why Static Testing?

### Benefits

✅ **Early Detection** - Find bugs before code runs  
✅ **Cheaper** - Fix issues before they become bugs  
✅ **Prevent Defects** - Catch issues in design phase  
✅ **No Test Data Needed** - Review code directly  
✅ **Find More Types** - Logic errors, standards violations, security flaws  
✅ **Improve Quality** - Better code structure and maintainability  

### Cost Comparison

```
Static Testing:  Find issue in code review → $50 to fix
Dynamic Testing: Find issue in testing → $500 to fix
Production:      Find issue in production → $5,000+ to fix
```

## Types of Static Testing

### 1. Manual Static Testing

**Code Reviews**
- Developers review each other's code
- Find logic errors, design issues
- Share knowledge

**Walkthroughs**
- Author presents code to team
- Informal discussion
- Educational

**Inspections**
- Formal process with defined roles
- Follow checklist
- Document findings

### 2. Automated Static Testing

**Linting**
- Analyze code for style violations
- Check coding standards
- Find common mistakes

**Static Analysis**
- Deep code analysis
- Find security vulnerabilities
- Detect complex bugs
- Check code metrics

**Type Checking**
- Verify type correctness
- Catch type errors
- Example: TypeScript, mypy

## What Static Testing Finds

### Common Issues Detected

✅ **Syntax Errors** - Invalid code structure  
✅ **Coding Standard Violations** - Style inconsistencies  
✅ **Security Vulnerabilities** - SQL injection, XSS  
✅ **Code Smells** - Duplicated code, long functions  
✅ **Undefined Variables** - Reference before declaration  
✅ **Unreachable Code** - Dead code paths  
✅ **Type Mismatches** - Incompatible types  
✅ **Logic Errors** - Flawed algorithms  
✅ **Documentation Issues** - Missing or incorrect docs  

### Example

```python
# Static analysis would catch:

def calculate_discount(price):
    if price > 100
        discount = price * 0.1  # Syntax error: missing colon
    else:
        discout = 0  # Typo: 'discout' instead of 'discount'
    
    total = price - discount  # Error: 'discount' undefined in else branch
    return total

# Issues found WITHOUT running the code!
```

## Static Testing in This Module

This module focuses on three key static testing tools:

### 1. Conventional Commits
- Standardized commit messages
- Automated changelog generation
- Better collaboration
- **Theory**: [Conventional Commits](./02-conventional-commits.md)

### 2. Pre-commit Hooks
- Automated checks before commit
- Prevent bad code from being committed
- Enforce quality gates
- **Theory**: [Pre-commit Hooks](./03-pre-commit-hooks.md)

### 3. Linting
- Automated code style checking
- Enforce coding standards
- Find common errors
- **Theory**: [Linting](./04-linting.md)

## Static Testing Workflow

```
1. Write Code
   ↓
2. Save File
   ↓
3. Linter Runs (in editor)
   ↓ (finds issues)
4. Fix Issues
   ↓
5. Stage for Commit (git add)
   ↓
6. Pre-commit Hooks Run
   ↓ (finds issues)
7. Fix Issues
   ↓
8. Commit (with conventional message)
   ↓
9. Code Review
   ↓ (finds issues)
10. Fix Issues
   ↓
11. Merge
```

Multiple layers of static testing!

## Static Testing Best Practices

### 1. Integrate Early
- Set up linting from day one
- Configure pre-commit hooks early
- Establish standards before coding

### 2. Automate Everything
- Use tools, not manual checks
- Run checks automatically
- Fail fast on violations

### 3. Consistent Standards
- Agree on coding standards
- Document the rules
- Apply to entire team

### 4. Fix Issues Immediately
- Don't accumulate violations
- Fix before committing
- Don't disable checks

### 5. Combine with Dynamic Testing
- Static + dynamic = comprehensive
- Static finds different issues
- Both are necessary

## Static vs Dynamic: What Each Finds

### Static Testing Finds

✅ Code style issues  
✅ Syntax errors  
✅ Type errors  
✅ Security vulnerabilities  
✅ Code smells  
✅ Documentation gaps  

### Dynamic Testing Finds

✅ Runtime errors  
✅ Performance issues  
✅ Integration problems  
✅ Incorrect behavior  
✅ Unexpected outputs  

### Both Together = Complete Testing

## Tools for Static Testing

### Code Quality

**Python**
- pylint - Comprehensive linter
- flake8 - Style guide enforcement
- black - Code formatter
- isort - Import sorting
- mypy - Type checking
- bandit - Security linting

**JavaScript/TypeScript**
- ESLint - Linting
- Prettier - Code formatter
- TypeScript - Type checking
- StandardJS - Zero-config linter

### Pre-commit Frameworks
- pre-commit (Python)
- husky (JavaScript)
- lefthook (Go)

### Static Analysis
- SonarQube - Enterprise analysis
- CodeClimate - Code quality
- Codacy - Automated review
- DeepSource - Bug detection

## Real-World Impact

### Case Study: Preventing Production Bug

**Scenario**: Payment calculation bug

**Without Static Testing**:
```python
def calculate_total(price, tax_rate):
    return price + tax_rate  # BUG: Should multiply!

# Committed → Merged → Deployed → Customers charged wrong amounts
# Cost: $50,000 in refunds + reputation damage
```

**With Static Testing**:
```python
def calculate_total(price, tax_rate):
    return price + tax_rate  # Linter: "Suspicious addition of percentage"

# Found during code review before commit
# Cost: 5 minutes to fix
```

### Case Study: Security Vulnerability

**Without Static Testing**:
```python
query = f"SELECT * FROM users WHERE name = '{user_input}'"
# SQL injection vulnerability!

# Deployed → Hacked → Database compromised
# Cost: $500,000+ incident response
```

**With Static Testing**:
```python
query = f"SELECT * FROM users WHERE name = '{user_input}'"
# Bandit: "SQL injection vulnerability detected [HIGH]"

# Found before commit
# Cost: 10 minutes to use parameterized query
```

## Integration with Development Workflow

### IDE Integration
```
Developer writes code
    ↓
IDE shows linting errors in real-time
    ↓
Developer fixes before saving
    ↓
First layer of defense!
```

### Pre-commit Integration
```
Developer commits code
    ↓
Pre-commit hooks run
    ↓
Issues found → Commit blocked
    ↓
Developer fixes issues
    ↓
Second layer of defense!
```

### CI/CD Integration
```
Code pushed to repository
    ↓
CI runs static analysis
    ↓
Issues found → Build fails
    ↓
PR cannot be merged
    ↓
Third layer of defense!
```

## Limitations of Static Testing

### What It Cannot Do

❌ **Cannot find runtime errors** - Need to execute code  
❌ **Cannot test performance** - Need real execution  
❌ **Cannot verify correctness** - Logic may be wrong but syntactically correct  
❌ **Cannot test integration** - Need components to interact  
❌ **May have false positives** - Flags correct code as wrong  

### Example of Limitation

```python
def divide(a, b):
    return a / b

# Static testing: Looks fine!
# Dynamic testing: divide(10, 0) → ZeroDivisionError
```

Static finds syntax/style issues, dynamic finds runtime issues.

## Key Takeaways

1. **Static testing = No execution** - Review code, don't run it
2. **Find issues early** - Cheaper and faster to fix
3. **Automate checks** - Linting, pre-commit, CI/CD
4. **Complement dynamic testing** - Both are necessary
5. **Multiple layers** - IDE → pre-commit → CI/CD
6. **Prevent > Detect** - Stop bad code from being committed
7. **Consistent standards** - Enforce across team

## Next Steps

Learn about the three main static testing tools in this module:

1. **[Conventional Commits](./02-conventional-commits.md)** - Standardized commit messages
2. **[Pre-commit Hooks](./03-pre-commit-hooks.md)** - Automated checks before commit
3. **[Linting](./04-linting.md)** - Code style and quality checking

---

## Additional Resources

- [ISTQB Static Testing](https://www.istqb.org/)
- [SonarQube Rules](https://rules.sonarsource.com/)
- [Google Style Guides](https://google.github.io/styleguide/)

## Questions to Consider

1. How is static testing different from code review?
2. Why is static testing cheaper than dynamic testing?
3. What types of bugs can static testing find that dynamic testing cannot?
4. Why use multiple layers of static testing (IDE, pre-commit, CI)?
5. Can static testing replace dynamic testing? Why or why not?

---

**Static testing catches bugs before they become bugs!** 🔍
