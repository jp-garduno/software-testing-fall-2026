# Canvas Integration Guide

## 🎯 Overview

This course uses **GitHub for submission** and **Canvas for grade recording**. Students submit their work via GitHub Pull Requests, automated grading runs via GitHub Actions, and you import grades into Canvas.

**No manual grading required!** ✨

---

## 📋 How It Works

### Student Workflow

```
1. Student completes assignment in their branch
   ├─→ Commits with proper messages
   └─→ Runs tests locally

2. Student pushes and creates Pull Request
   └─→ GitHub Actions runs automatically

3. Automated grading happens
   ├─→ Runs all tests
   ├─→ Calculates coverage
   ├─→ Checks code quality
   ├─→ Checks required files
   └─→ Generates grade (0-100)

4. Student submits to Canvas
   ├─→ Submits GitHub PR link
   └─→ Example: https://github.com/user/repo/pull/123

5. You import grades to Canvas
   └─→ Download CSV from GitHub Actions
   └─→ Import to Canvas gradebook
```

### Instructor Workflow

```
1. Student submits PR link in Canvas
   └─→ You receive Canvas notification

2. Visit the GitHub PR
   └─→ See automated grade in comments
   └─→ Review code if needed
   └─→ Add manual feedback (optional)

3. Download grade CSV from GitHub Actions
   └─→ Go to Actions tab
   └─→ Find "Automated Grading" workflow
   └─→ Download "canvas-import" artifact

4. Import to Canvas
   └─→ Canvas Gradebook → Import
   └─→ Upload CSV file
   └─→ Grades automatically populate
```

---

## 🎓 Canvas Setup

### 1. Create Assignment in Canvas

For each homework/exam/project milestone:

1. **Go to Canvas → Assignments → +Assignment**

2. **Configure Assignment**:

   ```
   Name: Homework 1 - Git Fundamentals
   Points: 100
   Submission Type: External Tool OR Website URL
   ```

3. **Use "Website URL" submission type**:

   - Students will submit GitHub PR link
   - Example format: `https://github.com/[username]/[repo]/pull/[number]`

4. **Add instructions**:

   ```markdown
   ## Submission Instructions

   1. Complete your work in the GitHub repository
   2. Create a Pull Request with your changes
   3. Ensure all automated checks pass (green checkmarks)
   4. Copy your PR link (https://github.com/...)
   5. Submit the PR link here in Canvas

   ## Grading

   Your work will be graded automatically via GitHub Actions:

   - Tests (40%)
   - Code Coverage (30%)
   - Code Quality (20%)
   - Structure/Documentation (10%)

   You can see your automated grade in the PR comments.
   ```

### 2. Gradebook Configuration

**Option A: Manual Import (Recommended for start)**

- Download CSV from GitHub Actions
- Import to Canvas gradebook
- Quick and simple

**Option B: Canvas API Integration (Advanced)**

- Set up automatic grade sync
- Requires Canvas API token
- See "Advanced Integration" section below

---

## 📥 Importing Grades to Canvas

### Method 1: Individual Assignment Import

1. **Go to GitHub Actions**

   - Navigate to your repository
   - Click "Actions" tab
   - Click "Automated Grading" workflow

2. **Find Completed Run**

   - Look for runs with ✅ green checkmark
   - Click on the run for the student's PR

3. **Download Artifact**

   - Scroll to "Artifacts" section at bottom
   - Download `canvas-import-pr-[number].zip`
   - Extract `canvas-grade.csv`

4. **Import to Canvas**
   - Canvas → Grades → Import
   - Upload the CSV file
   - Review and confirm import

**CSV Format**:

```csv
Student,Assignment,Score,Max Points,Submission Date,Comments
john_doe,1,85.5,100,2026-09-15,Automated grading via GitHub Actions - PR #42
```

### Method 2: Bulk Import (All Students)

Use the master gradebook that accumulates all grades:

1. **Access Master Gradebook**

   - Located in `.gradebook/master-gradebook.csv` in repository
   - Updated automatically when PRs merge

2. **Download Master Gradebook**

   ```bash
   # Clone or pull repository
   git pull origin main

   # View gradebook
   cat .gradebook/master-gradebook.csv
   ```

3. **Filter for Specific Assignment**

   ```bash
   # Filter homework 4 grades
   grep "homework-4" .gradebook/master-gradebook.csv > hw4-grades.csv
   ```

4. **Import to Canvas**
   - Canvas → Grades → Import
   - Upload filtered CSV
   - Map columns if needed

---

## 🏷️ PR Labeling System

Labels trigger different grading workflows:

| **Label**      | **Purpose**                 | **Grading Weight**      |
| -------------- | --------------------------- | ----------------------- |
| `homework`     | Regular homework assignment | Standard (see rubric)   |
| `exam`         | Exam submission             | Exam-specific rubric    |
| `project`      | Team project milestone      | Project-specific rubric |
| `extra-credit` | Optional extra work         | Bonus points            |
| `resubmission` | Second attempt after fixes  | May have deduction      |

**To label a PR**:

