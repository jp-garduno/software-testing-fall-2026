# Exams Overview

This course includes **three practical exams** throughout the semester. All exams are hands-on practical exercises, not multiple-choice or theoretical questions.

## 📅 Exam Schedule

| **Exam**   | **Week** | **Session** | **Coverage**    | **Duration** | **Submission**   | **Weight** |
| ---------- | -------- | ----------- | --------------- | ------------ | ---------------- | ---------- |
| **Exam 1** | Week 6   | Session 2   | Modules 1, 3, 4 | 90 minutes   | ZIP file, Canvas | 15%        |
| **Exam 2** | Week 11  | Session 2   | Modules 4-6     | 90 minutes   | GitHub repo URL  | 15%        |
| **Exam 3** | Week 16  | Session 2   | Modules 7-9     | 90 minutes   | GitHub repo URL  | 15%        |

All three exams are **90 minutes**, taken inside a 2-hour class session. The extra time is deliberate slack, not exam time.

**Total Exam Weight**: 45% of final grade

> Each exam's full statement, exercises and rubric are published in the corresponding **Canvas assignment**, not in this repository. The details below are a preview so you know what to prepare for.

---

## 🎯 Exam Format

### What to Expect

All exams follow a similar structure:

1. **Problem Description**: Real-world scenario or application
2. **Requirements**: What you need to implement/test
3. **Deliverables**: Code, tests, documentation
4. **Evaluation Criteria**: How you'll be graded

### Exam Environment

- **In-person**: All exams are taken in the classroom
- **Open resources**: You may use:
  - Course materials
  - Official documentation
  - Your own notes
  - Internet for documentation lookup
  - GitHub Copilot (if configured)
- **No collaboration**: Individual work only
- **Your machine**: Use your own laptop with pre-configured environment

### What You Can Bring

✅ **Allowed**:

- Your laptop with development environment set up
- Course materials (digital or printed)
- Your own notes and code from exercises
- Access to official documentation websites

❌ **Not Allowed**:

- Communication with other students
- Using someone else's solutions
- Asking for help during the exam
- Sharing code or answers

---

## 📋 Exam Details

### Exam 1: Git, Static Testing & Black Box Testing

**Week 6, Session 2 — 90 minutes — 3 exercises, 100 points**

**Coverage**:

- Git: branching, merge conflicts, Conventional Commits (25%)
- Static testing: pre-commit and linter configuration, fixing findings (30%)
- Black box test design: EP, BVA, decision tables, state transition (45%)

**Sample Tasks**:

- Build a local repository, produce a merge conflict and resolve it
- Write commit messages with the correct Conventional Commits type
- Configure `.pre-commit-config.yaml` and a linter config
- Take a module from a failing lint score to a clean one, without silencing checks
- Design equivalence partitions, boundary values, a decision table and state transition test cases from a written specification

**Note**: in Exam 1 you **design and document** tests; you do not write automated tests. Choose Python **or** JavaScript and use it throughout. You deliver a ZIP file on Canvas, not a repository URL.

---

### Exam 2: Black Box, White Box & TDD

**Week 11, Session 2**

**Coverage**:

- Black box test design (30%)
- White box testing with coverage (40%)
- TDD implementation (30%)

**Sample Tasks**:

- Design test cases using black box techniques
- Write unit tests achieving high coverage
- Implement feature using TDD
- Analyze and improve code coverage

---

### Exam 3: Data-Driven, System & Performance Testing

**Week 16, Session 2**

**Coverage**:

- System-level testing (BDD, Selenium/Playwright) (50%)
- Performance testing with JMeter (25%)
- Integration challenge (25%)

**Sample Tasks**:

- Write E2E tests for web application
- Create BDD scenarios
- Design performance test plan
- Execute and analyze load tests

---

## 🎓 Preparation Tips

### Before the Exam

1. **Review all module materials** - Theory and exercises
2. **Practice exercises** - Complete all practice problems
3. **Set up your environment** - Ensure all tools work
4. **Review homework solutions** - Understand your mistakes
5. **Create a cheat sheet** - Quick reference for commands/syntax
6. **Sleep well** - Be rested and alert

### During the Exam

