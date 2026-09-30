# Homework 1 — Git Workflow Practice

Personal portfolio website for **Pablo Portillo Madera**, built as the Homework 1
deliverable for the Software Testing course (Fall 2026). The site presents my CV
as a modern, single-page portfolio — my role, experience at Kadu Care, projects,
skills, and education.

## 🎨 Design

The visual language is inspired by the **Kadu Care** product UI: clean medical /
SaaS aesthetic, generous whitespace, soft blue accents, subtle shadows, and
`shadcn/ui`-style rounded cards. Typography uses **Inter** for a modern,
readable feel.

## 🛠 Technologies Used

- HTML5 (semantic markup)
- CSS3 (custom properties, grid, flexbox, responsive breakpoints)
- Google Fonts — Inter
- Git & GitHub for version control

No build step required — the page is fully static.

## 🚀 Setup / How to Run

Clone the repository and open the page in a browser:

```bash
git clone https://github.com/jp-garduno/software-testing-fall-2026.git
cd software-testing-fall-2026/students/pabloportillo1/homework-1
open index.html    # macOS
# or simply drag index.html into your browser
```

For a local dev server (optional):

```bash
python3 -m http.server 8080
# then open http://localhost:8080
```

## 🌿 Git Workflow

### Branching strategy

Feature-branch workflow: `main` is always deployable; each unit of work happens
on a short-lived branch and is merged back via PR.

Branches used for this assignment:

- `feat/pabloportillo1/homework-1` — main submission branch
- `feature/initial-structure` — HTML scaffolding
- `feature/add-styling` — Kadu-Care-inspired CSS
- `feature/add-content` — CV content, sections, links

### Commit message convention

Conventional Commits format:

```
<type>: <short description>

[optional body]
```

Types used: `feat`, `docs`, `style`, `fix`, `refactor`.

Examples:

- `feat: scaffold portfolio HTML structure`
- `feat: add Kadu-Care inspired styling`
- `docs: add README with workflow documentation`

## 📁 Files

```
students/pabloportillo1/homework-1/
├── index.html       # Portfolio page markup
├── styles.css       # Kadu-Care inspired styling
├── README.md        # This file
├── REFLECTION.md    # Reflection on the Git workflow
└── .gitignore
```

## ✅ Deliverables Checklist

- [x] Feature branch created from `main`
- [x] Portfolio site (HTML + CSS)
- [x] `.gitignore`
- [x] `README.md` with workflow documentation
- [x] `REFLECTION.md` with 200–300 word reflection
- [x] Multiple conventional commits
- [x] Pull request opened against `main` with `homework` label
