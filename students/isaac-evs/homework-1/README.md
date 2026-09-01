# Isaac Vazquez — Portfolio

A simple personal portfolio website built as the deliverable for **Homework 1: Git Workflow Practice** in the Software Testing course. The goal of this project isn't the complexity of the site itself, but practicing a real Git branching, committing, and pull-request workflow.

## Technologies Used

- HTML5
- CSS3 (custom properties, flexbox, media queries)
- Vanilla JavaScript (smooth scrolling)

## Git Workflow Documentation

### Branching Strategy

All work happened on a dedicated homework branch, `feat/isaac-evs/homework-1`, created from `main`. Within that branch, the project was broken into short-lived **feature branches**, each merged back with `--no-ff` so the history keeps a record of the work:

| Branch | Purpose |
| --- | --- |
| `feature/initial-structure` | Base HTML skeleton, `.gitignore`, and the navigation script |
| `feature/add-styling` | CSS variables, navbar styling, and responsive section/footer layout |
| `feature/add-content` | Real content for the hero, about, projects, contact, and footer sections |
| `feature/add-documentation` | This README and the homework reflection |

Each feature branch was merged into `feat/isaac-evs/homework-1` once its scope was complete, mirroring how the required branches (`feature/initial-structure`, `feature/add-styling`, `feature/add-content`) are described in the homework instructions.

### Commit Message Convention

Commits follow the [Conventional Commits](https://www.conventionalcommits.org/) style used throughout this repository:

```
<type>: <short description>

[optional longer description]
```

Types used in this project: `feat`, `fix`, `style`, `chore`, `docs`. Each commit represents one logical unit of work (e.g., one section of content, one styling concern) rather than bundling unrelated changes together.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/jp-garduno/software-testing-fall-2026.git
   ```
2. Navigate to this directory:
   ```bash
   cd software-testing-fall-2026/students/isaac-evs/homework-1
   ```
3. Open `index.html` in your browser (no build step or dependencies required).

## Lessons Learned

Working through this exercise reinforced how much easier it is to review and revert changes when commits are small and scoped to one idea, and how `--no-ff` merges keep feature branches visible in the history instead of flattening them into `main`.