1. **Read everything first** - Understand all requirements before coding
2. **Start with what you know** - Don't get stuck on one problem
3. **Manage your time** - follow the time budget in the exam statement; it is shorter than you think
4. **Test your code** - Make sure it runs before submitting
5. **Comment your code** - Explain your thinking
6. **Submit early** - Don't wait until the last second

### Common Mistakes to Avoid

- ❌ Not reading instructions carefully
- ❌ Spending too much time on one problem
- ❌ Not testing your code before submission
- ❌ Forgetting to commit and push your work, or zipping the wrong folder
- ❌ Not including required files or documentation
- ❌ Leaving code in broken state

---

## 📤 Submission Requirements

Submission differs by exam. The exact file names, folder structure and checklist are in the Canvas assignment — follow that, not a generic rule.

### Exam 1 — ZIP file on Canvas

- One folder named after you, containing one subfolder per exercise
- Zipped and uploaded to the Canvas assignment; **no repository URL**
- The Git exercise requires the hidden `.git/` folder to be inside the ZIP
- Evidence files (linter and Git output) included as specified in the statement

### Exams 2 and 3 — GitHub repository URL

1. **GitHub Repository**:

   - Create a repository for the exam
   - Commit your work regularly
   - Push final version before deadline
   - Include proper README

2. **Code**:

   - All code should run without errors
   - Include all dependencies (requirements.txt, package.json)
   - Proper project structure

3. **Documentation**:

   - README with setup instructions
   - Comments in code where necessary
   - Test execution results

4. **Submission**:
   - Submit repository URL on Canvas
   - Ensure repository is accessible
   - Submit before deadline (no late submissions)

---

## 🎯 Grading Criteria

**The authoritative rubric is the one published with each exam in Canvas**, broken down per exercise. Exam 1, for example, is graded with a per-criterion rubric inside each of its three exercises, and it does not use the breakdown below — it has no code to run and no automated tests to write.

The following is the default breakdown for exams whose deliverable is a working, tested codebase (Exams 2 and 3):

### Functionality (40%)

- Code works as specified
- All requirements met
- No critical bugs

### Testing Quality (30%)

- Tests are comprehensive
- Good coverage
- Tests actually validate functionality

### Code Quality (20%)

- Clean, readable code
- Proper structure and organization
- Follows best practices
- Good naming conventions

### Documentation (10%)

- Clear README
- Proper comments
- Test documentation
- Setup instructions

---

## 🔧 Technical Setup Checklist

Before each exam, ensure you have:

### For All Exams

- [ ] Git installed and configured
- [ ] GitHub account set up (Exams 2 and 3)
- [ ] Code editor (VS Code recommended)
- [ ] Internet connection

### For Exam 1

- [ ] Pylint (Python) or ESLint (JavaScript) installed and runnable from the command line
- [ ] A tool that can create a ZIP **including hidden folders** like `.git/`
- [ ] Practice resolving a merge conflict from the command line

You do **not** need to install or run pre-commit for Exam 1: the configuration file is graded by inspection.

### For Exam 2

- [ ] pytest and Jest installed
- [ ] Coverage tools configured
- [ ] Familiar with TDD workflow

### For Exam 3

- [ ] Selenium or Playwright set up
- [ ] JMeter installed
- [ ] Behave (Python) or Cucumber (JS) configured
- [ ] WebDriver downloaded

---

## ❓ Frequently Asked Questions

**Q: Can I use Google during the exam?**
A: Yes, for looking up documentation and syntax. No copying solutions.

**Q: What if my code doesn't work perfectly?**
A: Partial credit is given. Show your work and reasoning.

**Q: Can I ask questions during the exam?**
A: Only clarifying questions about requirements. No technical help.

**Q: What if I finish early?**
A: Review your work, improve code quality, add comments, enhance tests.

**Q: What happens if I miss an exam?**
A: Make-up exams only for documented emergencies. Contact instructor ASAP.

**Q: Can I use old homework code?**
A: Yes, if it's your own work and helps solve the exam problems.

**Q: How much is each question worth?**
A: Point distribution is specified in each exam. Budget time accordingly.

---

## 📚 Additional Resources

Exam specifications and practice materials will be provided closer to exam dates.

---

**Good luck on your exams!** Remember: these are practical assessments of real-world skills. Focus on demonstrating what you've learned. 🎯
