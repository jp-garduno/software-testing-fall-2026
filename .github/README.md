# GitHub Actions Workflows

This directory contains CI/CD workflows that automatically validate code quality, run tests, and provide feedback on student submissions.

## 📋 Available Workflows

### 1. CI - Continuous Integration (`ci.yml`)

**Triggers**: Push to `main`/`develop`, Pull Requests

**Jobs**:

- **Python Tests**: Runs pytest with coverage (Python 3.11, 3.12, 3.13, 3.14)
- **JavaScript Tests**: Runs Jest with coverage (Node 22.x, 24.x, 26.x)
- **Pre-commit Hooks**: Validates all pre-commit checks pass
- **Playwright E2E Tests**: Runs end-to-end browser tests
- **Security Scan**: Runs Trivy vulnerability scanner
- **Quality Checks**: Checks for large files, broken links, TODOs

**Status Badge**:

```markdown
![CI Status](https://github.com/[username]/software-testing-fall-2026/workflows/CI/badge.svg)
```

### 2. Student Submission Validator (`student-submission.yml`)

**Triggers**: Pull Requests modifying files in `students/**`

**Purpose**: Automatically validates student work when they submit via PR

**Actions**:

- Identifies changed Python and JavaScript files
- Runs tests on submitted code
- Checks code style (Pylint, ESLint)
- Comments on PR with validation status

**Usage for Students**:

1. Create branch: `git checkout -b feat/homework-4-john-doe`
2. Add your work in `students/your-name/` directory
3. Commit and push
4. Create PR
5. Wait for automated validation
6. Review feedback in PR comments

### 3. Homework Checker (`homework-checker.yml`)

**Triggers**: Pull Requests labeled with `homework`

**Purpose**: Provides automated feedback on homework submissions

**Actions**:

- Extracts homework number from branch name
- Runs homework-specific validation
- Checks for required files (README, tests, etc.)
- Generates feedback comment with checklist

**Usage for Students**:

1. Create PR for your homework
2. Add label `homework` (or instructor will add it)
3. Workflow runs automatically
4. Review automated feedback
5. Instructor provides manual review

## 🔧 Workflow Configuration

### Matrix Testing

Both Python and JavaScript tests run across multiple versions to ensure compatibility:

```yaml
# Python: 3.9, 3.10, 3.11, 3.12
# Node.js: 18.x, 20.x
```

### Coverage Reporting

Coverage reports are uploaded to Codecov (when configured):

- Python coverage: `coverage.xml`
- JavaScript coverage: `coverage/coverage-final.json`

### Artifacts

Failed test runs preserve artifacts for debugging:

- Playwright reports (30-day retention)
- Test output logs
- Coverage reports

## 📊 Adding Status Badges to README

Add workflow status badges to your repository README:

```markdown
[![CI Status](https://github.com/[username]/software-testing-fall-2026/workflows/CI%20-%20Continuous%20Integration/badge.svg)](https://github.com/[username]/software-testing-fall-2026/actions)

[![Student Validation](https://github.com/[username]/software-testing-fall-2026/workflows/Student%20Submission%20Validator/badge.svg)](https://github.com/[username]/software-testing-fall-2026/actions)
```

## 🛠️ Customizing Workflows

### Adding New Checks

To add a new check to CI workflow:

1. Open `.github/workflows/ci.yml`
2. Add new job:

```yaml
your-new-check:
  name: Your Check Name
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Run your check
      run: your-command
```

3. Add to summary job dependencies:

```yaml
all-checks:
  needs: [...existing-jobs, your-new-check]
```

### Modifying Test Commands

Edit the test execution steps in each workflow:

```yaml
- name: Run Python tests
  run: |
    pytest --cov=. --cov-report=xml --cov-report=html
```

### Configuring Notifications

To get notifications on workflow failures:

1. Go to GitHub Settings → Notifications
2. Enable "Actions" notifications
3. Choose email or web notifications

## 🚨 Troubleshooting

### Workflow Failing Locally Passes

**Possible causes**:

- Different Python/Node versions
- Missing dependencies
- Environment variables
- File system differences (line endings)

**Solution**:

```bash
# Check versions match workflow
python --version
node --version

# Run pre-commit checks
pre-commit run --all-files

# Clear caches
rm -rf .pytest_cache node_modules
```

### Tests Timeout

**Solution**: Increase timeout in workflow:

```yaml
- name: Run tests
  run: pytest
  timeout-minutes: 10 # Default is 360 (6 hours)
```

### Permission Errors

**Solution**: Ensure GITHUB_TOKEN has correct permissions:

```yaml
permissions:
  contents: read
  pull-requests: write
  issues: write
```

## 📚 GitHub Actions Resources

### Official Documentation

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Contexts](https://docs.github.com/en/actions/learn-github-actions/contexts)

### Useful Actions

- [actions/checkout@v4](https://github.com/actions/checkout) - Check out repository
- [actions/setup-python@v5](https://github.com/actions/setup-python) - Set up Python
- [actions/setup-node@v4](https://github.com/actions/setup-node) - Set up Node.js
- [codecov/codecov-action@v4](https://github.com/codecov/codecov-action) - Upload coverage

### Learning Resources

- [GitHub Skills: Introduction to GitHub Actions](https://skills.github.com/)
- [Awesome Actions](https://github.com/sdras/awesome-actions)

## 🎓 For Students

### Understanding Workflow Results

When you create a PR, workflows run automatically. Here's what each status means:

- ✅ **Green checkmark**: All checks passed
- ❌ **Red X**: Some checks failed - click to see details
- 🟡 **Yellow circle**: Checks are running
- ⚪ **Gray**: Checks haven't started yet

### Viewing Failed Checks

1. Click on the failed check in your PR
2. Click "Details" next to the failed job
3. Expand the failed step to see error messages
4. Fix the issues and push again

### Common Failures

| **Error**                   | **Meaning**              | **Fix**                    |
| --------------------------- | ------------------------ | -------------------------- |
| `pytest: command not found` | Python env not set up    | Install dependencies       |
| `ModuleNotFoundError`       | Missing Python package   | Add to requirements.txt    |
| `npm test failed`           | JavaScript tests failing | Run `npm test` locally     |
| `Linting errors`            | Code style issues        | Run linter locally and fix |
| `Coverage too low`          | Not enough tests         | Add more test cases        |

## 🔐 Security

### Secrets Management

Never commit sensitive data. Use GitHub Secrets for:

- API keys
- Database credentials
- Service tokens

Access in workflows:

```yaml
env:
  API_KEY: ${{ secrets.API_KEY }}
```

### Dependabot

Dependabot automatically creates PRs to update dependencies:

- Configured in `.github/dependabot.yml` (if present)
- Helps keep dependencies secure and up-to-date
- Review and merge Dependabot PRs regularly

## 📈 Monitoring

### Viewing Workflow History

1. Go to "Actions" tab in GitHub
2. Select a workflow from the left sidebar
3. View all runs with status and duration

### Performance

Monitor workflow performance:

- Check run duration
- Identify slow steps
- Optimize as needed

### Usage Limits

GitHub Actions has usage limits:

- **Public repos**: Unlimited minutes
- **Private repos**: Limited based on plan
- **Concurrent jobs**: Varies by plan

Check usage: Settings → Billing → Actions

---

**Questions?** Open an issue or ask in class!
