# Pull Requests

## What is a Pull Request?

A PR is a request to merge changes, enabling code review and discussion.

## Creating a PR

```bash
# 1. Push branch
git push origin feature/add-login

# 2. On GitHub: Create Pull Request
# 3. Fill out template
# 4. Request reviewers
# 5. Wait for approval
# 6. Merge
```

## PR Components

- **Title**: Conventional commit format
- **Description**: What, why, how
- **Reviewers**: Who should review
- **Labels**: feature, bug, docs
- **Linked Issues**: Closes #123

## Code Review

### As Author
- Keep PRs small (< 400 lines)
- Respond to feedback
- Test your code

### As Reviewer
- Review promptly (1-2 days)
- Be constructive
- Test the code

## Merge Options

1. **Merge Commit**: Keeps all commits
2. **Squash**: Combines into one commit
3. **Rebase**: Linear history

## PR Checklist

Before creating:
- [ ] Tests pass
- [ ] Code is linted  
- [ ] Branch pushed

Before merging:
- [ ] Approved
- [ ] Checks passing
- [ ] Up to date with main

Next: [Conflicts](./08-conflicts.md)
