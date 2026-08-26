# Homework 3: Static Testing Setup

**Module**: 3 - Static Testing  
**Due Date**: End of Week 4  
**Points**: 100  
**Estimated Time**: 3-4 hours

---

## 🎯 Objectives

This homework will help you:

- Set up pre-commit hooks for a project
- Configure linting tools
- Write conventional commit messages
- Generate a static analysis report
- Understand the benefits of static testing

---

## 📋 Assignment Overview

You will set up complete static testing infrastructure for a Python or JavaScript project, configure all tools, and write a report on your findings.

---

## 📝 Part 1: Project Setup (15 points)

### Choose a Project

**Option A**: Use your Homework 1 (Git) project  
**Option B**: Create a new simple project (calculator, todo list, etc.)  
**Option C**: Use an existing personal project

### Requirements

- At least 3 Python OR JavaScript files **in `src/` directory**
- At least 100 lines of code total (excluding tests)
- Code should have some intentional issues for linters to find
- Include test files (`test_*.py` or `*.test.js`)

---

## 📝 Part 2: Configure Pre-commit (25 points)

### Step 1: Install Pre-commit

```bash
pip install pre-commit
```

### Step 2: Create Configuration File

Create `.pre-commit-config.yaml` with:

**For Python projects**:

- trailing-whitespace
- end-of-file-fixer
- check-yaml
- check-json
- check-added-large-files
- black
- isort
- pylint

**For JavaScript projects**:

- trailing-whitespace
- end-of-file-fixer
- check-yaml
- check-json
- prettier
- eslint

### Step 3: Install Hooks

```bash
pre-commit install
```

### Step 4: Run on All Files

```bash
pre-commit run --all-files
```

**Deliverable**: `.pre-commit-config.yaml` file with 5+ hooks configured

---

## 📝 Part 3: Configure Linting (30 points)

### For Python

**1. Create `.pylintrc`** configuration:

```bash
pylint --generate-rcfile > .pylintrc
```

Edit to customize rules.

**2. Run Pylint**:

```bash
pylint yourfile.py > pylint-report.txt
```

**3. Format with Black**:

```bash
black .
```

**4. Sort imports with isort**:

```bash
isort --profile=black .
```

### For JavaScript

**1. Initialize ESLint**:

```bash
npx eslint --init
```

**2. Create `.prettierrc`**:

```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2
}
```

**3. Run ESLint**:

```bash
npx eslint . > eslint-report.txt
```

**4. Format with Prettier**:

```bash
npx prettier --write .
```

**Deliverables**:

- Configuration files (`.pylintrc` or `.eslintrc.js`)
- Source code files with linting applied
- Optionally: linting report files for reference (not graded)

---

## 📝 Part 4: Fix Issues (15 points)

Fix at least **5 issues** found by linters.

**Document fixes in your REPORT.md** (Part 6) or as code comments. Example documentation format:

````markdown
### Issue 1

- **Tool**: Pylint
- **Error**: C0301: Line too long (120/100)
- **Location**: calculator.py:15
- **Fix**: Split line into multiple lines
- **Before**:
  ```python
  # code before
  ```
````

- **After**:
  ```python
  # code after
  ```

**Deliverable**: Fixed code with issues resolved, documented in REPORT.md

---

## 📝 Part 5: Conventional Commits (10 points)

Commit all changes using conventional commits format.

**Required commits** (at least 5 total):

1. Initial project setup
2. Add pre-commit configuration
3. Add linting configuration
4. Fix linting issues (multiple commits, one per fix or group)
5. Update documentation

**Deliverable**: Git history with conventional commits (verified automatically by grading system)

---

## 📝 Part 6: Analysis Report (15 points)

**File**: `REPORT.md` (minimum 500 words, markdown format)

Write a report (500-700 words) covering:

### 1. Issues Found

- How many issues did linters find?
- What categories (style, errors, complexity, etc.)?
- Which issues were most common?

### 2. Benefits Observed

- What problems did static testing catch?
- Would these have been found by manual review?
- How long did setup take vs potential time saved?

### 3. Integration

- How would you integrate this into team workflow?
- When should each tool run (IDE, pre-commit, CI)?

### 4. Recommendations

- Which tools were most useful?
- What would you change about the configuration?
- Would you use this in future projects? Why?

**Deliverable**: `REPORT.md` file (markdown format, 500+ words)

---

## 📤 Submission Requirements

**To receive automated grading and credit**, you must submit your work in this course repository.

### Submission Structure

Create your submission directory in the course repository:

```bash
students/<your-github-username>/homework-3/
```

### Required Files

Your submission directory must include:

**README.md Template**:

```markdown
# Homework 3: Static Testing Setup

**Student**: [Your Name]
**Project**: [Project Name]
**Language**: Python/JavaScript

## Description

Brief description of your project (2-3 sentences)

## Setup Instructions

1. Install dependencies
2. Install pre-commit hooks
3. Run the project

## Pre-commit Hooks Configured

- List your configured hooks

## Testing

Instructions to run tests
```

