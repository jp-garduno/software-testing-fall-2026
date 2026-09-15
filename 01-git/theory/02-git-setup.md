# Git Setup and Configuration

## Installing Git

### Windows

**Option 1: Git for Windows (Recommended)**

1. Download from [git-scm.com](https://git-scm.com/download/win)
2. Run the installer
3. **Important settings during installation**:

   - Editor: Choose VS Code (or your preferred editor)
   - PATH: "Git from the command line and also from 3rd-party software"
   - Line endings: "Checkout Windows-style, commit Unix-style"
   - Terminal: "Use Windows' default console window" or "Use MinTTY"
   - Everything else: Keep defaults

4. Verify installation:
   ```bash
   git --version
   # Should show: git version 2.43.0 (or higher)
   ```

**Option 2: GitHub Desktop**

- Download from [desktop.github.com](https://desktop.github.com/)
- GUI application (easier for beginners)
- Includes Git command-line tools

### macOS

**Option 1: Homebrew (Recommended)**

```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Git
brew install git

# Verify
git --version
```

**Option 2: Xcode Command Line Tools**

```bash
xcode-select --install
git --version
```

**Option 3: Download installer**

- Download from [git-scm.com/download/mac](https://git-scm.com/download/mac)

### Linux

**Ubuntu/Debian**:

```bash
sudo apt update
sudo apt install git
git --version
```

**Fedora/RHEL**:

```bash
sudo dnf install git
git --version
```

**Arch Linux**:

```bash
sudo pacman -S git
git --version
```

---

## Initial Configuration

After installing Git, you need to configure it. Git stores configuration at three levels:

### Configuration Levels

1. **System** - All users on the computer (`--system`)
2. **Global** - All repositories for your user (`--global`)
3. **Local** - Specific repository (`--local`)

We'll focus on **global** configuration.

### Essential Configuration

#### 1. Set Your Identity

**This is required!** Git uses this information for every commit.

```bash
# Set your name
git config --global user.name "Your Name"

# Set your email (use the same email as your GitHub account)
git config --global user.email "your.email@example.com"

# Verify
git config --global user.name
git config --global user.email
```

**Example**:

```bash
git config --global user.name "Jane Smith"
git config --global user.email "jane.smith@university.edu"
```

#### 2. Set Default Branch Name

GitHub and modern Git use `main` instead of `master`:

```bash
git config --global init.defaultBranch main
```

#### 3. Set Default Editor

Choose your preferred text editor for commit messages:

**VS Code**:

```bash
git config --global core.editor "code --wait"
```

**Vim** (default):

```bash
git config --global core.editor vim
```

**Nano** (easier than Vim):

```bash
git config --global core.editor nano
```

**Notepad** (Windows):

```bash
git config --global core.editor notepad
```

#### 4. Set Line Ending Preferences

**Windows**:

```bash
git config --global core.autocrlf true
```

**macOS/Linux**:

```bash
git config --global core.autocrlf input
```

**Why?** Windows uses CRLF (`\r\n`) for line endings, Unix/Mac use LF (`\n`). This setting normalizes them.

---

## Recommended Configuration

### Make Output Colorful

```bash
git config --global color.ui auto
```

### Set Default Pull Behavior

```bash
git config --global pull.rebase false
```

### Enable Helpful Features

```bash
# Show original state in conflict markers
git config --global merge.conflictstyle diff3

# Better diff algorithm
git config --global diff.algorithm histogram

# Cache credentials (don't type password repeatedly)
# Windows
git config --global credential.helper wincred

# macOS
git config --global credential.helper osxkeychain

# Linux
git config --global credential.helper cache
```

---

## View Your Configuration

### View All Settings

```bash
git config --list
```

### View Specific Setting

```bash
git config user.name
git config user.email
```

### View with Origin

See where each setting comes from:

```bash
git config --list --show-origin
```

---

## Configuration File Locations

Git stores configuration in text files you can edit directly:

### Global Configuration

**Windows**: `C:\Users\YourName\.gitconfig`  
**macOS/Linux**: `~/.gitconfig`

Example `.gitconfig`:

```ini
[user]
    name = Jane Smith
    email = jane.smith@university.edu
[init]
    defaultBranch = main
[core]
    editor = code --wait
    autocrlf = true
[color]
    ui = auto
[pull]
    rebase = false
```

You can edit this file directly or use `git config` commands.

---

## Setting Up SSH Keys (Optional but Recommended)

SSH keys allow you to connect to GitHub without typing your password.

### 1. Check for Existing Keys

```bash
ls -la ~/.ssh
# Look for id_rsa.pub, id_ed25519.pub, or similar
```

### 2. Generate New SSH Key

```bash
ssh-keygen -t ed25519 -C "your.email@example.com"
```

**During generation**:

- Press Enter to accept default location
- Enter a passphrase (optional but recommended)

### 3. Start SSH Agent

**Windows (Git Bash)**:

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

**macOS**:

```bash
eval "$(ssh-agent -s)"
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```

**Linux**:

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

### 4. Copy Public Key

```bash
# macOS
pbcopy < ~/.ssh/id_ed25519.pub

# Linux
cat ~/.ssh/id_ed25519.pub | xclip -selection clipboard

# Windows (Git Bash)
cat ~/.ssh/id_ed25519.pub | clip

# Or just view it
cat ~/.ssh/id_ed25519.pub
```

### 5. Add to GitHub

1. Go to [github.com](https://github.com)
2. Click your profile picture → Settings
3. Click "SSH and GPG keys"
4. Click "New SSH key"
5. Title: "My Laptop" (or any name)
6. Paste your public key
7. Click "Add SSH key"

### 6. Test Connection

```bash
ssh -T git@github.com
```

Should show:

```
Hi username! You've successfully authenticated, but GitHub does not provide shell access.
```

---

## Setting Up GitHub Account

### 1. Create Account

1. Go to [github.com](https://github.com/)
2. Click "Sign up"
3. Follow the prompts
4. **Use your university email** for education benefits

### 2. GitHub Student Benefits

With your university email, you get:

- Free GitHub Pro
- Free GitHub Copilot
- Various tool credits

Apply at: [education.github.com/students](https://education.github.com/students)

### 3. Configure Profile

- Add a profile picture
- Add your name
- Add a bio
- Set location
- Add social links

---

## Useful Git Aliases

Aliases are shortcuts for common commands.

```bash
# Status shortcut
git config --global alias.st status

# Commit shortcut
git config --global alias.ci commit

# Checkout shortcut
git config --global alias.co checkout

# Branch shortcut
git config --global alias.br branch

# Pretty log
git config --global alias.lg "log --oneline --graph --decorate --all"

# Last commit
git config --global alias.last "log -1 HEAD"

# Undo last commit (keep changes)
git config --global alias.undo "reset HEAD~1 --soft"
```

**Usage**:

```bash
git st          # Instead of: git status
git ci -m "msg" # Instead of: git commit -m "msg"
git lg          # Pretty log graph
```

---

## Verification Checklist

Make sure everything is set up correctly:

```bash
# 1. Git version
git --version
# Should be 2.30+ or higher

# 2. User name
git config user.name
# Should show your name

# 3. User email
git config user.email
# Should show your email

# 4. Default branch
git config init.defaultBranch
# Should show: main

# 5. Editor (optional)
git config core.editor
# Should show your editor

# 6. GitHub connection (if using SSH)
ssh -T git@github.com
# Should authenticate successfully
```

---

## Creating Your First Repository

Now that Git is configured, let's create a test repository:

```bash
# Create a directory
mkdir my-first-repo
cd my-first-repo

# Initialize Git repository
git init

# Create a README file
echo "# My First Repository" > README.md

# Check status
git status

# Add file to staging
git add README.md

# Make first commit
git commit -m "feat: initial commit"

# View history
git log
```

**Congratulations!** You just created your first Git repository and made your first commit! 🎉

---

## Troubleshooting

### Problem: Command not found

**Error**: `git: command not found`

**Solution**:

- Git not installed or not in PATH
- Close and reopen terminal
- Reinstall Git

### Problem: Permission denied (SSH)

**Error**: `Permission denied (publickey)`

**Solution**:

- SSH key not added to GitHub
- Follow SSH setup steps above
- Or use HTTPS instead

### Problem: Wrong email in commits

**Error**: Commits show wrong email

**Solution**:

```bash
# Fix configuration
git config --global user.email "correct.email@example.com"

# Amend last commit
git commit --amend --reset-author
```

### Problem: Editor doesn't open

**Error**: Strange editor opens or nothing happens

**Solution**:

```bash
# Set editor to VS Code
git config --global core.editor "code --wait"

# Or Nano (easier)
git config --global core.editor nano
```

---

## Next Steps

Now that Git is installed and configured, you're ready to:

1. **[Learn basic Git commands](./03-basic-commands.md)**
2. **[Understand commits](./04-commits.md)**
3. **[Work with branches](./05-branching.md)**

---

## Quick Reference Card

```bash
# Configuration
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --global init.defaultBranch main
git config --global core.editor "code --wait"

# View configuration
git config --list
git config user.name
git config user.email

# Create repository
git init

# Check everything works
git --version
git config --list
```

---

## Additional Resources

- [Git Configuration Documentation](https://git-scm.com/book/en/v2/Customizing-Git-Git-Configuration)
- [GitHub SSH Setup](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
- [Git Aliases](https://git-scm.com/book/en/v2/Git-Basics-Git-Aliases)

---

You're all set! Time to start using Git. 🚀
