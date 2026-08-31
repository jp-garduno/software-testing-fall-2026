# Vittorio Catino — Git Workflow Portfolio

A responsive personal portfolio created for Homework 1: Git Workflow Practice. The project intentionally stays small so that the Git workflow, focused commits, documentation, and review process remain the central learning goals.

## Technologies used

- HTML5 for semantic page structure
- CSS3 for responsive layout and visual design
- Vanilla JavaScript for rendering project cards

## Run locally

1. Clone this repository.
2. Open `students/vittoriocatino/homework-1/index.html` in any modern browser.
3. No packages, build process, or server are required.

## Git workflow

I used a feature-branch workflow. Each focused area started from `main`, was developed in a descriptive feature branch, and contains small conventional commits. The branches created for this project are:

- `feature/portfolio-structure` — page markup, ignore rules, and project-card script
- `feature/portfolio-styling` — design tokens, layout, responsive cards, and call to action
- `feature/portfolio-documentation` — project documentation and reflection
- `feat/vittoriocatino/homework-1` — final submission branch

Commit messages follow the conventional format `<type>(homework-1): <description>`. I used `feat`, `style`, `docs`, and `chore` to make each commit’s purpose visible in the history. The final submission brings the completed feature work together for a pull request into `main`.
