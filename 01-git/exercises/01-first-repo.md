# Exercise 1: Your First Repository

**Difficulty**: Beginner  
**Time**: 20-30 minutes  
**Objectives**: Create a repository, make commits, view history

---

## Part 1: Create and Initialize Repository

### Step 1: Create Project Directory

```bash
# Create directory
mkdir my-portfolio
cd my-portfolio

# Initialize Git
git init

# Verify
git status
```

**Expected output**:

```
Initialized empty Git repository in .../my-portfolio/.git/
On branch main
No commits yet
nothing to commit (create/copy files and commit them)
```

---

## Part 2: Create Your First File

### Step 2: Create README

```bash
# Create README.md
echo "# My Portfolio" > README.md

# Check status
git status
```

**Questions**:

1. What does `git status` show?
2. Is README.md tracked or untracked?

### Step 3: Stage and Commit

```bash
# Stage the file
git add README.md

# Check status again
git status

# Commit
git commit -m "feat: initial commit with README"

# View history
git log
```

**Questions**: 3. What information does `git log` show? 4. What is the commit hash (ID)?

---

## Part 3: Make Multiple Commits

### Step 4: Add More Content

```bash
# Add content to README
echo "## About Me" >> README.md
echo "I am learning Git!" >> README.md

# View changes
git diff

# Stage and commit
git add README.md
git commit -m "docs: add about me section"
```

### Step 5: Create New File

```bash
# Create index.html
cat > index.html << EOF
<!DOCTYPE html>
<html>
<head>
    <title>My Portfolio</title>
</head>
<body>
    <h1>Welcome to My Portfolio</h1>
</body>
</html>
EOF

# Stage and commit
git add index.html
git commit -m "feat: add homepage"
```

### Step 6: Create CSS File

```bash
# Create style.css
cat > style.css << EOF
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 20px;
}

h1 {
    color: #333;
}
EOF

# Stage and commit
git add style.css
git commit -m "style: add basic CSS styling"
```

---

## Part 4: View History

### Step 7: Explore History

```bash
# View full log
git log

# View compact log
git log --oneline

# View with graph
git log --graph --oneline

# View last 3 commits
git log -3

# View specific commit
git show <commit-hash>
```

**Expected**: You should have at least 4 commits now.

---

## Part 5: Make Changes

### Step 8: Modify Files

```bash
# Update index.html
echo "    <p>This is my portfolio website.</p>" >> index.html

# Update README.md
echo "## Projects" >> README.md
echo "Coming soon!" >> README.md

# View all changes
git diff

# Stage only index.html
git add index.html

# Check status (README.md should still be unstaged)
git status

# Commit
git commit -m "feat: add content to homepage"

# Now stage and commit README
git add README.md
git commit -m "docs: add projects section"
```

---

## Part 6: Practice .gitignore

### Step 9: Create Files to Ignore

```bash
# Create files that should be ignored
touch secret.txt
touch temp.log
mkdir cache
touch cache/data.tmp

# Check status (all files appear)
git status
```

### Step 10: Create .gitignore

```bash
# Create .gitignore
cat > .gitignore << EOF
secret.txt
*.log
cache/
EOF

# Check status (ignored files shouldn't appear)
git status

# Commit .gitignore
git add .gitignore
git commit -m "chore: add gitignore file"
```

---

## Part 7: View Your Progress

### Step 11: Final Review

```bash
# View all commits
git log --oneline

# Count commits
git rev-list --count HEAD

# See all files tracked
git ls-files

# View repository size
du -sh .git
```

---

## Verification Checklist

Check that you have:

- [ ] Initialized a Git repository
- [ ] Created at least 6 commits
- [ ] Used different commit types (feat, docs, style, chore)
- [ ] Created and committed README.md
- [ ] Created and committed index.html
- [ ] Created and committed style.css
- [ ] Created and committed .gitignore
- [ ] Used `git status`, `git log`, `git diff`
- [ ] Practiced staging individual files

---

## Challenges (Optional)

### Challenge 1: Amend a Commit

```bash
# Make a small change
echo "/* More styles coming soon */" >> style.css

# Amend last commit instead of creating new one
git add style.css
git commit --amend --no-edit

# Verify (should still have same number of commits)
git log --oneline
```

### Challenge 2: View Detailed History

```bash
# View changes in each commit
git log -p

# View stats
git log --stat

# View pretty graph
git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cd) %C(bold blue)<%an>%Creset' --abbrev-commit --date=short
```

### Challenge 3: Practice Undoing

```bash
# Make an unwanted change
echo "This is a mistake" >> README.md

# View the change
git diff

# Discard the change
git restore README.md

# Verify it's gone
git diff
```

---

## Expected Final Structure

```
my-portfolio/
├── .git/
├── .gitignore
├── README.md
├── index.html
├── style.css
├── secret.txt (ignored)
├── temp.log (ignored)
└── cache/ (ignored)
```

---

## Questions to Answer

1. What is the difference between `git add` and `git commit`?
2. Why do we need a `.gitignore` file?
3. How can you see what changed in a specific commit?
4. What happens if you don't stage files before committing?
5. How do you undo unstaged changes to a file?

---

## Submission

For this exercise, submit:

1. Screenshot of `git log --oneline` showing your commits
2. Screenshot of `git status` (should be clean)
3. Your final `.gitignore` file contents
4. Answers to the 5 questions above

---

## Common Issues

**Issue**: `git commit` does nothing  
**Solution**: Make sure you staged files with `git add` first

**Issue**: Can't see commit history  
**Solution**: Make sure you have made at least one commit

**Issue**: Files still show in status despite .gitignore  
**Solution**: .gitignore only affects untracked files. If files were already tracked, you need to untrack them:

```bash
git rm --cached filename
```

---

**Congratulations!** 🎉 You've created your first Git repository and made several commits. You now understand the basic Git workflow!

**Next Exercise**: [Branching Practice](./02-branching.md)
