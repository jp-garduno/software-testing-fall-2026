# Milestone 2: Foundation & Setup

**Due**: End of Week 6  
**Points**: 10 (10% of project grade)  
**Focus**: Repository setup, static testing, development environment  
**Modules Applied**: Git (Module 1), Static Testing (Module 3)

---

## 🎯 Objectives

- Set up professional Git workflow
- Configure pre-commit hooks and linting
- Establish code quality standards
- Create basic project structure
- Set up CI/CD pipeline (basic)
- Implement foundational features

---

## 📋 Deliverables

### 1. GitHub Repository Setup (20 points)

#### 1.1 Repository Configuration

**Required settings**:

- [ ] Public repository (or private with instructor access)
- [ ] All team members added as collaborators
- [ ] Branch protection rules on `main`:
  - Require pull request reviews (at least 1)
  - Require status checks to pass
  - No direct pushes to `main`
- [ ] `.gitignore` configured for your stack
- [ ] License file (MIT recommended)
- [ ] Comprehensive README.md

**README.md Requirements**:

```markdown
# Project Name

Brief description (2-3 sentences)

## Team Members

- Name (Role) - GitHub: @username
- ...

## Features

- [ ] Feature 1
- [ ] Feature 2
- ...

## Technology Stack

**Backend**: Python/FastAPI
**Frontend**: React
**Database**: PostgreSQL
**Testing**: pytest, Jest, Selenium

## Setup Instructions

### Prerequisites

- Python 3.11+
- Node.js 22+
- PostgreSQL

### Installation

[Step-by-step instructions]

### Running the Application

[How to run locally]

### Running Tests

[How to run test suites]

## Project Structure

[Directory tree]

## Contributing

See CONTRIBUTING.md

## License

MIT
```

#### 1.2 Branching Strategy

Document branching strategy in `CONTRIBUTING.md`:

- `main` - Production-ready code
- `develop` - Integration branch
- `feature/<name>` - New features
- `fix/<name>` - Bug fixes
- `hotfix/<name>` - Emergency fixes

**Pull Request Template** (`.github/PULL_REQUEST_TEMPLATE.md`):

```markdown
## Description

[What does this PR do?]

## Related Issue

Closes #[issue number]

## Type of Change

- [ ] New feature
- [ ] Bug fix
- [ ] Documentation
- [ ] Refactoring

## Testing

- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Checklist

- [ ] Code follows project style guidelines
- [ ] Pre-commit hooks pass
- [ ] All tests pass
- [ ] Documentation updated
```

---

### 2. Static Testing Configuration (25 points)

#### 2.1 Pre-commit Hooks

Create `.pre-commit-config.yaml`:

```yaml
repos:
  # General hooks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-merge-conflict
      - id: detect-private-key

  # Python hooks
  - repo: https://github.com/psf/black
    rev: 24.1.1
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pycqa/pylint
    rev: v3.0.3
    hooks:
      - id: pylint
        args: ["--rcfile=.pylintrc"]

  # JavaScript/TypeScript hooks (if applicable)
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v9.0.0
    hooks:
      - id: eslint
        files: \.(js|jsx|ts|tsx)$
        additional_dependencies:
          - eslint@8.56.0
          - "@typescript-eslint/parser@6.20.0"
          - "@typescript-eslint/eslint-plugin@6.20.0"

  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v4.0.0-alpha.8
    hooks:
      - id: prettier
        types_or: [javascript, jsx, ts, tsx, json, css, markdown]

  # Conventional commits (optional but recommended)
  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: v3.0.0
    hooks:
      - id: conventional-pre-commit
        stages: [commit-msg]
```

**Installation**:

```bash
pip install pre-commit
pre-commit install
pre-commit install --hook-type commit-msg
```

#### 2.2 Linting Configuration

**Python** - Create `.pylintrc`:

```ini
[MASTER]
max-line-length=120
disable=
    C0111,  # missing-docstring
    R0903,  # too-few-public-methods (OK for models)

[MESSAGES CONTROL]
confidence=HIGH

[FORMAT]
indent-string='    '
```

**JavaScript/TypeScript** - Create `.eslintrc.json`:

```json
{
  "extends": ["eslint:recommended", "prettier"],
  "env": {
    "node": true,
    "browser": true,
    "es2021": true,
    "jest": true
  },
  "parserOptions": {
    "ecmaVersion": 2021,
    "sourceType": "module"
  },
  "rules": {
    "no-console": "warn",
    "no-unused-vars": "error"
  }
}
```

