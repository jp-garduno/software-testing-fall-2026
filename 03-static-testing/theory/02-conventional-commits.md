# Conventional Commits

## What are Conventional Commits?

**Conventional Commits** is a specification for writing standardized, meaningful commit messages.

**Website**: https://www.conventionalcommits.org/

## Why Use Conventional Commits?

### Benefits

✅ **Automated Changelogs** - Generate from commit history  
✅ **Semantic Versioning** - Automatically determine version bumps  
✅ **Clear History** - Easy to understand what changed  
✅ **Better Collaboration** - Team understands changes quickly  
✅ **Automated Releases** - CI/CD can trigger releases  
✅ **Easy Navigation** - Filter commits by type  
✅ **Professional** - Industry standard practice

## Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Required: Type and Subject

```
feat: add user authentication
```

### Optional: Scope, Body, Footer

```
feat(auth): add JWT token support

Implement JWT tokens for user authentication
with automatic token refresh.

BREAKING CHANGE: Old session tokens no longer supported
Closes #123
```

## Commit Types

### Primary Types

| Type         | Purpose                    | Example                         |
| ------------ | -------------------------- | ------------------------------- |
| **feat**     | New feature                | `feat: add password reset`      |
| **fix**      | Bug fix                    | `fix: correct email validation` |
| **docs**     | Documentation only         | `docs: update API guide`        |
| **style**    | Formatting, no code change | `style: format with prettier`   |
| **refactor** | Code restructuring         | `refactor: simplify auth logic` |
| **test**     | Adding/updating tests      | `test: add login tests`         |
| **chore**    | Maintenance, tooling       | `chore: update dependencies`    |

### Additional Types (Optional)

| Type       | Purpose                 | Example                                |
| ---------- | ----------------------- | -------------------------------------- |
| **perf**   | Performance improvement | `perf: optimize database queries`      |
| **ci**     | CI/CD changes           | `ci: add GitHub Actions workflow`      |
| **build**  | Build system changes    | `build: update webpack config`         |
| **revert** | Revert previous commit  | `revert: revert "feat: add feature X"` |

## Scope (Optional)

The scope specifies **what part** of the codebase is affected.

**Format**: `type(scope): subject`

**Examples**:

```bash
feat(auth): add login functionality
fix(api): correct user validation
docs(readme): update installation steps
test(cart): add checkout tests
```

**Common Scopes**:

- Module names: `auth`, `api`, `database`
- Components: `header`, `footer`, `cart`
- Features: `login`, `checkout`, `search`

## Subject

The subject is a **short description** of the change.

### Rules

1. **Use imperative mood** - "add" not "added" or "adds"
2. **Lowercase** - Don't capitalize first letter
3. **No period** - Don't end with a period
4. **Max 50 characters** - Keep it concise
5. **Describe what, not how** - Focus on the change

### Good Examples

```bash
feat: add user registration
fix: prevent memory leak in parser
docs: update contributing guidelines
style: format code with black
refactor: extract validation logic
test: add edge case tests
chore: bump dependency versions
```

### Bad Examples

```bash
# ❌ Past tense
feat: added user registration

# ❌ Capitalized
feat: Add user registration

# ❌ Period at end
feat: add user registration.

# ❌ Too long
feat: add user registration with email verification and password validation and terms acceptance

# ❌ Too vague
feat: changes
fix: stuff
docs: update
```

## Body (Optional)

Provides **more context** about the change.

### When to Use

- Explain **why** the change was made
- Describe **motivation** behind the change
- Provide **additional details**
- Reference **related issues**

### Format

- Blank line after subject
- Wrap at 72 characters
- Use paragraphs if needed

### Example

```
feat: add password strength meter

Users were creating weak passwords, leading to security
concerns. This adds a real-time password strength indicator
that encourages stronger passwords.

The meter uses zxcvbn library for accurate strength
assessment and provides helpful suggestions.
```

## Footer (Optional)

Contains **metadata** about the commit.

### Common Uses

**Breaking Changes**:

```
BREAKING CHANGE: API endpoint /users changed to /api/users
```

**Issue References**:

```
Closes #123
Fixes #456
Resolves #789
Related to #234
```

**Co-authors**:

```
Co-authored-by: John Doe <john@example.com>
```

### Example

```
feat: migrate to new API

BREAKING CHANGE: All API endpoints now require /api prefix

Closes #123
Closes #456
Co-authored-by: Jane Smith <jane@example.com>
```

## Breaking Changes

**BREAKING CHANGE** indicates an incompatible API change.

### Two Ways to Indicate

**1. In footer**:

```
feat: change user API structure

BREAKING CHANGE: User object structure changed
```

**2. With exclamation mark**:

```
feat!: change user API structure
```

**Both with scope**:

```
feat(api)!: change user endpoint

BREAKING CHANGE: /users endpoint moved to /api/users
```

## Complete Examples

### Simple Commit

```
feat: add dark mode toggle
```

### With Scope

```
fix(auth): correct token expiration check
```

### With Body

```
refactor: simplify database queries

Extracted common query logic into reusable functions.
This reduces code duplication and makes queries easier
to maintain and test.
```

### With Footer

```
feat: add export to CSV feature

Users can now export their data to CSV format.
Export includes all user-selected fields.

Closes #234
Closes #267
```

### Breaking Change

```
feat(api)!: redesign authentication endpoints

BREAKING CHANGE: Authentication now uses JWT tokens.
Old session-based auth is no longer supported.
Clients must update to use Bearer tokens.

Migration guide: docs/migration-jwt.md

Closes #789
```

