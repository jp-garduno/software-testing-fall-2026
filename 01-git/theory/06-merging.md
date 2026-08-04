# Merging Branches

## What is Merging?

Merging combines changes from different branches into one branch.

## Basic Merge
```bash
git checkout main
git merge feature-branch
```

## Types of Merges

### 1. Fast-Forward Merge
When target branch hasn't changed.
```
main:    A -- B -- C -- D
```

### 2. Three-Way Merge
When both branches have commits.
```
main:    A -- B -- C -- F (merge commit)
              \         /
feature:       D ----- E
```

### 3. Squash Merge
```bash
git merge --squash feature-branch
```

## Merge Workflow
```bash
git checkout main
git pull
git merge feature/new-feature
git push
git branch -d feature/new-feature
```

## Merge vs Rebase

**Merge**: Preserves history, creates merge commits
**Rebase**: Linear history, rewrites commits

Rule: Never rebase public branches!

## Best Practices
1. Merge frequently
2. Test before merging
3. Delete merged branches
4. Use meaningful merge messages

Next: [Pull Requests](./07-pull-requests.md)
