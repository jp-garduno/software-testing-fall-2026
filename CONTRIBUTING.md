# Contributing to Software Testing Fall 2026

Thank you for contributing to this course repository! This guide will help you understand how to contribute effectively.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Contribution Workflow](#contribution-workflow)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing Guidelines](#testing-guidelines)

---

## 📜 Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Accept constructive criticism gracefully
- Focus on what is best for the learning community
- Show empathy towards other community members

### Unacceptable Behavior

- Harassment or discriminatory language
- Trolling or insulting comments
- Publishing others' private information
- Cheating or plagiarism
- Other conduct inappropriate in a professional setting

---

## 🚀 Getting Started

### Prerequisites

1. **Git** installed and configured
2. **GitHub account** set up
3. **Development environment** configured:
   - Python 3.11+
   - Node.js 22+
   - Code editor (VS Code recommended)

### Initial Setup

1. **Fork the repository** (if contributing to main repo)

   ```bash
   # Click "Fork" button on GitHub
   ```

2. **Clone your fork**

   ```bash
   git clone https://github.com/YOUR-USERNAME/software-testing-fall-2026.git
   cd software-testing-fall-2026
   ```

3. **Add upstream remote**

   ```bash
   git remote add upstream https://github.com/ORIGINAL-OWNER/software-testing-fall-2026.git
   ```

4. **Install dependencies**

   ```bash
   # Python
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt

   # JavaScript
   npm install
   ```

5. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

---

## 🔄 Contribution Workflow

### 1. Create a Branch

Always create a new branch for your work:

```bash
git checkout -b <type>/<description>
```

**Branch naming conventions**:

- `feat/add-new-exercise` - New feature or content
- `fix/correct-typo-in-readme` - Bug fix
- `docs/update-module-3` - Documentation only
- `refactor/reorganize-tests` - Code refactoring
- `chore/update-dependencies` - Maintenance

### 2. Make Your Changes

- Write clear, concise code
- Follow style guidelines (enforced by linters)
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes

```bash
# Python tests
pytest

# JavaScript tests
npm test

# Run linters
pylint your_file.py
npm run lint
```

### 4. Commit Your Changes

Follow [Conventional Commits](#commit-message-guidelines):

```bash
git add .
git commit -m "feat(module-4): add boundary value analysis exercises"
```

### 5. Keep Your Branch Updated

```bash
git fetch upstream
git rebase upstream/main
```

### 6. Push Your Changes

```bash
git push origin <your-branch-name>
```

### 7. Create Pull Request

- Go to GitHub and create a Pull Request
- Fill out the PR template
- Link related issues
- Request review from maintainers

---

## 📝 Commit Message Guidelines

We follow the **Conventional Commits** specification.

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation only changes
- **style**: Code style changes (formatting, no logic change)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Maintenance tasks, dependencies
- **perf**: Performance improvements
- **ci**: CI/CD changes

### Scope

The scope indicates which module or area is affected:

- `module-1`, `module-2`, ..., `module-9`
- `exam-1`, `exam-2`, `exam-3`
- `project`
- `docs`
- `config`

### Subject

- Use imperative mood: "add" not "added" or "adds"
- Don't capitalize first letter
- No period at the end
- Maximum 50 characters

### Examples

```
feat(module-4): add equivalence partitioning exercises

Added three new exercises focusing on equivalence partitioning:
- Credit card validation
- Date validation
- Flight booking eligibility

Closes #42

---

fix(module-5): correct coverage calculation example

The example in theory/02-coverage.md had incorrect percentage.
Updated to show proper formula.

---

docs(readme): update installation instructions

Added troubleshooting section for Windows users experiencing
issues with pre-commit hooks.

---

test(module-6): add TDD kata solutions

Added example solutions for:
- FizzBuzz kata
- String calculator kata
- Bowling game kata

---

chore: update dependencies to latest versions

Updated pytest to 8.0.0 and jest to 29.7.0.
All tests still pass.
```

---

## 🔀 Pull Request Process

### Before Creating a PR

1. ✅ All tests pass
2. ✅ Linters report no errors
3. ✅ Documentation is updated
4. ✅ Commit messages follow convention
5. ✅ Branch is up-to-date with main

### PR Title

Use conventional commit format:

```
feat(module-4): add decision table exercises
```

### PR Description Template

```markdown
## Description

Brief description of what this PR does.

## Type of Change

- [ ] New feature (feat)
- [ ] Bug fix (fix)
- [ ] Documentation (docs)
- [ ] Refactoring (refactor)
- [ ] Tests (test)
- [ ] Other (chore, style, perf, ci)

## Changes Made

- Change 1
- Change 2
- Change 3

## Related Issues

Closes #123
Related to #456

## Testing

- [ ] Existing tests pass
- [ ] New tests added (if applicable)
- [ ] Manual testing completed

## Screenshots (if applicable)

Add screenshots here

## Checklist

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No merge conflicts
- [ ] PR is ready for review
```

### Review Process

1. **Automated checks** must pass (CI/CD)
2. **At least one reviewer** must approve
3. **Resolve all comments** before merging
4. **Squash and merge** for cleaner history (optional)

### After PR is Merged

1. **Delete your branch** (if appropriate)

   ```bash
   git branch -d <branch-name>
   git push origin --delete <branch-name>
   ```

2. **Update your local main**
   ```bash
   git checkout main
   git pull upstream main
   ```

---

## 🎨 Code Style Guidelines

### Python

Follow **PEP 8** with these specifics:

- Line length: 120 characters
- Use Black for formatting
- Use isort for import sorting
- Docstrings for all public functions/classes

```python
def calculate_discount(price: float, discount_rate: float) -> float:
    """
    Calculate the discounted price.

    Args:
        price: Original price
        discount_rate: Discount percentage (0-100)

    Returns:
        Discounted price

    Raises:
        ValueError: If price is negative or discount_rate is invalid
    """
    if price < 0:
        raise ValueError("Price cannot be negative")
    if not 0 <= discount_rate <= 100:
        raise ValueError("Discount rate must be between 0 and 100")

    return price * (1 - discount_rate / 100)
```

### JavaScript/TypeScript

Follow **Airbnb Style Guide** with ESLint:

- Use modern ES6+ syntax
- Prefer const/let over var
- Use arrow functions when appropriate
- JSDoc for public functions

```javascript
/**
 * Calculate the discounted price
 * @param {number} price - Original price
 * @param {number} discountRate - Discount percentage (0-100)
 * @returns {number} Discounted price
 * @throws {Error} If inputs are invalid
 */
function calculateDiscount(price, discountRate) {
  if (price < 0) {
    throw new Error("Price cannot be negative");
  }
  if (discountRate < 0 || discountRate > 100) {
    throw new Error("Discount rate must be between 0 and 100");
  }

  return price * (1 - discountRate / 100);
}
```

### General Guidelines

- **Naming**:

  - Use descriptive names
  - Functions: `verb_noun` (Python) or `verbNoun` (JavaScript)
  - Classes: `PascalCase`
  - Constants: `UPPER_SNAKE_CASE`

- **Comments**:

  - Explain WHY, not WHAT
  - Update comments when code changes
  - Remove commented-out code

- **File Organization**:
  - One class per file (when practical)
  - Group related functions
  - Clear imports at the top

---

## 🧪 Testing Guidelines

### Writing Tests

1. **Test file naming**:

   - Python: `test_<module>.py`
   - JavaScript: `<module>.test.js` or `<module>.spec.js`

2. **Test function naming**:

   - Descriptive: `test_calculate_discount_with_valid_inputs`
   - Use `test_` prefix in Python

3. **Test structure** (Arrange-Act-Assert):

   ```python
   def test_calculate_discount_applies_correctly():
       # Arrange
       price = 100
       discount_rate = 20

       # Act
       result = calculate_discount(price, discount_rate)

       # Assert
       assert result == 80
   ```

4. **Coverage requirements**:
   - Aim for 80%+ coverage for new code
   - Test happy paths and edge cases
   - Test error conditions

### Running Tests

```bash
# Python - all tests
pytest

# Python - specific file
pytest tests/test_calculator.py

# Python - with coverage
pytest --cov=. --cov-report=html

# JavaScript - all tests
npm test

# JavaScript - watch mode
npm run test:watch

# JavaScript - with coverage
npm test -- --coverage
```

---

## ❓ Questions or Issues?

- **General questions**: Use GitHub Discussions
- **Bug reports**: Open an issue with details
- **Feature requests**: Open an issue with proposal
- **Security issues**: Email the instructor directly (don't open public issue)

---

## 📚 Additional Resources

- [Git Workflow](./01-git/README.md)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Python PEP 8](https://www.python.org/dev/peps/pep-0008/)
- [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- [Writing Good Pull Requests](https://github.blog/2015-01-21-how-to-write-the-perfect-pull-request/)

---

Thank you for contributing! Your efforts help make this course better for everyone. 🎓✨
