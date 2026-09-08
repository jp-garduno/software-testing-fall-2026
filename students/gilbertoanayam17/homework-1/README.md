# Personal Portfolio — Homework 1

A personal portfolio built with plain HTML, CSS and a few lines of
JavaScript for the Software Testing course (Module 1: Git Fundamentals). The
site is intentionally simple: the point of the assignment is the Git workflow,
not the complexity of the project.

## Technologies Used

- HTML5 (semantic markup)
- CSS3 (custom properties, flexbox, grid, one media query)
- Vanilla JavaScript (no frameworks, no build step)
- Git & GitHub (branches, pull requests, code review)

## Git Workflow Documentation

### Branching strategy

I used a **feature branch workflow** on top of a single integration branch.
`feat/gilbertoanayam17/homework-1` is the submission branch created from `main`;
every unit of work got its own short-lived branch created from it, was pushed to
GitHub, reviewed in a pull request and rebased back onto it. Because
`main` in this course repository is shared by everyone, the practice pull
requests target my submission branch instead of `main`, and a single final pull
request takes the whole homework into `main`.

### Branches

| Branch                                       | Purpose                                   |
| -------------------------------------------- | ----------------------------------------- |
| `feat/gilbertoanayam17/homework-1`           | Integration branch for the whole homework |
| `feature/gilbertoanayam17/initial-structure` | HTML skeleton and initial README          |
| `feature/gilbertoanayam17/add-styling`       | Stylesheet and responsive layout          |
| `fix/gilbertoanayam17/nav-and-title-typos`   | Fix for a broken anchor and a title typo  |
| `feature/gilbertoanayam17/add-content`       | Projects, contact and footer script       |

Branches names excluding homework-1 (which follows the instructions convention) follow `<type>/<username>/<short-description>` convention. The username is in the middle on purpose because the course repository already had branches called `feature/add-styling` and `feature/add-content` from other classmates, so I followed that convention.

### Commit message convention

Conventional Commits: `<type>(<scope>): <subject>` in the imperative mood, with
an optional body listing the details.

- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation
- `style:` formatting or visual changes with no logic change
- `refactor:` restructuring with no change in behaviour
- `chore:` maintenance (scaffolding, `.gitignore`)

## Setup Instructions

```bash
git clone https://github.com/jp-garduno/software-testing-fall-2026.git
cd software-testing-fall-2026/students/gilbertoanayam17/homework-1
```

Then open `index.html` in any browser, there is nothing to install or build.

## Lessons Learned about Git

- A commit message is documentation for your future self. `git log --oneline`
  should read like a changelog.
- `git commit --amend` is only safe before pushing.
- `git status` before every `git add` catches files that should never be
  committed.
