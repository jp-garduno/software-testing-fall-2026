# Student Submission Guide

## 📚 How to Submit Assignments

All homework, exams, and project milestones are submitted through **GitHub Pull Requests** and tracked in **Canvas**.

---

## 🎯 Quick Overview

```
1. Complete work in GitHub → 2. Create PR → 3. Wait for automated grade → 4. Submit PR link to Canvas
```

**Time to grade**: 2-5 minutes (automated) ⚡

---

## 📋 Step-by-Step Guide

### Step 1: Set Up Your Workspace

**First time only**:

```bash
# Clone the repository
git clone https://github.com/jp-garduno/software-testing-fall-2026.git
cd software-testing-fall-2026

# Set up Python
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up JavaScript
npm install

# Install pre-commit hooks
pre-commit install
```

### Step 2: Create Your Branch

For each assignment, create a new branch:

```bash
# Format: feat/homework-X-yourname or feat/exam-X-yourname
git checkout -b feat/homework-4-john-doe

# Example for project
git checkout -b feat/project-milestone-2-team-alpha
```

**Branch Naming Rules**:
- Use `feat/homework-X-yourname` for homework
- Use `feat/exam-X-yourname` for exams
- Use `feat/project-milestone-X-teamname` for project
- Replace spaces with dashes
- Keep it lowercase

### Step 3: Complete Your Work

Work in the appropriate directory:

```
For Homework:
  students/yourname/homework-X/

For Exams:
  students/yourname/exam-X/

For Project:
  team-project/teamname/milestone-X/
```

**Directory Structure Example**:
```
students/john-doe/homework-4/
├── README.md                    # Your documentation
├── src/                         # Your source code
│   ├── calculator.py
│   └── validator.js
├── tests/                       # Your test files
│   ├── test_calculator.py
│   └── validator.test.js
└── docs/                        # Additional documentation
    └── test-plan.md
```

### Step 4: Run Tests Locally

**Always test locally before pushing!**

```bash
# Python tests
pytest
pytest --cov=. --cov-report=html  # With coverage

# JavaScript tests
npm test
npm test -- --coverage

# Run linting
pylint **/*.py
npm run lint

# Run all pre-commit checks
pre-commit run --all-files
```

**What to look for**:
- ✅ All tests pass
- ✅ Coverage is at least 80%
- ✅ No linting errors
- ✅ All files committed

### Step 5: Commit Your Changes

Use **conventional commits**:

```bash
# Stage your files
git add .

# Commit with proper format
git commit -m "feat(homework-4): complete boundary value analysis exercises"
```

**Commit Message Format**:
```
<type>(<scope>): <description>

Types:
- feat: New feature or exercise completion
- fix: Bug fix
- docs: Documentation only
- test: Adding tests
- refactor: Code restructuring

Examples:
✅ feat(homework-4): add equivalence partitioning tests
✅ fix(exam-2): correct coverage calculation
✅ docs(project): update README with setup instructions
✅ test(homework-3): add edge case tests
```

### Step 6: Push to GitHub

```bash
# Push your branch
git push origin feat/homework-4-john-doe
```

If this is your first push, you might need:
```bash
git push -u origin feat/homework-4-john-doe
```

### Step 7: Create Pull Request

1. **Go to GitHub** → your repository
2. **Click "Pull requests"** tab
3. **Click "New pull request"**
4. **Select your branch**:
   - base: `main`
   - compare: `feat/homework-4-john-doe`
5. **Fill out the template**:
   ```markdown
   ## Description
   Completed Homework 4: Black Box Testing

   ## Type of Change
   - [x] Homework submission

   ## Module/Assignment
   - Module: Module 4: Black Box Testing
   - Assignment: Homework 4

   ## Student Information
   - Name: John Doe
   - Student ID: 12345678

   ## Changes Made
   - Implemented equivalence partitioning tests
   - Added boundary value analysis
   - Created decision tables
   - 90% test coverage achieved

   ## Testing Performed
   - [x] All tests pass locally
   - [x] Code is properly formatted
   - [x] Linting passes
   - [x] Pre-commit hooks pass

   ## Coverage Report
   - Python Coverage: 92%
   - JavaScript Coverage: 88%
   ```
