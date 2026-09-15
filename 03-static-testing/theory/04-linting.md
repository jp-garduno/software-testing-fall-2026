# Linting

## What is Linting?

**Linting** is automated checking of source code for programmatic and stylistic errors.

**Name origin**: Lint was a Unix tool that examined C code (like removing lint from clothing).

## Why Lint?

✅ **Catch errors early** - Before code runs  
✅ **Enforce standards** - Consistent code style  
✅ **Improve quality** - Prevent common mistakes  
✅ **Save time** - Auto-fix many issues  
✅ **Team consistency** - Everyone follows same rules  
✅ **Learning tool** - Teaches best practices

## What Linters Find

### Errors

- Undefined variables
- Syntax errors
- Type mismatches
- Import errors

### Code Quality

- Unused variables
- Unreachable code
- Complexity warnings
- Duplicated code

### Style

- Indentation
- Line length
- Naming conventions
- Import ordering

### Security

- SQL injection risks
- XSS vulnerabilities
- Weak cryptography
- Insecure functions

## Python Linting

### Pylint

**Most comprehensive Python linter**

```bash
# Install
pip install pylint

# Run
pylint myfile.py
pylint mypackage/

# Output
************* Module myfile
myfile.py:1:0: C0114: Missing module docstring (missing-module-docstring)
myfile.py:5:4: E0602: Undefined variable 'result' (undefined-variable)

Your code has been rated at 7.50/10
```

**Features**:

- Error detection
- Code smells
- Refactoring suggestions
- Style checking
- Configurable rules

**Configuration** (`.pylintrc` or `pyproject.toml`):

```ini
[MASTER]
max-line-length=120
disable=missing-docstring,too-few-public-methods

[MESSAGES CONTROL]
enable=all
disable=C0111,C0103
```

### Black

**Opinionated Python formatter**

```bash
# Install
pip install black

# Format
black myfile.py

# Check only
black --check myfile.py
```

**Features**:

- Zero configuration
- Consistent style
- Fast
- Deterministic

### isort

**Import statement organizer**

```bash
pip install isort

# Sort imports
isort myfile.py

# With black compatibility
isort --profile=black myfile.py
```

### Flake8

**Style guide enforcement**

```bash
pip install flake8

flake8 myfile.py
```

Checks PEP 8 compliance.

### mypy

**Static type checker**

```bash
pip install mypy

mypy myfile.py
```

## JavaScript/TypeScript Linting

### ESLint

**Pluggable JavaScript linter**

```bash
# Install
npm install --save-dev eslint

# Initialize
npx eslint --init

# Run
npx eslint file.js
npx eslint src/
```

**Configuration** (`eslint.config.js` or `.eslintrc.js`):

```javascript
export default [
  {
    rules: {
      "no-unused-vars": "error",
      "no-console": "warn",
      semi: ["error", "always"],
      quotes: ["error", "single"],
    },
  },
];
```

**Popular Configs**:

- `eslint:recommended`
- `airbnb`
- `standard`
- `google`

### Prettier

**Opinionated code formatter**

```bash
npm install --save-dev prettier

# Format
npx prettier --write file.js

# Check
npx prettier --check file.js
```

**Configuration** (`.prettierrc`):

```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5"
}
```

### TypeScript Compiler

```bash
# Type check
npx tsc --noEmit

# Check specific file
npx tsc file.ts --noEmit
```

## IDE Integration

### VS Code

**Python**:

```json
// settings.json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true
}
```

**JavaScript**:

```json
{
  "eslint.enable": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "editor.defaultFormatter": "esbenp.prettier-vscode"
}
```

## Common Linting Rules

### Python

**Error Detection**:

- `E0602`: Undefined variable
- `E1101`: No member
- `E0401`: Import error

**Code Quality**:

- `R0913`: Too many arguments
- `R0914`: Too many local variables
- `W0612`: Unused variable

**Style**:

- `C0103`: Invalid name
- `C0301`: Line too long
- `C0111`: Missing docstring

### JavaScript

**Error Detection**:

- `no-undef`: Undefined variable
- `no-unused-vars`: Unused variable
- `no-unreachable`: Unreachable code

**Best Practices**:

- `eqeqeq`: Use === instead of ==
- `no-eval`: Don't use eval()
- `no-console`: No console.log

**Style**:

- `semi`: Require semicolons
- `quotes`: Single or double quotes
- `indent`: Indentation

## Auto-fixing

Many linters can fix issues automatically:

```bash
# Python
black myfile.py
isort myfile.py

# JavaScript
npx eslint --fix file.js
npx prettier --write file.js
```

## Ignoring Warnings

### Inline Ignores

**Python**:

```python
result = dangerous_operation()  # pylint: disable=no-member
```

**JavaScript**:

```javascript
// eslint-disable-next-line no-console
console.log("Debug message");
```

### File-level Ignores

**Python**:

```python
# pylint: disable=missing-docstring
```

**JavaScript**:

```javascript
/* eslint-disable no-console */
```

### Configuration Ignores

**Python** (`.pylintrc`):

```ini
[MESSAGES CONTROL]
disable=missing-docstring,too-many-arguments
```

**JavaScript** (`.eslintrc.js`):

```javascript
{
  "rules": {
    "no-console": "off",
    "no-unused-vars": "warn"
  }
}
```

## Best Practices

### DO

✅ Enable linting from project start  
✅ Use IDE integration  
✅ Auto-fix on save  
✅ Run in pre-commit hooks  
✅ Run in CI/CD  
✅ Agree on rules as team

### DON'T

❌ Disable too many rules  
❌ Ignore all warnings  
❌ Skip linting "just this once"  
❌ Have inconsistent configs  
❌ Over-configure (keep it simple)

## Linting Workflow

```
1. Write code
   ↓
2. IDE shows linting errors in real-time
   ↓
3. Fix issues as you type
   ↓
4. Save → Auto-format (Black/Prettier)
   ↓
5. Commit → Pre-commit runs linters
   ↓
6. Push → CI runs linters
```

## Quick Reference

**Python**:

```bash
pip install pylint black isort
pylint myfile.py
black myfile.py
isort --profile=black myfile.py
```

**JavaScript**:

```bash
npm install --save-dev eslint prettier
npx eslint file.js --fix
npx prettier --write file.js
```

**Pre-commit Integration**: See [Pre-commit Hooks](./03-pre-commit-hooks.md)

---

Next: [Exercises](../exercises/)
