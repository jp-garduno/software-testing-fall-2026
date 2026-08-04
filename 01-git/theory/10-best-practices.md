# Git Best Practices

## Commit Best Practices

### 1. Commit Often
```bash
# ✅ Good: Small, focused commits
git commit -m "feat: add login form"
git commit -m "test: add login form tests"  
git commit -m "docs: update API documentation"

# ❌ Bad: One huge commit at end of day
git commit -m "did everything"
```

### 2. Write Clear Commit Messages

**Format**:
```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

**Examples**:
```bash
feat(auth): add JWT token authentication
fix(api): correct user validation logic
docs(readme): update installation steps
style(css): format with prettier
refactor(db): optimize query performance
test(calculator): add edge case tests
chore(deps): update dependencies
```

### 3. Keep Commits Atomic

One commit = one logical change

```bash
# ✅ Good
git add login.py login_test.py
git commit -m "feat: implement login feature"

# ❌ Bad: Unrelated changes
git add login.py report.py config.py
git commit -m "various updates"
```

## Branch Best Practices

### 1. Name Branches Clearly

```bash
# ✅ Good
feature/user-authentication
fix/memory-leak-in-parser
docs/api-documentation
refactor/database-layer

# ❌ Bad
my-branch
test
new-stuff
branch1
```

### 2. Keep Branches Short-Lived

- Merge within a week
- Don't let branches diverge too much
- Delete after merging

### 3. Update Branches Regularly

```bash
# Daily: Update your feature branch with main
git checkout feature/my-feature
git merge main
```

## Merge Best Practices

### 1. Test Before Merging

```bash
# Always test first
pytest
npm test

# Then merge
git checkout main
git merge feature/my-feature
```

### 2. Review Before Merging

- Don't merge your own PRs (when possible)
- Have someone review
- Use GitHub PR reviews

### 3. Delete Merged Branches

```bash
# Delete local branch
git branch -d feature/my-feature

# Delete remote branch
git push origin --delete feature/my-feature
```

## Code Review Best Practices

### For Authors

1. **Keep PRs small** (< 400 lines changed)
2. **Add good description**
3. **Respond to comments quickly**
4. **Don't take feedback personally**
5. **Thank reviewers**

### For Reviewers

1. **Review within 24 hours**
2. **Be kind and constructive**
3. **Explain your suggestions**
4. **Approve good code**
5. **Test the changes**

## Security Best Practices

### Never Commit Secrets

```bash
# ❌ Never commit
.env
secrets.json
api_keys.txt
passwords.txt
private_keys/

# ✅ Add to .gitignore
echo ".env" >> .gitignore
echo "secrets.json" >> .gitignore
```

### If You Accidentally Commit Secrets

```bash
# 1. Remove from current commit
git rm --cached secrets.txt
git commit --amend

# 2. If already pushed, rotate the secret!
# Change password, regenerate API key, etc.
```

## .gitignore Best Practices

### Common Patterns

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

# Build
dist/
build/
```

### Use Templates

GitHub provides gitignore templates:
```bash
# Download Python .gitignore
curl https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore > .gitignore
```

## Collaboration Best Practices

### 1. Pull Before You Push

```bash
# Always pull first
git pull origin main

# Then push
git push origin main
```

### 2. Communicate

- Tell team about big changes
- Coordinate who's working on what
- Use issues/project boards

### 3. Document

- Write clear README
- Add comments for complex code
- Keep documentation updated

## Workflow Best Practices

### 1. Always Work on a Branch

```bash
# ❌ Bad: Work directly on main
git checkout main
# edit files
git commit -am "changes"

# ✅ Good: Create feature branch
git checkout -b feature/new-feature
# edit files
git commit -am "feat: add new feature"
```

### 2. Keep Main Stable

- Never push broken code to main
- All tests should pass
- Code should be reviewed

### 3. Use Pull Requests

- Even for small changes
- Get code reviewed
- Run automated tests

## History Best Practices

### 1. Don't Rewrite Public History

```bash
# ❌ Bad: Rebase pushed commits
git push origin feature
git rebase main  # Others have this branch!
git push --force  # BREAKS OTHERS' WORK

# ✅ Good: Only rebase local commits
git rebase main  # Before pushing
git push origin feature
```

### 2. Use Meaningful Tags

```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### 3. Keep Clean History

- Delete merged branches
- Squash fixup commits
- Rebase instead of merge (for local branches)

## Performance Best Practices

### 1. Use .gitignore Properly

Don't commit large binary files, build artifacts, dependencies.

### 2. Shallow Clone for CI/CD

```bash
git clone --depth=1 repo-url
```

### 3. Prune Old Branches

```bash
# Delete local branches that are gone on remote
git fetch --prune

# See what's merged
git branch --merged
```

## Emergency Procedures

### Undo Last Commit (Not Pushed)

```bash
# Keep changes
git reset HEAD~1

# Discard changes
git reset --hard HEAD~1
```

### Undo Pushed Commit

```bash
# Create new commit that undoes changes
git revert HEAD
git push
```

### Recover Deleted Branch

```bash
# Find commit hash
git reflog

# Recreate branch
git checkout -b recovered-branch <commit-hash>
```

### Fix Merge Conflict

```bash
# If stuck in merge
git merge --abort

# Start over
git reset --hard HEAD
```

## Documentation Best Practices

### README.md Should Include

1. Project description
2. Installation instructions
3. Usage examples
4. Contributing guidelines
5. License

### CONTRIBUTING.md Should Include

1. How to set up development environment
2. Coding standards
3. Commit message format
4. PR process
5. Where to ask questions

## Automation Best Practices

### Use Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Set up hooks
pre-commit install

# Hooks run automatically on commit
```

### Use CI/CD

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: npm test
```

## Checklist: Before Pushing

- [ ] Code works (tested locally)
- [ ] Tests pass
- [ ] Code is linted
- [ ] Commit messages are clear
- [ ] No secrets committed
- [ ] No unnecessary files committed
- [ ] Branch is up to date with main

## Checklist: Before Merging PR

- [ ] Code reviewed
- [ ] All tests pass
- [ ] No merge conflicts
- [ ] Documentation updated
- [ ] Approved by reviewer(s)
- [ ] Branch is up to date with main

## Common Mistakes to Avoid

1. ❌ Committing directly to main
2. ❌ Force pushing to shared branches
3. ❌ Committing secrets
4. ❌ Vague commit messages
5. ❌ Giant commits with many changes
6. ❌ Not pulling before pushing
7. ❌ Leaving branches undeleted
8. ❌ Not testing before committing
9. ❌ Ignoring conflicts
10. ❌ Rewriting public history

## Learning Resources

- [Pro Git Book](https://git-scm.com/book)
- [GitHub Guides](https://guides.github.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Best Practices](https://sethrobertson.github.io/GitBestPractices/)

## Summary

**Golden Rules**:
1. Commit often with clear messages
2. Always work on branches
3. Test before committing
4. Pull before pushing
5. Review code before merging
6. Never commit secrets
7. Keep main stable
8. Delete merged branches
9. Communicate with team
10. Learn from mistakes

Follow these practices and you'll be a Git pro! 🚀
