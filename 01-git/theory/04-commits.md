# Understanding Commits

## What is a Commit?

A commit is a **snapshot** of your project at a specific point in time.

Think of it like a save point in a video game - you can always return to it.

## Anatomy of a Commit

Each commit contains:
- **Unique ID** (SHA hash): `a1b2c3d4e5f6...`
- **Author**: Who made the commit
- **Date**: When it was made
- **Message**: What changed and why
- **Parent**: Previous commit(s)
- **Changes**: Diff of what was added/removed/modified

Example:
```
commit a1b2c3d4e5f6789...
Author: Jane Smith <jane@example.com>
Date:   Mon Jan 15 14:30:00 2026 -0500

    feat: add user authentication

    - Implement login form
    - Add password hashing
    - Create session management
```

## Commit Messages

### Format (Conventional Commits)

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting (no code change)
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

### Examples

**Good**:
```bash
feat(auth): add JWT token authentication
fix(api): correct user validation logic
docs(readme): update installation steps
test(calculator): add edge case tests
```

**Bad**:
```bash
changes
update
fix stuff
asdf
```

## When to Commit?

### Commit Frequently

✅ **Do commit**:
- After completing a logical unit of work
- When tests pass
- Before switching tasks
- At the end of the day
- Before trying something risky

❌ **Don't commit**:
- Broken code (unless on feature branch)
- Half-finished features to main
- Debug statements and commented code
- Sensitive data (passwords, API keys)

### The Goldilocks Principle

- **Too few commits**: Hard to track what changed
- **Too many commits**: Cluttered history
- **Just right**: Each commit = one logical change

## Commit Best Practices

### 1. Write Clear Messages

```bash
# ✅ Imperative mood (like giving a command)
feat: add user dashboard
fix: prevent memory leak in parser

# ❌ Past tense
feat: added user dashboard
fix: fixed memory leak
```

### 2. Keep Commits Focused

```bash
# ✅ One concern per commit
git commit -m "feat: add login form"
git commit -m "test: add login form tests"

# ❌ Multiple unrelated changes
git commit -m "add login, fix bug, update docs, refactor code"
```

### 3. Commit Complete Changes

```bash
# ✅ All related files together
git add login.py login.html login_tests.py
git commit -m "feat: implement login feature"

# ❌ Incomplete feature
git add login.py
git commit -m "feat: start login feature"
# (Missing tests and templates)
```

## Viewing Commits

```bash
# Basic log
git log

# One line per commit
git log --oneline

# With graph
git log --graph --oneline --all

# Last N commits
git log -3

# Search commits
git log --grep="login"
git log --author="Jane"
git log --since="1 week ago"

# Show specific commit
git show a1b2c3d

# Files changed in commit
git show --name-only a1b2c3d
```

## Commit History

### Linear History
```
A -- B -- C -- D (main)
```

### Branched History
```
A -- B -- C -- F (main)
      \
       D -- E (feature)
```

## Atomic Commits

Make each commit "atomic" - a single, complete change.

**Benefits**:
- Easy to understand
- Easy to revert
- Easy to review
- Better history

**Example of atomic commits**:
```bash
commit 1: feat: add database schema for users
commit 2: feat: create User model class
commit 3: feat: implement user registration endpoint
commit 4: test: add tests for user registration
commit 5: docs: document user registration API
```

## Amending Commits

Fix the last commit:

```bash
# Forgot to add a file
git add forgotten_file.py
git commit --amend --no-edit

# Change commit message
git commit --amend -m "New message"

# Add changes and update message
git add another_file.py
git commit --amend
```

⚠️ **Warning**: Only amend unpushed commits!

## Commit Tips

1. **Use imperative mood**: "add feature" not "added feature"
2. **Explain why, not what**: Code shows what; commit message explains why
3. **Reference issues**: "fix: resolve user login bug (#123)"
4. **Keep first line under 50 chars**
5. **Add detailed body if needed**
6. **Review before committing**: `git diff --staged`

## Example Workflow

```bash
# 1. Make changes
vim calculator.py

# 2. Review changes
git diff

# 3. Stage changes
git add calculator.py

# 4. Review staged changes
git diff --staged

# 5. Commit with good message
git commit -m "feat: add multiplication function

- Implement multiply() method
- Handle edge cases (zero, negative)
- Add input validation"

# 6. View history
git log --oneline -3
```

## Next Steps

- [Branching](./05-branching.md)
- [Merging](./06-merging.md)
- [Pull Requests](./07-pull-requests.md)