1. Go to the student's PR
2. Right sidebar → Labels
3. Select appropriate label
4. Automated grading triggers

---

## 📊 Understanding Automated Grades

### Grading Breakdown (Default)

```
FINAL GRADE = (Tests × 40%) + (Coverage × 30%) + (Quality × 20%) + (Structure × 10%)
```

#### Tests (40%)

- Percentage of passing tests
- Both Python and JavaScript combined
- Formula: `(passed_tests / total_tests) × 100`

#### Coverage (30%)

- Code coverage percentage
- Minimum recommended: 80%
- Directly from coverage report

#### Code Quality (20%)

- Pylint score for Python
- ESLint error count for JavaScript
- Deductions for style violations

#### Structure (10%)

- README.md present (+3)
- Test files present (+4)
- Proper directory structure (+3)

### Example Calculation

```
Student: John Doe
Assignment: Homework 4

Tests: 18/20 passed = 90/100
Coverage: 85%
Code Quality: 95/100 (few linting issues)
Structure: 10/10 (all files present)

Final Grade:
= (90 × 0.40) + (85 × 0.30) + (95 × 0.20) + (100 × 0.10)
= 36 + 25.5 + 19 + 10
= 90.5/100
```

---

## 🎯 Customizing Grading Rubrics

### Per-Assignment Weights

Edit `.github/workflows/grading-automation.yml`:

```yaml
# For homework
TESTS_WEIGHT=40
COVERAGE_WEIGHT=30
CODE_QUALITY_WEIGHT=20
STRUCTURE_WEIGHT=10

# For exams (emphasize tests)
TESTS_WEIGHT=60
COVERAGE_WEIGHT=20
CODE_QUALITY_WEIGHT=10
STRUCTURE_WEIGHT=10

# For project (emphasize quality)
TESTS_WEIGHT=30
COVERAGE_WEIGHT=25
CODE_QUALITY_WEIGHT=25
STRUCTURE_WEIGHT=20
```

### Assignment-Specific Grading

Create separate workflow files:

```yaml
# .github/workflows/grade-homework.yml
# .github/workflows/grade-exam.yml
# .github/workflows/grade-project.yml
```

Or use conditionals:

```yaml
- name: Set grading weights
  run: |
    if [[ "${{ github.event.pull_request.labels.*.name }}" == *"exam"* ]]; then
      echo "TESTS_WEIGHT=60" >> $GITHUB_ENV
      echo "COVERAGE_WEIGHT=20" >> $GITHUB_ENV
    else
      echo "TESTS_WEIGHT=40" >> $GITHUB_ENV
      echo "COVERAGE_WEIGHT=30" >> $GITHUB_ENV
    fi
```

---

## 📝 Student Instructions for Canvas

Add this to your Canvas course or send as announcement:

### For Students: How to Submit Assignments

**Step 1: Complete Your Work in GitHub**

```bash
# Create your branch
git checkout -b feat/homework-4-yourname

# Do your work, commit changes
git add .
git commit -m "feat(homework-4): complete black box testing exercises"

# Push to GitHub
git push origin feat/homework-4-yourname
```

**Step 2: Create Pull Request**

1. Go to GitHub repository
2. Click "Pull requests" → "New pull request"
3. Select your branch
4. Fill out the PR template
5. Create pull request

**Step 3: Wait for Automated Checks**

- GitHub Actions will run automatically (~2-5 minutes)
- Wait for all checks to complete
- Look for ✅ green checkmarks or ❌ red X's
- Click "Details" on any failed checks to see what needs fixing

**Step 4: Review Your Automated Grade**

- Scroll down in your PR
- Find the "Automated Grading Report" comment
- Review your score breakdown
- Fix issues if needed and push again (checks re-run automatically)

**Step 5: Submit PR Link to Canvas**

1. Copy your PR URL (e.g., `https://github.com/yourname/software-testing-fall-2026/pull/42`)
2. Go to Canvas assignment
3. Click "Submit Assignment"
4. Paste the PR link
5. Click "Submit"

**Important Notes**:

- ✅ All automated checks must pass before final submission
- ✅ Your automated grade is visible in the PR
- ✅ Instructor may add manual feedback after automated grading
- ❌ Do not submit until checks are green
- ❌ Do not submit repository link - submit the specific PR link

---

## 🔧 Manual Grade Adjustments

Sometimes you need to adjust grades manually:

### In GitHub PR

```markdown
## Manual Grade Adjustment

**Original Automated Grade**: 85/100
**Adjusted Grade**: 90/100

**Reason**: Excellent documentation and edge case handling not captured by automated tests

**Breakdown**:

- Tests: 40/40 (no change)
- Coverage: 25/30 (no change)
- Quality: 20/20 (+5 bonus for exceptional quality)
- Structure: 10/10 (no change)
```

### In Canvas

1. Go to Canvas Gradebook
2. Find the student and assignment
3. Click on the grade
4. Override with manual grade
5. Add comment with reasoning

---

## 📊 Viewing All Grades

### Option 1: GitHub Actions Dashboard

