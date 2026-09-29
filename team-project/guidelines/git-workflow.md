# Git Workflow Guidelines

## 🌳 Branching Strategy

### Branch Types

```
main (production-ready)
  └── develop (integration branch)
      ├── feature/user-authentication
      ├── feature/product-catalog
      ├── fix/cart-calculation-bug
      └── hotfix/security-patch
```

### Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `hotfix/description` - Urgent production fixes
- `chore/description` - Maintenance tasks
- `docs/description` - Documentation only

**Examples**:

- `feature/user-authentication`
- `fix/cart-total-calculation`
- `chore/update-dependencies`
- `docs/api-documentation`

### Branch Protection Rules

**main branch**:

- ✅ Require pull request reviews (minimum 1)
- ✅ Require status checks to pass
- ✅ No direct commits
- ✅ No force push

**develop branch**:

- ✅ Require pull request reviews (minimum 1)
- ✅ Require status checks to pass
- ⚠️ Team leads can merge without review (use sparingly)

---

## 📝 Commit Messages

### Conventional Commits Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation changes
- `style` - Code style changes (formatting, no logic change)
- `refactor` - Code refactoring
- `test` - Adding or updating tests
- `chore` - Maintenance tasks

### Examples

**Good commits**:

```bash
feat(auth): add JWT token generation

Implements token-based authentication using PyJWT.
Tokens expire after 24 hours.

Closes #42
```

```bash
fix(cart): correct total calculation when discount applied

The discount was being applied twice when using percentage-based codes.
Now correctly applies discount only once.

Fixes #67
```

```bash
test(orders): add unit tests for order validation

Added 8 new test cases covering:
- Valid order creation
- Invalid payment method
- Out of stock items
- Address validation
```

**Bad commits**:

```bash
update stuff
fixed bug
WIP
asdf
```

### Commit Best Practices

1. **Keep commits atomic** - One logical change per commit
2. **Write clear subjects** - Max 50 characters, imperative mood
3. **Explain the why** - Body should explain motivation, not what changed
4. **Reference issues** - Use "Closes #123" or "Fixes #456"
5. **Don't commit broken code** - Every commit should leave code in working state

---

## 🔄 Pull Request Workflow

### Creating a Pull Request

1. **Create feature branch**

   ```bash
   git checkout develop
   git pull
   git checkout -b feature/user-profile
   ```

2. **Make changes and commit**

   ```bash
   # Make changes
   git add src/profile.py tests/test_profile.py
   git commit -m "feat(profile): add user profile page"
   ```

3. **Keep branch updated**

   ```bash
   git checkout develop
   git pull
   git checkout feature/user-profile
   git merge develop
   # Resolve conflicts if any
   ```

4. **Push branch**

   ```bash
   git push -u origin feature/user-profile
   ```

5. **Create PR on GitHub**
   - Use PR template
   - Add description
   - Link related issues
   - Request reviewers
   - Add labels

### PR Size Guidelines

- **Small PR**: < 200 lines changed ✅ Preferred
- **Medium PR**: 200-400 lines ⚠️ Acceptable
- **Large PR**: > 400 lines ❌ Split it up

**Tip**: If your PR is getting large, break it into multiple smaller PRs.

### PR Review Process

1. **Author creates PR** - Clear description, tests passing
2. **Reviewers review** - Within 48 hours
3. **Author addresses feedback** - Make changes or discuss
4. **Reviewers approve** - At least 1 approval required
5. **Author merges** - Delete branch after merge

---

## 🔀 Merging Strategies

### Merge to develop

**Use**: Squash and merge

- Keeps develop history clean
- All commits from feature branch become one commit
- Useful for small features

```bash
# GitHub will do this automatically when you select "Squash and merge"
```

### Merge to main

**Use**: Create a merge commit

- Preserves milestone history
- Shows when features were integrated
- Used for milestone completion

```bash
# GitHub will do this automatically when you select "Merge commit"
```

