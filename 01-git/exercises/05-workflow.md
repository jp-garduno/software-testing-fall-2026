# Exercise 5: Real-World Workflow

**Difficulty**: Intermediate  
**Time**: 40-45 minutes  
**Objectives**: Simulate complete feature development cycle

## Scenario

You're developing a simple calculator application. You'll implement features using proper Git workflow.

## Part 1: Project Setup

```bash
mkdir calculator-project
cd calculator-project
git init

# Create initial structure
mkdir src tests
touch README.md .gitignore

# Setup .gitignore
cat > .gitignore << EOF
__pycache__/
*.pyc
node_modules/
.env
EOF

# Initial commit
git add .
git commit -m "chore: initialize project structure"

# Create main README
cat > README.md << EOF
# Calculator Project

A simple calculator built with Git best practices.

## Features
- TBD

## Setup
\`\`\`bash
# Instructions coming soon
\`\`\`
EOF

git add README.md
git commit -m "docs: add initial README"
```

## Part 2: Feature 1 - Addition

### Step 1: Create Feature Branch

```bash
git checkout -b feature/add-function
```

### Step 2: Implement Feature

```bash
# Create calculator file
cat > src/calculator.py << EOF
def add(a, b):
    """Add two numbers."""
    return a + b
EOF

git add src/calculator.py
git commit -m "feat(calculator): implement addition function"
```

### Step 3: Add Tests

```bash
cat > tests/test_calculator.py << EOF
from src.calculator import add

def test_add_positive():
    assert add(2, 3) == 5

def test_add_negative():
    assert add(-1, -1) == -2

def test_add_zero():
    assert add(5, 0) == 5
EOF

git add tests/test_calculator.py
git commit -m "test(calculator): add tests for addition"
```

### Step 4: Update Documentation

```bash
# Update README
cat >> README.md << EOF

## Features
- Addition: \`add(a, b)\`
EOF

git add README.md
git commit -m "docs: document addition feature"
```

### Step 5: Merge Feature

```bash
# Switch to main
git checkout main

# Merge feature
git merge feature/add-function --no-ff

# Delete branch
git branch -d feature/add-function

# View history
git log --graph --oneline
```

## Part 3: Feature 2 - Subtraction (Parallel)

### Step 1: New Feature Branch

```bash
git checkout -b feature/subtract-function
```

### Step 2: Implement

```bash
# Add to calculator
cat >> src/calculator.py << EOF

def subtract(a, b):
    """Subtract b from a."""
    return a - b
EOF

git add src/calculator.py
git commit -m "feat(calculator): implement subtraction"

# Add tests
cat >> tests/test_calculator.py << EOF

def test_subtract_positive():
    assert subtract(5, 3) == 2

def test_subtract_negative():
    assert subtract(-1, -1) == 0
EOF

git add tests/test_calculator.py
git commit -m "test(calculator): add subtraction tests"

# Update docs
sed -i '' 's/- Addition:/- Addition: `add(a, b)`\n- Subtraction: `subtract(a, b)`/' README.md
git add README.md
git commit -m "docs: document subtraction feature"
```

### Step 3: Simulate Work on Main

While you were working, someone else updated main:

```bash
# Simulate another commit on main
git checkout main
echo "\n## Installation\npip install -r requirements.txt" >> README.md
git add README.md
git commit -m "docs: add installation section"
```

### Step 4: Update Feature Branch

```bash
# Go back to feature
git checkout feature/subtract-function

# Update with main
git merge main
# OR: git rebase main

# Resolve any conflicts if needed
```

### Step 5: Merge When Ready

```bash
git checkout main
git merge feature/subtract-function --no-ff
git branch -d feature/subtract-function
```

## Part 4: Bug Fix

### Step 1: Create Bug Fix Branch

```bash
git checkout -b fix/edge-case-zero-division
```

### Step 2: Add Division (with bug)

```bash
cat >> src/calculator.py << EOF

def divide(a, b):
    """Divide a by b."""
    return a / b  # BUG: No zero check!
EOF

git add src/calculator.py
git commit -m "feat(calculator): add division"

# Add test that exposes bug
cat >> tests/test_calculator.py << EOF

def test_divide():
    assert divide(10, 2) == 5

def test_divide_by_zero():
    # This will fail!
    try:
        divide(10, 0)
        assert False, "Should raise exception"
    except ZeroDivisionError:
        assert True
EOF

git add tests/test_calculator.py
git commit -m "test(calculator): add division tests"
```

### Step 3: Fix Bug

```bash
# Fix the function
cat > src/calculator.py << EOF
def add(a, b):
    """Add two numbers."""
    return a + b

def subtract(a, b):
    """Subtract b from a."""
    return a - b

def divide(a, b):
    """Divide a by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
EOF

git add src/calculator.py
git commit -m "fix(calculator): handle division by zero"
```

### Step 4: Merge Fix

```bash
git checkout main
git merge fix/edge-case-zero-division --no-ff
git branch -d fix/edge-case-zero-division
```

## Part 5: Release Tagging

```bash
# Tag version
git tag -a v1.0.0 -m "Release version 1.0.0

Features:
- Addition
- Subtraction
- Division (with zero check)
"

# View tags
git tag

# View tag details
git show v1.0.0
```

## Part 6: Hotfix

### Step 1: Critical Bug in Production

```bash
# Branch from tag
git checkout -b hotfix/1.0.1 v1.0.0

# Fix critical bug
echo "# Critical fix for multiply" >> src/calculator.py

git add src/calculator.py
git commit -m "fix: critical production bug"
```

### Step 2: Merge Hotfix

```bash
# Merge to main
git checkout main
git merge hotfix/1.0.1 --no-ff

# Tag new version
git tag -a v1.0.1 -m "Hotfix release 1.0.1"

# Cleanup
git branch -d hotfix/1.0.1
```

## Part 7: View Complete History

```bash
# See everything
git log --graph --oneline --all --decorate

# See only merges
git log --merges --oneline

# See tags
git tag -l

# See branches
git branch -a
```

## Final State

```
Repository:
- src/calculator.py (with all functions)
- tests/test_calculator.py (with all tests)
- README.md (complete documentation)
- .gitignore

Branches:
- main (only)

Tags:
- v1.0.0
- v1.0.1

Commits:
- Initial setup
- Addition feature (3 commits merged)
- Subtraction feature (3 commits merged)
- Bug fix for division (3 commits merged)
- Hotfix (1 commit merged)
```

## Verification Checklist

- [ ] Created at least 4 feature/fix branches
- [ ] Made multiple commits per branch
- [ ] Merged branches with --no-ff
- [ ] Deleted merged branches
- [ ] Created tags for releases
- [ ] Updated documentation with features
- [ ] Followed conventional commits
- [ ] Practiced complete workflow

## Questions

1. Why use `--no-ff` when merging?
2. What's the difference between a feature and a hotfix branch?
3. How do tags help with releases?
4. Why create separate commits for code, tests, and docs?

## Bonus Challenges

1. **Add CI/CD**: Create `.github/workflows/test.yml`
2. **Add Contributing Guide**: Create `CONTRIBUTING.md`
3. **Add License**: Create `LICENSE`
4. **Add Changelog**: Create `CHANGELOG.md`

**Congratulations!** 🎉 You've completed a full Git workflow simulation!