6. **Create pull request**

### Step 8: Wait for Automated Checks

GitHub Actions will automatically:
- Run all your tests
- Check code quality
- Calculate coverage
- Generate your grade

**This takes 2-5 minutes** ⏱️

Watch the PR page for:
- 🟡 Yellow dot = Running
- ✅ Green checkmark = All passed
- ❌ Red X = Something failed

### Step 9: Review Your Automated Grade

Once checks complete:

1. **Scroll down in your PR**
2. **Find "Automated Grading Report" comment**
3. **Review your grade**:
   ```
   Final Grade: 87.5/100

   Breakdown:
   - Tests: 90/100 (40% weight)
   - Coverage: 85/100 (30% weight)
   - Code Quality: 88/100 (20% weight)
   - Structure: 10/10 (10% weight)
   ```

4. **If you need to improve**:
   - Fix issues locally
   - Commit and push again
   - Checks will re-run automatically
   - Repeat until satisfied

### Step 10: Submit to Canvas

Once you're happy with your grade:

1. **Copy your PR URL**
   - Example: `https://github.com/john-doe/software-testing-fall-2026/pull/42`

2. **Go to Canvas assignment**

3. **Click "Submit Assignment"**

4. **Paste the PR link** in the URL field

5. **Click "Submit"**

**Important**: 
- ✅ Submit the **PR link**, not the repository link
- ✅ Make sure all checks are **green** ✅ before submitting
- ✅ You can see your grade in the PR **before** submitting to Canvas

---

## 🎯 Grading Breakdown

### How You're Graded (Automated)

Your final grade is calculated as:

```
Final Grade = (Tests × 40%) + (Coverage × 30%) + (Quality × 20%) + (Structure × 10%)
```

#### Tests (40%)
- **What**: Percentage of passing tests
- **How**: `(tests_passed / total_tests) × 100`
- **Example**: 18/20 tests pass = 90/100

#### Coverage (30%)
- **What**: Code coverage percentage
- **How**: Measured by coverage tools
- **Target**: Aim for 80%+
- **Example**: 85% coverage = 85/100

#### Code Quality (20%)
- **What**: Linting and style
- **How**: Pylint (Python) and ESLint (JavaScript)
- **Deductions**: Errors and warnings reduce score
- **Example**: Few minor issues = 95/100

#### Structure & Documentation (10%)
- **What**: Required files and organization
- **Points**:
  - README.md: 3 points
  - Test files: 4 points
  - Proper structure: 3 points
- **Example**: All present = 10/10

### Example Calculation

```
Your Results:
- Tests: 18/20 passed = 90/100
- Coverage: 85%
- Code Quality: 95/100 (2 minor linting warnings)
- Structure: 10/10 (all files present)

Calculation:
= (90 × 0.40) + (85 × 0.30) + (95 × 0.20) + (100 × 0.10)
= 36 + 25.5 + 19 + 10
= 90.5/100

Your Grade: 90.5/100 🎉
```

---

## ✅ Checklist Before Submitting

Use this checklist for every assignment:

### Local Testing
- [ ] All tests pass (`pytest` and `npm test`)
- [ ] Coverage is at least 80%
- [ ] No linting errors
- [ ] Code is properly formatted
- [ ] Pre-commit hooks pass

### Documentation
- [ ] README.md is complete
- [ ] Code has necessary comments
- [ ] Test cases are documented
- [ ] Setup instructions are clear

### GitHub
- [ ] Branch name follows convention
- [ ] Commits use conventional format
- [ ] PR template is filled out
- [ ] All automated checks are green ✅

### Canvas
- [ ] PR link is copied
- [ ] Assignment is selected
- [ ] Submission is confirmed

---

## 🚨 Common Issues & Solutions

### Issue 1: Tests Pass Locally, Fail in GitHub

**Why**: Different environment or missing files

**Solution**:
```bash
# Check Python version
python --version  # Should be 3.9-3.12

# Check Node version
node --version    # Should be 18.x or 20.x

# Clean and reinstall
rm -rf venv node_modules
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
npm ci

# Test again
pytest
npm test
```

### Issue 2: Linting Errors

**Why**: Code doesn't follow style guidelines

