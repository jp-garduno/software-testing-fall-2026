# Branching in Git

## What is a Branch?

A branch is an independent line of development. Think of it as a parallel universe for your code.

```
main:    A -- B -- C -- D
              \
feature:       E -- F -- G
```

## Why Use Branches?

✅ Work on features without breaking main code
✅ Experiment safely  
✅ Collaborate with others  
✅ Keep production code stable  
✅ Work on multiple features simultaneously  

## Branch Commands

### Create Branch
```bash
# Create new branch
git branch feature-name

# Create and switch to branch
git checkout -b feature-name
# or (Git 2.23+)
git switch -c feature-name
```

### List Branches
```bash
# List local branches
git branch

# List all branches (local + remote)
git branch -a

# List with last commit
git branch -v
```

### Switch Branches
```bash
# Switch to branch
git checkout branch-name
# or (Git 2.23+)
git switch branch-name

# Switch to previous branch
git checkout -
```

### Delete Branch
```bash
# Delete merged branch
git branch -d branch-name

# Force delete (even if not merged)
git branch -D branch-name
```

## Branch Workflow

### Feature Branch Workflow
```bash
# 1. Create feature branch from main
git checkout main
git checkout -b feature/login

# 2. Work on feature
# Edit files...
git add .
git commit -m "feat: add login form"

# 3. More work...
git add .
git commit -m "feat: add validation"

# 4. Switch back to main
git checkout main

# 5. Merge feature
git merge feature/login

# 6. Delete feature branch
git branch -d feature/login
```

## Branch Naming

### Good Branch Names
```
feature/user-authentication
fix/memory-leak
docs/api-documentation
refactor/database-queries
test/add-unit-tests
```

### Convention
```
<type>/<description>

Types:
- feature/ or feat/
- fix/ or bugfix/
- docs/
- refactor/
- test/
- chore/
```

## Branching Strategies

### 1. Feature Branch Workflow
- Main branch stays stable
- Create branch for each feature
- Merge when complete

### 2. Git Flow
```
main (production)
  ↓
develop (integration)
  ↓
feature branches
```

### 3. GitHub Flow (Simplest)
```
main branch
  ↓
feature branches
  ↓
pull requests
  ↓
back to main
```

## Best Practices

1. **Branch from main**: Always start from updated main
2. **Keep branches short-lived**: Merge within a week
3. **One feature per branch**: Don't mix features
4. **Update frequently**: Pull main changes regularly
5. **Delete after merge**: Clean up merged branches

## Common Scenarios

### Scenario 1: Work on New Feature
```bash
git checkout main
git pull
git checkout -b feature/new-dashboard
# Work...
git add .
git commit -m "feat: implement dashboard"
# Create PR on GitHub
```

### Scenario 2: Quick Bug Fix
```bash
git checkout main
git checkout -b fix/login-bug
# Fix...
git add .
git commit -m "fix: correct login validation"
git checkout main
git merge fix/login-bug
git branch -d fix/login-bug
```

### Scenario 3: Switch Between Features
```bash
# Working on feature A
git checkout feature-a
# Need to switch to feature B
git checkout feature-b
# Back to feature A
git checkout feature-a
```

## Visualizing Branches

```bash
# See branch graph
git log --graph --oneline --all

# Pretty graph
git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
```

Example output:
```
* a1b2c3d - (HEAD -> feature) feat: add feature
* e4f5g6h - fix: bug fix
| * h7i8j9k - (main) docs: update readme
|/
* k0l1m2n - initial commit
```

Next: [Merging](./06-merging.md)