**Directory Structure**:

```
students/<your-username>/homework-3/
├── README.md                      # Project overview and setup instructions
├── .pre-commit-config.yaml        # Pre-commit configuration (5+ hooks required)
├── .pylintrc or .eslintrc.js      # Linter configuration
├── .prettierrc                    # Prettier config (if JavaScript)
├── requirements.txt               # Python dependencies (if Python)
├── package.json                   # Node dependencies (if JavaScript)
├── src/                           # Source code directory
│   ├── *.py or *.js              # At least 3 files, 100+ lines total
│   └── ...
├── test_*.py or *.test.js         # Test files
└── REPORT.md                      # Analysis report (500+ words, markdown format)
```

**Important**:

- **REPORT.md** must be in markdown format (not PDF), minimum 500 words
- Source files must be in `src/` directory
- At least 3 source files required
- At least 100 lines of code total in `src/`
- Pre-commit config must have 5+ hooks

### Submission Process

1. **Create your branch**:

   ```bash
   git checkout -b feat/<your-username>/homework-3
   ```

2. **Create your directory**:

   ```bash
   mkdir -p students/<your-username>/homework-3
   cd students/<your-username>/homework-3
   ```

3. **Complete all work in this directory**

4. **Commit with conventional commits** (at least 5 commits required):

   ```bash
   git add .
   git commit -m "feat: add initial project setup"
   git commit -m "chore: configure pre-commit hooks"
   git commit -m "chore: configure linting tools"
   git commit -m "fix: resolve linting issues"
   git commit -m "docs: add analysis report"
   ```

5. **Push your branch**:

   ```bash
   git push -u origin feat/<your-username>/homework-3
   ```

6. **Create a Pull Request**:
   - Title: `Homework 3: Static Testing Setup - <Your Name>`
   - Base branch: `main`
   - **Add the `homework` label** to your PR
   - Fill out the PR description using the template

---

## 🎯 Grading Rubric

| **Category**             | **Points** | **Criteria**                                    |
| ------------------------ | ---------- | ----------------------------------------------- |
| **Project Setup**        | 15         | Project with sufficient code, runs successfully |
| **Pre-commit Config**    | 25         | Correct configuration, hooks installed and work |
| **Linting Config**       | 30         | Proper configuration, reports generated         |
| **Issue Fixes**          | 15         | At least 5 issues documented and fixed          |
| **Conventional Commits** | 10         | All commits follow format, meaningful messages  |
| **Analysis Report**      | 15         | Complete analysis, thoughtful insights          |
| **Documentation**        | 5          | Clear README, well-organized                    |
| **Total**                | **110**    | (10 bonus points available)                     |

### Bonus Points

- **+5**: Configure CI/CD to run static analysis
- **+3**: Add security linting (bandit for Python, eslint-plugin-security for JS)
- **+2**: Create a team style guide document

---

## 💡 Tips for Success

1. **Start early** - Setup takes time the first time
2. **Test incrementally** - Run tools after each configuration
3. **Read error messages** - Linters explain what's wrong
4. **Use auto-fix** - Let Black/Prettier fix style automatically
5. **Don't disable everything** - Learn from the warnings
6. **Document as you go** - Take screenshots when you encounter issues

---

## ⚠️ Common Mistakes to Avoid

- ❌ Committing configuration files with invalid syntax
- ❌ Not running pre-commit before trying to commit
- ❌ Disabling too many linting rules
- ❌ Using vague conventional commit messages
- ❌ Not documenting issues found and fixed
- ❌ Submitting project without testing pre-commit works

---

## 🆘 Getting Help

- Review [Module 3 theory materials](../theory/)
- Check [pre-commit documentation](https://pre-commit.com/)
- Ask in course discussion forum
- Attend office hours

---

## 📚 Resources

- [Pre-commit Hooks](https://pre-commit.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Pylint Documentation](https://pylint.readthedocs.io/)
- [ESLint Documentation](https://eslint.org/)
- [Black Documentation](https://black.readthedocs.io/)
- [Prettier Documentation](https://prettier.io/)

---

## ✅ Submission Checklist

Before submitting:

- [ ] All files are in `students/<your-username>/homework-3/`
- [ ] At least 5 commits with conventional commit messages
- [ ] Pre-commit config has 5+ hooks and works (test with a commit)
- [ ] At least 3 source files in `src/` directory
- [ ] At least 100 lines of code total in `src/`
- [ ] Test files present (test\__.py or _.test.js)
- [ ] Linting configuration is valid (.pylintrc or .eslintrc.js)
- [ ] REPORT.md written (500+ words in markdown format)
- [ ] README.md includes project overview and setup instructions
- [ ] requirements.txt or package.json present with dependencies
- [ ] Created a pull request in the course repository
- [ ] Added the `homework` label to your PR
- [ ] All files are committed and pushed to your branch

---

**Good luck!** This homework sets up habits that will make you a better developer! 🚀

```

```
