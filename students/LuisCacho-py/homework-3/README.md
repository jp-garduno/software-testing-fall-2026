# Homework 3 — Static Testing Setup

**Student:** Luis Cacho (`LuisCacho-py`)
**Module:** 3 — Static Testing

## Project Description

A Python utility library that demonstrates complete static testing
infrastructure, including pre-commit hooks, linting, formatting, and
security scanning.

## Project Structure

```
homework-3/
├── src/
│   ├── __init__.py          # Package public API
│   ├── calculator.py        # Basic arithmetic operations
│   ├── validator.py         # Input validation utilities
│   └── statistics_utils.py  # Descriptive statistics functions
├── .pre-commit-config.yaml  # Pre-commit hooks (12 hooks)
├── .pylintrc                # Pylint configuration
├── pyproject.toml           # Bandit security scan config
├── REPORT.md                # Static analysis report (500+ words)
└── README.md                # This file
```

## Tools Used

| Tool | Version | Purpose |
|------|---------|---------|
| pre-commit | ≥ 3.6 | Hook orchestration |
| Black | 24.1.1 | Code formatting |
| isort | 5.13.2 | Import sorting |
| Pylint | 3.0.3 | Static analysis |
| Bandit | 1.7.7 | Security scanning |

## Setup

```bash
# Install dependencies
pip install pre-commit pylint black isort bandit

# Install pre-commit hooks (run once)
pre-commit install

# Run hooks on all files
pre-commit run --all-files

# Run Pylint
pylint src/ > pylint-report.txt

# Run Bandit security scan
bandit -r src/ -c pyproject.toml
```

## Results

- **Pre-commit:** All 12 hooks pass ✅
- **Pylint score:** > 9.5/10 ✅
- **Bandit:** Zero medium/high severity issues ✅
- **Issues fixed:** 6 linting issues documented in [REPORT.md](REPORT.md)

## Conventional Commits Used

```
feat(homework-3): add initial project setup with src modules
feat(homework-3): add pre-commit hooks configuration
feat(homework-3): add pylint and bandit linting configuration
fix(homework-3): resolve pylint issues - line length and naming
fix(homework-3): remove unused imports and add missing docstrings
docs(homework-3): add static analysis report
```
