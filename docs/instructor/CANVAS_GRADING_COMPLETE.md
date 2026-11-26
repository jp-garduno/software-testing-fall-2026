# ✅ Canvas + GitHub Automated Grading - Setup Complete!

## 🎉 What You Have Now

Your Software Testing course now has **fully automated grading** integrated with Canvas. No manual grading required!

---

## 📊 Complete System Overview

### Student Experience (Simplified)

```
1. Student works in GitHub
   └─→ Commits, pushes, creates PR

2. Automated tests run (2-5 min)
   ├─→ All tests execute
   ├─→ Coverage calculated
   ├─→ Code quality checked
   └─→ Grade generated (0-100)

3. Student sees grade instantly
   └─→ In PR comments on GitHub

4. Student submits PR link to Canvas
   └─→ Simple URL submission

5. You import grades to Canvas
   └─→ One-click CSV import
```

### Your Experience (Minimal Effort)

```
1. Assignment due
   └─→ Students submit PR links in Canvas

2. Review GitHub PRs
   └─→ Automated grades already calculated
   └─→ Just review code if needed

3. Download grades
   └─→ Actions → Download CSV artifact

4. Import to Canvas
   └─→ Gradebook → Import → Done

5. Add manual feedback (optional)
   └─→ PR comments or Canvas
```

**Time saved**: ~90% of grading time! ⚡

---

## 📁 New Files Created

### Automated Grading System

1. **`.github/workflows/grading-automation.yml`**
   - Main automated grading workflow
   - Runs tests, calculates coverage, checks quality
   - Generates grades and reports
   - Creates Canvas-ready CSV files
   - Updates master gradebook

### Documentation

2. **`CANVAS_INTEGRATION.md`** (17KB)

   - Complete guide for instructors
   - Canvas setup instructions
   - Grade import process
   - Customization options
   - Troubleshooting

3. **`STUDENT_SUBMISSION_GUIDE.md`** (15KB)
   - Step-by-step for students
   - Complete submission workflow
   - Common issues & solutions
   - Grading breakdown explained
   - Tips for success

### Updates

4. **Main README.md** - Updated with:
   - Submission process
   - Links to guides
   - Assessment structure

---

## 🔧 How Automated Grading Works

### Grading Formula

```
FINAL GRADE = (Tests × 40%) + (Coverage × 30%) + (Quality × 20%) + (Structure × 10%)
```

### Components Measured

#### 1. Tests (40%)

```python
# Runs the Python and JavaScript tests of the submission directory
pytest -v --junitxml=python-results.xml --cov=src   # --cov=. without src/
npm test -- --coverage --json                       # only with the submission's own package.json
npx playwright test --reporter=json                 # homework 8 only, next to each playwright.config.*
behave -f json / npx cucumber-js --format json      # homework 8 only, one test per BDD scenario

# Pass rate over all of them; a pytest error (e.g. in a fixture) counts as failed,
# skipped and xfailed tests count neither way
tests_score = passed / (passed + failed) × 100
```

#### 2. Coverage (30%)

```python
# Statement coverage per language (homework 5: statements and branches together),
# averaged over the languages that produced a report
coverage = average(python_coverage, javascript_coverage)

# Full credit at the course target of 80%, proportional below it
coverage_score = min(coverage / 80 × 100, 100)    # 60% covered -> 75/100
# No report in either language -> 0
```

#### 3. Code Quality (20%)

```python
# Pylint with the course configuration (.github/grading/pylintrc: 120-column lines,
# docstrings not counted), or the submission's own configuration if it has one
python_quality = pylint_score × 10                  # 8.5/10 -> 85/100

# ESLint errors (warnings are reported but not penalized)
javascript_quality = 100 if errors == 0 else 85 if errors <= 5 else 70 if errors <= 10 else 50

# Averaged over the languages that were linted; a linter that cannot run is left out
quality_score = average(python_quality, javascript_quality)
```

#### 4. Structure (10%)

```bash
# Checks required files
[ -f README.md ] → +2 points (+1 in homework 2, 3 and 9)
[ test files exist ] → +4 points
[ -d src ] || [ -d tests ] → +4 points
```

Homework 1, 2, 3, 8 and 9 have their own checks for the files each assignment asks for (see "Check required files"
in `.github/workflows/grading-automation.yml`). Homework 1 and 2 weigh structure 60% and give full marks for tests,
coverage and quality; homework 3 weighs structure 75% and quality 25%; homework 8, whose application under test is
an external site, grades no coverage and weighs tests 70%, quality 20% and structure 10%; homework 9, a JMeter
assignment with no code, is graded on structure only.

### Example Grading Run