1. Actions tab → "Automated Grading"
2. View all completed runs
3. See grades at a glance
4. Download artifacts as needed

### Option 2: Master Gradebook (CSV)

```bash
# View all grades
cat .gradebook/master-gradebook.csv

# Filter by assignment
grep "homework-4" .gradebook/master-gradebook.csv

# Filter by student
grep "john_doe" .gradebook/master-gradebook.csv

# Export to Excel-friendly format
cat .gradebook/master-gradebook.csv | column -t -s,
```

### Option 3: GitHub Insights

- Go to repository Insights → Community
- See PR activity
- Track submission rates

---

## 🚨 Troubleshooting

### Student Submitted Wrong Link

**Problem**: Student submitted repository link instead of PR link

**Solution**:

1. Ask student to find their PR number
2. Construct correct URL: `https://github.com/[user]/[repo]/pull/[number]`
3. Update Canvas submission

### Automated Grading Failed

**Problem**: Workflow errors, doesn't complete

**Solution**:

1. Check Actions tab for error details
2. Common issues:
   - Missing dependencies
   - Syntax errors in code
   - Timeout (tests take too long)
3. Run workflow manually: Actions → Workflow → "Run workflow"

### Grade Not in Canvas

**Problem**: Can't find grade to import

**Solution**:

1. Verify PR has required label (`homework`, `exam`, or `project`)
2. Check if grading workflow completed successfully
3. Download artifact from Actions tab
4. Manually import CSV if auto-update failed

### Student Disputes Grade

**Problem**: Student thinks grade is incorrect

**Solution**:

1. Review PR and grading report together
2. Show exact test results and coverage
3. Explain rubric weights
4. Adjust manually if justified
5. Document decision in PR comments

---

## 🎓 Advanced: Canvas API Integration

For automatic grade sync (optional):

### Setup

1. **Get Canvas API Token**

   - Canvas → Account → Settings
   - "+ New Access Token"
   - Copy token securely

2. **Add Token to GitHub Secrets**

   - Repository Settings → Secrets and variables → Actions
   - New repository secret
   - Name: `CANVAS_API_TOKEN`
   - Value: Your token

3. **Configure Workflow**

Add to `.github/workflows/grading-automation.yml`:

```yaml
- name: Sync grade to Canvas
  if: github.event.pull_request.merged == true
  env:
    CANVAS_TOKEN: ${{ secrets.CANVAS_API_TOKEN }}
    CANVAS_URL: https://your-school.instructure.com
  run: |
    # Canvas API call to post grade
    COURSE_ID="12345"  # Your Canvas course ID
    ASSIGNMENT_ID="67890"  # Canvas assignment ID
    STUDENT_ID="11111"  # Student Canvas ID
    GRADE="${{ steps.calculate-grade.outputs.grade }}"

    curl -X PUT \
      "$CANVAS_URL/api/v1/courses/$COURSE_ID/assignments/$ASSIGNMENT_ID/submissions/$STUDENT_ID" \
      -H "Authorization: Bearer $CANVAS_TOKEN" \
      -F "submission[posted_grade]=$GRADE" \
      -F "comment[text_comment]=Automated grade from GitHub PR #${{ github.event.pull_request.number }}"
```

**Note**: This requires mapping GitHub usernames to Canvas student IDs.

---

## 📚 Best Practices

### For Instructors

1. **Review First Week Carefully**

   - Watch for submission issues
   - Verify students understand the process
   - Adjust if needed

2. **Spot Check Automated Grades**

   - Randomly review a few each week
   - Ensure rubric is fair
   - Adjust weights if necessary

3. **Provide Manual Feedback**

   - Automated grades are quantitative
   - Add qualitative comments
   - Highlight good practices

4. **Keep Gradebook Synced**

   - Import grades weekly
   - Don't wait until end of semester
   - Students can track progress

5. **Communicate Clearly**
   - Explain grading process in syllabus
   - Show example submissions
   - Address concerns promptly

### For Students

1. **Test Locally First** - Don't rely only on GitHub Actions
2. **Submit Early** - Don't wait until deadline
3. **Check Automated Grade** - Review before Canvas submission
4. **Ask Questions** - If grade seems wrong, ask instructor
5. **Keep PRs Clean** - One PR per assignment

---

## ✅ Quick Reference

### For Each Assignment

- [ ] Create assignment in Canvas (100 points, URL submission)
- [ ] Announce assignment and GitHub requirements
- [ ] Students submit PR links in Canvas
- [ ] Review automated grades in PRs
- [ ] Download grade CSV from Actions
- [ ] Import grades to Canvas
- [ ] Provide manual feedback as needed
- [ ] Mark assignment complete in Canvas

### Grading Workflow Commands

```bash
# View all grading runs
gh run list --workflow=grading-automation.yml

# Download grade for specific PR
gh run download [run-id] --name canvas-import-pr-42

# View master gradebook
cat .gradebook/master-gradebook.csv

# Export grades for specific assignment
grep "homework-4" .gradebook/master-gradebook.csv > hw4-export.csv
```

---

**Questions?** Contact [your email] or open an issue in the repository!
