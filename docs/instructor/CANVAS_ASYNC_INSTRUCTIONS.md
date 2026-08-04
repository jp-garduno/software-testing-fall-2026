# Canvas Instructions - Async Weeks 1-3

**Purpose**: Copy these instructions into Canvas for each session during the offline/async period.

---

## Week 1: Git Fundamentals

### 📅 Session 1: Git Basics (4 hours)

**Canvas Module Title**: Week 1 - Session 1: Git Basics

**Instructions to post in Canvas**:

---

#### Welcome to Week 1! 🎉

This week, you'll learn Git fundamentals - the foundation for modern software development and testing. Since we're working asynchronously, follow these steps carefully.

#### 📚 What You'll Learn
- Version control concepts
- Git installation and setup
- Basic Git commands
- Creating and managing repositories

#### 🎯 Step-by-Step Instructions

**Step 1: Access the Repository (5 minutes)**

1. Go to: `https://github.com/jp-garduno/software-testing-fall-2026`
2. Click the green "Code" button
3. Copy the repository URL
4. Clone to your computer:
   ```bash
   git clone https://github.com/jp-garduno/software-testing-fall-2026.git
   cd software-testing-fall-2026
   ```

**Step 2: Read Theory Documents (2 hours)**

📖 Read these files in the `01-git/theory/` folder **in order**:

1. **[01-version-control-intro.md](../../01-git/theory/01-version-control-intro.md)** (15 min)
   - What is version control?
   - Why do we need it?
   - Git vs other systems

2. **[02-git-setup.md](../../01-git/theory/02-git-setup.md)** (20 min)
   - Installing Git
   - Initial configuration
   - Setting up your identity

3. **[03-basic-commands.md](../../01-git/theory/03-basic-commands.md)** (30 min)
   - `git init`, `git clone`
   - `git status`, `git log`
   - Basic workflow

4. **[04-commits.md](../../01-git/theory/04-commits.md)** (30 min)
   - `git add`, `git commit`
   - Writing good commit messages
   - Viewing history

5. **[05-branching.md](../../01-git/theory/05-branching.md)** (25 min)
   - What are branches?
   - Creating and switching branches
   - Branch strategies

**Step 3: Complete Exercise 1 (1 hour)**

📝 Open and complete:
- **[01-git/exercises/01-first-repo.md](../../01-git/exercises/01-first-repo.md)**

This exercise walks you through:
- Creating your first Git repository
- Making commits
- Viewing history
- Understanding Git workflow

**Step 4: Setup Your Development Environment (1 hour)**

