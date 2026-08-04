# Module 3: Static Testing

## 🎯 Learning Objectives

By the end of this module, you will be able to:
- Understand the benefits of static testing vs dynamic testing
- Write commit messages following Conventional Commits specification
- Configure and use pre-commit hooks
- Set up and use linters (Pylint, ESLint)
- Integrate static analysis into your development workflow
- Prevent common bugs before code execution

## 📚 Theory Materials

### [1. Introduction to Static Testing](./theory/01-introduction.md)
- Static vs Dynamic testing
- Benefits of early defect detection
- Types of static testing
- Code reviews and inspections

### [2. Conventional Commits](./theory/02-conventional-commits.md)
- Commit message standards
- Commit types (feat, fix, docs, etc.)
- Benefits for collaboration and automation
- Semantic versioning connection

### [3. Pre-commit Hooks](./theory/03-pre-commit-hooks.md)
- What are Git hooks
- Setting up pre-commit framework
- Configuring hooks
- Common pre-commit hooks

### [4. Linting](./theory/04-linting.md)
- Purpose of linting
- Pylint for Python
- ESLint for JavaScript
- Configuration and customization
- Integrating with editors

## 🛠️ Setup Instructions

### Install Pre-commit Framework
```bash
pip install pre-commit
```

### Create `.pre-commit-config.yaml`
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-yaml
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 24.1.1
    hooks:
      - id: black

  - repo: https://github.com/PyCQA/pylint
    rev: v3.0.3
    hooks:
      - id: pylint
```

### Install Hooks
```bash
pre-commit install
```

### Python Linting
```bash
pip install pylint black isort
pylint your_file.py
black your_file.py
```

### JavaScript Linting
```bash
npm install --save-dev eslint
npx eslint your_file.js --fix
```

## 💻 Practical Exercises

### [Exercise 1: Conventional Commits Practice](./exercises/01-conventional-commits-practice.md)
Rewrite bad commit messages using Conventional Commits.

### [Exercise 2: Pre-commit Setup](./exercises/02-precommit-setup.md)
Set up pre-commit hooks for a project from scratch.

### [Exercise 3: Linting Configuration](./exercises/03-linting-config.md)
Configure Pylint and ESLint with custom rules.

### [Exercise 4: Fix Linting Issues](./exercises/04-fix-issues.md)
Given code with linting errors, fix all issues.

## 📝 Homework Assignment

**[Homework 3: Static Testing Setup](./homework/homework-3.md)**

**Due**: End of Week 4

**Objectives**: 
- Configure static testing tools for a project
- Set up pre-commit hooks
- Configure linters
- Write a report on findings

## 📖 Conventional Commits Quick Reference

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, no code change
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

**Examples**:
```
feat(auth): add login functionality
fix(cart): correct total calculation
docs(readme): update installation instructions
style: format code with black
test(user): add user validation tests
```

## 🎯 Self-Assessment Checklist

- [ ] Understand benefits of static testing
- [ ] Write proper conventional commit messages
- [ ] Set up pre-commit hooks
- [ ] Configure Pylint for Python
- [ ] Configure ESLint for JavaScript
- [ ] Fix linting issues
- [ ] Integrate static testing into workflow

## 🚀 Next Steps

- Complete [Homework 3](./homework/homework-3.md)
- Preview [Module 4: Black Box Testing](../04-black-box-testing/README.md)
- Prepare for **Exam 1** (Week 6, Session 2)
