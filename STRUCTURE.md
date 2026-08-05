# Repository Structure

## 📁 Clean, Organized Layout

```
software-testing-fall-2026/
├── 📄 README.md                    # Course overview & getting started
├── 📄 CONTRIBUTING.md              # Git workflow & standards
├── 📄 TIMELINE.md                  # 16-week schedule
│
├── 📂 docs/                        # 📚 All documentation
│   ├── README.md                   # Documentation index
│   ├── instructor/                 # 👨‍🏫 For instructors
│   │   ├── CANVAS_INTEGRATION.md   # Canvas LMS setup
│   │   └── CANVAS_GRADING_COMPLETE.md
│   ├── student/                    # 👨‍🎓 For students
│   │   └── STUDENT_SUBMISSION_GUIDE.md
│   └── setup/                      # ⚙️ Setup & maintenance
│       ├── GITHUB_ACTIONS_SETUP.md
│       ├── SETUP_COMPLETE.md
│       └── REPOSITORY_AUDIT.md
│
├── 📂 resources/                   # Learning materials
│   └── README.md                   # Books, courses, tools, etc.
│
├── 📂 01-git/                      # Module 1
│   ├── README.md
│   ├── theory/
│   ├── exercises/
│   └── homework/
│
├── 📂 02-testing-concepts/         # Module 2
│   ├── README.md
│   ├── theory/
│   ├── exercises/
│   └── homework/
│
├── 📂 03-static-testing/           # Module 3
│   ├── README.md
│   ├── theory/
│   ├── exercises/
│   └── homework/
│
├── 📂 04-black-box-testing/        # Module 4 ✅
│   ├── README.md
│   ├── theory/
│   ├── exercises/
│   └── homework/
│
├── 📂 05-white-box-testing/        # Module 5 ✅
│   ├── README.md
│   ├── theory/
│   ├── exercises/
│   │   ├── python/
│   │   └── javascript/
│   └── homework/
│
├── 📂 06-test-driven-development/  # Module 6 ✅
│   ├── README.md
│   ├── theory/
│   ├── exercises/
│   └── homework/
│
├── 📂 07-data-driven-testing/      # Module 7 ✅
│   ├── README.md
│   ├── theory/
│   ├── exercises/
│   │   ├── python/
│   │   └── javascript/
│   └── homework/
│
├── 📂 08-system-level-testing/     # Module 8 ✅
│   ├── README.md
│   ├── theory/
│   ├── exercises/
│   └── homework/
│
├── 📂 09-performance-testing/      # Module 9 ✅
│   ├── README.md
│   ├── theory/
│   ├── exercises/
│   └── homework/
│
├── 📂 exams/                       # Exam specifications (pending)
├── 📂 team-project/                # Team project guidelines (pending)
│
├── 📂 .github/                     # GitHub configuration
│   ├── workflows/                  # CI/CD automation
│   │   ├── ci.yml
│   │   ├── grading-automation.yml  # 🔥 Automated grading
│   │   ├── student-submission.yml
│   │   └── homework-checker.yml
│   ├── ISSUE_TEMPLATE/
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── README.md
│
├── 📂 .claude/                     # AI assistance context
│   ├── CLAUDE.md
│   └── commands.md
│
├── 📄 .pre-commit-config.yaml      # Pre-commit hooks
├── 📄 requirements.txt             # Python dependencies
├── 📄 package.json                 # JavaScript dependencies
└── 📄 .gitignore
```

## 🎯 Key Improvements

### Before

```
Root had 9+ markdown files mixed together:
- Student guides
- Instructor guides
- Setup documentation
- Course materials
```

### After

```
Root now has only 3 essential files:
✅ README.md - Course overview
✅ CONTRIBUTING.md - Git standards
✅ TIMELINE.md - Schedule

Everything else organized in docs/:
📁 docs/instructor/ - Instructor-only docs
📁 docs/student/ - Student guides
📁 docs/setup/ - Technical setup
```

## 📍 Quick Navigation

### For Students

- Start: [README.md](README.md)
- Submit homework: [docs/student/STUDENT_SUBMISSION_GUIDE.md](docs/student/STUDENT_SUBMISSION_GUIDE.md)
- Schedule: [TIMELINE.md](TIMELINE.md)
- Resources: [resources/README.md](resources/README.md)

### For Instructors

- Canvas setup: [docs/instructor/CANVAS_INTEGRATION.md](docs/instructor/CANVAS_INTEGRATION.md)
- Grading: [docs/instructor/CANVAS_GRADING_COMPLETE.md](docs/instructor/CANVAS_GRADING_COMPLETE.md)

### For Maintainers

- Setup checklist: [docs/setup/SETUP_COMPLETE.md](docs/setup/SETUP_COMPLETE.md)
- Audit report: [docs/setup/REPOSITORY_AUDIT.md](docs/setup/REPOSITORY_AUDIT.md)
- GitHub Actions: [docs/setup/GITHUB_ACTIONS_SETUP.md](docs/setup/GITHUB_ACTIONS_SETUP.md)

---

**Much cleaner!** 🎉
