# Homework 1: Git Workflow Practice

**Module**: 1 - Git Fundamentals  
**Due Date**: End of Week 2  
**Points**: 100  
**Estimated Time**: 3-4 hours

---

## 🎯 Objectives

This homework will help you:

- Practice the complete Git workflow
- Understand branching and merging strategies
- Write meaningful commit messages
- Collaborate using pull requests
- Build a portfolio project

---

## 📋 Assignment Overview

You will create a personal portfolio website (or any simple project of your choice) and manage its development using Git and GitHub. The focus is on demonstrating proper Git workflow, not on the complexity of the project itself.

---

## 📝 Requirements

### Part 1: Repository Setup (15 points)

**You have two options for practicing:**

**Option A: Practice in a separate repository** (recommended for learning)

1. **Create a new GitHub repository** named `git-workflow-practice` or similar
   - Initialize with a README
   - Add a `.gitignore` file appropriate for your project
   - Add a license (MIT recommended)
2. Complete all parts of the assignment in this repository
3. Document your work with screenshots/links for your final submission

**Option B: Work directly in the course repository**

1. **Clone the course repository** if you haven't already
2. **Create your branch** from `main`:
   ```bash
   git checkout -b feat/<your-username>/homework-1
   ```
3. **Create your directory**: `students/<your-username>/homework-1/`
4. Complete all work in this directory

**Regardless of which option you choose**, you must configure Git locally:

