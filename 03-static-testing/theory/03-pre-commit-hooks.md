# Pre-commit Hooks

## What are Pre-commit Hooks?

**Pre-commit hooks** are scripts that run **automatically before** you commit code. They check code quality and prevent bad code from being committed.

## How They Work

```
1. Developer runs: git commit
   ↓
2. Pre-commit hooks run automatically
   ↓
3. If hooks pass: Commit succeeds ✅
   If hooks fail: Commit blocked ❌
   ↓
4. Developer fixes issues
   ↓
5. Try commit again
```

## Why Use Pre-commit Hooks?

✅ **Prevent bad code** - Catch issues before commit  
✅ **Enforce standards** - Automatic checking  
✅ **Save time** - Find issues locally, not in CI  
✅ **Consistent quality** - Same checks for everyone  
✅ **No manual checking** - Automated quality gates

## Pre-commit Framework

**Website**: https://pre-commit.com/

### Installation

```bash
pip install pre-commit
```

### Setup

1. **Create configuration file** (`.pre-commit-config.yaml`)
2. **Install hooks**: `pre-commit install`
3. **Hooks run automatically** on `git commit`

## Configuration File

### Basic Example

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
```

### Python Project Example

```yaml
repos:
  # General checks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: detect-private-key

  # Python formatting
  - repo: https://github.com/psf/black
    rev: 24.1.1
    hooks:
      - id: black

  # Python import sorting
  - repo: https://github.com/PyCQA/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: [--profile=black]

  # Python linting
  - repo: https://github.com/PyCQA/pylint
    rev: v3.0.3
    hooks:
      - id: pylint
```

### JavaScript Project Example

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json

  # JavaScript/TypeScript
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.1.0
    hooks:
      - id: prettier
        types_or: [javascript, jsx, ts, tsx, json]

  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.56.0
    hooks:
      - id: eslint
        files: \.(js|jsx|ts|tsx)$
```

## Common Hooks

### File Checks

- `trailing-whitespace` - Remove trailing spaces
- `end-of-file-fixer` - Ensure newline at EOF
- `check-added-large-files` - Prevent large files
- `check-merge-conflict` - Detect merge markers
- `check-yaml` - Validate YAML syntax
- `check-json` - Validate JSON syntax

### Security

- `detect-private-key` - Find private keys
- `detect-aws-credentials` - Find AWS credentials

### Python

- `black` - Code formatter
- `isort` - Sort imports
- `pylint` - Linter
- `mypy` - Type checking
- `pytest` - Run tests

### JavaScript

- `prettier` - Code formatter
- `eslint` - Linter
- `tsc` - TypeScript compiler

## Using Pre-commit

### Install Hooks

```bash
# In your repository
pre-commit install
```

### Run Manually

```bash
# Run on all files
pre-commit run --all-files

# Run on staged files
pre-commit run

# Run specific hook
pre-commit run black
```

### Update Hooks

```bash
pre-commit autoupdate
```

## Workflow Example

```bash
# 1. Edit file
echo "hello world" > test.py

# 2. Stage file
git add test.py

# 3. Try to commit
git commit -m "feat: add test file"

# Pre-commit runs:
# - trailing-whitespace.............Passed
# - end-of-file-fixer...............Failed
# - black...........................Failed

# 4. Hooks auto-fix some issues
# Files were modified by this hook. Additional output:
# test.py

# 5. Stage fixed files
git add test.py

# 6. Commit again
git commit -m "feat: add test file"
# All hooks pass! ✅
```

## Hook Configuration

### Arguments

```yaml
- repo: https://github.com/psf/black
  rev: 24.1.1
  hooks:
    - id: black
      args: [--line-length=120]
```

### File Types

```yaml
- repo: https://github.com/pre-commit/mirrors-prettier
  rev: v3.1.0
  hooks:
    - id: prettier
      types_or: [javascript, jsx, ts, tsx]
```

### Exclude Files

```yaml
- repo: https://github.com/psf/black
  rev: 24.1.1
  hooks:
    - id: black
      exclude: ^migrations/
```

## Advanced Features

### Stages

```yaml
- repo: https://github.com/compilerla/conventional-pre-commit
  rev: v3.0.0
  hooks:
    - id: conventional-pre-commit
      stages: [commit-msg]
```

**Stages**:

- `commit` - Before commit (default)
- `commit-msg` - Check commit message
- `push` - Before push
- `merge-commit` - Merge commits

### Local Hooks

```yaml
- repo: local
  hooks:
    - id: pytest
      name: pytest
      entry: pytest
      language: system
      pass_filenames: false
      always_run: true
```

## Best Practices

### DO

✅ Install hooks for all team members  
✅ Keep hooks fast (< 10 seconds)  
✅ Auto-fix when possible  
✅ Update hooks regularly  
✅ Document in README

### DON'T

❌ Skip hooks with `--no-verify`  
❌ Make hooks too slow  
❌ Run extensive tests in pre-commit  
❌ Fail on warnings (only errors)

## Skipping Hooks

### When to Skip

Only skip hooks for:

- Emergency hotfixes
- Work-in-progress commits
- Known issues being fixed

### How to Skip

```bash
# Skip all hooks
git commit --no-verify -m "message"

# Or
git commit -n -m "message"
```

**⚠️ Use sparingly!**

## Troubleshooting

### Hook Failed But No Error

```bash
# Run manually to see details
pre-commit run --all-files
```

### Hook Too Slow

```bash
# Remove slow hook or optimize
# Consider running in CI instead
```

### Hook Conflicts

```bash
# Clear cache and reinstall
pre-commit clean
pre-commit install
```

## Integration with CI

Pre-commit can also run in CI:

```yaml
# .github/workflows/pre-commit.yml
name: Pre-commit
on: [pull_request]
jobs:
  pre-commit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - uses: pre-commit/action@v3.0.0
```

## Quick Reference

```bash
# Install
pip install pre-commit
pre-commit install

# Run
pre-commit run --all-files

# Update
pre-commit autoupdate

# Skip (rarely!)
git commit --no-verify
```

Next: [Linting](./04-linting.md)
