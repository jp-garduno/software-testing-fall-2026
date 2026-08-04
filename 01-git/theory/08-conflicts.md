# Resolving Conflicts

## What is a Merge Conflict?

A conflict occurs when Git can't automatically merge changes because the same lines were modified in both branches.

## When Conflicts Happen

```
main:    A -- B -- C (modified file.txt line 5)
              \
feature:       D (modified file.txt line 5 differently)
```

When you try to merge, Git says: "I don't know which version to keep!"

## Identifying Conflicts

```bash
git merge feature-branch

# Output:
Auto-merging file.txt
CONFLICT (content): Merge conflict in file.txt
Automatic merge failed; fix conflicts and then commit the result.
```

## Conflict Markers

Git adds markers to show conflicts:

```python
<<<<<<< HEAD (current branch)
def calculate_total(price, tax):
    return price + tax
=======
def calculate_total(price, tax_rate):
    return price * (1 + tax_rate)
>>>>>>> feature-branch
```

**Sections**:

- `<<<<<<< HEAD`: Your current branch version
- `=======`: Separator
- `>>>>>>> branch-name`: Incoming branch version

## Resolving Conflicts

### Step 1: Check Status

```bash
git status
# Shows conflicted files
```

### Step 2: Open Conflicted Files

Edit files and choose which version to keep:

**Option A: Keep yours**

```python
def calculate_total(price, tax):
    return price + tax
```

**Option B: Keep theirs**

```python
def calculate_total(price, tax_rate):
    return price * (1 + tax_rate)
```

**Option C: Keep both (manual merge)**

```python
def calculate_total(price, tax=0, tax_rate=0):
    if tax_rate:
        return price * (1 + tax_rate)
    return price + tax
```

### Step 3: Remove Conflict Markers

Delete the `<<<<<<<`, `=======`, `>>>>>>>` lines.

### Step 4: Stage Resolved Files

```bash
git add file.txt
```

### Step 5: Complete Merge

```bash
git commit
# Git opens editor with default merge message
# Save and close
```

## Aborting a Merge

If you want to cancel:

```bash
git merge --abort
```

Returns to state before merge.

## Merge Tools

### Using VS Code

VS Code shows conflict resolution UI:

- **Accept Current Change**: Keep your version
- **Accept Incoming Change**: Keep their version
- **Accept Both Changes**: Keep both
- **Compare Changes**: Side-by-side view

### Command Line Tools

```bash
# Configure merge tool (e.g., VS Code)
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait $MERGED'

# Use merge tool
git mergetool
```

## Preventing Conflicts

1. **Pull frequently**: Stay up to date
2. **Communicate**: Tell team what you're working on
3. **Keep branches short-lived**: Merge within a week
4. **Work on different files**: Avoid editing same files
5. **Small, focused commits**: Easier to merge

## Conflict Resolution Strategies

### Strategy 1: Accept Theirs

```bash
git merge -X theirs feature-branch
```

Automatically prefer incoming changes.

### Strategy 2: Accept Ours

```bash
git merge -X ours feature-branch
```

Automatically prefer your changes.

### Strategy 3: Manual

Review each conflict individually (best for important code).

## Common Conflict Scenarios

### Scenario 1: Both Modified Same Lines

```
You:   Updated function signature
Them:  Updated function body
```

**Solution**: Manually combine both changes.

### Scenario 2: You Deleted, They Modified

```
You:   Deleted file
Them:  Modified file
```

**Solution**: Decide if file should exist.

### Scenario 3: Binary Files

```
Conflict in image.png
```

**Solution**: Choose one version (can't merge binaries).

## Conflict Resolution Workflow

```bash
# 1. Try to merge
git merge feature-branch
# CONFLICT!

# 2. See what's conflicted
git status

# 3. Open conflicted files
code file.txt

# 4. Resolve conflicts
# Edit file, remove markers

# 5. Stage resolved files
git add file.txt

# 6. Continue merge
git commit

# 7. Verify
git log --graph --oneline
```

## Best Practices

1. **Communicate**: Tell team before big refactors
2. **Update often**: Pull main changes regularly
3. **Small merges**: Don't let branches diverge too much
4. **Test after resolving**: Make sure code still works
5. **Ask for help**: If conflict is complex, ask teammate
6. **Document**: Add comment if resolution is non-obvious

## Checking for Conflicts Before Merge

```bash
# See what would merge
git diff main..feature-branch

# See if merge would conflict (dry run)
git merge --no-commit --no-ff feature-branch
git merge --abort  # Cancel preview
```

## Next Steps

- [Git Workflows](./09-workflows.md)
- [Best Practices](./10-best-practices.md)

## Quick Reference

```bash
# Check status
git status

# Resolve and stage
git add resolved-file.txt

# Complete merge
git commit

# Abort merge
git merge --abort

# Use merge tool
git mergetool
```
