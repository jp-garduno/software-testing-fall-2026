# Exercise 3: Linting Configuration

**Time**: 30-45 minutes  
**Objective**: Configure and customize linters for Python and JavaScript

---

## Part 1: Python - Pylint Configuration

### Step 1: Install Pylint

```bash
pip install pylint
```

### Step 2: Generate Default Configuration

```bash
pylint --generate-rcfile > .pylintrc
```

This creates a `.pylintrc` file with all available options.

### Step 3: Understand Key Settings

Open `.pylintrc` and find these sections:

**[MASTER]** - Basic configuration
```ini
[MASTER]
jobs=0  # Use all CPU cores
```

**[MESSAGES CONTROL]** - Enable/disable warnings
```ini
[MESSAGES CONTROL]
disable=C0111,  # missing-docstring
        C0103,  # invalid-name
        R0903   # too-few-public-methods
```

**[FORMAT]** - Code style
```ini
[FORMAT]
max-line-length=120
indent-string='    '  # 4 spaces
```

### Step 4: Create Custom Configuration

Create a minimal `.pylintrc`:

```ini
[MASTER]
jobs=0
max-line-length=120

[MESSAGES CONTROL]
disable=
    missing-docstring,
    invalid-name,
    too-few-public-methods

[FORMAT]
max-line-length=120
indent-string='    '

[DESIGN]
max-args=7
max-locals=20
max-returns=6
max-branches=15
```

### Step 5: Test Pylint

Create `test_code.py`:

```python
def calculate_total(price, tax_rate, discount, shipping, insurance, handling_fee):
    """Calculate total with many parameters."""
    subtotal = price - discount
    tax = subtotal * tax_rate
    total = subtotal + tax + shipping + insurance + handling_fee
    return total


class MyClass:
    """A class with too many instance attributes."""
    
    def __init__(self):
        self.a = 1
        self.b = 2
        self.c = 3
        self.d = 4
        self.e = 5
        self.f = 6
        self.g = 7
        self.h = 8
        self.i = 9
        self.j = 10


def complex_function(x):
    """Function with too many branches."""
    if x == 1:
        return "one"
    elif x == 2:
        return "two"
    elif x == 3:
        return "three"
    elif x == 4:
        return "four"
    elif x == 5:
        return "five"
    elif x == 6:
        return "six"
    elif x == 7:
        return "seven"
    elif x == 8:
        return "eight"
    elif x == 9:
        return "nine"
    elif x == 10:
        return "ten"
    else:
        return "other"
```

**Run Pylint**:
```bash
pylint test_code.py
```

---

## Part 2: Python - Black Configuration

### Step 1: Install Black

```bash
pip install black
```

### Step 2: Create `pyproject.toml`

```toml
[tool.black]
line-length = 120
target-version = ['py39', 'py310', 'py311']
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.venv
  | build
  | dist
)/
'''
```

### Step 3: Test Black

```bash
black test_code.py
black --check test_code.py  # Check without modifying
black --diff test_code.py   # Show what would change
```

---

## Part 3: JavaScript - ESLint Configuration

### Step 1: Install ESLint

```bash
npm install --save-dev eslint
```

### Step 2: Initialize Configuration

```bash
npx eslint --init
```

Answer the prompts:
- How would you like to use ESLint? **To check syntax and find problems**
- What type of modules? **JavaScript modules (import/export)**
- Which framework? **None**
- Does your project use TypeScript? **No**
- Where does your code run? **Node**
- What format for config? **JSON**

### Step 3: Customize Configuration

Edit `eslint.config.js` (or `.eslintrc.json`):

```javascript
export default [
  {
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'module',
      globals: {
        console: 'readonly',
        process: 'readonly',
      },
    },
    rules: {
      'no-console': 'warn',
      'no-unused-vars': 'error',
      'no-undef': 'error',
      'semi': ['error', 'always'],
      'quotes': ['error', 'single'],
      'indent': ['error', 2],
      'max-len': ['warn', { code: 120 }],
      'eqeqeq': ['error', 'always'],
      'curly': ['error', 'all'],
    },
  },
];
```

### Step 4: Test ESLint

