# Exercise 4: Conflict Resolution

**Difficulty**: Intermediate  
**Time**: 25-30 minutes  
**Objectives**: Intentionally create and resolve merge conflicts

## Part 1: Setup

```bash
mkdir conflict-practice
cd conflict-practice
git init

# Create initial file
echo "Line 1: Original" > file.txt
git add file.txt
git commit -m "feat: initial commit"
```

## Part 2: Create Conflicting Changes

### Step 1: Create Branch A

```bash
git checkout -b branch-a

# Modify line 1
echo "Line 1: Modified by Branch A" > file.txt
git add file.txt
git commit -m "feat: update from branch a"
```

### Step 2: Create Branch B

```bash
# Go back to main
git checkout main

# Create branch B from main
git checkout -b branch-b

# Modify same line differently
echo "Line 1: Modified by Branch B" > file.txt
git add file.txt
git commit -m "feat: update from branch b"
```

## Part 3: Merge and Create Conflict

```bash
# Go back to main
git checkout main

# Merge branch-a (should work fine)
git merge branch-a
cat file.txt  # See branch-a's version

# Try to merge branch-b (CONFLICT!)
git merge branch-b
```

**Expected**: Conflict message

## Part 4: Resolve Conflict

```bash
# See conflicted files
git status

# View conflict markers
cat file.txt
```

**You'll see**:

```
<<<<<<< HEAD
Line 1: Modified by Branch A
=======
Line 1: Modified by Branch B
>>>>>>> branch-b
```

### Step 1: Edit File

Choose how to resolve:

**Option 1 - Keep A**:

```
Line 1: Modified by Branch A
```

**Option 2 - Keep B**:

```
Line 1: Modified by Branch B
```

**Option 3 - Keep Both**:

```
Line 1: Modified by Branch A and Branch B
```

**Option 4 - New Solution**:

```
Line 1: Merged version from both branches
```

### Step 2: Complete Merge

```bash
# Stage resolved file
git add file.txt

# Complete merge
git commit -m "merge: resolve conflict between branch-a and branch-b"

# View history
git log --graph --oneline
```

## Part 5: Practice More Conflicts

### Multiple File Conflicts

```bash
# Create branch with multiple files
git checkout -b multi-file-conflict

echo "Feature A content" > feature-a.txt
echo "Feature B content" > feature-b.txt
git add .
git commit -m "feat: add multiple features"

# Go back and create conflicting version
git checkout main
echo "Different A content" > feature-a.txt
echo "Different B content" > feature-b.txt
git add .
git commit -m "feat: different features"

# Merge (conflicts!)
git merge multi-file-conflict

# Resolve each file
# Stage each
# Commit
```

## Part 6: Using Merge Tools

```bash
# Configure VS Code as merge tool
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait $MERGED'

# When conflict occurs
git mergetool
```

## Challenges

1. **Three-way conflict**: Create 3 branches that all modify same line
2. **Binary conflict**: Add image, modify in two branches
3. **Delete vs modify**: Delete file in one branch, modify in another

## Verification

- [ ] Created intentional conflicts
- [ ] Resolved conflicts manually
- [ ] Completed merge
- [ ] Practiced with multiple files
- [ ] Used merge tool
- [ ] Understand conflict markers

Next: [Real-World Workflow](./05-workflow.md)