✅ Install required tools:
1. **Git** - Already done in Step 1
2. **VS Code** (or your preferred editor)
3. **Python 3.9+** - [Download here](https://www.python.org/downloads/)
4. **Node.js 18+** - [Download here](https://nodejs.org/)

Verify installations:
```bash
git --version
python --version
node --version
```

#### ✅ Self-Check

Before moving to Session 2, make sure you can:
- [ ] Clone a repository
- [ ] Make a commit
- [ ] View commit history
- [ ] Create a branch
- [ ] Understand the staging area

#### 📊 Time Breakdown
- Reading: 2 hours
- Exercise: 1 hour
- Setup: 1 hour
- **Total: ~4 hours**

#### 🆘 Need Help?
- Post questions in the **Discussion Board**
- Check the [Contributing Guide](../../CONTRIBUTING.md)
- Review [Git cheat sheet](../../resources/README.md#git-commands)

#### ➡️ Next Session
Session 2 covers merging, pull requests, and collaboration!

---

### 📅 Session 2: Collaboration & Workflows (3 hours)

**Canvas Module Title**: Week 1 - Session 2: Git Collaboration

**Instructions to post in Canvas**:

---

#### Continuing Week 1! 🚀

Now that you understand Git basics, let's learn how to collaborate with others and handle conflicts.

#### 📚 What You'll Learn
- Merging branches
- Handling conflicts
- Pull requests
- Git workflows
- Best practices

#### 🎯 Step-by-Step Instructions

**Step 1: Read Theory Documents (1.5 hours)**

📖 Read these files in the `01-git/theory/` folder:

6. **[06-merging.md](../../01-git/theory/06-merging.md)** (20 min)
   - Merge strategies
   - Fast-forward vs. three-way merge
   - When to merge

7. **[07-pull-requests.md](../../01-git/theory/07-pull-requests.md)** (20 min)
   - What is a pull request?
   - GitHub PR workflow
   - Code review process

8. **[08-conflicts.md](../../01-git/theory/08-conflicts.md)** (25 min)
   - Why conflicts happen
   - Resolving conflicts
   - Conflict markers

9. **[09-workflows.md](../../01-git/theory/09-workflows.md)** (15 min)
   - Feature branch workflow
   - Gitflow
   - Trunk-based development

10. **[10-best-practices.md](../../01-git/theory/10-best-practices.md)** (10 min)
    - Commit message guidelines
    - When to commit
    - Branch naming

**Step 2: Complete Exercises 2-4 (1.5 hours)**

📝 Complete these exercises **in order**:

1. **[02-branching.md](../../01-git/exercises/02-branching.md)** (30 min)
   - Practice creating branches
   - Switching between branches
   - Branch management

2. **[03-collaboration.md](../../01-git/exercises/03-collaboration.md)** (30 min)
   - Simulating team collaboration
   - Using remote repositories
   - Push and pull

3. **[04-conflicts.md](../../01-git/exercises/04-conflicts.md)** (30 min)
   - Creating conflicts intentionally
   - Resolving merge conflicts
   - Using conflict resolution tools

**Step 3: Review Homework 1 (Preview Only - Don't Start Yet)**

📋 Read through:
- **[01-git/homework/homework-1.md](../../01-git/homework/homework-1.md)**

This is due at the **end of Week 2**. Just familiarize yourself with the requirements.

#### ✅ Self-Check

Before moving to Week 2, make sure you can:
- [ ] Merge branches
- [ ] Resolve conflicts
- [ ] Create a pull request
- [ ] Understand different Git workflows
- [ ] Write good commit messages

#### 📊 Time Breakdown
- Reading: 1.5 hours
- Exercises: 1.5 hours
- **Total: ~3 hours**

#### 🎯 Action Items Before Week 2
- Complete exercises 1-4
- Start thinking about Homework 1
- Review Git cheat sheet

#### ➡️ Next Week
Week 2: Software Testing Concepts!

---

## Week 2: Software Testing Concepts

### 📅 Session 3: Introduction to Testing (4 hours)

**Canvas Module Title**: Week 2 - Session 3: Testing Fundamentals

**Instructions to post in Canvas**:

---

#### Welcome to Week 2! 🧪

This week focuses on software testing concepts - what testing is, why it matters, and the different types of testing.

#### 📚 What You'll Learn
- Introduction to software testing
- Testing types (functional vs. non-functional)
- Testing levels (unit, integration, system, acceptance)
- Real-world testing disasters

#### 🎯 Step-by-Step Instructions

**Step 1: Read Theory Documents (2 hours)**

📖 Read these files in the `02-testing-concepts/theory/` folder:

1. **[01-introduction.md](../../02-testing-concepts/theory/01-introduction.md)** (45 min)
   - What is software testing?
   - Testing vs. debugging
   - Real-world disasters (Ariane 5, Therac-25, Knight Capital)
   - The Rule of 10
   - Cost of fixing bugs

2. **[02-testing-types.md](../../02-testing-concepts/theory/02-testing-types.md)** (45 min)
   - Functional testing
   - Non-functional testing
   - Smoke, sanity, and regression testing
   - When to use each type

**Step 2: Take the Quiz (30 minutes)**

📝 Complete:
- **[02-testing-concepts/exercises/quiz.md](../../02-testing-concepts/exercises/quiz.md)**

This is a **self-assessment quiz** with 20 questions covering:
- Testing introduction (Q1-3)
- Testing types (Q4-7)
- Answers included at the bottom

**How to submit**: Take a screenshot of your score and post in the **Discussion Board** (optional - for self-assessment only)

**Step 3: Start Case Study 1 (1.5 hours)**

📊 Begin working on:
- **[02-testing-concepts/exercises/case-studies.md](../../02-testing-concepts/exercises/case-studies.md)**

**For this session, complete ONLY**:
- **Case Study 1: E-Commerce Platform (ShopFast)**

Answer all questions for this case study. You'll complete the other two in Session 4.

#### ✅ Self-Check

After this session, you should understand:
- [ ] The difference between testing and debugging
- [ ] Why testing is important (real-world examples)
- [ ] Functional vs. non-functional testing
- [ ] Different testing types (smoke, sanity, regression)
- [ ] The cost of late bug detection

#### 📊 Time Breakdown
- Reading: 2 hours
- Quiz: 30 minutes
- Case Study: 1.5 hours
- **Total: ~4 hours**

#### 💡 Key Takeaway
Testing is not optional - it saves time, money, and sometimes lives!

#### ➡️ Next Session
Session 4: Testing levels and principles

---

### 📅 Session 4: Testing Levels & Principles (4 hours)

**Canvas Module Title**: Week 2 - Session 4: Testing Pyramid & Principles

**Instructions to post in Canvas**:

---

#### Continuing Week 2! 📊

Learn about the testing pyramid and the seven fundamental testing principles that guide all testing activities.

#### 📚 What You'll Learn
- Testing levels (unit, integration, system, acceptance)
- The testing pyramid
- Seven ISTQB testing principles
- Applying testing concepts

#### 🎯 Step-by-Step Instructions

**Step 1: Read Theory Documents (1.5 hours)**

📖 Read these files in the `02-testing-concepts/theory/` folder:

3. **[03-testing-levels.md](../../02-testing-concepts/theory/03-testing-levels.md)** (45 min)
   - Unit testing
   - Integration testing
   - System testing
   - Acceptance testing
   - The testing pyramid
   - When to use each level

4. **[04-testing-principles.md](../../02-testing-concepts/theory/04-testing-principles.md)** (45 min)
   - Principle 1: Testing shows presence of defects
   - Principle 2: Exhaustive testing is impossible
   - Principle 3: Early testing
   - Principle 4: Defect clustering
   - Principle 5: Pesticide paradox
   - Principle 6: Testing is context dependent
   - Principle 7: Absence of errors fallacy

**Step 2: Review Concept Maps (30 minutes)**

📊 Study:
- **[02-testing-concepts/exercises/concept-maps.md](../../02-testing-concepts/exercises/concept-maps.md)**

Review all 7 concept maps:
1. Testing Overview
2. Testing Types Hierarchy
3. Testing Pyramid
4. Seven Principles
5. Testing in SDLC
6. Testing Workflow
7. Testing Metrics

**Optional**: Draw your own version to help memorize.

**Step 3: Complete Case Studies 2 & 3 (1.5 hours)**

📊 Continue with:
- **[02-testing-concepts/exercises/case-studies.md](../../02-testing-concepts/exercises/case-studies.md)**

Complete:
- **Case Study 2: Healthcare Management System (MedTrack)** (45 min)
- **Case Study 3: Mobile Gaming App (Puzzle Quest)** (45 min)

**Step 4: Compare & Reflect (30 minutes)**

Complete the comparison exercise at the bottom of the case studies file:
- Compare all three case studies
- Answer reflection questions

#### 🎯 Action Item: Start Homework 1

**⚠️ IMPORTANT**: Homework 1 is **DUE at the end of this week (Week 2)**

Begin working on:
- **[01-git/homework/homework-1.md](../../01-git/homework/homework-1.md)**

You should have already completed the exercises, so this homework should take 3-4 hours.

**Submission Process**:
1. Create a feature branch: `git checkout -b homework-1-yourname`
2. Complete the homework
3. Commit your changes
4. Push to GitHub
5. Create a Pull Request
6. Submit the PR link to Canvas

📖 Detailed submission instructions:
- **[docs/student/STUDENT_SUBMISSION_GUIDE.md](../../docs/student/STUDENT_SUBMISSION_GUIDE.md)**

#### ✅ Self-Check

After this session, you should understand:
- [ ] The testing pyramid (more unit tests, fewer E2E tests)
- [ ] All seven ISTQB testing principles
- [ ] When to apply each testing level
- [ ] How context affects testing strategy
- [ ] How to analyze testing needs for different applications

#### 📊 Time Breakdown
- Reading: 1.5 hours
- Concept maps: 30 minutes
- Case studies: 1.5 hours
- Comparison: 30 minutes
- **Total: ~4 hours**

#### 📝 Homework Due This Week
- **Homework 1 (Git)** - Due end of Week 2
- Start early! Don't wait until the last day.

#### ➡️ Next Week
Week 3: Static Testing (pre-commit hooks, linting)

---

## Week 3: Static Testing

### 📅 Session 5: Conventional Commits & Pre-commit (4 hours)

**Canvas Module Title**: Week 3 - Session 5: Static Testing Setup

**Instructions to post in Canvas**:

---

#### Welcome to Week 3! 🔍

This week covers **static testing** - catching bugs without running code! You'll learn about conventional commits, pre-commit hooks, and linting.

#### 📚 What You'll Learn
- Static vs. dynamic testing
- Conventional commits specification
- Pre-commit hooks
- Automating code quality checks

#### 🎯 Step-by-Step Instructions

**Step 1: Read Theory Documents (1.5 hours)**

📖 Read these files in the `03-static-testing/theory/` folder:

1. **[01-introduction.md](../../03-static-testing/theory/01-introduction.md)** (30 min)
   - Static vs. dynamic testing
   - Benefits of early defect detection
   - Cost comparison ($50 review vs. $5000+ production bug)
   - Types of static testing

2. **[02-conventional-commits.md](../../03-static-testing/theory/02-conventional-commits.md)** (30 min)
   - Commit message format: `type(scope): subject`
   - Types: feat, fix, docs, style, refactor, test, chore
   - Breaking changes
   - Real-world examples

3. **[03-pre-commit-hooks.md](../../03-static-testing/theory/03-pre-commit-hooks.md)** (30 min)
   - What are Git hooks?
   - Pre-commit framework
   - Configuration examples
   - Common hooks

**Step 2: Complete Exercise 1 (45 minutes)**

📝 Practice conventional commits:
- **[03-static-testing/exercises/01-conventional-commits-practice.md](../../03-static-testing/exercises/01-conventional-commits-practice.md)**

This exercise includes:
- Part 1: Fix bad commit messages
- Part 2: Write commit messages for scenarios
- Part 3: Add scopes
- Part 4: Write complete commit messages

**Step 3: Complete Exercise 2 (1.5 hours)**

🛠️ Hands-on pre-commit setup:
- **[03-static-testing/exercises/02-precommit-setup.md](../../03-static-testing/exercises/02-precommit-setup.md)**

This is a **practical exercise** where you'll:
1. Create a new project
2. Install pre-commit
3. Configure hooks
4. Test the setup
5. See hooks block bad commits

**Follow every step carefully!**

**Step 4: Review Homework 2 (15 minutes)**

📋 Read through:
- **[02-testing-concepts/homework/homework-2.md](../../02-testing-concepts/homework/homework-2.md)**

This is due at the **end of Week 3**. Just familiarize yourself with requirements.

#### ⚠️ IMPORTANT: Homework 1 Due Today!

If you haven't submitted Homework 1 yet, **submit it today**:
1. Create your Pull Request
2. Wait for automated grading (2-5 minutes)
3. Review your grade in PR comments
4. Submit PR link to Canvas

#### ✅ Self-Check

After this session, you should:
- [ ] Understand static vs. dynamic testing
- [ ] Know conventional commit format
- [ ] Have pre-commit installed and configured
- [ ] Understand how hooks prevent bad commits
- [ ] Be able to write proper commit messages

#### 📊 Time Breakdown
- Reading: 1.5 hours
- Exercise 1: 45 minutes
- Exercise 2: 1.5 hours
- Homework review: 15 minutes
- **Total: ~4 hours**

#### 💡 Pro Tip
From now on, use conventional commits in all your work!

#### ➡️ Next Session
Session 6: Linting with Pylint and ESLint

---

### 📅 Session 6: Linting & Code Quality (4 hours)

**Canvas Module Title**: Week 3 - Session 6: Linting Tools

**Instructions to post in Canvas**:

---

#### Final Session of Async Weeks! 🎉

Learn about linting tools that automatically check your code quality and style.

#### 📚 What You'll Learn
- What is linting?
- Pylint for Python
- ESLint for JavaScript
- Code formatters (Black, Prettier)
- Fixing linting issues

#### 🎯 Step-by-Step Instructions

**Step 1: Read Theory Document (45 minutes)**

📖 Read:
- **[03-static-testing/theory/04-linting.md](../../03-static-testing/theory/04-linting.md)**

Covers:
- Purpose of linting
- Pylint configuration and usage
- ESLint configuration and usage
- Black and Prettier formatters
- Integrating with your editor

**Step 2: Complete Exercise 3 (1.5 hours)**

⚙️ Configure linters:
- **[03-static-testing/exercises/03-linting-config.md](../../03-static-testing/exercises/03-linting-config.md)**

You'll configure:
- Pylint for Python (create `.pylintrc`)
- ESLint for JavaScript
- Black formatter
- Prettier formatter

**This is hands-on - follow all steps!**

**Step 3: Complete Exercise 4 (1.5 hours)**

🔧 Fix real linting issues:
- **[03-static-testing/exercises/04-fix-issues.md](../../03-static-testing/exercises/04-fix-issues.md)**

This exercise includes:
- Python code with linting issues
- JavaScript code with linting issues
- Step-by-step fixing guide
- Auto-fix vs. manual fixes

**Step 4: Review Homework 3 (30 minutes)**

📋 Carefully read:
- **[03-static-testing/homework/homework-3.md](../../03-static-testing/homework/homework-3.md)**

This is due at the **end of Week 4** (first week of in-person classes).

**Homework 3 Requirements**:
- Set up complete static testing infrastructure
- Configure pre-commit hooks
- Configure linters
- Fix at least 5 issues
- Write an analysis report

**Time estimate**: 3-4 hours

#### 🎯 Action Items for This Week

**1. Submit Homework 2 (Testing Concepts)**

Due **end of Week 3**:
- Complete all parts of Homework 2
- Create Pull Request
- Submit PR link to Canvas

**2. Start Homework 3 (Static Testing)**

Due **end of Week 4**:
- You can start early!
- All concepts covered in Week 3

#### ✅ Self-Check

After this session, you should:
- [ ] Understand what linting is and why it matters
- [ ] Have Pylint configured for Python
- [ ] Have ESLint configured for JavaScript
- [ ] Know how to use Black and Prettier
- [ ] Be able to fix common linting issues
- [ ] Have a complete static testing setup

#### 📊 Time Breakdown
- Reading: 45 minutes
- Exercise 3: 1.5 hours
- Exercise 4: 1.5 hours
- Homework review: 30 minutes
- **Total: ~4 hours**

#### 🎉 Async Weeks Complete!

**You've covered**:
- ✅ Module 1: Git Fundamentals
- ✅ Module 2: Software Testing Concepts
- ✅ Module 3: Static Testing

**Get ready for in-person classes starting Week 4!**

#### 📝 Homework Status Check

Before Week 4:
- [ ] Homework 1 (Git) - Should be submitted
- [ ] Homework 2 (Testing Concepts) - Due end of Week 3
- [ ] Homework 3 (Static Testing) - Due end of Week 4 (can start now)

#### ➡️ Next Week
**Week 4: In-Person Classes Begin!**
- Black Box Testing
- Equivalence Partitioning
- Test Case Design

---

## 📊 Summary Table for Students

| Week | Session | Topic | Key Files | Time | Homework Due |
|------|---------|-------|-----------|------|--------------|
| 1 | 1 | Git Basics | 01-git/theory (1-5), exercise 01 | 4h | - |
| 1 | 2 | Git Collaboration | 01-git/theory (6-10), exercises 02-04 | 3h | - |
| 2 | 3 | Testing Intro | 02-testing-concepts/theory (1-2), quiz, case study 1 | 4h | - |
| 2 | 4 | Testing Levels | 02-testing-concepts/theory (3-4), case studies 2-3 | 4h | **HW1** |
| 3 | 5 | Static Testing | 03-static-testing/theory (1-3), exercises 01-02 | 4h | - |
| 3 | 6 | Linting | 03-static-testing/theory (4), exercises 03-04 | 4h | **HW2** |

**Total Async Learning Time**: ~23 hours over 3 weeks

---

## 📋 Quick Links for Students

### Essential Documents
- **[Student Submission Guide](../student/STUDENT_SUBMISSION_GUIDE.md)** - How to submit homework
- **[Course Timeline](../../TIMELINE.md)** - Full 16-week schedule
- **[Resources](../../resources/README.md)** - Books, videos, cheat sheets

### Module Overviews
- **[Module 1: Git](../../01-git/README.md)**
- **[Module 2: Testing Concepts](../../02-testing-concepts/README.md)**
- **[Module 3: Static Testing](../../03-static-testing/README.md)**

### Getting Help
- Use the Canvas **Discussion Board**
- Post questions early - others probably have the same question!
- Check resources folder for cheat sheets

---

**End of Async Instructions**