**Solution**:
```bash
# Python - auto-fix most issues
black .
isort .

# JavaScript - auto-fix
npm run lint:fix

# Check what remains
pylint **/*.py
npm run lint
```

### Issue 3: Low Coverage

**Why**: Not enough tests

**Solution**:
```bash
# See what's missing
pytest --cov=. --cov-report=html
open htmlcov/index.html  # View report

# Add tests for:
# - Red/orange lines in coverage report
# - Edge cases
# - Error conditions
```

### Issue 4: Can't Create PR

**Why**: Branch not pushed or conflicts

**Solution**:
```bash
# Make sure branch is pushed
git push origin your-branch-name

# Update from main if needed
git fetch origin
git rebase origin/main

# Resolve conflicts if any
# Then push again
```

### Issue 5: Wrong Grade

**Why**: Misunderstanding or actual error

**Solution**:
1. Review grading report in PR comments
2. Check which component is low
3. Review the rubric
4. If you think there's an error, ask instructor
5. Provide specific details about discrepancy

---

## 🎓 Tips for Success

### General Tips

1. **Start Early**
   - Don't wait until the deadline
   - Gives you time to fix issues
   - Automated grading is instant, but fixing takes time

2. **Test Frequently**
   - Run tests after every change
   - Don't write all code then test
   - Faster to fix issues immediately

3. **Read Error Messages**
   - They tell you exactly what's wrong
   - Click "Details" on failed checks
   - Learn from the feedback

4. **Ask for Help**
   - Use GitHub Discussions
   - Ask in class
   - Check with classmates (but don't copy code)

5. **Keep PRs Clean**
   - One PR per assignment
   - Don't mix homework with exams
   - Close old PRs before new ones

### Testing Tips

1. **Write Tests First** (TDD approach)
   - Helps design better code
   - Ensures you meet requirements
   - Higher coverage naturally

2. **Test Edge Cases**
   - Empty inputs
   - Maximum/minimum values
   - Invalid data
   - Error conditions

3. **Use Descriptive Test Names**
   - `test_add_positive_numbers`
   - `test_divide_by_zero_raises_error`
   - Helps understand failures

### Code Quality Tips

1. **Use Meaningful Names**
   - `calculateDiscount` not `calc`
   - `userEmail` not `x`

2. **Keep Functions Small**
   - One function = one purpose
   - Easier to test
   - Better grade on quality

3. **Remove Debug Code**
   - No `console.log()` or `print()`
   - Use proper logging if needed
   - Clean code scores higher

---

## 📞 Getting Help

### During the Assignment

1. **GitHub Discussions**: Ask questions, help classmates
2. **Office Hours**: Weekly office hours available
3. **Email Instructor**: For private concerns
4. **Class**: Ask during next session

### After Submission

1. **Review PR Comments**: Automated + instructor feedback
2. **Request Clarification**: If grade seems wrong
3. **Resubmission**: Check if allowed for your assignment

---

## 📚 Resources

- [Git Workflow Guide](./01-git/README.md)
- [Testing Best Practices](./resources/README.md)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Python Testing with pytest](https://docs.pytest.org/)
- [JavaScript Testing with Jest](https://jestjs.io/)

---

## ❓ FAQ

**Q: Can I submit multiple times?**
A: You can push to your PR multiple times. Each push re-runs the automated checks. Only submit to Canvas when you're satisfied with your grade.

**Q: What if I submit late?**
A: Follow the course late policy. Automated grading still works, but Canvas may mark it late.

**Q: Can I see others' submissions?**
A: If the repository is public, yes. But don't copy code - that's academic dishonesty.

**Q: What if automated grading is wrong?**
A: Review the grading report carefully. If you believe there's an error, contact your instructor with specific details.

**Q: Do I need to merge my PR?**
A: No! Just create the PR. Instructor will review and merge if appropriate.

**Q: Can I work with a partner?**
A: Follow the assignment instructions. Some allow collaboration, most don't. For team project, yes!

**Q: What's the minimum grade to pass?**
A: Check your syllabus. Aim for 70%+ on all submissions.

---

**Good luck with your assignments!** 🚀

Remember: The automated grading is there to help you, not trick you. It gives you instant feedback so you can improve before the instructor even looks at your work!