---

## 🚫 Common Mistakes

### ❌ Committing directly to main

**Wrong**:

```bash
git checkout main
git add .
git commit -m "quick fix"
git push
```

**Right**:

```bash
git checkout -b fix/quick-fix
git add .
git commit -m "fix(api): correct endpoint URL"
git push -u origin fix/quick-fix
# Create PR
```

### ❌ Not syncing with develop

**Problem**: Your branch gets outdated and creates conflicts

**Solution**: Sync regularly

```bash
git checkout develop
git pull
git checkout feature/your-feature
git merge develop
# Resolve conflicts immediately
```

### ❌ Mixing unrelated changes

**Wrong**: One commit with auth changes + cart changes + styling

**Right**: Separate commits for each logical change

```bash
git add src/auth.py tests/test_auth.py
git commit -m "feat(auth): add login endpoint"

git add src/cart.py tests/test_cart.py
git commit -m "feat(cart): implement add to cart"
```

### ❌ Force pushing to shared branches

**Never do this**:

```bash
git push --force origin develop  # ❌❌❌
```

**Exception**: Only force push to your own feature branch if needed

```bash
git push --force origin feature/your-branch  # ⚠️ Only your branch!
```

---

## 🔧 Useful Git Commands

### Checking Status

```bash
# See what changed
git status

# See commit history
git log --oneline --graph --all

# See what changed in specific commit
git show <commit-hash>

# See branch list
git branch -a
```

### Fixing Mistakes

```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard uncommitted changes
git checkout -- <file>

# Amend last commit message
git commit --amend -m "new message"

# Stash changes temporarily
git stash
git stash pop
```

### Cleaning Up

```bash
# Delete local branch
git branch -d feature/old-feature

# Delete remote branch
git push origin --delete feature/old-feature

# Prune deleted remote branches
git fetch --prune
```

---

## 📊 Example Workflow

### Daily Development

**Morning**:

```bash
# Start your day
git checkout develop
git pull
git checkout feature/your-feature
git merge develop  # Sync with latest
```

**During Day**:

```bash
# Make changes
# Commit regularly (every 1-2 hours of work)
git add <files>
git commit -m "feat(scope): what you did"
```

**End of Day**:

```bash
# Push your work
git push origin feature/your-feature
```

### Completing a Feature

```bash
# 1. Make sure all tests pass
pytest tests/

# 2. Sync with develop one last time
git checkout develop
git pull
git checkout feature/your-feature
git merge develop

# 3. Push final version
git push origin feature/your-feature

# 4. Create pull request on GitHub
# 5. Wait for review and approval
# 6. Merge PR
# 7. Delete feature branch
git checkout develop
git pull
git branch -d feature/your-feature
```

---

## 🆘 Emergency Hotfix

When production is broken and needs immediate fix:

```bash
# 1. Create hotfix from main
git checkout main
git pull
git checkout -b hotfix/critical-bug

# 2. Fix the bug
# Make minimal changes

# 3. Test thoroughly
pytest tests/

# 4. Commit
git commit -m "fix: critical production bug"

# 5. Create PR to main
# Get fast-track approval

# 6. After merge to main, merge to develop too
git checkout develop
git merge main
git push
```

---

## ✅ Pre-commit Checklist

Before every commit:

- [ ] Code runs without errors
- [ ] Tests pass (`pytest` or `npm test`)
- [ ] Pre-commit hooks pass
- [ ] No debug statements left (console.log, print)
- [ ] No commented-out code
- [ ] Clear commit message written

---

## 📚 Resources

- [Git Branching Model](https://nvie.com/posts/a-successful-git-branching-model/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Flight Rules](https://github.com/k88hudson/git-flight-rules)
- [Oh Shit, Git!?!](https://ohshitgit.com/)

---

**Remember**: Good Git practices make collaboration smooth and rollbacks easy! 🚀
