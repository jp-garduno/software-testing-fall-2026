# Common Commands Reference

## Development Setup

### Initial Setup

```bash
# Clone repository
git clone https://github.com/[username]/software-testing-fall-2026.git
cd software-testing-fall-2026

# Python environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# JavaScript environment
npm install

# Pre-commit hooks
pre-commit install
```

### Updating Dependencies

```bash
# Python
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt

# JavaScript
npm update
npm audit fix
```

## Testing Commands

### Python Tests

```bash
# Run all tests
pytest

# Run specific module tests
pytest 04-black-box-testing/

# Run with coverage
pytest --cov=. --cov-report=html --cov-report=term

# Run with verbose output
pytest -v

# Run specific test file
pytest test_calculator.py

# Run tests matching pattern
pytest -k "test_addition"

# Stop at first failure
pytest -x

# Show print statements
pytest -s
```

### JavaScript Tests

```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm run test:watch

# Run specific file
npm test -- calculator.test.js

# Run tests matching pattern
npm test -- -t "addition"

# Update snapshots
npm test -- -u
```

### Playwright Tests

```bash
# Run E2E tests
npm run playwright

# Run in headed mode (see browser)
npm run playwright:headed

# Run in UI mode
npm run playwright:ui

# Run specific test
npx playwright test login.spec.js
```

## Code Quality

### Python Linting and Formatting

```bash
# Check with Pylint
pylint **/*.py

# Check specific file
pylint module.py

# Format with Black
black .

# Check formatting (no changes)
black --check .

# Sort imports
isort .

# Type checking with mypy
mypy .
```

### JavaScript Linting and Formatting

```bash
# Lint all files
npm run lint

# Fix auto-fixable issues
npm run lint:fix

# Format with Prettier
npm run format

# Check specific file
npx eslint file.js
```

### Pre-commit Hooks

```bash
# Run on all files
pre-commit run --all-files

# Run on staged files only
pre-commit run

# Update hooks
pre-commit autoupdate

# Skip hooks (not recommended)
git commit --no-verify
```

## Git Workflow

### Branch Management

```bash
# Create and switch to new branch
git checkout -b feat/homework-4

# List branches
git branch -a

# Switch branches
git checkout main

# Delete local branch
git branch -d feat/old-feature

# Delete remote branch
git push origin --delete feat/old-feature
```

### Committing

```bash
# Stage changes
git add file.py

# Commit with message (conventional commits)
git commit -m "feat(module-4): add boundary value analysis exercises"

# Amend last commit
git commit --amend

# Stage all changes
git add .
```

### Syncing

```bash
# Pull latest changes
git pull origin main

# Push changes
git push origin feat/homework-4

# Fetch without merging
git fetch origin

# Rebase on main
git rebase main
```

### Stashing

```bash
# Stash changes
git stash

# Stash with message
git stash save "WIP: working on homework"

# List stashes
git stash list

# Apply latest stash
git stash pop

# Apply specific stash
git stash apply stash@{0}
```

## Coverage Reports

### Python Coverage

```bash
# Generate HTML report
pytest --cov=. --cov-report=html
# Open: htmlcov/index.html

# Generate terminal report
pytest --cov=. --cov-report=term

# Generate XML (for CI/CD)
pytest --cov=. --cov-report=xml

# Check coverage threshold
pytest --cov=. --cov-fail-under=80
```

### JavaScript Coverage

```bash
# Generate coverage
npm test -- --coverage

# Open HTML report
open coverage/lcov-report/index.html  # macOS
start coverage/lcov-report/index.html # Windows
```

## Module-Specific Commands

### Black Box Testing (Module 4)

```bash
# Run black box tests
pytest 04-black-box-testing/

# With coverage
pytest 04-black-box-testing/ --cov=04-black-box-testing --cov-report=html
```

### TDD (Module 6)

```bash
# Run in watch mode for TDD
pytest --watch  # requires pytest-watch

# Or use npm for JavaScript TDD
npm run test:watch
```

### System Testing (Module 8)

```bash
# Run Behave (BDD) tests
behave

# Run specific feature
behave features/login.feature

# Run Playwright E2E
npm run playwright

# Run Selenium tests
pytest selenium/tests/
```

### Performance Testing (Module 9)

```bash
# Run JMeter test plan (non-GUI)
jmeter -n -t test-plan.jmx -l results.jtl -e -o report/

# Run Locust (Python)
locust -f locustfile.py --host=http://example.com
```

## Cleanup

### Remove Generated Files

```bash
# Python
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
rm -rf .pytest_cache
rm -rf htmlcov
rm -rf .coverage

# JavaScript
rm -rf node_modules
rm -rf coverage
rm -rf playwright-report
rm -rf .npm

# Both
rm -rf .tox
rm -rf dist
rm -rf build
```

### Reset Environment

```bash
# Python
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# JavaScript
rm -rf node_modules package-lock.json
npm install
```

## GitHub Actions

### Triggering Workflows

```bash
# Push triggers CI
git push origin main

# Create PR triggers validation
gh pr create --title "feat: add exercise" --body "Description"

# Manual trigger (if workflow_dispatch enabled)
gh workflow run ci.yml
```

### Viewing Results

```bash
# List workflows
gh workflow list

# View run status
gh run list

# View specific run
gh run view [run-id]

# Watch run
gh run watch
```

## Quick References

### Running Full Test Suite

```bash
# Everything at once
pytest && npm test && pre-commit run --all-files
```

### Before Submitting PR

```bash
# Run all checks
pre-commit run --all-files
pytest --cov=. --cov-report=term
npm test
git status
git diff
```

### Common Issues

**Tests failing in CI but passing locally:**

```bash
# Ensure clean state
git status
pre-commit run --all-files

# Check Python version
python --version

# Check Node version
node --version
```

**Coverage too low:**

```bash
# Generate report to see what's missing
pytest --cov=. --cov-report=html
open htmlcov/index.html
```

**Pre-commit hooks failing:**

```bash
# Run manually to see errors
pre-commit run --all-files

# Update hooks
pre-commit autoupdate

# Clear cache
pre-commit clean
```
