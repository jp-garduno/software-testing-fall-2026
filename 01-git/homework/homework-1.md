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

1. **Create a new GitHub repository** named `git-workflow-practice` or similar
   - Initialize with a README
   - Add a `.gitignore` file appropriate for your project
   - Add a license (MIT recommended)

2. **Clone the repository** to your local machine

3. **Configure Git locally**
   ```bash
   git config user.name "Your Name"
   git config user.email "your.email@example.com"
   ```

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

Submit the following on the course LMS:

1. **GitHub Repository URL**: Link to your public repository
2. **Reflection Document** (PDF or Markdown):
   - What challenges did you face?
   - What Git commands did you find most useful?
   - How will you apply this workflow in the team project?
   - (200-300 words)

---

## 🎯 Grading Rubric

| **Category** | **Points** | **Criteria** |
|--------------|------------|--------------|
| **Repository Setup** | 15 | Repository properly initialized, configured, and organized |
| **Branching Strategy** | 25 | At least 3 feature branches with proper naming and workflow |
| **Commit History** | 30 | At least 10 commits with clear, meaningful messages |
| **Pull Requests** | 20 | At least 2 PRs with good descriptions and proper merges |
| **Documentation** | 10 | Complete README with workflow documentation |
| **Total** | **100** | |

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
- [ ] Repository is public and accessible
- [ ] At least 3 feature branches created and merged
- [ ] At least 10 commits with meaningful messages
- [ ] At least 2 pull requests created and merged
- [ ] README is complete and well-formatted
- [ ] Reflection document is written
- [ ] Repository URL submitted on LMS
- [ ] All files are committed and pushed

---

**Good luck!** Remember, the goal is to practice the Git workflow, not to create a perfect project. Focus on demonstrating your understanding of version control. 🚀