Create `.prettierrc`:

```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2
}
```

#### 2.3 Conventional Commits

Document commit message format in `CONTRIBUTING.md`:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Examples**:

```
feat(auth): add user registration endpoint
fix(cart): correct total price calculation
docs(readme): update installation instructions
test(orders): add unit tests for order service
```

---

### 3. CI/CD Pipeline (20 points)

#### 3.1 GitHub Actions Workflow

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test-python:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run linting
        run: |
          pip install black isort pylint
          black --check .
          isort --check .
          pylint src/

      - name: Run tests
        run: |
          pytest --cov=src --cov-report=xml --cov-report=html

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml

  test-javascript:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [22, 24]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}

      - name: Install dependencies
        run: npm ci

      - name: Run linting
        run: npm run lint

      - name: Run tests
        run: npm test -- --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage/coverage-final.json
```

**Required**: CI must pass before merging any PR.

---

### 4. Project Structure (15 points)

Create a well-organized project structure:

```
team-project/
├── .github/
│   ├── workflows/
│   │   └── ci.yml
│   └── PULL_REQUEST_TEMPLATE.md
├── docs/
│   └── milestones/
│       ├── M1/
│       └── M2/
├── src/                    # Source code
│   ├── api/               # Backend API
│   │   ├── __init__.py
│   │   ├── app.py
│   │   ├── models/
│   │   ├── routes/
│   │   └── services/
│   └── frontend/          # Frontend code
│       ├── components/
│       ├── pages/
│       └── utils/
├── tests/                 # All tests
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   └── performance/
├── .env.example           # Environment variables template
├── .gitignore
├── .pre-commit-config.yaml
├── .pylintrc              # Python linting config
├── .eslintrc.json         # JS linting config
├── .prettierrc            # Prettier config
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── requirements.txt       # Python dependencies
├── package.json           # Node.js dependencies
└── pyproject.toml         # Python project config
```

---

### 5. Foundational Features (20 points)

Implement basic working features:

#### 5.1 Backend (10 points)

**Minimum requirements**:

- [ ] Database connection working
- [ ] User model defined
- [ ] User registration endpoint (`POST /api/users/register`)
- [ ] User login endpoint (`POST /api/users/login`)
- [ ] Authentication working (JWT or sessions)
- [ ] At least one protected endpoint
- [ ] Basic error handling
- [ ] Environment configuration

**Example API structure** (Flask/FastAPI):

```python
# src/api/routes/auth.py
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/register")
async def register(user_data: UserCreate):
    """Register a new user"""
    # Implementation
    pass

@router.post("/login")
async def login(credentials: UserLogin):
    """Authenticate user and return token"""
    # Implementation
    pass
```

#### 5.2 Frontend (Optional for M2, 5 bonus points)

If implementing frontend already:

- [ ] Basic UI setup (React/Vue/etc)
- [ ] Login page
- [ ] Registration page
- [ ] Protected route example
- [ ] API integration working

#### 5.3 Database (5 points)

- [ ] Database created and accessible
- [ ] Initial schema/models defined
- [ ] Migrations set up (Alembic for Python, Knex for Node.js)
- [ ] Seed data (optional)

---

## 📤 Submission Instructions

### 1. Create Pull Request

```bash
# Create feature branch
git checkout -b milestone-2-foundation

# Make all changes
git add .
git commit -m "feat(setup): complete M2 foundation and setup"

# Push and create PR
git push -u origin milestone-2-foundation
gh pr create --title "Milestone 2: Foundation & Setup" --body "..."
```

### 2. Required Documentation

Create `docs/milestones/M2/setup-report.md`:

```markdown
# Milestone 2: Setup Report

## Team: [Team Name]

## Completed Tasks

- [x] Repository configured with branch protection
- [x] Pre-commit hooks installed and working
- [x] CI/CD pipeline passing
- [x] Project structure created
- [x] Basic authentication implemented

## Setup Instructions

[How team members can set up the project locally]

## Testing the Setup

[How to verify everything works]

## Challenges Faced

[Any issues encountered and how you solved them]

## Screenshots

[Screenshots of CI passing, pre-commit working, etc.]

## Next Steps

