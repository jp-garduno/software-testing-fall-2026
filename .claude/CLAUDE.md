# Software Testing Course - Fall 2026

## Project Context

This is a university-level Software Testing course repository. The course runs for 16 weeks with a mix of asynchronous (weeks 1-3) and in-person (weeks 4-16) instruction.

## Repository Structure

### Modules (9 total)

1. **Git** - Version control fundamentals
2. **Testing Concepts** - Types, levels, principles
3. **Static Testing** - Pre-commit, linting, conventional commits
4. **Black Box Testing** - EP, BVA, decision tables, state transition
5. **White Box Testing** - Coverage, unit tests, mocking
6. **TDD** - Test-driven development
7. **Data-Driven Testing** - Parameterized tests
8. **System Testing** - BDD, Selenium, Playwright
9. **Performance Testing** - JMeter, load testing

### Key Directories

- `0X-module-name/` - Each module has theory/, exercises/, homework/ subdirectories
- `exams/` - Three practical exams throughout semester
- `team-project/` - Semester-long team project (4-5 students)
- `resources/` - Additional learning materials
- `.github/workflows/` - CI/CD automation

## Technologies

### Languages

- **Python** (3.11+) - Primary language for testing examples
- **JavaScript/TypeScript** (Node 22+) - Secondary language

### Testing Frameworks

- Python: pytest, behave, selenium, playwright
- JavaScript: Jest, Playwright, Selenium WebDriver

### Code Quality

- Python: black, isort, pylint
- JavaScript: ESLint, Prettier
- Pre-commit hooks for both

## Coding Standards

### Commit Messages

Follow Conventional Commits specification:

```
<type>(<scope>): <description>

[optional body]
```

Types: feat, fix, docs, style, refactor, test, chore

### Python Style

- PEP 8 compliant
- Line length: 120 characters
- Black formatter
- Type hints encouraged
- Docstrings for public functions

### JavaScript Style

- Airbnb style guide
- ESLint + Prettier
- Modern ES6+ syntax
- JSDoc for public functions

## Common Tasks

### Adding a New Exercise

1. Create exercise file in appropriate module's `exercises/` directory
2. Include both Python and JavaScript versions if applicable
3. Add solution in separate `solutions/` subdirectory
4. Update module README with exercise link
5. Add corresponding tests

### Adding Theory Content

1. Create markdown file in module's `theory/` directory
2. Use clear headings and examples
3. Include code snippets in both languages
4. Add diagrams using Mermaid when helpful
5. Update module README

### Creating Homework Assignment

1. Create homework-X.md in module's `homework/` directory
2. Include: objectives, requirements, deliverables, rubric
3. Estimate time (typically 3-5 hours)
4. Provide starter code/templates if needed
5. Link from module README and TIMELINE.md

## Testing Guidelines

### When Writing Tests

- Arrange-Act-Assert pattern
- One assertion per test when possible
- Clear test names: `test_<what>_<condition>_<expected>`
- Use fixtures for setup/teardown
- Mock external dependencies

### Coverage Goals

- Minimum: 70% for exercises
- Homework: 80%
- Team project: 80%+

## Course Timeline

- **Weeks 1-3**: Async (Git, Concepts, Static Testing)
- **Week 6**: Exam 1 (Modules 1-3)
- **Week 11**: Exam 2 (Modules 4-6)
- **Week 16**: Exam 3 (Modules 7-9) + Final presentations

## Important Notes

### For Content Creation

- All content should be beginner-friendly but comprehensive
- Include both theoretical explanations and practical examples
- Use real-world scenarios students can relate to
- Provide solutions but encourage students to try first
- GitHub Copilot is available to students

### For Automation (GitHub Actions)

- CI/CD runs on all PRs and pushes
- Validates code style, tests, coverage
- Student submissions get automated feedback
- Pre-commit hooks must pass before commit

### For Assessment

- 3 practical exams (not theory/multiple choice)
- 9 homework assignments (one per module)
- Team project with 7 milestones
- All grading rubrics included in assignment files

## Common Patterns

### Module README Structure

```markdown
# Module X: Title

- Learning Objectives
- Theory Materials
- Exercises
- Homework Assignment
- Tools Required
- Self-Assessment Checklist
- Next Steps
```

### Exercise File Structure

```markdown
# Exercise: Title

- Requirement description
- Input/output examples
- Constraints
- Starter code (both Python and JS)
- Hints
- Expected outcome
```

## File Naming Conventions

- Module directories: `0X-module-name/`
- Theory files: `01-topic-name.md`
- Exercises: `01-descriptive-name.md`
- Homework: `homework-X.md`
- Tests: `test_*.py` or `*.test.js`

## Student Workflow

1. Clone repository
2. Create feature branch: `feat/homework-X` or `feat/module-X-exercise`
3. Complete work
4. Run tests locally
5. Commit with conventional commits
6. Push and create PR
7. CI/CD runs automated checks
8. Instructor reviews and provides feedback

## Resources Location

- Course materials: Each module's theory/ directory
- External resources: resources/README.md
- Code examples: Each module's exercises/ directory
- Reference implementations: solutions/ subdirectories (when present)

## Maintenance Notes

- Update TIMELINE.md if schedule changes
- Keep requirements.txt and package.json in sync with new dependencies
- Test all exercises in both Python and JavaScript
- Update CI/CD workflows if new checks needed
- Archive old semester repositories (don't delete)

## Contact

For questions about this repository structure or course design, refer to CONTRIBUTING.md or open an issue.