```bash
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

**Important**: Whether you use Option A or B, you must submit your final deliverables in the course repository under `students/<your-username>/homework-1/` for automated grading.

### Part 2: Branching Strategy (25 points)

Create and work on **at least 3 feature branches**:

1. **Branch naming convention**: Use descriptive names

   - ✅ Good: `feature/add-navigation`, `feature/create-about-page`, `fix/typo-in-readme`
   - ❌ Bad: `branch1`, `test`, `my-branch`

2. **Required branches** (examples for a portfolio website):

   - `feature/initial-structure` - Create basic HTML/file structure
   - `feature/add-styling` - Add CSS or styling
   - `feature/add-content` - Add actual content (text, images, etc.)
   - (Optional) Additional branches for extra features

3. **Branch workflow**:
   - Create each branch from `main`
   - Make commits on the feature branch
   - Create a pull request to merge back to `main`
   - Merge the pull request on GitHub

**Note**: You can practice this workflow in a separate repository. Document your branch strategy and include screenshots/links in your REFLECTION.md for grading.

### Part 3: Commit History (30 points)

Make **at least 10 meaningful commits** across your branches:

1. **Commit message format**:

   ```
   <type>: <short description>

   [optional longer description]
   ```

2. **Commit types**:

   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `style:` - Formatting, no code change
   - `refactor:` - Code restructuring

3. **Examples**:

   ```
   feat: add navigation menu to header

   - Created nav element with links
   - Added basic styling for mobile responsiveness

   fix: correct typo in about page title

   docs: update README with project description

   style: format CSS with consistent indentation
   ```

4. **Requirements**:
   - Each commit should represent a logical unit of work
   - Commit messages must be clear and descriptive
   - Avoid commits like "update", "fix", "changes"

### Part 4: Pull Requests (20 points)

Create **at least 2 pull requests**:

1. **For each PR**:

   - Write a descriptive title
   - Add a description explaining what changes were made
   - Include why the changes were needed
   - (Optional) Add screenshots if relevant

2. **PR Description Template**:

   ```markdown
   ## Description

   Brief description of changes

   ## Changes Made

   - Change 1
   - Change 2

   ## Testing

   How you tested these changes

   ## Screenshots (if applicable)

   [Add images here]
   ```

3. **Merge your PRs** - Use the "Squash and merge" or "Merge commit" option

**Note**: You can create these PRs in a practice repository. Document them with screenshots/links in your REFLECTION.md. Your final submission PR in the course repository will also be evaluated.

### Part 5: Documentation (10 points)

Update your **README.md** to include:

1. **Project Title and Description**
2. **Technologies Used**
3. **Git Workflow Documentation**:
   - Explain your branching strategy
   - List the branches you created
   - Describe your commit message convention
4. **Setup Instructions** (how to clone and run)
5. **(Optional)** Lessons learned about Git

---

## 📤 Submission

### Option 1: Practice Repository (Recommended for Learning)

You can practice Git workflow in a separate repository (e.g., `git-workflow-practice`) to fully experience creating a repository from scratch, managing branches, and creating pull requests independently.

### Option 2: Submit for Automated Grading (Required for Credit)

**To receive automated grading and credit**, you must submit your work in this course repository:

1. **Create your submission directory**:

   ```bash
   students/<your-github-username>/homework-1/
   ```

2. **Copy your final project files** to this directory:

   - All source files (HTML, CSS, JavaScript, or other project files)
   - `.gitignore`
   - `README.md` with complete documentation
   - `REFLECTION.md` with your reflection (200-300 words)

3. **Create a Pull Request** in this repository:

   - Branch name: `feat/<your-username>/homework-1`
   - Title: `Homework 1: Git Workflow Practice - <Your Name>`
   - Base branch: `main`
   - Add the `homework` label to your PR
   - Fill out the PR description using the template

4. **REFLECTION.md should include**:
   - What challenges did you face?
   - What Git commands did you find most useful?
   - How will you apply this workflow in the team project?
   - Documentation of your commit history and branching strategy (can link to practice repo if you used one)

**Important**: The automated grading system only works for pull requests in the course repository (`software-testing-fall-2026`). If you practiced in a separate repository, make sure to create a PR in this repository with your final deliverables for grading.

---

## 🎯 Grading Rubric

| **Category**           | **Points** | **Criteria**                                                |
| ---------------------- | ---------- | ----------------------------------------------------------- |
| **Repository Setup**   | 15         | Repository properly initialized, configured, and organized  |
| **Branching Strategy** | 25         | At least 3 feature branches with proper naming and workflow |
| **Commit History**     | 30         | At least 10 commits with clear, meaningful messages         |
| **Pull Requests**      | 20         | At least 2 PRs with good descriptions and proper merges     |
| **Documentation**      | 10         | Complete README with workflow documentation                 |
| **Total**              | **100**    |                                                             |

### Bonus Points (up to +10)

- Resolve a merge conflict intentionally and document it (+5)
- Use Git tags for releases (+3)
- Add a CONTRIBUTING.md file explaining your workflow (+2)

---

## 💡 Tips for Success

1. **Start early** - Don't wait until the last day
2. **Commit often** - Small, frequent commits are better than large ones
3. **Test your workflow** - Make sure all branches merge cleanly
4. **Read your messages** - Before committing, review your commit message
5. **Use GitHub's features** - Explore issues, projects, and wikis
6. **Don't be afraid to experiment** - You can always create a new branch

---

## ⚠️ Common Mistakes to Avoid

- ❌ Committing directly to `main` without branches
- ❌ Using vague commit messages like "update" or "fix"
- ❌ Making one huge commit with many unrelated changes
- ❌ Not testing if branches merge cleanly
- ❌ Leaving empty or default PR descriptions
- ❌ Not updating the README

---

## 🆘 Getting Help

If you're stuck:

1. Review the [Module 1 theory materials](../theory/)
2. Check the [interactive exercises](../exercises/)
3. Ask questions in the course discussion forum
4. Attend office hours
5. Consult the [Git documentation](https://git-scm.com/doc)

---

## 📚 Resources

- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [GitHub Guides](https://guides.github.com/)
- [Writing Good Commit Messages](https://chris.beams.io/posts/git-commit/)
- [Pull Request Best Practices](https://github.blog/2015-01-21-how-to-write-the-perfect-pull-request/)

---

## ✅ Submission Checklist

Before submitting, verify:

- [ ] All required files are in `students/<your-username>/homework-1/`
- [ ] At least 3 feature branches created and merged (documented in REFLECTION.md)
- [ ] At least 10 commits with meaningful messages (documented in REFLECTION.md)
- [ ] At least 2 pull requests created (in practice repo or documented in REFLECTION.md)
- [ ] README.md is complete and well-formatted
- [ ] REFLECTION.md is written (200-300 words)
- [ ] Created a pull request in the course repository
- [ ] Added the `homework` label to your PR
- [ ] All files are committed and pushed to your branch

---

**Good luck!** Remember, the goal is to practice the Git workflow, not to create a perfect project. Focus on demonstrating your understanding of version control. 🚀
