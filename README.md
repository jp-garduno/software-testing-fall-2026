# Software Testing Course - Fall 2026

Welcome to the Software Testing course! This repository contains all materials, exercises, and resources for the Fall 2026 semester.

## 📚 Course Information

- **Duration**: 16 weeks (2 days/week, 2 hours/session)
- **Format**:
  - Weeks 1-3: Offline/Async
  - Weeks 4-16: In-person at University
- **Languages**: Python and JavaScript/TypeScript
- **Tools**: Students have access to GitHub Copilot

## 🎯 Learning Objectives

By the end of this course, you will be able to:

- Apply professional testing methodologies to real-world software projects
- Write effective unit, integration, and system tests
- Use industry-standard testing tools and frameworks
- Implement test-driven development practices
- Design comprehensive test strategies
- Collaborate on testing projects using Git and modern workflows

## 📖 Course Modules

1. **[Git Fundamentals](./01-git/)** - Version control and collaboration
2. **[Software Testing Concepts](./02-testing-concepts/)** - Introduction, types, levels, and principles
3. **[Static Testing](./03-static-testing/)** - Conventional commits, pre-commit hooks, and linting
4. **[Black Box Testing](./04-black-box-testing/)** - Test case design, equivalence partitioning, boundary value analysis, decision tables, state transition
5. **[White Box Testing](./05-white-box-testing/)** - Statement/branch/path coverage, code coverage tools, mocking
6. **[Test Driven Development](./06-test-driven-development/)** - TDD principles and practices
7. **[Data Driven Testing](./07-data-driven-testing/)** - Parameterized tests and data management
8. **[System Level Testing](./08-system-level-testing/)** - BDD, Selenium, and Playwright
9. **[Performance Testing](./09-performance-testing/)** - Load testing with JMeter

## 📝 Assessments

### Submission Process

All assignments are submitted via **GitHub Pull Requests** and tracked in **Canvas**:

1. Complete your work in a feature branch
2. Create a Pull Request
3. Automated grading runs via GitHub Actions (2-5 minutes)
4. Review your grade in the PR comments
5. Submit the PR link to Canvas

**📖 Guides**:

- **[Student Submission Guide](./docs/student/STUDENT_SUBMISSION_GUIDE.md)** - Complete walkthrough for students
- **[Canvas Integration Guide](./docs/instructor/CANVAS_INTEGRATION.md)** - For instructors using Canvas

### Homework Assignments

Each module includes a homework assignment to reinforce learning. See individual module folders for details.

- **Grading**: Automated via GitHub Actions (Tests 40%, Coverage 30%, Quality 20%, Structure 10%)
- **Submission**: GitHub PR link to Canvas
- **Turnaround**: Instant automated feedback, manual review within 48 hours

### Exams

- **[Exam 1](./exams/exam-1/)** - Week 6: Git, Testing Concepts, Static Testing
- **[Exam 2](./exams/exam-2/)** - Week 11: Black Box and White Box Testing, TDD
- **[Exam 3](./exams/exam-3/)** - Week 16: System Testing, Performance Testing

All exams are **practical** - you'll write code and tests to solve real problems. Same submission process as homework.

### Team Project

Work in teams of 4-5 students to build a complete application with comprehensive testing throughout the semester. See [Team Project Guidelines](./team-project/README.md).

- **7 Milestones**: Delivered incrementally throughout the semester
- **Automated Testing**: Same GitHub Actions workflow
- **Submission**: Team PR links to Canvas

## 📅 Course Timeline

See [TIMELINE.md](./TIMELINE.md) for the detailed weekly schedule.

## 🚀 Getting Started

### Prerequisites

- Basic programming knowledge in Python and JavaScript
- Git installed on your computer
- Code editor (VS Code recommended)
- GitHub account
- Python 3.9 or higher
- Node.js 18 or higher

### Setup Instructions

1. **Clone this repository**

   ```bash
   git clone https://github.com/jp-garduno/software-testing-fall-2026.git
   cd software-testing-fall-2026
   ```

2. **Set up Python environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up JavaScript/Node.js environment**

   ```bash
   npm install
   ```

4. **Install pre-commit hooks**

   ```bash
   pre-commit install
   ```

5. **Verify setup**

   ```bash
   # Python
   pytest --version
   pylint --version

   # JavaScript
   npm test -- --version
   npx eslint --version

   # Pre-commit
   pre-commit run --all-files
   ```

### CI/CD with GitHub Actions

This repository uses **GitHub Actions** for automated testing and validation:

- ✅ **Automated tests** run on every push and PR
- ✅ **Code quality checks** (linting, formatting)
- ✅ **Coverage reports** generated automatically
- ✅ **Student submissions** validated automatically

See [GitHub Actions Documentation](.github/README.md) for details.

## 📚 Resources

- [Course Resources](./resources/) - Additional reading materials, cheat sheets, and references
- [Conventional Commits](https://www.conventionalcommits.org/) - Commit message standard used in this course

## 🤝 Contributing

All commits in this repository follow the [Conventional Commits specification](https://www.conventionalcommits.org/en/v1.0.0/#specification).

### Commit Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Example**:

```
feat(black-box): add boundary value analysis exercises
test(white-box): add coverage tests for calculator module
docs(readme): update setup instructions
```

## 💡 Getting Help

- **GitHub Discussions**: Course Q&A and discussions
- **Issues**: Report bugs or problems with course materials
- **Office Hours**: Weekly office hours (schedule in Canvas)
- **Email**: For private concerns
- **Team**: Collaborate with your project team

## 📖 Important Documents

- **[Student Submission Guide](./docs/student/STUDENT_SUBMISSION_GUIDE.md)** - How to submit assignments
- **[Timeline](./TIMELINE.md)** - Complete 16-week schedule
- **[Contributing Guide](./CONTRIBUTING.md)** - Git workflow and standards
- **[Repository Structure](./STRUCTURE.md)** - Repository organization
- **[Documentation](./docs/README.md)** - All guides and setup docs
- **[Resources](./resources/README.md)** - Learning materials and references

## 📄 License

This course material is for educational purposes. All rights reserved.

---

**Happy Testing!** 🧪✨
