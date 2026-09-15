# Exercise 3: Collaboration Simulation

**Difficulty**: Intermediate  
**Time**: 30-35 minutes  
**Objectives**: Work with remote repositories, create pull requests, simulate team collaboration

## Part 1: Fork and Clone

### Step 1: Fork a Repository

1. Go to course repository on GitHub
2. Click "Fork" button
3. Create fork in your account

### Step 2: Clone Your Fork

```bash
git clone https://github.com/YOUR-USERNAME/software-testing-fall-2026.git
cd software-testing-fall-2026
```

### Step 3: Add Upstream Remote

```bash
# Add original repo as upstream
git remote add upstream https://github.com/ORIGINAL-OWNER/software-testing-fall-2026.git

# Verify remotes
git remote -v
```

## Part 2: Create Feature Branch

```bash
# Create your branch
git checkout -b feat/exercise-3-yourname

# Create your workspace
mkdir -p students/yourname/exercise-3
cd students/yourname/exercise-3

# Create files
echo "# My Collaboration Exercise" > README.md
git add README.md
git commit -m "feat(exercise-3): add README"

# Push to your fork
git push origin feat/exercise-3-yourname
```

## Part 3: Create Pull Request

1. Go to your fork on GitHub
2. Click "Pull requests" → "New pull request"
3. Select:
   - base: `main` (original repo)
   - compare: `feat/exercise-3-yourname` (your branch)
4. Fill out PR template
5. Create pull request

## Part 4: Update Your Branch

```bash
# Make more changes
echo "## Additional Work" >> README.md
git add README.md
git commit -m "docs(exercise-3): add more content"

# Push (PR updates automatically)
git push origin feat/exercise-3-yourname
```

## Part 5: Sync with Upstream

```bash
# Fetch upstream changes
git fetch upstream

# Merge upstream main into your branch
git merge upstream/main

# Or rebase (cleaner)
git rebase upstream/main

# Push updated branch
git push origin feat/exercise-3-yourname --force-with-lease
```

## Verification

- [ ] Forked repository
- [ ] Cloned locally
- [ ] Added upstream remote
- [ ] Created feature branch
- [ ] Made commits
- [ ] Pushed to fork
- [ ] Created pull request
- [ ] Updated PR with new commits

Next: [Conflict Resolution](./04-conflicts.md)
