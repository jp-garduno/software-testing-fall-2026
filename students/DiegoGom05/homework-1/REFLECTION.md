# Reflection - Git Workflow Practice

## Challenges Faced
During the development of this homework, one of the main challenges was maintaining a clean commit history and adhering strictly to the Conventional Commits specification (`feat:`, `style:`, `docs:`, `refactor:`). It required deliberate planning to break down changes into small, logical units rather than staging large chunks of code at once. Additionally, managing local branch switches and ensuring that feature branches merged cleanly into the primary submission branch (`feat/DiegoGom05/homework-1`) required constant verification using `git status` and `git log`.

## Most Useful Git Commands
Throughout the assignment, the most valuable commands were:
- `git checkout -b <branch-name>`: Allowed quick creation and context switching between isolated feature branches.
- `git log --oneline`: Provided a concise visual summary of the commit history to verify that commit messages were descriptive before merging.
- `git merge`: Facilitated combining isolated features back into the primary submission branch once milestone work was completed.

## Application to Team Projects
This workflow is directly applicable to collaborative software development. Using a Feature Branch Strategy prevents team members from committing directly to the main branch, reducing code collisions. Writing standardized commit messages allows team members to easily track why changes were introduced, and using Pull Requests ensures structured code reviews.

## Branching Strategy & Merged Branches
- `feature/initial-structure`: Created basic HTML layout and semantic containers. (Merged into main branch)
- `feature/add-content`: Populated technical stack, projects, contact info, and documentation. (Merged into main branch)
- `feature/add-styling`: Applied global CSS reset, card design, responsive layout, and reflection notes. (Merged into main branch)

## Simulated / Internal Pull Requests
1. **PR #1 (feature/initial-structure):** *Title:* "feat: add base HTML structure" — Integrated initial markup into main submission branch.
2. **PR #2 (feature/add-content):** *Title:* "feat: populate tech stack and project showcase" — Added personal information and project cards.
3. **PR #3 (feature/add-styling):** *Title:* "style: implement CSS styling and responsive grid" — Finalized responsive CSS layout and project documentation.

## Commit History Summary
1. `feat: add boilerplate HTML structure and hero section`
2. `feat: add about me and education sections layout`
3. `feat: include containers for tech stack and projects showcase`
4. `feat: populate tech stack with languages, backend and tools`
5. `feat: add project cards for java calculator, c tic-tac-toe and e-commerce`
6. `feat: add social links and contact section`
7. `docs: add initial project README with portfolio overview`
8. `style: add global reset and hero section css styles`
9. `style: define responsive grid layout for projects and stack cards`
10. `docs: add REFLECTION.md detailing git branching strategy and learnings`
11. `refactor: clean up HTML comments and format CSS rules`