Create `test-code.js`:

```javascript
function calculateTotal(price, taxRate, discount) {
  const subtotal = price - discount
  const tax = subtotal * taxRate
  
  if (tax > 0)
    console.log("Tax applied")
  
  const unusedVariable = 10
  
  return subtotal + tax
}

const result = calculateTotal(100, 0.1, 20)
console.log(result)
```

**Run ESLint**:
```bash
npx eslint test-code.js
```

**Auto-fix**:
```bash
npx eslint test-code.js --fix
```

---

## Part 4: JavaScript - Prettier Configuration

### Step 1: Install Prettier

```bash
npm install --save-dev prettier
```

### Step 2: Create `.prettierrc`

```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "useTabs": false,
  "printWidth": 120,
  "trailingComma": "es5",
  "bracketSpacing": true,
  "arrowParens": "avoid"
}
```

### Step 3: Create `.prettierignore`

```
node_modules/
dist/
build/
coverage/
*.min.js
```

### Step 4: Test Prettier

```bash
npx prettier --write test-code.js
npx prettier --check test-code.js
```

---

## Part 5: Integration

### Integrate ESLint and Prettier

Install compatibility package:

```bash
npm install --save-dev eslint-config-prettier
```

Update ESLint config:

```javascript
import prettierConfig from 'eslint-config-prettier';

export default [
  {
    // ... your existing config
  },
  prettierConfig,  // Disables conflicting rules
];
```

---

## Tasks

### Task 1: Python Configuration

Create `.pylintrc` that:
1. Sets max line length to 100
2. Disables `missing-docstring` warnings
3. Allows up to 8 arguments per function
4. Sets minimum name length to 2 characters

**Test with this code**:
```python
def f(x):  # Short name
    return x * 2

def long_function(a, b, c, d, e, f, g, h, i):  # Too many args
    return sum([a, b, c, d, e, f, g, h, i])
```

### Task 2: JavaScript Configuration

Create ESLint config that:
1. Requires double quotes (not single)
2. Requires 4-space indentation
3. Allows `console.log` (no warning)
4. Enforces semicolons
5. Max line length 100

**Test with this code**:
```javascript
function test(x, y, z) {
    console.log('Testing')
    return x + y + z
}
```

### Task 3: Find Optimal Settings

Run linters on your Homework 1 code and adjust settings to:
- Fix legitimate issues
- Suppress false positives
- Match your team's style preferences

Document 5 rules you changed and why.

---

## Questions

**1.** What's the difference between Pylint and Black?

**Answer:**

**2.** Can ESLint fix all issues automatically?

**Answer:**

**3.** When might you disable a linting rule?

**Answer:**

**4.** How do you disable a rule for one line only?

**Python:**
```python
# pylint: disable=rule-name
```

**JavaScript:**
```javascript
// eslint-disable-next-line rule-name
```

**5.** What happens when Black and Pylint disagree?

**Answer:**

---

## Advanced Challenges

### Challenge 1: Project-specific Rules

Create different linting rules for:
- `src/` (strict)
- `tests/` (relaxed)
- `scripts/` (very relaxed)

### Challenge 2: Custom Pylint Plugin

Create a custom Pylint checker that warns about:
- Functions longer than 50 lines
- Files longer than 500 lines

### Challenge 3: ESLint Custom Rule

Create custom ESLint rule that enforces:
- All functions must have at least one comment
- No function can have more than 20 lines

---

## Submission

Provide:
1. `.pylintrc` file
2. `pyproject.toml` (Black config)
3. `eslint.config.js`
4. `.prettierrc`
5. Screenshots of linting before/after configuration
6. Answers to questions
7. Documentation of 5 rule changes with justification

---

## Resources

- [Pylint Documentation](https://pylint.readthedocs.io/)
- [Black Documentation](https://black.readthedocs.io/)
- [ESLint Rules](https://eslint.org/docs/rules/)
- [Prettier Options](https://prettier.io/docs/en/options.html)
- [Pylint Messages](http://pylint-messages.wikidot.com/all-codes)

---

**Configuration is powerful!** Fine-tune your tools to match your workflow. ⚙️
