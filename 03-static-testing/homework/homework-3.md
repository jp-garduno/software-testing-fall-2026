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

- At least 3 Python OR JavaScript files
- At least 100 lines of code total
- Code should have some intentional issues for linters to find

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

**Deliverable**: Screenshot of pre-commit run output

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
- Configuration files
- Linting report (before fixes)
- Screenshot showing issues found

---

## 📝 Part 4: Fix Issues (15 points)

Fix at least **5 issues** found by linters.

**Document each fix**:
```markdown
### Issue 1
- **Tool**: Pylint
- **Error**: C0301: Line too long (120/100)
- **Location**: calculator.py:15
- **Fix**: Split line into multiple lines
- **Before**:
  ```python
  # code before
  ```
- **After**:
  ```python
  # code after
  ```
```

**Deliverable**: Document with 5+ fixes

---

## 📝 Part 5: Conventional Commits (10 points)

Commit all changes using conventional commits format.

**Required commits**:
1. Initial project setup
2. Add pre-commit configuration
3. Add linting configuration
4. Fix linting issues (multiple commits, one per fix or group)
5. Update documentation

**Deliverable**: Screenshot of `git log --oneline` showing conventional commits

---

## 📝 Part 6: Analysis Report (15 points)

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

**Deliverable**: PDF report

---

## 📤 Submission Requirements

### GitHub Repository

Your repository must include:

```
your-project/
├── .pre-commit-config.yaml
├── .pylintrc or eslint.config.js
├── .prettierrc (if JavaScript)
├── src/ (your code files)
├── README.md (updated with setup instructions)
├── reports/
│   ├── pylint-report.txt or eslint-report.txt
│   ├── issues-fixed.md
│   └── analysis-report.pdf
└── screenshots/
    ├── pre-commit-output.png
    ├── git-log.png
    └── linting-issues.png
```

### Canvas Submission

Submit:
1. **GitHub repository URL**
2. **Analysis report** (PDF)
3. **Reflection** (200-300 words): What did you learn about static testing?

---

## 🎯 Grading Rubric

| **Category** | **Points** | **Criteria** |
|--------------|------------|--------------|
| **Project Setup** | 15 | Project with sufficient code, runs successfully |
| **Pre-commit Config** | 25 | Correct configuration, hooks installed and work |
| **Linting Config** | 30 | Proper configuration, reports generated |
| **Issue Fixes** | 15 | At least 5 issues documented and fixed |
| **Conventional Commits** | 10 | All commits follow format, meaningful messages |
| **Analysis Report** | 15 | Complete analysis, thoughtful insights |
| **Documentation** | 5 | Clear README, well-organized |
| **Total** | **110** | (10 bonus points available) |

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
- [ ] All files committed with conventional commits
- [ ] Pre-commit hooks work (test with a commit)
- [ ] Linting configuration is valid
- [ ] At least 5 issues documented and fixed
- [ ] All required screenshots taken
- [ ] Analysis report written (500-700 words)
- [ ] README updated with setup instructions
- [ ] Repository is public and accessible
- [ ] GitHub URL submitted to Canvas

---

**Good luck!** This homework sets up habits that will make you a better developer! 🚀