```
Student: Jane Smith
Assignment: Homework 4
PR: #45

Tests:
- Python: 18/20 passed (90%)
- JavaScript: 15/15 passed (100%)
- Combined: 33/35 = 94.3%

Coverage:
- Python: 68%
- JavaScript: no report, left out
- Graded: 68% of the 80% target = 85/100

Code Quality:
- Pylint: 8.5/10 -> 85/100
- ESLint: 0 errors, 2 warnings -> 100/100
- Score: 92.5/100

Structure:
- README.md ✅
- Tests present ✅
- tests/ directory ✅
- Score: 10/10

FINAL CALCULATION:
= (94.3 × 0.40) + (85 × 0.30) + (92.5 × 0.20) + (100 × 0.10)
= 37.72 + 25.5 + 18.5 + 10
= 91.72/100

Grade: 91.72/100
```

---

## 🚀 Activation Checklist

### Before Semester Starts

- [ ] **Push all files to GitHub**

  ```bash
  cd c:/tmp/software-testing-fall-2026
  git add .
  git commit -m "feat: add automated grading with Canvas integration"
  git push origin main
  ```

- [ ] **Enable GitHub Actions**

  - Settings → Actions → Allow all actions

- [ ] **Test automated grading**

  - Create sample PR
  - Verify grading runs
  - Check CSV output

- [ ] **Set up Canvas course**

  - Create assignments
  - Configure for URL submission
  - Add instructions

- [ ] **Prepare student materials**
  - Share STUDENT_SUBMISSION_GUIDE.md
  - Demo the process in class
  - Answer questions

### First Week of Class

- [ ] **Introduce the system**

  - Explain GitHub + Canvas workflow
  - Show example PR and grading
  - Walk through submission process

- [ ] **Test with students**

  - Simple "Hello World" assignment
  - Verify they can create PRs
  - Check Canvas submissions work

- [ ] **Monitor first submissions**
  - Watch for common issues
  - Help students troubleshoot
  - Adjust documentation if needed

### Ongoing

- [ ] **Weekly grade imports**

  - Download CSVs from GitHub
  - Import to Canvas
  - Don't let grades pile up

- [ ] **Spot check grades**

  - Randomly verify automated grades
  - Adjust rubric if needed
  - Document edge cases

- [ ] **Provide feedback**
  - Add manual comments on PRs
  - Highlight good practices
  - Explain grade components

---

## 📖 Key Documents for Students

Share these links in Canvas:

1. **[STUDENT_SUBMISSION_GUIDE.md](../student/STUDENT_SUBMISSION_GUIDE.md)**

   - Complete walkthrough
   - Checklist
   - Troubleshooting
   - **Post in Canvas announcements**

2. **[CONTRIBUTING.md](./CONTRIBUTING.md)**

   - Git workflow
   - Commit standards
   - Code style

3. **Main [README.md](./README.md)**
   - Course overview
   - Module links
   - Resources

---

## 🎓 Teaching with This System

### Week 1: Introduction

**In-Class Demo** (30 minutes):

1. Show the course repository
2. Walk through a sample PR
3. Demonstrate automated grading
4. Show how to submit to Canvas
5. Answer questions

**Assignment**: Practice PR (not graded)

- Create branch
- Make small change
- Create PR
- See automated checks

### Week 2-16: Regular Workflow

**For Each Assignment**:

1. Post assignment in Canvas
2. Include GitHub instructions
3. Students submit PR links
4. Review PRs (automated grades already calculated)
5. Import grades weekly
6. Provide feedback

### Handling Issues

**Student Can't Create PR**:

- Check branch is pushed
- Verify repository access
- Review Git basics from Module 1

**Automated Grading Fails**:

- Check Actions tab for errors
- Common: missing dependencies, syntax errors
- Can re-run workflow manually

**Grade Seems Wrong**:

- Review grading report with student
- Check test output
- Explain rubric weights
- Adjust manually if justified

---

## 💰 Cost & Resources

### GitHub Actions

**Free Tier** (Public Repositories):

- ✅ **Unlimited** minutes for public repos
- ✅ **Unlimited** storage (within reason)
- ✅ **Concurrent jobs**: 20

**For This Course**:

- Each grading run: ~5 minutes
- With 30 students: 150 minutes per assignment
- 9 assignments + 3 exams: ~1,800 minutes total
- **Cost**: $0 (public repository)

### Benefits vs Traditional Grading

**Traditional Manual Grading**:

- 30 students × 9 assignments = 270 submissions
- 15 minutes per submission = 67.5 hours
- At $50/hour = $3,375 worth of time

**Automated Grading**:

- Setup time: 4 hours ($200)
- Ongoing per assignment: 30 minutes ($25)
- Total semester: ~8 hours ($400)

**Savings**: $2,975 + better consistency + instant feedback! 💰

---

## 🔧 Customization Options

