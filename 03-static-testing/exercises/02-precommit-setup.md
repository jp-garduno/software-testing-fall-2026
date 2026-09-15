# Exercise 2: Pre-commit Setup

**Time**: 30 minutes  
**Objective**: Set up pre-commit hooks from scratch

---

## Part 1: Project Setup

Create a new project directory:

```bash
mkdir static-testing-practice
cd static-testing-practice
git init
```

---

## Part 2: Install Pre-commit

**Python method**:

```bash
pip install pre-commit
```

**Or via system package manager** (macOS):

```bash
brew install pre-commit
```

**Verify installation**:

```bash
pre-commit --version
```

---

## Part 3: Create Configuration File

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files
        args: ["--maxkb=500"]

  - repo: https://github.com/psf/black
    rev: 24.1.1
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/PyCQA/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: [--profile=black]
```

---

## Part 4: Install Hooks

```bash
pre-commit install
```

Expected output:

```
pre-commit installed at .git/hooks/pre-commit
```

---

## Part 5: Create Test Files

**Create `calculator.py`**:

```python
def add(a,b):
    return a+b

def subtract(a,b):
    return a-b

def multiply(a,  b):
    return a*b
```

**Create `README.md`**:

```markdown
# Calculator

A simple calculator.
```

---

## Part 6: Test Pre-commit

**Stage files**:

```bash
git add .
```

**Try to commit**:

```bash
git commit -m "add calculator"
```

**What happens?**

- Pre-commit runs automatically
- Checks find issues
- Commit is blocked

**Expected issues**:

1. Trailing whitespace in README
2. No newline at end of file
3. Inconsistent spacing in Python

---

## Part 7: View Changes

Pre-commit automatically fixes some issues:

```bash
git diff
```

**Notice**:

- Black formatted Python code
- Trailing whitespace removed
- End-of-file fixer added newlines

---

## Part 8: Commit Again

**Stage fixed files**:

```bash
git add .
```

**Commit**:

```bash
git commit -m "add calculator"
```

**Success!** ✅

---

## Part 9: Test on All Files

Run pre-commit on all files (without committing):

```bash
pre-commit run --all-files
```

---

## Part 10: Add More Hooks

Update `.pre-commit-config.yaml` to add Pylint:

```yaml
- repo: https://github.com/PyCQA/pylint
  rev: v3.0.3
  hooks:
    - id: pylint
      args: [--max-line-length=120]
```

**Update hooks**:

```bash
pre-commit install --install-hooks
```

**Test again**:

```bash
pre-commit run --all-files
```

---

## Questions to Answer

**1.** What happens if you try to commit without staging the fixed files?

**Answer:**

---

**2.** Can you bypass pre-commit hooks? How?

**Answer:**

---

**3.** What's the difference between `pre-commit install` and `pre-commit run`?

**Answer:**

---

**4.** Where are pre-commit hooks stored?

**Answer:**

---

**5.** How would you temporarily disable a specific hook?

**Answer:**

---

## Challenges

### Challenge 1: Add JavaScript Support

Add ESLint hook to your configuration:

```yaml
- repo: https://github.com/pre-commit/mirrors-eslint
  rev: v8.56.0
  hooks:
    - id: eslint
      files: \.[jt]sx?$
      types: [file]
```

Create a JavaScript file with issues and test.

### Challenge 2: Conventional Commits Hook

Add conventional commits checker:

```yaml
- repo: https://github.com/compilerla/conventional-pre-commit
  rev: v3.0.0
  hooks:
    - id: conventional-pre-commit
      stages: [commit-msg]
```

Install commit-msg hook:

```bash
pre-commit install --hook-type commit-msg
```

Try committing with a bad message:

```bash
git commit -m "bad message"
```

What happens?

### Challenge 3: Custom Hook

Add a custom hook that checks for TODO comments:

```yaml
- repo: local
  hooks:
    - id: check-todos
      name: Check for TODOs
      entry: bash -c 'grep -r "TODO" . || exit 0'
      language: system
      pass_filenames: false
```

Does it work? Why or why not?

---

## Submission

Document your process:

1. Screenshot of successful pre-commit run
2. Screenshot of hook blocking bad commit
3. Your final `.pre-commit-config.yaml`
4. Answers to questions
5. At least one challenge completed

---

## Common Issues

**Issue**: `command not found: pre-commit`
**Solution**: Install pre-commit with pip or brew

**Issue**: Hooks not running
**Solution**: Run `pre-commit install` to install hooks

**Issue**: Hook fails every time
**Solution**: Check configuration syntax in YAML file

**Issue**: Want to commit anyway
**Solution**: Use `git commit --no-verify` (not recommended!)

---

## Resources

- [Pre-commit Documentation](https://pre-commit.com/)
- [Available Hooks](https://pre-commit.com/hooks.html)
- [Creating Custom Hooks](https://pre-commit.com/#creating-new-hooks)

---

**Great job!** You now have automated quality checks running on every commit! 🎉