### Complex Example

```
feat(payment): integrate Stripe payment processor

Add Stripe as a payment option alongside existing
PayPal integration. Users can now choose their
preferred payment method during checkout.

Implementation includes:
- Stripe API integration
- Payment form component
- Webhook handling for payment events
- Error handling and retry logic

Testing performed with Stripe test mode.

Closes #456
Closes #457
Related to #123
Co-authored-by: Alice Chen <alice@example.com>
```

## Real-World Workflow

### Scenario: Fix a Bug

```bash
# 1. Create branch
git checkout -b fix/login-validation

# 2. Fix the bug
# ... edit files ...

# 3. Stage changes
git add src/auth/login.py

# 4. Commit with conventional format
git commit -m "fix(auth): prevent empty password submission

Add validation to ensure password field is not empty
before submitting login form. Previously, empty passwords
were sent to the server, causing unnecessary API calls.

Closes #234"

# 5. Push
git push origin fix/login-validation
```

## Automation Benefits

### Automatic Changelog

```bash
# Commits:
feat: add dark mode
feat: add export feature
fix: correct date formatting
fix: fix memory leak
docs: update readme

# Generated changelog:
## Features
- add dark mode
- add export feature

## Bug Fixes
- correct date formatting
- fix memory leak

## Documentation
- update readme
```

### Automatic Versioning

```bash
# Based on commits:
feat: new feature     → Minor version bump (1.0.0 → 1.1.0)
fix: bug fix         → Patch version bump (1.1.0 → 1.1.1)
BREAKING CHANGE      → Major version bump (1.1.1 → 2.0.0)
```

### Triggering CI/CD

```yaml
# Deploy only on feature commits
if: contains(commit.message, 'feat:')
  deploy_to_staging

# Skip CI on docs changes
if: contains(commit.message, 'docs:')
  skip_ci
```

## Enforcing Conventional Commits

### 1. Git Hooks (Pre-commit)

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: v3.0.0
    hooks:
      - id: conventional-pre-commit
        stages: [commit-msg]
```

### 2. GitHub Actions

```yaml
# .github/workflows/commit-lint.yml
- name: Check Commit Message
  uses: wagoid/commitlint-github-action@v5
```

### 3. Commitizen

Interactive tool that guides you:

```bash
npm install -g commitizen

# Use it
git cz

# Interactive prompts:
? Select type: feat
? What is the scope: auth
? Short description: add login
? Longer description: ...
? Breaking change: No
? Issues closed: #123

# Generates: feat(auth): add login

Closes #123
```

## Configuration File

### commitlint.config.js

```javascript
module.exports = {
  extends: ["@commitlint/config-conventional"],
  rules: {
    "type-enum": [
      2,
      "always",
      ["feat", "fix", "docs", "style", "refactor", "test", "chore"],
    ],
    "subject-case": [2, "always", "lowercase"],
    "subject-empty": [2, "never"],
    "subject-max-length": [2, "always", 50],
    "body-max-line-length": [2, "always", 72],
  },
};
```

## Best Practices

### DO

✅ Use imperative mood: "add feature" not "added feature"  
✅ Keep subject under 50 characters  
✅ Separate subject and body with blank line  
✅ Use body to explain why, not what  
✅ Reference issues in footer  
✅ Use BREAKING CHANGE for incompatible changes

### DON'T

❌ Use past tense: "added feature"  
❌ Capitalize subject: "Add feature"  
❌ End subject with period: "add feature."  
❌ Be vague: "changes", "updates", "fixes"  
❌ Mix multiple changes in one commit  
❌ Skip type prefix

## Common Patterns

### Bug Fixes

```bash
fix: prevent race condition in cache
fix(api): handle timeout errors gracefully
fix(auth): correct token refresh logic
```

### Features

```bash
feat: add search functionality
feat(ui): implement responsive navigation
feat(api): add batch update endpoint
```

### Documentation

```bash
docs: add API examples
docs(readme): update installation steps
docs: fix typos in contributing guide
```

### Refactoring

```bash
refactor: extract common utilities
refactor(db): optimize query performance
refactor: simplify error handling
```

## Team Guidelines Template

```markdown
# Commit Message Guidelines

Use Conventional Commits format:
`type(scope): subject`

## Types

- feat: New feature
- fix: Bug fix
- docs: Documentation
- test: Tests
- refactor: Code restructuring
- style: Formatting
- chore: Maintenance

## Rules

1. Use imperative mood
2. Lowercase subject
3. No period at end
4. Max 50 chars for subject
5. Reference issues: "Closes #123"
6. Mark breaking changes

## Examples

✅ feat(auth): add login
✅ fix: correct validation
❌ Added new feature
❌ Fix stuff
```

## Quick Reference

```bash
# Format
<type>(<scope>): <subject>

# Examples
feat: add feature
fix: fix bug
docs: update docs
style: format code
refactor: restructure
test: add tests
chore: update deps

# With scope
feat(auth): add login
fix(api): correct endpoint

# Breaking change
feat!: change API
BREAKING CHANGE: ...

# With issues
Closes #123
Fixes #456
```

---

## Next Steps

- [Pre-commit Hooks](./03-pre-commit-hooks.md)
- [Linting](./04-linting.md)

## Additional Resources

- [Conventional Commits Website](https://www.conventionalcommits.org/)
- [Commitizen](https://github.com/commitizen/cz-cli)
- [Commitlint](https://commitlint.js.org/)

**Write commits that tell a story!** 📝
