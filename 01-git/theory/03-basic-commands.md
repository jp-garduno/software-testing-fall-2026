# Basic Git Commands

## The Git Workflow

```
Working Directory → Staging Area → Repository
     (edit)          (git add)     (git commit)
```

### Three Areas in Git

1. **Working Directory** - Your actual files where you work
2. **Staging Area** (Index) - Files ready to be committed
3. **Repository** - Committed history (snapshots)

---

## Essential Commands

### `git init` - Create a Repository

Initialize a new Git repository in the current directory.

```bash
# Create new directory
mkdir my-project
cd my-project

# Initialize Git
git init
```

**What it does**:

- Creates a `.git` folder (hidden)
- Sets up Git database
- Prepares for tracking

**Output**:

```
Initialized empty Git repository in /path/to/my-project/.git/
```

---

### `git status` - Check Status

See the current state of your repository.

```bash
git status
```

**What it shows**:

- Modified files
- Staged files
- Untracked files
- Current branch

**Example output**:

```
On branch main

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        README.md

nothing added to commit but untracked files present (use "git add" to track)
```

**💡 Tip**: Run `git status` frequently! It's your best friend.

---

### `git add` - Stage Files

Add files to the staging area.

```bash
# Add single file
git add filename.txt

# Add multiple files
git add file1.txt file2.txt

# Add all files in directory
git add .

# Add all files (from anywhere)
git add -A

# Add only modified files (not new ones)
git add -u
```

**Examples**:

```bash
# Stage README.md
git add README.md

# Stage all Python files
git add *.py

# Stage everything in src/ directory
git add src/

# Stage all JavaScript and CSS files
git add *.js *.css
```

**💡 Best Practice**: Stage related changes together, not everything at once.

---

### `git commit` - Save Snapshot

Save staged changes with a message.

```bash
# Commit with inline message
git commit -m "Your commit message"

# Commit with detailed message (opens editor)
git commit

# Add all and commit (skip staging)
git commit -am "Your message"
```

**Good commit messages**:

```bash
# ✅ Good
git commit -m "feat: add user authentication"
git commit -m "fix: correct calculation bug in total"
git commit -m "docs: update installation instructions"

# ❌ Bad
git commit -m "changes"
git commit -m "stuff"
git commit -m "idk"
```

**Conventional Commits format**:

```
<type>: <description>

[optional body]
```

**Types**:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

---

### `git log` - View History

See commit history.

```bash
# Full log
git log

# One line per commit
git log --oneline

# With graph
git log --graph --oneline

# Last N commits
git log -5

# By author
git log --author="John"

# By date
git log --since="2 weeks ago"

# Pretty format
git log --pretty=format:"%h - %an, %ar : %s"
```

**Example output**:

```bash
$ git log --oneline
a1b2c3d (HEAD -> main) feat: add login page
e4f5g6h fix: correct typo in README
i7j8k9l docs: update contributing guidelines
```

---

### `git diff` - See Changes

View differences between versions.

```bash
# Changes in working directory (not staged)
git diff

# Changes in staging area
git diff --staged
# or
git diff --cached

# Changes between commits
git diff commit1 commit2

# Changes in specific file
git diff filename.txt
```

**Example**:

```diff
diff --git a/calculator.py b/calculator.py
index 1234567..abcdefg 100644
--- a/calculator.py
+++ b/calculator.py
@@ -1,5 +1,5 @@
 def add(a, b):
-    return a + b
+    return a + b + 1  # Fixed bug

 def subtract(a, b):
     return a - b
```

---

## Complete Workflow Example

### Scenario: Adding a new feature

```bash
# 1. Check current status
git status

# 2. Create new file
echo "print('Hello, World!')" > hello.py

# 3. Check status again
git status
# Output: hello.py is untracked

# 4. Stage the file
git add hello.py

# 5. Check status
git status
# Output: hello.py is staged

# 6. Commit
git commit -m "feat: add hello world script"

# 7. View history
git log --oneline

# 8. Make changes
echo "print('Hello, Git!')" >> hello.py

# 9. See what changed
git diff

# 10. Stage and commit
git add hello.py
git commit -m "feat: improve greeting message"
```

---

## File States in Git

Files can be in different states:

```
Untracked → Unmodified → Modified → Staged → Committed
             ↑____________|
```