### Adjust Grading Weights

Edit `.github/workflows/grading-automation.yml`:

```yaml
# Default weights
TESTS_WEIGHT=40
COVERAGE_WEIGHT=30
CODE_QUALITY_WEIGHT=20
STRUCTURE_WEIGHT=10

# For exams (emphasize correctness)
TESTS_WEIGHT=60
COVERAGE_WEIGHT=20
CODE_QUALITY_WEIGHT=10
STRUCTURE_WEIGHT=10

# For projects (emphasize quality)
TESTS_WEIGHT=30
COVERAGE_WEIGHT=25
CODE_QUALITY_WEIGHT=30
STRUCTURE_WEIGHT=15
```

### Add Manual Component

Keep automated for objective metrics, add manual for subjective:

```
Automated Grade (80%):
- Tests: 40%
- Coverage: 30%
- Quality: 20%
- Structure: 10%

Manual Grade (20%):
- Code design
- Documentation quality
- Problem-solving approach
- Innovation/creativity
```

### Assignment-Specific Rubrics

Create separate workflows:

- `grading-homework.yml`
- `grading-exam.yml`
- `grading-project.yml`

Or use conditionals based on labels.

---

## 📊 Monitoring & Analytics

### View All Grades

**Master Gradebook**:

```bash
# View all grades
cat .gradebook/master-gradebook.csv

# Statistics
wc -l .gradebook/master-gradebook.csv  # Total submissions
grep "homework-4" .gradebook/master-gradebook.csv | wc -l  # Assignment count

# Average grade for assignment
grep "homework-4" .gradebook/master-gradebook.csv | awk -F',' '{sum+=$3; count++} END {print sum/count}'
```

**GitHub Insights**:

- Actions tab → Workflows
- See success rate
- Monitor timing
- Track issues

### Reports for Administration

Generate reports easily:

```bash
# Submission rate
grep "homework-4" .gradebook/master-gradebook.csv | wc -l
echo "out of 30 students"

# Grade distribution
grep "homework-4" .gradebook/master-gradebook.csv | awk -F',' '
  {if ($3>=90) A++; else if ($3>=80) B++; else if ($3>=70) C++; else D++}
  END {print "A:",A, "B:",B, "C:",C, "D:",D}'

# Average, min, max
grep "homework-4" .gradebook/master-gradebook.csv | awk -F',' '
  {sum+=$3; if(NR==1||$3<min) min=$3; if(NR==1||$3>max) max=$3; count++}
  END {print "Avg:",sum/count, "Min:",min, "Max:",max}'
```

---

## 🆘 Support & Troubleshooting

### For Students

Common issues and solutions documented in:

- [STUDENT_SUBMISSION_GUIDE.md](../student/STUDENT_SUBMISSION_GUIDE.md)

Quick answers:

- **Tests fail**: Fix code, push again
- **Low coverage**: Add more tests
- **Linting errors**: Run formatters
- **Can't create PR**: Check branch pushed

### For You

**GitHub Actions not running**:

1. Check Actions are enabled
2. Verify workflow syntax
3. Check triggers match

**Grades not calculating**:

1. Review Actions logs
2. Check test output
3. Verify rubric weights

**Canvas import failing**:

1. Check CSV format
2. Verify student IDs
3. Manual import as backup

**Need to regrade**:

```bash
# Re-run workflow for specific PR
gh workflow run grading-automation.yml -f pr_number=42
```

---

## ✅ Final Checklist

Before using with students:

- [ ] All workflow files pushed to GitHub
- [ ] GitHub Actions enabled and tested
- [ ] Sample PR created and graded successfully
- [ ] Canvas assignments created with URL submission
- [ ] Student guide shared in Canvas
- [ ] Demo prepared for first class
- [ ] Office hours scheduled for support
- [ ] Backup plan if system fails (manual grading)

---

## 📚 Additional Resources

- [Canvas Integration Guide](./CANVAS_INTEGRATION.md) - Full instructor guide
- [Student Submission Guide](../student/STUDENT_SUBMISSION_GUIDE.md) - For students
- [GitHub Actions Docs](.github/README.md) - Technical details
- [GitHub Actions Setup](./GITHUB_ACTIONS_SETUP.md) - Initial setup guide

---

## 🎉 Congratulations!

You now have a **state-of-the-art automated grading system** that:

✅ Saves you hours of manual grading  
✅ Provides instant feedback to students  
✅ Ensures consistent, objective grading  
✅ Scales to any class size  
✅ Integrates seamlessly with Canvas  
✅ Tracks all submissions automatically  
✅ Generates reports for administration  
✅ Works 24/7 without human intervention

**Ready to revolutionize your teaching!** 🚀

---

**Questions?** Review the documentation or open an issue in the repository!
