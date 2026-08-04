# Exercise 4: Fix Linting Issues

**Time**: 45 minutes  
**Objective**: Practice fixing real linting issues

---

## Part 1: Python Code with Issues

### Code: `calculator.py`

```python
import sys
import os

def add(a,b):
  return a+b

def subtract(x, y):
    result=x-y
    return result


def multiply(a,b,):
    return a*b



def divide(numerator,denominator):
  if denominator==0:
    print("Cannot divide by zero")
    return None
  return numerator/denominator


class Calculator():
  def __init__(self):
    self.history=[]

  def calculate(self,operation,a,b):
    if operation=="add":
      result=a+b
    elif operation=="subtract":
      result=a-b
    elif operation=="multiply":
      result=a*b
    elif operation=="divide":
      if b==0:
        return None
      result=a/b
    else:
      return None

    self.history.append(result)
    return result

  def get_history(self):
    return self.history


unused_variable = 42


def complex_function(x):
  if x<0:
    if x<-10:
      if x<-20:
        return "very negative"
      else:
        return "negative"
    else:
      return "slightly negative"
  else:
    if x>0:
      if x>10:
        if x>20:
          return "very positive"
        else:
          return "positive"
      else:
        return "slightly positive"
    else:
      return "zero"
```

---

## Part 2: Run Pylint

```bash
pip install pylint
pylint calculator.py
```

**Record the output:**

- How many errors?
- How many warnings?
- What's the score?

---

## Part 3: Categorize Issues

Group the issues by type:

### Style Issues (C)

- Example: Line too long

### Refactor Suggestions (R)

- Example: Too many branches

### Warnings (W)

- Example: Unused import

### Errors (E)

- Example: Syntax error

### Fatal (F)

- Example: Cannot open file

---

## Part 4: Fix Issues Systematically

### Step 1: Fix Imports

**Issues**:

- Unused imports (`sys`, `os`)

**Fix**:

```python
# Remove unused imports
```

---

### Step 2: Fix Formatting

**Issues**:

- Inconsistent spacing around operators
- Inconsistent indentation
- Too many blank lines
- Trailing comma in function parameters

**Fix with Black**:

```bash
pip install black
black calculator.py
```

---

### Step 3: Fix Naming

**Issues**:

- Class name has unnecessary parentheses

**Before**:

```python
class Calculator():
```

**After**:

```python
class Calculator:
```

---

### Step 4: Fix Comparison

**Issues**:

- Using `==` to compare with `None`
- Using `==` for string comparison (debatable)

**Before**:

```python
if denominator==0:
```

**After**:

```python
if denominator == 0:  # Black fixes spacing
```

---

### Step 5: Fix Complexity

**Issue**: `complex_function` has too many nested blocks

**Before**: (See above)

**After**:

```python
def complex_function(x):
    """Classify number by magnitude."""
    if x < -20:
        return "very negative"
    if x < -10:
        return "negative"
    if x < 0:
        return "slightly negative"
    if x == 0:
        return "zero"
    if x <= 10:
        return "slightly positive"
    if x <= 20:
        return "positive"
    return "very positive"
```

---

### Step 6: Remove Unused Code

**Issue**: `unused_variable` is never used

**Fix**: Delete it or prefix with underscore:

```python
_unused_variable = 42  # Explicitly unused
```

---

### Step 7: Add Docstrings

**Issue**: Missing module and function docstrings

**Fix**:

```python
"""Calculator module with basic arithmetic operations."""


def add(a, b):
    """Add two numbers."""
    return a + b


def subtract(x, y):
    """Subtract y from x."""
    result = x - y
    return result
```

---

## Part 5: JavaScript Code with Issues

### Code: `calculator.js`

