# Git Workflows

## What is a Git Workflow?

A standardized way for teams to collaborate using Git branches and merges.

## Common Workflows

### 1. Centralized Workflow

Everyone works on `main` branch.

```
main: A -- B -- C -- D -- E
```

**Pros**: Simple, good for small teams  
**Cons**: No isolation, conflicts common  
**Best for**: Very small teams, simple projects

### 2. Feature Branch Workflow

Each feature gets its own branch.

```
main:    A -- B ----------- F
              \             /
feature:       C -- D -- E
```

**Process**:
1. Create branch from main
2. Develop feature
3. Create PR
4. Merge to main
5. Delete branch

**Best for**: Most teams, this course

### 3. Git Flow

Structured workflow with multiple long-lived branches.

```
main (production releases)
  ↓
develop (integration)
  ↓
feature/*, hotfix/*, release/*
```

**Branches**:
- `main`: Production code only
- `develop`: Integration branch
- `feature/*`: New features
- `release/*`: Prepare releases
- `hotfix/*`: Urgent production fixes

**Best for**: Large projects, scheduled releases

### 4. GitHub Flow

Simplified flow optimized for continuous deployment.

```
main: A -- B -- C -- F -- G
            \       /
feature:     D -- E
```

**Process**:
1. Branch from main
2. Make changes
3. Create PR
4. Review and discuss
5. Merge to main
6. Deploy immediately

**Best for**: Web applications, continuous deployment

### 5. GitLab Flow

Combines feature branches with environment branches.

```
main
  ↓
pre-production
  ↓
production
```

**Best for**: Applications with staging environments

## Feature Branch Workflow (Detailed)

### Daily Workflow

```bash
# Morning: Update main
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/user-profile

# Work and commit
git add .
git commit -m "feat: add profile page"

# More work
git add .
git commit -m "test: add profile tests"

# Push branch
git push origin feature/user-profile

# Create PR on GitHub
# Get reviewed
# Merge
```

### Keeping Branch Updated

```bash
# Option 1: Merge main into feature
git checkout feature/user-profile
git merge main

# Option 2: Rebase on main (cleaner)
git checkout feature/user-profile
git rebase main
```

## Trunk-Based Development

Developers commit directly to `main` (or very short-lived branches).

**Requirements**:
- Strong CI/CD
- Feature flags
- High test coverage

**Best for**: Experienced teams, fast iteration

## Release Workflows

### Semantic Versioning

```
main: v1.0.0 -- v1.1.0 -- v2.0.0
```

Tag releases:
```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### Release Branches

```bash
# Create release branch
git checkout -b release/1.0.0

# Bug fixes only on release branch
git commit -m "fix: critical bug"

# Merge to main and develop
git checkout main
git merge release/1.0.0
git tag v1.0.0
```

## Team Collaboration Patterns

### Pattern 1: Personal Branches

```
main
  ├─ alice/feature-a
  ├─ bob/feature-b
  └─ carol/feature-c
```

Each team member has their feature branches.

### Pattern 2: Shared Feature Branch

```
main
  └─ feature/big-feature
       ├─ alice/sub-feature-1
       └─ bob/sub-feature-2
```

Multiple people work on same feature.

### Pattern 3: Mob/Pair Programming

```
main
  └─ feature/paired-work (both pushing)
```

Two+ developers work on same branch together.

## Workflow Selection Guide

**Choose based on**:

| **Factor** | **Simple Workflow** | **Complex Workflow** |
|------------|---------------------|----------------------|
| Team size | < 5 | > 10 |
| Release cycle | Continuous | Scheduled |
| Team experience | Beginners | Experienced |
| Project complexity | Simple | Complex |
| Deployment | Automated | Manual |

## Best Practices (All Workflows)

1. **Commit often**: Small, focused commits
2. **Pull before push**: Stay up to date
3. **Branch from updated main**: Start from latest
4. **Keep branches short-lived**: Merge within a week
5. **Write good commit messages**: Follow conventions
6. **Test before merging**: Ensure quality
7. **Delete merged branches**: Keep repo clean
8. **Communicate**: Tell team about branches

## Workflow for This Course

We use **Feature Branch + Pull Request Workflow**:

```bash
# 1. Create branch
git checkout -b feat/homework-1-yourname

# 2. Work in students/yourname/ directory
# 3. Commit changes
git commit -m "feat(homework-1): complete exercises"

# 4. Push
git push origin feat/homework-1-yourname

# 5. Create PR on GitHub
# 6. Automated grading runs
# 7. Submit PR link to Canvas
```

## Protecting Main Branch

On GitHub:
1. Settings → Branches
2. Add rule for `main`
3. Enable:
   - Require pull request reviews
   - Require status checks to pass
   - No force push
   - No deletion

## Next Steps

- [Best Practices](./10-best-practices.md)

## Quick Reference

```bash
# Feature branch workflow
git checkout main
git pull
git checkout -b feature/name
# Work...
git commit -am "feat: add feature"
git push origin feature/name
# Create PR, review, merge
```