[What you'll work on for M3]
```

### 3. Submit on Canvas

- **Pull Request URL**: Link to your M2 PR
- **CI Status**: Must be passing (green checkmark)
- **Documentation**: Link to `setup-report.md`

---

## 🎯 Grading Rubric

| Category                  | Points | Criteria                                          |
| ------------------------- | ------ | ------------------------------------------------- |
| **Repository Setup**      | 20     | Branch protection, collaborators, README complete |
| **Static Testing**        | 25     | Pre-commit hooks, linting configured and working  |
| **CI/CD Pipeline**        | 20     | GitHub Actions running, tests passing             |
| **Project Structure**     | 15     | Clean organization, proper separation             |
| **Foundational Features** | 20     | Auth working, database connected, endpoints work  |
| **Documentation**         | 10     | Setup report clear, instructions work             |
| **Code Quality**          | 10     | Clean code, consistent style, good commits        |
| **Bonus: Frontend**       | +5     | Basic UI implemented                              |

**Total**: 120 points (20% bonus available)

**Requirements for Full Credit**:

- All pre-commit hooks must pass
- CI pipeline must be green
- At least 5 meaningful commits from each team member
- All code follows conventional commits format

**Deductions**:

- CI not passing: -15 points
- Pre-commit hooks not working: -10 points
- Direct commits to main: -5 points each
- Missing branch protection: -10 points
- Poor code organization: -5 points

---

## ✅ Checklist

Before submitting:

### Repository

- [ ] Repository created and shared with team
- [ ] All team members have pushed at least one commit
- [ ] Branch protection enabled on `main`
- [ ] README.md complete and informative
- [ ] LICENSE file added
- [ ] .gitignore properly configured

### Static Testing

- [ ] `.pre-commit-config.yaml` created
- [ ] Pre-commit installed and working
- [ ] All hooks pass locally
- [ ] Linting rules configured
- [ ] Conventional commits enforced

### CI/CD

- [ ] GitHub Actions workflow created
- [ ] CI runs on PRs and pushes
- [ ] All checks passing (green)
- [ ] Coverage reports generated

### Code

- [ ] Project structure organized
- [ ] Database connection working
- [ ] User registration endpoint works
- [ ] User login endpoint works
- [ ] Authentication implemented
- [ ] Error handling in place
- [ ] Environment variables configured

### Documentation

- [ ] CONTRIBUTING.md created
- [ ] PR template created
- [ ] Setup report written
- [ ] Setup instructions tested by team member

### Testing

- [ ] Can run `pytest` successfully (Python)
- [ ] Can run `npm test` successfully (JS)
- [ ] Basic tests written (even if minimal)

---

## 💡 Tips for Success

### Week 5: Planning

- Review M1 feedback
- Set up local environments first
- Divide configuration tasks among team
- Test pre-commit hooks before committing

### Week 6: Implementation

- Backend team: Focus on auth endpoints
- Frontend team (if starting): Basic pages
- QA lead: Set up testing framework
- DevOps: CI/CD configuration

### Common Issues

**Pre-commit hooks failing**:

```bash
# Update hooks
pre-commit autoupdate

# Run manually to debug
pre-commit run --all-files
```

**CI failing but tests pass locally**:

- Check Python/Node versions match
- Verify all dependencies in requirements.txt/package.json
- Check environment variables

**Merge conflicts**:

- Sync with `main` frequently
- Communicate with team before modifying shared files
- Use smaller, focused PRs

### Git Workflow Best Practices

1. **Pull before you push**:

   ```bash
   git checkout main
   git pull
   git checkout your-branch
   git merge main
   ```

2. **Commit early, commit often**
3. **Write descriptive commit messages**
4. **Review your own PR before requesting review**
5. **Address review comments promptly**

---

## 📚 Resources

- [GitHub Branch Protection Guide](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches)
- [Pre-commit Documentation](https://pre-commit.com/)
- [Conventional Commits Spec](https://www.conventionalcommits.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Setup Examples](../examples/setup-examples/)

---

## ❓ FAQ

**Q: Should we implement all features by M2?**  
A: No! Just authentication and basic setup. Main features come in M3-M4.

**Q: What if pre-commit hooks are too strict?**  
A: You can adjust rules in config files, but don't disable them entirely. Discuss with team.

**Q: Can we use Docker?**  
A: Yes, encouraged! Helps with environment consistency. Add Docker setup bonus points.

**Q: How many commits should we have?**  
A: Quality over quantity, but aim for 5+ per member. Shows active participation.

**Q: What if CI keeps failing?**  
A: Debug locally first. Check Actions logs for details. Ask for help in office hours.

**Q: Should we have tests by M2?**  
A: Basic tests are encouraged. Main test suite comes in M4. At minimum, have test framework configured.

---

**This milestone sets the foundation for your entire project. Take time to do it right!** 🏗️✨