```javascript
function add(a, b) {
  return a + b;
}

function subtract(x, y) {
  const result = x - y;
  return result;
}

function multiply(a, b) {
  return a * b;
}

function divide(numerator, denominator) {
  if (denominator == 0) {
    console.log("Cannot divide by zero");
    return null;
  }
  return numerator / denominator;
}

class Calculator {
  constructor() {
    this.history = [];
  }

  calculate(operation, a, b) {
    let result;
    if (operation == "add") {
      result = a + b;
    } else if (operation == "subtract") {
      result = a - b;
    } else if (operation == "multiply") {
      result = a * b;
    } else if (operation == "divide") {
      if (b == 0) return null;
      result = a / b;
    } else {
      return null;
    }

    this.history.push(result);
    return result;
  }

  getHistory() {
    return this.history;
  }
}

const unusedVariable = 42;

function complexFunction(x) {
  if (x < 0) {
    if (x < -10) {
      if (x < -20) {
        return "very negative";
      } else {
        return "negative";
      }
    } else {
      return "slightly negative";
    }
  } else {
    if (x > 0) {
      if (x > 10) {
        if (x > 20) {
          return "very positive";
        } else {
          return "positive";
        }
      } else {
        return "slightly positive";
      }
    } else {
      return "zero";
    }
  }
}

module.exports = { Calculator, add, subtract, multiply, divide };
```

---

## Part 6: Run ESLint

```bash
npm install --save-dev eslint
npx eslint calculator.js
```

**Record the output:**

- How many errors?
- How many warnings?

---

## Part 7: Fix JavaScript Issues

### Auto-fix What You Can

```bash
npx eslint calculator.js --fix
```

### Manually Fix Remaining Issues

**Issue**: `==` instead of `===`

**Before**:

```javascript
if (denominator == 0) {
```

**After**:

```javascript
if (denominator === 0) {
```

**Issue**: Unused variable

```javascript
// Remove or rename with underscore prefix
const _unusedVariable = 42;
```

**Issue**: Complexity in `complexFunction`

Same fix as Python version - use early returns.

---

## Part 8: Run Prettier

```bash
npm install --save-dev prettier
npx prettier --write calculator.js
```

This will fix:

- Spacing
- Semicolons
- Brace style
- Indentation

---

## Tasks

For each codebase:

1. **Run linter and record initial score**
2. **Categorize all issues**
3. **Fix issues one category at a time**
4. **Run linter after each fix**
5. **Achieve 10/10 Pylint score** (or as close as possible)
6. **Achieve 0 ESLint errors**

---

## Deliverables

### 1. Issue Report

| Language   | Initial Score | Final Score | Issues Fixed |
| ---------- | ------------- | ----------- | ------------ |
| Python     |               |             |              |
| JavaScript |               |             |              |

### 2. Detailed Fix Log

For each issue fixed:

````markdown
#### Issue #1

- **Tool**: Pylint
- **Code**: C0303
- **Message**: Trailing whitespace
- **Location**: Line 15
- **Before**:
  ```python
  return result
  ```
````

- **After**:
  ```python
  return result
  ```

````

Create at least **10 fix logs** (5 Python, 5 JavaScript).

### 3. Reflection

**Questions**:

1. Which issues were easy to fix automatically?
2. Which required manual refactoring?
3. Which rules would you disable? Why?
4. How long did it take to fix all issues?
5. Would you prefer to fix issues as you write code or in batch?

---

## Bonus Challenges

### Challenge 1: Complexity Metrics

Before and after refactoring:
- Count cyclomatic complexity
- Count lines of code
- Measure function length

Tools:
```bash
pip install radon
radon cc calculator.py
radon mi calculator.py
````

### Challenge 2: Coverage

Add tests and check if linting helps coverage:

```bash
pytest --cov=calculator
```

### Challenge 3: Pre-commit Integration

Configure pre-commit to catch these issues automatically.

---

## Common Mistakes to Avoid

❌ **Blindly disabling rules** - Understand why they exist first
❌ **Fixing only some issues** - Be consistent
❌ **Not testing after changes** - Linting fixes can break code
❌ **Formatting manually** - Use Black/Prettier
❌ **Not committing incrementally** - Commit after each major fix

✅ **Understand each issue**
✅ **Fix by category**
✅ **Test after each change**
✅ **Use auto-formatters**
✅ **Commit often**

---

## Resources

- [Pylint Messages Reference](http://pylint-messages.wikidot.com/)
- [ESLint Rules](https://eslint.org/docs/rules/)
- [Cyclomatic Complexity](https://en.wikipedia.org/wiki/Cyclomatic_complexity)

---

**Clean code starts with addressing linting warnings!** 🧹
