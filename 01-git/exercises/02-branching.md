# Exercise 2: Branching Practice

**Difficulty**: Beginner  
**Time**: 25-30 minutes  
**Objectives**: Create branches, switch between them, understand branch isolation

---

## Setup

```bash
# Create new repository
mkdir git-branching-practice
cd git-branching-practice
git init

# Create initial file
echo "# Branching Practice" > README.md
git add README.md
git commit -m "feat: initial commit"
```

---

## Part 1: Create and Switch Branches

### Step 1: Create Feature Branch

```bash
# Create new branch
git branch feature/add-about

# List branches (* shows current branch)
git branch

# Switch to feature branch
git checkout feature/add-about

# Verify current branch
git branch
```

**Questions**:

1. What does the `*` indicate in `git branch` output?
2. Are you now on main or feature/add-about?

### Step 2: Work on Feature Branch

```bash
# Create about page
cat > about.txt << EOF
# About This Project

This is a practice repository for learning Git branching.

## Author
[Your Name]
EOF

# Stage and commit
git add about.txt
git commit -m "feat: add about page"

# View history
git log --oneline
```

---

## Part 2: Branch Isolation

### Step 3: Switch Back to Main

```bash
# Switch to main
git checkout main

# List files
ls

# Check if about.txt exists
ls about.txt
```

**Question**: Is about.txt visible on main branch? Why or why not?

### Step 4: Create Another Feature Branch

```bash
# Create and switch in one command
git checkout -b feature/add-contact

# Create contact page
cat > contact.txt << EOF
# Contact Information

Email: your.email@example.com
GitHub: github.com/yourname
EOF

# Commit
git add contact.txt
git commit -m "feat: add contact page"

# View log
git log --oneline
```

---

## Part 3: Multiple Branches

### Step 5: Create Third Branch

```bash
# Create projects branch from main
git checkout main
git checkout -b feature/add-projects

# Create projects file
cat > projects.txt << EOF
# My Projects

1. Project One
2. Project Two
3. Project Three
EOF

# Commit
git add projects.txt
git commit -m "feat: add projects list"
```

### Step 6: Visualize Branches

```bash
# See all branches
git branch

# See branch history graphically
git log --graph --oneline --all
```

**Expected output**:

```
* abc1234 (HEAD -> feature/add-projects) feat: add projects list
| * def5678 (feature/add-contact) feat: add contact page
|/
| * ghi9012 (feature/add-about) feat: add about page
|/
* jkl3456 (main) feat: initial commit
```

---

## Part 4: Switching Between Branches

### Step 7: Navigate Between Branches

```bash
# Switch to about branch
git checkout feature/add-about
ls  # See about.txt

# Switch to contact branch
git checkout feature/add-contact
ls  # See contact.txt

# Switch to projects branch
git checkout feature/add-projects
ls  # See projects.txt

# Back to main
git checkout main
ls  # See only README.md
```

**Questions**: 3. What files do you see on each branch? 4. Do the files "disappear" when you switch branches?

---

## Part 5: Making Changes on Different Branches

### Step 8: Update README on Main

```bash
# Make sure you're on main
git checkout main

# Update README
echo "\n## Branches\nThis project uses feature branches." >> README.md

# Commit
git add README.md
git commit -m "docs: update README with branch info"
```

### Step 9: Update About Branch

```bash
# Switch to about branch
git checkout feature/add-about

# Update about page
echo "\n## Skills\n- Git\n- Version Control" >> about.txt

# Commit
git add about.txt
git commit -m "docs: add skills section to about"
```

### Step 10: View Graph Again

```bash
git log --graph --oneline --all
```

You should now see divergent history!

---

## Part 6: Branch Information

### Step 11: Explore Branch Commands

```bash
# List all branches with last commit
git branch -v

# See which branches are merged into main
git checkout main
git branch --merged

# See which branches are not merged
git branch --no-merged

# See remote branches (if any)
git branch -r

# See all branches (local and remote)
git branch -a
```

---

## Part 7: Merge Practice (Preview)

### Step 12: Merge About Branch

```bash
# Switch to main
git checkout main

# Merge about branch
git merge feature/add-about

# See merged files
ls

# View history
git log --graph --oneline
```

**Question**: Is about.txt now on main?

### Step 13: Merge Contact Branch

```bash
# Still on main
git merge feature/add-contact

# View all files
ls

# View history
git log --graph --oneline --all
```

---

## Part 8: Cleanup

### Step 14: Delete Merged Branches

```bash
# Delete merged branches
git branch -d feature/add-about
git branch -d feature/add-contact

# Try to delete unmerged branch
git branch -d feature/add-projects
# This will fail!

# Force delete if you really want to
git branch -D feature/add-projects

# Verify cleanup
git branch
```

---

## Challenges (Optional)

### Challenge 1: Create Branch from Specific Commit

```bash
# View history
git log --oneline

# Create branch from older commit
git checkout -b feature/from-past <commit-hash>

# Verify
git log --oneline
```

### Challenge 2: Rename a Branch

```bash
# Create branch
git checkout -b feature/old-name

# Rename it
git branch -m feature/new-name

# Verify
git branch
```

### Challenge 3: Branch from Another Branch

```bash
# Create main feature
git checkout -b feature/main-feature

# Create sub-feature from it
git checkout -b feature/sub-feature

# Verify relationship
git log --graph --oneline --all
```

---

## Verification Checklist

- [ ] Created at least 3 feature branches
- [ ] Switched between branches multiple times
- [ ] Made commits on different branches
- [ ] Viewed branch graph
- [ ] Merged branches to main
- [ ] Deleted merged branches
- [ ] Understand branch isolation

---

## Expected Final State

```
Repository structure:
git-branching-practice/
├── README.md (updated)
├── about.txt (from merge)
└── contact.txt (from merge)

Branches:
- main (only branch remaining)

History:
- Initial commit
- Add about page
- Add contact page
- Merge commits
```

---

## Questions to Answer

1. What is the difference between `git branch name` and `git checkout -b name`?
2. Why don't files from feature branches appear on main until merged?
3. What does `git branch -d` vs `git branch -D` do?
4. How can you see which branch you're currently on?
5. What happens to commits when you delete a branch?

---

## Common Issues

**Issue**: Can't switch branches - "uncommitted changes"  
**Solution**: Commit or stash your changes first

**Issue**: Can't delete branch - "not fully merged"  
**Solution**: Use `-D` to force delete, or merge it first

**Issue**: Lost track of which branch I'm on  
**Solution**: Run `git branch` or look at terminal prompt

---

**Great job!** 🎉 You now understand how Git branches work and can use them effectively!

**Next Exercise**: [Collaboration Simulation](./03-collaboration.md)