### Untracked

- New files Git doesn't know about
- Not in version control
- Won't be in commits

### Unmodified

- File is tracked
- No changes since last commit

### Modified

- File has changes
- Not staged yet

### Staged

- Changes marked for commit
- Will be in next commit

### Committed

- Safely stored in repository
- Part of project history

---

## Common Scenarios

### Scenario 1: Undo Unstaged Changes

You edited a file but want to discard changes:

```bash
# Discard changes in specific file
git restore filename.txt

# Or (older Git versions)
git checkout -- filename.txt

# Discard all unstaged changes (CAREFUL!)
git restore .
```

### Scenario 2: Unstage File

You staged a file by mistake:

```bash
# Unstage specific file (keep changes)
git restore --staged filename.txt

# Or (older versions)
git reset HEAD filename.txt
```

### Scenario 3: Amend Last Commit

You forgot to add a file or want to change the message:

```bash
# Add forgotten file and amend
git add forgotten_file.txt
git commit --amend --no-edit

# Change commit message
git commit --amend -m "New message"
```

**⚠️ Warning**: Only amend commits that haven't been pushed!

---

## Ignoring Files

Create `.gitignore` to ignore files:

```bash
# Create .gitignore
touch .gitignore
```

**Example `.gitignore`**:

```
# Python
__pycache__/
*.pyc
*.pyo
venv/
.env

# JavaScript
node_modules/
npm-debug.log
.env

# IDEs
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Build artifacts
dist/
build/
*.exe
```

**Common patterns**:

```
# Ignore specific file
secret.txt

# Ignore all .log files
*.log

# Ignore directory
temp/

# Ignore files in directory
logs/*.log

# Don't ignore specific file
!important.log
```

---

## Viewing File History

```bash
# See history of file
git log filename.txt

# See changes in file
git log -p filename.txt

# Who changed each line
git blame filename.txt

# See file at specific commit
git show commit_hash:filename.txt
```

---

## Quick Reference

### Setup

```bash
git init                    # Initialize repository
git config --global user.name "Name"
git config --global user.email "email"
```

### Basic Workflow

```bash
git status                  # Check status
git add file.txt            # Stage file
git add .                   # Stage all files
git commit -m "message"     # Commit with message
git log                     # View history
git log --oneline           # Compact history
```

### Undoing

```bash
git restore file.txt        # Discard changes
git restore --staged file.txt  # Unstage
git commit --amend          # Modify last commit
```

### Viewing Changes

```bash
git diff                    # Unstaged changes
git diff --staged           # Staged changes
git show commit_hash        # View commit
```

---

## Practice Exercises

Try these to build muscle memory:

1. **Create a repository and make 5 commits**
2. **Stage only specific files, not all**
3. **Use `git log` with different options**
4. **Make a change, view diff, then discard it**
5. **Create a `.gitignore` file**
6. **Amend a commit**
7. **Use `git blame` on a file**

---

## Common Mistakes

### Mistake 1: Committing without staging

```bash
# ❌ This doesn't work
git commit -m "message"
# Nothing happens if nothing is staged!

# ✅ Either stage first
git add file.txt
git commit -m "message"

# ✅ Or use -a flag
git commit -am "message"  # Only for tracked files
```

### Mistake 2: Vague commit messages

```bash
# ❌ Bad
git commit -m "changes"
git commit -m "update"
git commit -m "fix"

# ✅ Good
git commit -m "feat: add user registration form"
git commit -m "fix: correct email validation regex"
git commit -m "docs: update API documentation"
```

### Mistake 3: Committing sensitive data

```bash
# ❌ Never commit
passwords.txt
.env
api_keys.json
secret_token.txt

# ✅ Add to .gitignore
echo "passwords.txt" >> .gitignore
echo ".env" >> .gitignore
```

---

## Next Steps

You now know the essential Git commands! Next, learn:

1. **[Understanding Commits](./04-commits.md)**
2. **[Branching](./05-branching.md)**
3. **[Merging](./06-merging.md)**

---

## Additional Resources

- [Git Command Reference](https://git-scm.com/docs)
- [Interactive Git Tutorial](https://learngitbranching.js.org/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

---

**Remember**: The best way to learn Git is by using it! Practice with real projects. 🚀
